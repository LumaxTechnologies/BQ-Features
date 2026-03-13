# Use case 1: Load raw data (CSV, Excel) into GCS

## Goal

Load raw financial data from **CSV and Excel** files into the **GCS bucket** associated with the demo project so it can be used later for ETL and analytics.

## Context

Analysts receive data as files (exports, feeds). The first step is to land them in a project-owned bucket with a clear structure (e.g. `raw/`, `demo_data/`).

## Demo resources

- **CLI:** `bqdemo deploy infra` creates the demo GCS bucket (e.g. `gs://bq-studio-demo-<project_id>/`).
- **Bundled CSVs:** The CLI can upload bundled finance demo CSVs to the bucket when you run `bqdemo deploy infra --with-demo-data` (they go under `demo_data/`: `portfolio_holdings.csv`, `daily_prices.csv`, `transactions.csv`, `pnl_daily.csv`).
- **Your own files:** Place CSV or Excel files in a local directory and use the same bucket paths for a custom load (see below).

## Steps

### 1. Create the bucket (if not already done)

```bash
bqdemo deploy infra
```

This creates the bucket `gs://bq-studio-demo-<project_id>/` (or your configured `bucket_prefix`). No demo data is loaded yet.

### 2. Load bundled demo CSVs into the bucket

```bash
bqdemo deploy infra --with-demo-data
```

This uploads the bundled CSV files from the CLI package to `gs://<bucket>/demo_data/`. You can inspect them in the Cloud Console (**Cloud Storage** → your bucket → `demo_data/`).

### 3. Load your own CSV or Excel files

- **CSV:** Use `gsutil cp` or the Cloud Console upload:
  ```bash
  gsutil -m cp /path/to/*.csv gs://bq-studio-demo-YOUR_PROJECT/raw/
  ```
  Or drag-and-drop in **Cloud Storage** → bucket → **Upload**.

- **Excel:** Upload `.xlsx` the same way to a prefix like `raw/excel/`. BigQuery can query Excel via external tables or after conversion to CSV; for ETL you may convert Excel to CSV in a first step (e.g. with a small script or Dataform).

### 4. Optional: Load CSV from GCS into BigQuery (same run as infra)

`bqdemo deploy infra --with-demo-data` also **loads** the bundled CSVs into BigQuery tables in the demo dataset (`portfolio_holdings`, `daily_prices`, etc.). To load your own CSV directory into BQ:

```bash
bqdemo deploy infra --csv-dir /path/to/your/csvs --no-demo-data
```

Table names in BQ will match the CSV filenames (without extension). The same files can be present in the bucket for raw retention.

## What you get

- GCS bucket with a known prefix (e.g. `bq-studio-demo-<project_id>`).
- `demo_data/` (and optionally `raw/`) containing CSV (and optionally Excel) files.
- Optionally, BigQuery tables populated from those files (when using `--with-demo-data` or `--csv-dir`).

## Next

- **Use case 2:** Use the pre-filled BQ datasets (and tools to generate them).
- **Use case 4:** Build ETLs that read from these GCS paths and write refined tables in BQ.
