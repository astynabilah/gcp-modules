# -*- coding: utf-8 -*-
"""Diagrams for the Gemini tuning module.

Run:  python tools/figures/mod_gemtune.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("gemtune")

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

def fig_ladder():
    w, h = 940, 580
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Tuning is the fourth thing to try, not the first",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Each rung costs more and is harder to undo. Stop at the "
                            "first one that works.", 11, c.GREY))

    rungs = [
        ("1.  Prompt engineering", "changes the instruction", "~free", c.GREEN),
        ("2.  Few-shot prompting", "changes the examples in the prompt", "tokens", c.GREEN),
        ("3.  RAG / grounding", "changes what the model can SEE", "retrieval infra", c.AMBER),
        ("4.  Supervised fine-tuning", "changes the model's WEIGHTS",
         "a tuning job + serving", c.RED),
    ]
    y = 88
    for name, what, cost, col in rungs:
        body.append(c.rect(24, y, w - 48, 62, fill="#ffffff", stroke=col, rx=8, sw=1.4))
        body.append(c.rect(24, y, 5, 62, fill=col, rx=2.5))
        body.append(c.t(46, y + 26, name, 12.5, c.TEXT, "700"))
        body.append(c.t(46, y + 46, what, 10, c.GREY))
        ch, _cw = c.chip(700, y + 20, cost, fill="#f1f3f4", fg=c.GREY)
        body += ch
        y += 72

    body.append(c.t(24, y + 26, "The question that tells you which one you need",
                    12.5, c.TEXT, "700"))
    body.append(c.rect(24, y + 42, 440, 92, fill="#f2fbf5", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.t(244, y + 68, "Missing FACTS?", 13, c.GREEN, "700", "middle"))
    body.append(c.t(244, y + 90, "your catalogue, this quarter's policy, the wiki",
                    10, c.GREY, "400", "middle"))
    body.append(c.t(244, y + 112, "-> that is RETRIEVAL. Tuning stores facts badly.",
                    10.5, c.TEXT, "500", "middle"))

    body.append(c.rect(476, y + 42, 440, 92, fill="#faf5ff", stroke=c.PURPLE, rx=8, sw=1.4))
    body.append(c.t(696, y + 68, "Missing BEHAVIOUR?", 13, c.PURPLE, "700", "middle"))
    body.append(c.t(696, y + 90, "house tone, rigid structure, refusal patterns",
                    10, c.GREY, "400", "middle"))
    body.append(c.t(696, y + 112, "-> that is what TUNING is for.",
                    10.5, c.TEXT, "500", "middle"))

    write("gt-01-ladder.svg", w, h, body,
          "Prompting, few-shot, RAG and fine-tuning in order of cost")


def fig_endpoint():
    w, h = 940, 520
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "A tuned Gemini model gets exactly one endpoint type",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The instinct - make it private - is good architecture and "
                            "an unsupported configuration.", 11, c.GREY))

    opts = [
        ("Shared public endpoint", c.GREEN, "SUPPORTED",
         "The only target. Tuning deploys here automatically when the job finishes."),
        ("Dedicated public endpoint", c.RED, "not supported",
         "Higher limits and gRPC for custom-trained models. Not for tuned Gemini."),
        ("Private Service Connect", c.RED, "not supported",
         "The normal private answer, with a projectAllowlist. Refused for tuned Gemini."),
        ("Private services access", c.RED, "not supported",
         "The older VPC Network Peering path. Also refused."),
    ]
    y = 84
    for name, col, tag, desc in opts:
        body.append(c.rect(24, y, w - 48, 60, fill="#ffffff", stroke=col, rx=8, sw=1.4))
        body.append(c.rect(24, y, 5, 60, fill=col, rx=2.5))
        body.append(c.t(46, y + 26, name, 12, c.TEXT, "700"))
        ch, _cw = c.chip(300, y + 14, tag,
                         fill="#e6f4ea" if col == c.GREEN else "#fce8e6", fg=col)
        body += ch
        body.append(c.t(46, y + 46, desc, 10, c.GREY))
        y += 68

    body.append(c.t(24, y + 26, "So the corporate-network requirement is met differently",
                    12.5, c.TEXT, "700"))
    yy = y + 42
    body += node(40, yy, 250, 56, "Shared public endpoint", "the only option",
                 col=c.AMBER, fill="#fff8e6")
    body += node(350, yy, 250, 56, "VPC Service Controls", "perimeter", col=c.GREEN,
                 fill="#f2fbf5")
    body += node(660, yy, 240, 56, "Access level", "corporate IP ranges", col=c.GREEN,
                 fill="#f2fbf5")
    body += arrow(290, yy + 28, 350, yy + 28, col="#bdc1c6", sw=1.5)
    body += arrow(600, yy + 28, 660, yy + 28, col="#bdc1c6", sw=1.5)
    body.append(c.t(470, yy + 82, "public in name, unusable from anywhere but your network",
                    10.5, c.GREEN, "700", "middle"))
    body.append(c.t(470, yy + 100, "and IAP is not an option - it does not front Vertex "
                                   "endpoints", 10, c.RED, "700", "middle"))

    write("gt-02-endpoint.svg", w, h, body,
          "Tuned Gemini models deploy only to shared public endpoints")


if __name__ == "__main__":
    print("Generating Gemini tuning figures into %s" % HERE)
    fig_ladder()
    fig_endpoint()
    print("done.")
