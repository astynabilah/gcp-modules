# Choosing specs: what do I use for this?

**A lookup reference, not an explanation.** Every other module explains *why*; this one answers *"I have this case — what do I type?"* Each answer links to the module that justifies it.

> **Module, not a lab.** If an answer here surprises you, the linked module is where the reasoning lives.

---

## 0. Three questions decide most of it

Before any table, answer these. They eliminate most of the option space in about ten seconds.

| # | Question | Why it decides so much |
|---|---|---|
| **1** | **Where does the data already live?** | If it's in BigQuery and the model can be BigQuery ML, you may need **no compute spec at all** — no machine type, no region matching, no endpoint. |
| **2** | **Is anything *waiting* for the answer?** | No → batch, which costs nothing between runs. Yes → online, which means a machine is up around the clock. This is the single biggest cost lever in the whole path. |
| **3** | **Is it deep learning?** | No → **no accelerator**. Tabular models, trees, linear models get nothing from a GPU. Yes → then, and only then, the accelerator tables below. |

**A large fraction of real work answers: BigQuery, nothing is waiting, and no.** That combination has no spec. It is a scheduled query. Reach for the tables below only when your case falls outside it.

---

## 0a. How to read a requirement

Most wrong spec answers come from misreading the requirement, not from missing knowledge. They answer a question next to the one that was asked. The method below has four steps, and step 1 does most of the work.

### Step 1 — find the hard constraint

Requirements contain two kinds of phrase, and they are not equal:

| Phrase type | Example | What it does |
|---|---|---|
| **Hard constraint** | "hardware-level isolation" · "must not traverse the internet" · "both HTTP and gRPC" · "cannot be preempted" | **Eliminates options.** Often down to one. |
| **Soft preference** | "cost-effective" · "small models" · "minimal overhead" · "efficient" | **Ranks** whatever survives. |

**Find the hard constraint first and apply it before anything else.** A soft preference can never rescue an option the hard constraint excluded. This is where the reasoning usually goes wrong, because soft preferences are the words that feel most like the point of the request.

> ### A worked example of the failure
>
> *"Multiple small deep learning models, each needing a fraction of a GPU, requiring **hardware-level isolation**, with autoscaling."*
>
> **The tempting path:** "small models" → a small GPU is cost-effective → **L4**. Every step of that is sound reasoning about GPU selection, and it answers the wrong question.
>
> **The hard constraint is "hardware-level isolation".** Only one GPU sharing strategy provides it: **MIG**. And MIG runs only on **A100, H100, H200, B200, GB200, RTX PRO 6000**. **L4 is not on that list**, so the L4 is eliminated before its cost-effectiveness matters.
>
> The requirement was never "which GPU is right for small models". It was "which sharing strategy gives hardware isolation", and the GPU follows from the strategy. Reading "small models" as the deciding phrase inverts the dependency.

**The tell**: "small models" and "fraction of a GPU" are *context*. They explain why you are sharing at all. "Hardware-level isolation" is a *requirement*. Context motivates; requirements decide.

### Step 2 — check capability before quality

Some options are **impossible** rather than worse. Reject those first and you never have to compare them.

| Constraint | Eliminates |
|---|---|
| Hardware isolation on a shared GPU | everything but MIG — and MIG-capable hardware |
| A non-differentiable model | integrated gradients, XRAI |
| A tuned Gemini model | every endpoint type but shared public |
| VPC Service Controls on the endpoint | dedicated **public** endpoints |
| A T4 | MIG |
| Training data no longer exists | skew detection |
| gRPC | shared public and private-services-access endpoints |
| TPU v5e | SparseCores, prebuilt containers |
| A 64-chip v5e topology | `ct5lp-hightpu-8t` and `-1t` |

**"Does this combination even exist?" comes before "which is better?"** A surprising share of plausible answers are configurations the platform refuses.

### Step 3 — say what each rejected option *is* for

If you can't name the case where a rejected option would be correct, you probably have not understood the distinction. You have only memorised an answer.

