# Low-code ML on Google Cloud — a six-lab series

Six self-paced, Google-Cloud-Skills-Boost-style labs plus thirteen theoretical modules, covering the path from raw data to a validated, explainable, served model. Mostly in SQL and the console. Labs 1–5 need no Python at all; Lab 6 and the Kubeflow/ML Metadata modules are where you deliberately step outside low-code, and each says why.

> **Written against the Google Cloud console as of 23 August 2026.** See [Recent platform changes](#recent-platform-changes) — the Vertex AI rebrand moved several menu paths that older tutorials still reference.

---

## The labs

### [Lab 1 — Analyze customer review sentiment with Gemini in BigQuery](lab-01-sentiment-analysis-bigquery-gemini.md)

**75–90 min · Intermediate · ~US$2–4 in Gemini usage for the full run**

Score 22,641 real e-commerce clothing reviews for sentiment, confidence, and product themes by calling Gemini directly from a `SELECT` statement — then validate the model against the star ratings it never saw.

| You'll use | For |
|---|---|
| `AI.GENERATE` | Row-level classification in SQL |
| `output_schema` | Forcing typed columns instead of prose |
| `AI.GENERATE_TABLE` + remote models | The governed alternative, and when to prefer it |
| BigQuery connections + IAM | Letting BigQuery call the Agent Platform |
| Looker Studio | Publishing the result |

**Dataset:** [Women's E-Commerce Clothing Reviews](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews) — 23,486 rows, CC0. Chosen because it pairs free text with a star rating, giving you a ground-truth signal to validate against.

---

### [Lab 2 — Predict customer churn end-to-end with BigQuery ML](lab-02-customer-churn-lowcode-bqml.md)

**90–110 min · Intermediate · low cost — mostly inside the BigQuery free tier**

Build a complete churn pipeline in SQL: type repair, feature engineering, gradient-boosted training, evaluation, explanation, hyperparameter tuning, scoring, and a decision threshold chosen from expected value rather than from `0.5`.

| You'll use | For |
|---|---|
| `CREATE MODEL … BOOSTED_TREE_CLASSIFIER` | Training, in one statement |
| `AUTO_CLASS_WEIGHTS` | Handling a 26.5% positive class |
| `ML.EVALUATE` / `ML.CONFUSION_MATRIX` / `ML.ROC_CURVE` | Measuring what matters |
| `ML.GLOBAL_EXPLAIN` / `ML.EXPLAIN_PREDICT` | Explaining the model globally and per customer |
| `NUM_TRIALS` + `TRANSFORM` | Automated tuning and skew-free preprocessing |
| Agent Platform model registry | Versioning and rollback |

**Dataset:** [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) — 7,043 rows, 21 columns. Small, honest, and containing a type trap that most tutorials walk past silently.

---

### [Lab 3 — Serve a trained model: batch, online, and back inside SQL](lab-03-serving-ml-models-lowcode.md)

**90–110 min · Intermediate · an online endpoint bills per node-hour while deployed, even with zero traffic**

Take the churn model from Lab 2 and serve it three ways, then learn which one you need. Most teams build an endpoint when a scheduled query would have done, and pay for a node 24 hours a day to do twenty minutes of work.

| You'll use | For |
|---|---|
| Scheduled queries + partitioned `MERGE` | Batch serving that costs nothing between runs |
| Agent Platform Registry → Deployments | Deploying a registered BQML model online |
| `gcloud ai endpoints predict` / REST | Calling the endpoint, and reading parallel-array responses safely |
| `CREATE MODEL … REMOTE` | Calling the deployed endpoint back *from* BigQuery |
| Model Monitoring | Drift and training-serving skew, and how to read an alert |
| Traffic splitting | Canarying a new version with instant rollback |

**Prerequisite:** Lab 2's models — or use the 3-minute catch-up script in Task 0.

---

### [Lab 4 — Computer vision without training anything](lab-04-image-vision-lowcode-bigquery.md)

**60–75 min · Intermediate · under US$0.10 — Vision API's first 1,000 units/month are free**

The deliberately minimal lab. A few dozen public-domain movie posters already in a Google-owned bucket — nothing to download, nothing to upload, nothing to train. Run the same images through three kinds of vision and feel the difference.

| You'll use | For |
|---|---|
| Object tables (`object_metadata = 'SIMPLE'`) | Giving unstructured files rows, without copying bytes |
| `ML.ANNOTATE_IMAGE` | Cloud Vision labels — a fixed pretrained vocabulary |
| `AI.GENERATE` over `ref` | Gemini answering *your* question, returning typed columns |
| `AI.EMBED` + `VECTOR_SEARCH` | Similarity and text-to-image search with no labels at all |

**Dataset:** `gs://cloud-samples-data/.../classic-movie-posters/` — public, no download. The filenames are the film titles, which gives you free ground truth to validate against.

---

### [Lab 5 — Feature engineering for tabular data](lab-05-feature-engineering-tabular.md)

**90–110 min · Intermediate–Advanced · low cost**

The part Lab 2 skipped. Covers the four separate jobs hiding inside "feature engineering" (transformation, extraction, selection, importance), with **leakage** as the centrepiece.

| You'll use | For |
|---|---|
| Window functions + `LEFT JOIN` | Event streams → one row per prediction unit |
| An explicit `as_of` cutoff | Point-in-time correctness (no tool enforces this for you) |
| `CORR`, `ML.FEATURE_INFO` | Selection filters that need no model |
| `ML.FEATURE_IMPORTANCE` vs `ML.GLOBAL_EXPLAIN` vs drop-column | Three importances, three different questions |
| `TRANSFORM`, Dataform | Binding preprocessing to the model; managing feature SQL |

You **deliberately build a leaky feature**, watch AUC jump to 0.99, and then detect it four different ways.

---

### [Lab 6 — Exploring BigQuery data from a notebook](lab-06-data-exploration-bigquery-colab.md)

**45–60 min · Beginner–Intermediate · effectively free**

Data is in BigQuery, you want it in Python. Six ways to bridge that gap, and they are not interchangeable. Uses **free Colab** — the cheapest option, with the cost comparison shown so the reasoning is visible.

| You'll use | For |
|---|---|
| Dry runs (`dry_run=True`) | Pricing a query *before* running it |
| `%%bigquery`, `to_dataframe()`, Storage Read API, `pandas_gbq` | The pull-down options and their ceilings |
| `bigframes` | Push-down — pandas API, executed in BigQuery, nothing downloaded |
| `TABLESAMPLE` vs `FARM_FINGERPRINT` | Sampling properly, and why `LIMIT` is neither a sample nor a discount |

**Dataset:** `bigquery-public-data.austin_bikeshare.bikeshare_trips` — 1.7M rows, public, no prerequisites.


---

## Not labs: the concept modules

All thirteen live at the repository root. **Modules are theoretical** — concepts, decision frameworks and reference code. The numbered **labs above are hands-on**.

### [Scaling prototypes into ML models](../modules/SCALING-PROTOTYPES-TO-ML.md)

The five stages between "it works in a notebook" and "it runs in production", which GCP service belongs at each stage, three reference architectures, a cost table, the common anti-patterns, and a readiness checklist.

Read it **before** the labs if you want the map first, or **after** Lab 3 to see how the pieces fit.

### [Vertex ML Metadata](../modules/VERTEX-ML-METADATA.md)

Lineage, artifacts, and why numeric metadata must be queried as `metadata.<field>.number_value`. Traces the answer through all three layers (the JSON you write, the `google.protobuf.Struct` it becomes, and the filter grammar that falls out of it), then covers the full data model (Artifact / Execution / Event / Context), the complete filter cheat sheet, lineage queries, and the gotchas (**there is no `int_value`**; a missing type suffix returns empty rather than erroring).

### [Vertex AI Model Monitoring](../modules/VERTEX-MODEL-MONITORING.md)

Why numerical features use **Jensen-Shannon divergence** and categorical features use **L-infinity distance**, with the reasoning rather than the mnemonic. Covers skew vs. drift (same maths, different baseline), the three things you can watch (features, predictions, attributions), threshold setting, how to read an alert without over-reacting, and why none of it measures accuracy.

### [Vertex AI Prediction autoscaling — from zero](../modules/VERTEX-AUTOSCALING.md)

Assumes no autoscaling background. Built around the one asymmetric rule that explains almost everything: with a GPU attached, Vertex scales **up when either** CPU or GPU duty cycle exceeds 60%, and **down only when both** are below. That single OR/AND produces two opposite complaints ("it scales constantly" and "it won't scale"), and the module walks both. Plus why scaling takes minutes not seconds, and why `minReplicaCount` matters more than any target tuning.

### [Networking for ML serving — from zero](../modules/GCP-NETWORKING-FOR-ML-SERVING.md)

Assumes **no networking knowledge at all** — starts from what an IP address is. Builds up to why a global external Application Load Balancer routes to the nearest region for free (anycast), the five chained objects that make up a load balancer, what a NEG is, and why **serverless NEG backends support no health checks** and need no firewall rules for probe ranges. Ends with a debugging checklist and a glossary.

### [Git and version control for ML work](../modules/GIT-FOR-ML-ON-GCP.md)

The mechanics behind the Scaling module's Stage 1. Connecting a Workbench instance to GitHub happens **entirely inside the instance** — there is no console OAuth integration and `jupyterlab-git` is already installed. Covers `git config`, generating an SSH key *in the instance* (never copying one in), and the harder half: why `.ipynb` files diff terribly, how `nbstripout` / `jupytext` / `nbdime` fix it, and what should never reach the repo.

### [Serving models on Cloud Run](../modules/SERVING-MODELS-ON-CLOUD-RUN.md)

The container side of serving, which Vertex endpoints hide. Cold start is a six-stage sequence, and the stage you control is **where the model weights live** — in the image (container streaming, good under ~10 GB), Cloud Storage, a FUSE mount, or an external hub. Explains why lazy-loading on first request is not an optimisation, and where the current documentation has moved past the advice still in wide circulation.

### [Fairness and bias detection](../modules/VERTEX-FAIRNESS-AND-BIAS.md)

The rest of the series measures whether a model is *accurate*; this one measures whether it is *fair*. `DetectDataBiasOp` before training and `DetectModelBiasOp` after batch prediction, both configured with a `BiasConfig` naming the slice feature. Explains why **feature attribution is not a bias check** (a model discriminates through proxies with the protected attribute's attribution near zero), why sliced performance metrics aren't fairness metrics, and why you should gate on the result rather than report it.

### [Event-driven ML automation](../modules/EVENT-DRIVEN-ML-AUTOMATION.md)

The counterpart to Kubeflow. Kubeflow covers how work is *organised*; this covers how it gets *started*. Cloud Functions gives **at-least-once** execution, so a timed-out API call plus a retry produces duplicate training jobs. The key point: a timeout means the outcome is **unknown**, not failed. Covers the idempotent handler keyed on the **CloudEvent id**, why the check-and-write needs a **transaction**, why the file name is the wrong dedup key, and the 7-day retry trap. Explains the idempotency that three other documents only assert.

### [`v1` vs `v1beta1` — API versions and launch stages](../modules/GCP-API-VERSIONS-AND-LAUNCH-STAGES.md)

Starts by untangling the **four different things called "version"**: API version, feature generation, SDK semver, model version. Most of the confusion comes from there. Then: what each launch stage promises (GA has an SLA and 12 months' notice; Preview has neither), how to select a version in REST / Python / gcloud, and **a section on what the split means in each other module**: scale-to-zero being `v1beta1`-only, Model Monitoring v2 living on `v1beta1`, ML Metadata needing none of it.

Every other module carries a matching **API version note** pointing back here.

### [Low-code AI solutions on Google Cloud](../modules/LOW-CODE-AI-ON-GCP.md)

The four tiers ordered by *who supplies what* (pretrained APIs, generative, AutoML, BigQuery ML), and which to pick per data type. Centrepiece is **AutoML's Cloud/Edge fork**, chosen before training and irreversible: Cloud models deploy to endpoints and cannot be exported; Edge models export to TF Lite / Core ML / TF.js and cannot be served by Google. Also: what Vertex AI Vision really is, and AutoML Edge's 2026 maintenance-mode status.

### [Where model training runs](../modules/VERTEX-TRAINING-COMPUTE.md)

The five places training can happen (BigQuery ML, the notebook kernel, the **notebook executor**, a custom training job, a pipeline step), and how to pick. Covers the Workbench **G2 ↔ non-G2** resize restriction, why the executor beats resizing your instance, the four worker pools of a custom training job, Reduction Server, and why you should fill one machine before reaching for distributed training.

### [Kubeflow Pipelines on Google Cloud](../modules/KUBEFLOW-PIPELINES-ON-GCP.md)

**The one module that is not low-code** — KFP is a Python SDK, and that is the point. Covers the KFP / Kubeflow / Vertex AI Pipelines terminology tangle, what happens when you run a pipeline, parameters vs. artifacts, control flow, caching, a real churn-retraining pipeline wrapping Lab 2's SQL with a quality gate, cost, and a clear decision map for when a scheduled query would have done instead.

---

## Recent platform changes

Everything here is written against the August 2026 console. These will trip you up if you follow older material:

| Change | Effect |
|---|---|
| **Vertex AI → Gemini Enterprise Agent Platform.** Announced 22 Apr 2026; the Vertex AI console entry was removed 21 May 2026. | Navigate to **Agent Platform**. Model Registry is now **Govern → Registry**; Endpoints are **Scale → Deployments**. The API (`aiplatform.googleapis.com`), IAM role IDs (`roles/aiplatform.user`), the `gcloud ai` commands, and all BigQuery ML SQL are **unchanged** — including the option value `MODEL_REGISTRY = 'VERTEX_AI'`. |
| **The `AI.*` scalar functions are GA.** | Prefer `AI.GENERATE` over `ML.GENERATE_TEXT` for new work. It needs no remote model, accepts `output_schema`, and returns cleaner columns. |
| **BigQuery accepts every Gemini model by short name.** | Google's reference states: *"All of the generally available and preview Gemini models are supported."* The full endpoint URL is optional, not required. Use the **global** endpoint form to cut 429 errors or to reach a model your region lacks; it works only with `AI.GENERATE_TEXT`. The labs pin `gemini-2.5-flash` for reproducible output — it **retires 20 October 2026**. |
| **The generative modules of `google-cloud-aiplatform` were removed 24 Jun 2026** (replaced by `google-genai`). | This does **not** affect `aiplatform.PipelineJob` or Vertex AI Pipelines — a distinction the headlines blur. See the [Kubeflow module](../modules/KUBEFLOW-PIPELINES-ON-GCP.md). |
| **Feature Store optimized online serving is deprecated** (sunset 17 Feb 2027). | Bigtable online serving only for new work. |
| **Feature Store optimized online serving is deprecated.** No new features since 17 May 2026; APIs sunset 17 Feb 2027. | Only **Bigtable online serving** is supported for new work. Lab 3 covers this as awareness only — don't build anything new on optimized serving. |
| **Online prediction is not supported for AutoML classifier/regressor models.** | If you take Lab 2's optional AutoML path, that model is batch-only. Pick the model type with the serving pattern in mind. |

---

## What's in this repository

```
Portfolio/
├── SCALING-PROTOTYPES-TO-ML.md / .html        concept module
├── KUBEFLOW-PIPELINES-ON-GCP.md / .html       concept module
├── VERTEX-ML-METADATA.md / .html              concept module
├── VERTEX-MODEL-MONITORING.md / .html         concept module
├── VERTEX-AUTOSCALING.md / .html              concept module
├── GCP-NETWORKING-FOR-ML-SERVING.md / .html   concept module
├── VERTEX-TRAINING-COMPUTE.md / .html         concept module
├── LOW-CODE-AI-ON-GCP.md / .html              concept module
├── GCP-API-VERSIONS-AND-LAUNCH-STAGES.md      concept module
├── EVENT-DRIVEN-ML-AUTOMATION.md / .html      concept module
├── VERTEX-FAIRNESS-AND-BIAS.md / .html        concept module
├── SERVING-MODELS-ON-CLOUD-RUN.md / .html     concept module
├── GIT-FOR-ML-ON-GCP.md / .html               concept module
├── assets/{scaling,kfp,mlmd,monitoring,
│         autoscaling,networking,training,
│         lowcode,apiversions,eventdriven,
│         fairness,cloudrun,git}/             38 SVG diagrams + generators
└── gcp-labs/
    ├── README.md                              this page
    ├── lab-01 … lab-06 .md                    the six labs
    ├── figures/                               33 SVG console mockups
    │   ├── _gen_common.py                     drawing primitives
    │   ├── _generate.py / _gen_lab3..6.py     figure generators
    │   └── _check.py                          validates them (XML + overflow)
    ├── sql/lab01 … lab05/                     every SQL block, extracted
    ├── site/                                  index + 6 self-contained lab pages
    └── build.py                               regenerates figures, SQL and HTML
```

### Reading the labs

- **Markdown** — read the `.md` files directly. Everything renders in GitHub, VS Code, or any Markdown viewer.
- **HTML** — open `site/lab-01.html` or `site/lab-02.html` in a browser. These are fully self-contained: the SVG figures are inlined, there are no external requests, and they follow your system light/dark theme.

### Rebuilding

```bash
python -m pip install markdown pygments
python build.py
```

This regenerates the figures, validates them, re-extracts the SQL files, and rebuilds the HTML.

---

## A note on the figures

The console screenshots in these labs are **hand-built SVG mockups**, not captures of a live console. They are drawn to match the August 2026 console layout and are labelled with representative values.

Numbers shown in result grids are consistent with the real datasets — row counts, the 26.5% churn rate, the ~1,409-row evaluation split, the 22,641 reviews with text — but figures marked *sample output* will differ from your run by small amounts. Gemini is not deterministic even at `temperature: 0`, and BigQuery ML's `AUTO_SPLIT` picks a different random hold-out each time you train.

---

## What order to do them in

The numbering reflects when each lab was written, **not** the order to work through them. There is one recommended path and two shortcuts.

### The recommended path

Three tracks. Do **Track 1 first** — it is the spine, and the only track with prerequisites.

**Track 1 — the tabular spine** (~5 hours)

| Order | Lab | Why here |
|---|---|---|
| 1 | **[Lab 6 — Exploration](lab-06-data-exploration-bigquery-colab.md)** | Free, 45 min, no prerequisites. Teaches BigQuery's cost model, which every later lab depends on. |
| 2 | **[Lab 2 — Churn with BigQuery ML](lab-02-customer-churn-lowcode-bqml.md)** | The core. Baseline → train → evaluate → explain → decide. |
| 3 | **[Lab 5 — Feature engineering](lab-05-feature-engineering-tabular.md)** | Explicitly "the part Lab 2 skipped". Reuses Lab 2's tables. |
| 4 | **[Lab 3 — Serving](lab-03-serving-ml-models-lowcode.md)** | Closes the lifecycle. **Needs Lab 2's models** (or its 3-minute catch-up script). |

> Features-before-training is the real-world order, but Lab 2 → Lab 5 is the better *learning* order: train a working baseline first, then improve its inputs and measure what that bought.

**Track 2 — unstructured data** (~2.5 hours, independent of Track 1)

| Order | Lab | Why here |
|---|---|---|
| 1 | **[Lab 1 — Sentiment with Gemini](lab-01-sentiment-analysis-bigquery-gemini.md)** | Introduces `AI.GENERATE` and `output_schema` on text. |
| 2 | **[Lab 4 — Vision](lab-04-image-vision-lowcode-bigquery.md)** | The same pattern on images, plus object tables. Cheaper and shorter — swap the order if you want the quick win first. |

**Track 3 — the modules** (reading only, no console)

| When | Module |
|---|---|
| Before anything, or after Lab 3 | **[Scaling prototypes into ML models](../modules/SCALING-PROTOTYPES-TO-ML.md)** — the map |
| After Lab 3 | **[Model Monitoring](../modules/VERTEX-MODEL-MONITORING.md)** — Lab 3 Task 9 sets it up; this explains it |
| After Lab 3 | **[Kubeflow Pipelines](../modules/KUBEFLOW-PIPELINES-ON-GCP.md)** — only makes sense once you have steps worth orchestrating |
| After KFP | **[Vertex ML Metadata](../modules/VERTEX-ML-METADATA.md)** — it is what pipelines populate |

### Shortcut A — "I have one evening"

**Lab 1** on its own. A scored table inside 20 minutes, and it stands alone.

### Shortcut B — "I already know ML, I just need the GCP surface"

Skip Lab 6. Go **Lab 2 → Lab 3 → Lab 5**, then read all four modules. Lab 2's explanations of precision/recall and class imbalance will be familiar. The new parts are `TRANSFORM`, the registry, and how little infrastructure any of it needs.

### If you just want one answer

| Question | Answer |
|---|---|
| The fastest visible result | **Lab 1** — a scored table inside 20 minutes |
| ML fundamentals done properly | **Lab 2** — the most rigorous of the three |
| The architectural map before any building | **[Scaling prototypes into ML models](../modules/SCALING-PROTOTYPES-TO-ML.md)** |
| To understand deployment | **Lab 2 → Lab 3** (Lab 3 needs Lab 2's models, or its catch-up script) |

Done in order (the Scaling module, then Labs 1 → 2 → 3), they walk the whole path from "it works in a notebook" to "it runs in production and someone knows when it breaks."

### Where the tracks join up

Track 1 and Track 2 meet at the end: customers who are both **high churn risk** and **writing negative reviews** are the highest-priority contacts in the business. Both scores live in the same warehouse, so that is a join, not an integration project.
