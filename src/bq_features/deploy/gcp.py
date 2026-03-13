"""GCP API helpers for BigQuery and Cloud Storage."""

from __future__ import annotations

import warnings
from pathlib import Path

import click
from google.cloud import bigquery, storage

# Optional: BigQuery Data Transfer for scheduled queries
try:
    from google.cloud import bigquery_datatransfer
except ImportError:
    bigquery_datatransfer = None  # type: ignore[assignment]

# Suppress "without a quota project" warning when using gcloud user credentials.
# We use the project_id for all API calls; quota is applied to that project.
_CLOUD_SDK_QUOTA_WARNING = "Your application has authenticated using end user credentials from Google Cloud SDK without a quota project"


def get_bigquery_client(project_id: str) -> bigquery.Client:
    """Return BigQuery client for the given project."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=_CLOUD_SDK_QUOTA_WARNING)
        return bigquery.Client(project=project_id)


def get_storage_client(project_id: str) -> storage.Client:
    """Return Cloud Storage client for the given project."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=_CLOUD_SDK_QUOTA_WARNING)
        return storage.Client(project=project_id)


def get_datatransfer_client(project_id: str):
    """Return BigQuery Data Transfer client if available."""
    if bigquery_datatransfer is None:
        return None
    return bigquery_datatransfer.DataTransferServiceClient()


def create_dataset(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    location: str,
    description: str = "",
) -> None:
    """Create a BigQuery dataset if it does not exist."""
    full_id = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(full_id)
    dataset.location = location
    dataset.description = description
    client.create_dataset(dataset, exists_ok=True)


def create_bucket(
    client: storage.Client,
    bucket_name: str,
    location: str,
) -> None:
    """Create a GCS bucket if it does not exist."""
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        bucket.create(location=location)


def load_csv_dir_to_bq(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    csv_dir: Path,
) -> None:
    """Load all CSV files in a directory as BigQuery tables (table name = stem of filename)."""
    import pandas as pd

    dataset_ref = f"{project_id}.{dataset_id}"
    for path in sorted(csv_dir.glob("*.csv")):
        table_id = path.stem
        df = pd.read_csv(path)
        # Infer schema from DataFrame
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )
        table_ref = f"{dataset_ref}.{table_id}"
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        click.echo(f"  Loaded {path.name} -> {table_ref}")


def upload_csv_dir_to_gcs(
    client: storage.Client,
    bucket_name: str,
    csv_dir: Path,
    blob_prefix: str = "demo_data",
) -> None:
    """Upload all CSV files in a directory to GCS under the given prefix."""
    bucket = client.bucket(bucket_name)
    for path in sorted(csv_dir.glob("*.csv")):
        blob = bucket.blob(f"{blob_prefix}/{path.name}")
        blob.upload_from_filename(str(path))
        click.echo(f"  Uploaded {path.name} -> gs://{bucket_name}/{blob_prefix}/{path.name}")


def create_scheduled_query(
    project_id: str,
    location: str,
    display_name: str,
    query: str,
    schedule: str,
    destination_dataset_id: str,
    destination_table_template: str,
    service_account_email: str | None = None,
) -> str | None:
    """Create a scheduled query via Data Transfer API. Returns transfer config ID or None if API unavailable."""
    if bigquery_datatransfer is None:
        return None
    from google.cloud.bigquery_datatransfer_v1 import TransferConfig
    from google.protobuf import struct_pb2

    dt_client = get_datatransfer_client(project_id)
    loc = location.upper() if len(location) <= 3 else location
    if loc in ("US", "EU"):
        loc = "us" if loc == "US" else "eu"
    else:
        loc = location.lower().replace("-", "_")
    parent = f"projects/{project_id}/locations/{loc}"

    params = struct_pb2.Struct()
    params["query"] = query
    params["destination_table_name_template"] = destination_table_template

    config = TransferConfig(
        destination_dataset_id=destination_dataset_id,
        display_name=display_name,
        data_source_id="scheduled_query",
        schedule=schedule,
        params=params,
    )
    if service_account_email:
        config.service_account_name = (
            f"projects/{project_id}/serviceAccounts/{service_account_email}"
        )
    response = dt_client.create_transfer_config(parent=parent, transfer_config=config)
    return response.name if response else None
