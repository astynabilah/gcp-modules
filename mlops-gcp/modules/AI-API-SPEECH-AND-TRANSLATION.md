# Speech and translation APIs

Three products sit here: audio in, audio out, and language in between. All three are alive, all three are priced, and all three carry version splits that decide what you can do.

> **Module, not a lab.** Nothing here needs running.

---

## TL;DR

- Speech-to-Text **V1 and V2 are both GA**. V1 is **not deprecated**, and no sunset notice exists anywhere.
- V1 has the **60 minutes per month free tier**. **V2 has none.** Migrating to V2 costs you the free minutes.
- **Chirp 3** is the current speech flagship. GA on **13 October 2025**, V2 only, `us` and `eu` multi-regions.
- Chirp 3 has **no word-level timestamps and no word-level confidence**. If you need either, stay on `chirp_2` or a V1 model.
- Text-to-Speech now groups Studio, Neural2, Polyglot, WaveNet and Standard under **"Legacy"**. None is formally deprecated, and all still show **GA**.
- **Studio costs $160 per 1M characters**, more than five times Chirp 3: HD at $30, despite the legacy label.
- Cloud Translation **Basic (v2) and Advanced (v3) are both GA**. Basic accepts API keys. Advanced does not.
- **AutoML Translation shut down on 30 September 2025.** Its custom-model job moved inside Translation Advanced.
- The three move at very different speeds. Newest release notes: Speech-to-Text **13 November 2025**, Text-to-Speech **30 December 2025**, Translation **24 February 2026**.
- These APIs are **not being absorbed into Gemini**. Gemini models are being delivered *through* them. See §15.

For the wider map of pretrained APIs, start at [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md).

---

## 1. What is in this family?

Three products, and every one of them has at least two names.

| Product | Docs name | Marketing name | Former name |
|---|---|---|---|
| **Speech-to-Text** | Cloud Speech-to-Text | Speech-to-Text | **Cloud Speech API** |
| **Text-to-Speech** | Cloud Text-to-Speech | Text-to-Speech | Never renamed |
| **Cloud Translation** | Cloud Translation | **Translation AI** | The Google Translate API |

**Speech-to-Text** went public in 2016 as the Cloud Speech API. The rename to Speech-to-Text happened around the Text-to-Speech launch in 2018, when Google needed a matching pair of names. I could not verify the exact rename date, so treat 2018 as approximate.

**Text-to-Speech** launched on **27 March 2018** and reached GA on **28 August 2018**. It has never been renamed.

**Cloud Translation** is the oldest of the three and grew out of the Google Translate API. The documentation calls it Cloud Translation. The Google Cloud product listing calls it Translation AI. Both names point at the same endpoints.

---

## 2. Speech-to-Text V1 and V2

Both versions are GA. Both are current. This surprises people who assume V2 replaced V1.

**V1 is not deprecated.** There is no sunset date, no migration banner, and no deprecation entry in any release note. The migration guide says only this:

> *"Migration from the V1 API to the V2 API does not happen automatically."*

That is the whole of Google's position. Nothing pushes you off V1.

**The free tier runs the wrong way.** V1 gives you **60 minutes per month free**. V2 gives you nothing free. So the newer API bills from the first second. If you are learning, or running small jobs, V1 is cheaper for reasons that have nothing to do with quality.

**V1 pricing.**

| Model | Price per minute |
|---|---|
| Standard, **with** data logging | **$0.016** |
| Standard, **without** data logging | **$0.024** |
| Medical models | **$0.078** |

Data logging means letting Google keep your audio to improve its models. Opting out costs 50% more.

**V2 pricing**, which is tiered by monthly volume.

| Monthly minutes | Price per minute |
|---|---|
| First 500,000 | **$0.016** |
| 500,000 to 1,000,000 | **$0.010** |
| 1,000,000 to 2,000,000 | **$0.008** |
| Above 2,000,000 | **$0.004** |
| **Dynamic batch**, any volume | **$0.003** |

**Dynamic batch is V2 only and roughly five times cheaper** than the entry rate. Google schedules the work when it has spare capacity, so you trade latency for price. This is the strongest reason to move to V2, stronger than any feature.

---

## 3. Sending audio: sync, streaming, batch

