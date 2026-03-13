# Pipelines

## What it is

**Pipelines** in BigQuery Studio are DAGs of tasks (SQL, data preparation runs, notebook runs) that you create from the UI. You can orchestrate and optionally schedule them. The Data Engineering Agent can help generate pipeline definitions.

## Demo doc

Build a simple pipeline that runs a demo SQL script (e.g. refresh daily PnL summary) or a data preparation based on the demo dataset. This complements a scheduled query that refreshes `daily_pnl_summary` from `pnl_daily`.

## Demo material

1. **Create a pipeline**  
   In BigQuery Studio → **Home** → **Create new** → **Pipeline** (or from Explorer → Pipelines). Name it e.g. `Demo daily refresh`.

2. **Add a SQL task**  
   Add a task that runs SQL. Use the same logic as the demo scheduled query:
   ```sql
   CREATE OR REPLACE TABLE `YOUR_PROJECT.bq_studio_demo.daily_pnl_summary` AS
   SELECT date, strategy, SUM(CAST(pnl AS FLOAT64)) AS total_pnl
   FROM `YOUR_PROJECT.bq_studio_demo.pnl_daily`
   GROUP BY date, strategy;
   ```
   Replace `YOUR_PROJECT` with your project ID.

3. **Add a second task (optional)**  
   Add another task that runs a query from `bq_studio_demos/sql/01_portfolio_value.sql` and writes to a table, or that runs a data preparation you created on `transactions`. Set the order (e.g. run after the first task).

4. **Run the pipeline**  
   Execute the pipeline once and confirm `daily_pnl_summary` (and any other outputs) are updated.

5. **Schedule (optional)**  
   If the UI supports scheduling for pipelines, set a schedule (e.g. daily). Otherwise use **Pipelines and integration** → Scheduled queries for the single-query case.

## Demo data used

- `bq_studio_demo.pnl_daily` → output `daily_pnl_summary`.  
- Optional: `portfolio_holdings`, `daily_prices` for a second task.

## References

- [Manage pipelines](https://cloud.google.com/bigquery/docs/manage-pipelines)  
- Main README: “Pipelines – example task DAG”
