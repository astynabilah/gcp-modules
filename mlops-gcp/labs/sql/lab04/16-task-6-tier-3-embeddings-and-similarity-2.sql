-- Lab 4 — Computer vision without training anything
-- Task 6. Tier 3 — embeddings and similarity

SELECT file_name, ARRAY_LENGTH(embedding) AS dims
FROM `vision_lab.poster_embeddings`
LIMIT 3;
