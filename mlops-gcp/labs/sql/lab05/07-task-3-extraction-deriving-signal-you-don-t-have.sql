-- Lab 5 — Feature engineering for tabular data
-- Task 3. Extraction — deriving signal you don't have

CREATE OR REPLACE TABLE `telco_churn.features_v3` AS
SELECT
  * EXCEPT (churn),

  -- 1. RATIOS: relationships, not levels
  SAFE_DIVIDE(monthly_charges, NULLIF(addon_count + 1, 0))      AS charge_per_service,
  SAFE_DIVIDE(total_charges, NULLIF(tenure_months, 0))          AS lifetime_avg_charge,
  SAFE_DIVIDE(monthly_charges,
              NULLIF(SAFE_DIVIDE(total_charges, NULLIF(tenure_months, 0)), 0))
                                                                 AS charge_drift,

  -- 2. FLAGS: encode a threshold the business already believes in
  monthly_charges > 80                                           AS is_high_value,
  tenure_months <= 3                                             AS is_new_customer,
  complaints_90d >= 2                                            AS is_repeat_complainer,

  -- 3. INTERACTIONS: combinations a tree would need many splits to reach
  CONCAT(contract, ' | ', internet_service)                      AS contract_internet,

  -- 4. RELATIVE POSITION: how this customer compares to their peers
  PERCENT_RANK() OVER (PARTITION BY contract ORDER BY monthly_charges)
                                                                 AS charge_pctile_in_contract,

  churn
FROM `telco_churn.features_v2`;
