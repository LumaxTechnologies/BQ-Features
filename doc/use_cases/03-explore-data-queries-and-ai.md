# Use case 3: Explore data (structured queries and AI-assisted analytics)

## Goal

**Explore** the available data using **structured SQL queries** and **AI-assisted analytics** (Gemini in BigQuery Studio, data canvas) so analysts can discover patterns and prepare for ETL or reporting.

## Context

Analysts need to understand content, quality, and relationships before building ETLs or models. BigQuery Studio offers the query editor (and saved queries), the data canvas (natural language + Gemini), and notebooks.

## Demo resources

- **Dataset:** `bq_studio_demo` with tables `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions` (from `bqdemo deploy infra --with-demo-data`).
- **SQL scripts:** `bq_studio_demos/sql/` (e.g. `01_portfolio_value.sql`, `02_returns_and_volatility.sql`, `03_pnl_by_strategy.sql`) — run in the query editor or upload as saved queries.
- **Notebook:** `bq_studio_demos/notebooks/finance_analytics_demo.ipynb` — load tables, compute returns, plot PnL.
- **Docs:** `bq_studio_demos/docs/gemini-in-bigquery-studio.md` for enabling and using Gemini.
- **Feature docs:** [features/1-studio/](../features/1-studio/) (queries, data canvas, notebooks).

## Steps

### 1. Run structured demo queries

- Open **BigQuery Studio** → **SQL query**.
- Paste or open content from `bq_studio_demos/sql/01_portfolio_value.sql` (replace project/dataset with yours). Run and inspect results.
- Do the same for `02_returns_and_volatility.sql` and `03_pnl_by_strategy.sql` to explore returns and PnL by strategy.

### 2. Save and share queries (optional)

Save each as a **saved query** (Save button, name, region). They will appear under **Explorer → Queries**. Use **Share** to grant teammates **Code Viewer** or **Code Editor**. See [code-writing-sharing.md](../code-writing-sharing.md).

### 3. Use Gemini for ad-hoc exploration

- In the query editor, use the **Gemini** assist. Try prompts such as:
  - “List all tables in `bq_studio_demo`.”
  - “Daily returns by symbol from `daily_prices`.”
  - “Total PnL by strategy and date from `pnl_daily`.”
- Run the generated SQL and iterate (e.g. add filters, rounding). See `bq_studio_demos/docs/gemini-in-bigquery-studio.md`.

### 4. Use the data canvas

- **Create new** → **Data canvas**.
- Add a **Search** or **Table** node for `portfolio_holdings` and `daily_prices`. Add a **SQL** node with a Gemini prompt: “Join holdings and prices and compute market value by date.” Add a **Visualization** node (e.g. line chart of market value over time). See [data-canvas.md](../features/1-studio/data-canvas.md).

### 5. Use the finance notebook

- Upload and open `bq_studio_demos/notebooks/finance_analytics_demo.ipynb` (or use `bqdemo upload-to-studio`). Set the project and dataset in the first cells, then run: load tables → time series and returns → PnL bar chart. See [notebooks.md](../features/1-studio/notebooks.md).

## What you get

- Familiarity with the demo schema and content.
- Saved queries and/or a notebook for reuse.
- Experience with Gemini and the data canvas for exploration.

## Next

- **Use case 4:** Create ETLs that move and transform data from GCS into BQ (multiple layers).
- **Use case 6:** Share and version those ETLs.
