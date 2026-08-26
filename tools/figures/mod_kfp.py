import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("kfp")

W = 940
PY, KW, STR, CM = c.TEXT, "#1967d2", "#0d652d", "#9aa0a6"
DEC = "#8430ce"


def write(name, w, h, body, title):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-28s %sx%s" % (name, w, h))


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if len(trial) > width and cur:
            lines.append(cur); cur = wd
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def node(x, y, w, h, title, sub=None, col=c.BLUE, fill="#ffffff", size=11.5):
    out = [c.rect(x, y, w, h, fill=fill, stroke=col, rx=8, sw=1.5)]
    ty = y + h / 2 + (-5 if sub else 4)
    out.append(c.t(x + w / 2, ty, title, size, c.TEXT, "500", "middle"))
    if sub:
        out.append(c.t(x + w / 2, y + h / 2 + 12, sub, 9.5, c.GREY, "400", "middle"))
    return out


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6, label=None, dash=None):
    import math
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


def fig_anatomy():
    w, h = 940, 470
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "What actually happens when you 'run a pipeline'",
                    14.5, c.TEXT, "500"))
    body.append(c.t(24, 56, "Your Python never runs on Vertex. It runs once, locally, to "
                            "produce a YAML description of a DAG.", 11, c.GREY))

    # local side
    body.append(c.rect(24, 80, 400, 300, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.3, op=0.9))
    body.append(c.t(40, 102, "YOUR MACHINE  (or Cloud Shell)", 9.5, c.BLUE, "600"))

    lines = [
        [("@dsl.component", DEC)],
        [("def", KW), (" train(data: Input[Dataset],", PY)],
        [("          model: Output[Model]):", PY)],
        [("    ", PY), ("# plain python", CM)],
        [("", PY)],
        [("@dsl.pipeline", DEC)],
        [("def", KW), (" churn_pipeline():", PY)],
        [("    d = extract()", PY)],
        [("    m = train(data=d.outputs[", PY), ("'out'", STR), ("])", PY)],
    ]
    blk = []
    for i, spans in enumerate(lines):
        cx = 44
        for txt, col in spans:
            blk.append(c.mono(cx, 132 + i * 16, txt, 10.5, col))
            cx += len(txt) * 6.1
    body += blk

    body += node(44, 296, 168, 44, "compiler.compile()", col=c.BLUE)
    body += node(236, 296, 168, 44, "pipeline.yaml", "the IR — a DAG spec", col=c.BLUE)
    body += arrow(212, 318, 236, 318, col=c.BLUE)

    # remote side
    body.append(c.rect(452, 80, 464, 300, fill="#faf5ff", stroke=DEC, rx=10, sw=1.3, op=0.9))
    body.append(c.t(468, 102, "VERTEX AI PIPELINES  (Agent Platform)", 9.5, DEC, "600"))

    body += arrow(424, 318, 452, 318, col=DEC, label=None)
    body.append(c.t(438, 300, "submit", 8.5, c.GREY, "500", "middle"))

    steps = [("extract", 476), ("train", 616), ("evaluate", 756)]
    for name, x in steps:
        body += node(x, 132, 124, 52, name, "one container", col=DEC)
    body += arrow(600, 158, 616, 158, col=DEC)
    body += arrow(740, 158, 756, 158, col=DEC)

    for name, x in steps:
        body.append(c.rect(x + 18, 214, 88, 34, fill=c.AMBER, rx=6, op=0.16))
        body.append(c.t(x + 62, 235, "artifact", 9.5, c.AMBER, "600", "middle"))
        body += arrow(x + 62, 186, x + 62, 212, col=c.AMBER, sw=1.3)

    body.append(c.rect(476, 276, 404, 44, fill="#ffffff", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.t(678, 296, "ML Metadata — lineage, params, artifacts, cached runs",
                    10.5, c.TEXT, "500", "middle"))
    body.append(c.t(678, 310, "every run recorded and comparable", 9, c.GREY, "400", "middle"))
    for _, x in steps:
        body.append(c.line(x + 62, 248, x + 62, 276, c.GREEN, 1.2, dash="3 3"))

    co, _ = c.callout(24, 396, w - 48, [
        "Each component becomes its own container on its own machine. That is the source of both the",
        "power (independent scaling, any language, cached steps) and the friction (cold starts, "
        "everything crossing a boundary must be serialisable).",
    ], "info")
    body += co
    write("k-01-anatomy.svg", w, h, body, "Anatomy of a Vertex AI Pipelines run")


def fig_data():
    w, h = 940, 430
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Parameters vs. Artifacts — the distinction that trips everyone up",
                    14.5, c.TEXT, "500"))

    cols = [
        ("Parameter", c.BLUE, "small values, by value",
         ["int, float, str, bool,", "list, dict", "",
          "Stored in ML Metadata.", "Visible in the run UI.", "Comparable across runs.", "",
          "Use for: config, dates,", "thresholds, table names."]),
        ("Artifact", c.AMBER, "big things, by reference",
         ["Dataset, Model, Metrics,", "HTML, Markdown", "",
          "Stored in Cloud Storage.", "Passed as a PATH, not", "as the bytes.", "",
          "Use for: files, model", "weights, dataframes."]),
    ]
    for i, (name, col, sub, lines) in enumerate(cols):
        x = 24 + i * 452
        body.append(c.rect(x, 66, 436, 250, fill="#ffffff", stroke=col, rx=10, sw=1.6))
        body.append(c.rect(x, 66, 436, 48, fill=col, rx=10, op=0.13))
        body.append(c.rect(x, 104, 436, 10, fill="#ffffff"))
        body.append(c.t(x + 20, 90, name, 13, c.TEXT, "600"))
        body.append(c.t(x + 20, 106, sub, 9.5, col, "600"))
        for j, ln in enumerate(lines):
            body.append(c.t(x + 20, 138 + j * 17, ln, 10.5,
                            c.TEXT if j < 2 else c.GREY))

    body.append(c.rect(486, 208, 200, 26, fill="#ffffff"))
    code = [
        ("def clean(", PY), ("src: str", KW), (",", PY),
    ]
    body.append(c.mono(500, 226, "src: str            # parameter", 10, c.BLUE))
    body.append(c.mono(500, 244, "out: Output[Dataset] # artifact", 10, c.AMBER))

    co, _ = c.callout(24, 336, w - 48, [
        "The rule: a parameter is passed BY VALUE and shows up in the run comparison UI; an artifact is",
        "passed BY REFERENCE and you read/write its .path. Returning a 2 GB DataFrame as a parameter is",
        "the single most common KFP mistake — it serialises through metadata and the run falls over.",
    ], "warn")
    body += co
    write("k-02-params-artifacts.svg", w, h, body, "Parameters versus artifacts in KFP")


