# The modules

**Theory, not tutorials.** Concepts, decision frameworks and reference material — nothing to run. The hands-on counterparts are in [`../labs/`](../labs/README.md), and the big picture connecting both is in [ROADMAP.md](../ROADMAP.md).

Each module is self-contained: read the one you need. Most carry an **API version note** explaining what `v1` vs `v1beta1` means for *that* topic specifically.

---

## Start here if you know what you need but not what to type

### [Choosing specs: what do I use for this?](CHOOSING-COMPUTE-SPECS.md)
A **lookup reference**, not an explanation. Fifteen worked cases end to end (churn on 200k rows, a 7B pretrain, ten services sharing a T4, notebooks with no internet), each with the machine type, the accelerator, the scheduling strategy and the serving shape, linked back to the module that justifies it. Opens with the three questions that eliminate most of the option space, and closes with cost checks that catch the usual mistakes.

---

## Strategy — what to build, and how far

### [Scaling prototypes into ML models](SCALING-PROTOTYPES-TO-ML.md)
The five stages between "it works in a notebook" and "it runs in production", which GCP service belongs at each, three reference architectures, a cost table, and a readiness checklist. **Read this first if you want the map before the detail.**

### [Low-code AI solutions on Google Cloud](LOW-CODE-AI-ON-GCP.md)
The four tiers ordered by *who supplies what* (pretrained APIs, generative, AutoML, BigQuery ML), plus the full catalogue of **23 BigQuery ML model types**, how "milli node hours" work, class imbalance levers, and AutoML's irreversible **Cloud/Edge fork**.

---

## Google's own AI APIs

### [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md)
The map of Google's **pretrained APIs** — models you rent per call, with no training data of your own. Answers what they are, why they still exist next to Gemini, when to pick one, and how the call pattern works. Carries the **rename map**, including the search product that was renamed five times between 2023 and 2026 while its API endpoints never changed. Ends with what is already switched off, what dies in September 2026, and the three products that vanished with no announcement at all.

### [Vision and video APIs](AI-API-VISION-AND-VIDEO.md)
Cloud Vision, Vision API Product Search and Video Intelligence — what each detects, inline bytes versus Cloud Storage, and the free tiers. Also **Agent Platform Vision** (formerly Vertex AI Vision), which is **deprecated as of 15 June 2026 and reaches end of life on 30 September 2026**, and Visual Inspection AI, which disappeared with no announcement at all.

### [Document AI and text APIs](AI-API-DOCUMENT-AND-TEXT.md)
The processor gallery after the **30 June 2026 cull** that removed the tax, procurement and lending parsers (only W-2 survived), **Layout Parser** and why its chunking suits RAG, what training a custom extractor costs, and the **Natural Language API**, frozen since August 2023 with v2 in three years of unannounced limbo.

### [Speech and translation APIs](AI-API-SPEECH-AND-TRANSLATION.md)
Speech-to-Text v1 versus v2 (**v1 keeps the free tier, v2 has none**), the Chirp lineage up to `chirp_3`, and the two features Chirp 3 cannot do at all: word-level timestamps and confidence. Text-to-Speech voice tiers, where Google now labels WaveNet, Studio, Neural2 and Standard **"Legacy"** without deprecating any of them. Translation Basic versus Advanced, and the Gemini-derived **Translation LLM**. Ends with the structural point: these APIs are not being absorbed into Gemini — Gemini models are being delivered *through* them.

### [Search, conversation and agents](AI-API-SEARCH-AND-CONVERSATION.md)
The messiest naming in Google Cloud, made readable. The enterprise search product took **six names in three years** (Generative AI App Builder to Agent Search) while its API endpoints never moved once. Also the commerce chain that absorbed **Recommendations AI** and **Retail Search**, why **Dialogflow CX and ES are supported rather than deprecated**, why CX Agent Studio is a successor and not a rename, and a layer map showing that **ADK, Agent Runtime and Agent Search are layers, not alternatives** — write, run, retrieve.

---

## Forecasting

### [Time series forecasting](TIME-SERIES-FORECASTING.md)
The one part of ML where a **random train/test split is wrong**, because it puts later rows into training and earlier rows into testing. Covers why regression is the wrong tool, `DATA_SPLIT_METHOD = 'SEQ'`, and **`ARIMA_PLUS`**, whose single statement runs a nine-step pipeline. Holiday modelling stays off until you set `HOLIDAY_REGION`. Also **TimesFM via `AI.FORECAST`**, which needs no training and matches ARIMA_PLUS on accuracy but loses on explainability.

---

## Learning without labels

### [Unsupervised learning](UNSUPERVISED-LEARNING-ON-GCP.md)
Everything else here assumes a label column. This one does not. **`KMEANS`** for segmentation (set `KMEANS++`, because the default is `RANDOM`), **`PCA`** for dimensionality reduction, **`MATRIX_FACTORIZATION`** for recommenders (which needs an Enterprise reservation, not on-demand), and **`ML.DETECT_ANOMALIES`**, where `contamination` *sets* the anomaly rate rather than measuring it. Ends with the honest problem: there is no held-out set, so metrics measure geometry, not correctness.

