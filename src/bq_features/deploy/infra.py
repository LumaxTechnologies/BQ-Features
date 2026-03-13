"""Deploy BigQuery datasets, GCS buckets, and load CSV demo data."""

from __future__ import annotations

from pathlib import Path

import click
from google.auth.exceptions import DefaultCredentialsError

from bq_features.deploy import gcp
from bq_features.deploy.demo_data import get_bundled_demo_data_dir, write_bundled_demo_data


def run_deploy_infra(
    project_id: str,
    region: str,
    with_demo_data: bool,
    csv_dir: Path | None,
    bucket_prefix: str,
    dataset_prefix: str,
    dry_run: bool,
    config: dict,
) -> None:
    """Create datasets, buckets, and optionally load CSV data."""
    dataset_id = f"{dataset_prefix}"
    staging_dataset_id = f"{dataset_prefix}_staging"
    bucket_name = f"{bucket_prefix}-{project_id}".replace("_", "-").lower()

    if dry_run:
        click.echo("[DRY RUN] Would create:")
        click.echo(f"  - BigQuery dataset: {project_id}.{dataset_id} (region: {region})")
        click.echo(f"  - BigQuery dataset: {project_id}.{staging_dataset_id}")
        click.echo(f"  - GCS bucket: gs://{bucket_name}")
        if with_demo_data or csv_dir:
            click.echo("  - Load CSV data into tables (see tables below)")
        return

    try:
        client_bq = gcp.get_bigquery_client(project_id)
        client_gcs = gcp.get_storage_client(project_id)
    except DefaultCredentialsError:
        click.echo("Google Cloud credentials not found.", err=True)
        click.echo("", err=True)
        click.echo("Run the following to log in and set Application Default Credentials:", err=True)
        click.echo("  gcloud auth application-default login", err=True)
        click.echo("", err=True)
        click.echo("See: https://cloud.google.com/docs/authentication/external/set-up-adc", err=True)
        raise click.ClickException("Authentication required.")

    # Create datasets
    click.echo("Creating BigQuery datasets...")
    gcp.create_dataset(client_bq, project_id, dataset_id, region, description="BQ Studio demo – main")
    gcp.create_dataset(
        client_bq, project_id, staging_dataset_id, region, description="BQ Studio demo – staging/raw"
    )

    # Create bucket
    click.echo("Creating GCS bucket...")
    gcp.create_bucket(client_gcs, bucket_name, region)

    # CSV loading
    data_dir = csv_dir
    if with_demo_data and not csv_dir:
        data_dir = get_bundled_demo_data_dir()
        if not data_dir or not data_dir.is_dir():
            demo_root = Path(__file__).resolve().parent.parent.parent.parent / "demo_data"
            demo_root.mkdir(parents=True, exist_ok=True)
            write_bundled_demo_data(demo_root)
            data_dir = demo_root

    if data_dir and data_dir.is_dir():
        click.echo("Loading CSV data into BigQuery and uploading to GCS...")
        gcp.load_csv_dir_to_bq(client_bq, project_id, dataset_id, data_dir)
        gcp.upload_csv_dir_to_gcs(client_gcs, bucket_name, data_dir)
    else:
        click.echo("No CSV directory provided; skipping data load.")

    click.echo("Infra deploy complete.")
    click.echo(f"  Datasets: {dataset_id}, {staging_dataset_id}")
    click.echo(f"  Bucket: gs://{bucket_name}")
