-- Lab 5 — Feature engineering for tabular data
-- Task 6. Importance — three different questions

SELECT feature, attribution
FROM ML.GLOBAL_EXPLAIN(MODEL `telco_churn.model_v3`)
ORDER BY attribution DESC
LIMIT 15;
