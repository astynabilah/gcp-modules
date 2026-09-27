# BigQuery fundamentals

How BigQuery stores data, how it charges you, and the two table settings that decide most of your bill.

> **Module, not a lab.** This is the layer under every SQL query in the labs.

---

## Names that changed

BigQuery renames things often. You will meet the old names in older docs, blog posts and Stack Overflow answers, so both are listed here.

| Former name | Current name | When |
|---|---|---|
| **BigLake** | **Google Cloud Lakehouse** | 22 Apr 2026 |
| **BigLake metastore** | **Lakehouse runtime catalog** | 22 Apr 2026 |
| **BigQuery tables for Apache Iceberg**, then **BigLake tables for Apache Iceberg in BigQuery** | **Apache Iceberg managed tables** | 2026 |
| **Capacity management** (console) | **Workload management** | 2026 |
| **`tabledata.insertAll`** | **Storage Write API (REST)** | 2026 |
| The old **Storage Write API** | **Storage Write API (gRPC)** | 2026 |
| **BigQuery change data capture** | **change data capture ingestion** | 28 Jan 2026 |
| **Flat-rate pricing** | removed, replaced by **editions** | 5 Jul 2023 |

The APIs, CLI and IAM role names still say `biglake`. Only the documentation and console changed.

---

## 1. Storage and compute are separate

This is the design decision everything else follows from.

> *"One of the key features of BigQuery's architecture is the separation of storage and compute. This allows BigQuery to scale both storage and compute independently, based on demand."*

Three practical results:

- You pay for storage and compute on **separate meters**. You can hold a petabyte and pay nothing for compute until you query it.
- Compute scales per query. There is no cluster to resize.
- Editions are *"a property of compute power, not storage"*, so you can query any dataset no matter how it is stored.

Data is stored in **columnar** format, one column at a time. The storage format is called **Capacitor**. Scanning three columns of a hundred-column table reads three columns, not the whole row.

> **A note on the famous names.** You will read that BigQuery runs on Dremel, Colossus, Borg and Jupiter. Those names come from Google engineering blog posts and research papers. They do **not** appear in the current documentation, which names only Capacitor. The architecture is real; the names are not something you can cite from the docs.

---

## 2. Partitioning

Partitioning splits a table into segments by date or by an integer range. A query with a filter on the partition column reads only the segments it needs.

### The choices

```sql
CREATE TABLE mydataset.events (
  event_time TIMESTAMP,
  user_id STRING,
  amount NUMERIC
)
PARTITION BY DATE(event_time)
OPTIONS (
  require_partition_filter = TRUE,
  partition_expiration_days = 90
);
```

Valid `PARTITION BY` expressions:

| Expression | Gives you |
|---|---|
| `DATE(<timestamp_column>)` | daily partitions on a timestamp |
| `<date_column>` | daily partitions on a date |
| `TIMESTAMP_TRUNC(<ts>, {DAY\|HOUR\|MONTH\|YEAR})` | your choice of granularity |
| `DATETIME_TRUNC(<dt>, {DAY\|HOUR\|MONTH\|YEAR})` | same, for DATETIME |
| `DATE_TRUNC(<date>, {MONTH\|YEAR})` | monthly or yearly |
| `_PARTITIONDATE` | ingestion time, daily |
| `RANGE_BUCKET(<int>, GENERATE_ARRAY(start, end, interval))` | integer ranges |

Daily is the default granularity.

### Ingestion-time partitioning

If you partition by ingestion time, BigQuery adds two pseudocolumns:

- **`_PARTITIONTIME`** — *"the ingestion time for each row, truncated to the partition boundary"*
- **`_PARTITIONDATE`** — *"the UTC date corresponding to the value in the `_PARTITIONTIME` pseudocolumn"*

Two special partitions can appear. `__NULL__` holds rows where the partition column is NULL. `__UNPARTITIONED__` holds rows outside the defined range. You can address them directly:

```sql
SELECT * FROM `mydataset.mytable$__UNPARTITIONED__`;
```

### `require_partition_filter`

This forces every query to filter on the partition column. Without a filter, the query fails instead of scanning the whole table.

Turn it on for any large table. It converts an expensive accident into an error message.

### The limits

