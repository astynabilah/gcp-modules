-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 2. Batch serving with a scheduled query

MERGE `telco_churn.churn_scores_history` T
USING (
  SELECT
    CURRENT_DATE()  AS score_date,
    customer_id,
    (SELECT prob FROM UNNEST(predicted_churn_probs) WHERE label = 'Yes') AS p_churn,
    contract,
    tenure_months,
    monthly_charges,
    'churn_model@v1' AS model_version,
    CURRENT_TIMESTAMP() AS scored_at
  FROM ML.PREDICT(
    MODEL `telco_churn.churn_model`,
    (SELECT * FROM `telco_churn.customers_ml`)
  )
) S
ON  T.score_date  = S.score_date
AND T.customer_id = S.customer_id
WHEN MATCHED THEN UPDATE SET
  p_churn = S.p_churn,
  risk_tier = CASE WHEN S.p_churn >= 0.60 THEN 'High'
                   WHEN S.p_churn >= 0.35 THEN 'Medium' ELSE 'Low' END,
  contract = S.contract,
  tenure_months = S.tenure_months,
  monthly_charges = S.monthly_charges,
  model_version = S.model_version,
  scored_at = S.scored_at
WHEN NOT MATCHED THEN INSERT (
  score_date, customer_id, p_churn, risk_tier, contract,
  tenure_months, monthly_charges, model_version, scored_at
) VALUES (
  S.score_date, S.customer_id, S.p_churn,
  CASE WHEN S.p_churn >= 0.60 THEN 'High'
       WHEN S.p_churn >= 0.35 THEN 'Medium' ELSE 'Low' END,
  S.contract, S.tenure_months, S.monthly_charges, S.model_version, S.scored_at
);
