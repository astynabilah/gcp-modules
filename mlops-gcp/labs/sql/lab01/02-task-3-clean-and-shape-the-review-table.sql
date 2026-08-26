-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 3. Clean and shape the review table

CREATE OR REPLACE TABLE `retail_reviews.reviews_clean` AS
SELECT
  FORMAT('R%05d', index_id)                     AS review_id,
  clothing_id,
  age,
  NULLIF(TRIM(title), '')                       AS title,
  TRIM(review_text)                             AS review_text,
  rating,
  recommended_ind = 1                           AS recommended,
  positive_feedback_count,
  division_name,
  department_name,
  class_name
FROM `retail_reviews.reviews_raw`
WHERE review_text IS NOT NULL
  AND TRIM(review_text) != '';
