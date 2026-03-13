# Use case 8: Monitor ETLs

## Goal

**Monitor** ETL runs (scheduled queries, Dataform workflows) so the team can see success/failure, duration, and resource usage, and can troubleshoot and alert on failures.

## Context

Scheduled and ad-hoc ETL jobs produce BigQuery jobs and (for Dataform) execution logs. Monitoring uses the Jobs explorer, admin resource charts, Cloud Monitoring, and optional alerting.

## Demo resources

- **Administration:** [monitoring.md](../features/4-administration/monitoring.md), [jobs.md](../features/4-administration/jobs.md).
- **Demo jobs:** After running `bqdemo deploy demos --with-schedulers` and triggering a Dataform run, jobs will appear in the Jobs explorer and in resource charts.
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

## Next

- **Use case 9:** Add data science modelling on top of the same (or refined) data.
- **Use case 10:** Turn models into industrialized, scheduled processes.
