-- Lab 4 — Computer vision without training anything
-- Task 3. Tier 1 — a pretrained API

CREATE OR REPLACE MODEL `vision_lab.vision_api`
REMOTE WITH CONNECTION DEFAULT
OPTIONS (REMOTE_SERVICE_TYPE = 'CLOUD_AI_VISION_V1');
