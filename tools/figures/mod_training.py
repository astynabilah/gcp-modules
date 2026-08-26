import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("training")

W = 940


def write(name, w, h, body, title):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-30s %sx%s" % (name, w, h))


def node(x, y, w, h, title, sub=None, col=c.BLUE, fill="#ffffff", size=11.5):
    out = [c.rect(x, y, w, h, fill=fill, stroke=col, rx=8, sw=1.5)]
    ty = y + h / 2 + (-5 if sub else 4)
    out.append(c.t(x + w / 2, ty, title, size, c.TEXT, "500", "middle"))
    if sub:
        out.append(c.t(x + w / 2, y + h / 2 + 12, sub, 9.5, c.GREY, "400", "middle"))
    return out


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

def fig_places():
    w, h = 940, 600
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Five places model training can actually run", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "They are not tiers of sophistication. They are different answers "
                            "to 'where does the compute live?'", 11, c.GREY))

    rows = [
        ("BigQuery ML", c.BLUE, "CREATE MODEL",
         "Inside the warehouse. No container, no cluster, no machine to pick.",
         "Tabular problems on data already in BigQuery. Labs 2 and 5."),
        ("The notebook kernel", c.GREY, "Workbench / Colab",
         "On the VM your notebook is running on. Interactive, and capped by that VM.",
         "Prototyping. Where you start, and where you should stop."),
        ("The notebook executor", c.GREEN, "Workbench -> custom training",
         "Submits the .ipynb itself as a training job on different hardware.",
         "Scaling up WITHOUT leaving the notebook. The bridge."),
        ("A custom training job", c.PURPLE, "CustomJob / worker pools",
         "Your container, your machines, up to four worker pools.",
         "Distributed training, long runs, anything reproducible."),
        ("A pipeline step", c.AMBER, "Vertex AI Pipelines",
         "The same custom training, wrapped as a DAG node.",
         "When training is one step among many. See the KFP module."),
    ]
    y = 78
    for name, col, tag, what, when in rows:
        body.append(c.rect(24, y, w - 48, 82, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, 82, fill=col, rx=3))
        body.append(c.t(46, y + 26, name, 12.5, c.TEXT, "700"))
        ch, cw = c.chip(46 + len(name) * 7.6 + 14, y + 14, tag, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 48, what, 10.5, c.GREY))
        body.append(c.t(46, y + 68, when, 10.5, c.TEXT))
        y += 90

    co, _ = c.callout(24, y + 4, w - 48, [
        "The jump people find hardest is row 2 to row 4 — from 'it runs in my notebook' to 'it runs",
        "in a container somewhere else'. Row 3 exists precisely to make that jump smaller.",
    ], "info")
    body += co
    write("tr-01-where-training-runs.svg", w, h, body,
          "Five places model training can run on Google Cloud")


