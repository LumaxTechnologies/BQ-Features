-- Portfolio market value by snapshot date
-- Run in BigQuery Studio > SQL workspace

SELECT
  p.as_of_date,
  p.symbol,
  p.quantity,
  d.close AS price,
  p.quantity * d.close AS market_value
FROM `bq-features-489714.bq_studio_demo.portfolio_holdings` p
JOIN `bq-features-489714.bq_studio_demo.daily_prices` d
  ON p.symbol = d.symbol AND p.as_of_date = d.date
ORDER BY p.as_of_date, p.symbol;