Three call shapes, three sets of limits. Pick the shape first, because the limits decide what is possible.

| Call type | Input | Hard limits |
|---|---|---|
| **Synchronous** | Inline bytes or a Cloud Storage URI | **10 MB or 1 minute**, whichever comes first |
| **Streaming** | A live audio stream | **25 KB per request**; stream stays open **5 minutes** maximum |
| **Batch** | **Cloud Storage URI only** | **8 hours per file**, at most **5 files per request** |

Three things follow from this table.

The synchronous limit is a pair, not a choice. A 30-second file over 10 MB still fails.

The 5-minute streaming cap means long live sessions need reconnection logic. You cannot hold one stream open for an hour-long call.

Batch will not accept inline bytes at all. Anything long has to reach Cloud Storage first.

---

## 4. Recognizers in V2

V2 added an object that V1 never had. Google's definition, quoted exactly:

> *"Recognizers are reusable recognition configurations that can contain a combination of model, language, and features."*

The idea is that you create a recognizer once, then reference it from every call. You get one place to change the model or the language.

**Recognizers are optional, and most current samples skip them.** You pass the literal `recognizers/_` as the resource name and supply the configuration inline in the request instead. That path is fully supported and simpler for learning.

The quota is **5,000 recognizers per region**. That is generous, but it is a per-region limit rather than a per-project one.

Use a recognizer when many clients share one configuration. Use `recognizers/_` when a single service owns the call and the config lives in its code.

---

## 5. The Chirp models

Chirp is Google's family of large speech models. Three generations exist, and the naming hides how much changed between them.

| Model ID | Generation | Status |
|---|---|---|
| `chirp` | Original | Now only a footnote on the pricing page, listed as a "Standard" model |
| `chirp_2` | USM and LLM powered | GA **27 January 2025** |
| `chirp_3` | Current flagship | GA **13 October 2025** |

**`chirp`** has been dropped from the model-comparison page entirely. It survives only in a pricing-page footnote that groups it with Standard models. Google published no deprecation notice for it.

**`chirp_2`** is built on the Universal Speech Model and adds LLM capability. It handles streaming and batch, and it does **transcription and translation**. It went GA on 27 January 2025 in `asia-southeast1`, `us-central1` and `europe-west4`.

**`chirp_3`** moved through three stages in 2025: private preview in **April 2025**, public preview on **29 August 2025**, GA on **13 October 2025**. It exists **only in V2**, and only in the `us` and `eu` multi-regions.

That last point matters for two reasons. Chirp 3 is one more reason to be on V2. And multi-region only means you cannot pin it to a single country.

---

## 6. What Chirp 3 cannot do

The flagship model has real gaps, and they are easy to miss because the feature list looks long.

| Feature | Status |
|---|---|
| Automatic punctuation | GA |
| Automatic capitalization | GA |
| Utterance-level timestamps | GA — **`StreamingRecognize` only** |
| Speaker diarization | GA — **`BatchRecognize` only** |
| Speech adaptation (biasing) | GA |
| Language-agnostic transcription | GA |
| Custom prompt | Preview |
| **Word-level timestamps** | **Not supported** |
| **Word-level confidence** | **Not supported** |

On confidence scores, Google is unusually direct about the value it returns:

> *"The API returns a value, but it isn't truly a confidence score."*

So even where a number comes back, do not build thresholds on it.

### Two traps

**Trap one: word-level output.** If you need per-word timestamps for captions, or per-word confidence for quality routing, Chirp 3 cannot serve you. Stay on `chirp_2` or a V1 model. This is a case where the newest model is the wrong choice.

**Trap two: diarization and timestamps come from different calls.** Speaker diarization works only in `BatchRecognize`. Utterance-level timestamps work only in `StreamingRecognize`. You cannot get both from one call. A meeting transcript that needs speaker labels *and* timings needs two passes, or a different model.

### Adaptation limits

Speech adaptation biases the model towards words it would otherwise miss, such as product names or drug names. The quotas are tight enough to plan around.

| Limit | Value |
|---|---|
| Maximum boost value | **20** |
| Phrases per PhraseSet | **1,200** |
| Phrases per request | **5,000** |
| Characters per phrase | **100** |
| Total characters per request | **100,000** |
| Items per CustomClass | **500** |
| PhraseSets per SpeechAdaptation | **20** |
| CustomClasses per SpeechAdaptation | **20** |

