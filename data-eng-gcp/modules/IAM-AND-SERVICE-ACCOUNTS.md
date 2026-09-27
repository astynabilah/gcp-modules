# IAM and service accounts

Who can do what, on which resource. Every permission problem you hit on Google Cloud comes back to this page.

> **Module, not a lab.** Nothing here needs running.

---

## 1. Three things make up an access rule

Google Cloud access has three parts. Learn these three words and most error messages start to make sense.

| Part | Description |
|---|---|
| **Principal** | Who is asking. A person, a group, or a service account. |
| **Role** | A named bundle of permissions, like `roles/bigquery.dataViewer`. |
| **Allow policy** | The document that binds principals to roles on a resource. |

You never grant a permission directly. You grant a **role**, and the role contains permissions.

Principals are written in a fixed format:

```
user:alex@example.com
group:data-team@example.com
serviceAccount:etl-runner@my-project.iam.gserviceaccount.com
domain:example.com
```

Two special values exist. `allUsers` means anyone on the internet. `allAuthenticatedUsers` means anyone with a Google account. Both are blocked by default in organizations created after 3 May 2024.

> **A note on old wording.** Google used to call principals "members" and allow policies "IAM policies". Some APIs still use the old words. They mean the same thing.

---

## 2. Policies flow downhill, and they add up

Resources sit in a hierarchy: **organization → folder → project → resource**.

A policy set on a parent applies to everything below it. The rule is short:

> *"The effective allow policy for a resource is the union of the allow policy set at that resource and the allow policy inherited from its parent."*

**Union** is the word to hold on to. A child policy adds access. It cannot take access away.

The docs give a plain example:

> *"if the allow policy for a project grants a user the ability to administer Compute Engine virtual machine (VM) instances, then the user can administer any Compute Engine VM in that project, regardless of the allow policy you set on each VM."*

Two things follow from this.

**You cannot narrow an inherited grant.** If someone has Editor on the project, giving them a smaller role on one table changes nothing. The docs say it plainly: granting a role with the same or fewer permissions "is redundant, and doesn't have any effect."

**To actually reduce access, you must fix it at the level where it was granted.** Or use a deny policy, which is covered in §6.

Also worth knowing: access changes are **eventually consistent**. A grant may take a short while to work.

---

## 3. Three kinds of role

### Basic roles

Owner, Editor and Viewer. Google now calls these **legacy basic roles**. Newer Admin, Writer and Reader roles exist in Preview.

Google's advice on the legacy three is direct:

> *"Basic roles include thousands of permissions across all Google Cloud services. In production environments, do not grant basic roles unless there is no alternative."*

Two practical limits make them worse than they look:

- You **cannot attach IAM Conditions** to legacy basic roles. So you cannot say "Editor, but only on this bucket".
- They pick up extra access through side doors, including Cloud Storage convenience values and BigQuery special group membership.

### Predefined roles

Made and maintained by Google, named `roles/SERVICE.IDENTIFIER`. Google updates their permissions as services change. Start here.

### Custom roles

You choose the exact permission list. Use them when no predefined role fits.

The rules that catch people out:

| Rule | Detail |
|---|---|
| **Scope** | Organization or project only. **Not folders.** Define at org level if you need one inside a folder. |
| **Permission support** | Each permission is `SUPPORTED`, `TESTING`, or `NOT_SUPPORTED`. `TESTING` permissions "might see unexpected behavior" and are not for production. |
| **Project-level limits** | A project custom role cannot hold org-only permissions. You get `INVALID_ARGUMENT` if you try. |
| **Quotas** | 300 per organization, 300 per project, 3,000 permissions per role. |
| **IDs are permanent** | You cannot reuse a role ID for 44 days after deleting it. |

Launch stage (`ALPHA`, `BETA`, `GA`) is just a label. Only `DISABLED` does anything: the role stays in policies but stops working.

---

## 4. Service accounts are both a user and a thing

This is the idea that unlocks the rest. Google states it in one sentence:

> *"Because a service account is a principal, you must limit its privileges… Because a service account is a resource, you must protect it from being compromised."*

**As a principal**, a service account gets roles. You grant it `roles/storage.objectViewer` on a bucket so your pipeline can read files.

**As a resource**, a service account has its own allow policy. You grant *other people* roles *on it*, to control who may use it.

Mixing these up causes a lot of confused debugging. If your job cannot read a bucket, that is the first kind. If you cannot start the job at all, it is usually the second.

### Two roles that sound alike and are not

| | `roles/iam.serviceAccountUser` | `roles/iam.serviceAccountTokenCreator` |
|---|---|---|
| Lets you | **attach** the service account to a resource | **get tokens** for the service account |
| Works with `--impersonate-service-account` | **No** | **Yes** |

The docs are explicit that Service Account User "does not allow principals to create short-lived credentials for service accounts, or to use the `--impersonate-service-account` flag."

