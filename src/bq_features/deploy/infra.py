"""Deploy BigQuery datasets and GCS buckets (no demo data; use deploy demos for that)."""

from __future__ import annotations

from pathlib import Path

import click
from google.auth.exceptions import DefaultCredentialsError

from bq_features.deploy import gcp


def run_deploy_infra(
    project_id: str,
    region: str,
    bucket_prefix: str,
    dataset_prefix: str,
    dry_run: bool,
    config: dict,
) -> None:
    """Create datasets and bucket only. Load demo data with 'bqdemo deploy demos'."""
    dataset_id = f"{dataset_prefix}"
    staging_dataset_id = f"{dataset_prefix}_staging"
    bucket_name = f"{bucket_prefix}-{project_id}".replace("_", "-").lower()

    if dry_run:
        click.echo("[DRY RUN] Would create:")
        click.echo(f"  - BigQuery dataset: {project_id}.{dataset_id} (region: {region})")
        click.echo(f"  - BigQuery dataset: {project_id}.{staging_dataset_id}")
        click.echo(f"  - GCS bucket: gs://{bucket_name}")
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

    click.echo("Infra deploy complete.")
    click.echo(f"  Datasets: {dataset_id}, {staging_dataset_id}")
    click.echo(f"  Bucket: gs://{bucket_name}")
    click.echo("  Load demo data with: bqdemo deploy demos")
