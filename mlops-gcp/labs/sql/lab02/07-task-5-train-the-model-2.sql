-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 5. Train the model

SELECT *
FROM ML.TRAINING_INFO(MODEL `telco_churn.churn_model`)
ORDER BY iteration;