def fig_decision():
    w, h = 940, 578
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Do you need a pipeline at all? — pick the lightest thing that works",
                    14.5, c.TEXT, "500"))

    rows = [
        ("Scheduled query", c.GREEN, "BigQuery",
         "One SQL statement on a timer.",
         "Zero infrastructure. Free between runs.",
         "No branching, no non-SQL steps, no lineage."),
        ("Workflows", c.TEAL, "Cloud Workflows",
         "A few API calls in sequence, with retries.",
         "Serverless, cheap, YAML.",
         "Not ML-aware: no artifacts, no caching, no experiment tracking."),
        ("Vertex AI Pipelines", DEC, "managed KFP",
         "ML DAG: training, evaluation, conditional deploy.",
         "Artifact lineage, step caching, run comparison, per-step machines.",
         "Python and containers. ~$0.03/run + compute. Cold starts per step."),
        ("Cloud Composer", c.AMBER, "managed Airflow",
         "Broad data orchestration across many systems.",
         "Huge operator ecosystem, mature scheduling.",
         "A cluster that runs — and bills — 24/7."),
    ]
    y = 66
    for name, col, sub, use, pro, con in rows:
        body.append(c.rect(24, y, w - 48, 96, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, 96, fill=col, rx=3))
        body.append(c.t(44, y + 26, name, 12.5, c.TEXT, "600"))
        body.append(c.t(44 + len(name) * 7.4 + 12, y + 26, sub, 9.5, col, "600"))
        body.append(c.t(44, y + 46, use, 10.5, c.TEXT))
        body.append(c.t(44, y + 66, "+  " + pro, 10, c.GREEN))
        body.append(c.t(44, y + 84, "−  " + con, 10, c.RED))
        y += 106

    co, _ = c.callout(24, y + 4, w - 48, [
        "Read top to bottom and stop at the first row that fits. Most teams reach for row 3 when row 1",
        "would have done — a pipeline is worth its overhead when you have real branching, expensive",
        "steps worth caching, or a compliance need to prove which data produced which model.",
    ], "ok")
    body += co
    write("k-03-when-to-use.svg", w, h, body, "Choosing an orchestrator on Google Cloud")


