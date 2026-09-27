# Time series forecasting

Predicting what comes next, when the data has an order. This is the one part of ML where a random train/test split is wrong.

> **Module, not a lab.** Everything here runs in BigQuery SQL unless marked otherwise.

---

## Deprecations and renames to know

| Item | Status |
|---|---|
| **`ARIMA`** model type | **Deprecated.** Use `ARIMA_PLUS`. |
| `ML.EVALUATE` without input data | **Deprecated.** Use `ML.ARIMA_EVALUATE`. |
| **TimesFM** via `AI.FORECAST` | **GA** since October 2025. Some reference pages still label it Preview; that badge is stale. |
| **Vertex AI** | Now branded **Gemini Enterprise Agent Platform**. Old URLs and SDK class names still work. |

---

## 1. Regression's mismatch with time-ordered data

A common question: if I have a date column and a number column, why not just run linear regression on the date?

You can. It usually looks fine and is usually wrong. Three reasons.

**Rows are not independent.** Ordinary regression assumes each row is an independent sample. Today's sales are not independent of yesterday's. That correlation between a series and its own past is called **autocorrelation**, and it breaks the assumption the model rests on.

**The series changes over time.** Trend and seasonality mean the average and the variance shift. A model fitted on last year's level does not describe this year's.

**A random split leaks the future.** This is the concrete one. Split randomly and your training set contains rows from *after* rows in your test set. The model has seen the future and is being tested on the past. The score looks excellent and means nothing.

Google states the rule directly in *Rules of Machine Learning*:

> *"**Rule #33: If you produce a model based on the data until January 5th, test the model on the data from January 6th and after.** In general, measure performance of a model on the data gathered after the data you trained the model on, as this better reflects what your system will do in production."*

And in the Vertex data-split docs:

> *"The default split is not the best choice if: **You're not training a forecasting model, but your data is time-sensitive.** In this case, use a chronological split, or a manual split that results in the most recent data being used as the test set."*

> **A caution about vocabulary.** The autocorrelation and non-stationarity arguments above are standard statistics, not something Google states in those words. Rule #33 and the split guidance are Google's. The rest is the field's.

### Splitting by time instead

| Context | Split approach |
|---|---|
| **BigQuery ML**, non-forecasting model on time data | `DATA_SPLIT_METHOD = 'SEQ'` with `DATA_SPLIT_COL` |
| **BigQuery ML**, `ARIMA_PLUS` | No split options exist. Hold out data yourself and pass it to `ML.EVALUATE`. |
| **Vertex AI** forecasting | **Chronological split by default**, 80/10/10 |
| **Vertex AI** other tabular models | Random by default. Change it if your data is time-sensitive. |

`SEQ` sorts by a column and takes the **last** rows for evaluation. Compare that with `RANDOM`, which the docs describe as *"based on the `FARM_FINGERPRINT` of the data"*: a hash, completely blind to time.

The field calls the proper approach **forward chaining** or **walk-forward validation**. Google's docs use *"chronological split"* and *"timestamp split"*. Same idea, different words.

---

## 2. `ARIMA_PLUS`: the automatic pipeline

```sql
CREATE OR REPLACE MODEL `mydataset.sales_forecast`
OPTIONS (
  MODEL_TYPE = 'ARIMA_PLUS',
  TIME_SERIES_TIMESTAMP_COL = 'sale_date',
  TIME_SERIES_DATA_COL = 'units_sold',
  HORIZON = 90,
  HOLIDAY_REGION = 'US'
) AS
SELECT sale_date, SUM(units) AS units_sold
FROM `mydataset.sales`
GROUP BY sale_date;
```

That one statement runs a nine-step pipeline:

1. Infer the data frequency
2. Handle irregular time intervals
3. Handle duplicate timestamps by taking the mean
4. Interpolate missing data
5. Detect and clean spike and dip outliers
6. Detect and adjust abrupt step changes
7. Detect and adjust holiday effects
8. Detect seasonal patterns using STL, extrapolate with double exponential smoothing
9. Model the trend with ARIMA, tuned automatically by auto.ARIMA

