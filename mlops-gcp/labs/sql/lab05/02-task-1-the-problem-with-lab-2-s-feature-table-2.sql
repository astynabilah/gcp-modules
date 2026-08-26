-- Lab 5 — Feature engineering for tabular data
-- Task 1. The problem with Lab 2's feature table

CREATE OR REPLACE TABLE `telco_churn.support_events` AS
WITH base AS (
  SELECT
    customerID AS customer_id,
    tenure,
    Churn,
    -- deterministic pseudo-random from the id, so this table is reproducible
    ABS(MOD(FARM_FINGERPRINT(customerID), 1000)) / 1000.0 AS r
  FROM `telco_churn.customers_raw`
  WHERE tenure > 0
),
expanded AS (
  SELECT
    customer_id,
    Churn,
    r,
    n
  FROM base, UNNEST(GENERATE_ARRAY(1, GREATEST(1, CAST(ROUND(r * 12) AS INT64)))) AS n
)
SELECT
  customer_id,
  -- events spread over the 180 days before the observation date
  DATE_SUB(DATE '2026-08-01',
           INTERVAL CAST(ROUND(180 * ABS(MOD(FARM_FINGERPRINT(
             CONCAT(customer_id, CAST(n AS STRING))), 1000)) / 1000.0) AS INT64) DAY) AS event_date,
  CASE MOD(ABS(FARM_FINGERPRINT(CONCAT(customer_id, CAST(n AS STRING)))), 4)
    WHEN 0 THEN 'billing_query'
    WHEN 1 THEN 'technical_fault'
    WHEN 2 THEN 'plan_change_request'
    ELSE        'complaint'
  END AS event_type
FROM expanded;
