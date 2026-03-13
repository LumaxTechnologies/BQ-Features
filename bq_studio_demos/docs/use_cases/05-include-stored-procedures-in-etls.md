# Use case 5: Include stored procedures in ETLs

## Goal

**Include stored procedures** in ETLs so that complex or parameterized logic (validation, multi-step updates, shared business rules) runs as part of the pipeline.

## Context

Stored procedures encapsulate logic that is awkward or impossible in a single SQL statement (variables, loops, conditional DDL/DML). BigQuery scheduled queries cannot call procedures; Dataform operations can. So ETLs that need procedures use **Dataform** (or Cloud Scheduler + Cloud Functions).

## Demo resources

- **Dataform operations:** Can run arbitrary SQL, including `CALL dataset.procedure_name();` See [06-share-version-etls.md](06-share-version-etls.md) and [dataform.md](../features/2-pipelines-integration/dataform.md).
- **Dataset:** `bq_studio_demo` (or staging) where you create the procedure and target tables.
- **Versioning:** Keep procedure DDL in a Dataform repo or Terraform so it is versioned (use case 6).

## Steps

### 1. Create a stored procedure in BQ

In the query editor (or a saved query), run:

```sql
CREATE OR REPLACE PROCEDURE `YOUR_PROJECT.bq_studio_demo.refresh_demo_summary`()
BEGIN
  -- Example: refresh an aggregated table
  CREATE OR REPLACE TABLE `YOUR_PROJECT.bq_studio_demo.daily_pnl_summary` AS
  SELECT date, strategy, SUM(CAST(pnl AS FLOAT64)) AS total_pnl
  FROM `YOUR_PROJECT.bq_studio_demo.pnl_daily`
  GROUP BY date, strategy;
END;
```

Replace `YOUR_PROJECT` with your project ID. Test with `CALL \`YOUR_PROJECT.bq_studio_demo.refresh_demo_summary\`();`

### 2. Add a Dataform operation that calls the procedure

In your Dataform repo (e.g. under `definitions/operations/`), add a `.sqlx` file:

```sql
config {
  type: "operations",
  description: "Call stored procedure to refresh demo summary"
}

CALL `YOUR_PROJECT.bq_studio_demo.refresh_demo_summary`();
```

Deploy this to the same Dataform repo you use for other ETL operations. When you run the Dataform workflow, this operation will execute the procedure.

### 3. Version the procedure DDL (recommended)

Keep the `CREATE PROCEDURE` script in the same Dataform repo (e.g. an operation that runs first, or a migrations folder) or in Terraform. That way the procedure definition is versioned and reproducible. See [06-share-version-etls.md](06-share-version-etls.md).

### 4. Use in a multi-step ETL

Order operations in Dataform so that: (1) tables are loaded or updated, (2) the operation that calls the procedure runs. The procedure can depend on tables built by earlier operations. Schedule the full workflow (use case 7).

## What you get

- A stored procedure in the demo dataset that performs a refresh (or validation step).
- A Dataform operation that invokes it, so the procedure runs as part of the ETL.
- A pattern for versioning procedure DDL and calling it from scheduled ETLs.

## Next

- **Use case 6:** Share and version the ETLs (including the procedure and the Dataform repo).
- **Use case 7:** Schedule the ETL (Dataform workflow that includes the procedure call).
