import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("fairness")

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

def fig_where():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Two bias checks, two places in the pipeline", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "They answer different questions, and you want both — one cannot "
                            "substitute for the other.", 11, c.GREY))

    pipeline = [
        ("Training data", None, c.GREY, 30),
        ("Train model", None, c.BLUE, 224),
        ("Batch predict", None, c.BLUE, 418),
        ("Deploy", None, c.PURPLE, 612),
        ("Monitor", "drift / skew", c.TEAL, 782),
    ]
    for name, sub, col, x in pipeline:
        wd = 138 if x < 700 else 134
        body += node(x, 96, wd, 50, name, sub, col=col)
        if x < 700:
            body += arrow(x + wd, 121, x + wd + 18, 121, col="#bdc1c6")
    body += arrow(746, 121, 782, 121, col="#bdc1c6")

    # data bias
    body.append(c.rect(24, 186, 440, 200, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.mono(44, 212, "DetectDataBiasOp", 12.5, c.BLUE))
    body.append(c.t(44, 232, "Runs BEFORE training, on the raw data and true labels.",
                    10.5, c.TEXT))
    body.append(c.line(99, 146, 99, 184, c.BLUE, 1.6, dash="4 4"))
    for i, ln in enumerate([
        "Asks: is the DATA already unbalanced?",
        "",
        "Compares slices in the data itself — group sizes,",
        "and the rate of positive outcomes in the TRUE labels.",
        "",
        "Catches bias you inherited. A model trained on this",
        "will reproduce it however good the algorithm is.",
    ]):
        body.append(c.t(44, 256 + i * 17, ln, 10,
                        c.BLUE if i == 0 else c.GREY, "700" if i == 0 else "400"))

    # model bias
    body.append(c.rect(476, 186, 440, 200, fill="#faf5ff", stroke=c.PURPLE, rx=10, sw=1.6))
    body.append(c.mono(496, 212, "DetectModelBiasOp", 12.5, c.PURPLE))
    body.append(c.t(496, 232, "Runs AFTER batch prediction, on the model's output.",
                    10.5, c.TEXT))
    body.append(c.line(487, 146, 487, 184, c.PURPLE, 1.6, dash="4 4"))
    for i, ln in enumerate([
        "Asks: is the MODEL treating slices differently?",
        "",
        "Compares predicted positive rates and error rates",
        "across slices — e.g. Difference in Positive",
        "Proportions in Predicted Labels, Accuracy Difference.",
        "",
        "Catches bias the model added, or failed to correct.",
    ]):
        body.append(c.t(496, 256 + i * 17, ln, 10,
                        c.PURPLE if i == 0 else c.GREY, "700" if i == 0 else "400"))

    body.append(c.rect(24, 402, w - 48, 40, fill=c.GREEN, rx=8, op=0.12))
    body.append(c.mono(60, 427, "BiasConfig", 12, c.GREEN))
    body.append(c.t(160, 427, "— both components take one. It names the SLICE FEATURE: the "
                              "column whose groups you compare.", 10.5, c.TEXT))

    co, _ = c.callout(24, 456, w - 48, [
        "Balanced data does not guarantee a fair model, and a biased model is not always the data's",
        "fault. That is why both checks exist and why running only one leaves a real gap: the first",
        "tells you what you inherited, the second tells you what you shipped.",
    ], "info")
    body += co
    write("fa-01-where.svg", w, h, body,
          "DetectDataBiasOp before training, DetectModelBiasOp after prediction")


def fig_notthesame():
    w, h = 940, 640
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Three things that sound like fairness measurement — one is",
                    15, c.TEXT, "500"))

    rows = [
        ("Feature attribution", c.RED, "NOT bias detection",
         "How much each feature contributed to a prediction.",
         "Per-prediction importance, not group comparison. A high attribution for 'region' means the",
         "model USES region — which may be entirely legitimate. And a model can discriminate with",
         "region attribution near zero, via proxies like postcode. Wrong instrument."),
        ("Sliced evaluation metrics", c.AMBER, "CLOSE, NOT IT",
         "ModelEvaluationClassificationOp with slicing_specs.",
         "Gives you accuracy, precision and recall per slice — genuinely useful, and the raw material",
         "for fairness. But they are PERFORMANCE metrics; you would still compute the fairness",
         "differences yourself, by hand, and defend your definitions."),
        ("Bias detection components", c.GREEN, "THIS ONE",
         "DetectDataBiasOp and DetectModelBiasOp.",
         "Purpose-built, standardised bias metrics computed across the slices you name in BiasConfig.",
         "Standardised matters for a regulator: you are reporting a defined metric rather than an",
         "in-house calculation you have to justify."),
    ]
    y = 66
    for name, col, verdict, what, l1, l2, l3 in rows:
        body.append(c.rect(24, y, w - 48, 152, fill="#ffffff", stroke=col, rx=9, sw=1.5))
        body.append(c.rect(24, y, 6, 152, fill=col, rx=3))
        body.append(c.t(46, y + 28, name, 12.5, c.TEXT, "700"))
        ch, cw = c.chip(w - 216, y + 15, verdict, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 50, what, 10.5, col, "600"))
        for i, ln in enumerate([l1, l2, l3]):
            body.append(c.t(46, y + 76 + i * 18, ln, 10, c.GREY))
        y += 160

    co, _ = c.callout(24, y + 6, w - 48, [
        "The distinction that matters: bias is a property of OUTCOMES ACROSS GROUPS, not of how much",
        "a feature mattered. Any method that never compares two slices to each other is measuring",
        "something else, however reasonable it sounds in a meeting.",
    ], "warn")
    body += co
    write("fa-02-not-the-same.svg", w, h, body,
          "Feature attribution and sliced metrics are not bias detection")


