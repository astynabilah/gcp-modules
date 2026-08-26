import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("scaling")

W = 940


def write(name, w, h, body, title):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-30s %sx%s" % (name, w, h))


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = wd
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


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    return [c.line(x1, y1, hx, hy, col, sw),
            c.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
                x2, y2,
                x2 - 9 * math.cos(ang - 0.42), y2 - 9 * math.sin(ang - 0.42),
                x2 - 9 * math.cos(ang + 0.42), y2 - 9 * math.sin(ang + 0.42)), fill=col)]


# --------------------------------------------------------------------------

def fig_ladder():
    w, h = 940, 520
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The five stages — each one fixes what the previous one broke",
                    14.5, c.TEXT, "500"))
    body.append(c.t(24, 56, "You do not climb this ladder because it exists. You climb one rung "
                            "when the failure named below actually starts hurting.", 11, c.GREY))

    stages = [
        ("0", "Prototype", c.GREY,
         "Notebook, Colab, a CSV on someone's laptop.",
         "Nobody else can reproduce it.",
         ["Colab", "BigQuery ad-hoc"]),
        ("1", "Reproducible", c.BLUE,
         "SQL and config in git. One command rebuilds everything from source data.",
         "Someone still has to remember to run it.",
         ["BigQuery", "Dataform", "git"]),
        ("2", "Scheduled", c.TEAL,
         "It runs itself on a schedule and writes to a partitioned table.",
         "Nobody knows whether the output is still correct.",
         ["Scheduled queries", "Cloud Scheduler", "Workflows"]),
        ("3", "Observed", c.AMBER,
         "Evaluation, drift monitoring, lineage, and alerts on failure.",
         "Only batch consumers can use it.",
         ["ML.EVALUATE", "Model Monitoring", "Dataplex lineage"]),
        ("4", "Served & governed", c.GREEN,
         "Online endpoint, versioned registry, safe rollout, retraining path.",
         "— this is production.",
         ["Agent Platform", "Registry", "Endpoints", "Pipelines"]),
    ]

    x0, cw, gap = 24, 168, 14
    top = 80
    for i, (num, name, col, have, breaks, svc) in enumerate(stages):
        x = x0 + i * (cw + gap)
        body.append(c.rect(x, top, cw, 380, fill="#ffffff", stroke=col, rx=10, sw=1.5))
        body.append(c.rect(x, top, cw, 46, fill=col, rx=10, op=0.12))
        body.append(c.rect(x, top + 36, cw, 10, fill="#ffffff"))
        body.append(c.circle(x + 26, top + 24, 13, fill=col))
        body.append(c.t(x + 26, top + 28.5, num, 13, "#ffffff", "600", "middle"))
        body.append(c.t(x + 48, top + 29, name, 12, c.TEXT, "600"))

        yy = top + 68
        body.append(c.t(x + 14, yy, "YOU HAVE", 8.5, c.GREY, "600"))
        for j, ln in enumerate(wrap(have, 25)):
            body.append(c.t(x + 14, yy + 16 + j * 14, ln, 10, c.TEXT))

        yy = top + 176
        body.append(c.t(x + 14, yy, "WHAT BREAKS NEXT", 8.5, c.RED, "600"))
        for j, ln in enumerate(wrap(breaks, 25)):
            body.append(c.t(x + 14, yy + 16 + j * 14, ln, 10,
                            c.GREEN if i == 4 else c.TEXT, "500" if i == 4 else "400"))

        yy = top + 262
        body.append(c.t(x + 14, yy, "GCP", 8.5, c.GREY, "600"))
        cy = yy + 10
        for s in svc:
            ch, cwid = c.chip(x + 14, cy, s, fill=col, fg=col, h=19, size=9.5)
            ch[0] = ch[0].replace('opacity="1"', 'opacity="0.13"')
            body += ch
            cy += 24

        if i < len(stages) - 1:
            body += arrow(x + cw + 1, top + 24, x + cw + gap - 1, top + 24, col="#bdc1c6", sw=1.8)

    write("s-01-ladder.svg", w, h, body, "The five stages of scaling a prototype")


