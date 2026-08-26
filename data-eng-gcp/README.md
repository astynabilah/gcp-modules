# Data engineering on Google Cloud

The platform layer underneath the machine learning — **the parts that would still matter if you never trained a model.** Spark clusters, cross-database queries, workflow orchestration, and the triggering mechanisms that make anything run by itself.

Its sibling, [`mlops-gcp/`](../mlops-gcp/README.md), covers everything ML-specific. The split is one question:

> **Would this document exist if you did no ML at all?**

The test is not whether the underlying technology is general (nearly all of it is). The test is whether the document is *written from* the ML angle. Networking for model serving is written from the ML angle and lives there. Airflow is not, and lives here.

---

## The modules

Full descriptions in [`modules/README.md`](modules/README.md).

**Foundations** · [BigQuery fundamentals](modules/BIGQUERY-FUNDAMENTALS.md) · [IAM and service accounts](modules/IAM-AND-SERVICE-ACCOUNTS.md)

**Processing** · [Dataproc and Spark](modules/DATAPROC-AND-SPARK.md)

**Data access** · [BigQuery connections and federated data](modules/BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md)

**Governance** · [Sensitive Data Protection](modules/SENSITIVE-DATA-PROTECTION.md)

**Orchestration** · [Cloud Composer, Airflow and DAGs](modules/CLOUD-COMPOSER-AND-DAGS.md) · [Triggers, schedules and cron](modules/TRIGGERS-SCHEDULES-AND-CRON.md)

---

## Where this meets the ML path

These modules deliberately keep the ML usage of each mechanism **in one place** rather than duplicating it into a stub on the other side. Where a mechanism has an ML-facing application, the section stays with the explanation of how the mechanism works, and the ML path links in:

| Fundamental | Its ML face |
|---|---|
| BigQuery **connections** — the auto-created service account, the two-hop IAM | The same `CLOUD_RESOURCE` connection is what `AI.GENERATE`, `AI.EMBED` and `ML.ANNOTATE_IMAGE` call through — [§5](modules/BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md#5-the-same-mechanism-for-ai) |
| **Cloud Composer** — Airflow, DAGs, pools | When to use it *instead of* Vertex AI Pipelines, and why one ML pipeline doesn't justify it — [§6](modules/CLOUD-COMPOSER-AND-DAGS.md#6-composer-vs-vertex-ai-pipelines) |
| **Triggers and cron** — the five fields, Eventarc, at-least-once | Retraining on new data, and why the handler must be idempotent — [Event-driven ML automation](../mlops-gcp/modules/EVENT-DRIVEN-ML-AUTOMATION.md) |
| **Dataproc** — clusters, custom images, serverless | Spark is for the ETL that *feeds* training, never for training itself — [Where training runs](../mlops-gcp/modules/VERTEX-TRAINING-COMPUTE.md) |

---

## No labs yet

This path is modules only for now. When labs arrive they follow the same shape as the [MLOps labs](../mlops-gcp/labs/README.md): a `labs/` folder with `figures/` and `sql/`, discovered automatically by the build.

---

## Reading it

- **Markdown** — read the `.md` files directly; everything renders on GitHub.
- **HTML** — `python tools/build.py`, then open `site/index.html`. Self-contained pages with the figures inlined.

The figures are **hand-drawn SVG mockups of the Google Cloud console, not screenshots.** They show the fields and controls you'll meet; expect the real console to have moved things.
