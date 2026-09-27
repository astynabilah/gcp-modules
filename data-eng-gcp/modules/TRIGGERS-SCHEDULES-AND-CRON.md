# Triggers, schedules and cron

**Everything that makes ML work start by itself** — clocks, events, and the five-field expression you will write more often than any other config on Google Cloud.

> **Module, not a lab.** [Kubeflow Pipelines](../../mlops-gcp/modules/KUBEFLOW-PIPELINES-ON-GCP.md), [Cloud Composer and DAGs](CLOUD-COMPOSER-AND-DAGS.md) and [Event-driven ML automation](../../mlops-gcp/modules/EVENT-DRIVEN-ML-AUTOMATION.md) each cover one orchestrator. This one is about the **triggering layer underneath all of them** — the part that's the same everywhere.

---

## 1. Two kinds of trigger, and one question

Everything that starts work automatically is either:

| | **Time-based** | **Event-based** |
|---|---|---|
| Fires when | the clock says so | something happened |
| Expressed as | a **cron expression** | an **event filter** |
| Runs | whether or not there's work | only when there is |
| Fails how | runs on empty, or misses a late arrival | fires twice, or fires on the wrong thing |

**One question decides it: does your work depend on data arriving, or on a deadline?**

*"Retrain every Sunday night"* is a deadline. The business wants a fresh model by Monday whether or not much changed. *"Retrain when new validated data lands"* is an arrival, because the work is meaningless until the data exists. Choose the wrong one and you get either a job that scores yesterday's data because today's was late, or a job that never runs because nobody uploaded anything this week.

> **Plenty of real systems use both**: an event trigger for responsiveness, plus a scheduled fallback so a silent upstream doesn't mean a silently stale model.

---

## 2. Reading a cron expression

Five fields, separated by spaces, always in this order:

```
┌───────────── minute        (0 - 59)
│ ┌─────────── hour          (0 - 23)
│ │ ┌───────── day of month  (1 - 31)
│ │ │ ┌─────── month         (1 - 12)
│ │ │ │ ┌───── day of week   (0 - 6, Sunday = 0)
│ │ │ │ │
0 2 * * *
```

**`*` means "every".** So `0 2 * * *` reads: **minute 0, hour 2, every day of month, every month, every day of week** — i.e. **02:00 every day**.

**Read it right to left when you're checking one**, because the coarse fields tell you how often it repeats and the fine fields tell you when within that.

### The characters

| Symbol | Means | Example |
|---|---|---|
| `*` | every value | `* * * * *` = every minute |
| `5` | exactly this value | `0 5 * * *` = 05:00 daily |
| `,` | a list | `0 8,20 * * *` = 08:00 and 20:00 |
| `-` | a range | `0 9-17 * * *` = hourly from 09:00 to 17:00 |
| `/` | a step | `*/15 * * * *` = every 15 minutes |
| `L` | last (where supported) | `0 3 L * *` = 03:00 on the last day of the month |

### Ones you'll write

| Expression | Means |
|---|---|
| `0 * * * *` | every hour, on the hour |
| `*/15 * * * *` | every 15 minutes |
| `0 2 * * *` | 02:00 daily |
| `0 2 * * 1` | 02:00 every **Monday** |
| `0 2 * * 0` | 02:00 every **Sunday** |
| `0 6 * * 1-5` | 06:00 on weekdays |
| `0 2 1 * *` | 02:00 on the **1st of the month** |
| `0 2 1 1 *` | 02:00 on **1 January** |
| `30 3 * * 6` | 03:30 every Saturday |
| `0 0 * * *` | midnight daily |

### Writing one from a requirement

Work through the fields in order and ask "does this need to be pinned?"

> *"Retrain weekly, early Monday morning, 3am."*
>
> - **minute** — 0, on the hour → `0`
> - **hour** — 3am → `3`
> - **day of month** — not pinned, it's weekly → `*`
> - **month** — every month → `*`
> - **day of week** — Monday → `1`
>
> **`0 3 * * 1`**