| Option | Wrong when isolation is required | Right when |
|---|---|---|
| **Time-sharing** | software isolation only | bursty, interactive, prototyping — works on **every** GPU |
| **MPS** | limited isolation, shared bandwidth | cooperative batch throughput, no latency SLO |
| **Whole GPU each** | wastes most of the GPU | the workload really needs a whole one |

Doing this for the options you rejected is also the fastest way to find out you rejected the wrong one.

### Step 4 — sanity-check the shape

Before committing, three questions:

1. **Is anything actually waiting?** If not, you may have specified an endpoint for a batch job.
2. **Does it need an accelerator at all?** If it isn't deep learning, no.
3. **Do the regions line up?** Input, model and output for batch; the endpoint for online.

---

## 0b. Phrases that decide the answer

Requirement wording is more standardised than it looks. These map almost one-to-one onto a spec:

| When you read | Reach for |
|---|---|
| "hardware-level isolation" · "predictable QoS" | **MIG** — and MIG-capable hardware |
| "concurrent kernels, no context switching" | **MPS** |
| "bursty" · "prototyping" · "any GPU model" | **time-sharing** |
| "must not traverse the public internet" | **Private Service Connect** |
| "must not leave our perimeter even with valid credentials" | **VPC Service Controls** |
| "no external IP but must reach Google APIs" | **Private Google Access** |
| "resource isolation from other tenants" · "gRPC" | **dedicated public endpoint** |
| "nobody is waiting" · "weekly scoring" | **batch prediction** or a scheduled query |
| "as soon as resources are available" · "3-day run" | **`FLEX_START`** |
| "interruption-tolerant" · "cheapest" | **Spot** |
| "must start at a known time" | **future reservation, calendar mode** |
| "the training data is no longer available" | **drift**, not skew |
| "embedding tables" · "recommendation model" | **SparseCores** — v5p or v6e |
| "proprietary library not in prebuilt containers" | **custom container** |
| "one team is starving the others" | **Airflow pools** |
| "active-passive" · "only if the primary is unavailable" | **Cloud DNS failover routing** |
| "route users to the nearest region" | **global ALB, Premium Tier, anycast** |
| "minimal operational overhead" | the **managed** option — usually the one you didn't build |

### And the phrases that mean "you are being offered scope creep"

Some options are correct architecture answering a bigger question than the one asked. They're recognisable:

- **"Create separate projects for each team"** when repository-level IAM would do.
- **"Deploy to an endpoint, run the batch, then undeploy"** when batch prediction takes a config field.
- **"Build a Cloud Function to trigger…"** when the service has a native scheduler.
- **"Export to BigQuery and join…"** when an SDK call returns a DataFrame.
- **"Use a service mesh to route…"** when the Model Registry does traffic splitting.

The pattern: **more infrastructure to reimplement a built-in feature.** When one option is markedly more elaborate than the others, that's usually why.

---

## 1. Training

### By what you're training

