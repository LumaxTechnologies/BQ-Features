"""Generate demo SQL, notebooks, and documentation."""

from __future__ import annotations

from pathlib import Path


def write_all_templates(
    output_dir: Path,
    project_id: str,
    dataset_id: str,
    bucket_name: str,
    region: str,
    with_looker: bool,
) -> None:
    """Write all demo artifacts to output_dir."""
    (output_dir / "sql").mkdir(parents=True, exist_ok=True)
    (output_dir / "notebooks").mkdir(parents=True, exist_ok=True)
    (output_dir / "docs").mkdir(parents=True, exist_ok=True)
    (output_dir / "dataform" / "definitions" / "operations").mkdir(parents=True, exist_ok=True)

    _write_sql_scripts(output_dir / "sql", project_id, dataset_id, bucket_name)
    _write_notebooks(output_dir / "notebooks", project_id, dataset_id, bucket_name)
    _write_docs(output_dir / "docs", project_id, dataset_id, bucket_name)
    _write_dataform_operations(output_dir / "dataform", project_id, dataset_id)
    if with_looker:
        _write_looker(output_dir / "docs", project_id, dataset_id)


def _write_sql_scripts(sql_dir: Path, project_id: str, dataset_id: str, bucket_name: str) -> None:
    """Write SQL scripts for BigQuery Studio query editor."""
    def tbl(name: str) -> str:
        return f"`{project_id}.{dataset_id}.{name}`"

    (sql_dir / "01_portfolio_value.sql").write_text(f"""-- Portfolio market value by snapshot date
-- Run in BigQuery Studio > SQL workspace

SELECT
  p.as_of_date,
  p.symbol,
  p.quantity,
  d.close AS price,
  p.quantity * d.close AS market_value
FROM {tbl('portfolio_holdings')} p
JOIN {tbl('daily_prices')} d
  ON p.symbol = d.symbol AND p.as_of_date = d.date
ORDER BY p.as_of_date, p.symbol;
""")

    (sql_dir / "02_returns_and_volatility.sql").write_text(f"""-- Daily returns and simple volatility (finance demo)
-- Uses daily_prices; replace with your own ticker table if needed

WITH daily_returns AS (
  SELECT
    symbol,
    date,
    close,
    LAG(close) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
    (close - LAG(close) OVER (PARTITION BY symbol ORDER BY date))
      / NULLIF(LAG(close) OVER (PARTITION BY symbol ORDER BY date), 0) AS daily_return
  FROM {tbl('daily_prices')}
)
SELECT
  symbol,
  date,
  ROUND(daily_return, 6) AS daily_return,
  ROUND(STDDEV(daily_return) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 20 PRECEDING AND CURRENT ROW), 6) AS volatility_20d
FROM daily_returns
WHERE daily_return IS NOT NULL
ORDER BY symbol, date;
""")

    (sql_dir / "03_pnl_by_strategy.sql").write_text(f"""-- PnL by strategy and date (aggregated)
-- Use in scheduled queries or ad-hoc in Studio

SELECT
  date,
  strategy,
  SUM(CAST(pnl AS FLOAT64)) AS total_pnl,
  COUNT(*) AS num_records
FROM {tbl('pnl_daily')}
GROUP BY date, strategy
ORDER BY date, strategy;
""")

    (sql_dir / "04_load_from_gcs.sql").write_text(f"""-- Example: load from GCS CSV into BigQuery (run after infra deploy)

-- LOAD DATA OVERWRITE not run here; use Console or bq load for first load.
-- Example DDL for external table (optional):

-- CREATE OR REPLACE EXTERNAL TABLE `{project_id}.{dataset_id}.daily_prices_external`
-- OPTIONS (
--   format = 'CSV',
--   uris = ['gs://{bucket_name}/demo_data/daily_prices.csv'],
--   skip_leading_rows = 1
-- );
""")


