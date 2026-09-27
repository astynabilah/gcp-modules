# Vision and video APIs

Google Cloud has five products for images and video. Three are stable and cheap, one is being switched off in weeks, and one has already gone.

> **Module, not a lab.** Nothing here needs running.

---

## TL;DR

- **Cloud Vision API** and **Video Intelligence API** are both GA, both cheap, and both safe to build on. Neither has been renamed.
- Both are frozen. Vision has had no release note since **2024-12-19**. Video Intelligence has had none since **2021-11-01**, making it the most static product in the family.
- **Vertex AI Vision** was renamed **Agent Platform Vision** on **22 April 2026**, then deprecated. It reaches End of Life on **30 September 2026**. Do not build on it.
- **Visual Inspection AI** is gone. Its page now redirects to Model Garden, with no dated announcement anywhere.
- Free tiers are monthly: **1,000 Vision units** and **1,000 Video Intelligence minutes** per month.
- Google publishes **no guidance on Vision API versus Gemini**. There is no migration banner on any Vision doc.

> **Warning.** If you find a tutorial about Streams, Applications, Processors or Vision Warehouse, it is about the product being switched off in September 2026. Read it as history. Details in §6.

For the wider map of pretrained APIs, start at [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md).

---

## 1. Products in This Family

Five products. Three still work, and two do not.

| Product | Former name | Status | What it takes in |
|---|---|---|---|
| **Cloud Vision API** | Never renamed | GA, frozen | One image, or a batch of images |
| **Vision API Product Search** | Never renamed | GA | An image, plus your own product catalogue |
| **Video Intelligence API** | Never renamed | GA, very frozen | One video file |
| **Agent Platform Vision** | **Vertex AI Vision** | Deprecated, dies 30 Sep 2026 | Live video streams |
| **Visual Inspection AI** | Never renamed | Gone, no notice | Factory images |

Cloud Vision and Video Intelligence work the same way. You send a file, you name the features you want, and you get JSON back. You supply no training data and operate no model. Product Search is the exception, because you build a catalogue first.

Agent Platform Vision was a different kind of product, and §6 explains why that matters.

---

## 2. Cloud Vision API Features

The API is a menu. You list the features you want in the request, and each one you ask for is billed separately.

| Feature | Returns |
|---|---|
| **Label detection** | General labels for the whole image, with confidence scores |
| **Text detection (OCR)** | Text found in a photo or a sign |
| **Document text detection** | Dense text, with pages, blocks, paragraphs and words |
| **Face detection** | Face boxes, landmarks, and emotion likelihoods |
| **Landmark detection** | Known places, with latitude and longitude |
| **Logo detection** | Brand logos |
| **Object localisation** | Multiple objects, each with a bounding box |
| **SafeSearch / explicit content** | Likelihoods for adult, violence, racy, spoof and medical |
| **Image properties** | Dominant colours |
| **Crop hints** | Suggested crop boxes for a target aspect ratio |
| **Web detection** | Matching and similar images found on the web |

**Face detection finds faces. It does not identify people.** The API tells you a face is present, where it is, and whether it looks happy. It never returns a name. Face recognition is a separate problem, and this API does not solve it by design.

Two features overlap. Text detection suits a photo with a few words in it. Document text detection suits a scanned page and gives you structure. For real form processing, Document AI is the better tool.

Google's own comparison table on the Vision product page positions the API as *"Quick and easy integration of basic vision features"*. That is a claim about speed and price, not a deprecation notice.

**A note on that page.** Parts of it are stale. Its pricing table still references "Gemini Pro Vision", a model name that has since moved on. Trust the docs at `/vision/docs` over the marketing page.

---

## 3. Sending an Image

Two choices, and they combine.

**Where the bytes live.** Small images go inline in the request body as base64. Large images go to Cloud Storage first, and you pass a `gs://` URI instead. Inline payloads are capped, so anything sizeable has to take the Cloud Storage route.

