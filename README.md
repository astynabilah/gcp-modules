# gcp-modules

Learning material for Google Cloud, written as I work through it — self-paced labs you can run in your own project, and reference modules explaining the platform mechanics behind them.

Everything is plain Markdown and renders on GitHub. The figures are hand-drawn SVG console mockups, generated from code in [`tools/`](tools/).

---

## Contents

Each folder below is a **path** — a self-contained set of labs and modules on one topic, with its own README and roadmap.

| Folder | Path | What it covers | Size |
|---|---|---|---|
| [`mlops-gcp/`](mlops-gcp/) | **MLOps on Google Cloud** | Raw data → trained model → served, monitored and automated. Mostly SQL and the console, with training compute, serving, networking, orchestration and Git explained alongside. | labs + modules |

Supporting folders:

| Folder | What it is |
|---|---|
| [`tools/`](tools/) | The entire build system — figure generators, SVG validator, Markdown→HTML renderer. One command, no config. |
| `site/` | Generated HTML. Gitignored; rebuild it rather than reading it from here. |

---

## Where to start

**[→ `mlops-gcp/`](mlops-gcp/)** is the only path so far.

Inside it: [`ROADMAP.md`](mlops-gcp/ROADMAP.md) is the big picture. It covers the ML lifecycle as a set of stages, the real options at each one (BigQuery ML vs AutoML vs custom; Cloud Run vs Vertex endpoint vs GKE vs batch), and which document covers which. Start there if you want the map before the territory. [`README.md`](mlops-gcp/README.md) is the table of contents if you'd rather just pick something.

---

## How a path is laid out

```
<path-name>/
├── README.md      table of contents for the path
├── ROADMAP.md     the big picture, in mermaid
├── labs/          hands-on, step-by-step, run in your own project
│   ├── README.md
│   ├── figures/   generated SVG console mockups
│   └── sql/       every SQL block, extracted as reviewable files
└── modules/       theory, decision frameworks, reference
    ├── README.md
    └── assets/    generated SVG diagrams
```

**Labs** produce a working thing and state their cost up front. **Modules** explain *why* and *which option*, and cost nothing because there is nothing to run.

A new path on another topic (`genai-gcp/`, `data-eng-gcp/`) is a sibling folder with the same shape. Nothing in [`tools/`](tools/) needs editing when one is added: the build locates path folders by looking for a directory containing both `labs/` and `modules/`.

---

## Building the HTML

Optional — the Markdown is the source of truth and reads fine on GitHub. But the HTML inlines every figure into a self-contained page that follows your system light/dark theme:

```bash
python -m pip install markdown pygments
python tools/build.py
```

Then open `site/index.html`. The build regenerates and validates every figure, extracts the SQL, and renders every page — see [`tools/README.md`](tools/README.md) for what each stage does.

---

## A note on accuracy

Everything here is written against the Google Cloud console **as of 23 August 2026**, including the Vertex AI → Gemini Enterprise Agent Platform rebrand. Each document carries a *What changed recently* section for the deprecations and renames that were live at the time of writing.

The screenshots are **mockups, not captures** — drawn in SVG so they stay legible and consistent. They show the fields and controls you'll meet, but expect the real console to differ in styling and to have moved things since.
