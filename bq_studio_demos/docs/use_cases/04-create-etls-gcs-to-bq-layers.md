# Use case 4: Create ETLs (GCS → BQ, multiple transformation layers)

## Goal

Create **ETLs** that read **raw data from GCS** and write **refined data into BigQuery tables** through **several layers** of transformation (e.g. raw → staging → cleansed → aggregated).

## Context

Analysts and engineers need repeatable pipelines that land raw files, clean and validate, then build business-level tables. This use case uses the demo bucket and dataset to show a layered ETL design.

## Demo resources

- **GCS:** Raw or demo CSVs in `gs://bq-studio-demo-<project_id>/demo_data/` (or `raw/`).
- **Datasets:** `bq_studio_demo` (staging/refined), `bq_studio_demo_staging` (optional staging layer).
- **Dataform operations:** `bq_studio_demos/dataform/definitions/operations/` — examples that read from BQ tables (themselves loaded from GCS) and write derived tables. You can adapt them to read from external tables over GCS or add new SQLX layers.
- **Data preparations:** BigQuery Studio **Data preparations** for no-code/low-code ETL (source → transform → destination). See [data-preparations.md](../features/1-studio/data-preparations.md).
- **SQL and load:** `bq_studio_demos/sql/04_load_from_gcs.sql` — example of loading from GCS (run manually or via scheduled query / Dataform).

## Steps

### 1. Define layers

- **Layer 0 (raw):** Data in GCS (e.g. `demo_data/*.csv`). Optionally create **external tables** over these paths for SQL access without loading.
- **Layer 1 (staging):** Tables in `bq_studio_demo_staging` (or a `staging` dataset): loaded from GCS with minimal transformation (e.g. type casting, column rename).
- **Layer 2 (refined):** Tables in `bq_studio_demo`: cleansed, validated, joined (e.g. `portfolio_value_snapshot`, `returns_volatility`, `daily_pnl_summary`).

### 2. Layer 0 → Layer 1 (load from GCS)

- **Option A — Console / bq load:** Use **Explorer → Add data** or `bq load` to load `gs://<bucket>/demo_data/daily_prices.csv` into `bq_studio_demo_staging.daily_prices_raw`. Repeat for other files.
- **Option B — External table then INSERT:** Create an external table over the CSV, then `INSERT INTO bq_studio_demo_staging.daily_prices_raw SELECT * FROM external_table` (with any casts). See `bq_studio_demos/sql/04_load_from_gcs.sql`.

### 3. Layer 1 → Layer 2 (transform in BQ)

- Use **Dataform** operations or **saved queries** that read from staging and write to the main dataset. Example (already in the demo): `refresh_daily_pnl_summary.sqlx` reads `pnl_daily` and writes `daily_pnl_summary`; you can add similar operations that read from `bq_studio_demo_staging` and write to `bq_studio_demo`.
- Or use **Data preparations**: source = staging table, add steps (parse dates, computed columns, filters), destination = refined table in `bq_studio_demo`.

### 4. Add a third layer (optional)

- **Aggregated / mart layer:** e.g. a dataset `bq_studio_demo_mart` with tables built from `bq_studio_demo` (e.g. daily KPIs, strategy summary). Implement as Dataform tables or operations, or as scheduled queries.

## What you get

- A clear separation: raw (GCS) → staging (BQ) → refined (BQ) [→ mart].
- Reusable ETL logic in Dataform and/or data preparations.
- Foundation for adding stored procedures (use case 5), versioning (6), scheduling (7), and monitoring (8).

## No-code / AI alternatives (BI analysts and non-developers)

- **Data preparations:** In **BigQuery Studio** → **Explorer** → **Data preparations**, create a new data preparation. Set the **source** to a table (e.g. one loaded from GCS via Create table) or an external table. Use the **data view** and **suggestion cards** from Gemini to add steps: parse dates, trim text, filter rows, deduplicate, or add computed columns. Set a **destination** table (e.g. in a staging or refined dataset). Run manually or schedule the data preparation. No SQLX or Dataform required for single-table or simple multi-step flows.
- **Pipelines:** Use **Create new** → **Pipeline** to chain multiple tasks (e.g. “run data preparation A”, then “run SQL or data preparation B”). Add tasks and set the order in the UI. Optionally set a schedule so the pipeline runs daily or weekly. The **Data Engineering Agent** can suggest or generate pipeline steps from natural language (e.g. “Load from GCS, clean, then aggregate by date”).
- **Layer-by-layer:** Create one data preparation per layer (e.g. raw → staging, staging → refined). Each preparation has one source and one destination; chain them by using the output table of one as the source of the next, or use a pipeline that runs them in sequence.

For BI analysts, data preparations plus pipelines cover most ETL needs without writing SQLX or using Dataform repos.

## Next

- **Use case 5:** Include stored procedures in these ETLs (e.g. validation or complex logic).
- **Use case 6:** Share and version the ETL definitions.
