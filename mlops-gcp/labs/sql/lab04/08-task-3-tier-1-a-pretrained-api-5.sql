-- Lab 4 — Computer vision without training anything
-- Task 3. Tier 1 — a pretrained API

SELECT label, COUNT(*) AS images, ROUND(AVG(score), 3) AS avg_score
FROM `vision_lab.poster_labels`
GROUP BY label
ORDER BY images DESC
LIMIT 15;
