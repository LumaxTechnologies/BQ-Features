"""Deploy BQ Studio demo material: notebooks, SQL, docs, demo data, schedulers, Looker."""

from __future__ import annotations

import shutil
from pathlib import Path

import click
from google.auth.exceptions import DefaultCredentialsError

from bq_features.deploy import gcp
from bq_features.deploy import templates
from bq_features.deploy.demo_data import get_bundled_demo_data_dir, write_bundled_demo_data


def run_deploy_demos(
    project_id: str,
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
    config: dict,
) -> None:
    """Generate and upload demo SQL, notebooks, docs; optionally load demo data into BQ and GCS; optionally deploy Dataform workspace and .sqlx."""
    dataset_id = dataset_prefix
    bucket_name = f"{bucket_prefix}-{project_id}".replace("_", "-").lower()

    if dry_run:
        click.echo("[DRY RUN] Would write to:")
        click.echo(f"  {output_dir.absolute()}")
        click.echo("  - SQL scripts, notebooks, docs, Dataform operations (dataform/definitions/operations/)")
        if with_demo_data or csv_dir:
            click.echo("  - Load demo/CSV data into BigQuery and upload to GCS (demo_data/)")
        if with_schedulers:
            click.echo("  - Create scheduled queries in project")
        if with_looker:
            click.echo("  - Looker instructions and LookML snippets")
        if upload_to_gcs:
            click.echo(f"  - Copy doc/use_cases/ into output docs/use_cases/")
            click.echo(f"  - Upload SQL to gs://{bucket_name}/sql/")
            click.echo(f"  - Upload notebooks to gs://{bucket_name}/notebooks/")
            click.echo(f"  - Upload docs (and docs/use_cases/) to gs://{bucket_name}/docs/")
            click.echo(f"  - Upload Dataform operations to gs://{bucket_name}/dataform/")
        if deploy_dataform:
            click.echo("  - Create Dataform demo-workspace (if missing) and deploy .sqlx into it")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    templates.write_all_templates(
        output_dir=output_dir,
        project_id=project_id,
        dataset_id=dataset_id,
        bucket_name=bucket_name,
        region=region,
        with_looker=with_looker,
    )

    # Copy use-case docs from repo doc/use_cases/ so they are uploaded to GCS with other docs
    _copy_use_cases_docs(output_dir)

    # Load demo data into BigQuery and GCS (deploy demos is the single command for demo data)
    if with_demo_data or csv_dir:
        _load_demo_data(project_id, dataset_id, bucket_name, with_demo_data, csv_dir)

    if with_schedulers:
        _create_schedulers(project_id, region, dataset_id, config)

    if deploy_dataform:
        from bq_features.deploy.dataform_deploy import deploy_dataform_workspace

        click.echo("Dataform: ensuring demo-workspace and deploying .sqlx ...")
        deploy_dataform_workspace(project_id, region, output_dir.resolve())

    if upload_to_gcs:
        click.echo(f"Uploading to gs://{bucket_name}/ ...")
        _upload_demos_to_gcs(output_dir.resolve(), project_id, bucket_name)

    click.echo("Demos deploy complete.")
    click.echo(f"  Local output: {output_dir.absolute()}")
    if upload_to_gcs:
        click.echo(f"  GCS bucket: gs://{bucket_name}/ (sql/, notebooks/, docs/, docs/use_cases/, dataform/)")
    click.echo("  To use the SQL in BigQuery Studio: Queries → View actions → Upload SQL query → select files from bq_studio_demos/sql/")


def _load_demo_data(
    project_id: str,
    dataset_id: str,
    bucket_name: str,
    with_demo_data: bool,
    csv_dir: Path | None,
) -> None:
    """Load CSV data into BigQuery and upload to GCS (bundled demo or custom --csv-dir)."""
    data_dir = csv_dir
    if with_demo_data and not csv_dir:
        data_dir = get_bundled_demo_data_dir()
        if not data_dir or not data_dir.is_dir():
            demo_root = Path(__file__).resolve().parent.parent.parent.parent / "demo_data"
            demo_root.mkdir(parents=True, exist_ok=True)
            write_bundled_demo_data(demo_root)
            data_dir = demo_root

    if not data_dir or not data_dir.is_dir():
        return

    try:
        client_bq = gcp.get_bigquery_client(project_id)
        client_gcs = gcp.get_storage_client(project_id)
    except DefaultCredentialsError:
        click.echo("Google Cloud credentials not found; skipping demo data load.", err=True)
        click.echo("  Run: gcloud auth application-default login", err=True)
        return

    click.echo("Loading demo data into BigQuery and uploading to GCS...")
    gcp.load_csv_dir_to_bq(client_bq, project_id, dataset_id, data_dir)
    gcp.upload_csv_dir_to_gcs(client_gcs, bucket_name, data_dir)


