-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 8. Tune, and preprocess inside the model

SELECT trial_id, hyperparameters, hparam_tuning_evaluation_metrics, is_optimal, status
FROM ML.TRIAL_INFO(MODEL `telco_churn.churn_model_tuned`)
ORDER BY trial_id;
