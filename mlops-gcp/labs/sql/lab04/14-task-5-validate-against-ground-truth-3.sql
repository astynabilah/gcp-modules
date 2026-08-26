-- Lab 4 — Computer vision without training anything
-- Task 5. Validate against ground truth

SELECT file_name, title, year, genre
FROM `vision_lab.poster_attributes`
WHERE title IS NOT NULL
ORDER BY file_name;
