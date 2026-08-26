-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 7. Enforce a typed output contract

SELECT
  review_id,
  rating,
  department_name,
  AI.GENERATE(
    prompt => (
      'You are a retail quality analyst. Analyze this clothing review.\n',
      '- sentiment: POSITIVE, NEGATIVE, or NEUTRAL, judged from the point of view of the reviewer.\n',
      '- confidence: 0.0 to 1.0, how certain you are of that label.\n',
      '- themes: 1 to 3 short lowercase noun phrases naming what the review is about ',
      '(e.g. "sizing runs small", "fabric quality", "colour differs from photo").\n',
      '- actionable_issue: the single most fixable product problem, or "none".\n',
      'Review: ',
      review_text
    ),
    connection_id => 'us.gemini-conn',
    endpoint => 'gemini-2.5-flash',
    model_params => JSON '{"generation_config": {"temperature": 0, "max_output_tokens": 256}}',
    output_schema => 'sentiment STRING, confidence FLOAT64, themes ARRAY<STRING>, actionable_issue STRING'
  ).* EXCEPT (full_response, status)
FROM `retail_reviews.reviews_clean`
ORDER BY review_id
LIMIT 5;
