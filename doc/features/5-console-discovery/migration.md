# Migration

## What it is

**Migration** in the BigQuery console provides guides and setup for moving from other data warehouses (e.g. Teradata, Redshift, Snowflake) to BigQuery. It includes assessment, schema and SQL translation, and data movement.

## Demo doc

The BQ-Features demo does not perform a real migration. Use the Migration section to **document** how the demo dataset fits into a migration story (e.g. “first load looks like this”) and to point trainees to the official migration tools if they will migrate production data later.

## Demo material

1. **Open Migration**  
   In BigQuery → **Migration** (from the left menu or Overview). Open the migration hub or assessment tool.

2. **Review migration options**  
   See what’s offered: assessment, SQL translation, data transfer from another warehouse. Note which of these apply to your org (e.g. “We will migrate from Redshift; use this guide.”). No need to run a full assessment for the demo.

3. **Relate demo to “first load”**  
   In your internal doc, write: “The BQ-Features demo simulates a **first load** into BigQuery: we have CSV files in GCS and tables in a dataset (`bq_studio_demo`). In a real migration, you’d use the Migration tools to translate schemas and SQL, then load data similarly.” Optionally load a small CSV export from another system into the demo dataset via **Create table** from GCS to show “migrated” data in the demo.

4. **SQL translation (optional)**  
   If the migration UI includes SQL translation (e.g. Redshift SQL → BigQuery SQL), paste a sample from the demo (e.g. `02_returns_and_volatility.sql`) and note that it’s already GoogleSQL; for legacy SQL, the translator would convert it. Document one example for trainees.

5. **Document**  
   “For migration to BigQuery: start at BigQuery → Migration. For our demo, data is already loaded into `bq_studio_demo`; the same pattern (GCS + load job or transfer) applies to migrated data.”

## Demo data used

- Demo dataset `bq_studio_demo` as an example of “target” schema and tables.  
- Optional: a small CSV export from another warehouse loaded into the demo dataset via **Create table** from GCS to mimic a migrated dataset.

## References

- [Migration to BigQuery](https://cloud.google.com/bigquery/docs/migration/migration-overview)