A simple way to choose:

- Deploying something that **runs as** the service account — a Dataflow job, a Cloud Run service, a Composer environment? You need **Service Account User**.
- Running `bq` or `gcloud` **as** the service account from your laptop or CI? You need **Service Account Token Creator**.

### Impersonation and short-lived credentials

Impersonation means acting as a service account using your own login. You get a token that lasts **1 hour** by default, up to 12 hours with an org policy.

```bash
gcloud auth print-access-token --impersonate-service-account=ETL_SA
```

Nothing is stored on your machine. That is the point.

---

## 5. The risk of service account keys

Google's guidance is short: *"We recommend that you avoid using service account keys whenever possible."*

The strongest reason is about audit logs, not theft:

> *"Cloud Audit Logs creates a log when a service account modifies a resource, but if the service account is authenticated with a service account key, there is no reliable way to tell who used the key. In comparison, authenticating as a service account by impersonating the service account with user credentials logs the principal who acted as the service account."*

So a key turns "Priya deleted the table" into "some process deleted the table". You lose the ability to answer the question you most need answered.

A key also skips extra sign-in checks. A leaked key usually just works.

**What to use instead**, in the order Google recommends:

1. Working locally or in Cloud Shell → **your own login**, or impersonate a service account with it.
2. Running on GKE → **Workload Identity Federation for GKE**.
3. Running elsewhere on Google Cloud → **attach a service account** to the resource.
4. Running outside Google Cloud → **Workload Identity Federation**.
5. Only if none of these work → create a key.

You can block keys entirely with two org policy constraints: **Disable service account key creation** and **Disable service account key upload**. These beat the `iam.serviceAccountKeys.create` permission, so even a key admin cannot make one. Organizations created on or after 3 May 2024 have them on by default.

---

## 6. The default service account problem

Every project gets a Compute Engine default service account:

```
PROJECT_NUMBER-compute@developer.gserviceaccount.com
```

Depending on your org policy, **it may be granted Editor on the whole project automatically**. Google's advice:

> *"We strongly recommend that you disable the automatic role grant by enforcing the `iam.automaticIamGrantsForDefaultServiceAccounts` organization policy constraint."*

Organizations created after 3 May 2024 already enforce it.

This matters a lot for data work, because **Dataproc, Dataflow and GKE all fall back to this account** when you do not set one. If it holds Editor, then every cluster, every pipeline and every node in the project runs with Editor. Fixing that one binding is usually the largest single security improvement available in a data platform.

If it already has Editor, replace it rather than deleting it. Use **Policy Simulator** to check what breaks first, and role recommendations to pick smaller roles.

---

## 7. Narrowing access further

### IAM Conditions

Add a condition to a role binding and it applies only some of the time.

```
resource.name.startsWith('projects/_/buckets/exampleco-site-assets/')
request.time < timestamp('2027-01-01T00:00:00.000Z')
resource.type == 'storage.googleapis.com/Object'
```

Conditions use CEL. A binding needs a `title` and an `expression`; `description` is optional. Adding any condition sets the policy `version` to 3.

Limits to remember: conditions do not work with legacy basic roles, `allUsers`, or `allAuthenticatedUsers`. Some services do not accept them at all.

### Deny policies

A deny policy blocks a permission no matter what roles say:

> *"IAM always checks relevant deny policies before checking relevant allow policies."*

Differences from allow policies you should expect:

- Attach only to an **organization, folder or project**, never to a single resource.
- You can attach **several** deny policies to one resource. Only one allow policy is allowed.
- Permissions use a different format: `iam.googleapis.com/roles.delete`, not `iam.roles.delete`.
- If a deny condition **cannot be evaluated**, the permission is denied. It fails closed.

### Tools that show what is happening

| Tool | Answers |
|---|---|
| **IAM Recommender** | Which granted permissions has this principal not used in 90 days? |
| **Policy Simulator** | What would break if I made this change? |
| **Policy Analyzer** | Who can access this resource? |
| **Policy Troubleshooter** | Why can this principal do this, or why not? |

Two blind spots in Policy Troubleshooter: it does not account for Cloud Storage ACLs, and it does not diagnose VPC Service Controls problems. If access looks impossible to explain, check those two by hand.

---

## 8. Workload Identity Federation

This lets a workload outside Google Cloud use its **existing identity** to get Google Cloud access. No key file.

> *"Workload Identity Federation eliminates the maintenance and security burden associated with service account keys."*

It works with AWS, Azure, Active Directory, GitHub, GitLab, Kubernetes clusters, Okta, and anything speaking OIDC or SAML 2.0.

There are **two ways to use it**, and the second is the one people miss:

- **Direct access** — grant roles straight to the federated identity. No service account at all.
- **Service account impersonation** — the federated identity impersonates a service account.

Google recommends one pool per environment: separate pools for development, staging and production.