### Four things that catch people

**Day-of-week is 0–6 with Sunday = 0.** Monday is 1. Some systems also accept 7 for Sunday and three-letter names (`MON`, `SUN`); don't rely on either without checking.

**Day-of-month and day-of-week are OR, not AND.** `0 2 15 * 1` fires on the 15th **and** every Monday — not "the 15th if it's a Monday". If both are set to something other than `*`, you get the union. This is easy to miss.

**There is no "seconds" field** in the standard five-field form. If you need sub-minute frequency, cron is the wrong tool.

**`*/7` doesn't mean "every 7 days".** Steps restart at the beginning of each field's range, so `0 0 */7 * *` fires on the 1st, 8th, 15th, 22nd, 29th — then again on the 1st, two days later. For true weekly, pin the day of week.

### The field that isn't in the expression: timezone

**A cron expression carries no timezone.** Every service that accepts one takes the timezone separately, and the default is almost always **UTC**.

```python
job.create_schedule(cron="0 3 * * *", timezone="Asia/Jakarta")
```

Leave it out and your "3am retrain" runs at 10am local in Jakarta, or 11am in daylight saving. And **daylight saving is why you should avoid scheduling between 00:00 and 03:00 local** in regions that observe it. That window can occur twice, or not at all, on transition days.

---

## 3. Where you'll type a cron expression

The same five fields, several services:

| Service | Field | Notes |
|---|---|---|
| **Vertex AI Pipelines** | `create_schedule(cron=...)` | Native scheduler. Takes `timezone`, `max_concurrent_run_count`, `max_run_count`. |
| **BigQuery scheduled queries** | schedule | Also accepts plain English — "every 24 hours" |
| **Cloud Scheduler** | `--schedule` | The general-purpose one: hits HTTP, Pub/Sub or App Engine targets |
| **Cloud Composer / Airflow** | `schedule=` on the DAG | Also accepts presets (`@daily`) and `timedelta` |
| **Dataproc workflow templates** | via Cloud Scheduler | No native cron |
| **Cloud Run jobs** | via Cloud Scheduler | |

> **Prefer the native scheduler when the service has one.** A Vertex AI Pipeline scheduled with `create_schedule()` gets concurrency control and a run cap for free; the same pipeline poked by Cloud Scheduler over HTTP means you build both yourself. Cloud Scheduler earns its place when the target has no scheduler of its own.

---

## 4. Event triggers: Eventarc and friends

When the trigger is an arrival rather than a clock, the pieces are:

```
something happens  →  an event is published  →  a filter matches  →  your code runs
```

**Eventarc** is the routing layer. You declare a **trigger**: which event type, from which source, delivered to which target (Cloud Run service, Cloud Run function, Workflows, GKE).

### Cloud Storage events — the ones ML uses

| Event type | Fires when |
|---|---|
| **`google.cloud.storage.object.v1.finalized`** | **A new object is created, or an existing one is overwritten** |
| `google.cloud.storage.object.v1.deleted` | An object is deleted |
| `google.cloud.storage.object.v1.archived` | With Object Versioning on, a live version becomes noncurrent |
| `google.cloud.storage.object.v1.metadataUpdated` | An existing object's metadata changes |

**`finalized` is the one that means "a new file landed."** The name is unhelpful. It refers to the write being finalised, not to anything being archived or completed in a business sense. The other three are all easy to reach for and all wrong for "new training data arrived":

- **`archived`** is about **Object Versioning**, not about files being tidied away. It fires when a *live* version becomes *noncurrent* — usually because something overwrote or deleted it. It cannot fire at all in a bucket without versioning.
- **`deleted`** is the opposite of what you want.
- **`metadataUpdated`** fires on label and header changes to objects that already exist.

```bash
gcloud eventarc triggers create retrain-on-new-data \
  --destination-run-service=retrain-trigger \
  --destination-run-region=us-central1 \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=my-training-data" \
  --service-account=eventarc-invoker@PROJECT.iam.gserviceaccount.com
```