def fig_decision():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Which GCP path — decided by your data and your constraint, "
                            "not by what sounds impressive", 14.5, c.TEXT, "500"))

    def q(x, y, wd, text, sub=None):
        out = [c.rect(x, y, wd, 54, fill="#fffaf0", stroke=c.AMBER, rx=8, sw=1.5)]
        lines = wrap(text, 34)
        for i, ln in enumerate(lines):
            out.append(c.t(x + wd / 2, y + 27 - (len(lines) - 1) * 7 + i * 14 + 4,
                           ln, 11, c.TEXT, "500", "middle"))
        return out

    body += q(330, 66, 280, "Can a simple rule already do the job?")
    body += node(60, 158, 226, 56, "Ship the rule", "and measure it honestly", col=c.GREEN,
                 fill="#f2fbf5")
    body += arrow(400, 120, 173, 158, col=c.GREEN)
    body.append(c.t(255, 138, "yes", 10, c.GREEN, "600"))

    body += q(330, 158, 280, "Is the data tabular and already in BigQuery?")
    body += arrow(470, 120, 470, 158)
    body.append(c.t(482, 141, "no", 10, c.GREY, "600"))

    body += q(330, 254, 280, "Do you need text, images, or generation?")
    body += arrow(470, 212, 470, 254)
    body.append(c.t(482, 237, "yes", 10, c.GREY, "600"))

    body += node(654, 158, 262, 56, "Vertex custom training", "your framework, your container",
                 col=c.PURPLE, fill="#faf5ff")
    body += arrow(610, 185, 654, 185)
    body.append(c.t(632, 178, "no", 10, c.GREY, "600"))

    body += node(654, 254, 262, 56, "AI.GENERATE in BigQuery", "Gemini, called from SQL",
                 col=c.PURPLE, fill="#faf5ff")
    body += arrow(610, 281, 654, 281)
    body.append(c.t(632, 274, "yes", 10, c.GREY, "600"))

    body += q(330, 350, 280, "Does something wait on the answer in real time?")
    body += arrow(470, 308, 470, 350)
    body.append(c.t(482, 333, "no", 10, c.GREY, "600"))

    body += node(60, 350, 226, 56, "BigQuery ML + scheduled query", "batch scoring into a table",
                 col=c.BLUE, fill="#f4f8ff")
    body += arrow(330, 377, 286, 377, col=c.BLUE)
    body.append(c.t(308, 370, "no", 10, c.BLUE, "600"))

    body += node(654, 350, 262, 56, "BigQuery ML + endpoint", "train in SQL, serve online",
                 col=c.GREEN, fill="#f2fbf5")
    body += arrow(610, 377, 654, 377, col=c.GREEN)
    body.append(c.t(632, 370, "yes", 10, c.GREEN, "600"))

    co, _ = c.callout(24, 440, w - 48, [
        "Two questions do most of the work. The first one — can a rule do this? — is the one teams",
        "skip, and it is the one that most often ends the project happily. The last one — is anything",
        "actually waiting? — decides whether you rent a node 24 hours a day or run a query at 3 a.m.",
        "Everything between is a matter of where your data already lives.",
    ], "info")
    body += co
    write("s-02-decision.svg", w, h, body, "Decision map for choosing a GCP ML path")


def fig_architectures():
    w, h = 940, 520
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Three reference architectures that cover most of what teams build",
                    14.5, c.TEXT, "500"))

    rows = [
        ("A", "Analytics-first", c.BLUE, "the default — no endpoint anywhere",
         ["Source tables", "BigQuery ML", "Scheduled query", "Partitioned scores", "Looker Studio"]),
        ("B", "Application serving", c.GREEN, "when a request is blocked on the answer",
         ["Source tables", "BigQuery ML", "Model registry", "Online endpoint", "Your app"]),
        ("C", "Generative enrichment", c.PURPLE, "unstructured text or images in the warehouse",
         ["Raw text / objects", "AI.GENERATE", "Typed columns", "Aggregate + join", "Dashboard"]),
    ]

    y = 68
    for tag, name, col, note, boxes in rows:
        body.append(c.rect(24, y, w - 48, 108, fill="#ffffff", stroke=c.BORDER, rx=9))
        body.append(c.circle(48, y + 26, 13, fill=col, op=0.16))
        body.append(c.t(48, y + 30, tag, 12, col, "700", "middle"))
        body.append(c.t(70, y + 30, name, 12.5, c.TEXT, "600"))
        body.append(c.t(70 + len(name) * 7.6 + 12, y + 30, note, 10.5, c.GREY))

        bw, gap = 152, 22
        x = 48
        for i, b in enumerate(boxes):
            body += node(x, y + 48, bw, 44, b, col=col, size=10.5)
            if i < len(boxes) - 1:
                body += arrow(x + bw, y + 70, x + bw + gap, y + 70, col=col, sw=1.5)
            x += bw + gap
        y += 122

    co, _ = c.callout(24, y + 4, w - 48, [
        "Architecture A is where most work should end. B adds one box — and that box is the only one",
        "in any of these diagrams that bills you while it does nothing. C is A with the extraction",
        "step replaced by a model call, which is why generative work fits the warehouse so naturally.",
    ], "ok")
    body += co
    write("s-03-architectures.svg", w, h, body, "Three reference architectures on GCP")


if __name__ == "__main__":
    print("Generating scaling-module figures into %s" % HERE)
    fig_ladder()
    fig_decision()
    fig_architectures()
    print("done.")