| Limit | Value |
|---|---|
| Partitions per table | **10,000** |
| Partitions modified by one job | **4,000** |
| Partition modifications per day (ingestion-time) | 11,000 |
| Ranges in a range-partitioned table | 10,000 |

You cannot convert an existing unpartitioned table to a partitioned one. You have to recreate it.

---

## 3. Clustering

Clustering sorts the data inside each partition by up to four columns.

> *"a clustered column is a user-defined table property that sorts storage blocks based on the values in the clustered columns… Colocation occurs at the level of the storage blocks, and not at the level of individual rows."*

```sql
CREATE TABLE mydataset.orders (...)
PARTITION BY DATE(order_date)
CLUSTER BY country, status;
```

### Key facts

**Maximum four columns.** If you need more, combine clustering with partitioning.

**Order matters.** With `CLUSTER BY order_date, country, status`, a query filtering on `order_date` and `country` is optimised. A query filtering on only `country` and `status` is not. Put the column you filter on most often first.

**It works by pruning blocks, so it needs a filter.** BigQuery uses the filter and the block metadata to skip blocks it does not need. A `SELECT *` with no filter prunes nothing and reads everything.

**Reclustering is free.** BigQuery reclusters in the background at no cost, and *"Automatic reclustering has no effect on query capacity."*

**Adding clustering later does not sort old data.** *"Only new data that's stored using the clustered columns is subject to automatic reclustering."*

Other details: STRING clustering uses *"only the first 1,024 characters"*, and tables under 64 MB usually see no benefit.

### Partition or cluster?

Partitioning gives you an accurate cost estimate before the query runs. Clustering does not, because *"the number of storage blocks to be scanned is not known before query execution."*

Choose **clustering** when:

- You need finer granularity than partitioning allows.
- Your queries filter on several columns.
- The column has high cardinality.
- Partitioning would give you less than about 10 GB per partition. Many small partitions increase metadata and slow down metadata access.
- You would exceed the partition limits.

Choose **both** when partitions average at least 10 GB and you want cost estimates as well as pruning. Partition first, cluster inside each partition.

> **One useful side effect.** On a **clustered** table, `LIMIT` can reduce bytes scanned, because scanning stops once enough blocks are read. On a non-clustered table, `LIMIT` never reduces cost.

---

## 4. Cost drivers

There are two compute pricing models and one storage model.

### On-demand compute

**$6.25 per TiB scanned** in us-central1. The first **1 TiB per month is free**.

The free tier applies per **account**, not per project. *"Pricing models apply to accounts, not individual projects, unless otherwise specified."*

### Capacity compute: editions and slots

A **slot** is *"a virtual compute unit used by BigQuery to execute SQL queries, Python code, or other job types."* You cannot set how many slots a query uses. You buy capacity, and BigQuery allocates it.

Three editions:

| | Standard | Enterprise | Enterprise Plus |
|---|---|---|---|
| SLO | ≥99.9% | ≥99.99% | ≥99.99% |
| Max reservation | **1,600 slots** | quota | quota |
| Commitments | **none** | 1-yr 20% / 3-yr 40% | 1-yr 20% / 3-yr 40% |
| BI Engine | no | yes | yes |
| Create materialized views | no | yes | yes |
| Assign to | project | project / folder / org | project / folder / org |

Enterprise costs roughly **$0.06 per slot-hour** in us-central1.

> **Check the current rates before you budget.** The pricing page builds its tables in the browser, so they are hard to quote reliably. The Enterprise figure above is confirmed by Google's own worked example ($0.036 per slot-hour at a three-year commitment, which is 40% off $0.06). Standard and Enterprise Plus rates could not be confirmed.

**Two discounts that are easy to confuse:**

| | Capacity commitment | Spend-based CUD |
|---|---|---|
| Discount | **20%** (1-yr), **40%** (3-yr) | **10%** (1-yr), **20%** (3-yr) |
| Applies to | slot commitments, Enterprise and above | spend |
| Minimum | 50 slots, in steps of 50 | — |

### Storage

The rule that halves your storage bill without you doing anything:

> *"Active storage includes any table or table partition that has been modified in the last 90 days. Long-term storage includes any table or table partition that has not been modified for 90 consecutive days. The price of storage for that table automatically drops by approximately 50%. There is no difference in performance, durability, or availability."*

