-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 8. Tune, and preprocess inside the model

CREATE OR REPLACE MODEL `telco_churn.churn_logreg`
OPTIONS (
  MODEL_TYPE         = 'LOGISTIC_REG',
  INPUT_LABEL_COLS   = ['churn'],
  AUTO_CLASS_WEIGHTS = TRUE
) AS
SELECT * EXCEPT (customer_id)
FROM `telco_churn.customers_ml`;
