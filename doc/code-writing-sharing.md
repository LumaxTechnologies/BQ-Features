# Writing, tracking, versioning, and sharing code in BigQuery

This doc explains how to **write** SQL queries and stored procedures in BigQuery, and how to **track**, **version**, and **share** them using the available tools, with best practices and guidance on which tool to use when.

---

## 1. What you can write

| Asset | Description | Where it lives |
|-------|-------------|----------------|
| **Queries** | Single or multi-statement GoogleSQL (SELECT, DDL, DML). Can be ad-hoc (unsaved) or saved. | Query editor (session) or **repository** (saved query). |
| **Stored procedures** | Named routines in a dataset: procedural logic (variables, IF/WHILE, parameters). Called with `CALL dataset.procedure_name(args)`. | **Dataset** (as a routine object). Source can be versioned in a repo or Terraform. |
| **Notebooks** | Python + SQL (Colab Enterprise); versioned and shareable. | **Repository**. |
| **Dataform assets** | SQLX tables, views, operations (custom SQL, including `CALL` to procedures). | **Dataform repository** (Git). |

---

## 2. Tools available

### 2.1 Query editor (BigQuery Studio)

- **What**: Write and run SQL in the browser. **Untitled** = session-only; **Save** = creates a saved query in a repo.
- **Track/version**: No tracking for untitled; for saved queries, version history is in the repo (see Repositories).
- **Share**: Untitled is not shareable; saved queries are shared via IAM on the query or repo (Code Viewer / Code Editor / Code Owner).
- **Use for**: Ad-hoc exploration, one-off runs, and saving reusable queries for the team.

### 2.2 Saved queries (BigQuery Studio + repositories)

- **What**: Named SQL scripts stored as **code assets** in a BigQuery **repository** (Dataform-backed). Appear under **Explorer → Queries**.
- **Track/version**: **Version history** in the UI (revert, branch from a version). If the repo is linked to **Git** (GitHub/GitLab/Bitbucket), full Git history and branches.
- **Share**: **IAM**: grant **Code Viewer** (read), **Code Editor** (edit/run), or **Code Owner** (delete, manage permissions) on the query or the repository.
- **Use for**: Reusable SQL for analysts and engineers: reporting, transformations, and documentation. Not for procedural logic (use stored procedures) or scheduled `CALL` (use Dataform or Cloud Scheduler).

### 2.3 Repositories and workspaces

- **What**: **Repositories** are Git-backed containers. **Workspaces** are where you edit files (e.g. default branch or feature branch). Saved queries and notebooks live as files in a repo.
- **Track/version**: Git inside BQ + optional **connection to GitHub/GitLab/Bitbucket** for push/pull and external CI/CD.
- **Share**: Share at **repository** level (Code Viewer/Editor/Owner). Everyone with access sees the same Queries/Notebooks backed by that repo.
- **Use for**: Central place for all Studio code assets; link to GitHub for review and deployment.

**Repositories in Studio vs Dataform, and workspaces** — BigQuery has two repository concepts and both use workspaces:

| | **Repositories in BigQuery Studio** | **Repositories in Dataform** |
|--|-------------------------------------|------------------------------|
| **Where** | BigQuery console → Explorer → Repositories. | Dataform console (e.g. BigQuery → Dataform, or direct Dataform page). |
| **Purpose** | Store **Studio code assets**: saved queries, notebooks, data preparations, data canvases. Version control and sharing for analysts/engineers working in the Studio UI. | Store **Dataform pipeline** code: SQLX (tables, views, operations, assertions), JavaScript, `workflow_settings.yaml`. Used to **compile** and **run/schedule** workflows in BigQuery. |
| **Scheduling** | Assets created in a **Studio repo** (including “Dataform workflows” saved there) **cannot be scheduled for execution** from the BigQuery repo. To schedule pipeline runs, you use a **Dataform** repository and its workflow/release configs. | **Designed for execution**: create release configs, workflow configs; trigger runs from the Dataform UI or Cloud Scheduler. |
| **Workspaces** | **Workspaces** live *inside* a Studio repo. Each workspace is an editable copy (branch-like) where you change files; you commit and push to the repo (and optionally to GitHub). Same Git idea as Dataform. | **Development workspaces** live *inside* a Dataform repo. Each workspace is your own editable copy of the repo; you develop, compile, trigger runs, then commit/push. Multiple people can have different workspaces (e.g. feature branches) in the same repo. |
| **Workspace UI** | File list, edit files, version control; focused on queries, notebooks, data prep, data canvas. | Code tab (files, compile, dry run), **Compiled graph** tab (DAG), **Executions** tab (run logs). Pipeline-oriented. |

