-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 11. Turn themes into an action list

SELECT AI.GENERATE(
  prompt => (
    'These are product complaint themes extracted from clothing reviews, with counts. ',
    'Group them into at most 8 distinct business issues. For each, give a canonical name, ',
    'the total mentions, and one concrete recommended action for a merchandising team.\n',
    (SELECT STRING_AGG(FORMAT('%s (%d)', theme, n), '; ')
     FROM (
       SELECT theme, COUNT(*) AS n
       FROM `retail_reviews.reviews_scored`, UNNEST(themes) AS theme
       WHERE UPPER(sentiment) = 'NEGATIVE'
       GROUP BY theme
       ORDER BY n DESC
       LIMIT 60
     ))
  ),
  connection_id => 'us.gemini-conn',
  endpoint => 'gemini-2.5-flash',
  output_schema => 'issue STRING, total_mentions INT64, recommended_action STRING'
) AS consolidated;
