-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 6. Evaluate — and pick the right metric

SELECT
  threshold,
  ROUND(true_positives  / NULLIF(true_positives + false_negatives, 0), 3) AS recall,
  ROUND(true_positives  / NULLIF(true_positives + false_positives, 0), 3) AS precision,
  true_positives, false_positives, false_negatives, true_negatives
FROM ML.ROC_CURVE(
  MODEL `telco_churn.churn_model`,
  (SELECT * EXCEPT (customer_id) FROM `telco_churn.customers_ml`)
)
WHERE threshold BETWEEN 0.2 AND 0.8
ORDER BY threshold;
