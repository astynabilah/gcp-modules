-- Lab 5 — Feature engineering for tabular data
-- Task 4. Leakage — the failure that looks like success

CREATE OR REPLACE MODEL `telco_churn.model_leaky`
OPTIONS (MODEL_TYPE = 'BOOSTED_TREE_CLASSIFIER', INPUT_LABEL_COLS = ['churn'],
         AUTO_CLASS_WEIGHTS = TRUE, ENABLE_GLOBAL_EXPLAIN = TRUE)
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.features_leaky`;

SELECT roc_auc, accuracy, recall, precision
FROM ML.EVALUATE(MODEL `telco_churn.model_leaky`,
     (SELECT * EXCEPT (customer_id) FROM `telco_churn.features_leaky`));
