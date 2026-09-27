# Search, conversation and agents

This module covers Agent Search, AI Commerce Search, Dialogflow, and the agent products around them. The names here changed far faster than the products did. One search product has carried **six names in three years**, while its API endpoint stayed the same throughout.

So this page has two jobs. First, let you recognise any old name you meet in a blog post, a tutorial or a console screen. Second, show you the layer map, so you know which product does what.

> **Module, not a lab.** Nothing here needs running.

---

## The Rename Chain in Brief

- The enterprise search product has had **six names since 2023**. The current one is **Agent Search**, from **22 April 2026**.
- Under all six sits one API that never moved: `discoveryengine.googleapis.com`. Check the endpoint, not the brand.
- The commerce product also collected six names, ending at **AI Commerce Search** on **29 June 2026**. Its endpoint is still `retail.googleapis.com`.
- Vertex AI itself became the **Gemini Enterprise Agent Platform** on **22 April 2026**. The search rename was one row in a table of about 55.
- **Dialogflow CX and ES are both still supported.** Neither is formally deprecated. CX is in maintenance, and its console was retired on **31 October 2025**.
- **CX Agent Studio is not a renamed Dialogflow CX.** It is a new product built on ADK.
- **ADK, Agent Runtime and Agent Search are layers, not alternatives**: write, run, retrieve.
- This family has **no deprecations page**. Both candidate URLs return 404, so every deprecation below came from reading release notes.

---

## 1. Six names in three years

Here is the full chain for the enterprise search product, with Google's own wording at each step.

| Date | From → To | Google's wording |
|---|---|---|
| 29 August 2023 | Generative AI App Builder → **Vertex AI Search and Conversation** | *"Vertex AI Search and Conversation is the new product name for Generative AI App Builder."* |
| 9 October 2023 | Console and docs catch up | *"The Google Cloud console and the documentation at cloud.google.com have been updated to show the current product name for Vertex AI Search and Conversation."* |
| 24 April 2024 | → **Vertex AI Agent Builder** | *"…have been updated to show the current product name for Vertex AI Agent Builder. On the console, look for 'Agent Builder'."* |
| 2 April 2025 | → **AI Applications** | *"The Vertex AI Agent Builder product has been renamed AI Applications… The product functionality and endpoints remain the same."* |
| 2 October 2025 | → **Vertex AI Search** | *"The AI Applications product has been renamed as Vertex AI Search…"* |
| **22 April 2026** | → **Agent Search** | *"The Vertex AI Search product has been renamed as Agent Search…"* |

Google keeps a standing banner on the docs, listing the old names:

> *"Some of the former names include Vertex AI Search, AI Applications, Agent Builder, Vertex AI Search and Conversation, Enterprise Search, and Generative AI App Builder."*

Note that **Enterprise Search** appears in that list but never got its own dated rename note. It was an early informal name for the same thing.

### Unchanged Elements

The 2 April 2025 note says it plainly: *"The product functionality and endpoints remain the same."* That has held at every step. Google also admits the console lags behind:

> *"The user interface in the Google Cloud console is still referred to as Vertex AI Search and AI Applications"*

> *"The APIs still use the Discovery Engine API endpoints."*

The documentation URLs are still under `/generative-ai-app-builder/`, which is the **2023** name. So one page can carry the 2026 brand, sit at a 2023 URL, and show you a 2025 label in the console.

**The practical lesson: check the endpoint, not the brand.** If a tutorial calls `discoveryengine.googleapis.com`, it is about this product, whatever name the page uses.

---

## 2. Discovery Engine, the layer that never moved

`discoveryengine.googleapis.com` survived all six renames unchanged. The API surface is `google.cloud.discoveryengine.v1`.

It now backs **two** products at once:

| Product | Description |
|---|---|
| **Agent Search** | The builder-facing search and RAG product |
| **Gemini Enterprise** | The finished end-user assistant (formerly Agentspace) |

It also gained an **MCP server at `https://discoveryengine.googleapis.com/mcp`**, GA on **22 April 2026**. That lets an agent query your data stores through the Model Context Protocol.

> **Operational hazard.** Because one API backs two products, **disabling `discoveryengine.googleapis.com` tears down the resources of both**. Someone cleaning up unused APIs on a project can remove a Gemini Enterprise deployment by accident. Check what else uses it before you turn it off.

---

## 3. The commerce chain

The ecommerce product went through six names of its own, and merged two older products on the way.

| Date | From → To |
|---|---|
| 15 January 2021 | Recommendations Engine API → **Retail API** |
| 21 January 2022 | Console merges Recommendations AI and Retail Search |
| 12 March 2024 | → **Vertex AI Search for retail** |
| 10 January 2025 | → **Vertex AI Search for commerce** |
| 22 April 2026 | → **Agent Search for Commerce** |
| **29 June 2026** | → **AI Commerce Search** (in Gemini Enterprise for Customer Experience) |

