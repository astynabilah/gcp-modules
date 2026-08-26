# -*- coding: utf-8 -*-
"""Diagrams for the BigQuery ML data validation module.

Run:  python tools/figures/mod_bqvalidate.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("bqvalidate")

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
        out.append(c.t((x1 + x2) / 2, min(y1, y2) - 10, label, 9.5, c.GREY, "500", "middle"))
    return out


# --------------------------------------------------------------------------

def fig_five():
    w, h = 940, 660
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Five functions: two describe, three validate",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "All GA since 19 September 2024. What each one takes and "
                            "what it hands back.", 11, c.GREY))

    # describe row
    body.append(c.rect(24, 82, 440, 218, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 108, "DESCRIBE  -  compute statistics", 10.5, c.BLUE, "700"))

    body += node(44, 126, 190, 70, "ML.DESCRIBE_DATA", "a table or query", col=c.BLUE)
    body += node(254, 126, 190, 70, "one row per column", "readable: nulls, min,", col=c.GREEN,
                 fill="#f2fbf5")
    body.append(c.t(349, 186, "max, mean, quantiles", 9.5, c.GREY, "400", "middle"))
    body += arrow(234, 161, 254, 161, col="#bdc1c6", sw=1.4)

    body += node(44, 212, 190, 70, "ML.TFDV_DESCRIBE", "a table or query", col=c.BLUE)
    body += node(254, 212, 190, 70, "ONE JSON blob", "a TFDV protobuf,", col=c.AMBER,
                 fill="#fff8e6")
    body.append(c.t(349, 272, "not per-column rows", 9.5, c.GREY, "400", "middle"))
    body += arrow(234, 247, 254, 247, col="#bdc1c6", sw=1.4)

    # validate
    body.append(c.rect(476, 82, 440, 218, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(496, 108, "VALIDATE  -  compare and flag", 10.5, c.GREEN, "700"))

    body += node(496, 126, 200, 46, "ML.VALIDATE_DATA_SKEW", None, col=c.GREEN)
    body.append(c.t(716, 144, "MODEL  +  serving table", 10, c.TEXT, "500"))
    body.append(c.t(716, 160, "training stats live in the model", 9.5, c.GREY))

    body += node(496, 182, 200, 46, "ML.VALIDATE_DATA_DRIFT", None, col=c.GREEN)
    body.append(c.t(716, 200, "two tables, no model", 10, c.TEXT, "500"))
    body.append(c.t(716, 216, "any two windows of data", 9.5, c.GREY))

    body += node(496, 238, 200, 46, "ML.TFDV_VALIDATE", None, col=c.AMBER)
    body.append(c.t(716, 256, "two JSON stats blobs", 10, c.TEXT, "500"))
    body.append(c.t(716, 272, "returns an Anomalies protobuf", 9.5, c.GREY))

    body.append(c.t(24, 336, "The output that is actually useful", 12.5, c.TEXT, "700"))
    body += c.grid(24, 352, ["input", "metric", "threshold", "value", "is_anomaly"],
                   [["tenure_months", "JENSEN_SHANNON_DIVERGENCE", "0.3", "0.041", "false"],
                    ["monthly_charges", "JENSEN_SHANNON_DIVERGENCE", "0.3", "0.088", "false"],
                    ["contract", "L_INFTY", "0.2", "0.310", "TRUE"],
                    ["payment_method", "L_INFTY", "0.2", "0.052", "false"]],
                   [200, 300, 130, 130, 132],
                   colors={(2, 4): "#fce8e6"})

    body.append(c.t(24, 502, "is_anomaly is just  value > threshold.  Nothing cleverer.",
                    10.5, c.GREY, "500"))

    co, _ = c.callout(24, 526, w - 48, [
        "ML.TFDV_VALIDATE is the family's odd one out: it takes POSITIONAL arguments, not a STRUCT,",
        "and supplying any optional argument means supplying every argument before it. Its",
        "detection_type accepts exactly two values - 'SKEW' and 'DRIFT'. There is no 'STATS'.",
        "Unless you need TFDV artifacts, the two VALIDATE_DATA_* functions give you rows instead.",
    ], "warn")
    body += co
    write("dv-01-five-functions.svg", w, h, body,
          "The five BigQuery ML data validation functions")


def fig_metrics():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Same metrics as Vertex AI Model Monitoring, reached from SQL",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Not a coincidence - the visualization links point into the "
                            "same console.", 11, c.GREY))

    body.append(c.rect(24, 84, 440, 200, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 110, "NUMERICAL COLUMNS", 10.5, c.BLUE, "700"))
    body += node(44, 128, 400, 56, "JENSEN_SHANNON_DIVERGENCE", "the only allowed value",
                 col=c.BLUE)
    body.append(c.t(244, 212, "You cannot change it. Numerical distributions can be", 10,
                    c.GREY, "400", "middle"))
    body.append(c.t(244, 228, "binned and ordered, so a divergence measure applies.", 10,
                    c.GREY, "400", "middle"))
    body.append(c.t(244, 258, "default threshold  0.3", 11, c.TEXT, "700", "middle"))

    body.append(c.rect(476, 84, 440, 200, fill="#faf5ff", stroke=c.PURPLE, rx=10, sw=1.6))
    body.append(c.t(496, 110, "CATEGORICAL COLUMNS", 10.5, c.PURPLE, "700"))
    body += node(496, 128, 196, 56, "L_INFTY", "the default", col=c.PURPLE)
    body += node(712, 128, 196, 56, "JENSEN_SHANNON", "optional override", col=c.GREY)
    body.append(c.t(696, 212, "No order, no distance - north is not closer to south", 10,
                    c.GREY, "400", "middle"))
    body.append(c.t(696, 228, "than to west. All you have is proportions.", 10,
                    c.GREY, "400", "middle"))
    body.append(c.t(696, 258, "default threshold  0.3", 11, c.TEXT, "700", "middle"))

    body.append(c.t(24, 324, "Skew or drift - the maths is identical, the baseline is not",
                    12.5, c.TEXT, "700"))

    body += node(40, 348, 210, 60, "training statistics", "stored in the MODEL",
                 col=c.GREEN, fill="#f2fbf5")
    body += node(365, 348, 210, 60, "current serving data", None, col=c.BLUE, fill="#f8fbff")
    body += node(690, 348, 210, 60, "an earlier window", "another TABLE",
                 col=c.AMBER, fill="#fff8e6")
    body += arrow(250, 378, 365, 378, col=c.GREEN, sw=1.8, label="SKEW")
    body += arrow(690, 378, 575, 378, col=c.AMBER, sw=1.8, label="DRIFT")

    body.append(c.t(470, 434, "VALIDATE_DATA_SKEW needs the model, not the training table.",
                    10.5, c.GREY, "500", "middle"))
    body.append(c.t(470, 450, "VALIDATE_DATA_DRIFT needs no model at all.",
                    10.5, c.GREY, "500", "middle"))

    co, _ = c.callout(24, 474, w - 48, [
        "Models created before 28 March 2024, or with WARM_START, carry no stored training",
        "statistics - skew detection cannot work on them and nothing can backfill it. Retrain.",
    ], "warn")
    body += co
    write("dv-02-metrics.svg", w, h, body,
          "Jensen-Shannon for numerical, L-infinity for categorical")


if __name__ == "__main__":
    print("Generating BQ validation figures into %s" % HERE)
    fig_five()
    fig_metrics()
    print("done.")
