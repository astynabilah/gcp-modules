-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 0. Prerequisites and catch-up

SELECT model_name, model_type, creation_time
FROM `telco_churn.INFORMATION_SCHEMA.MODELS`
ORDER BY creation_time;
