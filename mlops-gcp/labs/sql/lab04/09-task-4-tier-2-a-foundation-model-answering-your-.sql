-- Lab 4 — Computer vision without training anything
-- Task 4. Tier 2 — a foundation model answering your question

SELECT
  REGEXP_EXTRACT(uri, r'([^/]+)$') AS file_name,
  AI.GENERATE(
    (
      'This is a poster for a classic film. Identify it. ',
      'If you cannot determine a field with reasonable confidence, return NULL for it. ',
      ref
    ),
    endpoint => 'gemini-2.5-flash',
    model_params => JSON '{"generation_config": {"temperature": 0}}',
    output_schema => 'title STRING, year INT64, genre STRING, dominant_colours ARRAY<STRING>, has_text BOOL'
  ).* EXCEPT (full_response, status)
FROM `vision_lab.posters`
ORDER BY file_name
LIMIT 5;
