# Use case 2: Load formatted data from pre-filled BQ datasets

## Goal

Work with **pre-filled BigQuery datasets** (formatted, queryable tables) and use **tools to generate** these demo datasets so analysts can explore and build ETLs on a consistent baseline.

## Context

After raw files are in GCS (or in parallel), teams need a “golden” or staging dataset in BigQuery with clean schema and sample data. This use case covers generating and loading that dataset.

## Demo resources

- **CLI:** `bqdemo deploy infra --with-demo-data` creates the demo datasets and loads the **bundled finance CSVs** into BigQuery tables:
  - **Dataset:** `bq_studio_demo` (or your `dataset_prefix`).
  - **Tables:** `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.
- **Custom CSVs:** `bqdemo deploy infra --csv-dir /path/to/csvs` loads your own CSVs into the same project/dataset; table names = filenames without extension.
- **Bundled demo data location:** The CLI uses packaged CSVs (see `src/bq_features/demo_data/` or the installed package). You can replace or extend them for your own “formatted” demo.

## Steps

### 1. Generate and load the demo dataset

```bash
bqdemo deploy infra --with-demo-data
```

This creates:

- Dataset `bq_studio_demo` (and optionally `bq_studio_demo_staging`).
- Tables populated from the bundled CSVs: `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.

### 2. Verify in BigQuery

In **BigQuery Studio** → **Explorer**, expand your project and the `bq_studio_demo` dataset. Open each table (Overview / Details) and run `SELECT * FROM ... LIMIT 10` to confirm schema and data.

### 3. Generate demo datasets from your own CSVs

To create a “formatted” dataset from your own files (same project, same or different dataset):

```bash
bqdemo deploy infra --csv-dir /path/to/your/formatted/csvs --no-demo-data
```

Tables will be created in the demo dataset with names derived from your CSV filenames. Ensure column names and types are consistent (the loader infers types).

### 4. Optional: Staging dataset

The CLI creates a staging dataset (e.g. `bq_studio_demo_staging`) for ETL outputs. Use it as the destination for data preparations or Dataform so that “formatted” refined tables live alongside or instead of the initial load.

## What you get

- Pre-filled BigQuery dataset(s) with known tables and schema.
- A repeatable way to (re)generate demo datasets via the CLI (`--with-demo-data` or `--csv-dir`).
- Same project and region as the demo bucket for later ETL (GCS → BQ).

## Next

- **Use case 3:** Explore this data with structured queries and AI-assisted analytics.
- **Use case 4:** Build ETLs that read from GCS and write refined tables in BQ.
