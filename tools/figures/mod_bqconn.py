# -*- coding: utf-8 -*-
"""Diagrams for the BigQuery connections / federated data module.

Run:  python tools/figures/mod_bqconn.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("bqconn")

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


# --------------------------------------------------------------------------

def fig_two_hops():
    w, h = 940, 600
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "A federated query is two hops, and they need different grants",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The analyst never touches Cloud SQL. The connection does — "
                            "using its own service account.", 11, c.GREY))

    # actors
    body += node(30, 110, 150, 62, "Analyst", "a human", col=c.GREY)
    body += node(258, 110, 190, 62, "The connection", "a BigQuery resource", col=c.BLUE,
                 fill="#f8fbff")
    body += node(524, 110, 190, 62, "Connection SA", "auto-created by GCP",
                 col=c.PURPLE, fill="#faf5ff")
    body += node(766, 110, 148, 62, "Cloud SQL", "the database", col=c.GREEN,
                 fill="#f2fbf5")

    body += arrow(180, 141, 258, 141, col=c.BLUE, sw=1.8)
    body += arrow(448, 141, 524, 141, col="#bdc1c6", sw=1.5)
    body += arrow(714, 141, 766, 141, col=c.GREEN, sw=1.8)

    # grants under each hop
    body.append(c.rect(190, 196, 300, 74, fill="#f8fbff", stroke=c.BLUE, rx=8, sw=1.4))
    body.append(c.t(340, 218, "HOP 1  —  grant to the person", 10, c.BLUE, "700", "middle"))
    body.append(c.mono(340, 238, "roles/bigquery.connectionUser", 11, c.TEXT, "500", "middle"))
    body.append(c.t(340, 256, "on the connection resource", 9.5, c.GREY, "400", "middle"))

    body.append(c.rect(600, 196, 314, 74, fill="#f2fbf5", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.t(757, 218, "HOP 2  —  grant to the service account", 10, c.GREEN,
                    "700", "middle"))
    body.append(c.mono(757, 238, "roles/cloudsql.client", 11, c.TEXT, "500", "middle"))
    body.append(c.t(757, 256, "on the Cloud SQL project", 9.5, c.GREY, "400", "middle"))

    body.append(c.line(340, 172, 340, 196, c.BLUE, 1.3, dash="3 3"))
    body.append(c.line(757, 172, 757, 196, c.GREEN, 1.3, dash="3 3"))

    body.append(c.t(24, 310, "Why the analyst does not get cloudsql.client",
                    12.5, c.TEXT, "700"))
    body.append(c.rect(24, 326, w - 48, 68, fill="#fff8f7", stroke=c.RED, rx=8, sw=1.3))
    body.append(c.rect(24, 326, 5, 68, fill=c.RED, rx=2.5))
    body.append(c.t(44, 348, "Granting it directly works — and defeats the design",
                    11.5, c.TEXT, "700"))
    body.append(c.t(44, 366, "The whole point of a connection is that database credentials "
                             "live in one managed resource instead of being handed out. Give "
                             "the analyst", 10, c.GREY))
    body.append(c.t(44, 382, "cloudsql.client and they can now reach that instance from "
                             "anywhere, by any means, with no connection involved.",
                    10, c.GREY))

    body.append(c.t(24, 428, "The two roles that are easy to confuse", 12.5, c.TEXT, "700"))
    body += c.grid(24, 444, ["Role", "Can run queries through a connection",
                             "Can create / edit / delete connections"],
                   [["roles/bigquery.connectionUser", "yes", "no"],
                    ["roles/bigquery.connectionAdmin", "yes", "yes"]],
                   [300, 300, 292])

    co, _ = c.callout(24, 532, w - 48, [
        "\"Run queries but not manage connections\" is connectionUser, every time. connectionAdmin is",
        "for whoever sets the connection up once - not for the people using it every day.",
    ], "ok")
    body += co
    write("bqc-01-two-hops.svg", w, h, body,
          "The two IAM grants a federated query needs")


def fig_roles():
    w, h = 940, 600
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Roles that sound like they would work, and don't",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Connection permissions live on the connection. Nothing else "
                            "grants them by implication.", 11, c.GREY))

    rows = [
        ("roles/bigquery.dataViewer", c.RED, "on the dataset",
         "Read the tables. Says nothing about connections — a federated query still fails."),
        ("roles/bigquery.user", c.RED, "on the project",
         "Run jobs, create datasets. Still no permission to use a connection resource."),
        ("roles/bigquery.admin", c.AMBER, "on the project",
         "Works, because it contains everything — which is exactly why it is the wrong answer."),
        ("roles/bigquery.connectionUser", c.GREEN, "on the connection",
         "The one that grants it, scoped to a single connection. This is the answer."),
    ]
    y = 92
    for name, col, scope, desc in rows:
        body.append(c.rect(24, y, w - 48, 68, fill="#ffffff", stroke=col, rx=8, sw=1.4))
        body.append(c.rect(24, y, 5, 68, fill=col, rx=2.5))
        body.append(c.mono(44, y + 26, name, 12, c.TEXT, "500"))
        ch, _cw = c.chip(400, y + 14, scope, fill="#f1f3f4", fg=c.GREY)
        body += ch
        body.append(c.t(44, y + 50, desc, 10, c.GREY))
        y += 78

    body.append(c.t(24, y + 24, "The query it enables", 12.5, c.TEXT, "700"))
    sq, _sh = c.sql_block(24, y + 36, w - 48, [
        (0, [("SELECT", c.BLUE), (" c.customer_id, s.plan_tier, s.monthly_charges", c.TEXT)]),
        (0, [("FROM", c.BLUE), (" `proj.crm.customers`", "#137333"), (" AS c", c.TEXT)]),
        (0, [("JOIN ", c.BLUE), ("EXTERNAL_QUERY", "#8430ce"),
             ("(", c.TEXT), ('"us-central1.billing-db"', "#0d652d"), (",", c.TEXT)]),
        (1, [('"SELECT customer_id, plan_tier, monthly_charges FROM subs"', "#0d652d"),
             (") AS s", c.TEXT)]),
        (0, [("USING", c.BLUE), (" (customer_id)", c.TEXT)]),
    ], title="A federated join, from the analyst's side")
    body += sq
    write("bqc-02-roles.svg", w, h, body,
          "Which IAM role actually enables a federated query")


if __name__ == "__main__":
    print("Generating BigQuery connection figures into %s" % HERE)
    fig_two_hops()
    fig_roles()
    print("done.")
