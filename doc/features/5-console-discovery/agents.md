# Agents (Preview)

## What it is

**Data agents** (Preview) let you create and chat with agents that answer questions about BigQuery resources using natural language (conversational analytics). You define which tables or metadata the agent can use.

## Demo doc

Create an agent that has access to the demo dataset (`bq_studio_demo`) and ask it questions about portfolio value, PnL, and returns. Use it to show conversational analytics on the demo data.

## Demo material

1. **Open Agents**  
   In BigQuery → **Agents** (Preview). If the feature is not available, note it in your doc and skip to “Document for your team”.

2. **Create an agent**  
   Create a new data agent. Name it e.g. “Demo finance agent”. In the configuration, **select the demo dataset** (and optionally specific tables): `bq_studio_demo` with `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`. Add a short description and any use-case instructions (e.g. “Answer questions about portfolio value, daily returns, and PnL by strategy”).

3. **Chat with the agent**  
   Start a conversation. Ask in natural language:
   - “What is the total portfolio market value by date?”
   - “Show me PnL by strategy.”
   - “Which symbols have the highest volatility in the last 20 days?”
   Confirm the agent returns or suggests queries that use the demo tables and that you can run the suggested SQL.

4. **Run suggested SQL**  
   Use the agent’s “Run” or “Open in editor” to execute the suggested query. Verify results against the demo dataset.

5. **Share (optional)**  
   If the UI allows, share the agent with a teammate so they can ask the same demo questions. Document how to create and share agents for your org.

## Demo data used

- Dataset: `bq_studio_demo`.  
- Tables: `portfolio_holdings`, `daily_prices`, `pnl_daily`, `transactions`.  
- No schema changes; agent only reads metadata and generates/queries SQL.

## References

- [Create data agents](https://cloud.google.com/bigquery/docs/create-data-agents)  
- [Conversational analytics](https://cloud.google.com/bigquery/docs/conversational-analytics)
