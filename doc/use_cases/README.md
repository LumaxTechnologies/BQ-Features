# Use-case oriented demos (financial analyst team)

These demos follow a typical workflow for a **financial department analyst team**: from loading raw data into the cloud through ETL, versioning, scheduling, monitoring, and data science to industrialized models.

**Order of use cases:**

| # | Use case | Doc |
|---|----------|-----|
| 1 | Load raw data (CSV, Excel) into GCS | [01-load-raw-data-to-gcs.md](01-load-raw-data-to-gcs.md) |
| 2 | Load formatted data from pre-filled BQ datasets | [02-load-formatted-data-from-bq-datasets.md](02-load-formatted-data-from-bq-datasets.md) |
| 3 | Explore data (structured queries and AI-assisted analytics) | [03-explore-data-queries-and-ai.md](03-explore-data-queries-and-ai.md) |
| 4 | Create ETLs: raw GCS → BQ (multiple transformation layers) | [04-create-etls-gcs-to-bq-layers.md](04-create-etls-gcs-to-bq-layers.md) |
| 5 | Include stored procedures in ETLs | [05-include-stored-procedures-in-etls.md](05-include-stored-procedures-in-etls.md) |
| 6 | Share and version ETLs | [06-share-version-etls.md](06-share-version-etls.md) |
| 7 | Schedule ETLs | [07-schedule-etls.md](07-schedule-etls.md) |
| 8 | Monitor ETLs | [08-monitor-etls.md](08-monitor-etls.md) |
| 9 | Data science modelling on data | [09-data-science-modelling.md](09-data-science-modelling.md) |
| 10 | Industrialize data science models | [10-industrialize-data-science-models.md](10-industrialize-data-science-models.md) |

**Prerequisites:** Run `bqdemo deploy infra --with-demo-data` and `bqdemo deploy demos` so the demo bucket, dataset, and artifacts exist. Use case docs are uploaded to the demo GCS bucket when you run `bqdemo deploy demos` (with default upload).
