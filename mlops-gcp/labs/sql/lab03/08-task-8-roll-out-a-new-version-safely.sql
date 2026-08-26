-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 8. Roll out a new version safely

SELECT
  deployed_model_id,
  COUNT(*)                                   AS requests,
  ROUND(AVG(latency_ms), 1)                  AS avg_latency_ms,
  ROUND(AVG(predicted_p_churn), 4)           AS avg_score
FROM `telco_churn.prediction_logs`
WHERE DATE(request_timestamp) = CURRENT_DATE()
GROUP BY deployed_model_id;
