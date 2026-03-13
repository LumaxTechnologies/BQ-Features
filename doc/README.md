# BQ-Features documentation

This folder contains **feature-level demo docs** (by first-level and second-level BigQuery feature), **use-case oriented demos** (financial analyst workflow), and **general guides**. For the **list and descriptions of BigQuery features**, see **[big-query-features.md](big-query-features.md)**. That doc also links to the demo material for each feature in the [features/](features/) folder. For **end-to-end use cases** (load raw data → ETL → version → schedule → monitor → data science → industrialization), see **[use_cases/](use_cases/)**.

**Prerequisites:** The demo dataset, demo data, and assets (SQL, notebooks, Dataform operations) must exist (e.g. created by your project’s deployment process).

---

## General docs (top-level)

| Doc | Description |
|-----|-------------|
| [big-query-features.md](big-query-features.md) | First-level and second-level BigQuery features (what they are) and links to demo docs in [features/](features/). |

**Create a BQ repo and link to GitHub:** See [features/1-studio/repositories.md](features/1-studio/repositories.md) (section “Create a repository and link to GitHub”) for step-by-step HTTPS (personal access token) and SSH (key in Secret Manager).

**Writing, tracking, versioning, and sharing code:** Covered in [features/1-studio/repositories.md](features/1-studio/repositories.md) (Studio repos, saved queries, notebooks) and [use_cases/06-share-version-etls.md](use_cases/06-share-version-etls.md) (ETL sharing/versioning, stored procedures, Dataform, which tool to use when).

---

## Use-case demos (financial analyst team)

| Doc | Description |
|-----|-------------|
| [use_cases/](use_cases/) | End-to-end demos in order: load raw data to GCS, load from BQ datasets, explore (queries + AI), create ETLs, stored procedures, share/version, schedule, monitor, data science modelling, industrialize models. One markdown doc per use case; may be uploaded to GCS as part of the project’s deployment. |

---

## Demo data reference

All feature docs assume the following are available (after your project’s deployment):

- **Dataset:** `bq_studio_demo` (or your `dataset_prefix`).
- **Tables:** `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.
- **Optional outputs:** `daily_pnl_summary`, `portfolio_value_snapshot`, `returns_volatility` (from Dataform operations or scheduled query).
- **Staging dataset:** `bq_studio_demo_staging` (for data prep destinations, policy-tag demos, etc.).
- **GCS bucket:** `gs://bq-studio-demo-<project_id>/` (demo_data/, sql/, dataform/, notebooks/, docs/, docs/use_cases/).

Replace `YOUR_PROJECT` and `YOUR_DEMO_BUCKET` in the doc examples with your project ID and bucket name.
