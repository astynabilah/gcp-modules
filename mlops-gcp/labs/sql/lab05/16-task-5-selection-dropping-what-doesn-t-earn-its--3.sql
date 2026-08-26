-- Lab 5 — Feature engineering for tabular data
-- Task 5. Selection — dropping what doesn't earn its place

SELECT
  ROUND(CORR(total_charges, lifetime_avg_charge), 4)  AS total_vs_lifetime_avg,
  ROUND(CORR(total_charges, tenure_months), 4)        AS total_vs_tenure,
  ROUND(CORR(events_90d, events_180d), 4)             AS events_90_vs_180,
  ROUND(CORR(monthly_charges, charge_per_service), 4) AS monthly_vs_per_service
FROM `telco_churn.features_v3`;
