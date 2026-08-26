-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 0. Prerequisites and catch-up

CREATE OR REPLACE TABLE `telco_churn.customers_ml` AS
SELECT
  customerID AS customer_id, gender,
  SeniorCitizen = 1 AS senior_citizen,
  Partner = 'Yes' AS has_partner,
  Dependents = 'Yes' AS has_dependents,
  tenure AS tenure_months,
  Contract AS contract,
  PaperlessBilling = 'Yes' AS paperless_billing,
  PaymentMethod AS payment_method,
  PhoneService = 'Yes' AS phone_service,
  MultipleLines AS multiple_lines,
  InternetService AS internet_service,
  OnlineSecurity AS online_security,
  OnlineBackup AS online_backup,
  DeviceProtection AS device_protection,
  TechSupport AS tech_support,
  StreamingTV AS streaming_tv,
  StreamingMovies AS streaming_movies,
  MonthlyCharges AS monthly_charges,
  COALESCE(SAFE_CAST(TRIM(TotalCharges) AS FLOAT64), 0.0) AS total_charges,
  SAFE_DIVIDE(COALESCE(SAFE_CAST(TRIM(TotalCharges) AS FLOAT64), 0.0),
              NULLIF(tenure, 0)) AS avg_monthly_spend,
  CASE WHEN tenure <= 6 THEN 'new'
       WHEN tenure <= 24 THEN 'growing'
       ELSE 'established' END AS tenure_band,
  (CAST(OnlineSecurity   = 'Yes' AS INT64) + CAST(OnlineBackup     = 'Yes' AS INT64) +
   CAST(DeviceProtection = 'Yes' AS INT64) + CAST(TechSupport      = 'Yes' AS INT64) +
   CAST(StreamingTV      = 'Yes' AS INT64) + CAST(StreamingMovies  = 'Yes' AS INT64)) AS addon_count,
  Churn AS churn
FROM `telco_churn.customers_raw`;

CREATE OR REPLACE MODEL `telco_churn.churn_model`
OPTIONS (MODEL_TYPE='BOOSTED_TREE_CLASSIFIER', INPUT_LABEL_COLS=['churn'],
         AUTO_CLASS_WEIGHTS=TRUE, ENABLE_GLOBAL_EXPLAIN=TRUE,
         MODEL_REGISTRY='VERTEX_AI', VERTEX_AI_MODEL_ID='telco-churn-model')
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.customers_ml`;

CREATE OR REPLACE MODEL `telco_churn.churn_logreg`
OPTIONS (MODEL_TYPE='LOGISTIC_REG', INPUT_LABEL_COLS=['churn'],
         AUTO_CLASS_WEIGHTS=TRUE,
         MODEL_REGISTRY='VERTEX_AI', VERTEX_AI_MODEL_ID='telco-churn-logreg')
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.customers_ml`;