Step 9 is doing a lot: *"dozens of candidate models are trained and evaluated in parallel. The model with the lowest Akaike information criterion (AIC) is selected as the best model."*

Steps 2 and 3 are the ones people do not expect. Irregular gaps and duplicate timestamps are handled without you cleaning them first.

### The options that matter

| Option | Default | Notes |
|---|---|---|
| `TIME_SERIES_TIMESTAMP_COL` | required | `TIMESTAMP`, `DATE` or `DATETIME` |
| `TIME_SERIES_DATA_COL` | required | must be numeric |
| `TIME_SERIES_ID_COL` | none | one column or an array. See §5. |
| `HORIZON` | **1,000** | max 10,000 |
| `AUTO_ARIMA` | TRUE | must stay TRUE for multiple series |
| `DATA_FREQUENCY` | `AUTO_FREQUENCY` | finest is `PER_MINUTE` |
| `HOLIDAY_REGION` | **off** | see below |
| `CLEAN_SPIKES_AND_DIPS` | TRUE | |
| `ADJUST_STEP_CHANGES` | TRUE | |
| `DECOMPOSE_TIME_SERIES` | TRUE | needed for `ML.EXPLAIN_FORECAST` |

> **Holidays are off unless you ask.** Step 7 only runs if you set `HOLIDAY_REGION`. Two more limits: *"Holiday effect modeling is only applicable when the time series is daily or weekly, and longer than a year"*, and it is *"effective only for approximately 5 years"*.

---

## 3. Getting the forecast out

```sql
SELECT * FROM ML.FORECAST(
  MODEL `mydataset.sales_forecast`,
  STRUCT(30 AS horizon, 0.8 AS confidence_level)
);
```

`horizon` defaults to **3**. `confidence_level` defaults to **0.95** and must be in `[0, 1)`.

> **The forecast is computed at `CREATE MODEL` time, not here.** The docs are explicit: *"Forecasting takes place when the `CREATE MODEL` statement runs. `ML.FORECAST` just retrieves the forecasting values and computes the prediction intervals."*
>
> So `HORIZON` in `CREATE MODEL` is the real setting. The one in `ML.FORECAST` only filters what you already computed, and it cannot exceed it.

**Output columns:** `forecast_timestamp`, `forecast_value`, `standard_error`, `confidence_level`, plus both a **prediction interval** and a **confidence interval** (lower and upper bounds for each).

Two details worth knowing. `forecast_value` is *"the average of the `prediction_interval_lower_bound` and `prediction_interval_upper_bound` values"*. And `forecast_timestamp` is always a `TIMESTAMP`, whatever type your input column was.

---

## 4. Explaining a forecast

`ML.EXPLAIN_FORECAST` returns everything `ML.FORECAST` does, plus the decomposition. It needs `DECOMPOSE_TIME_SERIES = TRUE`.

```sql
SELECT * FROM ML.EXPLAIN_FORECAST(
  MODEL `mydataset.sales_forecast`,
  STRUCT(30 AS horizon)
);
```

You get history rows **and** forecast rows, marked by `time_series_type`. The components:

| Column | Is |
|---|---|
| `trend` | the long-run direction |
| `seasonal_period_yearly` … `_daily` | one column per detected seasonality |
| `holiday_effect` | plus one column per named holiday |
| `spikes_and_dips` | outliers that were cleaned |
| `step_changes` | level shifts that were adjusted |
| `residual` | what is left over |

They add up. For history rows, the data equals trend plus the seasonal terms plus holiday effect plus spikes and dips plus step changes plus residual.

> **Three columns are NULL on forecast rows.** `spikes_and_dips`, `step_changes` and `residual` describe what happened, so they do not exist for the future. The docs put it plainly: *"For future data, the `spikes_and_dips`, `step_changes`, and `residuals` values aren't applicable."*

This decomposition is the main reason to choose `ARIMA_PLUS` over a foundation model. You can show someone *why* the forecast rises in December.

