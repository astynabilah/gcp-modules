-- Lab 5 — Feature engineering for tabular data
-- Task 7. Ablation — did any of this pay?

SELECT 'v1 raw'            AS feature_set, ROUND(roc_auc, 4) AS roc_auc, ROUND(recall, 4) AS recall
FROM ML.EVALUATE(MODEL `telco_churn.abl_v1`)
UNION ALL
SELECT 'v2 + events',      ROUND(roc_auc, 4), ROUND(recall, 4)
FROM ML.EVALUATE(MODEL `telco_churn.abl_v2`)
UNION ALL
SELECT 'v3 + extraction',  ROUND(roc_auc, 4), ROUND(recall, 4)
FROM ML.EVALUATE(MODEL `telco_churn.abl_v3`)
ORDER BY roc_auc;
