# Use case 1: Load raw data (CSV, Excel) into GCS

## Goal

Load raw financial data from **CSV and Excel** files into the **GCS bucket** associated with the demo project so it can be used later for ETL and analytics.

## Context

Analysts receive data as files (exports, feeds). The first step is to land them in a project-owned bucket with a clear structure (e.g. `raw/`, `demo_data/`).

## Demo resources

- **GCS bucket:** The demo project has a GCS bucket (e.g. `gs://bq-studio-demo-<project_id>/`).
- **Bundled CSVs:** Bundled finance demo CSVs may be present under `demo_data/` (`portfolio_holdings.csv`, `daily_prices.csv`, `transactions.csv`, `pnl_daily.csv`).
- **Your own files:** Place CSV or Excel files in a local directory and upload them to the same bucket paths (see below).

## Steps

### 1. Ensure the bucket exists

The demo project should have a bucket such as `gs://bq-studio-demo-<project_id>/`. If you are setting up from scratch, create the bucket in **Cloud Console** → **Cloud Storage** → **Create bucket**, or use your project’s deployment process.

### 2. Ensure bundled demo CSVs are in the bucket (if applicable)

If your project deploys demo data, the bundled CSV files will be under `gs://<bucket>/demo_data/`. Inspect them in **Cloud Storage** → your bucket → `demo_data/`.

### 3. Load your own CSV or Excel files

- **CSV:** Use `gsutil cp` or the Cloud Console upload:
  ```bash
  gsutil -m cp /path/to/*.csv gs://bq-studio-demo-YOUR_PROJECT/raw/
  ```
  Or drag-and-drop in **Cloud Storage** → bucket → **Upload**.

- **Excel:** Upload `.xlsx` the same way to a prefix like `raw/excel/`. BigQuery can query Excel via external tables or after conversion to CSV; for ETL you may convert Excel to CSV in a first step (e.g. with a small script or Dataform).

### 4. Optional: Load your own CSV directory into BigQuery

To load your own CSV directory into BQ: upload the CSVs to the bucket (e.g. under `raw/` or `demo_data/`), then in **BigQuery Studio** use **Create table** → source **Google Cloud Storage**, select the GCS path(s). Table names can match the CSV filenames (without extension). Alternatively use **Load data** from the table menu for each file.

## What you get

- GCS bucket with a known prefix (e.g. `bq-studio-demo-<project_id>`).
- `demo_data/` (and optionally `raw/`) containing CSV (and optionally Excel) files.
- Optionally, BigQuery tables populated from those files (via your project’s deployment or via Create table / Load data from GCS in BigQuery Studio).

## No-code / AI alternatives (BI analysts and non-developers)

You can achieve the same outcome without the CLI:

- **Create or use a bucket:** In **Google Cloud Console** → **Cloud Storage** → **Buckets**, create a bucket (or use an existing one your admin has set up). No `gsutil` or terminal required.
- **Upload files:** In the bucket view, use **Upload files** or **Upload folder** (drag-and-drop) to upload CSV or Excel files into a prefix such as `raw/` or `demo_data/`. No command line needed.
- **Bulk or recurring loads:** Use **Transfer Service** (Console → **Transfer** or **BigQuery Data Transfer**) to schedule uploads from other clouds or from on-premises; the UI guides you through source and destination. For one-off loads, manual upload is enough.

If the bucket already exists (e.g. created by an admin), you can upload your own files into it via the Console only.

## Next

- **Use case 2:** Use the pre-filled BQ datasets (and tools to generate them).
- **Use case 4:** Build ETLs that read from these GCS paths and write refined tables in BQ.