| | per GiB-month (approx.) |
|---|---|
| Active logical | $0.023 |
| Long-term logical | $0.016 |
| Active physical | $0.040 |
| Long-term physical | $0.020 |

The first **10 GiB per month is free**.

**Logical or physical billing** is a choice you make per dataset. Physical bills the compressed size, so it is usually cheaper per byte. The catch is in the docs: *"There are no charges for time travel and failsafe storage for logical storage. Time travel and failsafe storage charges apply for physical storage."*

Two more details. Each partition is counted separately for long-term pricing. Editing a table resets the 90-day timer to zero.

### Free operations

Batch loading, table copies, exports, deletes and automatic reclustering cost nothing.

---

## 5. Controlling cost

| Tool | Effect |
|---|---|
| **`maximum_bytes_billed`** | Kills the query if it would scan more than a limit you set |
| **Dry run** | Estimates bytes without running the query |
| **Query cache** | Free, and results last about 24 hours |
| **Custom quotas** | Daily cap per project or per user |
| **Materialized views** | Precomputed results, refreshed automatically |
| **BI Engine** | In-memory cache for frequently used data (not in Standard) |

```bash
bq query --maximum_bytes_billed=1000000 --use_legacy_sql=false 'SELECT ...'
bq query --dry_run --use_legacy_sql=false 'SELECT ...'
```

The failure message is clear: `Error: Query exceeded limit for bytes billed: 1000000. 10485760 or higher required.`

**Common mistake: `SELECT *`.** You are charged for every column you select, so selecting all of them costs the most a query can cost. Name the columns you need.

**Dry-run estimates are an upper bound.** *"The estimate of the number of bytes that is billed for a query is an upper bound, and can be higher than the actual number of bytes billed."*

**Cached results are free**, but the cache is best-effort. *"The typical cache lifetime is 24 hours, but the cached results are best-effort and may be invalidated sooner."*

---

## 6. Table types

**Stored in BigQuery:**

| Type | Description |
|---|---|
| **Standard table** | Structured data in BigQuery storage |
| **Table clone** | A writeable copy. Only the difference from the base table is stored. |
| **Table snapshot** | A read-only copy at a point in time. Only the difference is stored. |

Clones are for development branches off production data. Snapshots are for backups.

**Stored outside BigQuery:**

| Type | Description |
|---|---|
| **Lakehouse tables** (formerly BigLake) | Structured data in Cloud Storage, S3 or Azure Blob, **with fine-grained security** |
| **Object tables** | Unstructured files such as images and PDFs |
| **External tables** | Direct queries over Cloud Storage, Bigtable or Drive, without fine-grained security |
| **Apache Iceberg managed tables** | Fully managed, but stored in your own bucket |

The difference between a Lakehouse table and a plain external table is security. Lakehouse tables support row-level and column-level access control; external tables do not.

**Views:**

- **View** — a saved query. It runs every time. No storage, no speed gain.
- **Materialized view** — the results are cached and refreshed. Costs storage and refresh compute, saves query compute.

---

## 7. Slots and waiting

When a query needs more slots than are free, the work waits:

> *"If a query requests more slots than are available, BigQuery queues up individual units of work and waits for slots to become available."*

You are not charged extra for this. Your query just takes longer.

**Sharing is fair, eventually:**

> *"The BigQuery scheduler enforces the equal sharing of slots among projects with running queries within a reservation, and then within jobs of a given project. The scheduler provides eventual fairness. During short periods, some jobs might get a disproportionate share of slots, but the scheduler eventually corrects this."*

Note the order: **per project first, then per job**. Ten projects sharing one reservation get 100 slots each, no matter how many queries each is running.

On-demand has its own caps: **2,000 concurrent slots per project** and **20,000 across the organization**.

> **A detail that affects planning.** *"In the event of contention in a region, Standard edition and on-demand capacity requests are more likely to experience access delays because the system allocates resources to higher-tier editions first."*

---

## 8. 2026 changes

| When | Change |
|---|---|
| **3 Jun 2026** | **Fluid scaling** GA — per-second billing with no minimum duration for autoscaling reservations. The old floor was one minute. |
| **12 Mar 2026** | **Advanced runtime** is now the default for all projects |
| **18 May 2026** | **Reservation groups** GA — grouped reservations share idle slots with each other first |
| **13 Jul 2026** | Partitioning, multi-statement transactions and advanced runtime GA for **Apache Iceberg managed tables** |
| **8 Oct 2025** | Default `QueryUsagePerDay` for new on-demand projects is now **200 TiB** |

