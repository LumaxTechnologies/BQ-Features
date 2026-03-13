# Jobs

## What it is

The **Jobs explorer** (administrative) lets you list, filter, inspect, and cancel BigQuery jobs. You see execution details, SQL, and resource usage. Useful for troubleshooting and cost control.

## Demo doc

Use the jobs created by running the demo SQL and Dataform operations to practice filtering, inspecting, and (if needed) killing a long-running or mistaken job.

## Demo material

1. **Open Jobs explorer**  
   In BigQuery → **Administration** → **Jobs** (or **Jobs explorer**). You may need **BigQuery Resource Viewer** or admin role.

2. **Run demo jobs**  
   Run a few queries from the demo: e.g. `01_portfolio_value.sql`, `03_pnl_by_strategy.sql`, and trigger the Dataform operations that refresh `daily_pnl_summary` and `portfolio_value_snapshot`. Leave the Jobs explorer open or refresh.

3. **Filter jobs**  
   Filter by **Project** (your demo project), **Job type** (Query, Load, etc.), **User**, and **Time range**. Find your recent demo queries and the Dataform/scheduled runs. Filter by **Status** (Success, Failed, Running).

4. **Inspect a job**  
   Click a completed query job. View **SQL**, **Execution graph**, **Bytes processed**, **Slot time**, and **Errors** (if any). Use this to explain how to debug a failed or slow query.

5. **Compare jobs (if supported)**  
   If the UI supports “Compare”, select two similar demo queries (e.g. two runs of portfolio value) and compare duration and slot usage. Show how to spot regressions.

6. **Cancel a job (optional)**  
   Start a long-running query (e.g. a cross join on the demo tables that returns many rows). In Jobs explorer, find the running job and **Cancel** it. Confirm the job stops and state updates.

## Demo data used

- Jobs from: running demo SQL scripts, Dataform operations, and scheduled query.  
- Dataset: `bq_studio_demo`.  
- No data changes; jobs are observed and optionally cancelled.

## References

- [Administrative jobs explorer](https://cloud.google.com/bigquery/docs/admin-jobs-explorer)  
- [Manage jobs](https://cloud.google.com/bigquery/docs/managing-jobs)
