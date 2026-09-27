# Unsupervised learning

What to do when you have no labels. Clustering, dimensionality reduction, recommenders and anomaly detection, all in SQL.

> **Module, not a lab.** Everything else in this path assumes you have a label column. This one does not.

---

## 1. The split that decides everything

Supervised learning needs a right answer for each row. Unsupervised learning does not.

| | Supervised | Unsupervised |
|---|---|---|
| Needs labels | yes | no |
| Answers | "what will happen?" | "what is in here?" |
| Evaluated against | held-out truth | itself |
| Example | will this customer churn? | what kinds of customer do we have? |

Google states the difference plainly:

> *"Unlike supervised machine learning, which is about predictive analytics, unsupervised machine learning is about descriptive analytics. Unsupervised machine learning can help you understand your data so that you can make data-driven decisions."*

That word **descriptive** carries a warning. These models describe your data. They do not tell you whether the description is correct. §6 covers what to do about that.

---

## 2. Four models, four jobs

| Model type | Use it to |
|---|---|
| **`KMEANS`** | Group similar rows together. Customer segments. |
| **`PCA`** | Reduce many columns to a few. |
| **`AUTOENCODER`** | Reduce non-linearly, or detect anomalies. |
| **`MATRIX_FACTORIZATION`** | Recommend items to users. |

All four support `ML.DETECT_ANOMALIES` except matrix factorization.

---

## 3. K-means clustering

```sql
CREATE OR REPLACE MODEL `mydataset.customer_segments`
OPTIONS (
  MODEL_TYPE = 'KMEANS',
  NUM_CLUSTERS = 5,
  KMEANS_INIT_METHOD = 'KMEANS++',
  DISTANCE_TYPE = 'EUCLIDEAN',
  STANDARDIZE_FEATURES = TRUE
) AS
SELECT
  tenure_months,
  monthly_charges,
  support_tickets_90d,
  contract
FROM `mydataset.customers`;
```

Note there is no `input_label_cols`. There is nothing to predict.

### The options that matter

| Option | Values | Default |
|---|---|---|
| `NUM_CLUSTERS` | 2 to 100 | **`log10(n)`** |
| `KMEANS_INIT_METHOD` | `RANDOM`, `KMEANS++`, `CUSTOM` | **`RANDOM`** |
| `DISTANCE_TYPE` | `EUCLIDEAN`, `COSINE` | `EUCLIDEAN` |
| `STANDARDIZE_FEATURES` | TRUE, FALSE | `TRUE` |
| `MAX_ITERATIONS` | integer | 20 |

> **Common mistake: leaving `KMEANS_INIT_METHOD` unset.** The default is `RANDOM`, not `KMEANS++`. Google says of KMEANS++: *"Using this approach usually trains a better model than using random cluster initialization."* Set it.

If you omit `NUM_CLUSTERS`, BigQuery picks `log10(n)`. For 100,000 rows that is 5. It is a starting point, not an answer.

### Choosing the number of clusters

Google's documented method is not the elbow method. It is hyperparameter tuning on the Davies-Bouldin index:

```sql
CREATE OR REPLACE MODEL `mydataset.customer_segments`
OPTIONS (
  MODEL_TYPE = 'KMEANS',
  NUM_CLUSTERS = HPARAM_RANGE(2, 10),
  NUM_TRIALS = 10,
  MAX_PARALLEL_TRIALS = 2,
  HPARAM_TUNING_OBJECTIVES = ['DAVIES_BOULDIN_INDEX']
) AS
SELECT ... FROM `mydataset.customers`;
```

Davies-Bouldin is the default objective if you tune and do not name one. Lower is better.

You may still use the elbow method. Just know it is general practice, not something Google documents here.

### Reading the result

`ML.PREDICT` gives you `centroid_id` and `nearest_centroids_distance`, an array of distances to the nearest clusters.

`ML.EVALUATE` gives you `davies_bouldin_index` and `mean_squared_distance`.

`ML.CENTROIDS` is the one you actually use to understand the clusters. It returns one row per feature per centroid:

```sql
SELECT centroid_id, feature, numerical_value
FROM ML.CENTROIDS(MODEL `mydataset.customer_segments`,
                  STRUCT(TRUE AS standardize))
ORDER BY centroid_id, ABS(numerical_value) DESC;
```

> **Set `STANDARDIZE` to TRUE here.** The argument defaults to `FALSE` on `ML.CENTROIDS`, which is the opposite of the training default. Standardizing *"allows the absolute magnitude of the values to be compared to each other"*. Without it, a feature measured in thousands looks more important than one measured in single digits.

### Feature handling under the hood

Categorical columns are one-hot encoded automatically. This applies to `BOOL`, `STRING`, `BYTES`, `DATE`, `DATETIME` and `TIME`.

`STANDARDIZE_FEATURES` controls numerical features only. It *"doesn't affect automatic preprocessing of non-numerical features"*.

One detail that surprises people: *"Changing the order of columns in the SELECT statement can affect the centroids in the final model."*

---

## 4. PCA

PCA turns many correlated columns into a few uncorrelated ones.

```sql
CREATE OR REPLACE MODEL `mydataset.customer_pca`
OPTIONS (
  MODEL_TYPE = 'PCA',
  PCA_EXPLAINED_VARIANCE_RATIO = 0.9,
  SCALE_FEATURES = TRUE
) AS
SELECT * EXCEPT (customer_id) FROM `mydataset.customers`;
```

**You must set exactly one of two options.** Either `NUM_PRINCIPAL_COMPONENTS` (how many components you want) or `PCA_EXPLAINED_VARIANCE_RATIO` (how much variance you want to keep, between 0 and 1). Setting both is an error.

The ratio is usually the better choice. It says "keep enough components to explain 90% of the variance" and lets the data decide how many that is.

> **Note the option name.** PCA uses `SCALE_FEATURES`. K-means uses `STANDARDIZE_FEATURES`. They do a similar job under different names, and both default to `TRUE`.

### The three inspection functions

| Function | Returns |
|---|---|
| `ML.PREDICT` | `principal_component_1`, `_2`, … — your reduced data |
| `ML.PRINCIPAL_COMPONENTS` | The eigenvectors: which original features load onto which component |
| `ML.PRINCIPAL_COMPONENT_INFO` | `eigenvalue`, `explained_variance_ratio`, `cumulative_explained_variance_ratio` |

The third one answers "how many components do I need?".

```sql
SELECT principal_component_id, explained_variance_ratio,
       cumulative_explained_variance_ratio
FROM ML.PRINCIPAL_COMPONENT_INFO(MODEL `mydataset.customer_pca`)
ORDER BY principal_component_id;
```

`ML.EVALUATE` on a PCA model returns one number: `total_explained_variance_ratio`.

---

## 5. Autoencoders and matrix factorization

### `AUTOENCODER`

A neural network that compresses data and reconstructs it. What it fails to reconstruct is unusual.

Use it for *"unsupervised anomaly detection and non-linear dimensionality reduction"*. PCA can only find linear structure; an autoencoder can find curved structure.

`ML.PREDICT` returns `latent_col_1`, `latent_col_2` and so on. It also works with `AI.GENERATE_EMBEDDING`.

### `MATRIX_FACTORIZATION`

The classic recommender. It learns hidden factors for users and items from a table of user, item and rating.

```sql
CREATE OR REPLACE MODEL `mydataset.recommender`
OPTIONS (
  MODEL_TYPE = 'MATRIX_FACTORIZATION',
  FEEDBACK_TYPE = 'IMPLICIT',
  USER_COL = 'user_id',
  ITEM_COL = 'product_id',
  RATING_COL = 'view_count',
  WALS_ALPHA = 40.0
) AS
SELECT user_id, product_id, view_count FROM `mydataset.events`;
```

**`FEEDBACK_TYPE` is the first decision.**

- `EXPLICIT` — real ratings, *"for example 1-5… movie recommendations"*.
- `IMPLICIT` — behaviour that suggests preference. Views, clicks, purchases. Use `WALS_ALPHA` with this one; it does nothing for explicit feedback.