def _write_notebooks(
    notebooks_dir: Path, project_id: str, dataset_id: str, bucket_name: str
) -> None:
    """Write Jupyter notebook for finance analytics (graphs, BQ DataFrames)."""
    nb = {
        "nbformat": 4,
        "nbformat_minor": 4,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# BigQuery Studio – Finance demo notebook\n",
                    "\n",
                    "This notebook loads data from BigQuery and GCS, runs finance-oriented analyses, and displays graphs.\n",
                    "\n",
                    "**Data sources:**\n",
                    f"- BigQuery dataset: `{project_id}.{dataset_id}`\n",
                    f"- GCS bucket: `gs://{bucket_name}`\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 1. Connect to BigQuery and load tables as DataFrames"],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [
                    "# Run in Vertex AI Workbench or Colab Enterprise with google-cloud-bigquery and pandas\n",
                    "from google.cloud import bigquery\n",
                    "import pandas as pd\n",
                    "\n",
                    "client = bigquery.Client(project='" + project_id + "')\n",
                    "dataset = '" + dataset_id + "'\n",
                    "\n",
                    f"def bq_to_df(table: str):\n",
                    f"    return client.query(f\"SELECT * FROM `{project_id}.{dataset_id}`.{{table}}\").to_dataframe()\n",
                    "\n",
                    "prices = bq_to_df('daily_prices')\n",
                    "holdings = bq_to_df('portfolio_holdings')\n",
                    "pnl = bq_to_df('pnl_daily')\n",
                    "print(prices.head())\n",
                    "print(pnl.head())\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 2. Time series: close price and simple returns"],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [
                    "prices['date'] = pd.to_datetime(prices['date'])\n",
                    "prices = prices.sort_values(['symbol', 'date'])\n",
                    "prices['return'] = prices.groupby('symbol')['close'].pct_change()\n",
                    "\n",
                    "# Plot close prices (sample)\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "fig, ax = plt.subplots(figsize=(10, 4))\n",
                    "for sym in prices['symbol'].unique()[:3]:\n",
                    "    d = prices[prices['symbol'] == sym]\n",
                    "    ax.plot(d['date'], d['close'], label=sym)\n",
                    "ax.set_title('Close prices (sample symbols)')\n",
                    "ax.legend()\n",
                    "ax.set_xlabel('Date')\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 3. PnL over time (bar chart)"],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [
                    "pnl['date'] = pd.to_datetime(pnl['date'])\n",
                    "pnl['pnl_num'] = pd.to_numeric(pnl['pnl'], errors='coerce')\n",
                    "agg = pnl.groupby('date')['pnl_num'].sum().reset_index()\n",
                    "\n",
                    "fig, ax = plt.subplots(figsize=(10, 4))\n",
                    "ax.bar(agg['date'], agg['pnl_num'], color='steelblue', edgecolor='navy')\n",
                    "ax.set_title('Daily PnL (aggregate)')\n",
                    "ax.set_xlabel('Date')\n",
                    "ax.set_ylabel('PnL')\n",
                    "plt.xticks(rotation=45)\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Using Gemini in BigQuery Studio\n",
                    "\n",
                    "In **BigQuery Studio** you can use **Gemini** to:\n",
                    "- Generate SQL from natural language (e.g. \"total portfolio value by date\")\n",
                    "- Explain existing queries\n",
                    "- Fix errors and suggest optimizations\n",
                    "\n",
                    "See `docs/gemini-in-bigquery-studio.md` for step-by-step instructions.\n",
                ],
            },
        ],
    }

    import json
    (notebooks_dir / "finance_analytics_demo.ipynb").write_text(json.dumps(nb, indent=2))


def _write_docs(docs_dir: Path, project_id: str, dataset_id: str, bucket_name: str) -> None:
    """Write documentation (Gemini/LLM usage, how-to)."""
    (docs_dir / "gemini-in-bigquery-studio.md").write_text("""# Using embedded GCP LLM (Gemini) in BigQuery Studio

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

- “List all tables in the `""" + dataset_id + """` dataset.”
- “Query `""" + dataset_id + """.daily_prices` and compute daily returns by symbol.”
- “Join `portfolio_holdings` and `daily_prices` to get portfolio value by as_of_date.”
- “Summarize `pnl_daily` by date and strategy.”
""")


