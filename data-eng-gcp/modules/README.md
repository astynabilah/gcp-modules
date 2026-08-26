# The modules

**Theory, not tutorials.** Concepts, decision frameworks and reference material — nothing to run. The ML counterparts are in [`../../mlops-gcp/`](../../mlops-gcp/README.md).

---

## Foundations

### [BigQuery fundamentals](BIGQUERY-FUNDAMENTALS.md)
How BigQuery stores data and how it charges you. **Partitioning** splits a table and caps at 10,000 partitions; `require_partition_filter` turns a full scan into an error. **Clustering** sorts up to four columns inside each partition, and column order matters. Storage drops about 50% after **90 days without modification**. Includes the rename table: BigLake is now **Google Cloud Lakehouse**.

### [IAM and service accounts](IAM-AND-SERVICE-ACCOUNTS.md)
Who can do what, on which resource. Policies flow down the hierarchy and combine as a **union**, so a grant on a child never removes inherited access. A service account is **both a principal and a resource**. Covers why `serviceAccountUser` and `serviceAccountTokenCreator` are not the same, why service account keys break your audit trail, and the Compute Engine default account that Dataproc, Dataflow and GKE all fall back to.

---

## Processing — moving and shaping data at scale

### [Dataproc and Spark](DATAPROC-AND-SPARK.md)
Managed Spark, and the production question that comes up most: consistent, fast-starting clusters with your own Python libraries. The answer is a **custom image**, because `pip.packages` installs at boot and Google explicitly warns against referencing **public initialization actions** — those scripts change underneath you. Plus pinning `major.minor` rather than a full version or the default, the **365-day custom-image expiry** that gates cluster *creation*, and why serverless starts in ~50 seconds against a cluster's ~120.

---

## Data access — reaching what isn't in BigQuery

### [BigQuery connections and federated data](BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md)
A connection is a resource with its own **auto-created service account**, and that account, not the caller, is what reaches Cloud SQL. So access is always **two grants to two identities**: `bigquery.connectionUser` to the person *on the connection*, and the target-service role to the connection's service account. Covers why `EXTERNAL_QUERY`'s inner string is the **source database's dialect**, which source types have no BigQuery equivalent (and why a UDF can't rescue them), and why federated queries are wrong for building training data.

---

## Governance — knowing what's in the data

### [Sensitive Data Protection](SENSITIVE-DATA-PROTECTION.md)
Finding and removing PII — including in data that never touches Google Cloud. Content methods cap at **0.5 MB**, storage jobs reach only Cloud Storage, BigQuery and Datastore, and **hybrid jobs** inspect *"payloads of data sent from virtually any source"*. On de-identification, the property that keeps data usable is **referential integrity**: `CryptoDeterministicConfig` for join keys, and `DateShiftConfig` for dates because it destroys the values while preserving **sequence and duration**.

---

## Orchestration — making things run by themselves

### [Cloud Composer, Airflow and DAGs](CLOUD-COMPOSER-AND-DAGS.md)
Starts from what a **DAG** is — directed, acyclic, and why forbidding cycles is what makes a graph runnable at all. Then Airflow's vocabulary, why `execution_date` names the **data interval** rather than the clock, the cross-DAG question (**`TriggerDagRunOperator`** versus `ExternalTaskSensor`, with `SubDagOperator` deprecated and `TaskGroup` being visual grouping only), and **Airflow pools** as the only concurrency control scoped to a team rather than a DAG or the whole environment.

### [Triggers, schedules and cron](TRIGGERS-SCHEDULES-AND-CRON.md)
The layer underneath every orchestrator. Teaches **cron properly**: five fields, `*` means every, Sunday is `0`, the two day fields combine as an **OR** not an AND, and the expression carries **no timezone**. Then Eventarc: which Cloud Storage event really means "a new file arrived" (**`finalized`**, and why `archived` is about Object Versioning), why **at-least-once delivery makes idempotency a requirement rather than a nicety**, and what to do when a bulk upload fires fifty triggers at once.

---

## Figures

Every diagram is generated from code in [`../../tools/figures/`](../../tools/README.md) and validated for overflow. They are **mockups of the Google Cloud console, not screenshots** — accurate about fields and controls, not about pixels.
