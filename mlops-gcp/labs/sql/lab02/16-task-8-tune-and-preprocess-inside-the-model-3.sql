-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 8. Tune, and preprocess inside the model

CREATE OR REPLACE MODEL `telco_churn.churn_tuned_explicit`
OPTIONS (
  MODEL_TYPE                = 'BOOSTED_TREE_CLASSIFIER',
  INPUT_LABEL_COLS          = ['churn'],
  AUTO_CLASS_WEIGHTS        = TRUE,
  NUM_TRIALS                = 10,
  DATA_SPLIT_METHOD         = 'RANDOM',
  DATA_SPLIT_EVAL_FRACTION  = 0.15,   -- 15% evaluation
  DATA_SPLIT_TEST_FRACTION  = 0.15    -- 15% test  ->  training is the remaining 70%
) AS
SELECT * EXCEPT (customer_id) FROM `telco_churn.customers_ml`;