The June 2026 note, quoted exactly, including Google's own typo:

> *"Vertex AI Search for commerce, which has been previously known under the mame [sic] Retail Search, has been rebranded to AI Commerce Search in Gemini Enterprise for Customer Experience."*

### A contradiction in the 2026 notes

The April 2026 Agent Platform rename table assigned this product the name **Agent Search for Commerce**. Ten weeks later, the June note moved it out of Agent Platform entirely, into the Customer Experience suite as **AI Commerce Search**. So the April name had a very short life. It is unverified whether it was ever used outside that one table.

### Recommendations AI and Retail Search are not separate products

This trips up older material. Both names still appear in tutorials as if they were two services you buy separately. They are not. They are the **recommendations half** and the **search half** of one product. One catalog, one event stream, one API: `retail.googleapis.com`, unchanged since 2021.

---

## 4. The platform rename, 22 April 2026

On that date, **Vertex AI** became the **Gemini Enterprise Agent Platform**. The Vertex AI release notes now carry a tombstone:

> *"Vertex AI documentation is no longer being updated. Vertex AI's services are now part of Gemini Enterprise Agent Platform."*

The rename table has roughly 55 rows. Some of the ones you will meet most:

| Vertex AI name | Agent Platform name |
|---|---|
| Vertex AI Platform / Vertex AI | **Agent Platform** |
| Vertex AI Search | **Agent Search** |
| Vertex AI Conversation | **Agent Conversation** |
| **Vertex AI Agent Engine** | **Agent Runtime** |
| **Vertex AI Vector Search 2.0** | **Agent Retrieval** |
| Vertex AI Studio | **Agent Studio** |
| Vertex AI RAG Engine | **RAG Engine** |

This is the useful context for §1. The move from Vertex AI Search to Agent Search was **one row in a platform-wide table**. It was not a decision about the search product. Everything with "Vertex AI" in front of it lost that prefix on the same day, and most gained "Agent" instead.

### Agentspace became Gemini Enterprise

Six months earlier, on **9 October 2025**:

> *"The Google Agentspace experience in the Google Cloud console and the default application is referred to as Gemini Enterprise. This includes all associated resources and documentation."*

A sibling product moved with it: **NotebookLM Enterprise → Gemini Notebook Enterprise**.

Agentspace launched around **December 2024**. Treat that date as approximate. The earliest release note I could find is **31 January 2025**, so the launch date is unverified.

---

## 5. Product Roles and Functions

### Agent Search

Three things: enterprise search over your own content, recommendations, and grounded generative answers.

The core concepts have not changed since 2023, which helps when you read old tutorials.

| Concept | Description |
|---|---|
| **Data store** | The indexed corpus. Your documents, websites, or structured records. |
| **App** (also called an engine) | The thing you query. It attaches to one or more data stores. |

Those two were separated into distinct entities in **August 2023**, and the split has held ever since. An old tutorial that talks about data stores and apps is still describing the current model.

Verticals available: **custom** (vertical-agnostic), **media**, **healthcare**, plus **custom recommendations** in Preview. See §8 on healthcare, which is now deprecated.

### Choosing a RAG path

Agent Search is the managed, batteries-included route to retrieval-augmented generation. It is not the only sanctioned one. Google's own healthcare deprecation note frames the choice cleanly:

> *"custom search apps on Agent Search"* … *"or, if you require fine-grained control over the underlying retrieval mechanisms and are prepared for a more customer-managed integration, use Agent Retrieval."*

There is a third route. **RAG Engine** treats the backend as pluggable, and accepts Agent Platform Search, Agent Retrieval, Vector Search, Feature Store, Weaviate or Pinecone.

So the short rule:

- **Agent Search** = the default managed RAG path. Less control, much less work.
- **Agent Retrieval** = the control-oriented alternative, when you need to tune retrieval yourself.
- **RAG Engine** = the middle layer, when you want to swap backends later.

### AI Commerce Search

Search, browse and recommendations over an ecommerce catalog. You ingest two things: a **product catalog** and a **user-event clickstream**.

The difference from general search is the ranking objective. It optimises for relevance **and revenue** together. General enterprise search has no reason to care about the second.

One practical detail: a single data feed serves both search and recommendations. You do not maintain two pipelines.

It also has a **Merchandising console** with Creator and Approver governance roles, added in **November 2025**. A merchandiser can propose a ranking change, and someone else approves it.

---

## 6. Dialogflow and Contact Center AI

### Dialogflow is supported, not deprecated

**Dialogflow CX and Dialogflow ES are both still documented and supported.** Neither is formally deprecated. This is easy to get wrong, because the surrounding brands moved so much.

CX is branded **"Conversational Agents (Dialogflow CX)"** in the docs. It is in maintenance mode. After **11 December 2025** the only release note is a security fix, dated **7 May 2026**.