The receiving function then submits the work. It does not *do* the work:

```python
import functions_framework
from google.cloud import aiplatform

@functions_framework.cloud_event
def on_new_data(cloud_event):
    name = cloud_event.data["name"]
    if not name.startswith("validated/") or not name.endswith(".parquet"):
        return                                   # filter in code as well

    aiplatform.PipelineJob(
        display_name=f"retrain-{name}",
        template_path="gs://my-bucket/pipelines/retrain.yaml",
        parameter_values={"data_uri": f"gs://{cloud_event.data['bucket']}/{name}"},
    ).submit()
```

> **A function is a doorbell, not a kitchen.** It should validate the event and submit a job. Training inside the function hits its timeout, its memory limit, and its lack of a GPU — see [Event-driven ML automation](../../mlops-gcp/modules/EVENT-DRIVEN-ML-AUTOMATION.md).

### The property that shapes everything: at-least-once delivery

**Event delivery is at-least-once, so your handler will eventually run twice for the same event.** This will happen, not might. Retries after a timeout, duplicate publishes, redeliveries.

That makes **idempotency a requirement, not a nicety**. The usual patterns:

- **Derive a deterministic job name from the event**, such as `retrain-{object_name}-{generation}`, so a duplicate submission collides instead of creating a second run.
- **Write to a partition keyed by the input**, so a repeat overwrites rather than appends.
- **Check before acting** — has a run for this object already succeeded?

A retraining pipeline that isn't idempotent doesn't fail loudly on a duplicate. It runs twice, costs twice, and leaves you two models where you expected one.

### Fifty files at once

A bulk upload produces one event per object. Fifty files means **fifty triggers**, which means fifty pipeline runs unless you do something about it.

| Approach | How |
|---|---|
| **Sentinel file** | Ignore the data files; trigger only on `_SUCCESS` or `MANIFEST.json` written last |
| **Debounce** | The function records arrivals and starts work only after a quiet period |
| **Batch on a schedule** | Events accumulate; a cron job processes what arrived — the hybrid from §1 |

The sentinel is the simplest option and holds up best in practice: the uploader decides when a batch is complete, which is knowledge the trigger doesn't have.

---

## 5. Picking a trigger mechanism

| You need | Use |
|---|---|
| A pipeline on a clock | **`create_schedule()`** on the `PipelineJob` |
| SQL on a clock | **BigQuery scheduled query** |
| Anything else on a clock | **Cloud Scheduler** → HTTP, Pub/Sub, or a Cloud Run job |
| React to a file landing | **Eventarc** on `storage.object.v1.finalized` |
| React to a message | **Pub/Sub** → Cloud Run or a function |
| React to an audit-logged action | **Eventarc** with a Cloud Audit Logs filter |
| A DAG across many systems | **Cloud Composer** |
| One DAG to follow another | **`TriggerDagRunOperator`** |
| A build on a commit | **Cloud Build trigger** |

> **Reach for the lightest thing that fits.** A scheduled query costs nothing to operate. Cloud Scheduler is a few cents a month. Eventarc plus a function is small. Cloud Composer runs continuously and costs hundreds. The gap between the first and last of those is far larger than the difference in capability for most ML work.

---

## 6. Anti-patterns

**Assuming a cron expression is in your timezone.** It's UTC unless you said otherwise.

**Scheduling in the 00:00–03:00 local window** where daylight saving applies. That hour can happen twice, or not at all.

**Using `*/7` for "weekly".** Steps restart each month. Pin the day of week.

**Setting day-of-month *and* day-of-week** and expecting an AND. It's an OR.

**A non-idempotent event handler.** At-least-once delivery means duplicates are certain, not possible.

**Triggering per file on a bulk upload.** Fifty files, fifty pipeline runs. Use a sentinel.

**Doing the work inside the trigger.** The function submits; the pipeline trains.

**Cloud Scheduler in front of a service that already has a scheduler.** You've taken on concurrency control and run counting that came for free.

**Choosing a schedule when the real dependency is data arrival.** You then debug a model trained on yesterday's data because today's landed late.

