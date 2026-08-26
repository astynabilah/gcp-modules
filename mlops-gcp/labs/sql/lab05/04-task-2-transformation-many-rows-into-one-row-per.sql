-- Lab 5 — Feature engineering for tabular data
-- Task 2. Transformation — many rows into one row per prediction unit

CREATE OR REPLACE TABLE `telco_churn.customer_event_features` AS
WITH cutoff AS (SELECT DATE '2026-08-01' AS as_of),
windowed AS (
  SELECT
    e.customer_id,
    -- three nested windows, all ending at the cutoff
    COUNTIF(e.event_date >  DATE_SUB(c.as_of, INTERVAL 30 DAY))   AS events_30d,
    COUNTIF(e.event_date >  DATE_SUB(c.as_of, INTERVAL 90 DAY))   AS events_90d,
    COUNT(*)                                                       AS events_180d,
    COUNTIF(e.event_type = 'complaint'
            AND e.event_date > DATE_SUB(c.as_of, INTERVAL 90 DAY)) AS complaints_90d,
    COUNTIF(e.event_type = 'technical_fault'
            AND e.event_date > DATE_SUB(c.as_of, INTERVAL 90 DAY)) AS faults_90d,
    MAX(e.event_date)                                              AS last_event_date
  FROM `telco_churn.support_events` e
  CROSS JOIN cutoff c
  WHERE e.event_date <= c.as_of          -- the line that enforces point-in-time
  GROUP BY e.customer_id
)
SELECT
  w.*,
  DATE_DIFF((SELECT as_of FROM cutoff), w.last_event_date, DAY) AS days_since_last_event,
  -- trend: recent activity relative to the longer baseline
  SAFE_DIVIDE(w.events_30d, NULLIF(w.events_180d / 6.0, 0))     AS activity_ratio_30d_vs_avg
FROM windowed w;