Most real data is implicit. People rarely rate things.

> ### This model needs a reservation
>
> *"Matrix factorization models are only available to customers with reservations."*
>
> *"To create a matrix factorization model you must create a reservation that uses the BigQuery Enterprise or Enterprise Plus edition, and then create a reservation assignment that uses the QUERY job type."*
>
> The pricing page lists on-demand matrix factorization model creation as **"Not supported"**. Standard edition does not qualify either. It must be Enterprise or Enterprise Plus.
>
> This applies to **creating** the model. `ML.RECOMMEND` and `ML.EVALUATE` run at normal on-demand rates.

`ML.RECOMMEND` *"generate[s] a predicted rating for every user-item row combination"*. Call it with no input and it returns every user against every item, which the docs warn *"can generate large outputs"*. Pass a table of users to limit it.

For a user or item never seen in training, it falls back to `global__intercept__ + __intercept__`. That is the cold-start problem, and it has no good answer inside the model.

---

## 6. Anomaly detection

`ML.DETECT_ANOMALIES` works on five model types:

| Model | Metric used |
|---|---|
| `KMEANS` | `normalized_distance` |
| `PCA` | `mean_squared_error` |
| `AUTOENCODER` | `mean_squared_error` |
| `ARIMA_PLUS`, `ARIMA_PLUS_XREG` | time series |

```sql
SELECT * FROM ML.DETECT_ANOMALIES(
  MODEL `mydataset.customer_segments`,
  STRUCT(0.02 AS contamination),
  TABLE `mydataset.new_customers`
);
```

**`CONTAMINATION` is you telling the model how many anomalies to find.** It is *"the proportion of anomalies in the training dataset"*, in the range [0, 0.5]. The model sorts rows by the metric and cuts at that quantile.

So setting `contamination = 0.02` guarantees that 2% of rows come back as anomalies. It does not discover that 2% are anomalous. If your data is perfectly clean, you still get 2%.

For k-means and PCA and autoencoder, `CONTAMINATION` and an input table are **required**. For the time-series models they are optional.

Output is always `is_anomaly`, plus the metric that produced it.

> **New in 2026: `AI.DETECT_ANOMALIES`.** It uses BigQuery ML's built-in pre-trained **TimesFM** model, so you train nothing. *"If you don't want to manage your own time series anomaly detection model, you can use the `AI.DETECT_ANOMALIES` function."* It is time-series only, so it does not replace `ML.DETECT_ANOMALIES` for k-means, PCA or autoencoder data.

---

## 7. The hard part: evaluating without truth

There is no held-out set. Google says so directly:

> *"For k-means, PCA, autoencoder, and ARIMA_PLUS models, BigQuery ML uses all of the input data as training data, and evaluation metrics are calculated against the entire input dataset."*

And:

> *"For unsupervised learning models, model evaluation is less defined and typically varies from model to model."*

This matters more than it sounds. A Davies-Bouldin index tells you the clusters are geometrically tight and well separated. It cannot tell you they are the **right** clusters, because there is no right answer to compare against.

### Practical substitutes for ground truth

**Name the clusters in business terms.** Google's own tutorial does this. It looks at a centroid and writes *"Centroid 3 shows a busy city station that is close to the city center."* If you cannot describe a cluster in a sentence a colleague would recognise, the clustering is probably not useful.

**Test it against a decision.** The same tutorial asks: *"Assume that you want to stock some stations with racing bikes. Which stations should you choose?"* Then it answers from the clusters. A segmentation that changes no decision is a segmentation nobody needs.

**Check stability.** Rerun with a different seed or a different sample. If the clusters move a lot, they are an artefact of the algorithm rather than a structure in the data.

**Check the sizes.** One cluster holding 95% of rows and four holding the rest usually means the features are wrong, not that you found four rare types.

---

## 8. Common mistakes

**Leaving `KMEANS_INIT_METHOD` at its default.** It is `RANDOM`. Set `KMEANS++`.

**Trusting `NUM_CLUSTERS` when you did not set it.** The default is `log10(n)`, which is a guess based on row count and nothing else.

