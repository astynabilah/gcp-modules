# What AI APIs are in Google Cloud?

Google sells a set of **pretrained AI APIs**: models it has already trained, that you call over HTTP and pay for per request. You bring no training data and no model. You send an image, an audio file, a document or a sentence, and you get structured JSON back.

This page is the map. It answers the five questions once, then sends you to a detailed module.

> **Module, not a lab.** Nothing here needs running.

---

## The Short Version

- There are about **eight** of these APIs still worth learning, grouped into vision, speech and language, documents, and search.
- They are **not deprecated in favour of Gemini**. Google has never published a page telling anyone to migrate off them.
- They are, however, **frozen**. Natural Language API has had no release note since **August 2023**; Video Intelligence none since **November 2021**.
- The one being actively developed is **Document AI**, and its newest parsers run on Gemini underneath.
- Almost every product in this area was **renamed between 2024 and 2026**, some three or four times. §6 is the rename map.
- Four products here are **already switched off**, two more go dark in **September 2026**, and three vanished with no announcement at all. See §7.

---

## 1. Pretrained AI APIs, Defined

A normal ML project has four costs: collecting data, labelling it, training, and serving. A pretrained API removes all four. Google trained the model on its own data and runs it on its own hardware. You call it.

```
Your app  --(image bytes)-->  Cloud Vision API  --(JSON: labels, text, faces)-->  Your app
```

The trade is fixed capability. The Vision API detects the things Google chose to detect. If you need "is this specific weld defective", no pretrained API will do it, because Google has never seen your welds.

This puts the APIs at one end of a range:

| Option | You supply | You control | Effort |
|---|---|---|---|
| **Pretrained API** | Nothing | Nothing | Minutes |
| **Gemini with a prompt** | A prompt | The instructions | Hours |
| **AutoML** | Labelled data | The label set | Days |
| **Custom training** | Data, model code | Everything | Weeks |

The habit worth building is trying these left to right, rather than reaching for the most capable option first. [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md) covers the full range.

---

## 2. Why They Still Exist Next to Gemini

Gemini can read an image, transcribe audio and classify text. So can these APIs. It is a fair question why both exist.

Google is quiet about this. The clearest statement is in the Gemini API documentation, not the Cloud documentation:

> *"Gemini can reduce the need to use specialized ML models depending on your quality and performance requirements."*

On the Cloud side, the comparison table on the Vision product page describes the Vision API as *"Quick and easy integration of basic vision features"*. That is a pitch about cost and simplicity, not a deprecation.

Three practical reasons to still pick an API:

1. **Price.** Vision API gives you 1,000 units a month free, then charges per unit. A Gemini call that reads the same image costs tokens in and tokens out.
2. **Shape of the output.** `analyzeEntities` returns a typed list. A language model returns text that you then have to force into a schema.
3. **Data residency.** Some pretrained endpoints are regional. Several of the new Gemini-backed processors are not, and Google flags this in writing: *"This processor version uses the Vertex AI Gemini global endpoint and is not compliant with Data Residency (DMZ) standards."*

**Be careful here.** The comparison above is my reasoning, not Google's recommendation. I looked for an official "API versus Gemini" guidance page and there is none. What Google has done instead is structural: Text-to-Speech now labels its old voices **"Legacy TTS models"**, the flagship translation model is Gemini-derived, and Document AI's newest parsers run on Gemini 3. The direction is visible in the product decisions rather than in any announcement.

---

## 3. Who Each One Is For

| API | Answers the question | Typical caller |
|---|---|---|
| **Cloud Vision API** | What is in this image? | Any app with user uploads |
| **Video Intelligence API** | What happens in this video file? | Media archives, moderation |
| **Speech-to-Text** | What was said in this audio? | Call centres, captioning |
| **Text-to-Speech** | Read this text aloud | IVR, accessibility |
| **Cloud Translation** | Say this in another language | Localisation pipelines |
| **Natural Language API** | What is this text about, and is it positive? | Review and ticket triage |
| **Document AI** | Pull the fields out of this form | Invoice and ID processing |
| **Agent Search** | Search across my company's own documents | Internal search, RAG |

---

## 4. When to Use One

Use a pretrained API when **all** of these hold:

- The task is a standard one, described in general terms (detect text, transcribe speech, translate).
- You have no labelled training data, and no plan to collect any.
- You want a fixed price per call rather than a model to operate.
- The output shape Google returns is close enough to what you need.

Choose something else when:

| Situation | Use instead |
|---|---|
| The categories are specific to your business | AutoML, or Gemini with a prompt |
| You need one call to do several things at once | Gemini |
| You need to reason about the content, not just label it | Gemini |
| The task is tabular prediction | [BigQuery ML](LOW-CODE-AI-ON-GCP.md) |
| You need the model on a device with no network | AutoML Edge export |

---

## 5. The Call Pattern

The pattern is the same across all of them.

1. **Enable the API** on the project. Each has its own service name, such as `vision.googleapis.com`.
2. **Authenticate.** A service account with the right role, or Application Default Credentials during development. See [IAM and service accounts](../../data-eng-gcp/modules/IAM-AND-SERVICE-ACCOUNTS.md).
3. **Send the payload.** Either inline bytes (base64) for small inputs, or a Cloud Storage URI for large ones.
4. **Choose sync or batch.** Synchronous calls have size and page limits. Batch calls read from Cloud Storage and write results back to Cloud Storage.
5. **Read the JSON.**

Two limits catch people out. **Inline payloads are capped**, so anything large has to go through Cloud Storage first. And **the free tier is monthly**, not one-off, so a test that fits inside it today can bill next week.

---

## 6. The rename map

This causes the most confusion, because the names changed far faster than the products did.

