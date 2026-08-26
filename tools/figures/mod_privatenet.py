# -*- coding: utf-8 -*-
"""Diagrams for the private networking module.

Run:  python tools/figures/mod_privatenet.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("privatenet")

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


def blocked(x, y, r=11, col=c.RED):
    return [c.circle(x, y, r, fill="#ffffff", stroke=col, sw=2),
            c.line(x - 6, y - 6, x + 6, y + 6, col, 2)]


# --------------------------------------------------------------------------

def fig_three():
    w, h = 940, 640
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Three mechanisms, three different jobs", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "A notebook with no external IP, and everything it is and "
                            "is not allowed to reach.", 11, c.GREY))

    # the VPC box
    body.append(c.rect(24, 84, 330, 300, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 110, "YOUR CUSTOM VPC", 10.5, c.BLUE, "700"))
    body.append(c.t(44, 128, "subnet: private google access ON", 9.5, c.GREY))
    body += node(58, 148, 262, 60, "Workbench instance", "no external IP", col=c.GREY)
    body += node(58, 236, 262, 52, "Cloud Router + Cloud NAT", None, col=c.PURPLE,
                 fill="#faf5ff")
    body.append(c.t(189, 316, "nothing on the internet can", 10, c.GREY, "400", "middle"))
    body.append(c.t(189, 332, "open a connection inward", 10, c.GREY, "400", "middle"))
    body += blocked(189, 358)

    # destinations
    body += node(560, 130, 250, 56, "Google APIs", "bigquery, storage, aiplatform",
                 col=c.GREEN, fill="#f2fbf5")
    body += node(560, 218, 250, 56, "The public internet", "pypi, github, anywhere",
                 col=c.AMBER, fill="#fff8e6")
    body += node(560, 306, 250, 56, "Another org's bucket", "exfiltration",
                 col=c.RED, fill="#fff8f7")

    body += arrow(354, 172, 560, 158, col=c.GREEN, sw=1.8)
    body.append(c.t(400, 140, "Private Google Access", 10, c.GREEN, "700"))
    body += arrow(354, 262, 560, 246, col=c.AMBER, sw=1.8)
    body.append(c.t(400, 232, "Cloud NAT", 10, c.AMBER, "700"))
    body.append(c.line(354, 330, 540, 334, "#bdc1c6", 1.5, dash="4 4"))
    body += blocked(470, 332)
    body.append(c.t(400, 372, "VPC Service Controls", 10, c.RED, "700"))
    body.append(c.t(400, 388, "refuses it even with valid credentials", 9.5, c.GREY))

    body.append(c.t(24, 434, "Why each is needed, and what it does not do",
                    12.5, c.TEXT, "700"))
    body += c.grid(24, 450, ["Mechanism", "Solves", "Does NOT"],
                   [["Private Google Access",
                     "reach Google APIs with no external IP",
                     "non-Google hosts; inbound"],
                    ["Cloud NAT (on Cloud Router)",
                     "outbound to anywhere, e.g. pip install",
                     "inbound; and it IS internet egress"],
                    ["VPC Service Controls",
                     "data leaving the perimeter, credentials or not",
                     "who may do what inside it - that is IAM"],
                    ["IAM",
                     "who may call which API at all",
                     "an authorised user copying data out"]],
                   [246, 330, 316])

    write("pn-01-three-mechanisms.svg", w, h, body,
          "Private Google Access, Cloud NAT and VPC Service Controls")


def fig_endpoints():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Four endpoint types, and the one model that only gets one",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The private options are real - for custom-trained models. "
                            "Tuned Gemini is the exception.", 11, c.GREY))

    body += c.grid(24, 84, ["Endpoint type", "Reached via", "Custom-trained", "Tuned Gemini"],
                   [["Shared public", "public googleapis.com", "yes", "YES - only option"],
                    ["Dedicated public", "a dedicated public DNS name", "yes", "no"],
                    ["Private Service Connect", "a private IP in your VPC", "yes", "no"],
                    ["Private services access", "VPC Network Peering", "yes", "no"]],
                   [230, 280, 190, 192],
                   colors={(0, 3): "#e6f4ea", (1, 3): "#fce8e6",
                           (2, 3): "#fce8e6", (3, 3): "#fce8e6"})

    body.append(c.t(24, 250, "So how do you restrict a tuned Gemini endpoint?",
                    12.5, c.TEXT, "700"))

    body += node(40, 274, 250, 62, "Shared public endpoint", "the only supported target",
                 col=c.AMBER, fill="#fff8e6")
    body += node(350, 274, 250, 62, "VPC Service Controls", "perimeter around the service",
                 col=c.GREEN, fill="#f2fbf5")
    body += node(660, 274, 240, 62, "Access level", "your corporate IP ranges",
                 col=c.GREEN, fill="#f2fbf5")
    body += arrow(290, 305, 350, 305, col="#bdc1c6", sw=1.5)
    body += arrow(600, 305, 660, 305, col="#bdc1c6", sw=1.5)

    body.append(c.t(470, 362, "public in name, unreachable from anywhere but your network",
                    10.5, c.GREEN, "700", "middle"))

    body.append(c.rect(24, 386, w - 48, 62, fill="#fff8f7", stroke=c.RED, rx=8, sw=1.3))
    body.append(c.rect(24, 386, 5, 62, fill=c.RED, rx=2.5))
    body.append(c.t(44, 408, "Identity-Aware Proxy is not an option here",
                    11.5, c.TEXT, "700"))
    body.append(c.t(44, 428, "IAP fronts App Engine, Compute Engine and GKE applications. "
                             "Vertex AI endpoints do not integrate with it.", 10, c.GREY))

    co, _ = c.callout(24, 462, w - 48, [
        "The instinct - make the endpoint private - is good architecture and an unsupported",
        "configuration. Check endpoint support before designing around it, not during the review.",
    ], "warn")
    body += co
    write("pn-02-endpoint-types.svg", w, h, body,
          "Vertex AI endpoint types and the tuned Gemini restriction")


if __name__ == "__main__":
    print("Generating private networking figures into %s" % HERE)
    fig_three()
    fig_endpoints()
    print("done.")
