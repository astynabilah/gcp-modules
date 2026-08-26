-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 6. Your first sentiment call

SELECT
  review_id,
  rating,
  review_text,
  AI.GENERATE(
    prompt => (
      'Classify the sentiment of this customer clothing review as exactly one word: ',
      'POSITIVE, NEGATIVE, or NEUTRAL. Return only that word. Review: ',
      review_text
    ),
    connection_id => 'us.gemini-conn',
    endpoint => 'gemini-2.5-flash'
  ).result AS sentiment
FROM `retail_reviews.reviews_clean`
ORDER BY review_id
LIMIT 5;