A boost of 20 is the ceiling, not a suggestion. Pushing every phrase to 20 removes the ranking you were trying to create.

**Release-note silence.** The newest Speech-to-Text release note is dated **13 November 2025**. There are **zero entries in 2026**. The product works and is sold, but the changelog has stopped.

---

## 7. Text-to-Speech: what you are billed for

The billing unit is **characters, including spaces and newlines**. Whitespace costs money.

SSML makes this worse than it sounds. **Every SSML tag except `<mark>` counts towards your character total.** So a heavily marked-up document bills for markup as well as speech. If you wrap each sentence in `<s>` tags, you pay for the tags.

Two habits follow. Strip indentation from generated SSML. And check whether the control you want needs a tag at all, because plain text is cheaper.

---

## 8. Voice tiers and the "Legacy" label

Google's pricing page splits the voices into two groups. The "Legacy" labels below are Google's own wording, not mine.

| Tier | Group on the pricing page | Free per month | Price per 1M chars |
|---|---|---|---|
| **Chirp 3: HD** | Latest TTS models | 1M chars | **$30** |
| **Instant Custom Voice** | Latest TTS models | none | **$60** |
| Studio | **Legacy** | 1M chars | **$160** |
| Neural2 | **Legacy** | 1M chars | **$16** |
| Polyglot (Preview) | **Legacy** | 1M chars | **$16** |
| WaveNet | **Legacy** | **4M chars** | **$4** |
| Standard | **Legacy** | **4M chars** | **$4** |

**"Legacy" is a positioning label, not a deprecation.** None of these tiers has a deprecation notice. All of them still show a **GA** launch stage on the voice-list page. You can build on Neural2 today and nothing tells you to stop. Google has moved them into a lower group on a pricing page, and that is the full extent of the signal.

Two oddities in that table deserve attention.

**Studio is the most expensive tier on the page.** At $160 per million characters it costs more than five times Chirp 3: HD, and ten times Neural2, while sitting in the legacy group. Price is not tracking Google's own positioning here.

**WaveNet and Standard now share one SKU at $4.** WaveNet used to carry a clear premium over Standard. That premium is gone, and both get the larger 4M character free tier. If you were choosing Standard to save money, there is no longer a reason to.

---

## 9. Gemini-TTS inside the Text-to-Speech API

Gemini speech models ship **inside the Cloud Text-to-Speech API**, not beside it. Same product, same API, different billing model.

They are priced on **tokens**, not characters, and there is **no free tier**.

| Model | Text tokens in, per 1M | Audio tokens out, per 1M |
|---|---|---|
| Gemini 2.5 Flash TTS | **$0.50** | **$10** |
| Gemini 2.5 Flash-Lite Preview TTS | **$0.50** | **$10** |
| Gemini 2.5 Pro TTS | **$1.00** | **$20** |
| **Gemini 3.1 Flash TTS (Preview)** | **$1.00** | **$20** |

The conversion you need for any estimate: **audio tokens are 25 tokens per second of audio**. One minute of speech is 1,500 audio tokens. At $10 per million, that is $0.015 a minute on Flash TTS.

**A gap in the changelog.** The newest Text-to-Speech release note is **30 December 2025**. Yet `gemini-3.1-flash-tts-preview` is live on the pricing page with its own SKUs, and it is fully documented. No release note announces it. Text-to-Speech is shipping models without updating its own changelog, so the release-note date understates how active the product is.

---

## 10. Chirp 3: HD, missing voices, and an SSML contradiction

Chirp 3: HD dominates the voice catalogue. Rough counts: **about 1,500 Chirp 3: HD entries**, against **about 69 Neural2** and **about 160 WaveNet**. It offers **30 styles**, and it **supports streaming**. The older tiers do not stream at all.

**One blocker to check early.** Chirp 3: HD is **"out of scope for regionalization and data residency"**. If your work has residency constraints, this rules the flagship out before any quality comparison starts.

### The SSML contradiction

Two live Google pages disagree about whether Chirp 3: HD accepts SSML.

The release note of **17 October 2025** says:

