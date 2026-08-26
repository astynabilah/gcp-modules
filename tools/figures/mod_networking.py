import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("networking")

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

def fig_journey():
    w, h = 940, 470
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "What actually happens when someone calls your model",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Five steps. If you know only this diagram, most of the rest "
                            "follows.", 11, c.GREY))

    steps = [
        ("Your app", 'POST predict.acme.com', c.GREY),
        ("DNS", "name -> IP address", c.BLUE),
        ("Anycast IP", "one IP, many locations", c.PURPLE),
        ("Google edge", "nearest of 180+ POPs", c.TEAL),
        ("Load balancer", "picks a backend", c.GREEN),
    ]
    x = 30
    for i, (name, sub, col) in enumerate(steps):
        body += node(x, 92, 156, 58, name, sub, col=col)
        if i < len(steps) - 1:
            body += arrow(x + 156, 121, x + 178, 121, col="#bdc1c6")
        x += 178

    body.append(c.t(30, 190, "…then the load balancer forwards to whichever backend is closest "
                             "and healthy:", 11, c.TEXT))

    body += node(180, 214, 240, 66, "Cloud Run — us-central1", "serving your model", col=c.GREEN)
    body += node(520, 214, 240, 66, "Cloud Run — europe-west1", "same container, other region",
                 col=c.GREEN)
    body.append(c.path("M 470 150 C 470 180 300 184 300 212", stroke=c.GREEN, sw=1.8))
    body.append(c.path("M 470 150 C 470 180 640 184 640 212", stroke=c.GREEN, sw=1.8,
                       dash="5 4"))
    body.append(c.t(300, 300, "a user in Chicago lands here", 10, c.GREY, "400", "middle"))
    body.append(c.t(640, 300, "a user in Berlin lands here", 10, c.GREY, "400", "middle"))

    co, _ = c.callout(24, 326, w - 48, [
        "The single most counter-intuitive part: there is ONE IP address, and it is announced from",
        "every Google edge location at once. Your user does not choose a region and neither do you —",
        "the internet's own routing delivers them to the nearest edge, and Google carries it from",
        "there. That is why 'route to the closest region' needs no code and no DNS trickery.",
    ], "info")
    body += co
    write("net-01-journey.svg", w, h, body, "The path of a prediction request")


def fig_anatomy():
    w, h = 940, 500
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "A load balancer is not one object — it is five, chained",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "You create them in this order, and each one points at the next.",
                    11, c.GREY))

    chain = [
        ("Forwarding rule", "the IP + port\n34.120.0.5:443", c.BLUE),
        ("Target proxy", "terminates TLS\nholds the certificate", c.PURPLE),
        ("URL map", "routing rules\n/predict -> which backend", c.TEAL),
        ("Backend service", "the policy: timeouts,\nCDN, Cloud Armor", c.AMBER),
        ("Backend (NEG)", "the actual thing\nthat serves", c.GREEN),
    ]
    y = 92
    for i, (name, sub, col) in enumerate(chain):
        x = 30 + i * 178
        body.append(c.rect(x, y, 156, 96, fill="#ffffff", stroke=col, rx=9, sw=1.6))
        body.append(c.rect(x, y, 156, 30, fill=col, rx=9, op=0.14))
        body.append(c.rect(x, y + 22, 156, 8, fill="#ffffff"))
        body.append(c.t(x + 78, y + 20, name, 11, c.TEXT, "600", "middle"))
        for j, ln in enumerate(sub.split("\n")):
            body.append(c.t(x + 78, y + 52 + j * 15, ln, 9.5, c.GREY, "400", "middle"))
        if i < len(chain) - 1:
            body += arrow(x + 156, y + 48, x + 178, y + 48, col="#bdc1c6")

    body.append(c.t(30, 232, "The mental shortcut", 12, c.TEXT, "600"))
    pairs = [
        ("Forwarding rule", "WHERE clients connect — the front door's address"),
        ("Target proxy", "WHAT protocol, and who holds the TLS certificate"),
        ("URL map", "WHICH backend, based on host and path"),
        ("Backend service", "HOW to treat the traffic — timeout, CDN, WAF, session affinity"),
        ("Backend / NEG", "WHO actually answers"),
    ]
    for i, (k, v) in enumerate(pairs):
        yy = 254 + i * 22
        body.append(c.mono(30, yy, k, 10.5, c.BLUE))
        body.append(c.t(196, yy, v, 10.5, c.TEXT))

    co, _ = c.callout(24, 380, w - 48, [
        "This is why a 'simple' load balancer takes five gcloud commands, and why error messages name",
        "objects you did not know existed. Nothing here is optional — the chain is the load balancer.",
        "Read an error like 'backend service X has no health check' by finding X in this chain first.",
    ], "warn")
    body += co
    write("net-02-anatomy.svg", w, h, body, "The five objects of a global external ALB")


