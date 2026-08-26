-- Lab 4 — Computer vision without training anything
-- Task 6. Tier 3 — embeddings and similarity

SELECT
  base.file_name,
  ROUND(distance, 4) AS distance
FROM VECTOR_SEARCH(
  TABLE `vision_lab.poster_embeddings`,
  'embedding',
  (
    SELECT embedding
    FROM `vision_lab.poster_embeddings`
    WHERE file_name = 'the_great_train_robbery.jpg'
  ),
  'embedding',
  top_k => 5
)
ORDER BY distance;
