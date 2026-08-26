-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 2. Create the dataset and load the CSV into BigQuery

SELECT COUNT(*) AS rows_loaded,
       COUNTIF(review_text IS NULL OR TRIM(review_text) = '') AS blank_reviews
FROM `retail_reviews.reviews_raw`;
