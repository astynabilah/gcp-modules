-- Lab 4 — Computer vision without training anything
-- Task 5. Validate against ground truth

WITH compared AS (
  SELECT
    LOWER(REGEXP_REPLACE(REGEXP_REPLACE(file_name, r'\.[a-z]+$', ''), r'_', ' ')) AS truth_title,
    LOWER(TRIM(COALESCE(title, ''))) AS pred_norm
  FROM `vision_lab.poster_attributes`
)
SELECT
  COUNT(*)                                                        AS images,
  COUNTIF(pred_norm = truth_title)                                AS exact,
  COUNTIF(pred_norm != '' AND pred_norm != truth_title
          AND (STRPOS(truth_title, pred_norm) > 0
            OR STRPOS(pred_norm, truth_title) > 0))               AS partial,
  COUNTIF(pred_norm = '')                                         AS abstained,
  ROUND(100 * COUNTIF(pred_norm = truth_title) / COUNT(*), 1)     AS exact_pct
FROM compared;
