import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("cloudrun")

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
    w, h = 940, 664
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Four places model weights can live — and the size threshold "
                            "that decides", 15, c.TEXT, "500"))

    rows = [
        ("In the container image", c.GREEN, "GOOD  < ~10 GB",
         "Weights are baked into the image and materialised by Cloud Run's optimised",
         "CONTAINER STREAMING infrastructure — no separate download step at all.",
         "Cost: rebuild the image to change the model; copies pile up in Artifact Registry."),
        ("Cloud Storage via SDK / CLI", c.BLUE, "GOOGLE'S DEFAULT",
         "Downloaded during container startup, using Google's network optimisations.",
         "One copy of the model, decoupled from the image. Scales past image limits.",
         "Cost: a real download on every cold start; you own the retry logic."),
        ("Cloud Storage FUSE mount", c.AMBER, "SOMETIMES",
         "Mounted as a volume; no Dockerfile changes. Supports file caching via",
         "cache-dir on an in-memory volume, and enable-buffered-read for prefetch.",
         "Cost: FUSE overhead; lazy first-read means the first user pays."),
        ("Internet (e.g. a model hub)", c.RED, "AVOID",
         "Downloaded from outside Google Cloud on every cold start.",
         "Slowest and least reliable; an external dependency in your startup path.",
         "Cost: someone else's uptime is now your uptime."),
    ]
    y = 62
    for name, col, verdict, l1, l2, l3 in rows:
        body.append(c.rect(24, y, w - 48, 118, fill="#ffffff", stroke=col, rx=9, sw=1.5))
        body.append(c.rect(24, y, 6, 118, fill=col, rx=3))
        body.append(c.t(46, y + 28, name, 12.5, c.TEXT, "700"))
        ch, cw = c.chip(w - 224, y + 15, verdict, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 52, l1, 10.5, c.TEXT))
        body.append(c.t(46, y + 71, l2, 10.5, c.TEXT))
        body.append(c.t(46, y + 96, l3, 10, c.GREY))
        y += 126

    co, _ = c.callout(24, y + 6, w - 48, [
        "The discriminator is SIZE, not preference. Under ~10 GB the image path wins because container",
        "streaming removes the download entirely. Past that, image pull and registry overhead become the",
        "bottleneck and streaming weights from Cloud Storage is the better trade. A 2 GB BERT model sits",
        "comfortably in the first case.",
    ], "info")
    body += co
    write("cr-01-where-weights-live.svg", w, h, body,
          "Four places to store model weights for Cloud Run")


def fig_coldstart():
    w, h = 940, 540
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Anatomy of a cold start — and which stage each option attacks",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "A request arrives with no warm instance. Everything below happens "
                            "before it gets an answer.", 11, c.GREY))

    stages = [
        ("Schedule", "find capacity", c.GREY),
        ("Pull image", "container streaming", c.GREEN),
        ("Start process", "python, imports", c.BLUE),
        ("Get weights", "the variable part", c.AMBER),
        ("Load to memory", "deserialise", c.PURPLE),
        ("Serve", "finally", c.TEAL),
    ]
    x = 28
    for i, (name, sub, col) in enumerate(stages):
        body += node(x, 92, 134, 56, name, sub, col=col)
        if i < len(stages) - 1:
            body += arrow(x + 134, 120, x + 148, 120, col="#bdc1c6")
        x += 148

    body.append(c.rect(472, 168, 148, 26, fill=c.AMBER, rx=6, op=0.18))
    body.append(c.t(546, 186, "this is the one", 10, c.AMBER, "700", "middle"))
    body.append(c.t(546, 210, "you actually control", 10, c.GREY, "400", "middle"))

    body.append(c.t(24, 250, "What each lever does", 12.5, c.TEXT, "700"))
    levers = [
        ("Weights in the image", c.GREEN,
         "Removes the 'get weights' stage entirely - it arrives with the image."),
        ("Startup CPU boost", c.BLUE,
         "More CPU during startup only. Helps the process-start and load stages."),
        ("min instances > 0", c.PURPLE,
         "Keeps warm instances so some requests never cold-start at all. Costs money when idle."),
        ("Concurrency", c.TEAL,
         "Higher concurrency means fewer instances for the same traffic - so fewer cold starts."),
        ("Smaller weights", c.AMBER,
         "Quantisation and formats like safetensors cut both transfer and deserialise time."),
    ]
    for i, (name, col, what) in enumerate(levers):
        yy = 276 + i * 26
        body.append(c.rect(24, yy - 12, 4, 18, fill=col, rx=2))
        body.append(c.t(38, yy, name, 10.5, c.TEXT, "600"))
        body.append(c.t(250, yy, what, 10.5, c.GREY))

    body.append(c.rect(24, 418, w - 48, 44, fill=c.RED, rx=8, op=0.10))
    body.append(c.t(44, 438, "Lazy-loading on first request does not reduce cold start.",
                    11, c.RED, "700"))
    body.append(c.t(44, 454, "It moves the cost onto the first user, who now waits for the whole "
                             "model load inside their request.", 10, c.TEXT))

    co, _ = c.callout(24, 474, w - 48, [
        "Cold start is not one number you tune - it is a sequence, and each lever shortens a different",
        "part of it. Measure which stage dominates before optimising the wrong one.",
    ], "ok")
    body += co
    write("cr-02-cold-start.svg", w, h, body,
          "The stages of a Cloud Run cold start and what shortens each")


if __name__ == "__main__":
    print("Generating Cloud Run figures into %s" % HERE)
    fig_where()
    fig_coldstart()
    print("done.")