**Summary**: **Studio repositories** = version control and sharing for “everything you see in BigQuery Studio” (queries, notebooks, etc.); no pipeline scheduling from there. **Dataform repositories** = version control and execution for **SQLX pipelines** (tables, views, operations); you schedule and run from Dataform. **Workspaces** in both = your personal/edit copy of a repo (branch-style); in Dataform they also give you compile/run and execution logs.

### 2.4 Stored procedures (dataset objects)

- **What**: Created with **CREATE [OR REPLACE] PROCEDURE** in the query editor or via **Terraform** (`google_bigquery_routine`). Live in a **dataset**; called with `CALL project.dataset.procedure_name(args)`.
- **Track/version**: BigQuery does **not** store version history of procedure DDL. To version: keep the **CREATE PROCEDURE** script in a **Dataform repo** (e.g. as an operation or in a migrations folder) or in **Terraform** and apply via CI/CD.
- **Share**: **IAM on dataset** (e.g. BigQuery Data Viewer/Editor) so users can `CALL` the procedure. For **secure delegation** (procedure runs with owner’s table access): use **authorized routines** so callers don’t need direct table access.
- **Use for**: Parameterized, multi-step logic; encapsulation; reuse from other queries or from Dataform/Cloud Scheduler.

### 2.5 Dataform (SQLX, operations, Git)

- **What**: **Dataform** repos contain **SQLX** (tables, views, assertions) and **operations** (arbitrary SQL, including `CALL dataset.procedure_name()`). Can be the **single source of truth** for DDL (e.g. procedures) and transformation DML.
- **Track/version**: **Git** (native). Connect BQ repo or standalone Dataform repo to GitHub; use branches and PRs.
- **Share**: IAM on the Dataform/BQ repository; execution runs as configured service account.
- **Use for**: Versioned pipelines, dependency graphs, scheduling (workflow configs), and running stored procedures on a schedule (operation that does `CALL`).

### 2.6 Notebooks

- **What**: Colab Enterprise notebooks (Python, SQL, DataFrames) in BigQuery Studio. Saved in a **repository**.
- **Track/version**: Same as saved queries: version history in Studio; full Git if repo is linked.
- **Share**: Same IAM model (Code Viewer/Editor/Owner).
- **Use for**: Exploratory analysis, mix of SQL and Python, sharing analyses with the team.

### 2.7 Terraform / CI-CD

- **What**: **Terraform** (`google_bigquery_routine`) or scripts that run **CREATE OR REPLACE PROCEDURE** (e.g. via `bq` or client libs) in a pipeline.
- **Track/version**: Terraform state + Git for `.tf` and SQL files.
- **Share**: Procedures are shared via dataset IAM and authorized routines; who can change them is controlled by who can run Terraform/CI.
- **Use for**: Infrastructure-as-code for procedures (and other BQ objects); strict change control and audit.

---

## 3. Tracking and versioning (summary)

| Tool / asset | How versioning works | Best practice |
|--------------|----------------------|----------------|
| **Saved queries** | Version history in repo; Git if repo linked to GitHub etc. | Save queries that matter; link repo to Git for team history. |
| **Stored procedures** | No BQ-native history. Procedure body is the current deployment only. | Keep **source of truth** in Git: Dataform (SQLX/operation) or Terraform + SQL file, and deploy from there. |
| **Dataform** | Git-only (and BQ workspace history). | One Dataform repo per “product” or domain; use branches and tags for releases. |
| **Notebooks** | Same as saved queries (repo + optional Git). | Save and share via repo; use Git for important notebooks. |

---

