-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 5. Train the model

CREATE OR REPLACE MODEL `telco_churn.churn_model`
OPTIONS (
  MODEL_TYPE            = 'BOOSTED_TREE_CLASSIFIER',
  INPUT_LABEL_COLS      = ['churn'],
  AUTO_CLASS_WEIGHTS    = TRUE,
  DATA_SPLIT_METHOD     = 'AUTO_SPLIT',
  EARLY_STOP            = TRUE,
  MAX_ITERATIONS        = 50,
  ENABLE_GLOBAL_EXPLAIN = TRUE,
  MODEL_REGISTRY        = 'VERTEX_AI',
  VERTEX_AI_MODEL_ID    = 'telco-churn-model'
) AS
SELECT * EXCEPT (customer_id)
FROM `telco_churn.customers_ml`;
