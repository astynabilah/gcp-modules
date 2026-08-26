import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

OUT = c.lab_figures()
W = 940

KW, STR, FN = "#1967d2", "#0d652d", "#8430ce"
PL, NUM, ID_ = c.TEXT, "#b06000", "#137333"


def write(name, w, h, body, title):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-34s %sx%s" % (name, w, h))


def node(x, y, w, h, title, sub=None, col=c.BLUE, fill="#ffffff", size=11.5):
    out = [c.rect(x, y, w, h, fill=fill, stroke=col, rx=8, sw=1.5)]
    ty = y + h / 2 + (-5 if sub else 4)
    out.append(c.t(x + w / 2, ty, title, size, c.TEXT, "500", "middle"))
    if sub:
        out.append(c.t(x + w / 2, y + h / 2 + 12, sub, 9.5, c.GREY, "400", "middle"))
    return out


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6, label=None):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    out = [c.line(x1, y1, hx, hy, col, sw),
           c.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
               x2, y2,
               x2 - 9 * math.cos(ang - 0.42), y2 - 9 * math.sin(ang - 0.42),
               x2 - 9 * math.cos(ang + 0.42), y2 - 9 * math.sin(ang + 0.42)), fill=col)]
    if label:
        out.append(c.t((x1 + x2) / 2, min(y1, y2) - 9, label, 9.5, c.GREY, "500", "middle"))
    return out


def fig_00():
    w, h = 940, 380
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Lab 5 — the four things people mean by “feature engineering”",
                    14.5, c.TEXT, "500"))
    body.append(c.t(24, 56, "They are different jobs with different tools, and only one of them "
                            "needs a model to exist first.", 11, c.GREY))

    stages = [
        ("Transformation", "types, joins,\nwindows", c.BLUE,
         "raw tables -> one row\nper prediction unit"),
        ("Extraction", "derive new signal\nfrom what you have", c.TEAL,
         "ratios, bands, counts,\nembeddings"),
        ("Selection", "drop what does not\nearn its place", c.AMBER,
         "cardinality, correlation,\nleakage"),
        ("Importance", "explain what the\nmodel actually used", c.PURPLE,
         "needs a trained model"),
    ]
    x0, cw, gap = 28, 206, 22
    for i, (name, what, col, detail) in enumerate(stages):
        x = x0 + i * (cw + gap)
        body.append(c.rect(x, 86, cw, 180, fill="#ffffff", stroke=col, rx=10, sw=1.6))
        body.append(c.rect(x, 86, cw, 40, fill=col, rx=10, op=0.13))
        body.append(c.rect(x, 116, cw, 10, fill="#ffffff"))
        body.append(c.t(x + cw / 2, 112, name, 12.5, c.TEXT, "600", "middle"))
        for j, ln in enumerate(what.split("\n")):
            body.append(c.t(x + cw / 2, 152 + j * 15, ln, 10.5, c.GREY, "400", "middle"))
        body.append(c.line(x + 20, 190, x + cw - 20, 190, c.BORDER, 1))
        for j, ln in enumerate(detail.split("\n")):
            body.append(c.t(x + cw / 2, 212 + j * 15, ln, 10, c.TEXT, "400", "middle"))
        if i < 3:
            body += arrow(x + cw + 2, 176, x + cw + gap - 2, 176, col="#bdc1c6", sw=1.8)

    co, _ = c.callout(24, 288, w - 48, [
        "The loop runs backwards too: importance tells you what to drop, which sends you back to",
        "selection, and a feature that turns out to be leakage sends you back to transformation.",
        "Only importance requires a trained model — the other three happen before any CREATE MODEL.",
    ], "info")
    body += co
    write("l5-00-overview.svg", w, h, body, "The four stages of feature work")


