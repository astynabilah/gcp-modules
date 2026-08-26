-- Lab 5 — Feature engineering for tabular data
-- Task 4. Leakage — the failure that looks like success

SELECT * FROM ML.GLOBAL_EXPLAIN(MODEL `telco_churn.model_leaky`)
ORDER BY attribution DESC;