**Forgetting `STANDARDIZE` on `ML.CENTROIDS`.** It defaults to FALSE, so unscaled features look more important than they are.

**Reading `contamination` as a measurement.** It is an instruction. You are choosing the anomaly rate.

**Planning a matrix factorization model on on-demand pricing.** It will not run. You need an Enterprise or Enterprise Plus reservation.

**Treating a low Davies-Bouldin score as proof.** It measures geometry, not meaning.

**Clustering on raw unstandardized money and counts.** Monthly charges in the hundreds will dominate ticket counts in the single digits. Standardization is on by default for a reason, so do not turn it off without a reason.

---

## 9. Practice questions

<details markdown="1">
<summary><b>1.</b> You cluster customers and every cluster looks the same on most features. What went wrong?</summary>

Most likely the features do not separate customers, or one feature dominates the distance calculation.

Check `ML.CENTROIDS` with `STANDARDIZE` set to TRUE and see which features actually differ between centroids. If none do, the problem is the feature set, not the number of clusters.
</details>

<details markdown="1">
<summary><b>2.</b> Your anomaly detection found exactly 2% anomalies. Is that the true rate?</summary>

No. You set `contamination = 0.02`, and that defines the cutoff. The function sorts rows by reconstruction error or distance and marks the worst 2%.

It ranks rows well. It does not decide how many are genuinely anomalous.
</details>

<details markdown="1">
<summary><b>3.</b> Your matrix factorization model fails to create. The query is valid.</summary>

Check your pricing model. Matrix factorization requires a **reservation using the Enterprise or Enterprise Plus edition**, with a reservation assignment for the `QUERY` job type. On-demand is listed as not supported, and Standard edition does not qualify.

Prediction is unaffected. Only model creation is restricted.
</details>

<details markdown="1">
<summary><b>4.</b> How do you know a clustering is good?</summary>

You cannot know it is correct, because there is no ground truth. `ML.EVALUATE` measures geometry only, and it measures it on the training data.

Judge it three ways instead. Can you name each cluster in business terms? Does it change a decision? Is it stable across reruns and samples?
</details>

---

## Choosing among the four model types

Unsupervised learning is **descriptive**, not predictive, and needs no labels. **`KMEANS`** groups rows: set `KMEANS_INIT_METHOD = 'KMEANS++'` because the default is `RANDOM`, and remember `NUM_CLUSTERS` defaults to `log10(n)`. Google's documented way to choose the cluster count is hyperparameter tuning on **`DAVIES_BOULDIN_INDEX`**, not the elbow method. Use **`ML.CENTROIDS` with `STANDARDIZE` set to TRUE** to interpret clusters, since that argument defaults to FALSE. **`PCA`** takes either `NUM_PRINCIPAL_COMPONENTS` or `PCA_EXPLAINED_VARIANCE_RATIO`, never both. **`MATRIX_FACTORIZATION`** builds recommenders but **requires an Enterprise or Enterprise Plus reservation** to create. **`ML.DETECT_ANOMALIES`** takes a `contamination` value that *sets* the anomaly rate rather than measuring it. And evaluation is the honest weak point: metrics are computed on the whole training set, so they show geometry rather than correctness. Validate by naming the clusters, testing a decision, and checking stability.

---

## BigQuery ML documentation links

- [CREATE MODEL for K-means](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans) · [for PCA](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca) · [for matrix factorization](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization) · [for autoencoder](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder)
- [ML.CENTROIDS](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-centroids) · [ML.PRINCIPAL_COMPONENT_INFO](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-principal-component-info) · [ML.RECOMMEND](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-recommend) · [ML.DETECT_ANOMALIES](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies)
- [Automatic preprocessing](https://cloud.google.com/bigquery/docs/auto-preprocessing) · [Model evaluation overview](https://cloud.google.com/bigquery/docs/evaluate-overview) · [K-means tutorial](https://cloud.google.com/bigquery/docs/kmeans-tutorial)
- Related: [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md) · [BigQuery fundamentals](../../data-eng-gcp/modules/BIGQUERY-FUNDAMENTALS.md)
