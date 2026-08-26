-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 10. Validate the model against star ratings

WITH banded AS (
  SELECT
    CASE
      WHEN rating <= 2 THEN '1-2 stars (negative)'
      WHEN rating  = 3 THEN '3 stars (neutral)'
      ELSE                  '4-5 stars (positive)'
    END AS rating_band,
    UPPER(TRIM(sentiment)) AS sentiment
  FROM `retail_reviews.reviews_scored`
  WHERE sentiment IS NOT NULL
)
SELECT
  rating_band,
  COUNTIF(sentiment = 'NEGATIVE') AS negative,
  COUNTIF(sentiment = 'NEUTRAL')  AS neutral,
  COUNTIF(sentiment = 'POSITIVE') AS positive,
  COUNT(*)                        AS total
FROM banded
GROUP BY rating_band
ORDER BY rating_band;
