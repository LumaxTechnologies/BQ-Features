# Use case 8: Monitor ETLs

## Goal

**Monitor** ETL runs (scheduled queries, Dataform workflows) so the team can see success/failure, duration, and resource usage, and can troubleshoot and alert on failures.

## Context

Scheduled and ad-hoc ETL jobs produce BigQuery jobs and (for Dataform) execution logs. Monitoring uses the Jobs explorer, admin resource charts, Cloud Monitoring, and optional alerting.

## Demo resources

- **Administration:** [monitoring.md](../features/4-administration/monitoring.md), [jobs.md](../features/4-administration/jobs.md).
- **Demo jobs:** After scheduled queries or Dataform runs are configured and executed, jobs will appear in the Jobs explorer and in resource charts.
- **Cloud Logging / Monitoring:** For Dataform, execution logs and (if configured) alerting on failure.

## Steps

### 1. Jobs explorer

- **BigQuery** → **Administration** → **Jobs** (or Jobs explorer).
- Filter by **Project** (your demo project), **Job type** (Query, Load), **Time range**. Find the scheduled query run (e.g. `daily_pnl_summary` refresh) and any Dataform-triggered jobs.
- Open a job to see **SQL**, **Execution graph**, **Bytes processed**, **Slot time**, **Errors**. Use this to debug failed or slow runs.

### 2. Admin resource charts

- In **Administration** → **Monitoring** (or resource charts), view **Bytes processed**, **Job duration**, **Errors**, **Slot usage** over time. Correlate spikes with your ETL schedule (e.g. daily 06:00).

### 3. Dataform execution logs

- In the **Dataform** repo, open **Executions** (or the run history). Select a run and inspect which actions succeeded or failed, and the compiled SQL for each. Use this to fix broken operations or procedure calls.

### 4. Cloud Monitoring and alerting (optional)

- In **Cloud Monitoring**, create a dashboard with BigQuery metrics (e.g. job count, bytes processed, errors) for your project. Filter by job label or transfer config name if you label them.
- Create an **alerting policy** that fires when a scheduled query or Dataform run fails (e.g. on error count or on a log-based metric). Send notifications to email or a channel.

### 5. Document runbooks

- In `doc/use_cases/` or the repo README, note: where to look for ETL jobs (Jobs explorer, Dataform Executions), how to interpret resource charts, and how to get alerted on failure. Link to this use case doc.

## What you get

- Visibility into ETL job success, duration, and cost.
- A path to alerting and runbooks for the financial team.

## No-code / AI alternatives (BI analysts and non-developers)

Monitoring in BigQuery is UI-driven; no code is required:

- **Jobs explorer:** In **BigQuery** → **Administration** → **Jobs**, filter by project, time range, and job type (Query, Load). Open any job to see SQL, duration, bytes processed, and errors. Use this to confirm scheduled data preparations and pipelines ran successfully or to debug failures.
- **Dataform / pipeline runs:** If you use **Dataform** or **Pipelines**, open **Executions** (or the run history) in the same console. Click a run to see which steps succeeded or failed and view logs. No scripts or APIs needed.
- **Cloud Monitoring and alerting:** In **Cloud Console** → **Monitoring**, use pre-built or custom dashboards for BigQuery (e.g. job count, errors, slot time). Create **alerting policies** in the UI: e.g. “Alert when query jobs fail” or “Alert when a specific transfer config fails.” Add notification channels (email, Slack, etc.) via the UI.

BI analysts and non-developers can own day-to-day monitoring and first-line troubleshooting using only the Console and Monitoring UIs; alerting can be configured without writing code.

## Next

- **Use case 9:** Add data science modelling on top of the same (or refined) data.
- **Use case 10:** Turn models into industrialized, scheduled processes.
