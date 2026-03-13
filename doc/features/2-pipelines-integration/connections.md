# Connections

## What it is

**Connections** let BigQuery connect to external systems (e.g. Cloud SQL, federated sources). **Federation** (external tables, BigLake) lets you query data without loading it into BigQuery. Connections are created and managed from the console or API.

## Demo doc

The demo uses data **inside** BigQuery (tables loaded from GCS by the CLI). To demo connections, you can create an **external table** or a **connection** that points at the demo GCS bucket and query CSV (or other format) without loading, or connect to a Cloud SQL instance if you have one.

## Demo material

1. **External table on demo GCS (federation)**  
   In the query editor, run:
   ```sql
   CREATE OR REPLACE EXTERNAL TABLE `YOUR_PROJECT.bq_studio_demo.daily_prices_external`
   OPTIONS (
     format = 'CSV',
     uris = ['gs://YOUR_DEMO_BUCKET/demo_data/daily_prices.csv'],
     skip_leading_rows = 1
   );
   ```
   Replace bucket name. Then query `bq_studio_demo.daily_prices_external` to confirm federation works. Compare with the native table `daily_prices` (loaded by the CLI).

2. **Connection to Cloud SQL (optional)**  
   If you have a Cloud SQL instance, create a **Connection** in BigQuery (e.g. **Pipelines and integration** or **Connections**). Configure the connection and optionally create a federated table or use it in a data transfer. Run a small query that uses the connection to show cross-source access.

3. **BigLake (optional)**  
   If you use BigLake for GCS or other object storage, create a BigLake table pointing at the demo bucket path and run a query. This demonstrates querying external storage with optional caching.

4. **Reference in a query**  
   Write a saved query that joins the demo BigQuery table `portfolio_holdings` with the external table `daily_prices_external` (if schema matches) to show mixed native + federated querying.

## Demo data used

- Demo GCS bucket: `gs://bq-studio-demo-YOUR_PROJECT/demo_data/`.  
- Dataset: `bq_studio_demo`.  
- Native tables: `portfolio_holdings`, `daily_prices` (for comparison).  
- External table: `daily_prices_external` (same data, federated).

## References

- [External data sources](https://cloud.google.com/bigquery/docs/external-data-sources)  
- [Connections](https://cloud.google.com/bigquery/docs/connections-api-intro)  
- Demo SQL: `bq_studio_demos/sql/04_load_from_gcs.sql`
