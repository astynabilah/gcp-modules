-- Lab 5 — Feature engineering for tabular data
-- Task 8. Binding preprocessing to the model, and managing the SQL

CREATE OR REPLACE MODEL `telco_churn.model_transform`
TRANSFORM (
  churn,
  contract, internet_service, payment_method, tenure_band, contract_internet,
  is_high_value, is_new_customer, is_repeat_complainer,
  ML.STANDARD_SCALER(monthly_charges)        OVER () AS monthly_charges_z,
  ML.STANDARD_SCALER(charge_drift)           OVER () AS charge_drift_z,
  ML.QUANTILE_BUCKETIZE(tenure_months, 5)    OVER () AS tenure_bucket,
  ML.QUANTILE_BUCKETIZE(events_90d, 4)       OVER () AS events_bucket,
  ML.FEATURE_CROSS(STRUCT(contract, tenure_band))    AS contract_x_tenure
)
OPTIONS (
  MODEL_TYPE = 'BOOSTED_TREE_CLASSIFIER',
  INPUT_LABEL_COLS = ['churn'],
  AUTO_CLASS_WEIGHTS = TRUE
)
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.features_v3`;
