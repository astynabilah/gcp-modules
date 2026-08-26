-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 9. Turn probabilities into a decision

SELECT
  decile,
  COUNT(*)                                              AS customers,
  ROUND(AVG(p_churn), 3)                                AS avg_predicted,
  ROUND(AVG(IF(actual_churn = 'Yes', 1, 0)), 3)         AS actual_churn_rate,
  ROUND(SUM(monthly_charges), 0)                        AS monthly_revenue
FROM (
  SELECT *, NTILE(10) OVER (ORDER BY p_churn) AS decile
  FROM `telco_churn.churn_scores`
)
GROUP BY decile
ORDER BY decile;
