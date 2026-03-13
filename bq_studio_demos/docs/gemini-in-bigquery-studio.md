# Using embedded GCP LLM (Gemini) in BigQuery Studio

BigQuery Studio integrates **Gemini for Google Cloud** to help you write and understand SQL and get insights without leaving the console.

## Enabling Gemini in BigQuery

1. **Open BigQuery Studio**
   - In Google Cloud Console, go to **BigQuery** > **BigQuery Studio** (or the SQL workspace).

2. **Start a new SQL query**
   - Click **+ SQL query** (or **Add** > **SQL query**).
   - In the editor, use the **Gemini** assist panel (often a sparkle or “Generate” button next to the editor).

3. **Generate SQL from natural language**
   - Type a comment or prompt in plain English, e.g.:
     - “Show me daily returns for each symbol in the daily_prices table”
     - “Total portfolio market value by as_of_date using portfolio_holdings and daily_prices”
   - Click **Generate** or use the inline suggestion. Gemini will propose a GoogleSQL query you can run or edit.

4. **Explain or fix existing SQL**
   - Select a query and ask Gemini to **Explain** it or **Fix** errors. Useful for learning and debugging.

5. **Python in notebooks**
   - In BigQuery Studio notebooks (Colab Enterprise), Gemini can also help with Python and BigQuery DataFrames (e.g. “load daily_prices and plot close by symbol”).

## Best practices

- **Reference your tables**: Mention dataset and table names in the prompt (e.g. `bq_studio_demo.daily_prices`) so Gemini can use the correct schema.
- **Iterate**: Run the generated query, then ask to “add a filter for symbol = 'AAPL'” or “round the returns to 4 decimals”.
- **Privacy**: Gemini for Google Cloud does not use your prompts or results to train public models unless you opt in.

## Quick prompts for this demo

- “List all tables in the `bq_studio_demo` dataset.”
- “Query `bq_studio_demo.daily_prices` and compute daily returns by symbol.”
- “Join `portfolio_holdings` and `daily_prices` to get portfolio value by as_of_date.”
- “Summarize `pnl_daily` by date and strategy.”
