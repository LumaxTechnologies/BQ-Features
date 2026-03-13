# Analytics & ML

## What it is

**BigQuery ML** lets you train and run models (e.g. linear regression, boosted tree, ARIMA) via SQL. **BI Engine** provides in-memory acceleration for dashboards. **Looker Studio / Looker** connect to BigQuery for reporting and LookML models.

## Demo doc

Use the demo dataset to try BigQuery ML (e.g. predict or classify from `daily_prices` or a small derived table) and to connect Looker Studio to the demo tables for a simple report.

## Demo material

### BigQuery ML

1. **Create a small training table**  
   From `daily_prices`, build a table with features and a target (e.g. next-day return or a binary label). Example:
   ```sql
   CREATE OR REPLACE TABLE `YOUR_PROJECT.bq_studio_demo.prices_ml_input` AS
   SELECT symbol, date, close,
          LAG(close) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
          (close - LAG(close) OVER (PARTITION BY symbol ORDER BY date))
            / NULLIF(LAG(close) OVER (PARTITION BY symbol ORDER BY date), 0) AS daily_return
   FROM `YOUR_PROJECT.bq_studio_demo.daily_prices`;
   ```

2. **Train a model**  
   Use BigQuery ML to train e.g. a linear regression or boosted tree on `prices_ml_input` (predict `daily_return` or a binned target). Run the training in the query editor and confirm the model is created in the dataset.

3. **Predict**  
   Use `ML.PREDICT` against the model and a subset of data. Run from the query editor or from a saved query.

### Looker Studio

4. **Connect Looker Studio**  
   In Looker Studio, add a data source → **BigQuery** → select your project and dataset `bq_studio_demo`. Choose tables: `daily_prices`, `pnl_daily`, `portfolio_holdings`.

5. **Build a simple report**  
   Create a report with a table or chart using `pnl_daily` (e.g. total PnL by date or strategy). Optionally add a chart from `daily_prices` (e.g. close by date for one symbol). Save and share the report link.

### BI Engine (optional)

6. **Reservation**  
   If you use BI Engine, create a reservation and attach it to your project. Point a Looker Studio report or dashboard to the demo dataset; BI Engine can accelerate queries on the demo tables.

## Demo data used

- `bq_studio_demo.daily_prices` (and derived `prices_ml_input`).  
- `bq_studio_demo.pnl_daily`, `bq_studio_demo.portfolio_holdings` for reporting.  
- BigQuery ML model in `bq_studio_demo` (e.g. `model_returns`).

## References

- [BigQuery ML](https://cloud.google.com/bigquery/docs/bigqueryml-intro)  
- [Looker Studio and BigQuery](https://cloud.google.com/bigquery/docs/looker)  
- [BI Engine](https://cloud.google.com/bigquery/docs/bi-engine-intro)  
- `bq_studio_demos/docs/looker-bigquery-studio-demo.md`
