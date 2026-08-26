-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 7. Explain the model

SELECT
  customer_id,
  predicted_churn,
  ROUND((SELECT prob FROM UNNEST(predicted_churn_probs) WHERE label = 'Yes'), 3) AS p_churn,
  top_feature_attributions
FROM ML.EXPLAIN_PREDICT(
  MODEL `telco_churn.churn_model`,
  (SELECT * FROM `telco_churn.customers_ml`),
  STRUCT(3 AS top_k_features)
)
ORDER BY p_churn DESC
LIMIT 10;
