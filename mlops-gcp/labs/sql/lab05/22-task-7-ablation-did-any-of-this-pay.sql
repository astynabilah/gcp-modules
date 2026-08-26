-- Lab 5 — Feature engineering for tabular data
-- Task 7. Ablation — did any of this pay?

-- v1: Lab 2's original features
CREATE OR REPLACE MODEL `telco_churn.abl_v1`
OPTIONS (MODEL_TYPE='BOOSTED_TREE_CLASSIFIER', INPUT_LABEL_COLS=['churn'],
         AUTO_CLASS_WEIGHTS=TRUE, DATA_SPLIT_METHOD='AUTO_SPLIT')
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.customers_ml`;

-- v2: + event-window features
CREATE OR REPLACE MODEL `telco_churn.abl_v2`
OPTIONS (MODEL_TYPE='BOOSTED_TREE_CLASSIFIER', INPUT_LABEL_COLS=['churn'],
         AUTO_CLASS_WEIGHTS=TRUE, DATA_SPLIT_METHOD='AUTO_SPLIT')
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.features_v2`;

-- v3: + extracted ratios, flags, interactions
CREATE OR REPLACE MODEL `telco_churn.abl_v3`
OPTIONS (MODEL_TYPE='BOOSTED_TREE_CLASSIFIER', INPUT_LABEL_COLS=['churn'],
         AUTO_CLASS_WEIGHTS=TRUE, DATA_SPLIT_METHOD='AUTO_SPLIT')
AS SELECT * EXCEPT (customer_id) FROM `telco_churn.features_v3`;
