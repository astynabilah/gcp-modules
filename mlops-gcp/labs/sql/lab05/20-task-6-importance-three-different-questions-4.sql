-- Lab 5 — Feature engineering for tabular data
-- Task 6. Importance — three different questions

WITH gain AS (
  SELECT feature, importance_gain,
         RANK() OVER (ORDER BY importance_gain DESC) AS gain_rank
  FROM ML.FEATURE_IMPORTANCE(MODEL `telco_churn.model_v3`)
),
attr AS (
  SELECT feature, attribution,
         RANK() OVER (ORDER BY attribution DESC) AS attr_rank
  FROM ML.GLOBAL_EXPLAIN(MODEL `telco_churn.model_v3`)
)
SELECT
  COALESCE(g.feature, a.feature)        AS feature,
  g.gain_rank,
  a.attr_rank,
  g.gain_rank - a.attr_rank             AS rank_gap
FROM gain g
FULL OUTER JOIN attr a ON g.feature = a.feature
ORDER BY ABS(COALESCE(g.gain_rank - a.attr_rank, 0)) DESC
LIMIT 15;
