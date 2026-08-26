-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 6. Evaluate — and pick the right metric

SELECT *
FROM ML.EVALUATE(
  MODEL `telco_churn.churn_model`,
  (SELECT * EXCEPT (customer_id) FROM `telco_churn.customers_ml`)
);