**The platform.** On **22 April 2026**, Vertex AI became the **Gemini Enterprise Agent Platform**. Vertex AI Studio became **Agent Studio**, the Vertex AI API became the Agent Platform API, and Agent Engine became **Agent Runtime**.

**The search product**, which holds the record. Google's own release notes admit the mess:

> *"Some of the former names include Vertex AI Search, AI Applications, Agent Builder, Vertex AI Search and Conversation, Enterprise Search, and Generative AI App Builder."*

| Date | Became |
|---|---|
| 29 August 2023 | Generative AI App Builder → **Vertex AI Search and Conversation** |
| 9 October 2023 | Console and docs catch up with that name |
| 24 April 2024 | → **Vertex AI Agent Builder** |
| 2 April 2025 | → **AI Applications** |
| 2 October 2025 | → **Vertex AI Search** |
| 22 April 2026 | → **Agent Search** |

Through all five renames, **the API endpoints never changed**. They are still Discovery Engine endpoints. This is the general rule in this area: marketing names move, API names do not.

**The commerce product**, which merged two older ones:

| Date | Became |
|---|---|
| 15 January 2021 | Recommendations Engine API → **Retail API** |
| 21 January 2022 | Console merges Recommendations AI and Retail Search |
| 12 March 2024 | → **Vertex AI Search for retail** |
| 10 January 2025 | → **Vertex AI Search for commerce** |
| 22 April 2026 | → **Agent Search for Commerce** |
| 29 June 2026 | → **AI Commerce Search in Gemini Enterprise for Customer Experience** |

The endpoint is still `retail.googleapis.com`. So Recommendations AI and Retail Search both survive, merged and renamed twice.

**Smaller renames to know:**

- Vertex AI Vision → **Agent Platform Vision** (and now deprecated, see §7)
- CCAI Insights → **Customer Experience Insights**
- Dialogflow CX → documented as **Conversational Agents (Dialogflow CX)**; the old CX console is labelled a *"Deprecated user interface"*
- Vector Search 2.0 → **Agent Retrieval**
- Agentspace → **Gemini Enterprise** (9 October 2025)
- LangChain on Vertex AI → Vertex AI Agent Engine (4 March 2025) → **Agent Runtime** (22 April 2026)
- Document AI Receipt Parser → **Expense Parser**

---

## 7. What's Dead, and What Dies Soon

**Switched off already:**

| Product | Deprecated | Shut down |
|---|---|---|
| Media Translation API | 30 June 2023 | **1 July 2024** |
| AutoML Translation | 16 September 2024 | **30 September 2025** |
| Healthcare Natural Language API | 27 May 2025 | **27 May 2026** |
| Document AI legacy processors | 17 February 2026 | **30 June 2026** |

That last one removed a long list of parsers: W-9, the 1099 family, 1120, US Passport, mortgage statement, utility, and the procurement and lending splitters. Only **W-2** survives from the tax group. Migration was by processor version, not by product.

**Dying now:**

| Product | Deprecated | End of life |
|---|---|---|
| **Vertex AI Vision** / Agent Platform Vision | 15 June 2026 | **30 September 2026** |
| **Translation Hub** | 30 June 2025 | **20 September 2026** |

Google's wording on the first, quoted exactly:

> *"Vertex AI Vision is deprecated as of June 15, 2026 and reaches End of Life on September 30, 2026. To migrate, see the Cloud Vision API, Agent Platform serverless training, or Agent Platform models."*

Both dates are close. If you meet either product in older material, treat it as history.

**Gone without an announcement.** Three products vanished with no deprecation notice that I could find: **Visual Inspection AI** (its page now redirects to Model Garden), **Timeseries Insights API** (every documentation URL returned 404 between late January and early February 2026), and **Text-to-Speech Journey voices**. For these the shutdown is *inferred from the documentation disappearing*, not confirmed by Google. Search engines still return their old pages, which makes this easy to get wrong.

**Alive but dormant.** Cloud Talent Solution still works and is still priced, but its last release note was December 2024 and its pricing page has not moved since 2021.

---

## 8. The Detailed Modules and Related Reading

| Module | Covers |
|---|---|
| [Vision and video APIs](AI-API-VISION-AND-VIDEO.md) | Cloud Vision, Product Search, Video Intelligence, and the Agent Platform Vision shutdown |
| [Speech and translation APIs](AI-API-SPEECH-AND-TRANSLATION.md) | Speech-to-Text v1 vs v2, the Chirp models, Text-to-Speech voice tiers, Translation Basic vs Advanced |
| [Document AI and text APIs](AI-API-DOCUMENT-AND-TEXT.md) | The processor gallery, Layout Parser and RAG chunking, Natural Language API |
| [Search and conversation](AI-API-SEARCH-AND-CONVERSATION.md) | Agent Search, commerce search, Dialogflow, and how the agent products fit together |

Related reading:

- [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md) — where these APIs sit next to AutoML and BigQuery ML
- [Choosing specs](CHOOSING-COMPUTE-SPECS.md) — when a task needs your own hardware instead

---

## The Map in One Paragraph

Google Cloud's pretrained AI APIs are models you rent by the call. Their appeal is that you supply no data and operate no infrastructure; their limit is that you cannot change what they detect. Roughly eight remain relevant, split across vision, speech and language, documents, and search. None has been formally deprecated in favour of Gemini, and no Google page recommends migrating away from them. Most are frozen, though, with Natural Language untouched since 2023 and Video Intelligence since 2021. Document AI is the exception and is developed actively, with its newest parsers running on Gemini. The bigger hazard is naming: the search product was renamed five times between 2023 and 2026 while its API endpoints stayed identical, so always check the endpoint rather than the brand. Four products have already been switched off, two more go dark in September 2026, and three disappeared without any notice at all.
