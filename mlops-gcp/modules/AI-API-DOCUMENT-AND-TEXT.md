# Document AI and text APIs

Two products sit at opposite ends of Google's attention span. **Document AI** ships release notes every few months. The **Natural Language API** has not had one since 2023. This page covers both.

> **Module, not a lab.** Nothing here needs running.

---

## Key Facts on Both APIs

- **Document AI kept its name.** No rename, no fold into Gemini. Latest release note: **2026-07-17**. Docs updated **2026-08-13**.
- The processor gallery is now **13 processors**, all GA. Everything else was removed on **30 June 2026**.
- **Document AI Workbench is gone as a brand.** Custom Extractor, Classifier and Splitter are ordinary processors now.
- Training a Custom Extractor has **three paths**: foundation model, conventional custom model, or up-training.
- **Layout Parser** exists for RAG. Its `ChunkingConfig` has exactly two fields, and **overlap is not one of them**.
- Google's own pages **contradict each other** in several places here, and **the pricing page is stale**. Each case is flagged below.
- **No page compares Document AI to Gemini.** None compares Natural Language to Gemini either. §10 covers what Google does and does not say.
- **Natural Language API** is frozen but alive. v2 drops **two** methods, not one, and its status has been unstated since 2023.
- **Healthcare Natural Language API** shut down on **27 May 2026**.

Start at [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md) if you have not read the map yet.

---

# Part 1 — Document AI

## 1. Document AI Overview

You send a PDF, an image or an office file. You get back structured JSON: text, layout, key-value pairs, or named fields like `invoice_id` and `total_amount`.

The unit of work is a **processor**. A processor is an endpoint you create in a project and a location, with a type ID and a version. You call it, you pay per page, and Google runs the model.

Google describes the product like this on the overview page:

> *"Document AI is built on top of products within Vertex AI with generative AI…"*

The RAG Engine page carries the same sentence with a different product name in it: **Gemini Enterprise Agent Platform** instead of Vertex AI. The 22 April 2026 rebrand is still rolling through the documentation, so both wordings are live at once. Google has not resolved this. Read either one as "the newer processors run on Gemini underneath".

---

## 2. The Processor Gallery

This is the complete current gallery. All of these are GA.

| Processor | Type ID |
|---|---|
| Enterprise Document OCR | `OCR_PROCESSOR` |
| Form Parser | `FORM_PARSER_PROCESSOR` |
| Layout Parser | `LAYOUT_PARSER_PROCESSOR` |
| Custom Extractor | `CUSTOM_EXTRACTION_PROCESSOR` |
| Custom Classifier | `CUSTOM_CLASSIFICATION_PROCESSOR` |
| Custom Splitter | `CUSTOM_SPLITTING_PROCESSOR` |
| Invoice Parser | `INVOICE_PROCESSOR` |
| Expense Parser (**formerly Receipt Parser**) | `EXPENSE_PROCESSOR` |
| Bank Statement Parser | `BANK_STATEMENT_PROCESSOR` |
| Pay Slip Parser | `PAYSTUB_PROCESSOR` |
| W2 Parser | `FORM_W2_PROCESSOR` |
| US Driver License Parser | `US_DRIVER_LICENSE_PROCESSOR` |
| Identity Document Proofing | `ID_PROOFING_PROCESSOR` |

They fall into three groups.

- **General**: OCR, Form Parser, Layout Parser. They work on any document and know nothing about your fields.
- **Specialized**: Invoice, Expense, Bank Statement, Pay Slip, W2, US Driver License, ID Proofing. Google trained these on one document type and named the fields for you.
- **Custom**: Extractor, Classifier, Splitter. You supply labelled documents.

A note on naming. **Document Quality is not a processor.** It is an add-on to Enterprise Document OCR, switched on with `OcrConfig.enableImageQualityScores`, and billed as an OCR add-on. Looking for it in the gallery is a dead end.

---

## 3. The 30 June 2026 Discontinuation

The release notes dated **2026-02-17** put it plainly:

