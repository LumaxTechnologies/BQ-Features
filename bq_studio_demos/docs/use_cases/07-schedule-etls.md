# Use case 7: Schedule ETLs

## Goal

**Schedule** ETLs so they run on a fixed cadence (e.g. daily) without manual triggers. Use BigQuery scheduled queries and/or Dataform workflow configurations.

## Context

Financial pipelines often run daily or intraday. BigQuery offers scheduled queries (Data Transfer Service) for single-query DDL/DML, and Dataform for multi-step workflows (including operations that call stored procedures).

## Demo resources

- **Scheduled query:** A scheduled query can refresh `daily_pnl_summary` from `pnl_daily` (e.g. daily at 06:00). Create one in **Pipelines and integration** → **Scheduled queries**, or use your project’s deployment to create it. Visible under **Pipelines and integration** → Scheduled queries.
- **Dataform:** Schedule a **workflow** that runs your release config (all or selected operations). [dataform.md](../features/2-pipelines-integration/dataform.md), [scheduled-queries.md](../features/2-pipelines-integration/scheduled-queries.md).
- **Stored procedures:** Scheduled queries cannot `CALL` procedures; use Dataform operations that call procedures and schedule the Dataform workflow. [doc/use_cases/05-include-stored-procedures-in-etls.md](05-include-stored-procedures-in-etls.md).

## Steps

### 1. Schedule a single query (demo)

Create a scheduled query that runs the `daily_pnl_summary` refresh (e.g. a query that inserts or replaces from `pnl_daily` into `daily_pnl_summary`). In **BigQuery** → **Pipelines and integration** → **Scheduled queries** (or **Data transfers**), create a new scheduled query, set the SQL and destination, and choose the schedule (e.g. daily at 06:00). Find the config to check the schedule and last run.

### 2. Schedule a Dataform workflow

- In the **Dataform** console, create a **release configuration** (compile from a branch).
- Create a **workflow configuration** that runs that release on a schedule (e.g. daily at 02:00). Attach a service account with access to the demo project and dataset.
- Save; the workflow will run at the set times. Confirm in **Executions** or in **Monitoring** (use case 8).

### 3. Add more scheduled queries (optional)

For other ETL steps that are plain DDL/DML (no `CALL`), create additional scheduled queries in the console or via the Data Transfer API: same project, same dataset, set destination table and schedule. Use parameterized queries (e.g. `@run_time`) if you need date-based partitioning.

### 4. Pipelines (Studio)

You can also create a **pipeline** in BigQuery Studio (Create new → Pipeline) that chains tasks (SQL, data prep, notebook). If the UI supports scheduling for pipelines, set a schedule there; otherwise use Dataform or scheduled queries for the actual runs.

## What you get

- At least one scheduled query (demo daily refresh) and optionally a Dataform workflow on a schedule.
- ETLs (and procedures invoked via Dataform) running without manual execution.

## No-code / AI alternatives (BI analysts and non-developers)

- **Schedule a data preparation:** Open your **data preparation** in BigQuery Studio → use **Schedule** (or **More** → **Schedule**). Set the frequency (e.g. daily, weekly) and time; the preparation will run and refresh the destination table without manual runs. No Dataform or transfer config setup required.
- **Schedule a saved query:** For a single query that refreshes a table, **Save** the query, then go to **Pipelines and integration** → **Scheduled queries** (or find **Schedule** on the saved query). Create a new scheduled query from that saved query and set the schedule in the UI.
- **Schedule a pipeline:** If you use a **Pipeline** (Create new → Pipeline) that chains data preparations and/or SQL tasks, use the pipeline’s **Schedule** option to run it on a cadence (e.g. daily at 06:00). All tasks in the pipeline run in order. No Dataform workflow or CLI needed.

BI analysts can schedule their data preparations and pipelines entirely from the BigQuery Studio and Cloud Console UIs.

## Next

- **Use case 8:** Monitor these ETLs (jobs, logs, alerts).
- **Use case 10:** Industrialize data science models (schedule retraining or prediction jobs).
