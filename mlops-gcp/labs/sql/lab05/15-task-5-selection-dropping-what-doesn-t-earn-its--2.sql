-- Lab 5 — Feature engineering for tabular data
-- Task 5. Selection — dropping what doesn't earn its place

WITH numeric_features AS (
  SELECT
    IF(churn = 'Yes', 1, 0) AS y,
    tenure_months, monthly_charges, total_charges, addon_count,
    events_90d, complaints_90d, days_since_last_event,
    activity_ratio_30d_vs_avg, charge_drift
  FROM `telco_churn.features_v3`
)
SELECT 'tenure_months' AS feature, ROUND(CORR(tenure_months, y), 4) AS corr_with_churn FROM numeric_features
UNION ALL SELECT 'monthly_charges',  ROUND(CORR(monthly_charges, y), 4)  FROM numeric_features
UNION ALL SELECT 'total_charges',    ROUND(CORR(total_charges, y), 4)    FROM numeric_features
UNION ALL SELECT 'addon_count',      ROUND(CORR(addon_count, y), 4)      FROM numeric_features
UNION ALL SELECT 'events_90d',       ROUND(CORR(events_90d, y), 4)       FROM numeric_features
UNION ALL SELECT 'complaints_90d',   ROUND(CORR(complaints_90d, y), 4)   FROM numeric_features
UNION ALL SELECT 'days_since_last_event', ROUND(CORR(days_since_last_event, y), 4) FROM numeric_features
UNION ALL SELECT 'activity_ratio_30d_vs_avg', ROUND(CORR(activity_ratio_30d_vs_avg, y), 4) FROM numeric_features
UNION ALL SELECT 'charge_drift',     ROUND(CORR(charge_drift, y), 4)     FROM numeric_features
ORDER BY ABS(corr_with_churn) DESC;
