-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 10. Validate the model against star ratings

SELECT
  COUNT(*) AS scored,
  ROUND(100 * COUNTIF(
    (rating <= 2 AND UPPER(sentiment) = 'NEGATIVE') OR
    (rating  = 3 AND UPPER(sentiment) = 'NEUTRAL')  OR
    (rating >= 4 AND UPPER(sentiment) = 'POSITIVE')
  ) / COUNT(*), 1) AS agreement_pct
FROM `retail_reviews.reviews_scored`
WHERE sentiment IS NOT NULL;
