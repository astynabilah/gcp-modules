-- Lab 5 — Feature engineering for tabular data
-- Cleanup

DROP TABLE IF EXISTS `telco_churn.support_events`;
DROP TABLE IF EXISTS `telco_churn.customer_event_features`;
DROP TABLE IF EXISTS `telco_churn.features_v2`;
DROP TABLE IF EXISTS `telco_churn.features_v3`;
DROP TABLE IF EXISTS `telco_churn.features_leaky`;
DROP MODEL IF EXISTS `telco_churn.model_v3`;
DROP MODEL IF EXISTS `telco_churn.model_leaky`;
DROP MODEL IF EXISTS `telco_churn.model_no_events`;
DROP MODEL IF EXISTS `telco_churn.model_transform`;
DROP MODEL IF EXISTS `telco_churn.abl_v1`;
DROP MODEL IF EXISTS `telco_churn.abl_v2`;
DROP MODEL IF EXISTS `telco_churn.abl_v3`;
