# BQ-Features: BigQuery Studio demo deployment CLI

CLI to deploy **BigQuery datasets**, **GCS buckets**, and **BigQuery Studio**–oriented demo material on a Google Cloud project. Use it to evaluate BigQuery Studio features with finance-focused sample data, notebooks, SQL scripts, optional Looker dashboards, and scheduled transformation tasks.

- [BQ-Features: BigQuery Studio demo deployment CLI](#bq-features-bigquery-studio-demo-deployment-cli)
  - [What gets deployed](#what-gets-deployed)
    - [1. Infrastructure (`deploy infra`)](#1-infrastructure-deploy-infra)
    - [2. Demo material (`deploy demos`)](#2-demo-material-deploy-demos)
  - [BigQuery concepts: data canvas, data preparations, pipelines](#bigquery-concepts-data-canvas-data-preparations-pipelines)
    - [Data canvas](#data-canvas)
  - [Data preparations](#data-preparations)
  - [Pipelines](#pipelines)
  - [Repositories](#repositories)
  - [Untitled vs shared resources (queries, notebooks)](#untitled-vs-shared-resources-queries-notebooks)
  - [Example contents (data canvas, data preparations, pipelines)](#example-contents-data-canvas-data-preparations-pipelines)
      - [Data canvas – example prompts and flow](#data-canvas--example-prompts-and-flow)
      - [Data preparations – example steps and outcome](#data-preparations--example-steps-and-outcome)
      - [Pipelines – example task DAG](#pipelines--example-task-dag)
  - [Prerequisites](#prerequisites)
  - [Authenticate with Google Cloud (do this first)](#authenticate-with-google-cloud-do-this-first)
    - [Why authenticate the gcloud CLI?](#why-authenticate-the-gcloud-cli)
    - [1. Install the gcloud CLI](#1-install-the-gcloud-cli)
    - [2. Log in and set Application Default Credentials](#2-log-in-and-set-application-default-credentials)
  - [Install](#install)
  - [Configuration](#configuration)
    - [Getting the Google Cloud project ID](#getting-the-google-cloud-project-id)
  - [Usage](#usage)
    - [Deploy infrastructure (datasets, bucket, demo data)](#deploy-infrastructure-datasets-bucket-demo-data)
    - [Deploy demo material (notebooks, SQL, docs, optional schedulers/Looker)](#deploy-demo-material-notebooks-sql-docs-optional-schedulerslooker)
  - [Using BigQuery Studio](#using-bigquery-studio)
    - [Using embedded GCP LLM (Gemini) in BigQuery Studio](#using-embedded-gcp-llm-gemini-in-bigquery-studio)
  - [Documentation helpers](#documentation-helpers)
  - [CLI examples](#cli-examples)
  - [Project layout after deploy](#project-layout-after-deploy)
  - [Options reference](#options-reference)
  - [License](#license)


## What gets deployed

### 1. Infrastructure (`deploy infra`)

- **BigQuery datasets**: main demo dataset and a staging dataset (e.g. `bq_studio_demo`, `bq_studio_demo_staging`).
- **GCS bucket**: one bucket for demo data and notebooks (e.g. `bq-studio-demo-<project_id>`).
- **Demo data** (optional): load bundled finance CSVs into BigQuery and upload the same files to GCS, or point to your own CSV directory.

### 2. Demo material (`deploy demos`)

- **SQL scripts**: runnable in BigQuery Studio (portfolio value, returns/volatility, PnL by strategy, load-from-GCS example).
- **Dataform operations**: SQLX operations that run against the demo data and materialize tables (`daily_pnl_summary`, `portfolio_value_snapshot`, `returns_volatility`). Copy into a Dataform repo to run or schedule.
- **Jupyter notebook**: finance analytics (load from BQ, time series, PnL charts); suitable for Vertex AI Workbench or Colab Enterprise.
- **Documentation**:
  - **Gemini in BigQuery Studio**: how to use the embedded GCP LLM to generate SQL, explain queries, and get insights.
  - **Use-case demos** ([doc/use_cases/](doc/use_cases/)): step-by-step demos for a financial analyst team (load raw data → BQ datasets → explore → ETL → stored procedures → share/version → schedule → monitor → data science → industrialize models). Uploaded to `gs://<bucket>/docs/use_cases/` when you run `bqdemo deploy demos`.
- **Optional**:
  - **Scheduled transformation tasks**: create a scheduled query that refreshes a summary table (e.g. daily PnL).
  - **Looker**: instructions and optional LookML snippet to connect Looker to the demo dataset and build dashboards.
  - **Upload notebooks to GCS**: for use in Vertex AI Workbench or Colab Enterprise.

## BigQuery concepts: data canvas, data preparations, pipelines

This section explains three BigQuery Studio concepts that the CLI’s demo material is designed to work with.

### Data canvas

**Data canvas** is an AI-powered analytics experience in BigQuery Studio (a [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-overview) feature). It lets you **find**, **transform**, **query**, and **visualize** data using natural language and a graphical workflow instead of writing SQL by hand.

- **Find data**: Use natural language or keyword search against [Dataplex Universal Catalog](https://docs.cloud.google.com/dataplex/docs/introduction) to discover tables, views, and materialized views.
- **Generate SQL**: Describe what you want in plain language; Gemini generates SQL (joins, filters, aggregations, etc.).
- **Visualize**: Request charts (bar, line, pie, scatter, heat map) from your result sets.
- **Workflow**: The canvas is a **DAG** (directed acyclic graph) of nodes: **Search** → **Table** → **SQL** → **Visualization** / **Insights** / **Destination**. You can branch, iterate, and save results to tables.

Data canvas is aimed at analysts and engineers who want to go from data to insights quickly; it is not meant for non-technical business users. The SQL scripts and demo tables deployed by this CLI are intended to be used in the query editor and in data canvas (e.g. “Show me portfolio value over time” against the demo dataset).

### Data preparations

**Data preparations** are BigQuery resources (powered by [Dataform](https://docs.cloud.google.com/dataform/docs/overview)) that implement **cleaning, transforming, and enriching** steps on your data. They are the building blocks for repeatable ETL-style workflows inside BigQuery.

- **AI-assisted**: Gemini suggests transformations (e.g. parsing dates, trimming strings, mapping schemas) based on a sample of your table. You apply, edit, or add steps in a **data view** and **graph view**.
- **Steps**: Typical steps include **Source** (BigQuery table), **Transformation** (SQL expressions), **Filter**, **Deduplicate**, **Validation**, **Join**, and **Destination** (output table).
- **Write modes**: You can run a data preparation in **full refresh**, **append**, **incremental**, or **upsert** mode to control how the destination table is updated.
- **Scheduling**: Data preparations can be run manually or on a schedule (via BigQuery scheduling / Dataform). The CLI’s optional “scheduled transformation tasks” create scheduled queries that refresh summary tables—conceptually similar to a single-step data preparation.

Data preparations are stored as **SQLX** assets and can live in a repository (for versioning) or standalone. They appear under **Explorer → Data preparations** in the BigQuery console.

### Pipelines

In BigQuery, **pipelines** are **orchestrated workflows** that run one or more tasks (e.g. SQL, data preparations, notebooks) in a defined order and optionally on a schedule.

- **BigQuery pipelines**: You create a pipeline from the BigQuery UI (**Create new → Pipeline**). A pipeline is a DAG of tasks (SQL queries, data preparation runs, notebook runs). The **[Data Engineering Agent](https://docs.cloud.google.com/bigquery/docs/data-engineering-agent-pipelines)** can generate or modify pipeline definitions from natural language; it produces SQLX code in a Dataform repository.
- **Pipeline vs data preparation**: A **data preparation** is a single ETL “job” (source → transform → destination). A **pipeline** composes multiple such jobs (and other tasks) and runs them in sequence or on a schedule. The CLI’s “scheduled transformation tasks” are one form of scheduled work; a full pipeline could chain several data preparations and SQL scripts.

### Repositories

**Repositories** in BigQuery Studio are Git-based containers for version-controlled code. They back saved queries, notebooks, pipelines, and data preparations that you see under **Explorer → Queries**, **Notebooks**, **Repositories**, etc.

- **What they are**: Each repository is a **Git repository**. BigQuery uses Git to record changes and manage file versions. You work inside **workspaces** (e.g. a default or branch-like workspace) to edit the files in the repo.
- **What lives in them**: Saved queries, notebooks, and other **code assets** are stored as files in a repository (powered by [Dataform](https://cloud.google.com/dataform/docs/overview)). When you save a query or upload a notebook, it is stored in a project repository (often an implicit/default one) in a chosen **region**.
- **Optional third-party Git**: A BigQuery repository can be connected to a remote Git repo (GitHub, GitLab, Bitbucket, Azure DevOps) via SSH or HTTPS. Then the code can be synced, pushed, and pulled like any Git repo; BigQuery still uses the Dataform service agent and Secret Manager for credentials.
- **Where to see them**: In the console, **Explorer → Repositories** lists your repositories. **Queries** and **Notebooks** in the Explorer are views over the same underlying assets (they may live in a default repo you don't manage explicitly).
- **Pricing and quotas**: Creating/updating/deleting repositories is free; [Dataform quotas](https://cloud.google.com/dataform/docs/quotas#quotas) apply. See [Introduction to repositories](https://cloud.google.com/bigquery/docs/repository-intro) and [Create and manage repositories](https://cloud.google.com/bigquery/docs/repositories).

### Untitled vs shared resources (queries, notebooks)

BigQuery Studio distinguishes between **untitled** (unsaved) and **saved** resources. Only saved resources can be **shared** and versioned.

| Aspect | **Untitled** (unsaved) | **Saved** (then optionally shared) |
|--------|------------------------|-----------------------------------|
| **Persistence** | Exists only in your current browser session. Closing the tab or losing the session loses the content unless you save. | Stored as a **code asset** in a repository (Dataform-backed). Survives closing the editor and is tied to the project and region. |
| **Naming** | Shown as "Untitled" (or "Untitled 1", etc.) in the tab. | Has a name you give when saving (or when uploading). |
| **Version history** | None. No history, no revert. | **Version history** is available: you can revert to or branch from previous versions; autosave appears as "Your changes" until you save a new version. |
| **Sharing** | Not shareable. Only you see it in your session. | **Shareable via IAM**: grant other users/groups **Code Viewer**, **Code Editor**, or **Code Owner** on the asset (or on the repository) so they can view, edit, or manage it. |
| **Visibility in Explorer** | Does not appear under **Queries** or **Notebooks** in the Explorer pane. | Appears under **Explorer → Queries** or **Explorer → Notebooks** (and in **Repositories** if you open the repo). |
| **Use case** | Quick ad-hoc SQL or notebook; try something without committing. | Reusable, collaborative, and auditable queries or notebooks; link from pipelines; share with the team. |

**Technical takeaway**: "Untitled" means the resource is **not** yet a first-class asset in a repository—it's session state in the UI. **Saving** (or uploading) creates that asset in a repository and unlocks versioning and IAM-based sharing. The same idea applies to queries and notebooks: save (or upload) to make them persistent and shareable.

Together, **data canvas** (ad-hoc analysis and visualization), **data preparations** (reusable transform jobs), and **pipelines** (orchestration) cover the flow from exploration to productionized data workflows in BigQuery Studio.

### Example contents (data canvas, data preparations, pipelines)

The following are **concrete examples of what you create or run inside BigQuery** for each feature—prompts, steps, and pipeline definitions—using the demo dataset (e.g. `bq_studio_demo.portfolio_holdings`, `daily_prices`, `transactions`, `pnl_daily`) after you deploy.

---

#### Data canvas – example prompts and flow

In the data canvas you work with **nodes** and **natural language prompts**. Examples:

| Where | Example prompt / action |
|--------|--------------------------|
| **Search node** | *“portfolio holdings and daily prices”* or *“tables with symbol and date”* → finds `portfolio_holdings`, `daily_prices` in the catalog. |
| **SQL node** (from table) | *“Join portfolio_holdings with daily_prices on symbol and date, and compute quantity times close as market_value”* → Gemini generates the JOIN and column expression. |
| **SQL node** (ad‑hoc) | *“Show total PnL by strategy and date from pnl_daily”* → generates `SELECT date, strategy, SUM(pnl), … GROUP BY date, strategy`. |
| **Visualization node** | *“Line chart of market value over as_of_date”* or *“Bar chart of total_pnl by strategy”* → creates the chart from the SQL result. |
| **Insights node** | *“Summarize trends in this result”* → generates a short summary. |
| **Destination node** | Save the SQL result to a table, e.g. `bq_studio_demo_staging.portfolio_value_snapshot`. |

**Example flow:** Search → add `portfolio_holdings` and `daily_prices` as table nodes → add SQL node with prompt above → add Visualization node → add Destination to persist the result. That is a full data-canvas workflow (find → query → visualize → save).

---

#### Data preparations – example steps and outcome

A **data preparation** is a sequence of steps that clean and transform a source table and write to a destination. Example for the demo table `transactions`:

| Step type | Example |
|-----------|---------|
| **Source** | `bq_studio_demo.transactions` (columns e.g. `symbol`, `quantity`, `price`, `txn_date`, …). |
| **Transformation** | Parse `txn_date` as DATE; add computed column `quantity * price AS notional`. |
| **Filter** | Keep rows where `quantity > 0` (or “Remove rows where quantity is null”). |
| **Deduplicate** | On keys `(symbol, txn_date, quantity, price)` with optional sort to keep latest. |
| **Validation** | “Fail if notional &lt; 0” → rows that fail go to an error table or fail the run. |
| **Destination** | `bq_studio_demo_staging.transactions_cleaned`, write mode **Incremental** on `txn_date` (or Full refresh). |

In the UI you get **suggestion cards** from Gemini (e.g. “Keep rows if quantity is not null”, “Parse txn_date as date”) that you apply or edit. The result is a single data preparation asset (stored as SQLX) you can run manually or on a schedule.

---

#### Pipelines – example task DAG

A **pipeline** orchestrates **multiple tasks** in order. Example with the demo dataset:

| Task order | Task type | Example |
|------------|-----------|---------|
| 1 | **Data preparation** | Run data preparation “Clean transactions” (e.g. the one above) → writes `transactions_cleaned`. |
| 2 | **SQL** | Run a query that builds `daily_pnl` from `transactions_cleaned` (e.g. aggregate by date/symbol). |
| 3 | **Data preparation** | Run data preparation “Enrich PnL with strategy” (join to a strategy lookup, write to `pnl_daily`). |

So the **pipeline** is: *Task 1 → Task 2 → Task 3* (each task is a BigQuery job: a data preparation run or a SQL execution). You define this DAG in **Create new → Pipeline**, add the three tasks, set dependencies, and optionally a schedule. The **Data Engineering Agent** can propose or modify this from prompts like: *“Create a pipeline that cleans transactions, then computes daily PnL, then enriches with strategy and writes to pnl_daily.”*

---

These examples use the tables created by `bqdemo deploy infra --with-demo-data` and `bqdemo deploy demos`. Replace dataset/table names with your project/dataset if different.

## Prerequisites

- Python 3.10+
- Google Cloud project with billing enabled.
- **APIs**: BigQuery API, Cloud Storage API; for scheduled queries, BigQuery Data Transfer API.
- **Authentication**: You must authenticate so that `bqdemo` can call Google Cloud APIs (see below).

---

## Authenticate with Google Cloud (do this first)

`bqdemo` talks to **BigQuery** and **Cloud Storage** on your behalf. Those APIs require proof of identity: every request must be authenticated. If you skip this step, you’ll see errors like *“Your default credentials were not found”* when running `bqdemo deploy infra`.

### Why authenticate the gcloud CLI?

Google client libraries (used by `bqdemo`) look for **Application Default Credentials (ADC)**. The easiest way to set ADC on your machine is with the **gcloud** CLI: the command `gcloud auth application-default login` signs you in via a browser and writes credentials to a standard location. Once that’s done, `bqdemo` (and other Google Cloud tools) can use those credentials automatically—no need to pass keys or tokens in config.

So the flow is: **install gcloud → run one auth command → then use bqdemo.**

### 1. Install the gcloud CLI

If you don’t have `gcloud` yet, install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) for your platform:

**Linux (Debian/Ubuntu)** – add the Cloud SDK repo and install:

```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
sudo apt-get update && sudo apt-get install google-cloud-cli
```

**Linux (RHEL/CentOS/Fedora)**:

```bash
sudo tee -a /etc/yum.repos.d/google-cloud-sdk.repo << EOM
[google-cloud-cli]
name=Google Cloud CLI
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el8-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOM
sudo yum install google-cloud-cli
```

**macOS** – with Homebrew:

```bash
brew install --cask google-cloud-sdk
```

Or use the [installer package](https://cloud.google.com/sdk/docs/install-sdk#mac) from the official docs.

**Windows** – use the [Google Cloud SDK installer](https://cloud.google.com/sdk/docs/install-sdk#windows) (download and run the executable).

Restart your terminal after installing, then check:

```bash
gcloud --version
```

### 2. Log in and set Application Default Credentials

Run:

```bash
gcloud auth application-default login
```

- A browser window opens so you can sign in with the **Google account that has access to your Cloud project**.
- After you approve, gcloud writes credentials to a well-known path on your machine.
- **bqdemo** (and the BigQuery/Storage libraries it uses) will automatically use these credentials—no extra config needed.

You only need to run this once per machine (or again if credentials expire or you switch accounts).

**Alternative (service account key):** If you prefer not to use your user account, create a service account in the Cloud Console, download a JSON key, and set:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

See [Set up Application Default Credentials](https://cloud.google.com/docs/authentication/external/set-up-adc) for more options.

## Install

From the repo root:

```bash
cd customers/Lumax/BQ-Features
pip install -e .
```

Or with a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
```

## Configuration

### Getting the Google Cloud project ID

You need the **project ID** (e.g. for `SERVICE_ACCOUNT_EMAIL` and `gcloud` commands). To get it from the web portal:

1. Open [Google Cloud Console](https://console.cloud.google.com) and sign in with the Google account that has access to the project.
2. In the top bar, click the **project selector** (it shows the current project name or “Select a project”).
3. In the dialog, either:
   - Pick the project from the list and note its **Project ID** (shown under the project name), or
   - Create a project with **New Project**, then copy the **Project ID** you set.
4. The **Project ID** is the value to use in config (e.g. `terraform-admin@YOUR_PROJECT_ID.iam.gserviceaccount.com`). It is not the same as the project *name* (the display label).

You can also see the current project ID in the **Dashboard** or in the **Project settings** (IAM & Admin → Settings) under “Project ID”.

Copy the example config and set your project ID:

```bash
cp bq_features_config.yaml.example bq_features_config.yaml
# Edit bq_features_config.yaml: set project_id to your GCP project ID.
```

Alternatively, set `GOOGLE_CLOUD_PROJECT` or pass `--project-id` on each command.

## Usage

### Deploy infrastructure (datasets, bucket, demo data)

```bash
# Default: create datasets, bucket, and load bundled finance demo data
bqdemo deploy infra

# Without demo data
bqdemo deploy infra --no-demo-data

# Load your own CSVs (table name = filename without .csv)
bqdemo deploy infra --csv-dir /path/to/csv/files

# Custom prefixes and region
bqdemo deploy infra --dataset-prefix my_demo --bucket-prefix my-bq-demo --region EU

# Dry run (no changes)
bqdemo deploy infra --dry-run
```

### Deploy demo material (notebooks, SQL, docs, optional schedulers/Looker)

```bash
# Generate demos and upload SQL, notebooks, and docs to the demo GCS bucket (default)
bqdemo deploy demos

# With scheduled queries and Looker instructions
bqdemo deploy demos --with-schedulers --with-looker

# Custom output directory (still uploads to GCS by default)
bqdemo deploy demos -o ./my_demos

# Skip GCS upload (write only to local output-dir)
bqdemo deploy demos --no-upload-to-gcs

# Upload SQL and notebooks into BigQuery Studio (browser automation)
bqdemo upload-to-studio
# Only SQL: bqdemo upload-to-studio --no-notebooks
# Only notebooks: bqdemo upload-to-studio --no-sql

# Dry run
bqdemo deploy demos --dry-run
```

By default, `deploy demos` uploads generated artifacts to your demo GCS bucket under `sql/`, `notebooks/`, and `docs/`. Run `bqdemo deploy infra` first so the bucket exists.

**Getting the demo SQL into BigQuery Studio:** Queries only appear under **Explorer → Queries** when you use the Studio UI (Google does not provide an API for that). Two options:

1. **Manual upload**  
   Run **`bqdemo deploy demos`**, then in **BigQuery Studio** → **Explorer** → your project → next to **Queries**, click **View actions** (⋮) → **Upload SQL query**. Browse to **`bq_studio_demos/sql/`**, select each `.sql` file, set **SQL name** and **Region** if needed, and click **Upload**. Repeat per file.

2. **Automated upload in the Studio UI**  
   After `bqdemo deploy demos`, run **`bqdemo upload-to-studio`**. This opens a browser and automates the same “Upload SQL query” and “Upload to Notebooks” flows so SQL files end up under **Queries** and notebooks under **Notebooks**. Requires: `pip install playwright && playwright install chromium`. You may need to sign in to Google Cloud in the browser once. Use `--no-notebooks` to upload only SQL, or `--no-sql` to upload only notebooks.

Alternatively, open and run SQL from **GCS**: `gs://<your-demo-bucket>/sql/*.sql` (after `deploy demos` with default GCS upload).

### Using BigQuery Studio

1. Open [Google Cloud Console](https://console.cloud.google.com) → **BigQuery** → **BigQuery Studio** (or SQL workspace).
2. **Run the demo SQL:** Use **Queries → View actions → Upload SQL query** and select files from **`bq_studio_demos/sql/`** (see “Getting the demo SQL into BigQuery Studio” above). Or open from GCS `gs://<bucket>/sql/*.sql` or paste from the local files.
3. Use **Gemini** in the editor to generate or explain SQL (see `bq_studio_demos/docs/gemini-in-bigquery-studio.md`).
4. For notebooks: open the generated `.ipynb` in **Vertex AI Workbench** or **Colab Enterprise** from the local folder or from GCS: `gs://<bucket>/notebooks/*.ipynb`.

### Using embedded GCP LLM (Gemini) in BigQuery Studio

The docs in `docs/gemini-in-bigquery-studio.md` (generated by `deploy demos`) describe how to:

- Enable and use Gemini in the BigQuery Studio SQL editor.
- Generate SQL from natural language (e.g. portfolio value, returns, PnL).
- Explain or fix existing queries.
- Use Gemini with Python in notebooks.

### CLI examples

You can print these from the CLI with `bqdemo examples`. Below, assume `project_id` is set in `bq_features_config.yaml` or passed via `--project-id`. Run `bqdemo deploy infra` first so datasets and the GCS bucket exist.

**Minimal setup (infra + demos, no schedulers or Looker):**

```bash
bqdemo deploy infra
bqdemo deploy demos --no-schedulers --no-looker
```

**Full demo with scheduled queries and Looker instructions:**

```bash
bqdemo deploy infra --with-demo-data
bqdemo deploy demos --with-schedulers --with-looker
```

**Use demos with data canvas:** After `deploy demos`, open BigQuery Studio and use the data canvas. Point a **Search** or **Table** node at the demo dataset (e.g. `bq_studio_demo`). Try prompts like “portfolio value by date” or “returns and volatility by symbol”; the demo tables (`portfolio_holdings`, `daily_prices`, etc.) are set up for this.

**Use demos with data preparations:** Load the demo tables with `deploy infra --with-demo-data`. In BigQuery Studio, go to **Explorer → Data preparations** and create a new data preparation from one of the demo tables (e.g. `transactions`). Use Gemini suggestions to clean or transform columns, then set a destination table (e.g. in `bq_studio_demo_staging`) and run or schedule it.

**Use demos with pipelines:** The scheduled query created by `deploy demos --with-schedulers` is a simple “pipeline” (one recurring SQL task). For a full pipeline (multiple data preparations + SQL), create a pipeline in the BigQuery UI (**Create new → Pipeline**) and add tasks that reference your data preparations and the SQL in `gs://<bucket>/sql/` (or the local `bq_studio_demos/sql/`).

**Custom region and prefixes:**

```bash
bqdemo deploy infra --region EU --dataset-prefix my_demo --bucket-prefix my-bq-demo
bqdemo deploy demos --dataset-prefix my_demo --bucket-prefix my-bq-demo
```

**Your own CSV data (table name = filename without `.csv`):**

```bash
bqdemo deploy infra --csv-dir /path/to/csv/files --no-demo-data
bqdemo deploy demos
```

**Generate demos locally only (no GCS upload):**

```bash
bqdemo deploy demos --no-upload-to-gcs -o ./my_demos
```

### Documentation helpers

**Inject project ID into docs (for easy copy/paste):**  
Copy the `doc/` tree into a new folder and replace placeholders (`YOUR_PROJECT`, `<project_id>`, bucket names) with your actual project ID:

```bash
bqdemo docs inject-project-id
# Output: doc_with_project/ (same structure as doc/)
# Custom: bqdemo docs inject-project-id --output-dir ./doc_filled --bucket-prefix my-bq-demo
```

**Export docs to .docx for SharePoint:**  
Mirror `doc/` to `doc_export/` and convert every `.md` file to `.docx` (same structure), ready to upload to SharePoint:

```bash
bqdemo docs export-docx
# Output: doc_export/ (e.g. doc_export/README.docx, doc_export/use_cases/01-load-raw-data-to-gcs.docx, ...)
# Requires pandoc (e.g. apt install pandoc, brew install pandoc, or https://pandoc.org/installing.html)
```

## Project layout after deploy

**Local** (default: `bq_studio_demos/`):

```
bq_studio_demos/
├── sql/                  # SQL for BigQuery Studio query editor
│   ├── 01_portfolio_value.sql
│   ├── 02_returns_and_volatility.sql
│   ├── 03_pnl_by_strategy.sql
│   └── 04_load_from_gcs.sql
├── dataform/             # Dataform operations (run on demo data)
│   ├── README.md
│   └── definitions/operations/
│       ├── refresh_daily_pnl_summary.sqlx
│       ├── refresh_portfolio_value_snapshot.sqlx
│       └── refresh_returns_volatility.sqlx
├── notebooks/
│   └── finance_analytics_demo.ipynb
└── docs/
    ├── gemini-in-bigquery-studio.md
    └── looker-bigquery-studio-demo.md   # if --with-looker
```

**GCS** (when `--upload-to-gcs` is set, default): the same files are uploaded to `gs://<bucket>/sql/`, `gs://<bucket>/dataform/`, `gs://<bucket>/notebooks/`, and `gs://<bucket>/docs/`.

## Options reference

| Option | Description |
|--------|-------------|
| `--config`, `-c` | Path to YAML config (default: `bq_features_config.yaml` or `BQ_FEATURES_CONFIG`). |
| `--project-id` | GCP project (overrides config and `GOOGLE_CLOUD_PROJECT`). |
| `--region` | BigQuery region (e.g. `US`, `EU`). |
| `--with-demo-data` / `--no-demo-data` | Load bundled finance CSVs (infra). |
| `--csv-dir` | Directory of CSV files to load (infra). |
| `--with-schedulers` / `--no-schedulers` | Create scheduled query (demos). |
| `--with-looker` / `--no-looker` | Emit Looker instructions and LookML (demos). |
| `--upload-to-gcs` / `--no-upload-to-gcs` | Upload SQL, notebooks, and docs to the demo GCS bucket (demos; default: on). |

**Docs commands:** `bqdemo docs inject-project-id` copies `doc/` to a folder (default `doc_with_project/`) with `YOUR_PROJECT` and `<project_id>` replaced by your project ID for easy copy/paste. `bqdemo docs export-docx` mirrors `doc/` to `doc_export/` as `.docx` files (requires [pandoc](https://pandoc.org/installing.html)) for SharePoint upload.

**Upload to Studio:** The command **`bqdemo upload-to-studio`** runs a Playwright script that automates the Studio “Upload SQL query” and “Upload to Notebooks” flows so demo SQL files appear under **Explorer → Queries** and notebooks under **Explorer → Notebooks**. Requires: `pip install playwright && playwright install chromium`. Use `--no-notebooks` or `--no-sql` to upload only one type.

## License

MIT (see LICENSE).
