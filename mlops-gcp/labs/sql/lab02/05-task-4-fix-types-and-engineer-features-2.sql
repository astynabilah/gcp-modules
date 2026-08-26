-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 4. Fix types and engineer features

SELECT
  COUNT(*)                                    AS rows,
  COUNTIF(total_charges = 0)                  AS zero_total_charges,
  COUNTIF(avg_monthly_spend IS NULL)          AS null_avg_spend,
  COUNT(DISTINCT churn)                       AS label_values,
  ROUND(AVG(addon_count), 2)                  AS avg_addons
FROM `telco_churn.customers_ml`;