def fig_executor():
    w, h = 940, 520
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Two ways to get more GPUs — only one of them scales",
                    15, c.TEXT, "500"))

    # --- resize the instance
    body.append(c.rect(24, 62, 440, 250, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.5))
    body.append(c.t(44, 86, "RESIZE THE INSTANCE", 10.5, c.RED, "700"))
    body.append(c.t(44, 104, "Stop it, change the machine type, start it again.", 10, c.GREY))

    body += node(44, 122, 130, 46, "Stop", "you are idle", col=c.GREY)
    body += node(198, 122, 130, 46, "Resize", "bigger GPU", col=c.RED)
    body += node(352, 122, 90, 46, "Start", None, col=c.GREY)
    body += arrow(174, 145, 198, 145, col=c.RED)
    body += arrow(328, 145, 352, 145, col=c.RED)

    for i, ln in enumerate([
        "Works, but:",
        "•  the instance must be shut down to change it",
        "•  G2 <-> non-G2 changes are NOT supported at all",
        "•  you now pay A100 rates while you edit cells",
        "•  one machine — no distributed training, ever",
    ]):
        body.append(c.t(44, 196 + i * 20, ln, 10.5,
                        c.RED if i == 0 else c.GREY, "700" if i == 0 else "400"))

    # --- executor
    body.append(c.rect(476, 62, 440, 250, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.5))
    body.append(c.t(496, 86, "THE NOTEBOOK EXECUTOR", 10.5, c.GREEN, "700"))
    body.append(c.t(496, 104, "Submit the notebook itself as a training job.", 10, c.GREY))

    body += node(496, 122, 150, 46, "Your notebook", "small, cheap", col=c.GREY)
    body += node(700, 122, 196, 46, "Custom training", "8x A100, distributed", col=c.GREEN)
    body += arrow(646, 145, 700, 145, col=c.GREEN)
    body.append(c.t(673, 137, "submit", 8.5, c.GREY, "600", "middle"))
    body.append(c.path("M 796 168 C 796 186 570 186 570 168", stroke=c.GREEN, sw=1.5,
                       dash="4 4"))
    body.append(c.t(683, 196, "results come back to the notebook", 9.5, c.GREEN, "600",
                    "middle"))

    for i, ln in enumerate([
        "Because:",
        "•  the .ipynb is the job — no export to .py needed",
        "•  hardware is chosen per RUN, not per instance",
        "•  your Workbench VM stays small and cheap",
        "•  one-off or scheduled; distributed training available",
    ]):
        body.append(c.t(496, 216 + i * 20, ln, 10.5,
                        c.GREEN if i == 0 else c.GREY, "700" if i == 0 else "400"))

    co, _ = c.callout(24, 332, w - 48, [
        "The executor's real trick is decoupling: the machine you EDIT on and the machine you TRAIN on",
        "stop being the same machine. That is why resizing feels wrong once you have seen it — you were",
        "paying training prices for an editor.",
    ], "ok")
    body += co

    co2, _ = c.callout(24, 412, w - 48, [
        "One limitation to know: the executor is NOT supported on Workbench instances that use VPC",
        "Service Controls. In a locked-down environment you are back to submitting a custom training",
        "job directly — which is the same destination, just without the notebook-shaped front door.",
    ], "warn")
    body += co2
    write("tr-02-executor.svg", w, h, body,
          "Resizing the instance versus using the notebook executor")


def fig_workerpools():
    w, h = 940, 500
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "What 'distributed training' looks like — up to four worker pools",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "A custom training job is a set of machine groups. Each pool has a "
                            "job.", 11, c.GREY))

    pools = [
        ("Pool 0", "Primary replica", "replica_count = 1 — always exactly one.\n"
         "The chief: coordinates and usually checkpoints.", c.BLUE),
        ("Pool 1", "Workers", "The rest of the training machines.\n"
         "1 primary + 7 workers = 8 GPU workers.", c.PURPLE),
        ("Pool 2", "Reduction Server\nor parameter servers", "Reducers for the all-reduce step.\n"
         "Cheap CPU machines — bandwidth is what matters.", c.AMBER),
        ("Pool 3", "Evaluators", "Optional. Runs evaluation\nalongside training.", c.GREEN),
    ]
    x = 28
    for tag, name, desc, col in pools:
        body.append(c.rect(x, 82, 214, 168, fill="#ffffff", stroke=col, rx=10, sw=1.6))
        body.append(c.rect(x, 82, 214, 34, fill=col, rx=10, op=0.14))
        body.append(c.rect(x, 108, 214, 8, fill="#ffffff"))
        body.append(c.t(x + 14, 104, tag, 11, col, "700"))
        for j, ln in enumerate(name.split("\n")):
            body.append(c.t(x + 107, 136 + j * 15, ln, 11.5, c.TEXT, "600", "middle"))
        yy = 136 + len(name.split("\n")) * 15 + 12
        for j, ln in enumerate(desc.split("\n")):
            body.append(c.t(x + 14, yy + j * 15, ln, 9.5, c.GREY))
        x += 226

    body.append(c.t(24, 288, "Reduction Server, in one sentence", 12.5, c.TEXT, "600"))
    for i, ln in enumerate([
        "In data-parallel training every worker computes gradients, and then they all have to agree on "
        "the average.",
        "That all-reduce step is network-bound, not GPU-bound. Reduction Server adds cheap CPU machines "
        "whose only",
        "job is doing that averaging efficiently — raising throughput and cutting latency without adding "
        "a single GPU.",
    ]):
        body.append(c.t(24, 310 + i * 18, ln, 10.5, c.GREY))

    co, _ = c.callout(24, 376, w - 48, [
        "Before you reach for any of this: one machine with several GPUs is simpler than several machines",
        "with one GPU each, and it avoids the network entirely. Scale up before you scale out. Multi-node",
        "is for when the model or the data genuinely will not fit on one box — not for a faster epoch.",
    ], "warn")
    body += co
    write("tr-03-worker-pools.svg", w, h, body,
          "The four worker pools of a Vertex AI custom training job")


