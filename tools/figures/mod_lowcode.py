import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("lowcode")

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

def fig_tiers():
    w, h = 940, 520
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Four tiers of low-code AI — the axis is who supplies what",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Moving right, you supply more and Google supplies less. Effort and "
                            "control rise together.", 11, c.GREY))

    tiers = [
        ("Pretrained API", c.TEAL, "Google supplies\nthe model AND\nthe training data",
         ["Vision, Speech,", "Translation,", "Natural Language,", "Document AI"],
         "You supply:\nnothing but input"),
        ("Generative", c.PURPLE, "Google supplies\nthe model; you\nsupply the question",
         ["Gemini via", "AI.GENERATE,", "Model Garden"],
         "You supply:\na prompt + schema"),
        ("AutoML", c.AMBER, "Google supplies\nthe architecture\nsearch",
         ["Tabular, image,", "text, video", "Cloud or Edge"],
         "You supply:\nlabelled data"),
        ("BigQuery ML", c.BLUE, "You pick the\nalgorithm; SQL\ndoes the rest",
         ["CREATE MODEL", "Boosted trees,", "logistic, k-means,", "ARIMA"],
         "You supply:\ndata + model type"),
    ]
    x = 28
    for name, col, who, items, supply in tiers:
        body.append(c.rect(x, 82, 214, 316, fill="#ffffff", stroke=col, rx=10, sw=1.6))
        body.append(c.rect(x, 82, 214, 38, fill=col, rx=10, op=0.14))
        body.append(c.rect(x, 112, 214, 8, fill="#ffffff"))
        body.append(c.t(x + 107, 107, name, 12.5, c.TEXT, "700", "middle"))
        for j, ln in enumerate(who.split("\n")):
            body.append(c.t(x + 107, 140 + j * 15, ln, 10, c.GREY, "400", "middle"))
        body.append(c.line(x + 20, 196, x + 194, 196, c.BORDER, 1))
        for j, ln in enumerate(items):
            body.append(c.t(x + 18, 218 + j * 17, ln, 10, c.TEXT))
        body.append(c.rect(x + 14, 306, 186, 46, fill=col, rx=6, op=0.10))
        for j, ln in enumerate(supply.split("\n")):
            body.append(c.t(x + 107, 324 + j * 14, ln, 9.5, col, "600", "middle"))
        x += 226

    body.append(c.line(28, 416, 916, 416, c.GREY, 1.4))
    body.append(c.t(28, 436, "less effort, less control", 10, c.TEAL, "600"))
    body.append(c.t(916, 436, "more effort, more control", 10, c.BLUE, "600", "end"))

    co, _ = c.callout(24, 452, w - 48, [
        "Custom training sits off the right edge of this diagram — it is not low-code at all. The habit",
        "worth building is to try each tier left-to-right and stop at the first one that clears the bar.",
    ], "info")
    body += co
    write("lc-01-tiers.svg", w, h, body, "Four tiers of low-code AI on Google Cloud")


