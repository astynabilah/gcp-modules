-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 9. Turn probabilities into a decision

WITH rule_based AS (
  SELECT COUNTIF(contract = 'Month-to-month') AS contacted,
         COUNTIF(contract = 'Month-to-month' AND actual_churn = 'Yes') AS caught
  FROM `telco_churn.churn_scores`
),
model_based AS (
  SELECT COUNTIF(p_churn >= 0.35) AS contacted,
         COUNTIF(p_churn >= 0.35 AND actual_churn = 'Yes') AS caught
  FROM `telco_churn.churn_scores`
)
SELECT 'contract rule' AS approach, contacted, caught,
       ROUND(caught / contacted, 3) AS precision FROM rule_based
UNION ALL
SELECT 'model @ 0.35', contacted, caught,
       ROUND(caught / contacted, 3) FROM model_based;