**How you wait for the answer.**

| Method | Behaviour |
|---|---|
| `images:annotate` | Synchronous. You send images and get JSON in the response. |
| `images:asyncBatchAnnotate` | Asynchronous. Results are written to Cloud Storage as JSON files. |

Use the synchronous call while you are learning, and for anything user-facing. Use the batch call for large jobs, where you would otherwise hold a connection open for a long time.

**Pricing.** The first **1,000 units per month** are free. A unit is one feature applied to one image, so a single image with three features requested is three units. Above **5,000,001 units per month** the per-unit price drops. The free tier resets monthly, so a test that costs nothing today can bill next month.

---

## 4. Vision API Product Search

Product Search answers a retail question. A customer photographs a shoe, and you need to know which of your shoes it is. Docs live at `/vision/product-search/docs`.

The general Vision API cannot do this. It knows "shoe", not "your SKU 4471 in navy". Product Search closes that gap by searching your own catalogue.

The setup has three steps, and none of them is a training job.

1. **Create products.** Each product has an ID, a category, and optional labels such as colour or style.
2. **Add reference images.** Several photos per product work better than one.
3. **Create a product set and index it.** Indexing runs on a schedule. New images are not searchable straight away.

At query time you send a photo and a product set. You get back matching products, ranked by score. You can filter by label, so "find this bag, but only in stock colours" is one request.

**A stale cross-reference to expect.** Some Product Search material points readers at **Vision Warehouse** for storing and searching media. Vision Warehouse belongs to Agent Platform Vision, the product being switched off. Ignore that path.

---

## 5. Video Intelligence API

The same idea as Vision, applied to a video file. You submit a file, Google analyses it, and you collect annotations with timestamps.

| Feature | Returns |
|---|---|
| **Label detection** | What appears, at segment, shot or frame level |
| **Shot change detection** | Where one camera shot ends and the next begins |
| **Explicit content detection** | Likelihood scores over time |
| **Speech transcription** | Words spoken, with timings |
| **Text detection** | On-screen text, such as captions or signs |
| **Object tracking** | One object followed across frames |
| **Person detection** | People, with pose landmarks |
| **Face detection** | Faces present, again without identifying anyone |
| **Logo recognition** | Brand logos, with time ranges |

Calls are asynchronous. You start an operation, poll it, and read the result when it finishes. Input comes from Cloud Storage for anything beyond a small clip.

**Pricing.** The first **1,000 minutes per month** are free. Above **100,000 minutes per month** the rate drops. Minutes are counted per feature, so asking for four features on a one-hour video bills four hours.

**This is the most frozen product covered here.** The last release note is dated **2021-11-01**. It still works and is still sold. Nothing new is arriving.

---

## 6. The Agent Platform Vision Shutdown

This is the most important item on the page, and the easiest to confuse with §5.

**The name.** It launched as **Vertex AI Vision**. On **22 April 2026** it became **Agent Platform Vision**, as part of the Vertex AI to Gemini Enterprise Agent Platform rebrand. The documentation path never changed, and is still `/vision-ai/docs`.

**The notice**, quoted exactly from Google's docs:

> *"Vertex AI Vision is deprecated as of June 15, 2026 and reaches End of Life on September 30, 2026. To migrate, see the Cloud Vision API, Agent Platform serverless training, or Agent Platform models."*

**What it was.** A managed platform for building computer-vision *applications* over video streams. Four concepts held it together:

| Concept | Meaning |
|---|---|
| **Stream** | A source of video. A live IP camera, or a file being replayed. |
| **Application** | A graph that connects a stream to one or more AI processors. |
| **Processor** | A unit of analysis: occupancy counting, person or vehicle detection, or your own custom model. |
| **Vision Warehouse** | Storage and search over the analysed video. |

**How it differs from the Video Intelligence API.** This pair causes the most confusion in this area, so hold on to the difference.