---

## 7. Test your understanding

<details markdown="1">
<summary><b>1.</b> What does <code>0 2 * * *</code> mean, and how would you change it to weekly on Mondays?</summary>

**02:00 every day** — minute 0, hour 2, every day of month, every month, every day of week.

Weekly on Mondays is **`0 2 * * 1`**: pin the last field to `1` and leave day-of-month as `*`. Sunday is `0`, so Monday is `1`.

And set the timezone separately — the expression itself carries none, and the default is UTC.
</details>

<details markdown="1">
<summary><b>2.</b> Which Cloud Storage event fires when new training data is uploaded?</summary>

**`google.cloud.storage.object.v1.finalized`** — it fires when an object is created **or an existing one is overwritten**.

The name misleads: "finalized" refers to the write completing, not to archiving. `archived` is an Object Versioning event (a live version becoming noncurrent), `deleted` is the opposite of what you want, and `metadataUpdated` fires on changes to objects that already exist.
</details>

<details markdown="1">
<summary><b>3.</b> Your retraining function occasionally runs twice for one upload. Is this a bug?</summary>

**No — it's the documented delivery semantics.** Event delivery is at-least-once, so duplicates are expected rather than exceptional.

The fix is in your handler: derive a deterministic job name from the event so a duplicate collides, write to a partition keyed by the input so a repeat overwrites, or check whether a run for this object already succeeded.
</details>

<details markdown="1">
<summary><b>4.</b> <code>0 2 15 * 1</code> — when does this fire?</summary>

**On the 15th of every month, AND every Monday.** Not "the 15th when it falls on a Monday".

When day-of-month and day-of-week are both set to something other than `*`, cron takes the **union**. If you want a specific weekday, leave day-of-month as `*`.
</details>

<details markdown="1">
<summary><b>5.</b> A nightly retrain, but you also want it to react to data arriving early. Which trigger?</summary>

**Both.** An Eventarc trigger on `finalized` for responsiveness, plus a scheduled run as a fallback so a silent upstream doesn't quietly leave you with a stale model.

That combination needs idempotency to work — otherwise the schedule and the event both fire and you retrain twice.
</details>

---

## Summary

Triggers are either **time-based** or **event-based**, and the deciding question is whether the work depends on a **deadline** or on an **arrival**. A **cron expression** is five fields (minute, hour, day-of-month, month, day-of-week), where `*` means every, day-of-week runs 0–6 with **Sunday = 0**, and the two "day" fields combine as an **OR**, not an AND. The expression carries **no timezone**; every service takes it separately and defaults to **UTC**. For events, **Eventarc** routes filtered event types to a target, and the one that means "a new file arrived" is **`google.cloud.storage.object.v1.finalized`**. `archived` is about Object Versioning, not about tidying. Delivery is **at-least-once**, which makes **idempotency a requirement**: derive deterministic job names from the event, or write to input-keyed partitions. A bulk upload produces one event per file, so use a **sentinel file** rather than triggering fifty runs. Prefer a service's **native scheduler** over Cloud Scheduler in front of it. The native one usually brings concurrency control and run caps you would otherwise build.

---

## References

- [Cloud Scheduler cron syntax](https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules)
- [Cloud Storage triggers](https://cloud.google.com/functions/docs/calling/storage) · [Eventarc](https://cloud.google.com/eventarc/docs/overview)
- [Schedule a pipeline run](https://cloud.google.com/vertex-ai/docs/pipelines/schedule-pipeline-run)
- Related: [Event-driven ML automation](../../mlops-gcp/modules/EVENT-DRIVEN-ML-AUTOMATION.md) · [Cloud Composer and DAGs](CLOUD-COMPOSER-AND-DAGS.md) · [Kubeflow Pipelines](../../mlops-gcp/modules/KUBEFLOW-PIPELINES-ON-GCP.md) · [CI/CD for ML](../../mlops-gcp/modules/CI-CD-FOR-ML-ON-GCP.md)