def fig_edge():
    w, h = 940, 600
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The AutoML fork you cannot undo later: Cloud or Edge",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "You choose this BEFORE training. It decides what the model can ever "
                            "be deployed to.", 11, c.GREY))

    body += node(392, 78, 156, 44, "Labelled data", None, col=c.GREY)
    body.append(c.path("M 470 122 C 470 144 240 142 240 164", stroke=c.BLUE, sw=1.8))
    body.append(c.path("M 470 122 C 470 144 700 142 700 164", stroke=c.GREEN, sw=1.8))

    # cloud
    body.append(c.rect(24, 164, 440, 300, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 190, "CLOUD", 12, c.BLUE, "700"))
    body.append(c.t(96, 190, "runs on Google's machines", 10, c.GREY))
    body.append(c.t(44, 216, "Model types", 10, c.TEXT, "600"))
    for i, (mt, desc) in enumerate([
        ("CLOUD", "the balanced default"),
        ("CLOUD_HIGH_ACCURACY_1", "accuracy over latency"),
        ("CLOUD_LOW_LATENCY_1", "latency over accuracy"),
    ]):
        body.append(c.mono(44, 238 + i * 20, mt, 10.5, c.BLUE))
        body.append(c.t(268, 238 + i * 20, desc, 9.5, c.GREY))

    body.append(c.t(44, 320, "Deployment", 10, c.TEXT, "600"))
    body += node(44, 332, 190, 44, "Vertex endpoint", "online or batch", col=c.BLUE)
    body.append(c.rect(252, 332, 190, 44, fill=c.RED, rx=8, op=0.10))
    body.append(c.t(347, 352, "Cannot be exported", 10.5, c.RED, "700", "middle"))
    body.append(c.t(347, 366, "to an edge device", 9.5, c.RED, "400", "middle"))

    body.append(c.t(44, 404, "Choose when inference happens in your datacentre or app backend,",
                    10, c.GREY))
    body.append(c.t(44, 420, "and a network round trip to Google is acceptable.", 10, c.GREY))
    body.append(c.t(44, 444, "Reachability, autoscaling and monitoring all come for free.",
                    10, c.TEXT))

    # edge
    body.append(c.rect(476, 164, 440, 300, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(496, 190, "EDGE", 12, c.GREEN, "700"))
    body.append(c.t(542, 190, "runs on YOUR device", 10, c.GREY))
    body.append(c.t(496, 216, "Model types", 10, c.TEXT, "600"))
    for i, (mt, desc) in enumerate([
        ("MOBILE_TF_VERSATILE_1", "the balanced default"),
        ("MOBILE_TF_HIGH_ACCURACY_1", "accuracy over latency"),
        ("MOBILE_TF_LOW_LATENCY_1", "latency over accuracy"),
    ]):
        body.append(c.mono(496, 238 + i * 20, mt, 10.5, c.GREEN))
        body.append(c.t(736, 238 + i * 20, desc, 9.5, c.GREY))

    body.append(c.t(496, 320, "Deployment — export, then ship it yourself", 10, c.TEXT, "600"))
    for i, (fmt, tgt) in enumerate([
        ("tflite", "phones, embedded, Coral"),
        ("edgetpu-tflite", "Edge TPU"),
        ("tf-js", "browser"),
        ("tf-saved-model", "your own container"),
        ("Core ML", "iOS / macOS"),
    ]):
        body.append(c.mono(496, 340 + i * 17, fmt, 10, c.GREEN))
        body.append(c.t(632, 340 + i * 17, tgt, 9.5, c.GREY))

    body.append(c.rect(496, 428, 400, 26, fill=c.RED, rx=6, op=0.10))
    body.append(c.t(696, 445, "Cannot be deployed to a Vertex AI endpoint", 10.5, c.RED,
                    "700", "middle"))

    co, _ = c.callout(24, 480, w - 48, [
        "The asymmetry is total and it is decided at training time: a Cloud model can never leave Google,",
        "and an Edge model can never be served by Google. Picking Edge and then choosing CLOUD as the",
        "model type — or expecting to deploy an Edge model to an endpoint — is the classic mistake, and",
        "the only fix is to train again.",
    ], "warn")
    body += co
    write("lc-02-cloud-vs-edge.svg", w, h, body,
          "AutoML Cloud model types versus Edge model types")


def fig_catalogue():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Pick by data type — and try the cheapest column first",
                    15, c.TEXT, "500"))

    cols = ["Your data", "Pretrained API", "Generative", "AutoML / BQML"]
    rows = [
        ["Images", "Vision API\nlabels, OCR, faces", "Gemini over\nObjectRef", "AutoML image\nCloud or Edge"],
        ["Video", "Video Intelligence\nAPI", "Gemini\nmultimodal", "AutoML video"],
        ["Text", "Natural Language\nAPI", "Gemini via\nAI.GENERATE", "AutoML text /\nBQML + embeddings"],
        ["Audio", "Speech-to-Text", "Gemini\nmultimodal", "—"],
        ["Documents", "Document AI\nforms, invoices", "Gemini over\nPDF ObjectRef", "Document AI\nCustom Extractor"],
        ["Tabular", "—", "—", "BigQuery ML\nor AutoML Tabular"],
    ]
    widths = [130, 250, 230, 260]
    x, y0 = 24, 62
    total = sum(widths)
    body.append(c.rect(x, y0, total, 30, fill=c.PANEL))
    body.append(c.rect(x, y0, total, 30 + 62 * len(rows), fill="none", stroke=c.BORDER, rx=4))
    heads = [c.GREY, c.TEAL, c.PURPLE, c.AMBER]
    cx = x
    for i, hc in enumerate(cols):
        body.append(c.t(cx + 12, y0 + 20, hc, 11, heads[i], "700"))
        if i:
            body.append(c.line(cx, y0, cx, y0 + 30 + 62 * len(rows), c.BORDER, 1, op=.7))
        cx += widths[i]
    body.append(c.line(x, y0 + 30, x + total, y0 + 30, c.BORDER, 1))
    for ri, row in enumerate(rows):
        ry = y0 + 30 + 62 * ri
        if ri % 2:
            body.append(c.rect(x, ry, total, 62, fill="#fcfcfd"))
        if ri:
            body.append(c.line(x, ry, x + total, ry, c.BORDER, 1, op=.55))
        cx = x
        for ci, cell in enumerate(row):
            lines = cell.split("\n")
            for li, ln in enumerate(lines):
                oy = 36 if len(lines) == 1 else 26 + li * 16
                body.append(c.t(cx + 12, ry + oy, ln, 10.5,
                                c.TEXT if (ci == 0 or li == 0) else c.GREY,
                                "700" if ci == 0 else "400"))
            cx += widths[ci]
    y = y0 + 30 + 62 * len(rows)

    co, _ = c.callout(24, y + 16, total, [
        "The generative column did not exist a few years ago and has quietly absorbed a large share of",
        "what AutoML was for: if a prompt with a typed output schema clears your accuracy bar, you have",
        "skipped labelling entirely. Try it first — it costs an afternoon, and it gives you the baseline",
        "that tells you whether training is worth it. Lab 1 and Lab 4 are that experiment.",
    ], "ok")
    body += co
    write("lc-03-catalogue.svg", w, h, body, "Low-code AI options by data type")


