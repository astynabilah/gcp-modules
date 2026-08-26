# -*- coding: utf-8 -*-
"""Diagrams for the Vertex AI batch prediction module.

Run:  python tools/figures/mod_batchpred.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("batchpred")

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

def fig_colocation():
    w, h = 940, 620
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Three things have a location, and they all have to agree",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Input data, the model, and the output destination. "
                            "A job is only as fast as its worst mismatch.", 11, c.GREY))

    # --- broken
    body.append(c.rect(24, 78, 440, 218, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.6))
    body.append(c.t(44, 102, "MISMATCHED", 10.5, c.RED, "700"))

    body += node(44, 118, 178, 50, "Input JSONL", "us-central1", col=c.RED)
    body += node(266, 118, 178, 50, "Model", "us-west1", col=c.RED)
    body += node(155, 196, 178, 50, "Output bucket", "us-central1", col=c.RED)
    body += arrow(222, 143, 266, 143, col=c.RED, sw=1.6)
    body.append(c.t(244, 274, "cross-region reads on every batch — slow, and not "
                              "guaranteed to work", 10, c.RED, "700", "middle"))

    # --- fixed
    body.append(c.rect(476, 78, 440, 218, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(496, 102, "COLOCATED", 10.5, c.GREEN, "700"))

    body += node(496, 118, 178, 50, "Input JSONL", "us-west1", col=c.GREEN)
    body += node(718, 118, 178, 50, "Model", "us-west1", col=c.GREEN)
    body += node(607, 196, 178, 50, "Output bucket", "us-west1  or  US", col=c.GREEN)
    body += arrow(674, 143, 718, 143, col=c.GREEN, sw=1.6)
    body.append(c.t(696, 274, "copy the data to the model, or re-register the model "
                              "by the data", 10, c.GREEN, "700", "middle"))

    body.append(c.t(24, 340, "What counts as \"the same place\"", 12.5, c.TEXT, "700"))
    body += c.grid(24, 356, ["Model is in", "Input may be in", "Output may be in", "Not"],
                   [["us-west1", "us-west1", "us-west1  ·  US", "us-central1, EU, ..."],
                    ["us-central1", "us-central1", "us-central1  ·  US", "us-west1, europe-west4"],
                    ["europe-west4", "europe-west4", "europe-west4  ·  EU", "US, us-central1"]],
                   [176, 200, 260, 260])

    co, _ = c.callout(24, 500, w - 48, [
        "A region is inside its multi-region: a us-west1 model may write to a US bucket. The reverse",
        "does not hold - US is not inside us-west1 - and two regions in the same continent are still",
        "two regions. The global endpoint is not an escape hatch here: custom-trained models do not",
        "support it for batch prediction, so there is no \"just let Google sort it out\" option.",
    ], "warn")
    body += co
    write("bp-01-colocation.svg", w, h, body,
          "Input, model and output must share a region or multi-region")


def fig_choose():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Batch or online — the question is who is waiting",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Not how much data. A million rows nobody is waiting for is "
                            "batch; one row a user is waiting for is online.", 11, c.GREY))

    body.append(c.rect(24, 80, 440, 250, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.5))
    body.append(c.t(44, 106, "BATCH PREDICTION", 11, c.BLUE, "700"))
    rows = [
        ("Nobody is blocked", "a scoring table read tomorrow morning"),
        ("No endpoint", "no machine sitting idle, no hourly bill"),
        ("Input", "Cloud Storage JSONL / CSV, or a BigQuery table"),
        ("Output", "Cloud Storage JSONL, or a BigQuery table"),
        ("Scales by", "starting_replica_count - max is ignored"),
        ("You pay", "only for the minutes the job runs"),
    ]
    y = 124
    for k, v in rows:
        body.append(c.t(44, y + 12, k, 10.5, c.TEXT, "700"))
        body.append(c.t(196, y + 12, v, 10, c.GREY))
        y += 32

    body.append(c.rect(476, 80, 440, 250, fill="#faf5ff", stroke=c.PURPLE, rx=10, sw=1.5))
    body.append(c.t(496, 106, "ONLINE PREDICTION", 11, c.PURPLE, "700"))
    rows2 = [
        ("Someone is waiting", "a page render, an app screen, a decision"),
        ("Endpoint required", "a machine is up whether called or not"),
        ("Input", "one request, JSON instances"),
        ("Output", "the response body"),
        ("Scales by", "min/max replicas on a duty-cycle target"),
        ("You pay", "per node-hour, around the clock"),
    ]
    y = 124
    for k, v in rows2:
        body.append(c.t(496, y + 12, k, 10.5, c.TEXT, "700"))
        body.append(c.t(648, y + 12, v, 10, c.GREY))
        y += 32

    body.append(c.t(24, 366, "And the third option people forget", 12.5, c.TEXT, "700"))
    body.append(c.rect(24, 382, w - 48, 62, fill="#f2fbf5", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.rect(24, 382, 5, 62, fill=c.GREEN, rx=2.5))
    body.append(c.t(44, 404, "The model already lives in BigQuery", 11.5, c.TEXT, "700"))
    body.append(c.t(44, 424, "ML.PREDICT over a table is batch scoring with no job, no "
                             "export, no region to match. If the data is in BigQuery and the "
                             "model is BQML, that is the batch story.", 10, c.GREY))

    co, _ = c.callout(24, 458, w - 48, [
        "Batch prediction is not \"online prediction for lots of rows\". It is a different service with",
        "its own job resource, and it does not need an endpoint at all - which is why it costs nothing",
        "between runs. Deploying to an endpoint so you can loop over it is the expensive mistake.",
    ], "ok")
    body += co
    write("bp-02-batch-vs-online.svg", w, h, body,
          "Choosing between batch and online prediction")


if __name__ == "__main__":
    print("Generating batch prediction figures into %s" % HERE)
    fig_colocation()
    fig_choose()
    print("done.")