## 4. Sharing (summary)

| Asset | How sharing works |
|-------|-------------------|
| **Saved query / notebook** | IAM on the asset or on the **repository**: **Code Viewer** (view/run), **Code Editor** (edit/run), **Code Owner** (delete, manage permissions). Users also need **BigQuery Job User** and **BigQuery Read Session User** to run queries. |
| **Stored procedure** | **Dataset IAM**: grant **BigQuery Data Viewer** (or **Editor**) so users can `CALL` the procedure. For **least privilege** (procedure accesses tables on behalf of owner): add procedure as **authorized routine** on the target dataset so callers don’t need direct table access. |
| **Dataform / repo** | **Repository**-level IAM (Code Viewer/Editor/Owner). Execution identity is the service account configured for the Dataform/BQ run. |

---

## 5. Which tool to use for what

| Goal | Recommended tool | Reason |
|------|-------------------|--------|
| One-off or exploratory SQL | **Query editor** (untitled) | No need to save; fast. |
| Reusable SQL for people to run or edit | **Saved query** in a **repository** | Version history, IAM sharing, visible in Explorer → Queries. |
| Parameterized or multi-step business logic | **Stored procedure** in a dataset | Variables, control flow, IN/OUT args; callable from SQL and Dataform. |
| Version and deploy procedure DDL | **Dataform** (operation or SQLX) or **Terraform** | Git history and controlled deploys; BQ does not version procedure DDL. |
| Schedule a stored procedure | **Dataform** (operation with `CALL`) + workflow config, or **Cloud Scheduler + Cloud Functions** | Native scheduled queries cannot `CALL`; Dataform or Cloud Functions can. |
| Full DAG of transforms + optional procedures | **Dataform** (SQLX + operations) | Dependencies, order, and scheduling in one place. |
| Python + SQL, shareable analysis | **Notebook** in a repo | Colab Enterprise, versioned and shared like saved queries. |
| Strict change control and audit for procedures | **Terraform** or **CI/CD** running DDL from Git | Single source of truth in Git; all changes via pipeline. |

---

## 6. Best practices

1. **Save anything reusable**  
   Don’t leave important SQL only in untitled tabs. Save as a **saved query** (or put it in a **Dataform** repo) so it’s versioned and shareable.

2. **Put repos on Git**  
   Link BigQuery repositories to **GitHub** (or GitLab/Bitbucket). Use Git for history, branches, and code review; use BQ for run and share.

3. **Version procedure source outside BQ**  
   BigQuery does not keep procedure history. Store **CREATE PROCEDURE** in **Dataform** (e.g. operation or dedicated SQLX) or in **Terraform** + SQL in Git, and deploy from there.

4. **Use authorized routines for least privilege**  
   When a procedure reads/writes tables that callers shouldn’t access directly, mark it as an **authorized routine** on those datasets so only the procedure needs table access.

5. **One repo per team or domain**  
   Keeps Queries/Notebooks/Dataform assets easy to find and share; avoid a single huge repo for everything.

6. **Name and document**  
   Give saved queries and procedures clear names and a short description (in the asset or in a README in the repo) so others know what to use.

7. **Schedule procedures via Dataform or Cloud Scheduler**  
   Use a **Dataform operation** that runs `CALL ...` and schedule it with a workflow config, or use **Cloud Scheduler + Cloud Functions** to run the procedure. Do not rely on native “scheduled query” for `CALL`.

---

## 7. References

- [Work with SQL stored procedures](https://cloud.google.com/bigquery/docs/procedures)
- [Authorized routines](https://cloud.google.com/bigquery/docs/authorized-routines)
- [Introduction to saved queries](https://cloud.google.com/bigquery/docs/saved-queries-introduction)
- [Create and manage repositories](https://cloud.google.com/bigquery/docs/repositories)
- [Share saved queries](https://cloud.google.com/bigquery/docs/work-with-saved-queries#share_saved_query)
- [Dataform: Create operations](https://cloud.google.com/dataform/docs/custom-sql)
- [Scheduling queries](https://cloud.google.com/bigquery/docs/scheduling-queries) (limitation: no `CALL`)
