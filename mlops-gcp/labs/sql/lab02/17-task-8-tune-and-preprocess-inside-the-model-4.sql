-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 8. Tune, and preprocess inside the model

CREATE OR REPLACE MODEL `telco_churn.churn_model_transform`
TRANSFORM (
  churn,
  contract,
  internet_service,
  payment_method,
  tenure_band,
  senior_citizen,
  addon_count,
  ML.STANDARD_SCALER(monthly_charges)  OVER () AS monthly_charges_scaled,
  ML.STANDARD_SCALER(total_charges)    OVER () AS total_charges_scaled,
  ML.QUANTILE_BUCKETIZE(tenure_months, 5) OVER () AS tenure_bucket
)
OPTIONS (
  MODEL_TYPE         = 'BOOSTED_TREE_CLASSIFIER',
  INPUT_LABEL_COLS   = ['churn'],
  AUTO_CLASS_WEIGHTS = TRUE
) AS
SELECT * EXCEPT (customer_id)
FROM `telco_churn.customers_ml`;
