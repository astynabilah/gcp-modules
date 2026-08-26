-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 9. Turn probabilities into a decision

CREATE OR REPLACE TABLE `telco_churn.churn_scores` AS
SELECT
  customer_id,
  contract,
  tenure_months,
  monthly_charges,
  churn AS actual_churn,
  (SELECT prob FROM UNNEST(predicted_churn_probs) WHERE label = 'Yes') AS p_churn
FROM ML.PREDICT(
  MODEL `telco_churn.churn_model`,
  (SELECT * FROM `telco_churn.customers_ml`)
);
