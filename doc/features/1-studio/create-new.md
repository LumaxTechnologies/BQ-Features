# Create new

## What it is

**Create new** on the BigQuery Studio Home tab gives shortcuts to create: **SQL query**, **notebook**, **Spark notebook**, **data canvas**, **data preparation**, **pipeline**, or **table**. It’s the main entry point for starting work.

## Demo doc

Use each “Create new” option once with the demo dataset so you know where to start for ad-hoc SQL, notebooks, canvas, data prep, and pipelines.

## Demo material

1. **SQL query**  
   **Create new** → **SQL query**. Run: `SELECT * FROM \`YOUR_PROJECT.bq_studio_demo.daily_prices\` LIMIT 10`. Save as a saved query if desired.

2. **Notebook**  
   **Create new** → **Notebook**. In the first cell, load `bq_studio_demo.daily_prices` with BigQuery Client or `%%bigquery`, then show a small plot. Save the notebook.

3. **Spark notebook**  
   **Create new** → **Spark notebook** (if available). Run a small Spark snippet that reads from the demo dataset if you have a Spark environment attached.

4. **Data canvas**  
   **Create new** → **Data canvas**. Add a Table node for `bq_studio_demo.pnl_daily` and a SQL node: “Total PnL by date.” Add a visualization.

5. **Data preparation**  
   **Create new** → **Data preparation**. Source: `bq_studio_demo.transactions`. Add one transform (e.g. computed column), set destination to `bq_studio_demo_staging.transactions_prep`, run once.

6. **Pipeline**  
   **Create new** → **Pipeline**. Add one SQL task that refreshes `daily_pnl_summary` from `pnl_daily` (see `1-studio/pipelines.md`). Run the pipeline.

7. **Table**  
   **Create new** → **Table**. Create an empty table in `bq_studio_demo` or `bq_studio_demo_staging` with a simple schema (e.g. symbol STRING, dt DATE, value FLOAT64). Use it as a destination for a data prep or SQL later.

## Demo data used

- Dataset: `bq_studio_demo` (and optionally `bq_studio_demo_staging`).  
- Tables: `daily_prices`, `pnl_daily`, `transactions`, `portfolio_holdings`.  
- Outputs: saved query, notebook, canvas, prep table, pipeline run, new empty table.

## References

- [Explore BigQuery in the console](https://cloud.google.com/bigquery/docs/bigquery-web-ui)  
- [Create notebooks](https://cloud.google.com/bigquery/docs/create-notebooks)  
- [Data canvas](https://cloud.google.com/bigquery/docs/data-canvas)
