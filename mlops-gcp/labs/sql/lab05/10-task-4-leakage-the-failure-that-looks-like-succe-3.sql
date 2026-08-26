-- Lab 5 — Feature engineering for tabular data
-- Task 4. Leakage — the failure that looks like success

SELECT 'v3 (honest)' AS feature_set, roc_auc FROM ML.EVALUATE(
  MODEL `telco_churn.model_v3`,
  (SELECT * EXCEPT (customer_id) FROM `telco_churn.features_v3`))
UNION ALL
SELECT 'leaky', roc_auc FROM ML.EVALUATE(
  MODEL `telco_churn.model_leaky`,
  (SELECT * EXCEPT (customer_id) FROM `telco_churn.features_leaky`));
