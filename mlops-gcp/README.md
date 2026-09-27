# MLOps on Google Cloud

Self-paced labs and reference modules covering the path from raw data to a model running in production on Google Cloud. Mostly in SQL and the console, with the platform mechanics (training compute, serving, networking, orchestration, Git) explained alongside.

Written against the Google Cloud console as of **23 August 2026**, including the Vertex AI → Gemini Enterprise Agent Platform rebrand.

> **New here? Start with [ROADMAP.md](ROADMAP.md)** — the big picture, the options at each stage, and which document covers what.

---

## Two kinds of document

|  | **Labs** | **Modules** |
|---|---|---|
| Format | Hands-on, step-by-step, console + SQL | Theory, decision frameworks, reference |
| You get | A working thing in your own project | Understanding of *why* and *which option* |
| Cost | Stated per lab (most are free or cents) | None — nothing to run |

---

## The labs

Full descriptions in [`labs/README.md`](labs/README.md).

| # | Lab | Time | Cost |
|---|---|---|---|
| 1 | [Sentiment analysis with Gemini in BigQuery](labs/lab-01-sentiment-analysis-bigquery-gemini.md) | 75–90 min | ~$2–4 |
| 2 | [Customer churn end-to-end with BigQuery ML](labs/lab-02-customer-churn-lowcode-bqml.md) | 90–110 min | low |
| 3 | [Serving a model: batch, online, and in SQL](labs/lab-03-serving-ml-models-lowcode.md) | 90–110 min | endpoint bills hourly |
| 4 | [Computer vision without training anything](labs/lab-04-image-vision-lowcode-bigquery.md) | 60–75 min | **< $0.10** |
| 5 | [Feature engineering for tabular data](labs/lab-05-feature-engineering-tabular.md) | 90–110 min | low |
| 6 | [Exploring BigQuery data from a notebook](labs/lab-06-data-exploration-bigquery-colab.md) | 45–60 min | **free** |

