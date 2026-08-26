-- Lab 5 — Feature engineering for tabular data
-- Task 4. Leakage — the failure that looks like success

CREATE OR REPLACE TABLE `telco_churn.features_leaky` AS
SELECT
  * EXCEPT (churn),
  -- a column that only has a value BECAUSE the customer churned
  CASE
    WHEN churn = 'Yes' THEN
      CASE MOD(ABS(FARM_FINGERPRINT(customer_id)), 3)
        WHEN 0 THEN 'price'
        WHEN 1 THEN 'service_quality'
        ELSE        'moving_home'
      END
    ELSE NULL
  END AS cancellation_reason,
  churn
FROM `telco_churn.features_v3`;
