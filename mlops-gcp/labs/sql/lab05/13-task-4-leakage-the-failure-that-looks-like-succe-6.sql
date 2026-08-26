-- Lab 5 — Feature engineering for tabular data
-- Task 4. Leakage — the failure that looks like success

-- The gap between cutoff and label window is deliberate: if you predict churn
-- "in the next 30 days", features must stop 30 days before the label is observed.
DECLARE as_of DATE DEFAULT DATE '2026-08-01';
DECLARE label_window_days INT64 DEFAULT 30;

SELECT
  as_of                                                      AS features_computed_up_to,
  DATE_ADD(as_of, INTERVAL label_window_days DAY)            AS label_observed_by,
  'features must use event_date <= as_of, no exceptions'     AS the_rule;
