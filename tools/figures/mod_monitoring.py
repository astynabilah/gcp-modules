import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("monitoring")

W = 940
TRAIN, SERVE = "#1a73e8", "#d93025"


def write(name, w, h, body, title):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-28s %sx%s" % (name, w, h))


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

def fig_metrics():
    """The centrepiece: which metric for which feature type, and why."""
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Two feature types, two distance metrics", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "This is the single most-tested fact about Model Monitoring — and it "
                            "is not arbitrary.", 11, c.GREY))

    # ---------------- numerical / Jensen-Shannon ----------------
    body.append(c.rect(24, 78, 440, 360, fill="#ffffff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.rect(24, 78, 440, 46, fill=c.BLUE, rx=10, op=0.13))
    body.append(c.rect(24, 114, 440, 10, fill="#ffffff"))
    body.append(c.t(44, 100, "NUMERICAL", 11, c.BLUE, "700"))
    body.append(c.t(130, 100, "age, income, monthly_charges", 10, c.GREY))
    body.append(c.t(44, 148, "Jensen-Shannon divergence", 13.5, c.TEXT, "600"))

    ax, ay, aw, ah = 60, 176, 372, 118
    body.append(c.line(ax, ay + ah, ax + aw, ay + ah, c.GREY, 1.3))

    def bell(mu, sd, scale):
        pts = []
        for i in range(61):
            xv = i / 60.0
            yv = math.exp(-((xv - mu) ** 2) / (2 * sd * sd))
            pts.append((ax + aw * xv, ay + ah - ah * yv * scale))
        return pts

    for mu, sd, col, lbl in ((0.38, 0.13, TRAIN, "training"), (0.60, 0.15, SERVE, "serving")):
        pts = bell(mu, sd, 0.86)
        d = "M " + " L ".join("%.1f %.1f" % p for p in pts)
        body.append(c.path(d + " L %.1f %.1f L %.1f %.1f Z" % (ax + aw, ay + ah, ax, ay + ah),
                           fill=col, op=0.16))
        body.append(c.path(d, stroke=col, sw=2.2))
    body.append(c.rect(60, 306, 11, 11, fill=TRAIN, rx=2.5))
    body.append(c.t(78, 316, "training distribution", 10, c.TEXT))
    body.append(c.rect(220, 306, 11, 11, fill=SERVE, rx=2.5))
    body.append(c.t(238, 316, "serving distribution", 10, c.TEXT))

    for i, ln in enumerate([
        "Values are binned into a histogram, then the two",
        "distributions are compared as a whole.",
        "Bounded 0–1, symmetric, and defined even where one",
        "distribution has zero mass — which is why it is used",
        "here and plain KL divergence is not.",
    ]):
        body.append(c.t(44, 342 + i * 17, ln, 10.5, c.GREY if i > 1 else c.TEXT))
    body.append(c.rect(44, 430, 400, 0.1, fill="none"))

    # ---------------- categorical / L-infinity ----------------
    body.append(c.rect(476, 78, 440, 360, fill="#ffffff", stroke=c.AMBER, rx=10, sw=1.6))
    body.append(c.rect(476, 78, 440, 46, fill=c.AMBER, rx=10, op=0.13))
    body.append(c.rect(476, 114, 440, 10, fill="#ffffff"))
    body.append(c.t(496, 100, "CATEGORICAL", 11, c.AMBER, "700"))
    body.append(c.t(596, 100, "region, product_category, contract", 10, c.GREY))
    body.append(c.t(496, 148, "L-infinity distance", 13.5, c.TEXT, "600"))

    cats = [("north", .30, .26), ("south", .25, .21), ("east", .28, .12), ("west", .17, .41)]
    bx, by, bh2 = 512, 176, 108
    slot = 96
    body.append(c.line(bx - 8, by + bh2, bx + slot * 4 - 8, by + bh2, c.GREY, 1.3))
    maxgap_i = 3
    for i, (name, tr, sv) in enumerate(cats):
        x = bx + i * slot
        body.append(c.rect(x, by + bh2 - bh2 * tr / .45, 28, bh2 * tr / .45, fill=TRAIN, rx=3))
        body.append(c.rect(x + 32, by + bh2 - bh2 * sv / .45, 28, bh2 * sv / .45,
                           fill=SERVE, rx=3))
        body.append(c.t(x + 30, by + bh2 + 15, name, 9.5, c.TEXT, "400", "middle"))
        if i == maxgap_i:
            y1 = by + bh2 - bh2 * tr / .45
            y2 = by + bh2 - bh2 * sv / .45
            body.append(c.line(x + 68, y1, x + 68, y2, c.RED, 2))
            body.append(c.line(x + 64, y1, x + 72, y1, c.RED, 2))
            body.append(c.line(x + 64, y2, x + 72, y2, c.RED, 2))
            body.append(c.t(x + 76, (y1 + y2) / 2 + 4, "0.24", 11, c.RED, "700"))

    body.append(c.rect(512, 306, 11, 11, fill=TRAIN, rx=2.5))
    body.append(c.t(530, 316, "training share", 10, c.TEXT))
    body.append(c.rect(652, 306, 11, 11, fill=SERVE, rx=2.5))
    body.append(c.t(670, 316, "serving share", 10, c.TEXT))

    for i, ln in enumerate([
        "The proportion of each category is compared, and the",
        "score is the single LARGEST gap — here 'west', 0.24.",
        "No binning is needed and no ordering is assumed,",
        "which matters: categories have no natural distance,",
        "so 'north' is not nearer 'south' than to 'west'.",
    ]):
        body.append(c.t(496, 342 + i * 17, ln, 10.5, c.GREY if i > 1 else c.TEXT))

    co, _ = c.callout(24, 452, w - 48, [
        "Reversing the two is the classic exam trap. The mapping follows from the data: numerical values",
        "have an order and a shape you can bin, so you compare whole distributions. Categories have",
        "neither, so you compare proportions and report the worst single discrepancy.",
    ], "warn")
    body += co
    write("mon-01-metrics.svg", w, h, body,
          "Jensen-Shannon for numerical features, L-infinity for categorical")


def fig_skew_drift():
    w, h = 940, 440
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Skew vs. drift — same maths, different baseline", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The metric never changes. What you compare production against does.",
                    11, c.GREY))

    # skew
    body.append(c.rect(24, 78, 440, 216, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.5))
    body.append(c.t(44, 102, "TRAINING-SERVING SKEW", 11, c.RED, "700"))
    body += node(44, 118, 168, 52, "Training data", "the baseline", col=c.GREY)
    body += node(268, 118, 168, 52, "Production", "recent requests", col=c.RED)
    body += arrow(212, 144, 268, 144, col=c.RED)
    body.append(c.t(240, 136, "vs", 9.5, c.GREY, "600", "middle"))
    for i, ln in enumerate([
        "Catches: a pipeline that preprocesses differently",
        "in production than it did in training. Sends",
        '"Month-to-Month" where the model learned',
        '"Month-to-month". Present from day one.',
    ]):
        body.append(c.t(44, 194 + i * 17, ln, 10.5, c.TEXT if i == 0 else c.GREY))

    # drift
    body.append(c.rect(476, 78, 440, 216, fill="#fffaf0", stroke=c.AMBER, rx=10, sw=1.5))
    body.append(c.t(496, 102, "PREDICTION / FEATURE DRIFT", 11, c.AMBER, "700"))
    body += node(496, 118, 168, 52, "Earlier production", "the baseline", col=c.GREY)
    body += node(720, 118, 168, 52, "Recent production", "latest window", col=c.AMBER)
    body += arrow(664, 144, 720, 144, col=c.AMBER)
    body.append(c.t(692, 136, "vs", 9.5, c.GREY, "600", "middle"))
    for i, ln in enumerate([
        "Catches: the world changing after you deployed.",
        "A pricing change, a new market, a marketing",
        "campaign that shifts who shows up. Appears",
        "gradually, weeks or months in.",
    ]):
        body.append(c.t(496, 194 + i * 17, ln, 10.5, c.TEXT if i == 0 else c.GREY))

    co, _ = c.callout(24, 312, w - 48, [
        "Skew is a bug you introduced; drift is the world moving. Both are measured with Jensen-Shannon",
        "(numerical) or L-infinity (categorical) against a threshold you set — the only difference is",
        "which distribution sits on the left of the comparison. Configure skew first: it is the one that",
        "is already wrong on the day you launch, and the one nobody notices without monitoring.",
    ], "info")
    body += co
    write("mon-02-skew-drift.svg", w, h, body, "Training-serving skew versus drift")


