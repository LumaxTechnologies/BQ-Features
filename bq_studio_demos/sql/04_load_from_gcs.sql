-- Example: load from GCS CSV into BigQuery (run after infra deploy)

-- LOAD DATA OVERWRITE not run here; use Console or bq load for first load.
-- Example DDL for external table (optional):

-- CREATE OR REPLACE EXTERNAL TABLE `bq-features-489714.bq_studio_demo.daily_prices_external`
-- OPTIONS (
--   format = 'CSV',
--   uris = ['gs://bq-studio-demo-bq-features-489714/demo_data/daily_prices.csv'],
--   skip_leading_rows = 1
-- );
