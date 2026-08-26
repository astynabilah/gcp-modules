-- Lab 3 — Serve a trained model: batch, online, and back inside SQL
-- Task 7. Call the endpoint back from BigQuery

CREATE OR REPLACE MODEL `telco_churn.churn_endpoint`
INPUT (
  contract         STRING,
  tenure_months    INT64,
  monthly_charges  FLOAT64
)
OUTPUT (
  predicted_churn  STRING,
  churn_probs      ARRAY<FLOAT64>
)
REMOTE WITH CONNECTION `us.gemini-conn`
OPTIONS (
  ENDPOINT = 'https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/endpoints/ENDPOINT_ID'
);
