-- Lab 5 — Feature engineering for tabular data
-- Task 1. The problem with Lab 2's feature table

SELECT column_name, data_type
FROM `telco_churn.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'customers_ml'
ORDER BY ordinal_position;
