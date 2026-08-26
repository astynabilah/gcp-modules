-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 9. The remote-model route (and when to use it)

SELECT review_id, rating, sentiment, confidence, themes
FROM AI.GENERATE_TABLE(
  MODEL `retail_reviews.gemini_flash`,
  (
    SELECT
      review_id, rating,
      CONCAT(
        'Analyze this clothing review. sentiment must be POSITIVE, NEGATIVE or NEUTRAL. ',
        'themes: 1-3 short lowercase noun phrases. Review: ',
        review_text
      ) AS prompt
    FROM `retail_reviews.reviews_clean`
    LIMIT 10
  ),
  STRUCT(
    'sentiment STRING, confidence FLOAT64, themes ARRAY<STRING>' AS output_schema,
    0 AS temperature
  )
);
