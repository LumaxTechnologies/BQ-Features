# Dataform

## What it is

**Dataform** repositories hold SQLX and JavaScript workflows that compile and run in BigQuery. You develop in workspaces, version in Git, and schedule runs via workflow/release configs or Cloud Scheduler.

## Demo doc

The CLI generates **Dataform operations** in `bq_studio_demos/dataform/definitions/operations/` that run against the demo dataset. Copy them into a Dataform repo to run or schedule refreshes of `daily_pnl_summary`, `portfolio_value_snapshot`, and `returns_volatility`.

## Demo material

1. **Create or open a Dataform repo**  
   In **BigQuery** → **Pipelines and integration** → **Dataform**, or open the Dataform console. Create a repository (or use an existing one) in the same project and region as your demo.

2. **Copy demo operations**  
   Copy the contents of `bq_studio_demos/dataform/definitions/operations/` into your Dataform repo’s `definitions/` tree (e.g. `definitions/operations/`). Ensure project/dataset in the SQL match your demo (`YOUR_PROJECT.bq_studio_demo`). The three operations:
   - `refresh_daily_pnl_summary.sqlx` → builds `daily_pnl_summary` from `pnl_daily`.
   - `refresh_portfolio_value_snapshot.sqlx` → builds `portfolio_value_snapshot` from `portfolio_holdings` and `daily_prices`.
   - `refresh_returns_volatility.sqlx` → builds `returns_volatility` from `daily_prices`.

3. **Open a workspace and run**  
   Create or open a development workspace. Compile and run the three operations (individually or as a workflow). Confirm the output tables exist in `bq_studio_demo` and have expected rows.

4. **Schedule (optional)**  
   Create a release config and a workflow configuration that runs these operations on a schedule (e.g. daily). Trigger a run and check execution logs.

5. **Link to GitHub**  
   Connect the Dataform repo to GitHub (see [repositories.md](../../features/1-studio/repositories.md), section “Create a repository and link to GitHub”, for HTTPS/SSH and Secret Manager; the same pattern applies to Dataform repos). Push the demo operations so they’re versioned and reviewable.

## Demo data used

- Input tables: `bq_studio_demo.pnl_daily`, `portfolio_holdings`, `daily_prices`.  
- Output tables: `daily_pnl_summary`, `portfolio_value_snapshot`, `returns_volatility` in the same dataset.

## References

- [Dataform overview](https://cloud.google.com/dataform/docs/overview)  
- [Create operations](https://cloud.google.com/dataform/docs/custom-sql)  
- [Schedule Dataform runs](https://cloud.google.com/dataform/docs/schedule-runs)  
- `bq_studio_demos/dataform/README.md`
