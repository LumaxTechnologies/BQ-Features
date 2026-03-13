# Use case 6: Share and version ETLs

## Goal

**Share** and **version** ETL definitions (Dataform, saved queries, data preparations) so the team can collaborate, review changes, and roll back if needed.

## Context

ETLs are code: SQL, SQLX, and configs. They should live in version control (Git) and be shareable via IAM. BigQuery Studio and Dataform both use repositories and workspaces for this.

## Demo resources

- **Repositories (Studio):** [repositories.md](../features/1-studio/repositories.md), [create-bq-repo-and-link-github.md](../create-bq-repo-and-link-github.md).
- **Dataform:** Git-backed repo; workspaces for editing; push to GitHub for review and CI. [dataform.md](../features/2-pipelines-integration/dataform.md), [code-writing-sharing.md](../code-writing-sharing.md).
- **Saved queries:** Version history in the repo; share via Code Viewer/Editor/Owner. [queries.md](../features/1-studio/queries.md).

## Steps

### 1. Put ETL SQL and Dataform in a repo

- **Studio:** Create a BigQuery **repository** (Explorer → Repositories → Add). Create a **workspace**. Add or paste your ETL SQL (and optionally the procedure DDL) as files in the workspace. Commit and push.
- **Dataform:** Use a **Dataform repository** (linked from BQ or the Dataform console). Develop in a **development workspace**. Put all SQLX operations (GCS load, staging → refined, procedure call) in `definitions/`. Commit and push to the workspace; connect the repo to **GitHub** (or GitLab) so pushes go to a remote branch.

### 2. Link the repo to GitHub

- For the **Studio repo:** Configuration → Connect with Git → add GitHub URL and credentials (HTTPS token or SSH). See [create-bq-repo-and-link-github.md](../create-bq-repo-and-link-github.md).
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
