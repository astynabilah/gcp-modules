-- Lab 4 — Computer vision without training anything
-- Bringing your own images

CREATE OR REPLACE EXTERNAL TABLE `vision_lab.my_images`
WITH CONNECTION DEFAULT
OPTIONS (
  object_metadata = 'SIMPLE',
  uris = ['gs://PROJECT_ID-vision-lab/images/*']
);