> *"Chirp 3 HD now supports speech synthesis using SSML input. Supported SSML tags are: `<phoneme>`, `<p>`, `<s>`, `<sub>`, and `<say-as>`."*

The currently-live supported-voices page says:

> *"Chirp 3: HD voices doesn't support SSML input, speaking rate and pitch-audio parameters, and the A-Law audio encoding."*

**This is unresolved.** One of the two pages is stale, and the documentation alone gives no way to tell which. Test SSML against Chirp 3: HD yourself before you depend on it. The two parameters in the second quote, speaking rate and pitch, are not contested by the release note, so treat those as unavailable.

### Voices that vanished

**Journey voices are entirely gone.** There are zero Journey entries in the voice catalogue, and **no deprecation notice was ever published**. The conclusion rests on their absence from the catalogue, so treat it as inferred rather than confirmed. Older tutorials still reference them.

**Polyglot is being quietly de-emphasised.** It is absent from the voice-type overview table, but it is still in the catalogue and still priced at $16 per million characters. It carries a Preview label after years. Nothing says it is going away, and nothing suggests it is being developed.

---

## 11. Long Audio Synthesis and Instant Custom Voice

Two features sit outside the normal synthesize call.

**Long Audio Synthesis** handles input too large for a standard request. It has been in **Preview for years**.

| Detail | Value |
|---|---|
| API version | `v1beta1` |
| Endpoint | `projects/{n}/locations/global:synthesizeLongAudio` |
| Shape | Asynchronous, long-running operation |
| Input limit | **1 million bytes** |
| Output | Written to Cloud Storage |
| Permissions needed | Storage Object Creator **and** Storage Object Viewer |

Note the endpoint is `locations/global`. This is another residency consideration, and the Preview stage has not moved in a long time.

**Instant Custom Voice** builds a voice from a short sample. It is **allow-list only**, and you request access through sales contact. It is built on Chirp 3.

| Capability | Detail |
|---|---|
| Pace control | **0.25x to 2x** |
| Pronunciation control | IPA and X-SAMPA, **experimental** |
| Language transfer | Supported |
| Price | **$60** per 1M chars, no free tier |

**It requires a spoken consent statement from the voice owner, per language.** The person whose voice you clone has to record a consent statement in each language you plan to use. This is a legal and ethical control built into the product, and it shows how voice cloning is being gated. If you meet consent requirements in other products later, this is the pattern.

---

## 12. Cloud Translation: Basic and Advanced

Two editions, both GA, neither deprecated. The split runs deeper than a version number, because the client libraries differ.

| | **Basic (v2)** | **Advanced (v3)** |
|---|---|---|
| Client libraries | v2 | v3 |
| Models | NMT only | Model selection |
| **API keys** | **Allowed** | **Not allowed** |
| Authentication | API keys, or service accounts | **Service accounts and IAM only** |
| Glossaries | No | Yes |
| Batch translation | No | Yes |
| Document translation | No | Yes, PDF, DOCX and PPT with layout preserved |
| Billing labels | No | Yes |
| Regional endpoints | No | Yes |
| Romanization | No | Yes |
| Model evaluation (BLEU) | No | Yes |

Google steers new work towards Advanced, quoted exactly:

> *"If you're planning a new project, you may want to choose the Advanced edition instead of the Basic edition, to take advantage of better security, more features, and the new service improvements that the Advanced edition will continue to make going forward."*

On compatibility, also quoted exactly:

> *"Cloud Translation - Advanced supports all Cloud Translation - Basic features and models, but due to required changes to the client libraries is not backward compatible."*

Read that carefully. Advanced is a superset in capability and a break in code. Moving is a rewrite of the call sites, not a version bump.

**One nuance undercuts the clean split.** Basic can also use the standard Translation LLM, if you give the model's full resource name in the request. So the LLM is not strictly Advanced-only. The tidy story of "Basic means NMT, Advanced means everything" is not quite true.

### The models

| Model | Model ID |
|---|---|
| Translation LLM (TLLM) | `general/translation-llm` |
| NMT | `general/nmt` |
| Customized TLLM | `translation-llm-custom/{id}` |
| Adaptive MT | `general/translation-llm-adaptive` |
| Customized NMT | generated |

Google describes the Translation LLM this way:

