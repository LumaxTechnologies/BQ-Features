"""BigQuery Studio features demo CLI."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import click
import yaml

from bq_features import __version__


def load_config(config_path: str | None) -> dict:
    """Load YAML config from path or default locations."""
    paths = []
    if config_path:
        paths.append(Path(config_path))
    paths.extend([
        Path("bq_features_config.yaml"),
        Path(os.environ.get("BQ_FEATURES_CONFIG", "")),
        Path(__file__).resolve().parent.parent.parent / "bq_features_config.yaml",
    ])
    for p in paths:
        if p and p.is_file():
            with open(p) as f:
                return yaml.safe_load(f) or {}
    return {}


def get_project_id(config: dict) -> str | None:
    """Get project ID from config or GOOGLE_CLOUD_PROJECT."""
    return config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")


@click.group()
@click.option(
    "--config",
    "-c",
    "config_path",
    type=click.Path(exists=True),
    default=None,
    help="Path to YAML config file.",
)
@click.pass_context
def main(ctx: click.Context, config_path: str | None) -> None:
    """Deploy BigQuery Studio demo infrastructure and finance-oriented demo material."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config_path)
    ctx.obj["config_path"] = config_path


@main.command()
def version() -> None:
    """Show version."""
    click.echo(__version__)


@main.command()
def examples() -> None:
    """Print example commands for deploy infra, demos, and using data canvas / data preparations / pipelines."""
    click.echo("CLI examples (see README for full context)")
    click.echo("")
    click.echo("# Minimal: infra + demos, no schedulers or Looker")
    click.echo("  bqdemo deploy infra")
    click.echo("  bqdemo deploy demos --no-schedulers --no-looker")
    click.echo("")
    click.echo("# Full demo with scheduled queries and Looker")
    click.echo("  bqdemo deploy infra")
    click.echo("  bqdemo deploy demos --with-schedulers --with-looker")
    click.echo("")
    click.echo("# Custom region and prefixes")
    click.echo("  bqdemo deploy infra --region EU --dataset-prefix my_demo --bucket-prefix my-bq-demo")
    click.echo("  bqdemo deploy demos --dataset-prefix my_demo --bucket-prefix my-bq-demo")
    click.echo("")
    click.echo("# Your own CSV data (table name = filename without .csv)")
    click.echo("  bqdemo deploy infra")
    click.echo("  bqdemo deploy demos --csv-dir /path/to/csv/files --no-demo-data")
    click.echo("")
    click.echo("# Generate demos locally only (no GCS upload)")
    click.echo("  bqdemo deploy demos --no-upload-to-gcs -o ./my_demos")


@main.group()
@click.pass_context
def deploy(ctx: click.Context) -> None:
    """Deploy infrastructure or demo material."""
    pass


@deploy.command("infra")
@click.option(
    "--project-id",
    envvar="GOOGLE_CLOUD_PROJECT",
    help="GCP project ID (overrides config).",
)
@click.option(
    "--region",
    default="US",
    help="BigQuery dataset region (e.g. US, EU).",
)
@click.option(
    "--bucket-prefix",
    default="bq-studio-demo",
    help="Prefix for GCS bucket name (full name: {prefix}-{project_id}).",
)
@click.option(
    "--dataset-prefix",
    default="bq_studio_demo",
    help="Prefix for BigQuery dataset IDs.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Print what would be created without making changes.",
)
@click.pass_context
def deploy_infra(
    ctx: click.Context,
    project_id: str | None,
    region: str,
    bucket_prefix: str,
    dataset_prefix: str,
    dry_run: bool,
) -> None:
    """Deploy BigQuery datasets and GCS bucket only. Load demo data with 'bqdemo deploy demos'."""
    from bq_features.deploy.infra import run_deploy_infra

    config = ctx.obj["config"]
    pid = project_id or get_project_id(config)
    if not pid:
        raise click.UsageError(
            "Set project_id in config (bq_features_config.yaml) or pass --project-id / GOOGLE_CLOUD_PROJECT"
        )

    run_deploy_infra(
        project_id=pid,
        region=region,
        bucket_prefix=bucket_prefix,
        dataset_prefix=dataset_prefix,
        dry_run=dry_run,
        config=config,
    )


