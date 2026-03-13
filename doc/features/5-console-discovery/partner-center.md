# Partner Center

## What it is

**Partner Center** in BigQuery surfaces partner tools and services (ETL, BI, data quality, etc.) that work with BigQuery. You can discover and enable integrations from the console.

## Demo doc

Use Partner Center to show what integrations are available. The demo dataset can be used with partner BI or ETL tools if you connect them to the same project; document one optional integration (e.g. a BI tool) that reads from `bq_studio_demo`.

## Demo material

1. **Open Partner Center**  
   In BigQuery → **Partner Center** (from the left menu). Browse the listed partners and categories (e.g. ETL, BI, data quality).

2. **Pick a relevant partner**  
   Choose a partner that fits your demo (e.g. a BI tool that connects to BigQuery). Open its card and read the short description and “Get started” or “Connect” steps. Do not install or configure unless you have approval; for the doc, summarize what the partner does and how it would connect to your project.

3. **Document for demo**  
   “Partner Center lists tools that work with BigQuery. To use the demo dataset with [Partner X]: connect [Partner X] to project Y and dataset `bq_studio_demo`; then you can build reports or pipelines on the same tables we use in the Studio demo.” Add the partner’s doc link if useful.

4. **Optional: connect one partner**  
   If you have access, connect one partner (e.g. Looker Studio, which is first-party but may appear in the list) to the demo project and build a simple report on `pnl_daily` or `daily_prices`. Document the connection steps so others can repeat.

## Demo data used

- Dataset: `bq_studio_demo` (and optionally `bq_studio_demo_staging`).  
- Tables: any demo tables the partner reads (e.g. for a BI report).  
- No schema changes; Partner Center is discovery and optional integration.

## References

- [BigQuery Ready Partners](https://cloud.google.com/bigquery/docs/bigquery-ready-overview#partner_center)  
- Partner-specific docs (from Partner Center links)
