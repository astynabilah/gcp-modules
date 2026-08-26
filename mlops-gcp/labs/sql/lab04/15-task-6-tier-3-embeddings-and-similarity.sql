-- Lab 4 — Computer vision without training anything
-- Task 6. Tier 3 — embeddings and similarity

CREATE OR REPLACE TABLE `vision_lab.poster_embeddings` AS
SELECT
  uri,
  REGEXP_EXTRACT(uri, r'([^/]+)$') AS file_name,
  AI.EMBED(ref, endpoint => 'multimodalembedding@001').result AS embedding
FROM `vision_lab.posters`;
