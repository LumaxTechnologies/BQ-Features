# Recommendations

## What it is

**Recommendations** in BigQuery suggest optimizations for cost and performance: e.g. partitioning, clustering, materialized views, and slot usage. You review and apply them from the console or API.

## Demo doc

Use the demo dataset and its tables to see what recommendations BigQuery suggests (e.g. add partitioning to `daily_prices` or `pnl_daily`). Apply one recommendation if appropriate so the demo doubles as a small optimization example.

## Demo material

1. **Open Recommendations**  
   In BigQuery → **Administration** → **Recommendations** (or the equivalent entry). You may need **BigQuery Admin** or **Resource Viewer** at org/project level.

2. **View recommendations for the project**  
   List recommendations for your project. Filter or search for the demo dataset `bq_studio_demo`. Common suggestions: add **partitioning** (e.g. on `date` for `daily_prices` or `pnl_daily`), add **clustering**, or create a **materialized view** for a frequent query.

3. **Inspect one recommendation**  
   Open a recommendation (e.g. “Partition table `daily_prices` by column `date`”). Read the estimated impact (query cost reduction, storage). Note the exact DDL or steps suggested.

4. **Apply (optional)**  
   If you want the demo to show an optimized table: apply partitioning to one demo table (e.g. create `daily_prices_partitioned` with `PARTITION BY date` and backfill from `daily_prices`, or alter if supported). Re-run a demo query that filters by date and show the same results with lower bytes processed if the recommendation claimed savings. Document before/after.

5. **Document for your team**  
   List 2–3 recommendation types you saw for the demo dataset (e.g. partitioning, clustering, slot recommendation). Add links to the official recommendations docs so analysts know where to look in production.

## Demo data used

- Dataset: `bq_studio_demo`.  
- Tables: `daily_prices`, `pnl_daily` (typical candidates for partitioning by date).  
- Optional: new partitioned/clustered table for before/after comparison.

## References

- [Recommendations](https://cloud.google.com/bigquery/docs/recommendations-intro)  
- [Partitioned tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