@deploy.command("demos")
@click.option(
    "--project-id",
    envvar="GOOGLE_CLOUD_PROJECT",
    help="GCP project ID (overrides config).",
)
@click.option(
    "--region",
    default="US",
    help="BigQuery region (must match infra).",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("bq_studio_demos"),
    help="Directory to write notebooks, SQL, and docs (for manual import into BigQuery Studio).",
)
@click.option(
    "--with-schedulers/--no-schedulers",
    "with_schedulers",
    default=True,
    help="Create and enable scheduled transformation tasks (scheduled queries).",
)
@click.option(
    "--with-looker/--no-looker",
    "with_looker",
    default=False,
    help="Generate Looker dashboard instructions and optional LookML snippets.",
)
@click.option(
    "--upload-to-gcs/--no-upload-to-gcs",
    "upload_to_gcs",
    default=None,
    help="Upload SQL, notebooks, and docs to the demo GCS bucket (default: on, or demos.upload_to_gcs in config).",
)
@click.option(
    "--with-demo-data/--no-demo-data",
    "with_demo_data",
    default=True,
    help="Load bundled finance demo data into BigQuery and GCS (demo_data/).",
)
@click.option(
    "--deploy-dataform/--no-deploy-dataform",
    "deploy_dataform",
    default=True,
    help="Create Dataform demo-workspace (if missing) and deploy .sqlx files into it.",
)
@click.option(
    "--csv-dir",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Directory of CSV files to load instead of bundled demo (table name = filename without .csv).",
)
@click.option(
    "--dataset-prefix",
    default="bq_studio_demo",
    help="BigQuery dataset prefix (must match infra).",
)
@click.option(
    "--bucket-prefix",
    default="bq-studio-demo",
    help="GCS bucket prefix (must match infra).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Print what would be created without making changes.",
)
@click.pass_context
def deploy_demos(
    ctx: click.Context,
    project_id: str | None,
    region: str,
    output_dir: Path,
    with_schedulers: bool,
    with_looker: bool,
    upload_to_gcs: bool,
    with_demo_data: bool,
    deploy_dataform: bool,
    csv_dir: Path | None,
    dataset_prefix: str,
    bucket_prefix: str,
    dry_run: bool,
) -> None:
    """Deploy BQ Studio demo material: notebooks, SQL, docs, demo data (BQ + GCS), optional Looker and schedulers."""
    from bq_features.deploy.demos import run_deploy_demos

    config = ctx.obj["config"]
    pid = project_id or get_project_id(config)
    if not pid:
        raise click.UsageError(
            "Set project_id in config or pass --project-id / GOOGLE_CLOUD_PROJECT"
        )

    if upload_to_gcs is None:
        upload_to_gcs = config.get("demos", {}).get("upload_to_gcs", True)

    run_deploy_demos(
        project_id=pid,
        region=region,
        output_dir=output_dir,
        with_schedulers=with_schedulers,
        with_looker=with_looker,
        upload_to_gcs=upload_to_gcs,
        with_demo_data=with_demo_data,
        deploy_dataform=deploy_dataform,
        csv_dir=csv_dir,
        dataset_prefix=dataset_prefix,
        bucket_prefix=bucket_prefix,
        dry_run=dry_run,
        config=config,
    )


@main.command("upload-to-studio")
@click.option(
    "--project-id",
    envvar="GOOGLE_CLOUD_PROJECT",
    help="GCP project ID (overrides config).",
)
@click.option(
    "--sql-dir",
    type=click.Path(path_type=Path),
    default=Path("bq_studio_demos/sql"),
    help="Directory containing .sql files to upload.",
)
@click.option(
    "--notebooks-dir",
    type=click.Path(path_type=Path),
    default=Path("bq_studio_demos/notebooks"),
    help="Directory containing .ipynb files to upload.",
)
@click.option(
    "--no-sql",
    is_flag=True,
    help="Do not upload SQL files (only notebooks).",
)
@click.option(
    "--no-notebooks",
    is_flag=True,
    help="Do not upload notebooks (only SQL).",
)
@click.option(
    "--region",
    default="US",
    help="BigQuery region for saved queries and notebooks.",
)
@click.option(
    "--headless",
    is_flag=True,
    help="Run browser headless (must be already logged in).",
)
@click.pass_context
def upload_to_studio(
    ctx: click.Context,
    project_id: str | None,
    sql_dir: Path,
    notebooks_dir: Path,
    no_sql: bool,
    no_notebooks: bool,
    region: str,
    headless: bool,
) -> None:
    """Upload SQL and notebooks into BigQuery Studio via browser automation.

    There is no Google API that creates saved queries or notebooks visible in Studio.
    This command runs a Playwright script that automates the same UI flows:
    "Upload SQL query" and "Upload to Notebooks".

    Requires: pip install playwright && playwright install chromium
    """
    config = ctx.obj["config"]
    pid = project_id or get_project_id(config)
    if not pid:
        raise click.UsageError(
            "Set project_id in config or pass --project-id / GOOGLE_CLOUD_PROJECT"
        )

    sql_dir = sql_dir.resolve()
    if not sql_dir.is_dir():
        raise click.ClickException(f"SQL directory not found: {sql_dir}")

    # Prefer script next to project root (e.g. BQ-Features/scripts/)
    script_candidates = [
        Path.cwd() / "scripts" / "upload_queries_to_studio.py",
        Path(__file__).resolve().parent.parent.parent / "scripts" / "upload_queries_to_studio.py",
    ]
    script_path = None
    for p in script_candidates:
        if p.is_file():
            script_path = p
            break

    if script_path is None:
        click.echo("Browser upload script not found. Run the following manually:")
        click.echo("")
        click.echo(
            f"  python scripts/upload_queries_to_studio.py --project-id {pid} --sql-dir {sql_dir} --region {region}"
        )
        click.echo("")
        click.echo("Requires: pip install playwright && playwright install chromium")
        click.echo("Script must be in the project's scripts/ directory.")
        return

    cmd = [
        sys.executable,
        str(script_path),
        "--project-id",
        pid,
        "--sql-dir",
        str(sql_dir),
        "--notebooks-dir",
        str(notebooks_dir),
        "--region",
        region,
    ]
    if no_sql:
        cmd.append("--no-sql")
    if no_notebooks:
        cmd.append("--no-notebooks")
    if headless:
        cmd.append("--headless")

    click.echo(f"Running: {' '.join(cmd)}")
    click.echo("Use the browser window to sign in if needed; the script will then upload SQL and/or notebook files.")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


