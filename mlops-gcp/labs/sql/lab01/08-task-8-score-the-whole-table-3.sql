-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 8. Score the whole table

MERGE `retail_reviews.reviews_scored` T
USING (
  SELECT review_id,
         AI.GENERATE(
           prompt => ('Classify sentiment as POSITIVE, NEGATIVE or NEUTRAL. Review: ', review_text),
           connection_id => 'us.gemini-conn',
           endpoint => 'gemini-2.5-flash',
           output_schema => 'sentiment STRING, confidence FLOAT64'
         ) AS g
  FROM `retail_reviews.reviews_scored`
  WHERE status != '' OR sentiment IS NULL
) S
ON T.review_id = S.review_id
WHEN MATCHED THEN UPDATE SET
  T.sentiment = S.g.sentiment,
  T.confidence = S.g.confidence,
  T.status = '';