def fig_healthcheck():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Health checks — and why serverless backends do not have them",
                    15, c.TEXT, "500"))

    # --- VM backends
    body.append(c.rect(24, 66, 440, 330, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.5))
    body.append(c.t(44, 90, "VM / INSTANCE GROUP BACKENDS", 10.5, c.BLUE, "700"))
    body.append(c.t(44, 108, "You run the machines, so you prove they are alive.",
                    10, c.GREY))

    body += node(44, 126, 150, 50, "Health checker", "Google probes", col=c.BLUE)
    body += node(292, 126, 150, 50, "Your VM", "port 8080 /healthz", col=c.GREY)
    body += arrow(194, 151, 292, 151, col=c.BLUE)
    body.append(c.t(243, 143, "every 10s", 9, c.GREY, "500", "middle"))

    body.append(c.rect(44, 194, 398, 62, fill="#ffffff", stroke=c.AMBER, rx=8, sw=1.4))
    body.append(c.t(60, 216, "You MUST allow the probe ranges in your firewall:",
                    10, c.TEXT, "600"))
    body.append(c.mono(60, 238, "35.191.0.0/16     130.211.0.0/22", 11, c.AMBER))

    for i, ln in enumerate([
        "Forget the firewall rule and every backend reads as",
        "UNHEALTHY — the implied-deny rule silently blocks the",
        "probes. This is the classic 'my load balancer is broken'",
        "and it is the reason those two ranges are worth memorising.",
    ]):
        body.append(c.t(44, 282 + i * 17, ln, 10, c.GREY))

    # --- serverless
    body.append(c.rect(476, 66, 440, 330, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.5))
    body.append(c.t(496, 90, "SERVERLESS NEG BACKENDS", 10.5, c.GREEN, "700"))
    body.append(c.t(496, 108, "Cloud Run, Cloud Run functions, App Engine.", 10, c.GREY))

    body += node(496, 126, 150, 50, "Health checker", "not used", col=c.GREY)
    body += node(744, 126, 150, 50, "Cloud Run", "Google runs it", col=c.GREEN)
    body.append(c.line(646, 151, 744, 151, c.RED, 1.8, dash="5 4"))
    body.append(c.circle(695, 151, 13, fill="#ffffff", stroke=c.RED, sw=2))
    body.append(c.line(688, 144, 702, 158, c.RED, 2))
    body.append(c.line(702, 144, 688, 158, c.RED, 2))

    body.append(c.rect(496, 194, 398, 62, fill="#ffffff", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.t(512, 216, "Health checks are NOT SUPPORTED here.", 10.5, c.GREEN, "700"))
    body.append(c.t(512, 238, "No firewall rule needed either — there is no VM to protect.",
                    10, c.TEXT))

    for i, ln in enumerate([
        "Google already manages the health of the underlying",
        "infrastructure. Attaching a health check to a backend",
        "service with serverless NEGs is a configuration error,",
        "not a safety net. Omit it.",
    ]):
        body.append(c.t(496, 282 + i * 17, ln, 10, c.GREY))

    co, _ = c.callout(24, 412, w - 48, [
        "If you still want per-backend failure handling on serverless, the feature is OUTLIER DETECTION,",
        "not health checks: it watches real request outcomes and steers new requests away from a",
        "misbehaving backend. Available on the global external ALB and the cross-region internal ALB —",
        "not on the classic Application Load Balancer.",
    ], "ok")
    body += co
    write("net-03-health-checks.svg", w, h, body,
          "Health checks on VM backends versus serverless NEG backends")


def fig_taxonomy():
    w, h = 940, 556
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Decoding the load balancer names — three questions, one name",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Every Google Cloud load balancer name is these three answers "
                            "concatenated.", 11, c.GREY))

    axes = [
        ("1. How far?", c.BLUE, [
            ("Global", "one IP worldwide, routes to nearest region"),
            ("Regional", "lives in one region only"),
            ("Cross-region", "internal, but spans regions"),
        ]),
        ("2. Who reaches it?", c.PURPLE, [
            ("External", "reachable from the internet"),
            ("Internal", "reachable only inside your VPC"),
        ]),
        ("3. What layer?", c.AMBER, [
            ("Application (L7)", "understands HTTP: paths, headers, TLS"),
            ("Network (L4)", "just moves packets: TCP/UDP, faster, dumber"),
        ]),
    ]
    y = 82
    for title, col, items in axes:
        bh = 34 + len(items) * 26
        body.append(c.rect(24, y, w - 48, bh, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, bh, fill=col, rx=3))
        body.append(c.t(46, y + 24, title, 12, col, "700"))
        for i, (name, desc) in enumerate(items):
            yy = y + 46 + i * 26
            body.append(c.mono(200, yy, name, 11, c.TEXT))
            body.append(c.t(360, yy, desc, 10.5, c.GREY))
        y += bh + 10

    body.append(c.t(24, y + 22, "So the one you want for a multi-region Cloud Run model:",
                    11.5, c.TEXT, "600"))
    body.append(c.rect(24, y + 32, w - 48, 40, fill=c.GREEN, rx=8, op=0.13))
    body.append(c.mono(46, y + 58, "global   external   Application Load Balancer", 14, c.GREEN))
    body.append(c.t(600, y + 58, "= one worldwide IP, public, HTTP-aware", 10.5, c.TEXT))

    co, _ = c.callout(24, y + 88, w - 48, [
        "Serverless NEGs work only with Application Load Balancers — never with Network Load Balancers,",
        "proxy or passthrough. If a tutorial has you attaching Cloud Run to an NLB, it is wrong.",
    ], "warn")
    body += co
    write("net-04-taxonomy.svg", w, h, body, "How to decode Google Cloud load balancer names")