def fig_wit():
    w, h = 940, 715
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The What-If Tool: one threshold, or one per group",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The same trained model, the same scores. Only the cut-off "
                            "moves - and that is the whole point.", 11, c.GREY))

    # single threshold
    body.append(c.rect(24, 80, 440, 250, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.5))
    body.append(c.t(44, 106, "SINGLE THRESHOLD  -  0.50 everywhere", 10.5, c.RED, "700"))
    body.append(c.t(44, 126, "Looks neutral. Is not, if the score distributions differ.",
                    10, c.GREY))
    bb = c.bars(44, 142, 400, 120, [
        ("Region A  hired", 0.41), ("Region B  hired", 0.38), ("Region C  hired", 0.12),
    ], maxv=0.5, color=c.RED, label_w=150, value_fmt="%.2f")
    body += bb
    body.append(c.t(44, 296, "12% vs 41% - the model is not asked to be fair, so it isn't.",
                    10.5, c.RED, "700"))

    # group thresholds
    body.append(c.rect(476, 80, 440, 250, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.5))
    body.append(c.t(496, 106, "GROUP THRESHOLDS  -  demographic parity", 10.5, c.GREEN, "700"))
    body.append(c.t(496, 126, "A: 0.52   B: 0.50   C: 0.31   -  set by the tool, not by hand.",
                    10, c.GREY))
    bb2 = c.bars(496, 142, 400, 120, [
        ("Region A  hired", 0.30), ("Region B  hired", 0.30), ("Region C  hired", 0.29),
    ], maxv=0.5, color=c.GREEN, label_w=150, value_fmt="%.2f")
    body += bb2
    body.append(c.t(496, 296, "Equal positive rates. No retraining, no new data.",
                    10.5, c.GREEN, "700"))

    body.append(c.t(24, 366, "The four tabs, and what each is actually for",
                    12.5, c.TEXT, "700"))
    rows = [
        ("Performance & Fairness", c.GREEN,
         "Slice by a feature, then optimise thresholds for a fairness constraint.",
         "The only tab that changes group outcomes. Demographic parity, equal opportunity,"),
        ("Datapoint Editor", c.BLUE,
         "Edit one example, re-run inference, watch the prediction move.",
         "Answers 'why this person'. One row at a time - not a fix for a group-level gap."),
        ("Counterfactuals", c.BLUE,
         "Find the most-similar example with the opposite prediction.",
         "Shows what would have had to differ. Diagnostic, not a remedy."),
        ("Partial dependence", c.AMBER,
         "Plot how the prediction moves as one feature varies.",
         "Reads the model. It cannot remove a feature - the model is already trained."),
    ]
    y = 384
    for name, col, l1, l2 in rows:
        body.append(c.rect(24, y, w - 48, 54, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 54, fill=col, rx=2.5))
        body.append(c.t(44, y + 21, name, 11.5, c.TEXT, "700"))
        body.append(c.t(232, y + 21, l1, 10, c.TEXT))
        body.append(c.t(44, y + 41, l2, 9.5, c.GREY))
        y += 60

    co, _ = c.callout(24, y + 6, w - 48, [
        "Different thresholds per group is a real technique with a real cost: two candidates with the",
        "same score can now get different answers because of their group. That may be defensible or",
        "may be illegal where you operate. The tool makes the trade-off visible; it does not make it.",
    ], "warn")
    body += co
    write("fa-03-what-if-tool.svg", w, h, body,
          "What-If Tool threshold optimisation across slices")


if __name__ == "__main__":
    print("Generating fairness figures into %s" % HERE)
    fig_where()
    fig_notthesame()
    fig_wit()
    print("done.")
