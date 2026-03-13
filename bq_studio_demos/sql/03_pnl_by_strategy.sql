-- PnL by strategy and date (aggregated)
-- Use in scheduled queries or ad-hoc in Studio

SELECT
  date,
  strategy,
  SUM(CAST(pnl AS FLOAT64)) AS total_pnl,
  COUNT(*) AS num_records
FROM `bq-features-489714.bq_studio_demo.pnl_daily`
GROUP BY date, strategy
ORDER BY date, strategy;
