# tools/ — the build system

Every line of code in this repository lives in this folder. Everything under
`mlops-gcp/` is prose, or is generated from here.

```bash
python tools/build.py
```

One command, three stages, no arguments.

---

## What's in here

| File | What it does |
|---|---|
| `build.py` | The only entry point. Runs the three stages below. |
| `svgkit.py` | SVG primitives — the Google Cloud console mockups are drawn, not screenshotted. |
| `check_svg.py` | Validates generated SVGs. Takes directories or files as arguments. |
| `figures/lab_*.py` | One generator per lab. Writes into `mlops-gcp/labs/figures/`. |
| `figures/mod_*.py` | One generator per module. Writes into `mlops-gcp/modules/assets/<name>/`. |

---

## The three stages

**1. Figures.** Every `figures/*.py` runs, drawing SVGs into the folder next to
the document that embeds them. Then `check_svg.py` parses each one and checks
for XML errors, rects outside the canvas, and text that overflows its box — the
last of these is estimated from character count and font size, deliberately
generously, so it flags anything close to the edge for a look rather than
silently shipping a clipped label.

**2. SQL extraction.** Every ` ```sql ` block in the labs is written out to
`mlops-gcp/labs/sql/labNN/NN-heading.sql`, named after the section it came from.
The queries end up reviewable as files rather than buried in prose.

**3. HTML.** Every `.md` renders into `site/` as one self-contained page —
SVGs inlined, CSS inlined, no external requests. `site/` is gitignored because
it is entirely reproducible.

---

## Why the code is here and not next to the documents

It used to be next to the documents: generators sat in `labs/figures/` and in
each `modules/assets/<name>/` folder, and the SVG validator existed as
**fourteen byte-identical copies**, one per asset directory. Fixing the
overflow estimate meant editing all fourteen.

Now there is one validator, one `svgkit`, and the content folders hold nothing
you'd have to read code to understand.

## Adding a figure

1. Write `tools/figures/mod_<name>.py`.
2. Get the output directory from `svgkit`:

```python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("yourmodule")     # or c.lab_figures() for a lab
```

3. Run `python tools/build.py`. Discovery is by glob — there is no list to
   register the new file in.

`asset_dir()` and `lab_figures()` create the directory if it doesn't exist, and
resolve it by **finding the folder that contains both `labs/` and `modules/`**
rather than hard-coding a path. That's the only place the content layout is
encoded, so moving or renaming the path folder — which has happened more than
once — doesn't mean editing twenty scripts.

## Adding a document

Add it to the `LABS` or `MODULES` list at the top of `build.py`. That list is
explicit rather than globbed because it also carries each page's title and, for
labs, the SQL output subdirectory.

---

## Dependencies

```bash
pip install markdown pygments
```

Standard library otherwise. No build tool, no bundler, no config file.
