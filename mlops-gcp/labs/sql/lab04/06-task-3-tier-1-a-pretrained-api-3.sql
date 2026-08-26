-- Lab 4 — Computer vision without training anything
-- Task 3. Tier 1 — a pretrained API

SELECT COUNTIF(ml_annotate_image_status != '') AS failed
FROM `vision_lab.poster_labels_raw`;
