import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("apiversions")

W = 940


def write(name, w, h, body, title):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-30s %sx%s" % (name, w, h))


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6, label=None, dash=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    out = [c.line(x1, y1, hx, hy, col, sw, dash=dash),
           c.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
               x2, y2,
               x2 - 9 * math.cos(ang - 0.42), y2 - 9 * math.sin(ang - 0.42),
               x2 - 9 * math.cos(ang + 0.42), y2 - 9 * math.sin(ang + 0.42)), fill=col)]
    if label:
        out.append(c.t((x1 + x2) / 2, min(y1, y2) - 9, label, 9.5, c.GREY, "500", "middle"))
    return out


# --------------------------------------------------------------------------

def fig_four_axes():
    w, h = 940, 688
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Four different things are all called 'version'", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "This is the actual source of the confusion. They are independent "
                            "of one another.", 11, c.GREY))

    axes = [
        ("1. API version", c.BLUE, "v1  ·  v1beta1",
         "The stability contract of the REST/gRPC surface.",
         ["v1      = GA. SLA, 12-month deprecation notice.",
          "v1beta1 = Preview. No SLA, may change, test only.",
          "New features usually land in v1beta1 first."],
         "Ask: is this feature stable?"),
        ("2. Feature generation", c.PURPLE, "Model Monitoring v2  ·  GCPC v1 / preview",
         "A redesign of a product, numbered by its maker.",
         ["Model Monitoring 'v2' is a NEW DESIGN of the",
          "feature - not the v2 of an API. It is reached",
          "through the same v1 / v1beta1 endpoints."],
         "Ask: which generation of the product?"),
        ("3. SDK / library version", c.AMBER, "kfp 2.x  ·  google-cloud-aiplatform 1.x",
         "Ordinary Python package semver.",
         ["KFP SDK v2 is a library major version.",
          "It is unrelated to API v1 vs v1beta1.",
          "A 2.x SDK can call a v1beta1 endpoint."],
         "Ask: which package release?"),
        ("4. Model version", c.GREEN, "churn-model v1, v2, v3",
         "Your own model revisions in the registry.",
         ["Incremented every time you re-register.",
          "Nothing to do with any of the above."],
         "Ask: which trained artifact?"),
    ]
    y = 80
    for name, col, examples, what, lines, ask in axes:
        body.append(c.rect(24, y, w - 48, 122, fill="#ffffff", stroke=col, rx=9, sw=1.5))
        body.append(c.rect(24, y, 6, 122, fill=col, rx=3))
        body.append(c.t(46, y + 26, name, 12.5, c.TEXT, "700"))
        body.append(c.mono(210, y + 26, examples, 11, col))
        body.append(c.t(46, y + 46, what, 10.5, c.GREY))
        for i, ln in enumerate(lines):
            body.append(c.t(46, y + 68 + i * 16, ln, 10, c.TEXT))
        body.append(c.rect(624, y + 58, 292, 30, fill=col, rx=6, op=0.10))
        body.append(c.t(770, y + 78, ask, 10.5, col, "700", "middle"))
        y += 130

    co, _ = c.callout(24, y + 4, w - 48, [
        "'Use Model Monitoring v2' and 'use the v1beta1 API' are not the same sentence and do not",
        "conflict. The first picks a product generation; the second picks a stability contract. Read",
        "any version number by first asking which of these four things it is numbering.",
    ], "info")
    body += co
    write("av-01-four-axes.svg", w, h, body, "Four independent meanings of 'version'")


