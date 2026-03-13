#!/usr/bin/env python3
"""
Upload local SQL and/or notebook files into BigQuery Studio by automating the Studio UI.

Google does not provide an API that creates saved queries or notebooks visible in Studio.
This script uses browser automation (Playwright) to perform the same "Upload SQL query"
and "Upload to Notebooks" flows you would do manually.

Requires: pip install playwright && playwright install chromium

Usage:
  # Upload SQL and notebooks (default)
  python scripts/upload_queries_to_studio.py --project-id MY_PROJECT

  # SQL only
  python scripts/upload_queries_to_studio.py --project-id MY_PROJECT --no-notebooks

  # Notebooks only
  python scripts/upload_queries_to_studio.py --project-id MY_PROJECT --no-sql

  # Custom dirs and region
  python scripts/upload_queries_to_studio.py --project-id MY_PROJECT --sql-dir bq_studio_demos/sql --notebooks-dir bq_studio_demos/notebooks --region EU
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _open_upload_dialog(page, kind: str, timeout: float) -> bool:
    """Open the Upload dialog: kind is 'sql' or 'notebook'."""
    if kind == "sql":
        menu_label = "Queries"
        item_text = "Upload SQL query"
    else:
        menu_label = "Notebooks"
        item_text = "Upload to Notebooks"
    try:
        upload_btn = page.get_by_role("button", name=item_text)
        if upload_btn.count() == 0:
            upload_btn = page.get_by_text(item_text)
        if upload_btn.count() > 0:
            upload_btn.first.click()
            return True
        page.get_by_text(menu_label).first.wait_for(state="visible", timeout=timeout)
        menu_btn = page.locator('[aria-label="View actions"]').first
        if menu_btn.count() == 0:
            menu_btn = page.get_by_label("View actions").first
        if menu_btn.count() > 0:
            menu_btn.click()
            page.get_by_role("menuitem", name=item_text).click()
            return True
        raise RuntimeError(f"Could not find 'View actions' or '{item_text}'")
    except Exception as e:
        print(f"  Could not open upload dialog: {e}.", file=sys.stderr)
        return False


def _do_upload(
    page,
    file_path: Path,
    region: str,
    name_placeholder_hint: str,
    timeout: float,
) -> None:
    """Fill the Upload dialog (file, name, region) and click Upload."""
    page.wait_for_timeout(1500)
    file_input = page.locator('input[type="file"]').first
    if file_input.count() > 0:
        file_input.set_input_files(str(file_path))
    else:
        with page.expect_file_chooser() as fc_info:
            browse = page.get_by_role("button", name="Browse")
            if browse.count() == 0:
                browse = page.get_by_text("Browse").first
            browse.click()
        fc_info.value.set_files(str(file_path))
    name_from_file = file_path.stem
    name_field = page.locator(
        f'input[aria-label*="name"], input[placeholder*="name"], input[aria-label*="{name_placeholder_hint}"]'
    ).first
    if name_field.count() > 0:
        name_field.fill(name_from_file)
    region_select = page.locator('[aria-label*="Region"], label:has-text("Region")').first
    if region_select.count() > 0:
        region_select.click()
        page.get_by_text(region, exact=True).click()
    upload_submit = page.get_by_role("button", name="Upload")
    if upload_submit.count() == 0:
        upload_submit = page.get_by_text("Upload").first
    upload_submit.click()
    page.wait_for_timeout(2000)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload SQL and/or notebook files into BigQuery Studio via browser automation."
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="GCP project ID (must match the project in BigQuery Studio).",
    )
    parser.add_argument(
        "--sql-dir",
        type=Path,
        default=Path("bq_studio_demos/sql"),
        help="Directory containing .sql files to upload (default: bq_studio_demos/sql).",
    )
    parser.add_argument(
        "--notebooks-dir",
        type=Path,
        default=Path("bq_studio_demos/notebooks"),
        help="Directory containing .ipynb files to upload (default: bq_studio_demos/notebooks).",
    )
    parser.add_argument(
        "--no-sql",
        action="store_true",
        help="Do not upload SQL files.",
    )
    parser.add_argument(
        "--no-notebooks",
        action="store_true",
        help="Do not upload notebooks.",
    )
    parser.add_argument(
        "--region",
        default="US",
        help="BigQuery region for saved queries and notebooks (default: US).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (you must be already logged in).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60_000,
        help="Timeout in ms for page actions (default: 60000).",
    )
    args = parser.parse_args()

    upload_sql = not args.no_sql
    upload_notebooks = not args.no_notebooks
    if not upload_sql and not upload_notebooks:
        print("Error: use at least one of --no-sql or --no-notebooks; or omit both to upload SQL and notebooks.", file=sys.stderr)
        return 1

    sql_files: list[Path] = []
    if upload_sql:
        sql_dir = args.sql_dir.resolve()
        if not sql_dir.is_dir():
            print(f"Error: SQL directory not found: {sql_dir}", file=sys.stderr)
            return 1
        sql_files = sorted(sql_dir.glob("*.sql"))

    notebook_files: list[Path] = []
    if upload_notebooks:
        nb_dir = args.notebooks_dir.resolve()
        if not nb_dir.is_dir():
            print(f"Error: Notebooks directory not found: {nb_dir}", file=sys.stderr)
            return 1
        notebook_files = sorted(nb_dir.glob("*.ipynb"))

    if not sql_files and not notebook_files:
        print("Error: no .sql or .ipynb files to upload. Run 'bqdemo deploy demos' first.", file=sys.stderr)
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright is required. Install with: pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        return 1

    url = f"https://console.cloud.google.com/bigquery?project={args.project_id}"
    timeout = args.timeout

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(accept_downloads=True)
        context.set_default_timeout(timeout)
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle", timeout=timeout)

            if "accounts.google.com" in page.url:
                print(
                    "Please sign in to Google Cloud in the browser window. When BigQuery Studio is visible, press Enter here to continue."
                )
                input()

            # Upload SQL files
            for i, sql_path in enumerate(sql_files):
                print(f"Uploading SQL ({i + 1}/{len(sql_files)}): {sql_path.name}")
                if not _open_upload_dialog(page, "sql", timeout):
                    print("  Open Queries → View actions → Upload SQL query and re-run if needed.", file=sys.stderr)
                    break
                _do_upload(page, sql_path, args.region, "SQL name", timeout)

            # Upload notebook files
            for i, nb_path in enumerate(notebook_files):
                print(f"Uploading notebook ({i + 1}/{len(notebook_files)}): {nb_path.name}")
                if not _open_upload_dialog(page, "notebook", timeout):
                    print("  Open Notebooks → View actions → Upload to Notebooks and re-run if needed.", file=sys.stderr)
                    break
                _do_upload(page, nb_path, args.region, "Notebook name", timeout)

            print("Done.")
        finally:
            if not args.headless:
                print("Close the browser window when finished.")
                page.wait_for_timeout(300_000)
            browser.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