def _copy_use_cases_docs(output_dir: Path) -> None:
    """Copy doc/use_cases/ from repo into output_dir/docs/use_cases/ for GCS upload."""
    # Repo root: from .../src/bq_features/deploy/demos.py -> .../src -> parent = repo root
    pkg_root = Path(__file__).resolve().parent.parent.parent
    repo_root = pkg_root.parent
    candidates = [
        repo_root / "doc" / "use_cases",
        Path.cwd() / "doc" / "use_cases",
    ]
    for src in candidates:
        if src.is_dir():
            dest = output_dir / "docs" / "use_cases"
            dest.mkdir(parents=True, exist_ok=True)
            for path in src.rglob("*"):
                if path.is_file():
                    rel = path.relative_to(src)
                    (dest / rel).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, dest / rel)
            return


def _create_schedulers(project_id: str, region: str, dataset_id: str, config: dict) -> None:
    """Create sample scheduled transformation tasks."""
    service_account = config.get("service_account_email")
    # Daily aggregation example
    query = f"""
    CREATE OR REPLACE TABLE `{project_id}.{dataset_id}.daily_pnl_summary` AS
    SELECT date, strategy, SUM(CAST(pnl AS FLOAT64)) AS total_pnl
    FROM `{project_id}.{dataset_id}.pnl_daily`
    GROUP BY date, strategy
    """
    schedule = "every day 06:00"
    try:
        name = gcp.create_scheduled_query(
            project_id=project_id,
            location=region,
            display_name="bq_studio_demo_daily_pnl",
            query=query,
            schedule=schedule,
            destination_dataset_id=dataset_id,
            destination_table_template="daily_pnl_summary",
            service_account_email=service_account,
        )
        if name:
            click.echo(f"  Scheduled query created: {name}")
        else:
            click.echo("  Skipped scheduled query (Data Transfer API not available).")
    except Exception as e:
        click.echo(f"  Scheduled query creation failed: {e}. Create manually in Console if needed.")


def _upload_demos_to_gcs(output_dir: Path, project_id: str, bucket_name: str) -> None:
    """Upload SQL scripts, notebooks, and docs to the demo GCS bucket."""
    client = gcp.get_storage_client(project_id)
    bucket = client.bucket(bucket_name)

    if not bucket.exists():
        raise click.ClickException(
            f"Bucket gs://{bucket_name} does not exist. Run 'bqdemo deploy infra' first to create it."
        )

    sql_dir = output_dir / "sql"
    notebooks_dir = output_dir / "notebooks"
    docs_dir = output_dir / "docs"
    dataform_dir = output_dir / "dataform"

    sql_files = sorted(sql_dir.glob("*.sql")) if sql_dir.is_dir() else []
    notebook_files = sorted(notebooks_dir.glob("*.ipynb")) if notebooks_dir.is_dir() else []
    doc_files = sorted(docs_dir.rglob("*.md")) if docs_dir.is_dir() else []
    dataform_sqlx = list((dataform_dir / "definitions" / "operations").glob("*.sqlx")) if (dataform_dir / "definitions" / "operations").is_dir() else []
    dataform_readme = [dataform_dir / "README.md"] if (dataform_dir / "README.md").is_file() else []

    if not sql_files and not notebook_files and not doc_files and not dataform_sqlx:
        raise click.ClickException(
            f"No files to upload in {output_dir}. Expected sql/*.sql, notebooks/*.ipynb, docs/*.md, dataform/. "
            "Templates may not have been written correctly."
        )

    # SQL scripts -> gs://bucket/sql/
    for path in sql_files:
        blob = bucket.blob(f"sql/{path.name}")
        blob.upload_from_filename(str(path), content_type="text/plain")
        click.echo(f"  Uploaded SQL: gs://{bucket_name}/sql/{path.name}")

    # Notebooks -> gs://bucket/notebooks/
    for path in notebook_files:
        blob = bucket.blob(f"notebooks/{path.name}")
        blob.upload_from_filename(str(path), content_type="application/json")
        click.echo(f"  Uploaded notebook: gs://{bucket_name}/notebooks/{path.name}")

    # Docs -> gs://bucket/docs/ (preserve subpaths, e.g. docs/use_cases/01-....md)
    for path in doc_files:
        rel = path.relative_to(docs_dir)
        blob_path = f"docs/{rel.as_posix()}"
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(str(path), content_type="text/markdown")
        click.echo(f"  Uploaded doc: gs://{bucket_name}/{blob_path}")

    # Dataform operations -> gs://bucket/dataform/definitions/operations/ and dataform/README.md
    for path in dataform_sqlx:
        blob = bucket.blob(f"dataform/definitions/operations/{path.name}")
        blob.upload_from_filename(str(path), content_type="text/plain")
        click.echo(f"  Uploaded Dataform: gs://{bucket_name}/dataform/definitions/operations/{path.name}")
    for path in dataform_readme:
        blob = bucket.blob("dataform/README.md")
        blob.upload_from_filename(str(path), content_type="text/markdown")
        click.echo(f"  Uploaded Dataform: gs://{bucket_name}/dataform/README.md")