---

## 5. Thousands of series in one statement

Set `TIME_SERIES_ID_COL` and BigQuery fits a separate model per series.

```sql
CREATE OR REPLACE MODEL `mydataset.store_forecast`
OPTIONS (
  MODEL_TYPE = 'ARIMA_PLUS',
  TIME_SERIES_TIMESTAMP_COL = 'date',
  TIME_SERIES_DATA_COL = 'units_sold',
  TIME_SERIES_ID_COL = ['store_id', 'product_id'],
  HORIZON = 30
) AS
SELECT date, store_id, product_id, SUM(units) AS units_sold
FROM `mydataset.sales`
GROUP BY date, store_id, product_id;
```

The documented ceiling is large: *"You can forecast up to **100,000,000** time series simultaneously with a single query."*

Other limits:

| Limit | Value |
|---|---|
| Minimum points per series | **3** |
| Maximum points per series | 500,000 with decomposition, 1,000,000 without |
| Maximum forecast points | 10,000 |
| Console evaluation tab shows | first **100** series only |

> **Failures are silent.** *"any invalid time series that fail the model fitting are ignored and don't appear in the results of forecast."* A warning appears, and `ML.ARIMA_EVALUATE` gives you the error message. If you forecast 5,000 products and get 4,900 back, nothing raises an error. Count your rows.

To speed up large runs, set `AUTO_ARIMA_MAX_ORDER = 1`. The docs say this cuts runtime *"by more than 50%"*.

---

## 6. Hierarchical forecasting

Forecasts of parts should add up to the forecast of the whole. If you predict per store, the store predictions should sum to the region prediction.

```sql
CREATE OR REPLACE MODEL `mydataset.liquor_forecast`
OPTIONS (
  MODEL_TYPE = 'ARIMA_PLUS',
  TIME_SERIES_TIMESTAMP_COL = 'date',
  TIME_SERIES_DATA_COL = 'total_bottles_sold',
  TIME_SERIES_ID_COL = ['store_number', 'zip_code', 'city', 'county'],
  HIERARCHICAL_TIME_SERIES_COLS = ['zip_code', 'store_number'],
  HOLIDAY_REGION = 'US'
) AS
SELECT ... ;
```

Two options doing different jobs:

- **`TIME_SERIES_ID_COL`** — which series to generate
- **`HIERARCHICAL_TIME_SERIES_COLS`** — which levels to roll up and reconcile

*"The column order represents the hierarchy structure, where the left-most column is the parent."* Reconciliation means *"the sum of the forecasted values for all of the cities in State A must be equal to the forecasted value for State A."*

This option is on `ARIMA_PLUS` only, not on `ARIMA_PLUS_XREG`.

---

## 7. Adding external variables: `ARIMA_PLUS_XREG`

`ARIMA_PLUS` looks only at the series' own history. `ARIMA_PLUS_XREG` adds outside variables such as price, temperature or a promotion flag. The docs describe it as *"an `ARIMA_PLUS` model with **linear external regressors**"*.

> **The catch: you must know the future values of your regressors.** `ARIMA_PLUS` needs no input at forecast time. `ARIMA_PLUS_XREG` needs a table of future regressor values, and for `ML.EXPLAIN_FORECAST` *"The TABLE argument is required for the `ARIMA_PLUS_XREG` model."*
>
> This is fine for planned promotions or known prices. It does not work for anything you would also have to forecast.

One more trap: missing regressor values are filled with *"the mean value of the entire data column, which might include values from different time series"*. Google's own advice is to impute them yourself before training.

---

## 8. TimesFM: forecasting without a model

Since 2025 BigQuery has a built-in pre-trained forecasting model. You train nothing.

```sql
SELECT * FROM AI.FORECAST(
  TABLE `mydataset.sales`,
  data_col => 'units_sold',
  timestamp_col => 'sale_date',
  horizon => 30
);
```

No `CREATE MODEL`. TimesFM is *"a foundation model for time-series forecasting that has been pre-trained on billions of time-points"*.