> *"Document AI legacy processors will be discontinued on June 30, 2026. To preempt the risk of service failure while using legacy processors, we recommend transitioning to more stable, higher-quality processors."*

Removed in that cull:

- **US Passport Parser** and **FR Driver License Parser**
- The **whole tax family**: `pretrained-1099misc`, `1099nec`, `1099r`, `1099int`, `1099g`, `ssa1099`, `1120`, and all `w9` versions
- **Mortgage Statement** and **Utility** parsers
- The **procurement** and **lending splitters**
- The **Summarizer** (`pretrained-foundation-model-v1.0-2023-08-22`)

**Only W-2 survives from the tax group.** If older material tells you to reach for the 1099 or W-9 parser, that advice is dead.

One detail changes how you read this. **Migration was by processor version, not by product.** Your processor may still exist while the version it points at does not.

Google labels 30 June 2026 two different ways. The deprecations page puts it in a column headed **"Deprecated date"**. The release note calls it the **discontinuation** date. Those mean different things. The date has now passed and the processors are absent from the catalogue, so read them as already shut down.

Google named these targets:

| From | Move to |
|---|---|
| OCR | `pretrained-ocr-v2.1-2024-08-07` |
| Expense | `pretrained-expense-v1.3.2-2024-09-11` |
| Invoice | `pretrained-invoice-v2.0-2023-12-06` |
| Pay slip | `pretrained-paystub-v3.0-2023-12-06` |
| Bank statement | `pretrained-bankstatement-v5.0-2023-12-06` |
| Custom classifier | `pretrained-classifier-v1.5-2025-08-05` |
| Custom splitter | `pretrained-splitter-v1.5-2025-07-14` |

### The pricing page was never cleaned up

This is the trap. The pricing page still lists processors that no longer exist:

- **Utility parser**
- **Procurement splitter**
- **Lending splitter**
- **US passport parser**
- **Summarizer** (`pretrained-foundation-model-v1.0-2023-08-22`), still showing **$0.025**

All five were removed from the catalogue and are covered by the 30 June 2026 discontinuation. So the Summarizer contradiction has a dull explanation: the price row is stale, not a sign that the processor survived.

**Do not budget from the pricing page alone.** Cross-check every row against the processor list before you plan a workload.

### Two dates for Custom Extractor v1.4

The release notes give the end date as **5 February 2026**. The deprecation table gives **31 March 2026**. Two Google pages, two dates, no correction on either. If you are planning a migration, use the earlier date and check the console.

---

## 4. Document AI Workbench, Retired as a Brand

It went away as a brand.

- `/document-ai/docs/workbench` returns **404**.
- "Workbench" appears **0 times** in the documentation navigation.
- It survives only as a label in the console navigation.

Custom Extractor, Custom Classifier and Custom Splitter are now first-class processors in the gallery, all GA. You create them the same way you create an Invoice Parser. Nothing was removed here, only the wrapper name.

The rename left visible damage. A botched find-and-replace is still live on the training page, with the doubled text intact:

> *"Here are some instances in which you might want to consider options besides Document AI **Document AI Workbench**, or adapt your workflow."*

That is evidence the brand is being scrubbed from the text rather than relocated to a new page.

This matters when reading older tutorials. Anything that tells you to "open Workbench and create a processor" now means "create a custom processor".

---

## 5. Training a Custom Extractor

There are three routes, and the console makes you choose between them.

### GenAI / foundation model

The default now. It scales with how much labelled data you have.

| Stage | Documents |
|---|---|
| **Zero-shot** | 0 |
| **Few-shot** | 5–10 |
| **Fine-tuning** | 10–50+ |

Fine-tuning knobs: **100–400 training steps**, a **learning-rate multiplier of 0.1–10**, and a **72-hour job timeout**.

Zero-shot is the reason to start here. You define the schema, you label nothing, and you get output. If quality is short, you add examples.

### Custom non-genAI model

The older approach. The console warns you what you are picking:

> *"will train a conventional non-Generative AI based model"*

and describes the alternative as:

> *"Fine-tuning will tune a foundation model, which is recommended"*

