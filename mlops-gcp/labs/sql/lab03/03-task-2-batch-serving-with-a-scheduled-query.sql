-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 2. Batch serving with a scheduled query

CREATE OR REPLACE TABLE `telco_churn.churn_scores_history` (
  score_date      DATE      NOT NULL,
  customer_id     STRING    NOT NULL,
  p_churn         FLOAT64,
  risk_tier       STRING,
  contract        STRING,
  tenure_months   INT64,
  monthly_charges FLOAT64,
  model_version   STRING,
  scored_at       TIMESTAMP
)
PARTITION BY score_date
CLUSTER BY risk_tier, customer_id
OPTIONS (
  partition_expiration_days = 400,
  description = 'Nightly churn scores. One partition per scoring run.'
);
