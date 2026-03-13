# Use case 2: Load formatted data from pre-filled BQ datasets

## Goal

Work with **pre-filled BigQuery datasets** (formatted, queryable tables) and use **tools to generate** these demo datasets so analysts can explore and build ETLs on a consistent baseline.

## Context

After raw files are in GCS (or in parallel), teams need a “golden” or staging dataset in BigQuery with clean schema and sample data. This use case covers generating and loading that dataset.

## Demo resources

- **Dataset:** `bq_studio_demo` (or your project’s dataset prefix) with tables **portfolio_holdings**, **daily_prices**, **pnl_daily**, **transactions**, populated from bundled finance CSVs or from your own load.
- **Custom CSVs:** Load your own CSVs into the same project/dataset via **BigQuery Studio** → **Create table** from GCS; table names can match filenames without extension.

## Steps

### 1. Ensure the demo dataset exists

The demo project should have:

- Dataset `bq_studio_demo` (and optionally `bq_studio_demo_staging`).
- Tables populated from the bundled CSVs: `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.

If you are setting up from scratch, create the dataset in **BigQuery Studio** → **Explorer** → **Create dataset**, then load the demo CSVs from GCS via **Create table** (see use case 1 for GCS paths).

### 2. Verify in BigQuery

In **BigQuery Studio** → **Explorer**, expand your project and the `bq_studio_demo` dataset. Open each table (Overview / Details) and run `SELECT * FROM ... LIMIT 10` to confirm schema and data.

### 3. Generate demo datasets from your own CSVs

To create a “formatted” dataset from your own files: upload the CSVs to GCS, then in **BigQuery Studio** use **Create table** → source **Google Cloud Storage** for each file (or a pattern). Tables will be created in the demo dataset with names you choose (e.g. matching filenames without extension). Ensure column names and types are consistent; use schema auto-detect or define the schema.

### 4. Optional: Staging dataset

The project may include a staging dataset (e.g. `bq_studio_demo_staging`) for ETL outputs. Use it as the destination for data preparations or Dataform so that “formatted” refined tables live alongside or instead of the initial load.

## What you get

- Pre-filled BigQuery dataset(s) with known tables and schema.
- A repeatable way to (re)generate demo datasets (via your project’s deployment or via Create table / Load data from GCS).
- Same project and region as the demo bucket for later ETL (GCS → BQ).

## No-code / AI alternatives (BI analysts and non-developers)

- **Create a table from GCS:** In **BigQuery Studio** → **Explorer** → your project → **Create dataset** (if needed), then **Create table**. Choose **Google Cloud Storage** as source, enter the GCS path (e.g. `gs://your-bucket/demo_data/*.csv`), and configure schema (auto-detect is available). No CLI or SQL required.
- **Load more files:** Repeat **Create table** from GCS for each file or pattern. For existing tables, use **Load data** (table actions) and select a GCS file; the UI handles format and options.
- **Data preparations:** Use **Data preparations** (Explorer → Data preparations) to create a flow that reads from a GCS-backed external table or an existing table, applies Gemini-suggested cleaning or transformations, and writes to a new table. That gives you “formatted” datasets without writing SQL or using the CLI.

If your organization has already run the CLI to create the demo dataset, you can still use the Console to create additional tables from GCS or to duplicate and adapt tables via copy/paste in the Explorer.

## Next

- **Use case 3:** Explore this data with structured queries and AI-assisted analytics.
- **Use case 4:** Build ETLs that read from GCS and write refined tables in BQ.
