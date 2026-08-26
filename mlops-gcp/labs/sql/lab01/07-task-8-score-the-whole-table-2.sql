-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 8. Score the whole table

SELECT
  COUNT(*)                                    AS rows_scored,
  COUNTIF(status != '')                       AS failed_rows,
  COUNTIF(sentiment IS NULL)                  AS null_sentiment,
  COUNT(DISTINCT sentiment)                   AS distinct_labels,
  STRING_AGG(DISTINCT sentiment ORDER BY sentiment) AS labels
FROM `retail_reviews.reviews_scored`;