@main.group()
def docs() -> None:
    """Documentation helpers: inject project ID, export to docx for SharePoint."""
    pass


@docs.command("inject-project-id")
@click.option(
    "--project-id",
    envvar="GOOGLE_CLOUD_PROJECT",
    help="GCP project ID to insert (overrides config).",
)
@click.option(
    "--source-dir",
    type=click.Path(path_type=Path),
    default=Path("doc"),
    help="Source documentation folder (default: doc/).",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=Path("doc_with_project"),
    help="Output folder mirroring source with project ID substituted (default: doc_with_project/).",
)
@click.option(
    "--bucket-prefix",
    default="bq-studio-demo",
    help="GCS bucket prefix used in replacements (default: bq-studio-demo).",
)
@click.pass_context
def docs_inject_project_id(
    ctx: click.Context,
    project_id: str | None,
    source_dir: Path,
    output_dir: Path,
    bucket_prefix: str,
) -> None:
    """Copy doc tree and replace YOUR_PROJECT / <project_id> with the real project ID.

    Produces a folder (e.g. doc_with_project/) with the same structure as doc/, so you can
    copy/paste from the generated .md files without editing placeholders.
    """
    from bq_features.docs_commands import inject_project_id

    config = ctx.obj["config"]
    pid = project_id or get_project_id(config)
    if not pid:
        raise click.UsageError(
            "Set project_id in config or pass --project-id / GOOGLE_CLOUD_PROJECT"
        )
    source_dir = source_dir.resolve()
    if not source_dir.is_dir():
        raise click.ClickException(f"Source directory not found: {source_dir}")
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    written = inject_project_id(
        source_dir=source_dir,
        output_dir=output_dir,
        project_id=pid,
        bucket_prefix=bucket_prefix,
    )
    click.echo(f"Injected project ID {pid!r} into {len(written)} .md files.")
    click.echo(f"Output: {output_dir}")


@docs.command("export-docx")
@click.option(
    "--source-dir",
    type=click.Path(path_type=Path),
    default=Path("doc"),
    help="Source documentation folder (default: doc/).",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=Path("doc_export"),
    help="Output folder for .docx files, mirroring source structure (default: doc_export/).",
)
def docs_export_docx(source_dir: Path, output_dir: Path) -> None:
    """Export doc/ to doc_export/ as .docx, mirroring structure (one .docx per .md).

    Every .md under the source folder is converted to .docx under the output folder with the same
    relative path (e.g. doc/features/1-studio/foo.md → doc_export/features/1-studio/foo.docx).
    Requires pandoc (apt install pandoc, brew install pandoc, or https://pandoc.org/installing.html).
    """
    from bq_features.docs_commands import export_docs_to_docx

    source_dir = source_dir.resolve()
    if not source_dir.is_dir():
        raise click.ClickException(f"Source directory not found: {source_dir}")
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    click.echo("Exporting .md → .docx (mirroring folder structure).")
    try:
        created = export_docs_to_docx(source_dir=source_dir, output_dir=output_dir)
    except RuntimeError as e:
        raise click.ClickException(str(e)) from e
    click.echo(f"Exported {len(created)} .md files to .docx under {output_dir}.")


if __name__ == "__main__":
    main()
