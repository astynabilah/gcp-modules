-- Lab 1 — Analyze customer review sentiment with Gemini in BigQuery
-- Task 9. The remote-model route (and when to use it)

CREATE OR REPLACE MODEL `retail_reviews.gemini_flash`
REMOTE WITH CONNECTION `us.gemini-conn`
OPTIONS (ENDPOINT = 'gemini-2.5-flash');
