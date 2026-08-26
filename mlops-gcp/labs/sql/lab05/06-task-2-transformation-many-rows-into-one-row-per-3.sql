-- Lab 5 — Feature engineering for tabular data
-- Task 2. Transformation — many rows into one row per prediction unit

SELECT
  COUNT(*)                                  AS rows,
  COUNT(DISTINCT customer_id)               AS unique_customers,
  COUNTIF(events_180d = 0)                  AS customers_no_events,
  ROUND(AVG(events_90d), 2)                 AS avg_events_90d,
  COUNTIF(days_since_last_event = 999)      AS never_contacted
FROM `telco_churn.features_v2`;