def fig_01():
    w, h = 940, 440
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Point-in-time correctness — the bug that makes a model look brilliant",
                    14.5, c.TEXT, "500"))

    # timeline
    ax, ay, aw = 60, 150, 820
    body.append(c.line(ax, ay, ax + aw, ay, c.GREY, 1.6))
    marks = [(0.10, "signup"), (0.42, "cutoff\n(features end here)"), (0.62, "label window opens"),
             (0.94, "churn observed")]
    for frac, lbl in marks:
        x = ax + aw * frac
        body.append(c.line(x, ay - 8, x, ay + 8, c.GREY, 1.6))
        for i, ln in enumerate(lbl.split("\n")):
            body.append(c.t(x, ay + 26 + i * 14, ln, 10, c.TEXT, "500", "middle"))

    body.append(c.rect(ax + aw * 0.10, ay - 44, aw * 0.32, 26, fill=c.BLUE, rx=5, op=0.20))
    body.append(c.t(ax + aw * 0.26, ay - 26, "features may use this", 10, c.BLUE, "600", "middle"))

    body.append(c.rect(ax + aw * 0.62, ay - 44, aw * 0.32, 26, fill=c.RED, rx=5, op=0.18))
    body.append(c.t(ax + aw * 0.78, ay - 26, "label lives here — features must NOT", 10, c.RED,
                    "600", "middle"))

    body.append(c.rect(ax + aw * 0.42, ay - 92, 2.5, 84, fill=c.AMBER))
    body.append(c.t(ax + aw * 0.42, ay - 100, "prediction time", 10.5, c.AMBER, "600", "middle"))

    body += c.grid(60, 232, ["Feature", "Verdict", "Why"], [
        ["tenure_months (at cutoff)", "safe", "known before the prediction is made"],
        ["support_tickets_last_30d", "safe", "windowed to end at the cutoff"],
        ["total_charges (lifetime, today)", "LEAKAGE", "includes billing after the cutoff"],
        ["cancellation_reason", "LEAKAGE", "only exists because they churned"],
        ["last_login_date (today)", "LEAKAGE", "updated after the label window opened"],
    ], [280, 110, 430], row_h=27,
        colors={(0, 1): c.GREEN, (1, 1): c.GREEN, (2, 1): c.RED, (3, 1): c.RED, (4, 1): c.RED})

    co, _ = c.callout(60, 386, 820, [
        "Leakage does not throw an error. It shows up as a suspiciously excellent model that collapses",
        "in production — the tell is an AUC that jumps far above your baseline for no clear reason.",
    ], "warn")
    body += co
    write("l5-01-leakage.svg", w, h, body, "Point-in-time correctness and feature leakage")


def fig_02():
    h = 606
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 26, "Feature selection — four cheap filters, run before any training",
                    13, c.TEXT, "500"))

    body += c.grid(px, y + 44,
                   ["Feature", "Null %", "Distinct", "Corr. w/ label", "Verdict"], [
        ["contract", "0.0", "3", "0.405", "keep"],
        ["tenure_months", "0.0", "73", "-0.352", "keep"],
        ["internet_service", "0.0", "3", "0.228", "keep"],
        ["total_charges", "0.2", "6,531", "-0.199", "keep"],
        ["avg_monthly_spend", "0.2", "6,585", "-0.193", "drop — corr 0.97 w/ total_charges"],
        ["customer_id", "0.0", "7,043", "0.004", "drop — an identifier, not a feature"],
        ["gender", "0.0", "2", "-0.009", "drop — no signal"],
        ["phone_service", "0.0", "2", "0.012", "drop — no signal"],
    ], [200, 76, 92, 122, 406], row_h=26, mono_cols=(1, 2, 3),
        align={1: "end", 2: "end", 3: "end"},
        colors={(i, 4): (c.GREEN if i < 4 else c.RED) for i in range(8)})

    body.append(c.t(px, y + 300, "Why each filter exists", 12, c.TEXT, "500"))
    items = [
        ("Null rate", "A column that is 90% null carries little and complicates serving.", c.BLUE),
        ("Cardinality = 1", "Constant. Contributes nothing, and hides broken pipelines.", c.BLUE),
        ("Cardinality = row count", "An identifier. Trees will happily memorise it.", c.RED),
        ("Pairwise correlation", "Near-duplicates split credit and destroy importance readings.", c.AMBER),
    ]
    for i, (name, why, col) in enumerate(items):
        yy = y + 318 + i * 26
        body.append(c.rect(px, yy, 4, 18, fill=col, rx=2))
        body.append(c.t(px + 14, yy + 13, name, 10.5, c.TEXT, "600"))
        body.append(c.t(px + 176, yy + 13, why, 10.5, c.GREY))

    co, _ = c.callout(px, y + 432, pw, [
        "None of this needs a model. Correlation with the label is a screen, not a decision — a feature",
        "with near-zero linear correlation can still matter enormously inside an interaction, which is",
        "why you drop on structural grounds (identifier, constant, duplicate) and only screen on signal.",
    ], "info")
    body += co
    write("l5-02-selection.svg", W, h, body, "Feature selection filters before training")


