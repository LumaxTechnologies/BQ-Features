# Scheduled queries

## What it is

**Scheduled queries** are recurring GoogleSQL jobs run by the BigQuery Data Transfer Service. You can parameterize by date/time and set a destination table. They support DDL/DML but **do not** support `CALL` to stored procedures (use Dataform operations or Cloud Scheduler + Cloud Functions for that).

## Demo doc

A scheduled query can be set up to refresh `daily_pnl_summary` from `pnl_daily` on a daily schedule. Use it as the reference for creating more scheduled queries against the demo dataset (**Pipelines and integration** → **Scheduled queries**).

## Demo material

1. **Locate the demo scheduled query**  
   In BigQuery → **Pipelines and integration** → **Scheduled queries** (or **Data transfers**). Find the config named e.g. `bq_studio_demo_daily_pnl` that runs daily and writes to `daily_pnl_summary`.

2. **Inspect the query**  
   Open the transfer config and view the query:
   ```sql
   CREATE OR REPLACE TABLE `YOUR_PROJECT.bq_studio_demo.daily_pnl_summary` AS
   SELECT date, strategy, SUM(CAST(pnl AS FLOAT64)) AS total_pnl
   FROM `YOUR_PROJECT.bq_studio_demo.pnl_daily`
   GROUP BY date, strategy
   ```
   Confirm destination dataset/table and schedule.

3. **Run now**  
   Trigger a one-off run from the UI. After it completes, query `bq_studio_demo.daily_pnl_summary` to confirm it matches the aggregation of `pnl_daily`.

4. **Create another scheduled query (optional)**  
   Create a new scheduled query that runs e.g. `01_portfolio_value.sql` logic and writes to a table like `portfolio_value_snapshot`. Use the same dataset and a schedule (e.g. daily). Do **not** use `CALL`; use plain DDL/DML only.

5. **Parameterize by date (optional)**  
   Use `@run_time` or similar in the query to filter `pnl_daily` by date (e.g. last 7 days). Check the Data Transfer UI for parameter syntax and set the destination table name template if needed.

## Demo data used

- Source: `bq_studio_demo.pnl_daily`.  
- Destination: `bq_studio_demo.daily_pnl_summary`.  
- Optional: `portfolio_holdings`, `daily_prices` for a second scheduled query.

## References

- [Scheduling queries](https://cloud.google.com/bigquery/docs/scheduling-queries)  
- [Create a scheduled query](https://cloud.google.com/bigquery/docs/samples/bigquerydatatransfer-create-scheduled-query)