def fig_stages():
    w, h = 940, 500
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Launch stages — what each one actually promises you",
                    15, c.TEXT, "500"))

    ax, ay, aw = 60, 96, 820
    body.append(c.line(ax, ay, ax + aw, ay, c.BORDER, 2))
    stages = [
        (0.02, "Experimental", c.GREY, "a prototype"),
        (0.28, "Preview", c.AMBER, "v1beta1 lives here"),
        (0.56, "GA", c.GREEN, "v1 lives here"),
        (0.82, "Deprecated", c.RED, "12-month notice"),
    ]
    for frac, name, col, sub in stages:
        x = ax + aw * frac
        body.append(c.circle(x, ay, 9, fill=col))
        body.append(c.t(x, ay - 22, name, 11.5, col, "700", "middle"))
        body.append(c.t(x, ay + 26, sub, 9.5, c.GREY, "400", "middle"))
    body.append(c.t(ax + aw, ay - 22, "Decommissioned", 11.5, c.TEXT, "700", "end"))

    rows = [
        ("Experimental", c.GREY, "no", "no", "no",
         "A prototype for feedback. May change or vanish."),
        ("Preview", c.AMBER, "no", "no", "no",
         "Test environments only. Not feature-complete. ~6 months typical."),
        ("GA", c.GREEN, "YES", "YES", "YES",
         "Production-ready. Console, CLI and API support."),
        ("Deprecated", c.RED, "—", "—", "12 mo",
         "Still works; stop using it. At least 12 months before shutdown."),
    ]
    cols = ["Stage", "SLA", "Support", "Deprecation policy", "What it means"]
    widths = [130, 70, 90, 150, 452]
    x, y0 = 24, 160
    total = sum(widths)
    body.append(c.rect(x, y0, total, 30, fill=c.PANEL))
    body.append(c.rect(x, y0, total, 30 + 46 * len(rows), fill="none", stroke=c.BORDER, rx=4))
    cx = x
    for i, hc in enumerate(cols):
        body.append(c.t(cx + 12, y0 + 20, hc, 10.5, c.GREY, "700"))
        if i:
            body.append(c.line(cx, y0, cx, y0 + 30 + 46 * len(rows), c.BORDER, 1, op=.7))
        cx += widths[i]
    body.append(c.line(x, y0 + 30, x + total, y0 + 30, c.BORDER, 1))
    for ri, (name, col, sla, sup, dep, meaning) in enumerate(rows):
        ry = y0 + 30 + 46 * ri
        if ri % 2:
            body.append(c.rect(x, ry, total, 46, fill="#fcfcfd"))
        if ri:
            body.append(c.line(x, ry, x + total, ry, c.BORDER, 1, op=.55))
        body.append(c.t(x + 12, ry + 28, name, 11, col, "700"))
        for k, (val, off) in enumerate([(sla, widths[0]),
                                        (sup, widths[0] + widths[1]),
                                        (dep, widths[0] + widths[1] + widths[2])]):
            vcol = c.GREEN if val == "YES" else (c.RED if val == "no" else c.GREY)
            body.append(c.t(x + off + 12, ry + 28, val, 10.5, vcol, "700"))
        body.append(c.t(x + widths[0] + widths[1] + widths[2] + widths[3] + 12, ry + 28,
                        meaning, 10.5, c.TEXT))

    co, _ = c.callout(24, y0 + 30 + 46 * len(rows) + 18, total, [
        "The line that matters for real work: Preview offerings carry no SLA and no support commitment,",
        "and Google states they are intended for test environments. That is not legal boilerplate — it",
        "means a v1beta1 feature can change shape under you between releases with no notice period.",
    ], "warn")
    body += co
    write("av-02-launch-stages.svg", w, h, body, "Google Cloud launch stages and their guarantees")


def fig_reach():
    w, h = 940, 700
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "How you actually select a version, in each surface",
                    15, c.TEXT, "500"))

    blocks = [
        ("REST endpoint", c.BLUE,
         ["https://LOCATION-aiplatform.googleapis.com/v1/projects/...",
          "https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/..."],
         "The version is a path segment. Nothing else changes."),
        ("Python — high level", c.GREEN,
         ["from google.cloud import aiplatform",
          "aiplatform.Model, aiplatform.PipelineJob, aiplatform.Endpoint"],
         "The curated SDK. Try this first — it is easier and more concise."),
        ("Python — generated (GAPIC)", c.PURPLE,
         ["from google.cloud import aiplatform_v1",
          "from google.cloud import aiplatform_v1beta1"],
         "One package per API version. Drop here only for what the SDK lacks."),
        ("gcloud", c.AMBER,
         ["gcloud ai ...            # GA surface",
          "gcloud beta ai ...       # preview surface"],
         "The release track is the word after gcloud."),
    ]
    y = 66
    for name, col, lines, note in blocks:
        bh = 44 + len(lines) * 20 + 20
        body.append(c.rect(24, y, w - 48, bh, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, bh, fill=col, rx=3))
        body.append(c.t(46, y + 26, name, 12, c.TEXT, "700"))
        for i, ln in enumerate(lines):
            body.append(c.mono(46, y + 50 + i * 20, ln, 10.5, col))
        body.append(c.t(46, y + 54 + len(lines) * 20, note, 10, c.GREY))
        y += bh + 12

    body.append(c.t(24, y + 22, "The order to try things", 12.5, c.TEXT, "700"))
    steps = [
        "1.  google.cloud.aiplatform  — the curated SDK",
        "2.  aiplatform_v1            — generated GA client, if the SDK lacks it",
        "3.  aiplatform_v1beta1       — only if the feature exists nowhere else",
    ]
    for i, ln in enumerate(steps):
        body.append(c.mono(24, y + 46 + i * 18, ln, 10.5,
                           c.GREEN if i == 0 else (c.BLUE if i == 1 else c.AMBER)))

    co, _ = c.callout(24, y + 108, w - 48, [
        "Prefer the stable client unless you need a beta-only feature. Reaching for v1beta1 first is",
        "how preview surface quietly ends up in production code that nobody meant to ship.",
    ], "ok")
    body += co
    write("av-03-selecting.svg", w, h, body, "Selecting an API version in each surface")


if __name__ == "__main__":
    print("Generating API-version figures into %s" % HERE)
    fig_four_axes()
    fig_stages()
    fig_reach()
    print("done.")
