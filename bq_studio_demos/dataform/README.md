# Dataform operations for BQ Studio demo

These SQLX **operations** run against the demo dataset `bq-features-489714.bq_studio_demo` (portfolio_holdings, daily_prices, pnl_daily). They materialize derived tables that you can query or expose in BI.

## Generated operations

| File | Description | Output table |
|------|-------------|--------------|
| `definitions/operations/refresh_daily_pnl_summary.sqlx` | Aggregates pnl_daily by date and strategy | `daily_pnl_summary` |
| `definitions/operations/refresh_portfolio_value_snapshot.sqlx` | Joins portfolio_holdings and daily_prices for market value | `portfolio_value_snapshot` |
| `definitions/operations/refresh_returns_volatility.sqlx` | Daily returns and 20d rolling volatility from daily_prices | `returns_volatility` |

## How to use

1. **Copy into your Dataform repo**  
   Copy the `definitions/operations/` folder (and these `.sqlx` files) into your Dataform repository's `definitions/` tree. Ensure `workflow_settings.yaml` uses the same BigQuery project (and default dataset if you prefer refs).

2. **Run from Dataform**  
   In a Dataform development workspace, run the operations (single file or full workflow). They will create or replace the tables in `bq-features-489714.bq_studio_demo`.

3. **Schedule**  
   Use a Dataform release config and workflow configuration to run these operations on a schedule (e.g. daily).

## Prerequisites

- Demo data must be loaded: run `bqdemo deploy demos` so `portfolio_holdings`, `daily_prices`, and `pnl_daily` exist.