**Suggested order is not 1→6.** See [the labs README](labs/README.md#recommended-lab-order) — the numbering reflects when each was written.

## The modules

Full descriptions in [`modules/README.md`](modules/README.md).

**Reference** · [Choosing specs: what do I use for this?](modules/CHOOSING-COMPUTE-SPECS.md) — the lookup table for "what machine type / accelerator / serving shape for case X"

**Google's AI APIs** · [What AI APIs are in Google Cloud?](modules/AI-APIS-OVERVIEW.md) — the pretrained-API map, the rename history, and what has been switched off · [Vision and video](modules/AI-API-VISION-AND-VIDEO.md) · [Document AI and text](modules/AI-API-DOCUMENT-AND-TEXT.md) · [Speech and translation](modules/AI-API-SPEECH-AND-TRANSLATION.md) · [Search, conversation and agents](modules/AI-API-SEARCH-AND-CONVERSATION.md)

**Learning without labels** · [Unsupervised learning](modules/UNSUPERVISED-LEARNING-ON-GCP.md)

**Forecasting** · [Time series forecasting](modules/TIME-SERIES-FORECASTING.md)

**Strategy** · [Scaling prototypes into ML models](modules/SCALING-PROTOTYPES-TO-ML.md) · [Low-code AI solutions](modules/LOW-CODE-AI-ON-GCP.md)

**Data** · [Dataproc for ML data prep](../data-eng-gcp/modules/DATAPROC-AND-SPARK.md) · [BigQuery data validation](modules/BIGQUERY-DATA-VALIDATION.md) · [BigQuery connections](../data-eng-gcp/modules/BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md)

**Training** · [Where training runs](modules/VERTEX-TRAINING-COMPUTE.md) · [GPUs and TPUs, from zero](modules/GPUS-AND-TPUS-FOR-ML.md)

**Orchestration** · [Kubeflow Pipelines](modules/KUBEFLOW-PIPELINES-ON-GCP.md) · [Event-driven ML automation](modules/EVENT-DRIVEN-ML-AUTOMATION.md) · [CI/CD for ML](modules/CI-CD-FOR-ML-ON-GCP.md) · [Composer, Airflow and DAGs](../data-eng-gcp/modules/CLOUD-COMPOSER-AND-DAGS.md) · [Triggers, schedules and cron](../data-eng-gcp/modules/TRIGGERS-SCHEDULES-AND-CRON.md)

**Serving** · [Cloud Run](modules/SERVING-MODELS-ON-CLOUD-RUN.md) · [LLMs on GKE](modules/SERVING-LLMS-ON-GKE.md) · [Autoscaling](modules/VERTEX-AUTOSCALING.md) · [Batch prediction](modules/VERTEX-BATCH-PREDICTION.md) · [Networking](modules/GCP-NETWORKING-FOR-ML-SERVING.md) · [Private networking](modules/GCP-PRIVATE-NETWORKING-FOR-ML.md) · [Gemini tuning](modules/GEMINI-TUNING-ON-VERTEX.md)

**Operating** · [Model Monitoring](modules/VERTEX-MODEL-MONITORING.md) · [Explainability and attribution](modules/EXPLAINABILITY-AND-ATTRIBUTION.md) · [ML Metadata](modules/VERTEX-ML-METADATA.md) · [Fairness and bias](modules/VERTEX-FAIRNESS-AND-BIAS.md)

**Practice** · [Git and version control](modules/GIT-FOR-ML-ON-GCP.md) · [`v1` vs `v1beta1`](modules/GCP-API-VERSIONS-AND-LAUNCH-STAGES.md)

---

## Layout

```
gcp-modules/                 ← the repository
├── tools/                   ← every line of build code lives here
│   ├── build.py             ← figures → SQL → HTML, one command
│   ├── svgkit.py            ← SVG primitives for the console mockups
│   ├── check_svg.py         ← validates every generated figure
│   └── figures/             ← one generator per lab / per module
├── site/                    ← generated HTML (gitignored)
└── mlops-gcp/               ← this learning path
    ├── README.md            ← you are here
    ├── ROADMAP.md           ← the big picture
    ├── labs/                hands-on · figures/ · sql/
    └── modules/             theory · assets/
```

A future path on another topic becomes a **sibling folder** (`genai-gcp/`, `data-eng-gcp/`) with the same `README` + `labs/` + `modules/` shape. `tools/` and `site/` stay shared: the build discovers the path folder rather than hard-coding it, so nothing needs editing when one is added or renamed.

**Everything under `mlops-gcp/` is either prose or generated from `tools/`.** No Python lives beside the documents, and the figures, the extracted SQL and the HTML are all reproducible with one command:

```bash
python tools/build.py
```

### Reading it

- **Markdown** — read the `.md` files directly. Everything renders on GitHub, including the mermaid diagrams in [ROADMAP.md](ROADMAP.md).
- **HTML** — run the build, then open `site/index.html`. Self-contained pages with the SVG figures inlined, no external requests, follows your system light/dark theme.

### Building

```bash
python -m pip install markdown pygments
python build.py
```

Regenerates every figure, validates them, re-extracts the SQL from the labs, and rebuilds `site/`.

---

## A note on the figures

The console screenshots are **hand-built SVG mockups**, not captures of a live console — drawn to match the August 2026 layout and generated by the scripts in `labs/figures/` and `modules/assets/*/`. A validator checks each one for XML validity and text overflow.

Numbers in result grids are consistent with the real datasets (row counts, the 26.5% churn rate, the ~1,409-row eval split), but anything marked *sample output* will differ from your run — Gemini is non-deterministic even at `temperature: 0`, and `AUTO_SPLIT` picks a different hold-out each time.

## Verification gaps

The SQL, `gcloud`, and Python in these documents is **checked against Google's documentation but not executed** against a live project. Treat it as carefully-researched reference, not as tested code. Expect to adjust region names, project IDs, and the occasional preview API.