| Argument | Default |
|---|---|
| `model` | **TimesFM 2.5** (2.0 also available) |
| `horizon` | 10, max 10,000 |
| `confidence_level` | 0.95 |
| `context_window` | auto; up to **15,360** on 2.5 |

`forecast_value` here is the **median**, described as *"the 50% quantile value"*.

### Choosing between them

Google publishes a comparison. The important rows:

| | `ARIMA_PLUS` | TimesFM via `AI.FORECAST` |
|---|---|---|
| Training | required | **none, pre-trained** |
| Ease of use | moderate | *"Very high. Requires a single function call"* |
| Customization | **High** | Low |
| Explainability | **High** | Low |
| Covariates | yes, via XREG | **no** |
| Accuracy | *"Very high"* | *"Very high"* |

Both are rated very high for accuracy, so accuracy is not the deciding factor. **Choose on whether you need to explain the result.** If someone will ask why the forecast moved, you need `ML.EXPLAIN_FORECAST` and therefore `ARIMA_PLUS`. If you need a number quickly, `AI.FORECAST` is one function call.

Companions: `AI.EVALUATE` and `AI.DETECT_ANOMALIES` work the same way.

> **New in August 2026, in Preview:** `ML.TREND`, `ML.SEASONALITY` and `ML.DETECT_CHANGE_POINTS`. These give you decomposition without training a model at all.

---

## 9. Vertex AI forecasting

Use this when your data is not in BigQuery, or when you want more model choice.

**Four training methods:**

| Method | Google's description |
|---|---|
| **TiDE** | *"Great model quality with fast training and inference, especially for long contexts and horizons."* |
| **TFT** | *"designed to produce high accuracy and interpretability"* |
| **AutoML (L2L)** | *"A good choice for a wide range of use cases."* |
| **Seq2Seq+** | *"performs well with a small time budget and on datasets smaller than 1 GB"* |

**Data requirements:**

| Requirement | Value |
|---|---|
| Size | ≤ 100 GB |
| Columns | 3 to 100 |
| Rows | 1,000 to 100,000,000 |
| Series length | ≤ 3,000 time steps |
| Format | narrow (long) |

Vertex makes a distinction BigQuery does not, and it is a useful one to learn:

| Column type | Known at forecast time? |
|---|---|
| **Attribute** — static, like store size | yes |
| **Covariate, available at forecast** — like a planned price | yes |
| **Covariate, unavailable at forecast** — like actual footfall | no |

Sorting your columns into those three buckets is most of the setup work.

Guidance on how much data: *"For best results, use at least 10 time series for every column you use to train the model."*

Note that AutoML Forecasting does not support online inference. For that you need Tabular Workflow for Forecasting, which is still Preview.

---

## 10. Evaluating a forecast

```sql
SELECT * FROM ML.EVALUATE(
  MODEL `mydataset.sales_forecast`,
  (SELECT sale_date, units_sold FROM `mydataset.holdout`)
);
```

Six metrics: `mean_absolute_error`, `mean_squared_error`, `root_mean_squared_error`, `mean_absolute_percentage_error`, `symmetric_mean_absolute_percentage_error`, `mean_absolute_scaled_error`.

Which to use:

- **MAE** — average error in your units. Easy to explain.
- **RMSE** — punishes large errors more.
- **MAPE** — percentage error. Breaks when actual values are near zero.
- **sMAPE** — a symmetric fix for MAPE.
- **MASE** — compares your model against a naive forecast. Below 1 means you beat it.

**MASE is the one to look at first.** A model that cannot beat "tomorrow equals today" is not worth deploying, and MASE tells you that in one number.

Calling `ML.EVALUATE` without input data is deprecated. Use `ML.ARIMA_EVALUATE` for model diagnostics such as AIC and the selected ARIMA order.

---

## 11. Common mistakes

**Splitting time data randomly.** The model sees the future. Use `SEQ`, or a chronological split.

**Using linear regression on a date column.** It ignores autocorrelation and seasonality.

