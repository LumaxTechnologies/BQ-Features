# BQ-Features documentation

This folder contains **feature-level demo docs** (by first-level and second-level BigQuery feature), **use-case oriented demos** (financial analyst workflow), and **general guides**. For the **list and descriptions of BigQuery features**, see **[big-query-features.md](big-query-features.md)**. That doc also links to the demo material for each feature in the [features/](features/) folder. For **end-to-end use cases** (load raw data → ETL → version → schedule → monitor → data science → industrialization), see **[use_cases/](use_cases/)**.

**Prerequisites:** Run `bqdemo deploy infra --with-demo-data` and `bqdemo deploy demos` so the demo dataset and assets (SQL, notebooks, Dataform operations) exist.

---

## General docs (top-level)

| Doc | Description |
|-----|-------------|
| [big-query-features.md](big-query-features.md) | First-level and second-level BigQuery features (what they are) and links to demo docs in [features/](features/). |
| [code-writing-sharing.md](code-writing-sharing.md) | Writing, tracking, versioning, and sharing queries and stored procedures; which tool to use when. |
| [create-bq-repo-and-link-github.md](create-bq-repo-and-link-github.md) | Create a BigQuery repository and link it to GitHub (HTTPS and SSH). |

---

## Use-case demos (financial analyst team)

| Doc | Description |
|-----|-------------|
| [use_cases/](use_cases/) | End-to-end demos in order: load raw data to GCS, load from BQ datasets, explore (queries + AI), create ETLs, stored procedures, share/version, schedule, monitor, data science modelling, industrialize models. One markdown doc per use case; uploaded to GCS with `bqdemo deploy demos`. |

---

## Demo data reference

All feature docs assume the following are available after `bqdemo deploy infra --with-demo-data` and `bqdemo deploy demos`:

- **Dataset:** `bq_studio_demo` (or your `dataset_prefix`).
- **Tables:** `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.
- **Optional outputs:** `daily_pnl_summary`, `portfolio_value_snapshot`, `returns_volatility` (from Dataform operations or scheduled query).
- **Staging dataset:** `bq_studio_demo_staging` (for data prep destinations, policy-tag demos, etc.).
- **GCS bucket:** `gs://bq-studio-demo-<project_id>/` (demo_data/, sql/, dataform/, notebooks/, docs/, docs/use_cases/).

Replace `YOUR_PROJECT` and `YOUR_DEMO_BUCKET` in the doc examples with your project ID and bucket name.
