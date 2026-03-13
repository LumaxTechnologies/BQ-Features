# BigQuery: first-level and second-level features

Summary of the main feature areas in **Google Cloud BigQuery** as exposed in the console and documentation. First-level is the product/area; second-level is the set of capabilities under each.

---

## 1. BigQuery Studio

Unified analytics workspace for querying, building, and managing assets (SQL, notebooks, data prep, pipelines). Main entry in the console: **BigQuery** → **Studio**.

| Second-level feature | Description |
|----------------------|-------------|
| **Explorer** | Browse and manage **datasets**, **tables**, **views**, **routines** (UDFs, stored procedures), **job history** (personal and project). **Add data**: stream, CDC, load, or federate external data. |
| **Repositories** | Git-backed version control for code. Create repos, connect to GitHub/GitLab/Bitbucket, use **workspaces** to edit files. Stores saved queries, notebooks, and other code assets (Dataform-backed). |
| **Queries** | **Saved queries**: named, versioned SQL assets in a repo; shareable via IAM. **Query editor**: run ad-hoc or saved SQL; view results; use Gemini for generation. |
| **Notebooks** | Colab Enterprise notebooks (Python, SQL, DataFrames) with runtimes; versioned and shareable. **Spark notebooks** for Apache Spark workloads. |
| **Data canvas** | AI-assisted flow: search → table → SQL → visualization / insights / destination. Natural language and graph-based DAG (Gemini in BigQuery). |
| **Data preparations** | No-code/low-code ETL: source → transform (AI-suggested) → filter, dedupe, validate, join → destination. Stored as SQLX; run manually or on a schedule. |
| **Pipelines** | Create **pipelines** (DAGs of tasks: SQL, data prep, notebooks) from Studio; orchestrate and optionally schedule. Data Engineering Agent can generate pipeline definitions. |
| **Files** | Organize code assets (saved queries, notebooks) in **user and team folders** (Preview). |
| **Create new** | From Home: **SQL query**, **notebook**, **Spark notebook**, **data canvas**, **data preparation**, **pipeline**, **table**. |
| **Analytics & ML** | **BigQuery ML**: train and run models (e.g. linear, boosted tree, ARIMA, Vertex integration) via SQL. **BI Engine**: in-memory acceleration for dashboards. **Looker Studio / Looker**: connect to BQ for reporting and LookML models. |

**Demo docs:** [features/1-studio/](features/1-studio/) — [Explorer](features/1-studio/explorer.md) · [Repositories](features/1-studio/repositories.md) · [Queries](features/1-studio/queries.md) · [Notebooks](features/1-studio/notebooks.md) · [Data canvas](features/1-studio/data-canvas.md) · [Data preparations](features/1-studio/data-preparations.md) · [Pipelines](features/1-studio/pipelines.md) · [Files](features/1-studio/files.md) · [Create new](features/1-studio/create-new.md) · [Analytics & ML](features/1-studio/analytics-ml.md)

---

## 2. Pipelines & Integration

Configure recurring data movement, transformations, and scheduled execution. Console: **BigQuery** → **Pipelines and integration**.

| Second-level feature | Description |
|----------------------|-------------|
| **Data Transfers** | **BigQuery Data Transfer Service**: scheduled load from Cloud Storage, S3, Azure Blob, Google Ads, Display & Video 360, and many other sources into BQ. Also **dataset copy** and **scheduled query** execution (transfer configs). |
| **Dataform** | **Dataform repositories** (standalone or linked from BQ): develop SQLX/JS workflows, version in Git, compile and run in BigQuery. Schedule via workflow/release configs or Cloud Scheduler. |
| **Scheduled queries** | Recurring GoogleSQL (DDL/DML) via Data Transfer Service. Parameterize by date/time; set destination table. *Does not support `CALL` to stored procedures*; use Dataform operations or Cloud Scheduler + Cloud Functions for that. |
| **Connections** | **Connections** to external systems (Cloud SQL, etc.) and **federation** (external tables, BigLake) for querying without loading. |

**Demo docs:** [features/2-pipelines-integration/](features/2-pipelines-integration/) — [Data Transfers](features/2-pipelines-integration/data-transfers.md) · [Dataform](features/2-pipelines-integration/dataform.md) · [Scheduled queries](features/2-pipelines-integration/scheduled-queries.md) · [Connections](features/2-pipelines-integration/connections.md)

---

## 3. Governance

