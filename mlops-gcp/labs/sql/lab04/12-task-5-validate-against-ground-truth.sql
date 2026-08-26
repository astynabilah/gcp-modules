-- Lab 4 — Computer vision without training anything
-- Task 5. Validate against ground truth

WITH compared AS (
  SELECT
    file_name,
    title AS predicted_title,
    -- filename -> comparable form: strip extension, underscores to spaces
    LOWER(REGEXP_REPLACE(REGEXP_REPLACE(file_name, r'\.[a-z]+$', ''), r'_', ' ')) AS truth_title,
    LOWER(TRIM(COALESCE(title, ''))) AS pred_norm,
    year, genre
  FROM `vision_lab.poster_attributes`
)
SELECT
  file_name,
  truth_title,
  predicted_title,
  year,
  CASE
    WHEN pred_norm = ''                              THEN 'abstained'
    WHEN pred_norm = truth_title                     THEN 'exact'
    WHEN STRPOS(truth_title, pred_norm) > 0
      OR STRPOS(pred_norm, truth_title) > 0          THEN 'partial'
    ELSE                                                  'mismatch'
  END AS verdict
FROM compared
ORDER BY verdict, file_name;
