-- Lab 4 — Computer vision without training anything
-- Task 4. Tier 2 — a foundation model answering your question

SELECT
  COUNT(*)                        AS images,
  COUNTIF(status != '')           AS failed,
  COUNTIF(title IS NULL)          AS no_title,
  COUNTIF(year IS NULL)           AS no_year,
  COUNT(DISTINCT genre)           AS genres
FROM `vision_lab.poster_attributes`;