Google is steering you to the foundation model, in the interface rather than in an announcement.

### Up-training

Taking a pretrained processor and improving it on your documents. Google explains the mechanism:

> *"Up training works by applying transfer learning on Google pretrained processor versions and generally requires less data than training from scratch."*

It is **available only for pretrained and specialized processors**. Custom processors cannot use it, and Google says why:

> *"Unlike other processors, custom processors don't come with any pretrained processor versions and thus, cannot process any documents until you train a version from scratch."*

So a fresh Custom Extractor does nothing at all until you train a version. A specialized parser works on day one.

### The schema cap

A custom processor schema holds at most **150 entity labels**. That is generous for an invoice and tight for a long contract. Check it before designing a schema with one label per clause.

### Foundation model versions

| Version | Model | Stage |
|---|---|---|
| `v1.5-2025-05-05` | Gemini 2.5 Flash | GA |
| `v1.5-pro-2025-06-20` | Gemini 2.5 Pro | GA |
| `v1.6-pro-2025-12-01` | Gemini 3 Pro | Preview |
| `v1.6-2026-01-13` | Gemini 3 Flash | Preview |
| `v3.5-2026-05-26` | Gemini 3.5 Flash | Preview |

Note the jump from `v1.6` to `v3.5`. The processor version now tracks the Gemini model number instead of its own sequence. Sorting these strings will not give you release order.

### The data residency warning

Google attaches this to the Gemini-backed versions:

> *"This processor version uses the Vertex AI Gemini global endpoint and is not compliant with Data Residency (DMZ) standards."*

If your documents carry a residency requirement, the newest and best processor versions are closed to you. Stay on a regional version instead.

---

## 6. Layout Parser and RAG

For search and RAG. Its documentation page is now titled **"Process documents with Gemini layout parser"**, and states the problem directly:

> *"It's designed to solve a critical problem for Search and Retrieval Augmented Generation (RAG): standard OCR flattens documents, destroying the very context and structure that adds valuable meaning."*

A heading, a table cell and a footnote all come back as plain text from OCR. Layout Parser keeps the structure. Google spells out the effect on chunks:

> *"Standard parsers often create chunks removed from their original context, separating a paragraph from its heading. Gemini layout parser understands the document's hierarchy. It creates context-aware chunks that include content from ancestral headings and table headers."*

The pipeline has three stages:

1. **Parse and Structure** — find blocks, headings, tables and lists.
2. **Annotate and Verbalize** (Preview) — describe images and tables in words so they can be embedded.
3. **Chunk and Augment** — split into chunks and attach the **ancestral headings** to each one.

Stage 3 is the useful part for RAG. A chunk that reads "must be replaced every 400 hours" means nothing on its own. With its parent headings attached, it becomes searchable.

### GA status is layered

| Piece | Stage |
|---|---|
| Layout Parser processor | GA |
| `pretrained-layout-parser-v1.0-2024-06-03` | GA |
| PDF, HTML, DOCX, PPTX, XLSX, XLSM | GA since **2025-11-04** |
| Image and table annotations | GA since **2026-05-27** |
| Gemini-powered v1.5 and v1.6 versions | Preview |

So "Layout Parser is GA" is true and still not the full answer. Check the version and the file type.

The file-type split also decides your bill:

> *"Support for the file types HTML, PDF, DOCX, PPTX, XLSX and XLSM is in General Availability and is subject to charges."*

> *"Support for the other file types is offered without charge because those types are in preview."*

### Size limits

| Mode | Limit |
|---|---|
| Online | **20 MB**, **15 pages per PDF** |
| Batch | **1 GB**, **500 pages** |

These are tighter than the general 40 MB online limit in §8. Layout Parser has its own numbers.

### Two products point you here

Layout Parser is the recommended default in both of Google's RAG products.

Gemini Enterprise:

> *"The default parser for Gemini Enterprise is the Layout parser. It's generally the best choice because it detects and understands document hierarchy, which leads to better chunking and ultimately better answer generation and retrieval."*

RAG Engine:

> *"In the Layout parser section, select the Document AI layout parser option, which has the highest accuracy for documents with images or charts."*

### ChunkingConfig has two fields

```
ChunkingConfig
  chunkSize
  includeAncestorHeadings
```

That is the whole object. **There is no chunk-overlap field and no semantic-chunking field in the Document AI API.**

This surprises people who have used other chunking libraries. Overlap is a **RAG Engine** setting, not a Document AI one. RAG Engine's recommended corpus defaults are **chunk size 1024** and **overlap 256**.

Keep the two products separate in your head. Document AI produces chunks. RAG Engine decides how a corpus stores and overlaps them.

---

## 7. Pricing

Per **1,000 pages** unless the row says otherwise.

| Processor | Price |
|---|---|
| Enterprise Document OCR | First 1,000 pages **free**, then **$1.50**, then **$0.60** above 5,000,000 |
| OCR add-ons (including quality scores) | **$6.00** — v2 only |
| Form Parser | **$30.00**, dropping to **$20.00** above 1M |
| Custom Extractor | **$30.00**, dropping to **$20.00** above 1M |
| Layout Parser | **$10.00** |
| Layout Parser re-chunking | **$0.02** per 1,000 |
| Custom Splitter | **$5.00**, then **$3.00** |
| Custom Classifier | **$5.00**, then **$3.00** |

Specialized parsers are priced per **count**, where one count is up to 10 pages:

| Processor | Price |
|---|---|
| Invoice, Expense, US Driver License, ID Proofing | **$0.10** per count |
| Bank Statement | **$0.75** per classified document |
| Pay Slip | **$0.30** per classified document |
| W2 | **$0.30** per classified document |

Three things to hold on to.

**Hosting is billed separately.** A deployed custom processor version costs **$0.05 per hour**. That is roughly **$438 per year per deployed version**, whether or not you send it a single page. This catches people who leave test versions deployed.

**GenAI carries no premium.** Google states it directly:

> *"The cost to call the custom extractor is the same whether you use a generative AI-powered processor version or custom model."*

**Training is free.** Also stated directly:

> *"There is no cost for training or up-training. You pay for hosting and prediction."*

There is **no product-wide free tier** for Document AI. The only free usage is the first 1,000 OCR units. This differs from Vision and Natural Language, which have monthly free allowances.

---

## 8. Recent Changes

| Date | Change |
|---|---|
| **2025-04-02** | `imageless_mode` allows up to **30 pages** in an online request |
| **2025-06-19** | Online request max file size rose from **20 MB to 40 MB** |
| **2025-09-09** | Two service tiers: **provisioned** and **best-effort** |
| **2026-01-12** | **Document-level prompting** for custom processors |
| **2026-02-17** | Legacy processor discontinuation announced |
| **2026-07-17** | Latest release note |

The 40 MB limit is the one to remember day to day. It decides whether a file goes through an online call or has to be staged in Cloud Storage for batch processing.

---

## 9. HITL and Document AI Warehouse

Both were **deprecated on 16 January 2024**.

- **Human in the Loop (HITL)** routed low-confidence extractions to a human reviewer. Its documentation URL now **301-redirects to the deprecation page**.
- **Document AI Warehouse** stored and searched processed documents.

**No shutdown date was ever published for either.** Their status here is *inferred from the documentation being removed*, not confirmed by Google. Treat both as gone, and treat any tutorial that builds a review queue on HITL as history.

---

## 10. Document AI Versus a Gemini Prompt

Google gives you almost nothing here.

- The Gemini document-understanding page **does not mention Document AI once**, across 26 KB of text.
- `/document-ai/docs/choose-processor` returns **404**.
- No page compares the two, in either direction.

So there is no official guidance to follow. Google's position looks like absorption rather than competition: every new 2026 processor version **is** a Gemini model.

The closest thing to an argument comes from the Layout Parser page:

> *"Unlike pure LLM-based parsers that try to read text that isn't there, Gemini layout parser's foundation in advanced OCR grounds it in the document's actual content. This leads to significantly fewer hallucinations."*

