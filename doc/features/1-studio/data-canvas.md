# Data canvas

## What it is

**Data canvas** is an AI-assisted flow in BigQuery Studio: search for data → add tables → generate SQL (with Gemini) → add visualization, insights, or destination. It’s a graph-based DAG (nodes and natural language) instead of writing SQL by hand.

## Demo doc

Use the demo dataset in the data canvas to go from search to SQL to visualization without writing SQL yourself. Tables `portfolio_holdings`, `daily_prices`, and `pnl_daily` are discoverable and work well with Gemini prompts.

## Demo material

1. **Open data canvas**  
   In BigQuery Studio → **Home** → **Create new** → **Data canvas** (or open from the tab bar).

2. **Search for demo data**  
   Add a **Search** node. In natural language, try: “portfolio holdings and daily prices” or “tables with symbol and date”. Select the demo dataset and add `portfolio_holdings` and `daily_prices` as table nodes.

3. **Generate SQL**  
   Add a **SQL** node. Prompt: “Join portfolio_holdings with daily_prices on symbol and date, and compute quantity times close as market_value.” Let Gemini generate the JOIN. Run the node and check results.

4. **Add visualization**  
   Add a **Visualization** node from the SQL result. Prompt: “Line chart of market value over as_of_date” or “Bar chart of total market value by symbol.” Confirm the chart reflects demo data.

5. **PnL flow**  
   Add a **Search** or **Table** node for `pnl_daily`. Add a **SQL** node: “Total PnL by strategy and date from pnl_daily.” Add **Visualization**: “Bar chart of total_pnl by strategy.”

6. **Save to table (optional)**  
   Add a **Destination** node to write the SQL result to a table (e.g. in `bq_studio_demo_staging`) for reuse.

## Demo data used

- Dataset: `bq_studio_demo`.  
- Tables: `portfolio_holdings`, `daily_prices`, `pnl_daily`.  
- Optional staging: `bq_studio_demo_staging` for destination.

## References

- [Data canvas](https://cloud.google.com/bigquery/docs/data-canvas)  
- Main README: “Data canvas – example prompts and flow”
