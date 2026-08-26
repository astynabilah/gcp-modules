-- Lab 5 — Feature engineering for tabular data
-- Task 2. Transformation — many rows into one row per prediction unit

CREATE OR REPLACE TABLE `telco_churn.features_v2` AS
SELECT
  m.* EXCEPT (churn),
  COALESCE(f.events_30d, 0)                    AS events_30d,
  COALESCE(f.events_90d, 0)                    AS events_90d,
  COALESCE(f.events_180d, 0)                   AS events_180d,
  COALESCE(f.complaints_90d, 0)                AS complaints_90d,
  COALESCE(f.faults_90d, 0)                    AS faults_90d,
  COALESCE(f.days_since_last_event, 999)       AS days_since_last_event,
  COALESCE(f.activity_ratio_30d_vs_avg, 0.0)   AS activity_ratio_30d_vs_avg,
  m.churn
FROM `telco_churn.customers_ml` m
LEFT JOIN `telco_churn.customer_event_features` f
  ON m.customer_id = f.customer_id;
