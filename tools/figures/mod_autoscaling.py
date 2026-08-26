import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("autoscaling")

W = 940
CPU, GPU = "#1a73e8", "#8430ce"


def write(name, w, h, body, title):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-30s %sx%s" % (name, w, h))


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


def gauge(x, y, w, pct, col, label, target=60):
    """A horizontal utilisation bar with a target marker."""
    out = [c.t(x, y - 6, label, 10, c.TEXT, "600"),
           c.rect(x, y, w, 20, fill=c.PANEL, rx=4),
           c.rect(x, y, w * pct / 100.0, 20, fill=col, rx=4),
           c.line(x + w * target / 100.0, y - 4, x + w * target / 100.0, y + 24,
                  c.RED, 1.8, dash="3 3"),
           c.t(x + w + 10, y + 14, "%d%%" % pct, 11, col, "700")]
    return out


# --------------------------------------------------------------------------

def fig_rule():
    w, h = 940, 584
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The one rule — asymmetric on purpose", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "With a GPU attached, Vertex AI watches TWO metrics. Scale-up and "
                            "scale-down use different logic.", 11, c.GREY))

    # scale up
    body.append(c.rect(24, 78, 440, 190, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.5))
    body.append(c.t(44, 102, "SCALE UP  —  logical OR", 11.5, c.GREEN, "700"))
    body.append(c.t(44, 122, "Adds a replica when EITHER metric is above its target.",
                    10.5, c.TEXT))
    body += gauge(44, 152, 300, 30, CPU, "CPU utilisation")
    body += gauge(44, 208, 300, 85, GPU, "GPU duty cycle")
    body.append(c.rect(392, 148, 56, 82, fill=c.GREEN, rx=8, op=0.16))
    body.append(c.t(420, 182, "SCALE", 10, c.GREEN, "700", "middle"))
    body.append(c.t(420, 196, "UP", 12, c.GREEN, "700", "middle"))

    # scale down
    body.append(c.rect(476, 78, 440, 190, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.5))
    body.append(c.t(496, 102, "SCALE DOWN  —  logical AND", 11.5, c.RED, "700"))
    body.append(c.t(496, 122, "Removes a replica only when BOTH are below target.",
                    10.5, c.TEXT))
    body += gauge(496, 152, 300, 30, CPU, "CPU utilisation")
    body += gauge(496, 208, 300, 45, GPU, "GPU duty cycle")
    body.append(c.rect(844, 148, 56, 82, fill=c.RED, rx=8, op=0.14))
    body.append(c.t(872, 182, "SCALE", 10, c.RED, "700", "middle"))
    body.append(c.t(872, 196, "DOWN", 11, c.RED, "700", "middle"))

    body.append(c.t(24, 300, "The same rule produces two opposite complaints", 12.5,
                    c.TEXT, "600"))

    cases = [
        ("“It scales too often!”", c.AMBER,
         "CPU-heavy preprocessing, GPU-light inference",
         [("CPU", 82, CPU), ("GPU", 20, GPU)],
         "CPU alone crosses 60% -> OR fires -> a replica is added\nwhile the GPU sits idle. Working as designed, not a bug."),
        ("“It won't scale up!”", c.BLUE,
         "GPU-heavy inference, CPU-light",
         [("CPU", 30, CPU), ("GPU", 85, GPU)],
         "GPU alone crosses 60% -> OR fires -> it SHOULD scale.\nIf it isn't, the default was overridden somewhere."),
    ]
    x = 24
    for title, col, sub, bars, note in cases:
        body.append(c.rect(x, 322, 440, 158, fill="#ffffff", stroke=col, rx=10, sw=1.5))
        body.append(c.rect(x, 322, 6, 158, fill=col, rx=3))
        body.append(c.t(x + 22, 346, title, 12.5, c.TEXT, "700"))
        body.append(c.t(x + 22, 364, sub, 10, c.GREY))
        for i, (nm, pct, bcol) in enumerate(bars):
            yy = 384 + i * 30
            body.append(c.t(x + 22, yy + 14, nm, 10, c.TEXT, "600"))
            body.append(c.rect(x + 62, yy, 240, 18, fill=c.PANEL, rx=4))
            body.append(c.rect(x + 62, yy, 240 * pct / 100.0, 18, fill=bcol, rx=4))
            body.append(c.line(x + 62 + 144, yy - 3, x + 62 + 144, yy + 21, c.RED, 1.6,
                               dash="3 3"))
            body.append(c.t(x + 312, yy + 13, "%d%%" % pct, 10.5, bcol, "700"))
        for i, ln in enumerate(note.split("\n")):
            body.append(c.t(x + 22, 452 + i * 14, ln, 9.5, c.GREY))
        x += 452

    body.append(c.t(470, 502, "red dashed line = the 60% default target", 9.5, c.RED,
                    "500", "middle"))

    co, _ = c.callout(24, 514, w - 48, [
        "Both complaints come from the same OR. Diagnose by asking which metric crossed 60% — not",
        "by assuming autoscaling is broken.",
    ], "info")
    body += co
    write("as-01-the-rule.svg", w, h, body,
          "Scale up on either metric, scale down only when both are below target")


