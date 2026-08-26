-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 8. Score the whole table

CREATE OR REPLACE TABLE `retail_reviews.reviews_scored` AS
WITH sampled AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY rating ORDER BY FARM_FINGERPRINT(review_id)) AS rn
  FROM `retail_reviews.reviews_clean`
)
SELECT
  review_id, clothing_id, age, rating, recommended,
  division_name, department_name, class_name, review_text,
  AI.GENERATE(
    prompt => (
      'You are a retail quality analyst. Analyze this clothing review.\n',
      '- sentiment: POSITIVE, NEGATIVE, or NEUTRAL, judged from the point of view of the reviewer.\n',
      '- confidence: 0.0 to 1.0, how certain you are of that label.\n',
      '- themes: 1 to 3 short lowercase noun phrases naming what the review is about.\n',
      '- actionable_issue: the single most fixable product problem, or "none".\n',
      'Review: ',
      review_text
    ),
    connection_id => 'us.gemini-conn',
    endpoint => 'gemini-2.5-flash',
    model_params => JSON '{"generation_config": {"temperature": 0, "max_output_tokens": 256}}',
    output_schema => 'sentiment STRING, confidence FLOAT64, themes ARRAY<STRING>, actionable_issue STRING'
  ).* EXCEPT (full_response)
FROM sampled
-- WHERE rn <= 400   -- sampled path: 400 per rating × 5 ratings = 2,000 rows
;
