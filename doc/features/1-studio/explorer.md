# Explorer

## What it is

The **Explorer** in BigQuery Studio is the left pane where you browse and manage datasets, tables, views, routines (UDFs, stored procedures), and job history. You can also **Add data** (stream, CDC, load, or federate external data).

## Demo doc

Use Explorer to discover the demo dataset and its tables. All demo material assumes dataset `bq_studio_demo` (or your project’s dataset prefix) with tables: `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.

## Demo material

1. **Open Explorer**  
   In BigQuery Studio, click **Explorer** in the left pane. Expand your project.

2. **Find the demo dataset**  
   Under your project, open **Datasets**. Locate `bq_studio_demo` (or your configured prefix). Click it to see **Tables** (and **Overview** / **Details**).

3. **Inspect demo tables**  
   - **portfolio_holdings**: as_of_date, symbol, quantity.  
   - **daily_prices**: symbol, date, open, high, low, close, volume.  
   - **pnl_daily**: date, strategy, pnl.  
   - **transactions**: symbol, quantity, price, txn_date, etc.  
   Click a table → **Overview** to see schema and details; use **Query** to generate a sample query.

4. **Job history**  
   Click **Job history** (personal or project) to see recent runs of queries and loads. Run one of the demo SQL scripts from `bq_studio_demos/sql/` and confirm it appears here.

5. **Add data (optional)**  
   Click **Add data** to see options: load from Cloud Storage (e.g. the demo bucket), stream, CDC, or create an external table. The demo CSVs are in `gs://<your-demo-bucket>/demo_data/`.

## Demo data used

- Dataset: `bq_studio_demo` (or `dataset_prefix` from config).  
- Tables: `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.

## References

- [Explore BigQuery in the console](https://cloud.google.com/bigquery/docs/bigquery-web-ui)
