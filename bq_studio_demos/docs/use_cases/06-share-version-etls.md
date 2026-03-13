# Use case 6: Share and version ETLs

## Goal

**Share** and **version** ETL definitions (Dataform, saved queries, data preparations) so the team can collaborate, review changes, and roll back if needed.

## Context

ETLs are code: SQL, SQLX, and configs. They should live in version control (Git) and be shareable via IAM. BigQuery Studio and Dataform both use repositories and workspaces for this.

## What you can write and where it lives

| Asset | Description | Where it lives |
|-------|-------------|----------------|
| **Queries** | Single or multi-statement GoogleSQL (SELECT, DDL, DML). Ad-hoc (unsaved) or saved. | Query editor (session) or **repository** (saved query). |
| **Stored procedures** | Named routines in a dataset: procedural logic (variables, IF/WHILE, parameters). Called with `CALL dataset.procedure_name(args)`. | **Dataset** (as a routine). Source can be versioned in a repo or Terraform. |
| **Dataform assets** | SQLX tables, views, operations (custom SQL, including `CALL` to procedures). | **Dataform repository** (Git). |
| **Notebooks** | Python + SQL (Colab Enterprise); versioned and shareable. | **Repository**. |

For **Studio** repos (saved queries, notebooks, data prep), see [repositories.md](../features/1-studio/repositories.md). For **Dataform** (pipeline execution and scheduling), see below and [dataform.md](../features/2-pipelines-integration/dataform.md).

## Tools for ETL: stored procedures, Dataform, Terraform

### Stored procedures (dataset objects)

- **What:** Created with **CREATE [OR REPLACE] PROCEDURE** in the query editor or via **Terraform** (`google_bigquery_routine`). Live in a **dataset**; called with `CALL project.dataset.procedure_name(args)`.
- **Track/version:** BigQuery does **not** store version history of procedure DDL. Keep the **CREATE PROCEDURE** script in a **Dataform repo** (e.g. as an operation or in a migrations folder) or in **Terraform** and apply via CI/CD.
- **Share:** IAM on dataset (e.g. BigQuery Data Viewer/Editor) so users can `CALL` the procedure. For **least privilege** (procedure runs with owner’s table access): use **authorized routines** so callers don’t need direct table access.
- **Use for:** Parameterized, multi-step logic; encapsulation; reuse from other queries or from Dataform/Cloud Scheduler.

### Dataform (SQLX, operations, Git)

- **What:** Dataform repos contain **SQLX** (tables, views, assertions) and **operations** (arbitrary SQL, including `CALL dataset.procedure_name()`). Can be the single source of truth for DDL (e.g. procedures) and transformation DML.
- **Track/version:** **Git** (native). Connect repo to GitHub; use branches and PRs.
- **Share:** IAM on the Dataform/BQ repository; execution runs as configured service account.
- **Use for:** Versioned pipelines, dependency graphs, scheduling (workflow configs), and running stored procedures on a schedule (operation that does `CALL`).

### Terraform / CI-CD

- **What:** **Terraform** (`google_bigquery_routine`) or scripts that run **CREATE OR REPLACE PROCEDURE** (e.g. via `bq` or client libs) in a pipeline.
- **Track/version:** Terraform state + Git for `.tf` and SQL files.
- **Share:** Procedures are shared via dataset IAM and authorized routines; who can change them is controlled by who can run Terraform/CI.
- **Use for:** Infrastructure-as-code for procedures; strict change control and audit.

## Tracking and versioning (summary)

| Tool / asset | How versioning works | Best practice |
|--------------|----------------------|----------------|
| **Saved queries** | Version history in repo; Git if repo linked to GitHub. | Save queries that matter; link repo to Git for team history. |
| **Stored procedures** | No BQ-native history. Procedure body is the current deployment only. | Keep **source of truth** in Git: Dataform (SQLX/operation) or Terraform + SQL file, and deploy from there. |
| **Dataform** | Git-only. | One Dataform repo per “product” or domain; use branches and tags for releases. |
| **Notebooks** | Same as saved queries (repo + optional Git). | Save and share via repo; use Git for important notebooks. |

## Sharing (summary)

| Asset | How sharing works |
|-------|-------------------|
| **Saved query / notebook** | IAM on the asset or on the **repository**: **Code Viewer** (view/run), **Code Editor** (edit/run), **Code Owner** (delete, manage). Users also need **BigQuery Job User** and **BigQuery Read Session User** to run queries. |
| **Stored procedure** | **Dataset IAM**: grant **BigQuery Data Viewer** (or **Editor**) so users can `CALL` the procedure. For **least privilege**: add procedure as **authorized routine** on the target dataset so callers don’t need direct table access. |
| **Dataform / repo** | **Repository**-level IAM (Code Viewer/Editor/Owner). Execution identity is the service account configured for the Dataform run. |

## Which tool to use for what