The **Dialogflow CX console was deprecated on 31 October 2025**. Users are now routed automatically to the Conversational Agents console.

ES remains the documented "standard agent type" for small-to-medium applications, and there is a published ES → CX migration path.

### CX Agent Studio is a successor, not a rename

The successor product is **CX Agent Studio** (Customer Experience Agent Studio). Be precise about what it is. Its docs say it *"represents the evolution of Dialogflow CX"* and that it *"is built on Agent Development Kit (ADK)"*.

So it is a **new product on a new foundation**. It sits beside Dialogflow rather than relabelling it. If you migrate, you are moving to ADK, not renaming an existing agent.

### Contact Center AI is now Gemini Enterprise for Customer Experience

The docs still live at `/customer-engagement-ai`. The suite contains CX Agent Studio, Agent Assist, CX Insights and the commerce agents.

| Product | Status |
|---|---|
| **Agent Assist** | Name unchanged. Actively developed. |
| **CCAI Insights → Conversational Insights → Customer Experience Insights (CX Insights)** | Renamed **12 January 2026**. Includes Quality AI. |
| **CCAI Platform** | **Name unchanged.** Still "Contact Center AI Platform" under "Google Cloud CCaaS". |

The CX Insights rename note, quoted:

> *"This product has a new name. The same product with the same features is now called Customer Experience Insights, or CX Insights for short."*

**CCAI Platform is the odd one out.** It sat out the rebrand completely and kept its name. It is also the most actively shipping product in the family, with release notes dated **25 August 2026**.

---

## 7. ADK, Agent Runtime, and how the layers fit

### ADK, the Agent Development Kit

An open-source agent framework in **Python, TypeScript, Go and Java**. You use it to build, debug, evaluate and deploy agents.

- Workflow agents for deterministic pipelines, or dynamic LLM-driven routing.
- Native multi-agent composition, so agents can call other agents.
- Deploy on your own infrastructure, or on Agent Runtime, Cloud Run, or GKE.

ADK is healthy and current, with docs updated **24 August 2026**. It has become the substrate other Google products are built on, including CX Agent Studio.

### Agent Runtime, renamed twice

| Date | Change |
|---|---|
| **4 March 2025** | *"LangChain on Vertex AI has been renamed to Vertex AI Agent Engine"*, announced the same day it went GA |
| **22 April 2026** | Vertex AI Agent Engine → **Agent Runtime** |

It is the managed serverless runtime for deployed agents. What it gives you:

- Sub-second cold starts, and under a minute to provision.
- Long-running operations up to **7 days**.
- Custom containers.
- **Agent Gateway** for egress control.
- An IAM agent identity, so the agent has its own principal.

It runs agents written with ADK, A2A, LangChain, LangGraph, AG2, LlamaIndex, or your own code. Three companion services were renamed with it: Agent Platform **Sessions**, **Memory Bank** and **Code Execution**.

### About "formerly Reasoning Engine"

You will see this claim often. Handle it carefully.

No dated release note announces a Reasoning Engine → Agent Engine rename. The only documented rename is **LangChain on Vertex AI → Vertex AI Agent Engine**. So treat the date as unverified.

The name is provably alive in the API, though. The current v1 REST surface is:

```
projects.locations.reasoningEngines
  .sessions
  .memories
  .runtimeRevisions
  .sandboxEnvironments
```

The original preview name survived three product renames inside the API. That is a compact illustration of this page's main lesson.

### The layer map

```
Gemini Enterprise  (umbrella brand)
│
├─ Gemini Enterprise  — the end-user app (ex-Agentspace)
│    the assistant employees use; Discovery Engine API
│
├─ Gemini Enterprise Agent Platform  (ex-Vertex AI) — the builder's platform
│    ├─ ADK ............... how you WRITE an agent (open source, 4 languages)
│    ├─ Agent Runtime ..... where you RUN it (ex-Agent Engine, ex-LangChain
│    │                       on Vertex AI; API: reasoningEngines)
│    ├─ Agent Search ...... what it RETRIEVES from (Discovery Engine API)
│    ├─ Agent Retrieval ... low-level retrieval (ex-Vector Search 2.0)
│    └─ Agent Studio, Model Garden, RAG Engine, Inference, ...
│
└─ Gemini Enterprise for Customer Experience  (ex-CCAI)
     ├─ CX Agent Studio ... built ON ADK; evolution of Dialogflow CX
     ├─ Agent Assist ...... human-agent assistance
     ├─ CX Insights ....... ex-CCAI Insights (2026-01-12)
     └─ AI Commerce Search  ex-Retail Search + Recommendations AI

Dialogflow CX / ES — alongside, supported, feature-frozen. CX console retired
                     2025-10-31 -> Conversational Agents console.
CCAI Platform (CCaaS) — untouched by the rebrand, actively shipping.
```

