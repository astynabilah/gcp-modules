-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 11. Turn themes into an action list

SELECT
  department_name,
  COUNT(*) AS reviews,
  ROUND(100 * COUNTIF(UPPER(sentiment) = 'NEGATIVE') / COUNT(*), 1) AS pct_negative,
  ROUND(AVG(rating), 2) AS avg_rating
FROM `retail_reviews.reviews_scored`
WHERE sentiment IS NOT NULL AND department_name IS NOT NULL
GROUP BY department_name
ORDER BY pct_negative DESC;
