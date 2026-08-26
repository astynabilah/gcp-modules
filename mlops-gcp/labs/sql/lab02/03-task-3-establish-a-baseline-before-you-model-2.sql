-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 3. Establish a baseline before you model

SELECT
  COUNTIF(Contract = 'Month-to-month')                             AS flagged,
  COUNTIF(Contract = 'Month-to-month' AND Churn = 'Yes')           AS churners_caught,
  ROUND(COUNTIF(Contract = 'Month-to-month' AND Churn = 'Yes')
        / COUNTIF(Churn = 'Yes'), 3)                               AS recall,
  ROUND(COUNTIF(Contract = 'Month-to-month' AND Churn = 'Yes')
        / COUNTIF(Contract = 'Month-to-month'), 3)                 AS precision
FROM `telco_churn.customers_raw`;