| Case | Spec | Why |
|---|---|---|
| Tabular, data in BigQuery, < ~100M rows | **BigQuery ML `CREATE MODEL`** — no machine spec | [Low-code AI](LOW-CODE-AI-ON-GCP.md) |
| Tabular, needs Python (sklearn / XGBoost) | `n1-standard-8`, **no accelerator** | A GPU does nothing for trees — [GPUs and TPUs §1](GPUS-AND-TPUS-FOR-ML.md) |
| Tabular, very wide or very large | `n1-highmem-16` (~104 GB RAM), no accelerator | Memory-bound, not compute-bound |
| Fine-tuning a small vision model | `n1-standard-8` + **1× T4** | 16 GB is usually enough; cheapest real GPU |
| Fine-tuning a mid-size model | `g2-standard-8` (**L4**, 24 GB) | Modern mid-tier, better price/performance than T4 |
| Training a model that needs >24 GB | `a2-highgpu-1g` (**A100 40 GB**) | Memory is the binding constraint, always check it first |
| Serious multi-GPU training | `a2-highgpu-8g` (**8× A100**) | **Scale up before out** — NVLink beats Ethernet |
| Frontier-scale | `a3-*` (**H100**) | Expensive and often supply-constrained |
| Large transformer, JAX or PyTorch | **TPU v5e** or **v6e** | Dense regular matmul is what a systolic array is for |
| **Recommender with big embeddings** | **TPU v5p** (or v6e) | **SparseCores** — [§4a](GPUS-AND-TPUS-FOR-ML.md#4a-sparsecores-why-embeddings-need-different-silicon). **v5e has none.** |
| Distributed Spark preprocessing | **Dataproc serverless**, or a cluster from a custom image | [Dataproc](../../data-eng-gcp/modules/DATAPROC-AND-SPARK.md) |

### The memory check, before you pick anything

**Training in float32 needs roughly 16 bytes per parameter** — weights, gradients, and Adam's two moment estimates. Then add a batch.

| Model size | Rough floor | Smallest sane GPU |
|---|---|---|
| 100M params | ~1.6 GB + batch | T4 (16 GB) |
| 1B params | ~16 GB + batch | A100 40 GB |
| 7B params | ~112 GB + batch | multi-GPU, or LoRA/adapters |

Mixed precision and adapter methods change this a lot. The point is to **do the arithmetic before choosing**, because an out-of-memory error is the failure mode, not slowness.

### Getting the hardware when it's scarce

| Case | `scheduling.strategy` |
|---|---|
| Small job, common hardware | `STANDARD` |
| Can be interrupted, checkpoints properly | `SPOT` — 60–91% off |
| **Can wait to start, cannot be interrupted, ≤7 days** | **`FLEX_START`** + `maxWaitDuration` — ~53% off |
| Must run at a known time, ≤90 days | **future reservation, calendar mode** |
| Must run now, no exceptions | **reservation** |

[Where training runs §4c](VERTEX-TRAINING-COMPUTE.md#4c-getting-the-hardware-at-all)

### And how you package it

| You have | `WorkerPoolSpec` field |
|---|---|
| A Python package, standard framework | **`pythonPackageSpec`** — `packageUris` (Cloud Storage), `pythonModule`, `executorImageUri` |
| A proprietary library, or system dependencies | **`containerSpec`** — `imageUri` in Artifact Registry |
| TPU v5e, any framework | **`containerSpec`** — there are no prebuilt v5e containers |

---

## 2. Serving

### Start here

| Is anything waiting? | Where's the model? | Answer |
|---|---|---|
| **No** | BigQuery ML | **`ML.PREDICT` on a schedule.** No spec. |
| **No** | Model Registry | **Batch prediction job** — [colocation rules apply](VERTEX-BATCH-PREDICTION.md) |
| **Yes** | anywhere | continue below |

> **The most expensive mistake in this document** is building an endpoint when a nightly scheduled query would have done. An endpoint rents a node 24 hours a day to do twenty minutes of work.

### Online serving

| Case | Spec |
|---|---|
| Standard artifact, want it managed | **Vertex endpoint**, `n1-standard-4`, `minReplicaCount=1` |
| Same, but GPU inference | **Vertex endpoint** + **T4** or **L4**; consider `autoscalingMetricSpecs` on duty cycle |
| Needs **isolation, gRPC, big payloads, long timeouts** | **Vertex dedicated public endpoint** |
| Same **and** must sit inside VPC-SC | **Private Service Connect endpoint** — dedicated *public* doesn't support VPC-SC |
| A **tuned Gemini** model | **Shared public endpoint only** — plus VPC-SC access levels to restrict |
| Custom serving logic, spiky traffic, no GPU | **Cloud Run**, `min-instances=1`, startup CPU boost |
| You already run Kubernetes | **GKE** — and read the [autoscaling metric](SERVING-LLMS-ON-GKE.md) section first |
| Analysts need it inside SQL | **Remote model** + `ML.PREDICT` over the endpoint |
| No network at all | **Edge export** — AutoML Edge, TF Lite |

### Serving-side sizing

| Question | Answer |
|---|---|
| How much memory? | Model size **plus** the framework **plus** a request's working set. Inference is roughly 2 bytes/param at fp16, without the optimizer state training needs. |
| GPU for inference? | Only if it's deep learning **and** latency matters. A T4 serves most models fine. |
| `minReplicaCount`? | **1 or more** if latency matters. 0 is v1beta1-only and means a cold start in a user's face. |
| Concurrency on Cloud Run? | Measure it. Raise until p50 degrades, then back off — [§6a](SERVING-MODELS-ON-CLOUD-RUN.md#6a-every-knob-is-right-for-something) |
| Sharing a GPU on GKE? | **MIG** for predictable QoS · **MPS** for concurrent throughput · **time-sharing** for bursty work |

---

## 3. Fifteen cases, end to end

Concrete scenarios with the full answer. Find the nearest one.

<details markdown="1">
<summary><b>1.</b> Churn prediction. 200k customers in BigQuery, scored weekly for a campaign.</summary>

**No compute spec at all.** `CREATE MODEL ... OPTIONS(model_type='BOOSTED_TREE_CLASSIFIER')` in BigQuery ML, then `ML.PREDICT` in a scheduled query writing to a table.

No machine type, no endpoint, no region matching, no accelerator. Cost is query bytes. This is the single most under-used answer in the whole path.
</details>

<details markdown="1">
<summary><b>2.</b> Same churn model, but the mobile app needs a score at signup.</summary>

Now something is waiting. Register the BQML model to the Model Registry (`MODEL_REGISTRY='VERTEX_AI'`), deploy to a **Vertex endpoint**, `n1-standard-2`, `minReplicaCount=1`, no accelerator.

Keep the scheduled query for the campaign. Two consumers, two serving patterns, one model.
</details>

<details markdown="1">
<summary><b>3.</b> Image classifier, 50k labelled images, no ML engineers on the team.</summary>

**AutoML Image Classification.** Budget in milli node hours; the spec is chosen for you.

Decide **Cloud vs Edge before training**. The choice is irreversible. Cloud deploys to an endpoint and cannot be exported; Edge exports to TF Lite and cannot be deployed to an endpoint.
</details>

<details markdown="1">
<summary><b>4.</b> Fine-tuning a ~300M-parameter vision transformer on 100k images.</summary>

Training memory ≈ 300M × 16 bytes ≈ **4.8 GB**, plus activations for the batch. Comfortably a **T4**, and an **L4** if you want headroom.

`n1-standard-8` + 1× `NVIDIA_TESLA_T4`, `pythonPackageSpec` with a prebuilt PyTorch container, `SPOT` if you checkpoint. Serve on a Vertex endpoint with an L4.
</details>

<details markdown="1">
<summary><b>5.</b> Pretraining a 7B-parameter language model.</summary>

7B × 16 ≈ **112 GB** before activations — no single GPU. Either **`a2-highgpu-8g`** (8× A100 80 GB, NVLink) or **TPU v5e/v6e** if you're on JAX or PyTorch/XLA.

For TPU: `ct5lp-hightpu-4t`, topology sized to your chip count, **`replicaCount: 1`**, custom container. Use `FLEX_START` with a `maxWaitDuration`. You can wait to start, but you cannot be preempted mid-run.
</details>

<details markdown="1">
<summary><b>6.</b> Recommender with a 50M-item embedding table.</summary>

**TPU v5p**, for **SparseCores** — four per chip, second generation, ~1.9× faster on embedding-dense models than v4.

**Not v5e.** It's the cost-efficient part and has **no SparseCores at all**, so your most expensive operation runs on hardware never designed for it. v6e is the other option, with two per chip.
</details>

<details markdown="1">
<summary><b>7.</b> Scoring 40M rows weekly with a custom-trained model.</summary>

**Batch prediction job.** No endpoint.

`machine_type='n1-standard-4'`, `starting_replica_count=20` (`max_replica_count` is **ignored** for custom-trained batch). BigQuery in, BigQuery out if the data's there.

**Check colocation**: input, model and output must share a region or multi-region. A model registered from a `US` multi-region BQML dataset silently became `us-central1`.
</details>

<details markdown="1">
<summary><b>8.</b> A 2 GB BERT model behind a custom API, traffic spiky with idle periods.</summary>

**Cloud Run**: weights **baked into the image** (container streaming beats a download under ~10 GB), `min-instances=1`, **startup CPU boost on**, memory ≥ 4 GB, concurrency measured rather than assumed.

`min-instances=1` gives up scale-to-zero. That is the trade-off for the latency, and it is usually right.
</details>

<details markdown="1">
<summary><b>9.</b> A 40 GB LLM on Cloud Run.</summary>

The advice **inverts**. The image is now unwieldy to build, push and cache, so weights go to **Cloud Storage or a FUSE mount** and load at startup. This is why "always bake it in" is a size-dependent rule rather than a principle.

Also reconsider whether Cloud Run is right at this size. A Vertex **dedicated public endpoint** or GKE may fit better.
</details>

<details markdown="1">
<summary><b>10.</b> Self-hosted LLM on GKE with vLLM, traffic spikes.</summary>

GPU node pool (**L4** or **A100** by model size), `minReplicas` **above zero**, HPA on **`vllm:num_requests_waiting`** via Managed Service for Prometheus, target found by load testing from 3–5 upward.

Cluster autoscaler profile: **`balanced`** (the default). `optimize-utilization` removes idle nodes faster and makes your next spike wait.
</details>

<details markdown="1">
<summary><b>11.</b> Ten small inference services, each needing a fraction of a T4.</summary>

**NVIDIA MPS**: `--gpu-sharing-strategy=mps --max-shared-clients-per-gpu=10`. GKE sets `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` to 10% per client.

**MIG isn't available**. It needs A100/H100/H200/B200/GB200/RTX PRO 6000, and a T4 is none of those. Time-sharing would work but adds context-switch latency and enforces no memory limit.
</details>

<details markdown="1">
<summary><b>12.</b> Same, but latency-sensitive and you can choose the hardware.</summary>

**A100 with MIG.** `gpu-partition-size=1g.5gb` gives seven hardware-isolated slices, each with dedicated compute and memory: *"predictable throughput and latency even when other containers saturate other partitions."*

Combine if useful: MIG-partition for the tenants that need QoS, then MPS or time-sharing *within* a partition for those that don't.
</details>

<details markdown="1">
<summary><b>13.</b> Notebooks over sensitive data, no internet allowed.</summary>

**Workbench instance, no external IP**, in a custom VPC with **Private Google Access** on the subnet, **Cloud Router + Cloud NAT** for `pip`, and a **VPC Service Controls** perimeter with an access level for your corporate IP ranges.

Machine spec by workload: `n1-standard-4` for exploration. Add a T4 only if you train in the notebook, and set idle shutdown if you do.
</details>

<details markdown="1">
<summary><b>14.</b> Nightly retraining with a quality gate, deploy only if it improves.</summary>

**Vertex AI Pipelines.** Per-step resources via `.set_accelerator_type()` / `.set_accelerator_limit()` on the task, or `create_custom_training_job_from_component()` when you need an exact machine type or a TPU.

Gate with `dsl.If`, schedule with `create_schedule(cron=..., max_concurrent_run_count=1)`, and set `failure_policy` deliberately if you have parallel branches.

**Not Cloud Composer** for one pipeline. Its scheduler runs continuously and costs hundreds a month before your DAG does anything.
</details>

<details markdown="1">
<summary><b>15.</b> 200 DAGs across warehouses, SaaS APIs and ML, several teams.</summary>

**Now** Cloud Composer earns it. Add **Airflow pools per team** so one team's heavy DAG can't starve another's, use **deferrable operators** for anything waiting on an external service, and submit the actual ML work to **Vertex AI Pipelines** rather than running it on Airflow workers.
</details>

---

## 4. Decoding a machine type in five seconds

```
a2-highgpu-8g
│  │       └── 8 GPUs
│  └── memory profile
└── family: a2 = accelerator-optimised (A100)
```

| Prefix | Means | Accelerator |
|---|---|---|
| `e2` `n1` `n2` `n4` | general purpose | attached, optional |
| `c2` `c3` `c4` | compute optimised | none |
| `m1` `m2` `m3` | memory optimised | none |
| `g2` | accelerator (L4) | **built in** |
| `a2` `a3` `a4` | accelerator (A100/H100) | **built in** |
| `ct5lp-` `ct6e-` | Cloud TPU | **is** the TPU |

| Suffix | RAM per vCPU |
|---|---|
| `highcpu` | ~0.9 GB |
| `standard` | ~3.75 GB |
| `highmem` | ~6.5 GB |

So `n1-highmem-16` is 16 vCPUs and ~104 GB. [Full version](GPUS-AND-TPUS-FOR-ML.md#2-reading-a-machine-type-name).

---

## 5. GPU cheat sheet

| GPU | Memory | Family | Use for |
|---|---|---|---|
| **T4** | 16 GB | attach to `n1` | Cheap inference, light training, notebooks |
| **L4** | 24 GB | `g2` | Modern mid-tier inference |
| **V100** | 16/32 GB | attach to `n1` | Older training |
| **A100** | 40/80 GB | `a2` | Serious training, MIG partitioning |
| **H100** | 80 GB | `a3` | Frontier scale |

**Pick by memory first, then budget.** If it fits in 16 GB, a T4 finishes the job for a fraction of an A100.

---

## 6. Cost sanity checks

Run these before committing a spec. Each one catches a real and common mistake.

| Check | If yes |
|---|---|
| Am I paying for an endpoint that nothing calls between batches? | Batch prediction, or a scheduled query |
| Is `minReplicaCount` higher than the traffic needs? | That's peak cost, permanently |
| Did I attach a GPU to something that isn't deep learning? | Remove it |
| Is a Workbench instance with a GPU left running overnight? | Idle shutdown |
| Can this job be interrupted? | Spot — 60–91% off |
| Can it wait to *start* but not be interrupted? | Flex-start — ~53% off |
| Is a Dataproc cluster idle between nightly runs? | Ephemeral cluster per workflow, or serverless |
| Am I running Composer for one pipeline? | Vertex AI Pipelines, ~$0.03/run |
| Is my TPU at 20% MXU utilisation? | Dimensions to multiples of 128, bfloat16 |

---

## Summary

Most spec questions are settled by three prior questions: **where the data lives**, **whether anything is waiting**, and **whether it's deep learning**. A large share of real work answers "BigQuery, nothing, no", which needs no spec at all. When you do need one: check **memory first** (≈16 bytes per parameter to train), pick the **smallest GPU that fits**, prefer **one machine with many GPUs** over many machines, and reach for **TPUs only for large regular dense work**, with **SparseCores** (v5p, v6e) if embeddings dominate. On the serving side the fork is **batch versus online**, and building an endpoint for work nobody is waiting for is the most expensive habit in this material. For scarce accelerators, the question is what you can tolerate: **interruption** (Spot), **waiting to start** (flex-start), or **neither** (a reservation, at full price).

---

## Where each answer comes from

- Hardware and TPUs → [GPUs and TPUs, from zero](GPUS-AND-TPUS-FOR-ML.md)
- Training jobs, containers, capacity → [Where model training actually runs](VERTEX-TRAINING-COMPUTE.md)
- Batch → [Vertex AI batch prediction](VERTEX-BATCH-PREDICTION.md)
- Endpoints and privacy → [Private networking for ML](GCP-PRIVATE-NETWORKING-FOR-ML.md)
- Autoscaling → [Vertex AI Prediction autoscaling](VERTEX-AUTOSCALING.md)
- Containers and cold starts → [Serving models on Cloud Run](SERVING-MODELS-ON-CLOUD-RUN.md)
- Kubernetes → [Serving LLMs on GKE](SERVING-LLMS-ON-GKE.md)
- Orchestration → [Kubeflow Pipelines](KUBEFLOW-PIPELINES-ON-GCP.md) · [Cloud Composer and DAGs](../../data-eng-gcp/modules/CLOUD-COMPOSER-AND-DAGS.md)
- Spark → [Dataproc for ML data preparation](../../data-eng-gcp/modules/DATAPROC-AND-SPARK.md)
- The no-spec answers → [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md)
