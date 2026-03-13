# Monitoring

## What it is

**Monitoring** for BigQuery includes **admin resource charts** (storage, bytes processed, job duration, errors, concurrency, shuffle, slot usage) and **Cloud Monitoring** integration. You use it to watch health and usage at project or org level.

## Demo doc

After running demo queries, scheduled queries, and Dataform operations against the demo dataset, use the admin charts and Monitoring to show how to observe BigQuery usage and troubleshoot.

## Demo material

1. **Open Administration**  
   In BigQuery → **Administration**. Open **Monitoring** or **Resource charts** (or the equivalent in your console).

2. **Generate some load**  
   Run several demo queries (e.g. from `bq_studio_demos/sql/`) and the Dataform operations that build `daily_pnl_summary`, `portfolio_value_snapshot`, and `returns_volatility`. Optionally run the scheduled query once. This produces jobs and bytes processed.

3. **View resource charts**  
   In the admin view, check **Bytes processed**, **Job duration**, **Errors**, **Slot usage** (and **Concurrency** / **Shuffle** if shown). Filter by project or dataset. Confirm your demo jobs appear and note approximate bytes and duration.

4. **Cloud Monitoring**  
   Open **Cloud Monitoring** (or the linked dashboard). Find BigQuery metrics (e.g. `bigquery.googleapis.com`). Create or open a dashboard that shows bytes processed, job count, and errors for your project. Relate a spike to the demo runs.

5. **Storage**  
   In the admin charts or in the dataset **Details**, view **Storage** for `bq_studio_demo`. Show how much space the demo tables use. After running the Dataform operations, confirm storage includes the new tables.

## Demo data used

- Jobs from: demo SQL scripts, Dataform operations, scheduled query run.  
- Dataset: `bq_studio_demo` (storage and table list).  
- No schema changes; monitoring is read-only observation.

## References

- [Introduction to BigQuery monitoring](https://cloud.google.com/bigquery/docs/monitoring)  
- [Admin resource charts](https://cloud.google.com/bigquery/docs/admin-resource-charts)