def fig_03():
    w, h = 940, 470
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Three kinds of “feature importance” — they answer different questions",
                    14.5, c.TEXT, "500"))

    cols = [
        ("ML.FEATURE_IMPORTANCE", c.BLUE, "split-based (gain)",
         ["How much each feature",
          "improved the trees'",
          "splits during training.",
          "",
          "Trees only. Free — it",
          "falls out of training.",
          "",
          "Biased toward high-",
          "cardinality columns."]),
        ("ML.GLOBAL_EXPLAIN", c.PURPLE, "attribution to predictions",
         ["Mean absolute contri-",
          "bution to the model's",
          "outputs.",
          "",
          "Needs ENABLE_GLOBAL_",
          "EXPLAIN at training.",
          "",
          "Correlated features",
          "split the credit."]),
        ("Drop-column test", c.AMBER, "retrain without it",
         ["Retrain with the column",
          "removed, compare AUC.",
          "",
          "The only one that",
          "answers 'do I still need",
          "this?'",
          "",
          "Costs one training run",
          "per feature."]),
    ]
    x0, cw, gap = 28, 288, 12
    for i, (name, col, sub, lines) in enumerate(cols):
        x = x0 + i * (cw + gap)
        body.append(c.rect(x, 66, cw, 300, fill="#ffffff", stroke=col, rx=10, sw=1.6))
        body.append(c.rect(x, 66, cw, 52, fill=col, rx=10, op=0.13))
        body.append(c.rect(x, 108, cw, 10, fill="#ffffff"))
        body.append(c.t(x + cw / 2, 90, name, 11.5, c.TEXT, "600", "middle", c.MONO))
        body.append(c.t(x + cw / 2, 106, sub, 9.5, col, "600", "middle"))
        for j, ln in enumerate(lines):
            body.append(c.t(x + 18, 142 + j * 17, ln, 10.5, c.TEXT if j < 3 else c.GREY))

    co, _ = c.callout(28, 386, 3 * cw + 2 * gap, [
        "The trap is using the first two for feature selection. Both are descriptions of one fitted",
        "model, not statements about the world: drop a feature that shares its signal with another and",
        "accuracy may not move at all. Only the drop-column test answers the selection question — and",
        "importance ranking is never evidence of causation, however much a stakeholder wants it to be.",
    ], "warn")
    body += co
    write("l5-03-importance.svg", w, h, body, "Three kinds of feature importance compared")


def fig_04():
    h = 500
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 26, "Does the engineering actually pay? Ablation on the same split",
                    13, c.TEXT, "500"))

    body += c.grid(px, y + 46,
                   ["Feature set", "Cols", "ROC AUC", "Recall", "Δ AUC vs. raw"], [
        ["Raw columns, types fixed only", "20", "0.831", "0.694", "—"],
        ["+ engineered (ratios, bands, counts)", "24", "0.847", "0.727", "+0.016"],
        ["+ event-window aggregates", "29", "0.869", "0.761", "+0.038"],
        ["+ hyperparameter tuning", "29", "0.876", "0.769", "+0.045"],
        ["Leaky version (cancellation_reason)", "30", "0.991", "0.982", "+0.160  ⚠"],
    ], [352, 70, 110, 100, 264], row_h=30, mono_cols=(1, 2, 3),
        align={1: "end", 2: "end", 3: "end"},
        colors={(1, 4): c.GREEN, (2, 4): c.GREEN, (3, 4): c.AMBER, (4, 4): c.RED,
                (4, 2): c.RED, (4, 3): c.RED})

    body.append(c.t(px, y + 232, "Read the last row carefully", 12, c.RED, "600"))
    for i, ln in enumerate([
        "0.991 AUC is not a breakthrough. cancellation_reason only has a value because the customer "
        "already churned,",
        "so the model is reading the answer. In production that column is null for everyone you "
        "actually want to score,",
        "and the model collapses to worse than the baseline rule.",
    ]):
        body.append(c.t(px, y + 254 + i * 17, ln, 10.5, c.TEXT))

    co, _ = c.callout(px, y + 318, pw, [
        "Feature engineering bought +0.038 AUC here; hyperparameter tuning bought +0.007. That ratio",
        "is typical and it is the argument for spending your next hour on features, not on a search",
        "space. It is also why ablation belongs in your workflow: without it you are guessing.",
    ], "ok")
    body += co
    write("l5-04-ablation.svg", W, h, body, "Ablation study comparing feature sets")


if __name__ == "__main__":
    print("Generating lab 5 figures into %s" % OUT)
    for fn in (fig_00, fig_01, fig_02, fig_03, fig_04):
        fn()
    print("done.")
