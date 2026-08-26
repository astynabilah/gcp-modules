-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 2. Batch serving with a scheduled query

SELECT
  score_date,
  COUNT(*)                              AS customers_scored,
  COUNTIF(risk_tier = 'High')           AS high_risk,
  ROUND(AVG(p_churn), 4)                AS avg_score,
  MAX(scored_at)                        AS last_run
FROM `telco_churn.churn_scores_history`
GROUP BY score_date
ORDER BY score_date DESC;