Fluid scaling is the most useful of these if your workload is bursty. The one-minute minimum used to make short autoscaled queries expensive.

---

## 9. Costly Habits to Avoid

**`SELECT *` on a wide table.** You pay for every column.

**No partition filter on a large table.** Set `require_partition_filter = TRUE` so this fails instead of costing money.

**Many small partitions.** Below about 10 GB per partition, metadata overhead outweighs the benefit. Cluster instead.

**Expecting clustering to help an unfiltered query.** Pruning needs a filter.

**Adding clustering to an existing table and expecting old data to sort.** Only new data is reclustered.

**Choosing physical storage billing without checking time travel.** Physical is cheaper per byte, but you start paying for time travel and fail-safe.

**Assuming the free tier is per project.** It is per account.

---

## 10. Partitioning and Cost Scenarios

<details markdown="1">
<summary><b>1.</b> A table has 3 years of daily data, about 200 MB per day. Partition by day?</summary>

Probably not. That is roughly 1,095 partitions at 200 MB each, well under the 10 GB guideline.

The docs list this case directly: partitioning is a poor fit when it *"results in a small amount of data per partition (approximately less than 10 GB)"*, because many small partitions increase metadata and slow metadata access.

Partition by month and cluster by the columns you filter on.
</details>

<details markdown="1">
<summary><b>2.</b> Your table is clustered by <code>country, status</code>. A query filters only on <code>status</code>. Does clustering help?</summary>

No. Order matters. Clustering sorts by `country` first, so rows with the same `status` are spread across many blocks.

Reverse the order, or add a second clustered table, depending on which filter is more common.
</details>

<details markdown="1">
<summary><b>3.</b> Storage costs dropped by half on an old table you did not touch. Why?</summary>

It reached 90 days without modification, so it moved to **long-term storage**. Nothing changes about performance or durability.

If you edit it, the price goes back to active and the 90-day timer restarts.
</details>

<details markdown="1">
<summary><b>4.</b> How do you stop one analyst running a $500 query by accident?</summary>

Two layers. Set **`maximum_bytes_billed`** so oversized queries fail instead of running. Set a **custom quota** for daily usage per user.

Also set `require_partition_filter = TRUE` on large tables, which blocks the most common cause.
</details>

---

## Storage, Compute, and Cost at a Glance

BigQuery separates **storage from compute**, so they scale and bill independently. Data is stored column by column in a format called **Capacitor**. **Partitioning** splits a table by date or integer range, with a limit of **10,000 partitions**, and `require_partition_filter = TRUE` turns a full-table scan into an error. **Clustering** sorts up to **four** columns inside each partition, the column order matters, and it only helps queries that filter. Reclustering is free. Compute is either **on-demand at $6.25 per TiB** with 1 TiB free per month per account, or **editions** measured in slots, where Enterprise runs about $0.06 per slot-hour. Storage drops about 50% after **90 days without modification**, and physical billing is cheaper per byte but adds time travel and fail-safe charges. Control cost with **`maximum_bytes_billed`**, dry runs and custom quotas, and remember that `SELECT *` charges you for every column.

---

## Pricing and Storage Documentation

- [Storage overview](https://cloud.google.com/bigquery/docs/storage_overview) · [Partitioned tables](https://cloud.google.com/bigquery/docs/partitioned-tables) · [Clustered tables](https://cloud.google.com/bigquery/docs/clustered-tables)
- [Pricing](https://cloud.google.com/bigquery/pricing) · [Editions](https://cloud.google.com/bigquery/docs/editions-intro) · [Slots](https://cloud.google.com/bigquery/docs/slots)
- [Cost best practices](https://cloud.google.com/bigquery/docs/best-practices-costs) · [Quotas and limits](https://cloud.google.com/bigquery/quotas)
- [Tables introduction](https://cloud.google.com/bigquery/docs/tables-intro) · [Apache Iceberg managed tables](https://cloud.google.com/bigquery/docs/iceberg-tables)
- Related: [BigQuery connections and federated data](BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md) · [Data validation in BigQuery ML](../../mlops-gcp/modules/BIGQUERY-DATA-VALIDATION.md)