> *"Competitor models will hallucinate values. Gemini layout parser correctly identifies values in images and tables."*

Read that carefully. It targets **third-party LLM parsers**, not Gemini itself. Google is not telling you to prefer Document AI over its own model. The point being made is about grounding: OCR reads pixels, and a language model predicts text. Document AI puts the OCR step first.

**Be careful here.** Anything beyond that quote is inference, mine or someone else's. The practical difference is output shape and price: Document AI returns typed fields at a fixed per-page rate, and a Gemini prompt returns text you have to validate. Google has not published that comparison.

One cross-reference does exist, running the other way. Document AI's training page sends text work elsewhere:

> *"Certain text-based input formats (.txt, .html, .docx, .md, and so forth) are not supported by Document AI... Consider other prebuilt or custom language processing offerings in Google Cloud, such as the Cloud Natural Language API."*

---

# Part 2 — Natural Language API

## 11. Natural Language API Status

It is still called the **Natural Language API**. No rename. It analyses text and returns typed JSON.

It is alive in a narrow sense:

- **No deprecation notice** anywhere in its documentation.
- **No "use Gemini instead" guidance** anywhere in its documentation.
- **No release note since 2023-08-28.**
- Yet its discovery document was republished at revision **`20260823`**.

So the machinery is maintained and the product is not. The docs still describe the models as **PaLM-based**, which tells you how long the text has sat untouched.

The API is neither deprecated nor defended. Google publishes no comparison against Gemini in either direction. The one cross-reference points inward, from Document AI's training page, and is quoted in §10.

---

## 12. Natural Language API Capabilities

Five methods matter.

| Method | Returns | Use it for |
|---|---|---|
| `analyzeEntities` | People, places, organisations, dates, numbers, with type and `salience` | Pulling structured facts out of free text |
| `analyzeSentiment` | A `score` (negative to positive) and `magnitude` (strength), per document and per sentence | Review triage |
| `classifyText` | Categories from Google's own taxonomy, with `confidence` | Ticket routing, content tagging |
| `moderateText` | Harm categories with confidence values | Content moderation |
| `annotateText` | Several of the above in one call | Cutting round trips |

Two fields decide most of the practical use.

**`salience`** is a field on `Entity`. It says how central that entity is to the document, not how confident the model is. A support ticket that names your product twice and a competitor once will rank your product higher on salience. This makes `analyzeEntities` useful for routing.

**`magnitude`** on sentiment is separate from `score`. A long document with strong praise and strong complaints averages to a neutral `score` but a high `magnitude`. Reading only the score hides that.

A third field is easy to put in the wrong place. **`probability` sits on `EntityMention`, not on `Entity`.** Google defines it:

> *"Probability score associated with the entity. The score shows the probability of the entity mention being the entity type. The score is in (0, 1] range."*

So it scores the type guess for one mention. It is not a salience replacement.

Typical jobs this fits: sorting reviews by sentiment before a human reads them, routing tickets by detected category, and screening user-submitted text before it is published.

---

## 13. V1 Versus V2

**Start with the status, because it is unclear.** The only status statement anywhere is the **2023-08-28** release note announcing Public Preview:

> *"The Natural Language API v2 is now available in Public Preview."*

No GA announcement ever followed. But the current v2 reference pages carry **no Preview badge either**. So Public Preview is the last thing Google said about v2, and nothing on the site asserts it today. Three years of unannounced limbo. Do not tell a colleague "v2 is Beta" as a fact; say the status was never updated.

**v1 has 7 methods. v2 has 5.** v2 drops **two**: `analyzeEntitySentiment` and `analyzeSyntax`. This is often reported as one dropped method, so count them yourself.

Field-level differences:

| | v1 | v2 |
|---|---|---|
| `Entity.salience` | Present | **Removed** |
| `wikipedia_url` in entity metadata | Present | **Removed** |
| `Document.language` | `language` | Renamed **`languageCode`** |
| `ClassificationCategory.confidence` | Present | Present |
| `ClassificationCategory.severity` | Absent | **Added** |
| `analyzeEntitySentiment` | Yes | No |
| `analyzeSyntax` | Yes | No |

