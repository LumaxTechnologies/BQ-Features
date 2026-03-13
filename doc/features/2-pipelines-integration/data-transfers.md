# Data Transfers

## What it is

**BigQuery Data Transfer Service** automates scheduled data movement into BigQuery: load from Cloud Storage, S3, Azure Blob, Google Ads, Display & Video 360, and many other sources. It also supports **dataset copy** and **scheduled query** execution (transfer configs).

## Demo doc

For the BQ-Features demo, data is loaded once via `bqdemo deploy infra` (CSVs into the demo dataset and GCS). You can add a **transfer config** that periodically loads from the demo GCS bucket into BigQuery to simulate recurring ingestion.

## Demo material

1. **Open Pipelines and integration**  
   In BigQuery → **Pipelines and integration** (or **Data transfers**). View existing transfers or click **Create transfer**.

2. **Create a transfer from GCS (optional)**  
   To demo recurring load from the demo bucket:  
   - **Source**: Cloud Storage.  
   - **Source URI**: `gs://YOUR_DEMO_BUCKET/demo_data/*.csv` (or a specific file).  
   - **Destination dataset**: `bq_studio_demo` (or staging).  
   - **Schedule**: e.g. daily or weekly.  
   - **Schema**: Auto-detect or provide.  
   Create and run once to confirm data lands in the demo tables (you may need to map files to table names or use a single table).

3. **Dataset copy (optional)**  
   Create a transfer that copies `bq_studio_demo` to another dataset (e.g. for backup or a dev copy). Useful to show dataset copy as a transfer type.

4. **Scheduled query**  
   The CLI creates a scheduled query via the same Data Transfer API (`bqdemo deploy demos --with-schedulers`). In **Pipelines and integration** → **Scheduled queries**, find the config that refreshes `daily_pnl_summary` from `pnl_daily`. Inspect schedule and run history.

## Demo data used

- Demo GCS bucket: `gs://bq-studio-demo-YOUR_PROJECT/` (or your bucket prefix).  
- Demo dataset: `bq_studio_demo`.  
- Scheduled query target: `daily_pnl_summary` from `pnl_daily`.

## References

- [Data Transfer Service introduction](https://cloud.google.com/bigquery/docs/dts-introduction)  
- [Create a transfer](https://cloud.google.com/bigquery/docs/transfer-config)
