"""CLI helpers for documentation: inject project ID and export to docx."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def inject_project_id(
    source_dir: Path,
    output_dir: Path,
    project_id: str,
    bucket_prefix: str = "bq-studio-demo",
) -> list[Path]:
    """Copy doc tree to output_dir, replacing project/bucket placeholders in .md files.

    Replacements (order matters):
    - gs://bq-studio-demo-YOUR_PROJECT / gs://bq-studio-demo-<project_id> -> gs://{bucket_prefix}-{project_id}
    - bq-studio-demo-YOUR_PROJECT / bq-studio-demo-<project_id> -> {bucket_prefix}-{project_id}
    - YOUR_DEMO_BUCKET -> {bucket_prefix}-{project_id}
    - YOUR_PROJECT_ID, YOUR_PROJECT -> project_id
    - <project_id> -> project_id

    Returns the list of written .md file paths (under output_dir).
    """
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()
    bucket_name = f"{bucket_prefix}-{project_id}".replace("_", "-").lower()
    written: list[Path] = []

    # Order: most specific first so we don't double-replace
    replacements = [
        ("gs://bq-studio-demo-YOUR_PROJECT", f"gs://{bucket_name}"),
        ("gs://bq-studio-demo-<project_id>", f"gs://{bucket_name}"),
        ("bq-studio-demo-YOUR_PROJECT", bucket_name),
        ("bq-studio-demo-<project_id>", bucket_name),
        ("YOUR_DEMO_BUCKET", bucket_name),
        ("YOUR_PROJECT_ID", project_id),
        ("YOUR_PROJECT", project_id),
        ("<project_id>", project_id),
    ]

    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(source_dir)
        dest = output_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == ".md":
            text = path.read_text(encoding="utf-8", errors="replace")
            for old, new in replacements:
                text = text.replace(old, new)
            dest.write_text(text, encoding="utf-8")
            written.append(dest)
        else:
            shutil.copy2(path, dest)

    return written


def export_docs_to_docx(source_dir: Path, output_dir: Path) -> list[Path]:
    """Export doc/ to doc_export/ mirroring structure: one .docx per .md file.

    Recursively finds every .md under source_dir and converts it to .docx under output_dir
    with the same relative path (e.g. doc/features/1-studio/foo.md → doc_export/features/1-studio/foo.docx).

    Requires pandoc on PATH. Returns the list of created .docx paths.
    """
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    try:
        subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(
            "pandoc is required for docx export. Install it (e.g. apt install pandoc, "
            "brew install pandoc, or https://pandoc.org/installing.html), then run again."
        ) from e

    def run_pandoc(md_path: Path, docx_path: Path, timeout: int = 60) -> None:
        md_path = md_path.resolve()
        docx_path = docx_path.resolve()
        docx_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "pandoc",
            "-f", "markdown",
            "-t", "docx",
            "-o", str(docx_path),
            str(md_path),
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(
                f"pandoc timed out after {timeout}s converting {md_path}"
            ) from e
        if result.returncode != 0:
            raise RuntimeError(
                f"pandoc failed for {md_path}: {result.stderr or result.stdout}"
            )

    for md_path in sorted(source_dir.rglob("*.md")):
        rel = md_path.relative_to(source_dir)
        docx_path = output_dir / rel.with_suffix(".docx")
        print(f"  {rel} → {docx_path.relative_to(output_dir)}")
        run_pandoc(md_path, docx_path)
        created.append(docx_path)

    return created
