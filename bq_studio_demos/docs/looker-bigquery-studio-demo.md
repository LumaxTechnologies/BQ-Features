# Looker dashboards for BigQuery Studio demo

This demo uses BigQuery datasets populated by the BQ-Features CLI. You can connect Looker to the same project and build dashboards on top of these tables.

## 1. Connect Looker to BigQuery

- In **Looker** > **Admin** > **Connections**, add a **BigQuery** connection.
- Use the same GCP **project** as your BigQuery Studio demo.
- Choose **Standard SQL** and the same **dataset** (e.g. `bq_studio_demo`).
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
  sql_table_name: `bq-features-489714.bq_studio_demo.daily_prices` ;;

  dimension: symbol { label: "Symbol" }
  dimension: date { type: time type: date sql: `${TABLE}.date` ;; }
  measure: close_avg { type: avg sql: `${close}` ;; format_value: "%.2f" }
  measure: volume_total { type: sum sql: `${TABLE}.volume` ;; }
}
```

After saving, create explores and build dashboards in Looker. For full setup, refer to [Looker BigQuery documentation](https://cloud.google.com/looker/docs/setup-with-bigquery).