---

## Training — where the compute lives

### [Dataproc for ML data preparation](../../data-eng-gcp/modules/DATAPROC-AND-SPARK.md)
Managed Spark for the ETL that *feeds* training, plus the production question that comes up most: consistent, fast-starting clusters with your own Python libraries. The answer is a **custom image**, because `pip.packages` installs at boot and Google explicitly warns against referencing **public initialization actions**. Plus pinning `major.minor`, the 365-day image expiry, and why serverless starts in 50 seconds rather than 120.

### [Where model training runs](VERTEX-TRAINING-COMPUTE.md)
Five places training can happen, the Workbench **G2 ↔ non-G2** resize restriction, why the **notebook executor** beats resizing your instance, the four worker pools of a custom training job, and Reduction Server.

---

## Orchestration — how work gets started

### [GPUs and TPUs, from zero](GPUS-AND-TPUS-FOR-ML.md)
The hardware, for someone who has trained models without thinking about silicon. How to read `n1-standard-4` and `a2-highgpu-8g`, why **memory** is the binding spec, and the TPU rules that cost money when unknown: `tpuTopology` replaced `acceleratorType` at v4, **`replicaCount` must be 1** even for a 16-chip `4x4` slice, and the **MXU is a 128×128 array**. So tensor dimensions that aren't multiples of 128 are padded and billed anyway.

### [Kubeflow Pipelines on Google Cloud](KUBEFLOW-PIPELINES-ON-GCP.md)
The only non-low-code module, deliberately. Terminology (you never install Kubeflow), what happens when you run a pipeline, parameters vs artifacts, control flow, per-step machine resources, caching, **portability across Vertex AI and on-prem Kubeflow**, and a clear decision map for when a scheduled query would have done.

### [Triggers, schedules and cron](../../data-eng-gcp/modules/TRIGGERS-SCHEDULES-AND-CRON.md)
The layer underneath every orchestrator: what makes work start by itself. Teaches **cron expressions properly** — five fields, `*` means every, Sunday is `0`, the two day fields combine as an **OR**, and the expression carries **no timezone**. Then Eventarc: which Cloud Storage event really means "a new file arrived" (`finalized`, and why `archived` doesn't), why **at-least-once delivery makes idempotency a requirement**, and what to do when a bulk upload fires fifty triggers.

### [Event-driven ML automation](EVENT-DRIVEN-ML-AUTOMATION.md)
Cloud Functions gives **at-least-once** execution, so a timed-out API call plus a retry produces duplicate training jobs. The idempotent handler keyed on the **CloudEvent id**, why check-and-write needs a **transaction**, and the 7-day retry trap.

### [Cloud Composer, Airflow and DAGs](../../data-eng-gcp/modules/CLOUD-COMPOSER-AND-DAGS.md)
Starts from what a **DAG** is — directed, acyclic, and why forbidding cycles is what makes a graph runnable. Then Airflow's vocabulary, why `execution_date` names the data interval rather than the clock, and the cross-DAG question: **`TriggerDagRunOperator`** (push, no polling, couples only on `dag_id`) versus **`ExternalTaskSensor`** (pull, aligned dates, hard-codes another team's task id), with `SubDagOperator` deprecated and `TaskGroup` being visual grouping only.

### [CI/CD for ML on Google Cloud](CI-CD-FOR-ML-ON-GCP.md)
How a commit becomes a container becomes a running pipeline. ML has **two pipelines, not one**: a fast code pipeline and a slow gated model pipeline. Conflating them means a broken test blocks a retrain. Plus the least-privilege pattern: **per-trigger service accounts and repository-scoped Artifact Registry bindings**, and why VPC Service Controls and folder-per-team don't isolate.

---

## Serving — getting predictions to consumers

### [Serving models on Cloud Run](SERVING-MODELS-ON-CLOUD-RUN.md)
The container side that Vertex endpoints hide. Cold start as a six-stage sequence, and the stage you control: **where the model weights live**. Why lazy-loading on first request is not an optimisation.

