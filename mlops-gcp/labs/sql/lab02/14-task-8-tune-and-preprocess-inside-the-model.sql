-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 8. Tune, and preprocess inside the model

CREATE OR REPLACE MODEL `telco_churn.churn_model_tuned`
OPTIONS (
  MODEL_TYPE               = 'BOOSTED_TREE_CLASSIFIER',
  INPUT_LABEL_COLS         = ['churn'],
  AUTO_CLASS_WEIGHTS       = TRUE,
  ENABLE_GLOBAL_EXPLAIN    = TRUE,
  NUM_TRIALS               = 10,
  MAX_PARALLEL_TRIALS      = 2,
  HPARAM_TUNING_OBJECTIVES = ['ROC_AUC'],
  MAX_TREE_DEPTH           = HPARAM_RANGE(3, 10),
  LEARN_RATE               = HPARAM_RANGE(0.05, 0.3),
  L2_REG                   = HPARAM_RANGE(0, 5),
  SUBSAMPLE                = HPARAM_RANGE(0.6, 1.0)
) AS
SELECT * EXCEPT (customer_id)
FROM `telco_churn.customers_ml`;
