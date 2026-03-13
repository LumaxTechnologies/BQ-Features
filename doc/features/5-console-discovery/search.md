# Search (Preview)

## What it is

The **Search** page (Preview) lets you search for Google Cloud resources from BigQuery using natural language or keywords. You find datasets, tables, and other assets without browsing the Explorer tree.

## Demo doc

Use Search to find the demo dataset and its tables by natural language (e.g. “tables with symbol and date”, “PnL”, “portfolio”). This demonstrates discovery for analysts who may not know exact project/dataset names.

## Demo material

1. **Open Search**  
   In BigQuery → **Search** (Preview). If the feature is not available, document that and use the standard Explorer search or catalog search instead.

2. **Search for demo data**  
   Try queries such as:
   - “tables with symbol and date”
   - “portfolio holdings”
   - “daily prices”
   - “PnL by strategy”
   - “bq_studio_demo”
   Confirm that `bq_studio_demo` and its tables (and views if any) appear in the results.

3. **Open a result**  
   Click a result (e.g. `bq_studio_demo.daily_prices`) and confirm it opens in the details pane or query editor. Run a quick `SELECT * FROM ... LIMIT 5` to verify access.

4. **Combine with Gemini**  
   After finding a table via Search, open a new SQL query and use Gemini to “generate a query for daily returns from daily_prices”. Show the flow: Search → find table → Query + Gemini → run.

5. **Document**  
   Note which search phrases worked best for the demo dataset. Add them to your team’s “how to find the demo” instructions.

## Demo data used

- Dataset: `bq_studio_demo`.  
- Tables: `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.  
- No schema changes; search is read-only discovery.

## References

- [Search for resources](https://cloud.google.com/bigquery/docs/search-resources)
