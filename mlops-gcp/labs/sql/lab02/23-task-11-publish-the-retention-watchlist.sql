-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 11. Publish the retention watchlist

CREATE OR REPLACE VIEW `telco_churn.retention_watchlist` AS
SELECT
  customer_id,
  ROUND(p_churn, 3)                                        AS risk_score,
  CASE
    WHEN p_churn >= 0.60 THEN 'High'
    WHEN p_churn >= 0.35 THEN 'Medium'
    ELSE                      'Low'
  END                                                      AS risk_tier,
  contract,
  tenure_months,
  monthly_charges,
  ROUND(monthly_charges * 12 * 0.45, 0)                    AS annual_margin_at_risk,
  CASE
    WHEN contract = 'Month-to-month' THEN 'Offer 12-month contract with discount'
    WHEN tenure_months <= 6          THEN 'Onboarding check-in call'
    ELSE                                  'Service quality review'
  END                                                      AS suggested_action
FROM `telco_churn.churn_scores`
WHERE p_churn >= 0.35
ORDER BY p_churn DESC;
