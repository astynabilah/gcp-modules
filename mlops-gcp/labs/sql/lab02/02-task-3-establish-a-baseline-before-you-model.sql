-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 3. Establish a baseline before you model

SELECT
  Contract,
  COUNT(*)                                          AS customers,
  COUNTIF(Churn = 'Yes')                            AS churners,
  ROUND(100 * COUNTIF(Churn = 'Yes') / COUNT(*), 1) AS churn_rate_pct
FROM `telco_churn.customers_raw`
GROUP BY Contract
ORDER BY churn_rate_pct DESC;
