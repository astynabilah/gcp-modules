-- Lab 5 — Feature engineering for tabular data
-- Task 6. Importance — three different questions

CREATE OR REPLACE MODEL `telco_churn.model_v3`
OPTIONS (MODEL_TYPE = 'BOOSTED_TREE_CLASSIFIER', INPUT_LABEL_COLS = ['churn'],
         AUTO_CLASS_WEIGHTS = TRUE, ENABLE_GLOBAL_EXPLAIN = TRUE)
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.features_v3`;
