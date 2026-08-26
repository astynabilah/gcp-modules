# -*- coding: utf-8 -*-
"""Diagrams for the Dataproc module.

Run:  python tools/figures/mod_dataproc.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("dataproc")

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


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6, label=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    out = [c.line(x1, y1, hx, hy, col, sw),
           c.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
               x2, y2,
               x2 - 9 * math.cos(ang - 0.42), y2 - 9 * math.sin(ang - 0.42),
               x2 - 9 * math.cos(ang + 0.42), y2 - 9 * math.sin(ang + 0.42)), fill=col)]
    if label:
        out.append(c.t((x1 + x2) / 2, min(y1, y2) - 10, label, 9.5, c.GREY, "500", "middle"))
    return out


# --------------------------------------------------------------------------

def fig_deployments():
    w, h = 940, 540
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Two deployment shapes, and what each costs you",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Now documented as Managed Service for Apache Spark. The CLI "
                            "and property names did not change.", 11, c.GREY))

    body.append(c.rect(24, 84, 440, 236, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 110, "CLUSTER DEPLOYMENT  (Compute Engine)", 10.5, c.BLUE, "700"))
    rows = [
        ("You manage", "masters, workers, autoscaling"),
        ("Startup", "~120 seconds"),
        ("Dependencies", "custom image  /  init actions  /  properties"),
        ("Idle cost", "you pay for uptime, jobs or not"),
        ("Premium", "$0.010 x vCPUs x hours, ON TOP of the VMs"),
        ("Fits", "Hadoop ecosystem, migrations, persistent envs"),
    ]
    y = 128
    for k, v in rows:
        body.append(c.t(44, y + 12, k, 10.5, c.TEXT, "700"))
        body.append(c.t(168, y + 12, v, 10, c.GREY))
        y += 30

    body.append(c.rect(476, 84, 440, 236, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(496, 110, "SERVERLESS DEPLOYMENT", 10.5, c.GREEN, "700"))
    rows2 = [
        ("You manage", "nothing"),
        ("Startup", "~50 seconds"),
        ("Dependencies", "a custom container image"),
        ("Idle cost", "none - you pay per job"),
        ("Billing", "DCUs + accelerators + shuffle storage"),
        ("Fits", "new pipelines, variable and ad-hoc workloads"),
    ]
    y = 128
    for k, v in rows2:
        body.append(c.t(496, y + 12, k, 10.5, c.TEXT, "700"))
        body.append(c.t(620, y + 12, v, 10, c.GREY))
        y += 30

    body.append(c.t(24, 356, "And the question before either of them", 12.5, c.TEXT, "700"))
    body.append(c.rect(24, 372, w - 48, 62, fill="#fff8e6", stroke=c.AMBER, rx=8, sw=1.4))
    body.append(c.rect(24, 372, 5, 62, fill=c.AMBER, rx=2.5))
    body.append(c.t(44, 394, "Could BigQuery have done this?", 11.5, c.TEXT, "700"))
    body.append(c.t(44, 412, "Standing up Spark to do what a CREATE TABLE AS SELECT would "
                             "have done is the most expensive habit here.", 10, c.GREY))
    body.append(c.t(44, 426, "Dataproc earns its place when you have Spark code already, or "
                             "the transform genuinely is not SQL.", 10, c.GREY))

    co, _ = c.callout(24, 448, w - 48, [
        "Dataproc is DATA PROCESSING, not model training. Spark is the right tool for the ETL that",
        "produces your training table and the wrong one for training the model on it. \"Distributed\"",
        "means something different in each context, which is where the confusion comes from.",
    ], "ok")
    body += co
    write("dp-01-deployments.svg", w, h, body,
          "Cluster versus serverless Dataproc deployment")


def fig_deps():
    w, h = 940, 620
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Four ways to get your Python libraries onto a cluster",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Only two of them are production answers, and they are the "
                            "two that install nothing at boot.", 11, c.GREY))

    rows = [
        ("dataproc:pip.packages  /  conda.packages", c.RED, "development only",
         "Downloads from PyPI or conda-forge on EVERY cluster creation.",
         "Startup latency, an external repo in your critical path, and a 10-minute creation timeout."),
        ("Public initialization actions", c.RED, "explicitly warned against",
         "gs://goog-dataproc-initialization-actions-REGION is a reference implementation.",
         "Google: updates to these scripts \"can break your cluster creation\". Copy them to your own bucket."),
        ("A custom image", c.GREEN, "the recommendation",
         "generate_custom_image.py bakes the libraries into a Compute Engine image.",
         "Nothing installs at boot: consistent by construction, and fast every time."),
        ("A custom container", c.GREEN, "serverless and GKE",
         "Dependencies in an image passed with --container-image.",
         "Spark is mounted at runtime - do not install it. Needs procps and tini; runs as UID 1099."),
    ]
    y = 84
    for name, col, tag, l1, l2 in rows:
        body.append(c.rect(24, y, w - 48, 78, fill="#ffffff", stroke=col, rx=8, sw=1.4))
        body.append(c.rect(24, y, 5, 78, fill=col, rx=2.5))
        body.append(c.t(46, y + 26, name, 12, c.TEXT, "700"))
        ch, _cw = c.chip(560, y + 14, tag,
                         fill="#e6f4ea" if col == c.GREEN else "#fce8e6", fg=col)
        body += ch
        body.append(c.t(46, y + 48, l1, 10, c.TEXT))
        body.append(c.t(46, y + 66, l2, 9.5, c.GREY))
        y += 86

    body.append(c.t(24, y + 26, "And pin the image version", 12.5, c.TEXT, "700"))
    body += c.grid(24, y + 42, ["You specify", "You get", "Verdict"],
                   [["nothing", "latest, whatever that becomes", "not for production"],
                    ["2.2", "latest 2.2.x - patches, fixed components", "THE RECOMMENDATION"],
                    ["2.2.65-debian12", "exactly that, forever", "reproducible and unpatched"]],
                   [230, 400, 262],
                   colors={(1, 2): "#e6f4ea"})

    write("dp-02-dependencies.svg", w, h, body,
          "Dependency management options for Dataproc clusters")


if __name__ == "__main__":
    print("Generating Dataproc figures into %s" % HERE)
    fig_deployments()
    fig_deps()
    print("done.")
