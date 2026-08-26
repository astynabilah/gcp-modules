-- Lab 4 — Computer vision without training anything
-- Task 3. Tier 1 — a pretrained API

CREATE OR REPLACE TABLE `vision_lab.poster_labels` AS
SELECT
  REGEXP_EXTRACT(uri, r'([^/]+)$')                     AS file_name,
  JSON_VALUE(label, '$.description')                   AS label,
  CAST(JSON_VALUE(label, '$.score') AS FLOAT64)        AS score
FROM `vision_lab.poster_labels_raw`,
     UNNEST(JSON_QUERY_ARRAY(ml_annotate_image_result, '$.label_annotations')) AS label
WHERE ml_annotate_image_status = '';

SELECT * FROM `vision_lab.poster_labels`
ORDER BY file_name, score DESC;
