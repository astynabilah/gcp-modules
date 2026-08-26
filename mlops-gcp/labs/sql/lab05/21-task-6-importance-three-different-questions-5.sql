-- Lab 5 — Feature engineering for tabular data
-- Task 6. Importance — three different questions

-- drop-column test for the event features as a block
CREATE OR REPLACE MODEL `telco_churn.model_no_events`
OPTIONS (MODEL_TYPE = 'BOOSTED_TREE_CLASSIFIER', INPUT_LABEL_COLS = ['churn'],
         AUTO_CLASS_WEIGHTS = TRUE)
AS SELECT * EXCEPT (customer_id, events_30d, events_90d, events_180d,
                    complaints_90d, faults_90d, days_since_last_event,
                    activity_ratio_30d_vs_avg)
FROM `telco_churn.features_v3`;

SELECT 'with events' AS variant, roc_auc FROM ML.EVALUATE(
  MODEL `telco_churn.model_v3`,
  (SELECT * EXCEPT (customer_id) FROM `telco_churn.features_v3`))
UNION ALL
SELECT 'without events', roc_auc FROM ML.EVALUATE(
  MODEL `telco_churn.model_no_events`,
  (SELECT * EXCEPT (customer_id) FROM `telco_churn.features_v3`));
