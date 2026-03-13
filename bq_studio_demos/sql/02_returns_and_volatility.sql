-- Daily returns and simple volatility (finance demo)
-- Uses daily_prices; replace with your own ticker table if needed

WITH daily_returns AS (
  SELECT
    symbol,
    date,
    close,
    LAG(close) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
    (close - LAG(close) OVER (PARTITION BY symbol ORDER BY date))
      / NULLIF(LAG(close) OVER (PARTITION BY symbol ORDER BY date), 0) AS daily_return
  FROM `bq-features-489714.bq_studio_demo.daily_prices`
)
SELECT
  symbol,
  date,
  ROUND(daily_return, 6) AS daily_return,
  ROUND(STDDEV(daily_return) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 20 PRECEDING AND CURRENT ROW), 6) AS volatility_20d
FROM daily_returns
WHERE daily_return IS NOT NULL
ORDER BY symbol, date;
