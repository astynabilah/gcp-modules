# Sensitive Data Protection

**Finding and removing PII before it becomes a problem** — including in data that never touches Google Cloud. The service formerly called Cloud DLP, and the one method that lets you inspect anything you can write a client for.

> **Module, not a lab.** The ML angle: training data is where PII quietly accumulates, because nobody de-identifies a dataset they only meant to explore.

---

## Naming and status

| | |
|---|---|
| **Renamed** | Cloud DLP is now part of **Sensitive Data Protection**. Every page carries the banner: *"Cloud Data Loss Prevention (Cloud DLP) is now a part of Sensitive Data Protection. The API name remains the same: Cloud Data Loss Prevention API (DLP API)."* |
| **Unchanged** | The endpoint is still `dlp.googleapis.com`, still **v2**, and the resources are still `dlpJobs`, `inspectTemplates`, `deidentifyTemplates`, `jobTriggers`, `storedInfoTypes`. |
| **Note the wording** | *"is now **a part of**"* — Sensitive Data Protection is a family (discovery, inspection, de-identification, risk analysis) of which the DLP API is one member. Not a 1:1 rename. |

Actively developed through 2026: batched content inspection (June), conversational content inspection (June), file label detection (June). One more is useful for anyone handling model logs: **`ANTHROPIC_API_KEY`, `GEMINI_API_KEY` and `OPENAI_API_KEY` detectors went to all regions in August 2026.**

---

## 1. Four ways to inspect, and how to choose

| Method type | Shape | Reaches |
|---|---|---|
| **Content** | synchronous, stateless, findings in the response | whatever you put in the request |
| **Storage jobs** | asynchronous, findings stored | **Cloud Storage, BigQuery, Datastore** — natively |
| **Hybrid** | asynchronous, you push the data | **anything you can write a client for** |
| **Discovery** | continuous profiling | BigQuery, Cloud SQL, Cloud Storage, Vertex AI — plus S3 and Azure Blob under a Security Command Center Enterprise activation |

### Content methods — small, synchronous, nothing stored

`content.inspect`, `content.deidentify`, `content.reidentify`, `image.redact`. *"The data to be inspected or transformed is sent directly in the request… Request data is encrypted in transit and **is not stored**."*

**The deciding limit: 0.5 MB per request** (4 MB for `image.redact`), 3,000 findings, 100 transformations. Google's own advice when you exceed it: *"If you need to inspect files that are larger than these limits, store those files on Cloud Storage and run an inspection job."*

### Storage inspection jobs — three sources, natively

A `dlpJob` with a `StorageConfig` scans **Cloud Storage, BigQuery, or Firestore in Datastore mode**, up to **2 TB**. It crawls the data itself; you configure and wait.

**And that is the limit.** Storage jobs cannot reach a MySQL instance in a VM, an on-premises warehouse, another cloud's database, or a stream. The third method exists for that.

### Hybrid jobs — inspection for everything else

> *"Hybrid jobs and job triggers encompass a set of asynchronous API methods that allow you to scan payloads of data sent from virtually any source for sensitive information, and then store the findings in Google Cloud. Hybrid jobs enable you to write your own data crawlers that behave and serve data similarly to the Sensitive Data Protection storage inspection methods."*

Google names the targets explicitly: *"Other cloud providers"*, *"On-premises servers or other data repositories"*, *"Non-native storage systems, such as systems running inside a virtual machine"*, *"Web and mobile apps."*

**One sentence sums it up:** *"A hybrid job is effectively a hybrid of content methods and storage methods."* You push the data like a content method. Findings are stored and tabulated like a storage job: *"unlike content methods, hybrid methods do not return inspection results in the API response."*

---

## 2. How a hybrid job works

```
your ingestion code  ──hybridInspect──▶  Sensitive Data Protection
                                              │  (config lives here, not in your client)
                                              ▼
                                    findings ──▶ BigQuery / SDP / Pub/Sub
```

**The methods:**