Four points to take from that diagram:

1. **ADK, Agent Runtime and Agent Search are layers, not alternatives.** You write with ADK, run on Agent Runtime, and retrieve from Agent Search. Picking one does not rule out the others.
2. **Dialogflow is the previous generation** of the conversational layer. Supported, but frozen.
3. **CX Agent Studio is its ADK-based replacement**, and a separate product.
4. **Gemini Enterprise is the finished app you buy** rather than build. Everything under Agent Platform is for building.

---

## 8. Deprecations

| Date | Item | Status |
|---|---|---|
| 26 May 2026 | Gemini Enterprise assist feature | Deprecated and shut down. Already gone. |
| 20 May 2026 | NotebookLM Enterprise Podcast API | Deprecated. No new allowlisting. |
| **15 May 2026** | **Agent Search for healthcare** | Deprecated. Migrate to custom search apps on Agent Search, or to Agent Retrieval. **No shutdown date given.** |
| 26 March 2026 | Gemini 3 Pro (Preview) for answer generation | Discontinued. Upgrade to Gemini 3.1 Pro (Preview). |
| 1 April 2026 | Agent Assist Article Suggestion and FAQ Assist | Permanent removal. Move to Generative knowledge assist. |
| 31 October 2025 | Dialogflow CX console | Deprecated. Auto-redirect to the Conversational Agents console. |
| October 2025 | Agent Assist Smart compose | Permanently removed. Move to Generative smart reply. |

Plan around the healthcare row first. It is deprecated with **no shutdown date**, so there is no deadline to work back from. The migration is not a version bump either. You rebuild on a custom search app or on Agent Retrieval.

**AI Commerce Search has no deprecations at all** in its release notes. For a product renamed six times, its surface has been remarkably stable.

### There is no deprecations page

Both of the obvious URLs return 404:

```
/generative-ai-app-builder/docs/deprecations
/gemini-enterprise-agent-platform/docs/deprecations
```

So the table above was built by reading release notes end to end. This matters for you as a reader. There is no single page to check to stay current, and a deprecation can appear in a release note you never see.

---

## 9. Unverified Claims

Four things in this module are unconfirmed. They are marked in place, and collected here.

| Item | Missing Documentation |
|---|---|
| **Reasoning Engine → Agent Engine** | No dated release note announces this rename. Only the LangChain on Vertex AI rename is documented. |
| **"Customer Engagement Suite with Google AI" → "Gemini Enterprise for Customer Experience"** | The new name is live across the docs, but no dated announcement exists. It falls between **12 January 2026** and **29 June 2026**. |
| **Agentspace launch** | Around **December 2024**. The earliest release note is **31 January 2025**. |
| **"Agent Search for Commerce"** | Unclear whether it was ever used outside the April 2026 rename table. |

---

## 10. Related Modules and Further Reading

- [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md) — the hub, with the short version of these rename tables
- [Document AI and text APIs](AI-API-DOCUMENT-AND-TEXT.md) — Layout Parser and the chunking that feeds RAG
- [IAM and service accounts](../../data-eng-gcp/modules/IAM-AND-SERVICE-ACCOUNTS.md) — the agent identity Agent Runtime gives you

---

## Six Renames, One Endpoint

The enterprise search product has been renamed six times since 2023, from Generative AI App Builder to Vertex AI Search and Conversation, Vertex AI Agent Builder, AI Applications, Vertex AI Search, and now **Agent Search**. Through all of it, `discoveryengine.googleapis.com` never changed, the console still shows older labels, and the docs still sit at a 2023 URL, so identify the product by its endpoint rather than its brand. The same pattern runs through the commerce product, which reached **AI Commerce Search** on 29 June 2026 while keeping `retail.googleapis.com` since 2021, and which merged Recommendations AI and Retail Search into one service years ago. The 2026 search rename was a single row in a platform-wide table when Vertex AI became the **Gemini Enterprise Agent Platform**, so read it as branding rather than product change. On the conversational side, **Dialogflow CX and ES are both still supported but frozen**, and their successor **CX Agent Studio is a new ADK-based product** rather than a rename. Keep the layer map above: **ADK writes an agent, Agent Runtime runs it, Agent Search retrieves for it**, with Agent Retrieval as the lower-level option and Gemini Enterprise as the finished app you buy. Deprecations are scattered, since this family has no deprecations page, and the largest open one is **Agent Search for healthcare**, deprecated on 15 May 2026 with no shutdown date.

---

## Source Pages for This Module

- [Agent Search introduction](https://docs.cloud.google.com/generative-ai-app-builder/docs/introduction)
- [AI Commerce Search documentation](https://docs.cloud.google.com/retail/docs)
- [Dialogflow documentation](https://docs.cloud.google.com/dialogflow/docs)
