-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 7. Call the endpoint back from BigQuery

SELECT
  customer_id,
  predicted_churn,
  churn_probs[OFFSET(0)] AS p_churn
FROM ML.PREDICT(
  MODEL `telco_churn.churn_endpoint`,
  (
    SELECT customer_id, contract, tenure_months, monthly_charges
    FROM `telco_churn.customers_ml`
    LIMIT 5
  )
);
