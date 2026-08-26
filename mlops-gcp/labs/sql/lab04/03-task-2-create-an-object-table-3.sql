-- Lab 4 — Computer vision without training anything
-- Task 2. Create an object table

SELECT
  COUNT(*)                                  AS images,
  COUNT(DISTINCT content_type)              AS content_types,
  ROUND(SUM(size) / 1024 / 1024, 2)         AS total_mb
FROM `vision_lab.posters`;