def fig_imbalance():
    w, h = 940, 600
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Class imbalance in AutoML Tabular - three levers, three problems",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "0.5% fraud. High accuracy, terrible recall. Each lever fixes a "
                            "different part of that.", 11, c.GREY))

    body.append(c.rect(24, 78, w - 48, 74, fill="#fff8f7", stroke=c.RED, rx=9, sw=1.5))
    body.append(c.rect(24, 78, 6, 74, fill=c.RED, rx=3))
    body.append(c.t(46, 102, "The symptom", 11.5, c.RED, "700"))
    body.append(c.t(46, 124, "A model that predicts 'not fraud' for every row scores 99.5% "
                             "accuracy and catches zero fraud.", 10.5, c.TEXT))
    body.append(c.t(46, 142, "Accuracy is not measuring what you care about, and neither is "
                             "the default configuration.", 10.5, c.GREY))

    levers = [
        ("1. Weight column", c.GREEN, "TRAINING",
         "Assign higher weights to the\nfraudulent rows and name that\ncolumn as the Weight column.",
         "The model pays more attention\nto the rare class while learning.",
         "Fixes: the model ignores\nthe minority class."),
        ("2. Stratified split", c.BLUE, "EVALUATION",
         "Split randomly, but preserve the\ndistribution of the target column\nacross train / validation / test.",
         "A random 10% test set of 0.5%\nfraud may hold almost none.",
         "Fixes: you cannot measure the\nthing you want to improve."),
        ("3. AUC-PR objective", c.PURPLE, "OPTIMISATION",
         "Set the optimisation objective to\nmaximize-au-prc instead of the\ndefault AUC-ROC.",
         "AUC-ROC looks excellent on\nimbalanced data even when almost\nno fraud is caught.",
         "Fixes: optimising for the\nwrong target."),
    ]
    x = 28
    for name, col, tag, what, why, fixes in levers:
        body.append(c.rect(x, 168, 290, 316, fill="#ffffff", stroke=col, rx=10, sw=1.6))
        body.append(c.rect(x, 168, 290, 42, fill=col, rx=10, op=0.14))
        body.append(c.rect(x, 202, 290, 8, fill="#ffffff"))
        body.append(c.t(x + 16, 188, name, 12, c.TEXT, "700"))
        body.append(c.t(x + 274, 188, tag, 8.5, col, "700", "end"))
        for j, ln in enumerate(what.split("\n")):
            body.append(c.t(x + 16, 232 + j * 15, ln, 10, c.TEXT))
        body.append(c.line(x + 16, 288, x + 274, 288, c.BORDER, 1))
        for j, ln in enumerate(why.split("\n")):
            body.append(c.t(x + 16, 308 + j * 15, ln, 9.5, c.GREY))
        body.append(c.rect(x + 12, 380, 266, 56, fill=col, rx=6, op=0.10))
        for j, ln in enumerate(fixes.split("\n")):
            body.append(c.t(x + 24, 400 + j * 14, ln, 9.5, col, "600"))
        x += 302

    body.append(c.t(470, 462, "these are complementary, not alternatives", 10, c.TEXT,
                    "700", "middle"))

    co, _ = c.callout(24, 496, w - 48, [
        "An exam makes you pick one. Real fraud work uses all three, because they address different",
        "failure points: the weight column changes what the model learns, the stratified split changes",
        "what you can measure, and the objective changes what the search optimises for. Fixing only",
        "one leaves the other two quietly broken.",
    ], "ok")
    body += co
    write("lc-04-imbalance.svg", w, h, body,
          "Three composable levers for class imbalance in AutoML Tabular")


if __name__ == "__main__":
    print("Generating low-code AI figures into %s" % HERE)
    fig_tiers()
    fig_edge()
    fig_catalogue()
    fig_imbalance()
    print("done.")
