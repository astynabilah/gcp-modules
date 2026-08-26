-- Lab 5 — Feature engineering for tabular data
-- Task 1. The problem with Lab 2's feature table

SELECT
  COUNT(*)                                   AS events,
  COUNT(DISTINCT customer_id)                AS customers_with_events,
  MIN(event_date)                            AS earliest,
  MAX(event_date)                            AS latest,
  COUNT(DISTINCT event_type)                 AS event_types
FROM `telco_churn.support_events`;