> *"a Large language model (LLM) powered by Gemini and fine-tuned for translation to provide the highest quality translations at fast latencies (2x faster latency than Gemini 2.0 Flash)."*

And NMT this way:

> *"Fastest translation model - ideal for real time and latency critical use cases."*

So the choice is quality against latency, with NMT still the fast option.

### Pricing

**Basic.** The first 500,000 characters per month are free, delivered as a **$10 credit**. From 500,000 characters to 1 billion, the rate is **$20 per 1M characters**.

**Advanced.**

| What | Price |
|---|---|
| NMT, text | **$20 per 1M characters**, input only |
| NMT, document | **$0.08 per page** |
| **Translation LLM** | **$10 per 1M in AND $10 per 1M out** |
| Adaptive MT (TLLM) | **$25 in + $25 out** per 1M characters |
| Custom TLLM | **$10 in + $10 out** per 1M characters |
| Custom NMT, text | **$80 → $60 → $40 → $30** per 1M characters by volume |
| Custom NMT, document | **$0.25 per page** |
| Custom model training | **$45 per hour**, capped at **$300 per job** |

The TLLM billing model differs from NMT. NMT bills input only. **TLLM bills both directions.** Google explains the intent, quoted exactly:

> *"If you use Translation LLM (LLM), then it is charged $10 per million characters input and $10 per million characters output, making it cost equivalent with NMT."*

The arithmetic works when input and output lengths match. Translation into a more verbose language produces more output characters than input, so the equivalence is approximate rather than exact.

**A free-tier trap.** The **$10 monthly credit** is documented against the **NMT** row, and it is **shared across Basic and Advanced**. It does not roll over. It does not apply to formatted document translation. **Whether it applies to Translation LLM is unconfirmed**, because the documentation attaches it to NMT and says nothing about TLLM. Assume it does not, and check your first bill.

---

## 13. AutoML Translation and Translation Hub

Two shutdowns here, and they are different in kind.

**AutoML Translation was absorbed rather than deleted.** It was deprecated on **16 September 2024** and shut down on **30 September 2025**. Its custom-model capability did not disappear. It now lives inside Cloud Translation Advanced as **custom NMT models**. Google's rationale, quoted exactly:

> *"We recommend that you use Cloud Translation because future enhancements to datasets and customs models will apply only to Cloud Translation."*

So if a course or article tells you to use AutoML Translation to train a custom translation model, the capability still exists. Only the front door moved.

**Translation Hub is a separate product**, and it is not the API. It was a document-translation portal for organisations, with a self-serve interface for staff. It was deprecated on **30 June 2025** and **shuts down on 20 September 2026**, which is weeks away at the time of writing. Nothing about the Cloud Translation API depends on it.

**Translation is the only one of the three still moving.** Its newest release note is **24 February 2026**:

> *"Translation LLM now supports full finetuning with LoRA."*

Speech-to-Text and Text-to-Speech have no 2026 release notes at all.

---

## 14. When should you use Gemini instead?

For most of this area Google publishes nothing. There is one exception, and it is not in the Cloud documentation.

The Gemini API audio documentation on `ai.google.dev` says:

> *"For dedicated speech to text models with support for real-time transcription, use the Google Cloud Speech-to-Text API."*

**That is the only explicit "use the API, not Gemini" statement I could find** across all three products. It covers speech only.

From it, and from the published limits, four decision axes follow. **These are my reasoning, not Google's recommendation**, except for the first row.

| What you need | Pick | Why |
|---|---|---|
| Real-time or streaming transcription | **Speech-to-Text** | Gemini audio is request and response over a file |
| A very long file in one prompt | **Gemini** | Gemini accepts **up to 9.5 hours** per prompt at 32 tokens per second, against **8 hours per file** for STT batch |
| Transcription plus reasoning in one call | **Gemini** | Summarise, classify and transcribe in one pass |
| Phrase biasing for domain vocabulary | **Speech-to-Text** | Gemini has no PhraseSet equivalent |

The second row surprises people. Gemini handles the *longer* file, not the shorter one. The API wins on real-time work, not on length.

**For translation and for text-to-speech, no guidance exists at all.** Google has published nothing comparing Cloud Translation with Gemini, and nothing comparing the TTS voice tiers with calling a Gemini model directly. Any comparison you read on those two, including one you construct yourself, is inference.