Data sharing, security, and metadata. Console: **BigQuery** → **Governance**.

| Second-level feature | Description |
|----------------------|-------------|
| **Data exchanges** | **Analytics Hub** / **BigQuery sharing**: create and manage **data exchanges** and **listings**; subscribe to shared datasets (zero-copy, read-only in your project). |
| **Data clean rooms** | **Data clean rooms**: multi-party analytics with privacy and policy controls; combine data without moving or exposing raw data (e.g. marketing, healthcare, finance). |
| **Policy tags** | **Column-level security** and **dynamic masking** via **policy tags** (Dataplex). Tag columns by sensitivity; IAM grants/denies by tag. |
| **Metadata curation** | **Automatic discovery**, **lineage**, and **metadata** (often through **Dataplex Universal Catalog**) for discovery, profiling, and compliance. |

**Demo docs:** [features/3-governance/](features/3-governance/) — [Data exchanges](features/3-governance/data-exchanges.md) · [Data clean rooms](features/3-governance/data-clean-rooms.md) · [Policy tags](features/3-governance/policy-tags.md) · [Metadata curation](features/3-governance/metadata-curation.md)

---

## 4. Administration

Operational control, capacity, and health. Console: **BigQuery** → **Administration**.

| Second-level feature | Description |
|----------------------|-------------|
| **Monitoring** | **Admin resource charts**: storage, bytes processed, job duration, errors, concurrency, shuffle, slot usage. **Cloud Monitoring** integration. |
| **Jobs** | **Jobs explorer**: list, filter, inspect, and cancel jobs; compare runs; view execution graph and SQL. |
| **Capacity / Reservations** | **Reservations** and **capacity commitment** for slots (flat-rate). **Reservations monitoring** for usage and assignment. |
| **Disaster recovery** | **Managed disaster recovery** (DR) for critical datasets (backup, restore). |
| **Recommendations** | **Recommendations**: optimize cost and performance (e.g. partitioning, clustering, slot usage). |

**Demo docs:** [features/4-administration/](features/4-administration/) — [Monitoring](features/4-administration/monitoring.md) · [Jobs](features/4-administration/jobs.md) · [Capacity / Reservations](features/4-administration/capacity-reservations.md) · [Disaster recovery](features/4-administration/disaster-recovery.md) · [Recommendations](features/4-administration/recommendations.md)

---

## 5. Console & discovery (other menu entries)

Additional BigQuery console entries that support discovery and setup.

| Second-level feature | Description |
|----------------------|-------------|
| **Agents** (Preview) | **Data agents**: create and chat with agents that answer questions about BQ resources using natural language (conversational analytics). |
| **Search** (Preview) | **Natural language search** for Google Cloud resources from BigQuery. |
| **Overview** (Preview) | **Overview** page: tutorials, get-started guides, release notes, role-based content (data admin, engineering, science, analysis). |
| **Settings** (Preview) | **Default configuration** and **UI settings** (e.g. default project, location, query options). |
| **Migration** | **Migration** to BigQuery: guides and setup for moving from other warehouses. |
| **Partner Center** | **Partner Center**: partner tools and services (e.g. ETL, BI) that work with BigQuery. |
| **Release notes** | **Release notes**: product updates and announcements. |

**Demo docs:** [features/5-console-discovery/](features/5-console-discovery/) — [Agents](features/5-console-discovery/agents.md) · [Search](features/5-console-discovery/search.md) · [Overview](features/5-console-discovery/overview.md) · [Settings](features/5-console-discovery/settings.md) · [Migration](features/5-console-discovery/migration.md) · [Partner Center](features/5-console-discovery/partner-center.md) · [Release notes](features/5-console-discovery/release-notes.md)

---

## References

- [Explore BigQuery in the Google Cloud console](https://cloud.google.com/bigquery/docs/bigquery-web-ui)
- [BigQuery Studio](https://cloud.google.com/bigquery/docs/query-overview#bigquery-studio)
- [Create and manage repositories](https://cloud.google.com/bigquery/docs/repositories)
- [Pipelines and connection page](https://cloud.google.com/bigquery/docs/pipeline-connection-page)
- [Introduction to data governance in BigQuery](https://cloud.google.com/bigquery/docs/data-governance)
- [Scheduling queries](https://cloud.google.com/bigquery/docs/scheduling-queries)
- [Introduction to BigQuery monitoring](https://cloud.google.com/bigquery/docs/monitoring)
