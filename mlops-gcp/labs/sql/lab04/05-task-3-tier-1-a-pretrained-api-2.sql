-- Lab 4 — Computer vision without training anything
-- Task 3. Tier 1 — a pretrained API

CREATE OR REPLACE TABLE `vision_lab.poster_labels_raw` AS
SELECT *
FROM ML.ANNOTATE_IMAGE(
  MODEL `vision_lab.vision_api`,
  TABLE `vision_lab.posters`,
  STRUCT(['LABEL_DETECTION'] AS vision_features)
);