---

## 9. Grant on the resource, not the project

Many services let you grant a role on a single resource. This is the practical form of least privilege, and it is easy to forget it is available.

| Service | You can grant on |
|---|---|
| **BigQuery** | datasets, tables, routines |
| **Cloud Storage** | buckets, managed folders |
| **Pub/Sub** | topics, subscriptions, schemas, snapshots |
| **Secret Manager** | secrets |
| **Cloud KMS** | crypto keys, key rings |
| **Cloud Run** | services, jobs, worker pools |
| **Bigtable**, **Spanner**, **Dataform**, **Artifact Registry** | various |

The docs give the shape of it: if a user only needs to publish to one Pub/Sub topic, grant Publisher **on that topic**.

Remember §2 though. A resource grant **adds** access. It never cancels something inherited from the project.

---

## 10. Frequent Permission Errors

**Granting Editor because a smaller role failed.** Find the missing permission instead. The error message usually names it.

**Trying to fix over-permission at the resource level.** Inheritance is a union. Fix it where it was granted.

**Confusing Service Account User with Token Creator.** Attaching is not impersonating.

**Creating a key because it is quicker.** You lose the audit trail, and the key outlives the reason you made it.

**Leaving the Compute Engine default service account with Editor.** Dataproc, Dataflow and GKE all inherit it.

**Custom roles at folder level.** Not supported. Define at the organization.

**Assuming a deny policy is just a smaller grant.** Deny always wins, and it fails closed when it cannot evaluate.

---

## 11. Access Control Scenarios

<details markdown="1">
<summary><b>1.</b> A user has Editor on the project. You grant them Viewer on one table to limit them. What happens?</summary>

Nothing changes. Inheritance is a **union**, so they keep Editor on that table along with everything else.

To reduce their access you must change the project-level grant, or add a deny policy.
</details>

<details markdown="1">
<summary><b>2.</b> Your CI pipeline runs <code>bq query</code> as a service account and gets a permission error before touching BigQuery. Which role is missing?</summary>

`roles/iam.serviceAccountTokenCreator` on that service account.

CI is **impersonating** the account, which needs a short-lived token. `roles/iam.serviceAccountUser` only lets you attach an account to a resource, and does not allow `--impersonate-service-account`.
</details>

<details markdown="1">
<summary><b>3.</b> Why is a service account key bad even if you store it safely?</summary>

Audit logs cannot tell you **who used it**. All actions appear as the service account.

Impersonation logs the person who acted as the account, so you keep the answer to "who did this".
</details>

<details markdown="1">
<summary><b>4.</b> Your Dataproc cluster can delete BigQuery tables it should never touch. Why?</summary>

You probably did not set a service account, so it uses the **Compute Engine default service account** — and that account may hold Editor on the project.

Enforce `iam.automaticIamGrantsForDefaultServiceAccounts`, then give the cluster its own account with only the roles it needs.
</details>

---

## Principals, Roles, and Policies Summarized

Access on Google Cloud is a **principal**, a **role**, and an **allow policy** that binds them. Policies flow down the hierarchy and combine as a **union**, so a grant on a child can never take away access inherited from a parent. Avoid legacy basic roles: they carry thousands of permissions and cannot take IAM Conditions. A **service account is both a principal and a resource** — grant it roles to give it access, and grant others roles on it to control who may use it. `serviceAccountUser` attaches an account to a resource; `serviceAccountTokenCreator` lets you impersonate it. Avoid **service account keys**, mainly because audit logs cannot tell you who used one. Check whether the **Compute Engine default service account** still has Editor, because Dataproc, Dataflow and GKE all fall back to it. Then narrow what is left with **IAM Conditions**, **deny policies** (which always win and fail closed), and **resource-level grants**.

---

## Source Documentation

- [IAM overview](https://cloud.google.com/iam/docs/overview) · [Roles and permissions](https://cloud.google.com/iam/docs/roles-overview)
- [Resource hierarchy access control](https://cloud.google.com/iam/docs/resource-hierarchy-access-control)
- [Service account overview](https://cloud.google.com/iam/docs/service-account-overview) · [Best practices for service accounts](https://cloud.google.com/iam/docs/best-practices-service-accounts)
- [Best practices for service account keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys)
- [IAM Conditions](https://cloud.google.com/iam/docs/conditions-overview) · [Deny policies](https://cloud.google.com/iam/docs/deny-overview)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Resource types that accept allow policies](https://cloud.google.com/iam/docs/resource-types-with-policies)
- Related: [BigQuery connections and federated data](BIGQUERY-CONNECTIONS-AND-FEDERATED-DATA.md) · [Sensitive Data Protection](SENSITIVE-DATA-PROTECTION.md) · [CI/CD for ML](../../mlops-gcp/modules/CI-CD-FOR-ML-ON-GCP.md)
