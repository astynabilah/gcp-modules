-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 2. Create the dataset and load the CSV

SELECT
  COUNT(*)                                              AS customers,
  COUNTIF(Churn = 'Yes')                                AS churners,
  ROUND(100 * COUNTIF(Churn = 'Yes') / COUNT(*), 2)     AS churn_rate_pct,
  COUNTIF(SAFE_CAST(TRIM(TotalCharges) AS FLOAT64) IS NULL) AS uncastable_totalcharges
FROM `telco_churn.customers_raw`;