def _write_looker(docs_dir: Path, project_id: str, dataset_id: str) -> None:
    """Write Looker connection and dashboard instructions plus optional LookML."""
    (docs_dir / "looker-bigquery-studio-demo.md").write_text("""# Looker dashboards for BigQuery Studio demo

This demo uses BigQuery datasets populated by the BQ-Features CLI. You can connect Looker to the same project and build dashboards on top of these tables.

## 1. Connect Looker to BigQuery

- In **Looker** > **Admin** > **Connections**, add a **BigQuery** connection.
- Use the same GCP **project** as your BigQuery Studio demo.
- Choose **Standard SQL** and the same **dataset** (e.g. `""" + dataset_id + """`).
- Save and test the connection.

## 2. Expose the demo dataset

- In **Looker** > **Develop** > **Manage LookML Projects**, create or open a project.
- Add a **connection** that points to your BigQuery connection.
- Create a **model** that includes the demo dataset and persist derived tables in BigQuery if desired.

## 3. Example explores (conceptual)

- **portfolio_value**: join `portfolio_holdings` and `daily_prices` to show market value by date and symbol.
- **pnl_dashboard**: explore `pnl_daily` by date and strategy with sum of PnL.
- **prices**: explore `daily_prices` (open, high, low, close, volume) with time dimensions.

## 4. Optional LookML snippet (view)

You can define a view for `daily_prices` and use it in explores. Example (adapt to your connection name):

```lookml
view: daily_prices {
  sql_table_name: `""" + project_id + """.""" + dataset_id + """.daily_prices` ;;

  dimension: symbol { label: "Symbol" }
  dimension: date { type: time type: date sql: `${TABLE}.date` ;; }
  measure: close_avg { type: avg sql: `${close}` ;; format_value: "%.2f" }
  measure: volume_total { type: sum sql: `${TABLE}.volume` ;; }
}
```

After saving, create explores and build dashboards in Looker. For full setup, refer to [Looker BigQuery documentation](https://cloud.google.com/looker/docs/setup-with-bigquery).
""")


def _write_dataform_operations(dataform_dir: Path, project_id: str, dataset_id: str) -> None:
    """Write Dataform SQLX operations that run against the demo dataset."""
    def tbl(name: str) -> str:
        return f"`{project_id}.{dataset_id}.{name}`"

    # Refresh daily PnL summary (mirrors the scheduled query; can be run from Dataform)
    (dataform_dir / "definitions" / "operations" / "refresh_daily_pnl_summary.sqlx").write_text(
        f'''config {{
  type: "operations",
  description: "Refresh daily_pnl_summary from pnl_daily (demo data)"
}}

CREATE OR REPLACE TABLE {tbl('daily_pnl_summary')} AS
SELECT
  date,
  strategy,
  SUM(CAST(pnl AS FLOAT64)) AS total_pnl,
  COUNT(*) AS num_records
FROM {tbl('pnl_daily')}
GROUP BY date, strategy;
'''
    )

    # Portfolio value snapshot: materialize portfolio market value by date/symbol
    (dataform_dir / "definitions" / "operations" / "refresh_portfolio_value_snapshot.sqlx").write_text(
        f'''config {{
  type: "operations",
  description: "Materialize portfolio market value by snapshot date (from portfolio_holdings and daily_prices)"
}}

CREATE OR REPLACE TABLE {tbl('portfolio_value_snapshot')} AS
SELECT
  p.as_of_date,
  p.symbol,
  p.quantity,
  d.close AS price,
  p.quantity * d.close AS market_value
FROM {tbl('portfolio_holdings')} p
JOIN {tbl('daily_prices')} d
  ON p.symbol = d.symbol AND p.as_of_date = d.date
ORDER BY p.as_of_date, p.symbol;
'''
    )

    # Returns and volatility: materialize daily returns and 20d volatility
    (dataform_dir / "definitions" / "operations" / "refresh_returns_volatility.sqlx").write_text(
        f'''config {{
  type: "operations",
  description: "Materialize daily returns and 20d rolling volatility from daily_prices (demo data)"
}}

CREATE OR REPLACE TABLE {tbl('returns_volatility')} AS
WITH daily_returns AS (
  SELECT
    symbol,
    date,
    close,
    (close - LAG(close) OVER (PARTITION BY symbol ORDER BY date))
      / NULLIF(LAG(close) OVER (PARTITION BY symbol ORDER BY date), 0) AS daily_return
  FROM {tbl('daily_prices')}
)
SELECT
  symbol,
  date,
  ROUND(daily_return, 6) AS daily_return,
  ROUND(STDDEV(daily_return) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 20 PRECEDING AND CURRENT ROW), 6) AS volatility_20d
FROM daily_returns
WHERE daily_return IS NOT NULL
ORDER BY symbol, date;
'''
    )

    (dataform_dir / "README.md").write_text(
        f"""# Dataform operations for BQ Studio demo

These SQLX **operations** run against the demo dataset `{project_id}.{dataset_id}` (portfolio_holdings, daily_prices, pnl_daily). They materialize derived tables that you can query or expose in BI.

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
   In a Dataform development workspace, run the operations (single file or full workflow). They will create or replace the tables in `{project_id}.{dataset_id}`.

3. **Schedule**  
   Use a Dataform release config and workflow configuration to run these operations on a schedule (e.g. daily).

## Prerequisites

- Demo data must be loaded: run `bqdemo deploy infra --with-demo-data` so `portfolio_holdings`, `daily_prices`, and `pnl_daily` exist.
"""
    )