def fig_timeline():
    w, h = 940, 470
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Why scaling is never instant", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Traffic arrives in milliseconds. A replica arrives in minutes. "
                            "That gap is the whole problem.", 11, c.GREY))

    ax, ay, aw, ah = 70, 90, 820, 150
    body.append(c.line(ax, ay + ah, ax + aw, ay + ah, c.GREY, 1.4))
    body.append(c.t(46, ay + 10, "load", 10, c.GREY, "400", "end"))

    # traffic curve: step up
    pts = []
    for i in range(101):
        xv = i / 100.0
        if xv < 0.22:
            yv = 0.25
        elif xv < 0.30:
            yv = 0.25 + (xv - 0.22) / 0.08 * 0.6
        else:
            yv = 0.85
        pts.append((ax + aw * xv, ay + ah - ah * yv))
    body.append(c.path("M " + " L ".join("%.1f %.1f" % p for p in pts), stroke=c.AMBER, sw=2.4))
    body.append(c.t(ax + aw * 0.10, ay + ah - ah * 0.25 - 10, "incoming traffic", 10, c.AMBER,
                    "600"))

    # capacity: stepped, lagging
    steps = [(0.0, 0.35), (0.52, 0.70), (0.78, 1.05)]
    prev = None
    for i, (xs, cap) in enumerate(steps):
        x0 = ax + aw * xs
        x1 = ax + aw * (steps[i + 1][0] if i + 1 < len(steps) else 1.0)
        yv = ay + ah - ah * cap
        body.append(c.line(x0, yv, x1, yv, c.GREEN, 2.4))
        if prev is not None:
            body.append(c.line(x0, prev, x0, yv, c.GREEN, 2.4))
        prev = yv
    body.append(c.t(ax + aw * 0.06, ay + ah - ah * 0.35 - 10, "capacity (replicas)", 10, c.GREEN,
                    "600"))

    marks = [
        (0.26, "metric crosses 60%"),
        (0.38, "decision made"),
        (0.52, "replica booting"),
        (0.78, "serving traffic"),
    ]
    for frac, lbl in marks:
        x = ax + aw * frac
        body.append(c.line(x, ay - 6, x, ay + ah, c.GREY, 1, dash="3 3"))
        body.append(c.t(x, ay + ah + 18, lbl, 9.5, c.TEXT, "500", "middle"))

    body.append(c.rect(ax + aw * 0.26, ay + ah + 30, aw * 0.52, 22, fill=c.RED, rx=5, op=0.14))
    body.append(c.t(ax + aw * 0.52, ay + ah + 45, "you are under-provisioned for this whole "
                                                  "window — seconds to minutes",
                    10, c.RED, "600", "middle"))

    body.append(c.t(24, 320, "What fills that gap", 12.5, c.TEXT, "600"))
    items = [
        ("Metric collection", "the signal is averaged over a window before it is acted on"),
        ("Cooldown", "a deliberate delay so the endpoint does not oscillate"),
        ("Node provisioning", "a machine has to be allocated"),
        ("Container + model load", "30 seconds to several minutes, depending on model size"),
    ]
    for i, (k, v) in enumerate(items):
        yy = 344 + i * 22
        body.append(c.rect(24, yy - 11, 4, 16, fill=c.BLUE, rx=2))
        body.append(c.t(38, yy, k, 10.5, c.TEXT, "600"))
        body.append(c.t(220, yy, v, 10.5, c.GREY))

    co, _ = c.callout(24, 436, w - 48, [
        "This is why minReplicaCount matters more than any target tuning: it is the only setting that "
        "buys headroom BEFORE the spike.",
    ], "warn")
    body += co
    write("as-02-timeline.svg", w, h, body, "The lag between traffic arriving and capacity arriving")


def fig_knobs():
    w, h = 940, 600
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The knobs, and which one to reach for", 15, c.TEXT, "500"))

    rows = [
        ("minReplicaCount", c.GREEN, "the floor",
         "How many replicas always run. 0 enables scale-to-zero (v1beta1).",
         "Your latency insurance AND your baseline bill. The most consequential setting."),
        ("maxReplicaCount", c.RED, "the ceiling",
         "The most replicas autoscaling may create.",
         "Your blast radius. A retry storm scales you to this number and bills for it."),
        ("machineSpec", c.BLUE, "the shape",
         "Machine type, accelerator type and count.",
         "accelerator_count > 0 is what turns on dual-metric autoscaling in the first place."),
        ("autoscalingMetricSpecs", c.PURPLE, "the trigger",
         "Override which metric and what target. Default target is 60 for both.",
         "Only needed when the default OR misfires — e.g. CPU-heavy preprocessing."),
        ("DedicatedResources", c.AMBER, "the mode",
         "The config block that exposes all of the above.",
         "AutomaticResources cannot express custom metrics — use DedicatedResources."),
    ]
    y = 62
    for name, col, tag, what, note in rows:
        body.append(c.rect(24, y, w - 48, 82, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, 82, fill=col, rx=3))
        body.append(c.mono(46, y + 26, name, 12, c.TEXT))
        ch, cw = c.chip(46 + len(name) * 7.4 + 14, y + 14, tag, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 48, what, 10.5, c.GREY))
        body.append(c.t(46, y + 68, note, 10.5, c.TEXT))
        y += 90

    co, _ = c.callout(24, y + 4, w - 48, [
        "Reach for them in this order: get minReplicaCount right first (it decides both your worst-case",
        "latency and your floor cost), cap maxReplicaCount so a bug cannot bankrupt you, and only then",
        "consider touching the metric targets. Most 'autoscaling problems' are a minReplicaCount of 1.",
    ], "ok")
    body += co
    write("as-03-knobs.svg", w, h, body, "Vertex AI autoscaling configuration knobs")


if __name__ == "__main__":
    print("Generating autoscaling figures into %s" % HERE)
    fig_rule()
    fig_timeline()
    fig_knobs()
    print("done.")
