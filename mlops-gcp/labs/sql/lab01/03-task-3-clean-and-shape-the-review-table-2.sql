-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 3. Clean and shape the review table

SELECT COUNT(*) AS reviews_with_text,
       MIN(rating) AS min_rating,
       MAX(rating) AS max_rating,
       ROUND(AVG(LENGTH(review_text)), 0) AS avg_chars
FROM `retail_reviews.reviews_clean`;