| | Video Intelligence API | Agent Platform Vision |
|---|---|---|
| Input | A finished file | A live or continuous stream |
| Shape | One API call per file | A running application you deploy |
| Question it answers | What is in this video? | What is happening right now? |
| Status | Alive, frozen | Dies 30 September 2026 |

Video Intelligence is a **per-file annotation API**. You hand it a video and it hands back JSON. Agent Platform Vision was a **streaming platform**, closer to an always-on service than to an API call.

**What to do.** Do not build anything new on it. Learn the four concepts only so you can recognise them in older articles, blog posts and course material, which are plentiful and mostly undated. [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md) covers it in §5 for the same reason.

---

## 7. Visual Inspection AI's Disappearance

It was a product for manufacturing defect detection. Two use cases dominated: **cosmetic inspection**, for scratches, dents and stains, and **assembly inspection**, for missing or misplaced parts. It trained on a small number of your own defect images.

Today, `cloud.google.com/solutions/visual-inspection-ai` returns a **301 redirect to the Model Garden explore-models page**.

**Be careful with this one.** No dated deprecation announcement was ever published, as far as I can find. There is no shutdown date, no migration guide, and no entry in any release note. The conclusion that it is gone rests on the redirect alone. That is inference from evidence, not a confirmed statement by Google.

Search engines still return its old pages and old marketing copy. Treat any result about it as historical.

---

## 8. Vision APIs Versus Gemini

Google has published nothing on this. There is no comparison page, no decision tree, and no migration banner on any Vision or Video Intelligence document. **Everything below is my reasoning, not Google's recommendation.**

Reasons to keep using the API:

- **Price is predictable.** You pay per unit or per minute, with a monthly free tier. A model call bills tokens in and tokens out.
- **The output has a fixed schema.** Bounding boxes and confidence scores arrive as typed JSON. A language model returns text you then have to parse.
- **The task is a standard one.** Reading text from a receipt, or flagging explicit content, needs no reasoning about your business.

Reasons to reach for Gemini:

- **The categories are yours.** "Is this weld defective" is not on the Vision menu.
- **You want one call to do several things.** Describe the image, extract the total, and judge the mood, in a single prompt.
- **You need reasoning, not labels.** "Why does this photo break our policy?" is not a detection task.

The signals from Google are structural rather than written. Both APIs sit frozen while Document AI's newest parsers run on Gemini. Read that as a direction of travel, not as advice to migrate.

---

## 9. Where to go next

- [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md) — the map of all the pretrained APIs, plus the full rename and shutdown tables
- [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md) — where these sit next to AutoML and BigQuery ML, with a §5 on Vertex AI Vision

Google documentation:

- [Cloud Vision](https://docs.cloud.google.com/vision/docs)
- [Video Intelligence](https://docs.cloud.google.com/video-intelligence/docs)
- [Vision AI, now Agent Platform Vision](https://docs.cloud.google.com/vision-ai/docs)

---

## Summary

Two products here are safe to use and two are not. **Cloud Vision API** gives you a menu of image features, billed per unit, with 1,000 units free each month, and it detects faces without ever identifying a person. **Video Intelligence API** does the same job for a video file, with 1,000 free minutes a month counted per feature. Both are GA, neither has been renamed, and both are frozen: Vision since 2024-12-19 and Video Intelligence since 2021-11-01. **Vision API Product Search** uses your own data, letting a shopper find a catalogue item from a photo once you have built and indexed a product set. **Vertex AI Vision**, renamed **Agent Platform Vision** in April 2026, was a streaming platform built from Streams, Applications, Processors and Vision Warehouse, and it reaches End of Life on 30 September 2026, so learn it only to recognise it in old material. **Visual Inspection AI** appears to be gone as well, though the only evidence is a redirect to Model Garden rather than any announcement. Google has published no guidance comparing these APIs with Gemini, so treat any such comparison, including mine in §8, as reasoning rather than a recommendation.
