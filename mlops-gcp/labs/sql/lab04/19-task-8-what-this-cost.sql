-- Lab 4 — Computer vision without training anything
-- Task 8. What this cost

SELECT
  (SELECT COUNT(*) FROM `vision_lab.posters`)                AS images,
  (SELECT COUNT(*) FROM `vision_lab.poster_labels_raw`)      AS vision_api_units,
  (SELECT COUNT(*) FROM `vision_lab.poster_attributes`)      AS gemini_calls,
  (SELECT COUNT(*) FROM `vision_lab.poster_embeddings`)      AS embedding_calls;
