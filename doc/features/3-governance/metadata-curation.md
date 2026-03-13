# Metadata curation

## What it is

**Metadata curation** covers **automatic discovery**, **lineage**, and **metadata** management, often through **Dataplex Universal Catalog**. It helps with data discovery, profiling, and compliance.

## Demo doc

Use the demo dataset and the assets created by the CLI (tables, saved queries, Dataform operations) to show how metadata and lineage appear in the catalog and how to enrich metadata (e.g. descriptions, tags).

## Demo material

1. **Open catalog / discovery**  
   In BigQuery → **Governance** or **Dataplex** → **Universal Catalog** (or **Discovery**). Search for your project and dataset `bq_studio_demo`.

2. **Discover demo tables**  
   Confirm `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions` (and any created tables like `daily_pnl_summary`, `portfolio_value_snapshot`) appear. Open a table and view schema, lineage, and usage if available.

3. **View lineage**  
   For a table built by the demo (e.g. `daily_pnl_summary`), open its lineage view. Show that it comes from `pnl_daily` and from a scheduled query or Dataform run. For `portfolio_value_snapshot`, show lineage from `portfolio_holdings` and `daily_prices`.

4. **Enrich metadata**  
   Add a **description** and **tags** to one or more demo tables (e.g. “Demo table: daily PnL by strategy”). Add a tag like `environment:demo` or `owner:analytics`. Save and confirm they appear in the catalog and in search.

5. **Search**  
   Use the catalog search (natural language or keywords) to find “tables with symbol and date” or “PnL” and confirm the demo tables are returned. Use this to show analysts how to discover the demo dataset.

6. **Profiling (if available)**  
   If the catalog or Dataplex offers profiling, run a profile on `bq_studio_demo.daily_prices` or `pnl_daily` and show column stats and quality indicators.

## Demo data used

- Dataset: `bq_studio_demo` (and `bq_studio_demo_staging` if used).  
- Tables: all demo tables plus any created by scheduled queries or Dataform operations.  
- Lineage from: scheduled query, Dataform operations, and manual CREATE TABLE runs.

## References

- [Introduction to data governance in BigQuery](https://cloud.google.com/bigquery/docs/data-governance)  
- [Dataplex](https://cloud.google.com/dataplex/docs)  
- [Automatic discovery](https://cloud.google.com/bigquery/docs/automatic-discovery)