def fig_resources():
    w, h = 940, 648
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Where machine resources are configured — and where they are not",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Three places look plausible. Only one of them accepts resource "
                            "settings.", 11, c.GREY))

    bands = [
        ("@dsl.component(...)", c.RED, "NO",
         "Defines WHAT runs: base_image, packages_to_install, target_image.",
         ["There is no gpu_limit, gpu_type or accelerator argument here.",
          "The decorator describes the component; resources belong to the task."]),
        ("task = train(...)   inside @dsl.pipeline", c.GREEN, "YES",
         "The DAG node. This is where per-step resources live.",
         [".set_cpu_limit('8')          .set_memory_limit('32G')",
          ".set_accelerator_type('NVIDIA_TESLA_T4')   .set_accelerator_limit(1)",
          ".set_retry(...)   .set_caching_options(...)   .set_env_variable(...)"]),
        ("aiplatform.PipelineJob(...)", c.RED, "NO",
         "Submission-level only: parameter_values, enable_caching, service_account, labels.",
         ["There is no machine_spec parameter, and nothing global for resources.",
          "Per-step sizing is the whole point — a global setting would defeat it."]),
    ]
    y = 78
    for name, col, verdict, what, lines in bands:
        bh = 118
        body.append(c.rect(24, y, w - 48, bh, fill="#ffffff", stroke=col, rx=9, sw=1.5))
        body.append(c.rect(24, y, 6, bh, fill=col, rx=3))
        body.append(c.mono(46, y + 26, name, 11.5, c.TEXT))
        ch, cw = c.chip(w - 96, y + 14, verdict, fill=col, fg=col, h=20)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 48, what, 10.5, c.GREY))
        for i, ln in enumerate(lines):
            body.append(c.mono(46, y + 72 + i * 15, ln, 10,
                               c.TEXT if col == c.GREEN else c.GREY))
        y += bh + 12

    body.append(c.rect(24, y, w - 48, 84, fill="#fffaf0", stroke=c.AMBER, rx=9, sw=1.5))
    body.append(c.rect(24, y, 6, 84, fill=c.AMBER, rx=3))
    body.append(c.mono(46, y + 26, "create_custom_training_job_from_component(...)", 11.5, c.TEXT))
    ch, cw = c.chip(w - 150, y + 14, "when you need MORE", fill=c.AMBER, fg=c.AMBER, h=20)
    ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
    body += ch
    body.append(c.t(46, y + 48, "Wraps a component as a Vertex custom training job.", 10.5, c.GREY))
    body.append(c.mono(46, y + 68, "Use for an EXACT machine_type, reservations, TPUs, or a "
                                   "custom service account.", 10, c.GREY))

    co, _ = c.callout(24, y + 96, w - 48, [
        "set_cpu_limit / set_memory_limit express a MINIMUM — Vertex picks a machine that satisfies",
        "them. If you must land on a specific machine type, that is the one thing the chained methods",
        "cannot do, and the reason the custom-training wrapper exists.",
    ], "info")
    body += co
    write("k-04-resources.svg", w, h, body,
          "Where per-step machine resources are configured in KFP")


if __name__ == "__main__":
    print("Generating KFP module figures into %s" % HERE)
    fig_anatomy()
    fig_data()
    fig_decision()
    fig_resources()
    print("done.")