The 2023 release note lists the changes in its own words:

> *"language field is now called 'language_code'. No salience field. No wikipedia_url as metadata. ... New probability score field is returned for all entities where NUMBER, PHONE_NUMBER, ADDRESS, PRICE, DATE will always be 1.0."*

That last clause matters. For those five types the probability is always `1.0`, so it carries no information. Filtering on it will not help.

**Why `analyzeEntitySentiment` was dropped.** It supports exactly **three languages: English, Japanese and Spanish**. A method that covers three languages is hard to keep in a general API, and v2 removed it rather than expanding it.

So the choice is real, not cosmetic. If you rely on `salience` for ranking, on `wikipedia_url` for entity linking, or on per-entity sentiment, **v1 is the version you need**. If you want the `severity` signal on classification, use v2.

There is a third option people forget. **`v1beta2` still exists and still has all 7 methods.** Its name says beta, and it has outlived the versions meant to replace it.

---

## 14. The Healthcare Natural Language API Shutdown

It is dead. Deprecated **27 May 2025**, shut down **27 May 2026**.

It extracted **diseases, medications, medical devices, procedures and clinical attributes** from clinical text, and mapped them to **RxNorm, ICD-10, MeSH and SNOMED CT**. Nothing in the general Natural Language API replaces that. Google's recommended alternative is quoted:

> *"you can use a Generally Available (GA) Gemini model on Vertex AI."*

That swaps a typed medical-ontology output for a prompt you have to write and validate yourself.

**One oddity to flag.** The shutdown banner still reads *"will be shut down"* in future tense, on a page updated **2026-08-11**. That is after the stated shutdown date. Google's pages do not resolve this. The date has passed, so read the tense as a stale template rather than a reprieve.

---

## 15. Common mistakes

**Looking for Document Quality in the processor list.** It is an OCR add-on, set with `OcrConfig.enableImageQualityScores`.

**Assuming your processor survived because the product did.** The June 2026 cull removed **versions**. Check the version your processor points at.

**Expecting a chunk-overlap setting in Document AI.** `ChunkingConfig` has `chunkSize` and `includeAncestorHeadings`. Overlap belongs to RAG Engine.

**Leaving custom processor versions deployed.** Hosting is $0.05 per hour per version, with no page traffic required.

**Assuming genAI processor versions cost more.** They cost the same. The real trade-off is data residency.

**Reading "Layout Parser is GA" as complete.** The Gemini-powered v1.5 and v1.6 versions are Preview.

**Budgeting from the Document AI pricing page.** It still lists five processors that no longer exist. Cross-check the processor list.

**Using the general 40 MB limit for Layout Parser.** Layout Parser is 20 MB and 15 pages online.

**Looking for `probability` on `Entity`.** It sits on `EntityMention`, and is always `1.0` for NUMBER, PHONE_NUMBER, ADDRESS, PRICE and DATE.

**Building on Natural Language v2 for entity ranking.** v2 removed `salience` and `wikipedia_url`.

**Following a tutorial that uses Workbench or HITL.** Both are gone as products.

---

## 16. Scenarios to Test Your Knowledge

<details markdown="1">
<summary><b>1.</b> Your invoice pipeline broke in July 2026 with no code change. What is the first thing to check?</summary>

The **processor version**, not the processor. Legacy versions were discontinued on **30 June 2026**.

Point the Invoice Parser at `pretrained-invoice-v2.0-2023-12-06`.
</details>

<details markdown="1">
<summary><b>2.</b> You need 200-token overlap between Layout Parser chunks. How do you set it?</summary>

You cannot set it in Document AI. `ChunkingConfig` only has `chunkSize` and `includeAncestorHeadings`.

Overlap is a **RAG Engine** corpus setting. Its recommended defaults are chunk size 1024 and overlap 256.
</details>

<details markdown="1">
<summary><b>3.</b> Your documents must stay in one region. Can you use <code>v1.6-pro-2025-12-01</code>?</summary>

