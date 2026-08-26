-- Lab 2 — Predict customer churn end-to-end with BigQuery ML (no code)
-- Task 9. Turn probabilities into a decision

DECLARE offer_cost      FLOAT64 DEFAULT 12.0;   -- cost of making a retention offer
DECLARE save_rate       FLOAT64 DEFAULT 0.30;   -- share of contacted churners actually retained
DECLARE months_retained FLOAT64 DEFAULT 12.0;   -- how long a saved customer stays
DECLARE margin_rate     FLOAT64 DEFAULT 0.45;   -- gross margin on revenue

SELECT
  ROUND(th, 2)                                                       AS threshold,
  COUNTIF(p_churn >= th)                                             AS contacted,
  COUNTIF(p_churn >= th AND actual_churn = 'Yes')                    AS churners_reached,
  ROUND(SAFE_DIVIDE(COUNTIF(p_churn >= th AND actual_churn = 'Yes'),
                    COUNTIF(p_churn >= th)), 3)                       AS precision,
  ROUND(SAFE_DIVIDE(COUNTIF(p_churn >= th AND actual_churn = 'Yes'),
                    COUNTIF(actual_churn = 'Yes')), 3)                AS recall,
  ROUND(
    SUM(IF(p_churn >= th AND actual_churn = 'Yes',
           monthly_charges * months_retained * margin_rate * save_rate, 0))
    - COUNTIF(p_churn >= th) * offer_cost
  , 0)                                                                AS net_value
FROM `telco_churn.churn_scores`, UNNEST(GENERATE_ARRAY(0.10, 0.90, 0.05)) AS th
GROUP BY th
ORDER BY th;
