-- Lab 4 — Computer vision without training anything
-- Task 2. Create an object table

CREATE OR REPLACE EXTERNAL TABLE `vision_lab.posters`
WITH CONNECTION DEFAULT
OPTIONS (
  object_metadata = 'SIMPLE',
  uris = ['gs://cloud-samples-data/vertex-ai/dataset-management/datasets/classic-movie-posters/*']
);