| Method | Does |
|---|---|
| `projects.locations.dlpJobs.hybridInspect` | *"Inspect hybrid content and store findings to a **job**."* |
| `projects.locations.jobTriggers.hybridInspect` | *"Inspect hybrid content and store findings to a **trigger**."* |
| `projects.locations.dlpJobs.finish` | *"Finish a running hybrid DlpJob."* |

The data source is declared in **`hybridOptions`** inside the `StorageConfig`.

### Job or trigger — and why a trigger is nearly always right

> *"A hybrid job trigger enables you to create, activate, and stop jobs so that you can trigger actions whenever you need. By ensuring that your script or code sends data that includes the hybrid job trigger's identifier, **you don't need to update your script or code whenever a new job is started.**"*

A bare hybrid job has an ID that your client must know, and someone must `finish` it. A **trigger** gives you a stable identifier that spawns jobs on demand. So the client is written once and never redeployed because a job rotated. For a continuously-running ingestion pipeline, that difference decides the design.

### The centralisation claim

> *"All inspection configuration is managed within Sensitive Data Protection, with **no extra configuration required on the client side**."*

That is the architectural benefit, and it should be stated plainly: **your crawler ships no detection logic.** It sends bytes and a trigger ID. What counts as sensitive, which infoTypes, which thresholds, what to do about findings — all of it lives in an **inspection template** that a security team owns and can change without touching your pipeline.

### Findings, and one behaviour unique to hybrid

Post-scan actions: **save to Sensitive Data Protection**, **save to BigQuery**, **Pub/Sub**, **email**, **publish to Cloud Monitoring**.

> *"These actions work with hybrid jobs similarly to how they work with other job types, with one important difference: **With hybrid jobs, findings are made available while the job is running; with other job types, findings are made available when the job ends.**"*

So a long-running hybrid job streams its findings out as it goes. This is what makes it usable in front of a live pipeline. The Pub/Sub, email and Monitoring actions still fire only at the end.

### Metadata is how findings stay traceable

Attachable at two levels — on the job/trigger, and per request:

- **Required labels** — requests missing them are rejected. A hard gate against an unlabelled client polluting your findings table.
- **Optional labels** — key-value pairs on each finding, e.g. `"env"="prod"`.
- **Container details** — `fullPath`, `rootPath`, `relativePath`, `type`, `version`.
- **`hybridOptions.tableOptions.identifyingFields`** — up to **three** column names, so a finding traces back to a source row.

That last one matters more than it looks: a finding you can't locate is a finding you can't fix.

---

## 3. infoTypes — what "sensitive" means

**Built-in detectors** cover roughly two hundred categories: `EMAIL_ADDRESS`, `PERSON_NAME`, `PHONE_NUMBER`, `CREDIT_CARD_NUMBER`, `US_SOCIAL_SECURITY_NUMBER`, plus the newer `AUTH_TOKEN`, `AWS_CREDENTIALS`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.

> Google's docs say only *"many built-in infoType detectors"* rather than publishing a count. Enumerate them from the API rather than trusting a number in a blog.

**Custom detectors** come in five kinds:

| Kind | For |
|---|---|
| **Regular custom dictionary** | word and phrase lists — *"at most several hundred thousand words"* |
| **Large custom dictionary** | from Cloud Storage or BigQuery — *"up to tens of millions"* |
| **Regex** | patterns — internal account formats, employee IDs |
| **Metadata label** | Google Drive or Microsoft sensitivity labels |
| **Surrogate** | *"only used with the `content:reidentify` method to reverse de-identification using format-preserving encryption"* |

InfoTypes are versioned. `InfoType.version` takes `latest`, `stable`, or `legacy`, so a detector can change under you. Pin `stable` where reproducibility matters.

---

## 4. De-identification — and the two transformations that matter for analytics

Redaction, replacement, masking, crypto-based tokenization, bucketing, date shifting, time extraction. The main distinction is **reversibility** and **referential integrity**:

| Transformation | Reversible | Referential integrity |
|---|---|---|
| `RedactConfig`, `ReplaceValueConfig`, `CharacterMaskConfig` | No | No |
| `CryptoHashConfig` | No (one-way) | Yes |
| **`CryptoDeterministicConfig`** | **Yes** | **Yes** |
| `CryptoReplaceFfxFpeConfig` (FPE) | Yes | Yes |
| `FixedSizeBucketingConfig`, `BucketingConfig` | No | No |
| **`DateShiftConfig`** | Yes | preserves sequence and duration |

**Referential integrity is what keeps de-identified data usable:**

> *"given the same crypto key and context, the data will be replaced with the same obfuscuted form each time it is transformed allowing for connections between records to be preserved."*

Without it, the same customer becomes a different token in every table and every join breaks. With it, you can de-identify a whole warehouse and still compute a per-customer aggregate.

> **Use `CryptoDeterministicConfig`, not FPE.** Google is direct here: *"**Don't use the `CryptoReplaceFfxFpeConfig` method, except when preserving the input alphabet space and size is a requirement.** The `CryptoReplaceFfxFpeConfig` method can run very slowly, and it has limitations on the size of the alphabet and number of tokens… The `CryptoDeterministicConfig` method has no limitations on the input and is much faster."* FPE exists for legacy systems where a field's length must stay the same.

**`DateShiftConfig` is easy to overlook.** Shifting every date for a given entity by the same random offset destroys the real dates while **preserving sequence and duration**. So "days between signup and churn" survives de-identification intact. For any time-series or survival analysis, that is the difference between usable and ruined data.

Structured data uses `recordTransformations`; unstructured uses `infoTypeTransformations`.

---

## 5. Where this belongs in a pipeline

The documented shape, in order:

1. **Discovery** to find where sensitive data really lives. Since 2026 this includes a dedicated **Vertex AI discovery** that profiles training datasets and tuning jobs, writing profiles to BigQuery.
2. **Templates** to centralise the configuration. Google's guidance on who holds them: *"accessible by only a small group of people—such as security admins—to avoid exposing de-identification methods and encryption keys."*
3. **Dataflow** to apply transformations at scale — the reference architecture reads from Cloud Storage **and Amazon S3**, writes to BigQuery, with a separate pipeline to re-identify.
4. **Hybrid jobs** for anything the storage methods can't reach.

> **The ML-specific version of the mistake:** a dataset gets exported "just to explore", lands in a notebook bucket, becomes a feature table, and ends up in a training set. By then the PII is in the model's inputs and possibly in its outputs. Inspect at ingestion, not at review time.

> **A retired page to be aware of:** Google's old *"Considerations for Sensitive Data within Machine Learning Datasets"* architecture guide now redirects to a generic de-identify how-to. If you have a link to it, it's stale.

---

## 6. What it doesn't do

**Model Armor is not this.** Model Armor screens prompts and responses for Gemini and *"is integrated with Google Cloud's Sensitive Data Protection service"* using an SDP template as a filter. But the documented limitation matters:

> *"Although Sensitive Data Protection de-identifies the data based on the template configuration, **Model Armor doesn't pass the de-identified data**—such as masked, redacted, or hashed content."*

So Model Armor gives you **detect-and-block**, not **detect-and-sanitise**. If you need actual redaction in a prompt path, call `content.deidentify` yourself.

**Detection is probabilistic.** InfoType detectors have likelihood levels for a reason. A free-text field will produce false positives and miss things a human would catch. Tune with exclusion rules and hotword rules rather than trusting the defaults.

---

## 7. Design Mistakes to Avoid

**Staging external data in Cloud Storage purely to make it scannable.** Adds a copy, a latency hop, and a second place your PII now lives — to reach a capability hybrid jobs give you directly.

**Calling `content.inspect` per record and building your own findings store.** You've reimplemented job management, aggregation and storage that hybrid jobs provide, and you own it forever.

**A custom Dataflow `DoFn` calling the API record-by-record** when a hybrid job trigger would do. Reach for Dataflow when you need the *transformation* at scale, not to get inspection working at all.

**Masking join keys.** `CharacterMaskConfig` on a customer ID destroys referential integrity and every downstream join with it. Use `CryptoDeterministicConfig`.

