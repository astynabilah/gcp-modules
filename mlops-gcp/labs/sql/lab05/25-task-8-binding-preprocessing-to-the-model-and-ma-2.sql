-- Lab 5 — Feature engineering for tabular data
-- Task 8. Binding preprocessing to the model, and managing the SQL

config {
  type: "table",
  schema: "telco_churn",
  name: "features_v2",
  description: "One row per customer, features as of the 2026-08-01 cutoff",
  assertions: {
    uniqueKey: ["customer_id"],
    nonNull: ["customer_id", "churn"]
  }
}

SELECT
  m.* EXCEPT (churn),
  COALESCE(f.events_90d, 0) AS events_90d,
  -- …
  m.churn
FROM ${ref("customers_ml")} m
LEFT JOIN ${ref("customer_event_features")} f USING (customer_id)
