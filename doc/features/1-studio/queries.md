# Queries

## What it is

**Queries** in BigQuery Studio are saved SQL scripts (versioned, shareable via IAM) and the **query editor** where you run ad-hoc or saved SQL and use Gemini for generation. Saved queries live in a repository and appear under **Explorer → Queries**.

## Demo doc

Use the demo dataset to practice saving and running queries. The CLI generates `bq_studio_demos/sql/*.sql`; upload or paste them into Studio and save so they appear under Queries.

## Demo material

1. **Run a demo query**  
   In Studio, open **SQL query** (Home → Create new → SQL query). Paste the content of `bq_studio_demos/sql/01_portfolio_value.sql` (replace project/dataset with yours). Run it and confirm results from `portfolio_holdings` and `daily_prices`.

2. **Save as a saved query**  
   With the query open, click **Save** (or Ctrl+S). Name it e.g. `Portfolio value (demo)`, choose region, and save. It will appear under **Explorer → Queries**.

3. **Try Gemini**  
   In the same or a new query, add a comment like: “Total PnL by strategy and date from pnl_daily.” Use the Gemini assist to generate SQL. Run against `bq_studio_demo.pnl_daily`.

4. **Version history**  
   Open your saved query → **Version history** to see autosave and saved versions. Revert to a previous version if needed.

5. **Share**  
   Open the saved query → **Share** → **Manage permissions** → add a user with **Code Viewer** or **Code Editor** so they can view or edit it.

## Demo data used

- `bq_studio_demo.portfolio_holdings`, `bq_studio_demo.daily_prices`, `bq_studio_demo.pnl_daily`.  
- Demo SQL files: `01_portfolio_value.sql`, `02_returns_and_volatility.sql`, `03_pnl_by_strategy.sql`.

## References

- [Create saved queries](https://cloud.google.com/bigquery/docs/work-with-saved-queries)  
- [Introduction to saved queries](https://cloud.google.com/bigquery/docs/saved-queries-introduction)