def fig_what():
    w, h = 940, 500
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "What you can monitor, and what each one catches",
                    15, c.TEXT, "500"))

    rows = [
        ("Input feature skew / drift", c.BLUE, "the inputs moved",
         "Compares each feature's distribution against the baseline.",
         "Cheapest and most common. Start here."),
        ("Prediction drift", c.PURPLE, "the outputs moved",
         "Compares the distribution of predictions over time.",
         "Catches problems no input feature shows individually — and needs no ground truth."),
        ("Feature attribution skew / drift", c.AMBER, "the reasoning moved",
         "Compares how much each feature contributed to predictions.",
         "Requires explainability configured on the model. Catches a shift in which feature drives the answer, even when every input distribution looks stable."),
    ]
    y = 62
    for name, col, tag, what, note in rows:
        body.append(c.rect(24, y, w - 48, 96, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, 96, fill=col, rx=3))
        body.append(c.t(46, y + 28, name, 12.5, c.TEXT, "600"))
        ch, cw = c.chip(46 + len(name) * 7.3 + 14, y + 16, tag, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 52, what, 10.5, c.GREY))
        # wrap the note
        words, line, ly = note.split(), "", 0
        for wd in words:
            if len(line + " " + wd) > 118 and line:
                body.append(c.t(46, y + 74 + ly * 14, line, 10, c.TEXT))
                line, ly = wd, ly + 1
            else:
                line = (line + " " + wd).strip()
        body.append(c.t(46, y + 74 + ly * 14, line, 10, c.TEXT))
        y += 106

    co, _ = c.callout(24, y + 4, w - 48, [
        "None of these measure accuracy, and that is not a limitation — it is the point. Ground truth",
        "for churn arrives months later, so monitoring watches the things observable today: what goes",
        "in, what comes out, and why. Accuracy is measured separately, when labels finally land.",
    ], "ok")
    body += co
    write("mon-03-what-to-monitor.svg", w, h, body, "The three things Model Monitoring can watch")


if __name__ == "__main__":
    print("Generating monitoring figures into %s" % HERE)
    fig_metrics()
    fig_skew_drift()
    fig_what()
    print("done.")