def fig_hpt():
    w, h = 940, 720
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Hyperparameter tuning: two channels your code must implement",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Neither is automatic, and each has a plausible-sounding "
                            "wrong answer.", 11, c.GREY))

    body += node(390, 92, 200, 52, "HyperparameterTuningJob", "Bayesian search",
                 col=c.PURPLE, fill="#faf5ff")
    body += node(390, 300, 200, 52, "your training container", "one trial",
                 col=c.BLUE, fill="#f8fbff")

    body.append(c.line(390, 118, 300, 118, c.GREEN, 2))
    body.append(c.line(300, 118, 300, 326, c.GREEN, 2))
    body.append(c.line(300, 326, 384, 326, c.GREEN, 2))
    body.append(c.path("M 390 326 L 382 320 L 382 332 Z", fill=c.GREEN))
    body.append(c.rect(40, 168, 236, 100, fill="#f2fbf5", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.t(158, 192, "IN: command-line arguments", 10.5, c.GREEN, "700", "middle"))
    body.append(c.mono(56, 218, "--learning-rate 0.031", 11, c.TEXT))
    body.append(c.mono(56, 238, "--num-layers 5", 11, c.TEXT))
    body.append(c.t(158, 258, "argparse. That is the whole mechanism.",
                    9.5, c.GREY, "400", "middle"))

    body.append(c.line(590, 326, 700, 326, c.AMBER, 2))
    body.append(c.line(700, 326, 700, 118, c.AMBER, 2))
    body.append(c.line(700, 118, 596, 118, c.AMBER, 2))
    body.append(c.path("M 590 118 L 598 112 L 598 124 Z", fill=c.AMBER))
    body.append(c.rect(722, 168, 194, 100, fill="#fff8e6", stroke=c.AMBER, rx=8, sw=1.4))
    body.append(c.t(819, 192, "OUT: cloudml-hypertune", 10.5, c.AMBER, "700", "middle"))
    body.append(c.mono(736, 218, "hpt.report_hyper", 10.5, c.TEXT))
    body.append(c.mono(736, 238, "parameter_tuning_metric", 10.5, c.TEXT))
    body.append(c.t(819, 258, "tag must match metric_spec", 9.5, c.GREY, "400", "middle"))

    body.append(c.t(24, 396, "Four ways people expect it to work, and it does not",
                    12.5, c.TEXT, "700"))
    rows = [
        ("Environment variables", c.RED,
         "Vertex passes hyperparameter values on the COMMAND LINE."),
        ("TF_CONFIG", c.RED,
         "That is the DISTRIBUTED TRAINING cluster spec - chief, workers. Different thing."),
        ("A config file Vertex writes per trial", c.RED,
         "No such file is generated. Nothing appears in your container to read."),
        ("Metrics scraped from Cloud Logging", c.RED,
         "Nothing reads your logs. cloudml-hypertune is the only channel."),
    ]
    y = 414
    for name, col, desc in rows:
        body.append(c.rect(24, y, w - 48, 44, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 44, fill=col, rx=2.5))
        body.append(c.t(44, y + 27, name, 11.5, c.TEXT, "700"))
        body.append(c.t(330, y + 27, desc, 10, c.GREY))
        y += 50

    co, _ = c.callout(24, y + 6, w - 48, [
        "And the container chooses itself: a proprietary library that is not pip-installable from a",
        "prebuilt image forces a custom one. Bake dependencies into the image rather than installing",
        "them at job start - install-at-runtime is a dev convenience and a production failure mode.",
    ], "warn")
    body += co
    write("tr-04-hyperparameter-tuning.svg", w, h, body,
          "How Vertex AI passes hyperparameters and receives metrics")


if __name__ == "__main__":
    print("Generating training-compute figures into %s" % HERE)
    fig_places()
    fig_executor()
    fig_workerpools()
    fig_hpt()
    print("done.")