No. Google states that version *"uses the Vertex AI Gemini global endpoint and is not compliant with Data Residency (DMZ) standards."*

Use a regional processor version instead, and accept the older model.
</details>

<details markdown="1">
<summary><b>4.</b> You need per-entity sentiment from a batch of reviews. Which API version?</summary>

**v1**, or `v1beta2`, which still carries all 7 methods. `analyzeEntitySentiment` is one of the two methods v2 dropped, along with `analyzeSyntax`.

v2 also removed `salience` and `wikipedia_url`. Check your language first: `analyzeEntitySentiment` supports only English, Japanese and Spanish.
</details>

<details markdown="1">
<summary><b>5.</b> You trained three Custom Extractor versions to compare them, then picked one. What is still costing you money?</summary>

The two deployed versions you are not using. Hosting is **$0.05 per hour per deployed version**, about **$438 a year** each.

Training itself was free. Undeploy the versions you rejected.
</details>

<details markdown="1">
<summary><b>6.</b> A colleague quotes the pricing page to budget a Utility parser workload. What do you tell them?</summary>

The Utility parser no longer exists. It was covered by the 30 June 2026 discontinuation.

The pricing page was never cleaned up. It still lists Utility, Procurement splitter, Lending splitter, US passport and Summarizer. Cross-check against the processor list.
</details>

---

## Where Document AI and Natural Language Stand

Document AI is the one classic AI API Google still develops, with its most recent release note dated 2026-07-17 and its name unchanged. Its gallery is now 13 GA processors in three groups: general (OCR, Form Parser, Layout Parser), specialized (Invoice, Expense, Bank Statement, Pay Slip, W2, US Driver License, ID Proofing), and custom (Extractor, Classifier, Splitter). Everything else was discontinued on 30 June 2026, including the whole tax family except W-2, and migration was by processor **version** rather than by product, so a working pipeline could break without any code change. Document AI Workbench disappeared as a brand and its three processors became first-class GA entries. Custom Extractor training now defaults to a Gemini foundation model, starting at zero-shot and scaling to fine-tuning, at the same price as the older conventional model but with a documented data-residency limit on the global Gemini endpoint. Layout Parser is the recommended default in both Gemini Enterprise and RAG Engine, and it attaches ancestral headings to chunks, but its `ChunkingConfig` holds only `chunkSize` and `includeAncestorHeadings`; overlap is a RAG Engine setting. Pricing has no product-wide free tier beyond the first 1,000 OCR units, deployed custom versions cost $0.05 an hour whether used or not, and the pricing page itself is stale, still listing five processors that were discontinued. No Google page compares Document AI with Gemini in either direction, so treat any such comparison as inference. On the text side, the Natural Language API is alive and frozen: no deprecation notice, no release note since August 2023, still PaLM-based in the docs, and a v2 whose only status statement is a Public Preview note from 2023 that was never followed by a GA announcement or contradicted by a Preview badge. That v2 dropped both `analyzeEntitySentiment` and `analyzeSyntax`, removed `salience` and `wikipedia_url`, renamed `language` to `languageCode`, and added `severity`; `v1beta2` still carries all seven methods. Its healthcare sibling shut down on 27 May 2026, with Gemini on Vertex AI as the only suggested replacement. Throughout this area Google's pages disagree with each other, on Custom Extractor v1.4 dates, on deprecated versus discontinued labelling, on the Vertex AI versus Gemini Enterprise Agent Platform wording, and on a shutdown banner still written in future tense. Check two sources before you trust one.

---

## Further Reading and Related Modules

- [Document AI documentation](https://docs.cloud.google.com/document-ai/docs)
- [Natural Language API documentation](https://docs.cloud.google.com/natural-language/docs)
- Back to the hub: [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md)
- Related: [Vision and video APIs](AI-API-VISION-AND-VIDEO.md) · [Speech and translation APIs](AI-API-SPEECH-AND-TRANSLATION.md) · [Search and conversation](AI-API-SEARCH-AND-CONVERSATION.md)
