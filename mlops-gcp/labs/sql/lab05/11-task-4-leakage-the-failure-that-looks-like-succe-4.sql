-- Lab 5 — Feature engineering for tabular data
-- Task 4. Leakage — the failure that looks like success

SELECT
  churn,
  COUNT(*)                                  AS rows,
  COUNTIF(cancellation_reason IS NULL)      AS nulls,
  ROUND(100 * COUNTIF(cancellation_reason IS NULL) / COUNT(*), 1) AS null_pct
FROM `telco_churn.features_leaky`
GROUP BY churn;
