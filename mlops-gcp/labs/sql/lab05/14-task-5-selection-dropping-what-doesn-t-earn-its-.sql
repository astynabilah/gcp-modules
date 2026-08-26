-- Lab 5 — Feature engineering for tabular data
-- Task 5. Selection — dropping what doesn't earn its place

SELECT
  COUNT(*)                                             AS rows,
  COUNT(DISTINCT customer_id)                          AS distinct_customer_id,
  COUNT(DISTINCT gender)                               AS distinct_gender,
  COUNT(DISTINCT contract)                             AS distinct_contract,
  COUNTIF(total_charges IS NULL)                       AS null_total_charges,
  COUNTIF(activity_ratio_30d_vs_avg IS NULL)           AS null_activity_ratio
FROM `telco_churn.features_v3`;
