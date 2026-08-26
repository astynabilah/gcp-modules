-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 11. Turn themes into an action list

SELECT
  theme,
  COUNT(*)                       AS mentions,
  ROUND(AVG(rating), 2)          AS avg_rating,
  ROUND(100 * COUNTIF(UPPER(sentiment) = 'NEGATIVE') / COUNT(*), 1) AS pct_negative,
  COUNT(DISTINCT clothing_id)    AS products_affected
FROM `retail_reviews.reviews_scored`, UNNEST(themes) AS theme
WHERE sentiment IS NOT NULL
GROUP BY theme
HAVING COUNT(*) >= 25
ORDER BY mentions DESC
LIMIT 25;
