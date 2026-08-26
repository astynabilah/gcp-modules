-- Lab 5 — Feature engineering for tabular data
-- Task 6. Importance — three different questions

SELECT feature, importance_gain, importance_weight, importance_cover
FROM ML.FEATURE_IMPORTANCE(MODEL `telco_churn.model_v3`)
ORDER BY importance_gain DESC
LIMIT 15;
