-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 4. Fix types and engineer features

CREATE OR REPLACE TABLE `telco_churn.customers_ml` AS
SELECT
  customerID                                   AS customer_id,

  -- demographics
  gender,
  SeniorCitizen = 1                            AS senior_citizen,
  Partner    = 'Yes'                           AS has_partner,
  Dependents = 'Yes'                           AS has_dependents,

  -- account
  tenure                                       AS tenure_months,
  Contract                                     AS contract,
  PaperlessBilling = 'Yes'                     AS paperless_billing,
  PaymentMethod                                AS payment_method,

  -- services
  PhoneService = 'Yes'                         AS phone_service,
  MultipleLines                                AS multiple_lines,
  InternetService                              AS internet_service,
  OnlineSecurity                               AS online_security,
  OnlineBackup                                 AS online_backup,
  DeviceProtection                             AS device_protection,
  TechSupport                                  AS tech_support,
  StreamingTV                                  AS streaming_tv,
  StreamingMovies                              AS streaming_movies,

  -- money: the fix
  MonthlyCharges                               AS monthly_charges,
  COALESCE(SAFE_CAST(TRIM(TotalCharges) AS FLOAT64), 0.0) AS total_charges,

  -- engineered features
  SAFE_DIVIDE(
    COALESCE(SAFE_CAST(TRIM(TotalCharges) AS FLOAT64), 0.0),
    NULLIF(tenure, 0)
  )                                            AS avg_monthly_spend,

  CASE
    WHEN tenure <= 6  THEN 'new'
    WHEN tenure <= 24 THEN 'growing'
    ELSE                   'established'
  END                                          AS tenure_band,

  (
    CAST(OnlineSecurity    = 'Yes' AS INT64) +
    CAST(OnlineBackup      = 'Yes' AS INT64) +
    CAST(DeviceProtection  = 'Yes' AS INT64) +
    CAST(TechSupport       = 'Yes' AS INT64) +
    CAST(StreamingTV       = 'Yes' AS INT64) +
    CAST(StreamingMovies   = 'Yes' AS INT64)
  )                                            AS addon_count,

  -- label
  Churn                                        AS churn
FROM `telco_churn.customers_raw`;