def fig_failover():
    w, h = 940, 790
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Active-active and active-passive are different architectures",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "One load balancer cannot do both. Read the requirement "
                            "before you pick the shape.", 11, c.GREY))

    body.append(c.rect(24, 82, 440, 246, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 108, "ACTIVE-ACTIVE  -  route everyone to their nearest",
                    10.5, c.BLUE, "700"))
    body += node(44, 128, 180, 44, "one anycast IP", None, col=c.BLUE)
    body += node(44, 186, 180, 44, "global external ALB", None, col=c.BLUE)
    body += node(44, 244, 180, 44, "Premium Tier", None, col=c.BLUE)
    body += node(268, 142, 172, 40, "us-east1", None, col=c.GREEN, fill="#f2fbf5")
    body += node(268, 194, 172, 40, "us-west1", None, col=c.GREEN, fill="#f2fbf5")
    body += node(268, 246, 172, 40, "asia-east1", None, col=c.GREEN, fill="#f2fbf5")
    for yy in (162, 214, 266):
        body.append(c.path("M 224 208 C 246 208 248 %s 268 %s" % (yy, yy),
                           stroke=c.GREEN, sw=1.5))
    body.append(c.t(244, 312, "all serving, all the time", 10.5, c.BLUE, "700", "middle"))

    body.append(c.rect(476, 82, 440, 246, fill="#faf5ff", stroke=c.PURPLE, rx=10, sw=1.6))
    body.append(c.t(496, 108, "ACTIVE-PASSIVE  -  use this one unless it is gone",
                    10.5, c.PURPLE, "700"))
    body += node(496, 128, 180, 44, "Cloud DNS record", None, col=c.PURPLE)
    body += node(496, 186, 180, 44, "failover policy", None, col=c.PURPLE)
    body += node(496, 244, 180, 44, "health check", None, col=c.PURPLE)
    body += node(720, 150, 180, 44, "PRIMARY  us-east1", None, col=c.GREEN, fill="#f2fbf5")
    body += node(720, 224, 180, 44, "BACKUP  us-west1", None, col=c.GREY, fill="#f8f9fa")
    body.append(c.path("M 676 208 C 700 208 700 172 720 172", stroke=c.GREEN, sw=2))
    body.append(c.path("M 676 208 C 700 208 700 246 720 246", stroke="#bdc1c6", sw=1.6,
                       dash="4 4"))
    body.append(c.t(810, 292, "idle until the primary fails", 9.5, c.GREY, "400", "middle"))
    body.append(c.t(696, 312, "regional external ALBs - only these can be a backup",
                    10.5, c.PURPLE, "700", "middle"))

    body.append(c.t(24, 366, "Three constraints on the failover setup", 12.5, c.TEXT, "700"))
    rows = [
        ("Only regional external ALBs can be the BACKUP", c.AMBER,
         "The primary may be global, regional or classic. The standby target must be regional."),
        ("The health check needs EXACTLY three source regions", c.AMBER,
         "Three vantage points separate a real regional outage from one unlucky probe path."),
        ("Failover is not instant", c.AMBER,
         "outage  =  DNS TTL  +  (check interval x unhealthy threshold).  Set TTL to 30-60s."),
    ]
    y = 384
    for name, col, desc in rows:
        body.append(c.rect(24, y, w - 48, 52, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 52, fill=col, rx=2.5))
        body.append(c.t(44, y + 22, name, 11.5, c.TEXT, "700"))
        body.append(c.t(44, y + 40, desc, 10, c.GREY))
        y += 60

    body.append(c.t(24, y + 24, "And what does NOT give you active-passive",
                    12.5, c.TEXT, "700"))
    body += c.grid(24, y + 40, ["Reached for", "What it really does"],
                   [["capacityScaler = 0",
                     "removes the backend entirely - nothing left to fail over to"],
                    ["outlier detection",
                     "active-active: steers away from backends returning errors"],
                    ["STRICT traffic isolation",
                     "the opposite - blocks cross-region failover, requests just fail"],
                    ["cross-region internal ALB",
                     "internal only - external client traffic never reaches it"],
                    ["Cloud DNS geolocation",
                     "active-active: routes by where the client is, not by preference"]],
                   [246, 646])

    write("net-05-failover.svg", w, h, body,
          "Active-active versus active-passive load balancing")


if __name__ == "__main__":
    print("Generating networking figures into %s" % HERE)
    fig_journey()
    fig_anatomy()
    fig_healthcheck()
    fig_taxonomy()
    fig_failover()
    print("done.")
