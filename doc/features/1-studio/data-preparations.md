# Data preparations

## What it is

**Data preparations** are no-code/low-code ETL in BigQuery Studio: source table → transform (AI-suggested) → filter, dedupe, validate, join → destination. They are stored as SQLX and can be run manually or on a schedule.

## Demo doc

Use a demo table (e.g. `transactions` or `pnl_daily`) as the source for a data preparation. Apply Gemini-suggested transforms, then write to a destination in the demo or staging dataset.

## Demo material

1. **Open data preparations**  
   In BigQuery Studio → **Explorer** → **Data preparations**. Click **Create** (or **Create data preparation**).

2. **Set source**  
   Choose **Source** and select your project and dataset. Pick `bq_studio_demo.transactions` (or `pnl_daily`). The schema and sample rows load.

3. **Add transformations**  
   Use the transform panel and Gemini suggestions to: parse dates (e.g. `txn_date`), add a computed column (e.g. `quantity * price AS notional`), or trim/clean strings. Apply and review the data view.

4. **Filter or dedupe (optional)**  
   Add a **Filter** or **Deduplicate** step if needed. For demo, you can filter `transactions` by symbol or date range.

5. **Set destination**  
   Choose **Destination**: dataset `bq_studio_demo` or `bq_studio_demo_staging`, and a new table name (e.g. `transactions_cleaned`). Select write mode (full refresh, append, etc.).

6. **Run**  
   Run the data preparation. Confirm the destination table exists and has the expected rows. You can schedule it later from **Pipelines and integration** or a pipeline.

## Demo data used

- Source: `bq_studio_demo.transactions` (or `pnl_daily`).  
- Destination: `bq_studio_demo` or `bq_studio_demo_staging` (e.g. `transactions_cleaned`).

## References

- [Data preparations](https://cloud.google.com/bigquery/docs/data-prep-introduction)  
- Main README: “Data preparations – example steps and outcome”