**Naive date redaction in time-series data.** Nulling dates kills the temporal signal. `DateShiftConfig` preserves it.

**Detection logic in the client.** The whole point of templates is that a security team can change what counts as sensitive without a deployment.

---

## 8. Inspection Method Scenarios

<details markdown="1">
<summary><b>1.</b> Streaming feedback from sources outside Google Cloud needs PII inspection, with centralised config and findings. What do you build?</summary>

**A hybrid job trigger with an inspection template**, with your ingestion application sending `hybridInspect` requests, and findings saved to BigQuery.

Storage inspection jobs only reach Cloud Storage, BigQuery and Datastore, so external sources are out. Staging into Cloud Storage first adds latency and a second copy. And `content.inspect` per record works, but it leaves you owning findings aggregation and storage, which is what hybrid jobs exist to provide.

A **trigger** rather than a bare job, so the client carries a stable identifier and never needs redeploying when a job rotates.
</details>

<details markdown="1">
<summary><b>2.</b> You de-identify customer IDs and every downstream join breaks. What went wrong?</summary>

You used a transformation without **referential integrity**. Masking or plain replacement gives a different output for the same input.

**`CryptoDeterministicConfig`** produces the same token for the same input given the same key and context, so joins survive. It's also reversible with the key, which masking is not.
</details>

<details markdown="1">
<summary><b>3.</b> How do you de-identify dates without destroying a churn model?</summary>

**`DateShiftConfig`.** It shifts dates by a consistent per-entity offset, so absolute dates are destroyed but **sequence and duration are preserved** — "days from signup to churn" still computes correctly.

Redaction or bucketing would remove exactly the signal the model depends on.
</details>

<details markdown="1">
<summary><b>4.</b> Model Armor is filtering prompts with an SDP template. Is your PII being redacted?</summary>

**No.** Model Armor detects and can block, but *"doesn't pass the de-identified data"* — you don't get the masked or hashed version back. For actual redaction in the prompt path, call `content.deidentify` yourself.
</details>

---

## Inspection and De-identification, Boiled Down

Sensitive Data Protection (the former Cloud DLP; still `dlp.googleapis.com`) inspects data four ways, and the one that decides your architecture is **hybrid jobs**: content methods cap at **0.5 MB** and store nothing, storage jobs reach only **Cloud Storage, BigQuery and Datastore**, and hybrid jobs inspect *"payloads of data sent from virtually any source"*, including on-premises, another cloud, or inside a VM. Prefer a **hybrid job trigger** over a bare job so the client holds a stable identifier, and note that hybrid findings appear **while the job runs** rather than at the end. Configuration lives in an **inspection template** so the client ships no detection logic. On de-identification, the property that keeps data usable is **referential integrity**. Use **`CryptoDeterministicConfig`** for join keys (Google explicitly discourages FPE as slow and constrained), and **`DateShiftConfig`** for dates, because it destroys the values while preserving **sequence and duration**. Model Armor is detect-and-block, not detect-and-sanitise.

---

## Related Documentation

- [Hybrid jobs and job triggers](https://cloud.google.com/sensitive-data-protection/docs/concepts-hybrid-jobs) · [Method types](https://cloud.google.com/sensitive-data-protection/docs/concepts-method-types)
- [Transformation reference](https://cloud.google.com/sensitive-data-protection/docs/transformations-reference) · [Pseudonymization](https://cloud.google.com/sensitive-data-protection/docs/pseudonymization)
- [Custom infoType detectors](https://cloud.google.com/sensitive-data-protection/docs/creating-custom-infotypes)
- [De-identification and re-identification of PII in large-scale datasets](https://cloud.google.com/architecture/de-identification-re-identification-pii-using-cloud-dlp)
- [Sensitive data discovery for Vertex AI](https://cloud.google.com/sensitive-data-protection/docs/discovery-for-vertex-ai)
- Related: [BigQuery connections and federated data](BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md) · [Dataproc and Spark](DATAPROC-AND-SPARK.md)