**One more thing to recognise.** The Gemini Enterprise Agent Platform has thin wrapper pages for speech and translation. They hand you off to the standalone products:

> *"For more models, advanced features, and ability to transcribe files up to 8 hours, see Speech-to-Text."*

The wrapper is heavily capped: **60 seconds or 10 MB** of audio, **Chirp only**, and **16-bit linear PCM WAV only**. It exists for convenience inside the platform, not as a replacement. If you find it first, do not mistake it for the real product.

---

## 15. Which way is the convergence running?

This is the most useful point on the page, and it runs against the common assumption.

**These APIs are not being absorbed into Gemini. Gemini models are being delivered through the Cloud APIs.**

The evidence is in the products themselves.

**Text-to-Speech.** Gemini-TTS ships *inside* Cloud Text-to-Speech, on Cloud TTS SKUs, billed on the Cloud TTS bill. Google describes it as *"the latest evolution of our Cloud TTS technology."* The Gemini model arrived as a feature of the older product.

**Cloud Translation.** The Translation LLM is Gemini-derived, and Google says so in the model description. It ships inside Cloud Translation, under a Cloud Translation model ID, priced on the Cloud Translation page.

**Speech-to-Text is the outlier.** Chirp 3 is an ASR-specific generative model, not a Gemini derivative. Speech-to-Text has received **no Gemini-branded model at all**. That fits its release-note silence since 13 November 2025.

So the pattern across the three is consistent, with one exception:

| Product | Gemini model inside it? | Newest release note |
|---|---|---|
| Text-to-Speech | **Yes**, Gemini-TTS | 30 December 2025 |
| Cloud Translation | **Yes**, Translation LLM | **24 February 2026** |
| Speech-to-Text | **No** | 13 November 2025 |

**Speech-to-Text is the one to watch.** It is the only one of the three with no Gemini path, the quietest changelog, and a flagship model missing features its predecessor had. None of that is a deprecation signal by itself. Together it is a product with less momentum than its neighbours.

---

## 16. Where to go next

- [What AI APIs are in Google Cloud?](AI-APIS-OVERVIEW.md) — the map of all the pretrained APIs, with the rename and shutdown tables
- [Vision and video APIs](AI-API-VISION-AND-VIDEO.md) — the same pattern applied to images and video
- [Low-code AI on Google Cloud](LOW-CODE-AI-ON-GCP.md) — where these sit next to AutoML and BigQuery ML

Google documentation:

- [Speech-to-Text](https://docs.cloud.google.com/speech-to-text/docs)
- [Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs)
- [Cloud Translation](https://docs.cloud.google.com/translate/docs)

---

## Summary

All three products here are alive, and each one carries a version split you have to choose from. **Speech-to-Text** keeps V1 and V2 both GA, with no deprecation notice on V1, and V1 holds the only free tier at 60 minutes a month, so migrating to V2 costs you free minutes in exchange for tiered pricing and $0.003 dynamic batch. **Chirp 3**, GA on 13 October 2025 and V2 only in the `us` and `eu` multi-regions, is the flagship but cannot return word-level timestamps or word-level confidence, and it splits diarization into `BatchRecognize` and utterance timestamps into `StreamingRecognize`, so one call cannot give you both. **Text-to-Speech** bills characters including spaces and all SSML tags except `<mark>`, and it now groups Studio, Neural2, Polyglot, WaveNet and Standard under a "Legacy" heading even though none is deprecated and all still show GA, which leaves the odd result that legacy Studio at $160 per million characters is the most expensive tier on the page. **Cloud Translation** keeps Basic and Advanced both GA, with API keys allowed only in Basic, and its Gemini-derived Translation LLM bills both input and output at $10 per million characters against NMT's input-only $20. **AutoML Translation** shut down on 30 September 2025 but its custom-model job moved inside Advanced, and the separate **Translation Hub** portal shuts down on 20 September 2026. The structural finding is that Gemini is not replacing these APIs; it is being shipped inside them, with Gemini-TTS in Cloud Text-to-Speech and the Translation LLM in Cloud Translation, while **Speech-to-Text alone has received no Gemini model and no release note since 13 November 2025**.