### [Serving LLMs on GKE](SERVING-LLMS-ON-GKE.md)
The branch where you own the cluster. Covers keeping non-GPU pods off GPU nodes (a **taint** plus GKE's automatic toleration injection, not per-workload affinity). It is built around one finding: **CPU utilisation is the wrong autoscaling signal for GPU inference**, because the work is on the GPU and servers like vLLM and TGI pre-allocate its memory. The signal that works is **queue size**. The reason is continuous batching, which keeps the queue near zero until batch space runs out and then fills it fast.

### [Vertex AI Prediction autoscaling](VERTEX-AUTOSCALING.md)
From zero. Built around one asymmetric rule: with a GPU attached, scale **up when either** CPU or GPU duty cycle exceeds 60%, **down only when both** are below. This explains two opposite complaints. Plus why `minReplicaCount` matters more than any target tuning.

### [Vertex AI batch prediction](VERTEX-BATCH-PREDICTION.md)
Scoring work **nobody is waiting for** — no endpoint, no bill between runs. The rule to watch is **colocation**: input data, model and output must share a region or multi-region, `us-central1` and `us-west1` are two different places, and there is no cross-region setting to enable. Plus why `max_replica_count` is ignored for custom-trained batch jobs.

### [Tuning Gemini on Vertex AI](GEMINI-TUNING-ON-VERTEX.md)
Supervised fine-tuning: when it beats prompting and RAG (**missing behaviour, not missing facts**), what parameter-efficient adapters really change, and a constraint that breaks designs late: a **tuned Gemini model can only be deployed to a shared public endpoint**, so "restrict it to the corporate network" is answered with VPC Service Controls and an IP access level, never a private endpoint.

### [Networking for ML serving](GCP-NETWORKING-FOR-ML-SERVING.md)
Assumes **no networking knowledge at all** — starts from what an IP address is. Anycast, the five chained objects that make up a load balancer, NEGs, and why **serverless backends support no health checks**.

---

## Operating — knowing it still works

### [Vertex AI Model Monitoring](VERTEX-MODEL-MONITORING.md)
Why numerical features use **Jensen-Shannon divergence** and categorical features use **L-infinity distance**, skew vs drift as the same maths with a different baseline, and why none of it measures accuracy.

### [Data validation in BigQuery ML](BIGQUERY-DATA-VALIDATION.md)
Skew and drift detection **in SQL**, with no endpoint and no prediction logging — plus the two other data-quality tools that get confused with it: **Knowledge Catalog scans** (scheduled, scored, `regexExpectation` and `rowConditionExpectation` rules) and **Dataform assertions** (in-pipeline gates). Five GA functions, and the same **Jensen-Shannon / L-infinity** split as Vertex AI Model Monitoring, reaching the same console. Covers which function needs the model versus two tables, why old models can't do skew detection at all, and the syntax trap: `ML.TFDV_VALIDATE` takes **positional arguments, not a `STRUCT`**.

### [Vertex ML Metadata](VERTEX-ML-METADATA.md)
Lineage and artifacts, and why numeric metadata is queried as `metadata.<field>.number_value` — traced through the JSON you write, the `google.protobuf.Struct` it becomes, and the filter grammar that follows. **There is no `int_value`.**

### [Explainability and feature attribution](EXPLAINABILITY-AND-ATTRIBUTION.md)
What a **Shapley value** really is: a feature's average marginal contribution across every subset of the others, and the *unique* fair division satisfying four properties. Then its relatives, split by scope: LIME and counterfactuals are local, permutation importance and partial dependence are global. The method is chosen by the **model**: sampled Shapley for non-differentiable ensembles, integrated gradients where gradients exist, XRAI for images only. Written to survive the product: Vertex Explainable AI sunsets in March 2027, the techniques don't.

### [Fairness and bias detection](VERTEX-FAIRNESS-AND-BIAS.md)
`DetectDataBiasOp` before training, `DetectModelBiasOp` after prediction, both configured with a `BiasConfig`. Why **feature attribution is not a bias check** — a model discriminates through proxies with the protected attribute's attribution near zero.

---

## Practice — the things around the model

### [Private networking for ML](GCP-PRIVATE-NETWORKING-FOR-ML.md)
The other half of networking: **traffic going out, and how to stop it.** Private Google Access for reaching Google APIs with no external IP, Cloud NAT + Cloud Router for controlled outbound, and **VPC Service Controls** for what neither can do: stopping data leaving when the credentials are valid. Plus the four Vertex endpoint types and which model types can use them.

### [BigQuery connections and federated data](../../data-eng-gcp/modules/BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md)
How BigQuery reaches what isn't in BigQuery — Cloud SQL, Spanner, Cloud Storage, Gemini. Access is always **two grants to two identities**: `bigquery.connectionUser` to the person *on the connection*, and the target-service role to the connection's **auto-created service account**. Plus why `EXTERNAL_QUERY`'s inner string is the source database's dialect, and why federated queries are wrong for building training data.

### [Git and version control for ML work](GIT-FOR-ML-ON-GCP.md)
The mechanics behind Stage 1 of the scaling ladder. Workbench → GitHub happens **entirely inside the instance**; there is no console OAuth. Plus why `.ipynb` files diff terribly and how `nbstripout` / `jupytext` / `nbdime` fix it.

### [`v1` vs `v1beta1` — API versions and launch stages](GCP-API-VERSIONS-AND-LAUNCH-STAGES.md)
Untangles the **four different things called "version"**, what each launch stage promises, and a section on what the split means in every other module — scale-to-zero being `v1beta1`-only, Model Monitoring v2 living on `v1beta1`, ML Metadata needing none of it.

---

## Figures

Each module's diagrams live in [`assets/<topic>/`](assets/) alongside the generator that draws them and a validator that checks them. Rebuild everything with `python build.py` from the repository root.
