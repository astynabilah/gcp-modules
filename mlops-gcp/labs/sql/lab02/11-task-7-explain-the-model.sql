-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 7. Explain the model

SELECT *
FROM ML.GLOBAL_EXPLAIN(MODEL `telco_churn.churn_model`)
ORDER BY attribution DESC;