**Expecting holiday modelling by default.** Set `HOLIDAY_REGION`.

**Setting a small `HORIZON` at `CREATE MODEL` time.** The forecast is computed there. `ML.FORECAST` cannot go beyond it.

**Not counting the returned series.** Failed series are dropped silently.

**Choosing `ARIMA_PLUS_XREG` without future regressor values.** You need them at forecast time, and you cannot forecast them with the same model.

**Reporting MAPE on data containing zeros.** It goes to infinity. Use sMAPE or MAE.

**Using the deprecated `ARIMA` model type.** Use `ARIMA_PLUS`.

---

## 12. Forecasting problems, worked through

<details markdown="1">
<summary><b>1.</b> Your sales model scores well in testing and badly in production. You split the data 80/20 at random. What happened?</summary>

The random split put later rows in training and earlier rows in testing, so the model was tested on a period it had partly already seen.

Split by time instead. Use `DATA_SPLIT_METHOD = 'SEQ'` in BigQuery ML, or a chronological split in Vertex AI, which is the default for forecasting models there.
</details>

<details markdown="1">
<summary><b>2.</b> You set <code>HORIZON = 30</code> in <code>CREATE MODEL</code> and now need 90 days. Can you just change <code>ML.FORECAST</code>?</summary>

No. The forecast is produced when the model is created. `ML.FORECAST` only retrieves it, and its `horizon` cannot exceed the model's.

Retrain with a larger `HORIZON`.
</details>

<details markdown="1">
<summary><b>3.</b> You need to forecast 5,000 products and only get 4,880 back. No error appeared. Why?</summary>

Series that fail model fitting are skipped silently. Common causes are fewer than three data points or constant values.

Use `ML.ARIMA_EVALUATE` to see the error message per series, and always compare the row count you got against the count you expected.
</details>

<details markdown="1">
<summary><b>4.</b> Someone asks why the forecast jumps every December. Which model type do you need?</summary>

`ARIMA_PLUS` with `DECOMPOSE_TIME_SERIES = TRUE`, then `ML.EXPLAIN_FORECAST`. It splits the forecast into trend, seasonal terms, and holiday effect.

TimesFM through `AI.FORECAST` is easier to run but rated Low for explainability, so it cannot answer that question.
</details>

---

## The forecasting essentials

Time series breaks the usual ML rules because rows are ordered and not independent. **A random split leaks the future**, so use `DATA_SPLIT_METHOD = 'SEQ'` in BigQuery ML or a chronological split in Vertex AI. **`ARIMA_PLUS`** runs a nine-step pipeline in one statement, including gap handling, duplicate timestamps, outlier cleaning, seasonality and auto.ARIMA tuning by lowest AIC — but **holiday modelling is off until you set `HOLIDAY_REGION`**. The forecast is produced at **`CREATE MODEL` time**, so `HORIZON` there is the setting that matters. Use `TIME_SERIES_ID_COL` for many series at once, up to 100,000,000, and check your row count because failed series are dropped silently. **`ARIMA_PLUS_XREG`** adds external variables but requires their future values. **TimesFM through `AI.FORECAST`** needs no training at all, matches ARIMA_PLUS on accuracy, and loses on explainability — so pick it when nobody will ask why. Evaluate with **MASE** first, because it tells you whether you beat a naive forecast.

---

## BigQuery ML forecasting reference

- [CREATE MODEL for time series](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series) · [ML.FORECAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast) · [ML.EXPLAIN_FORECAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast)
- [TimesFM model](https://cloud.google.com/bigquery/docs/timesfm-model) · [AI.FORECAST](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast)
- [Hierarchical forecasting tutorial](https://cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series)
- [Vertex AI forecasting: prepare data](https://cloud.google.com/vertex-ai/docs/tabular-data/forecasting/prepare-data) · [training methods](https://cloud.google.com/vertex-ai/docs/tabular-data/forecasting-parameters)
- [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
- Related: [Unsupervised learning](UNSUPERVISED-LEARNING-ON-GCP.md) · [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md)
