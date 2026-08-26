-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 10. Validate the model against star ratings

SELECT rating, sentiment, confidence, review_text
FROM `retail_reviews.reviews_scored`
WHERE rating >= 4 AND UPPER(sentiment) = 'NEGATIVE'
ORDER BY confidence DESC
LIMIT 20;