| Goal | Recommended tool | Reason |
|------|------------------|--------|
| One-off or exploratory SQL | **Query editor** (untitled) | No need to save; fast. |
| Reusable SQL for people to run or edit | **Saved query** in a **repository** | Version history, IAM sharing, visible in Explorer → Queries. |
| Parameterized or multi-step business logic | **Stored procedure** in a dataset | Variables, control flow, IN/OUT args; callable from SQL and Dataform. |
| Version and deploy procedure DDL | **Dataform** (operation or SQLX) or **Terraform** | Git history and controlled deploys; BQ does not version procedure DDL. |
| Schedule a stored procedure | **Dataform** (operation with `CALL`) + workflow config, or **Cloud Scheduler + Cloud Functions** | Native scheduled queries cannot `CALL`; Dataform or Cloud Functions can. |
| Full DAG of transforms + optional procedures | **Dataform** (SQLX + operations) | Dependencies, order, and scheduling in one place. |
| Python + SQL, shareable analysis | **Notebook** in a repo | Colab Enterprise, versioned and shared like saved queries. |
| Strict change control and audit for procedures | **Terraform** or **CI/CD** running DDL from Git | Single source of truth in Git; all changes via pipeline. |

## Best practices

1. **Save anything reusable** — Don’t leave important SQL only in untitled tabs. Save as a **saved query** or put it in a **Dataform** repo so it’s versioned and shareable.
2. **Put repos on Git** — Link BigQuery repositories to **GitHub** (or GitLab/Bitbucket). Use Git for history, branches, and code review.
3. **Version procedure source outside BQ** — Store **CREATE PROCEDURE** in **Dataform** (e.g. operation or dedicated SQLX) or in **Terraform** + SQL in Git, and deploy from there.
4. **Use authorized routines for least privilege** — When a procedure reads/writes tables that callers shouldn’t access directly, mark it as an **authorized routine** on those datasets.
5. **One repo per team or domain** — Keeps Queries/Notebooks/Dataform assets easy to find and share.
6. **Name and document** — Give saved queries and procedures clear names and a short description (in the asset or in a README in the repo).
7. **Schedule procedures via Dataform or Cloud Scheduler** — Use a **Dataform operation** that runs `CALL ...` and schedule it with a workflow config, or use **Cloud Scheduler + Cloud Functions**. Native “scheduled query” cannot `CALL`.

## Demo resources

- **Repositories (Studio):** [repositories.md](../features/1-studio/repositories.md) (create repo, link to GitHub via HTTPS or SSH, share).
- **Dataform:** [dataform.md](../features/2-pipelines-integration/dataform.md).
- **Saved queries:** [queries.md](../features/1-studio/queries.md).

## Steps

### 1. Put ETL SQL and Dataform in a repo

- **Studio:** Create a BigQuery **repository** (Explorer → Repositories → Add). Create a **workspace**. Add or paste your ETL SQL (and optionally the procedure DDL) as files in the workspace. Commit and push.
- **Dataform:** Use a **Dataform repository** (linked from BQ or the Dataform console). Develop in a **development workspace**. Put all SQLX operations (GCS load, staging → refined, procedure call) in `definitions/`. Commit and push to the workspace; connect the repo to **GitHub** (or GitLab) so pushes go to a remote branch.

### 2. Link the repo to GitHub

- For the **Studio repo:** In the repo’s **Configuration** tab → **Connect with Git** → add GitHub URL and credentials (HTTPS with a personal access token, or SSH with a key stored in Secret Manager). Full steps (token/SSH creation, Secret Manager, Dataform service agent) are in [repositories.md](../features/1-studio/repositories.md) (section “Create a repository and link to GitHub”).
- For the **Dataform repo:** Same idea in the Dataform repo settings. Push from the workspace to the default branch (e.g. `main`).

### 3. Share the repo with the team

- **Studio repo:** Open actions → **Share** → add users/groups and grant **Code Viewer** (read), **Code Editor** (edit/run), or **Code Owner** (manage). Teammates see the same Queries/Notebooks backed by the repo.
- **Dataform repo:** Share at the repository level (IAM on the Dataform repo resource) so others can open workspaces, edit, and run. Use branches in Git for feature work; merge after review.

### 4. Version and review

- Use **Git branches** for new ETL logic or changes. In Dataform, create a workspace from a branch; develop and test; then open a pull request on GitHub. After merge, run or schedule from the main branch.
- Use **version history** in Studio for saved queries (revert or branch from a version). For Dataform, Git tags or release branches can mark “releases” of the ETL.

### 5. Document

- Add a short README in the repo (or in `doc/use_cases/`) describing the ETL layers, how to run them, and how to add a new operation or procedure. Point to the use case docs (4, 5, 7, 8) for load, procedures, schedule, and monitor.

## What you get

- ETL definitions in a Git-backed repo (Studio and/or Dataform).
- Shared access via IAM; collaboration and review via Git.
- Clear path to scheduling (use case 7) and monitoring (use case 8) the same ETLs.

## Next

- **Use case 7:** Schedule the ETLs (Dataform workflow config or scheduled query).
- **Use case 8:** Monitor runs and troubleshoot.

## References

- [Work with SQL stored procedures](https://cloud.google.com/bigquery/docs/procedures)
- [Authorized routines](https://cloud.google.com/bigquery/docs/authorized-routines)
- [Create and manage repositories](https://cloud.google.com/bigquery/docs/repositories)
- [Share saved queries](https://cloud.google.com/bigquery/docs/work-with-saved-queries#share_saved_query)
- [Dataform: Create operations](https://cloud.google.com/dataform/docs/custom-sql)
- [Scheduling queries](https://cloud.google.com/bigquery/docs/scheduling-queries) (limitation: no `CALL`)
