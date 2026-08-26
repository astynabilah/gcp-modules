# -*- coding: utf-8 -*-
"""Diagrams for the Cloud Composer / DAG module.

Run:  python tools/figures/mod_composer.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("composer")

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

def fig_dag():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "A DAG is three words, each doing work", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Directed Acyclic Graph. Boxes, one-way arrows, and no "
                            "way back to where you started.", 11, c.GREY))

    # the graph
    body.append(c.rect(24, 84, w - 48, 190, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.5))
    body += node(48, 150, 140, 50, "extract", None, col=c.BLUE)
    body += node(228, 150, 140, 50, "validate", None, col=c.BLUE)
    body += node(408, 106, 140, 50, "profile_data", None, col=c.PURPLE)
    body += node(408, 194, 140, 50, "train", None, col=c.BLUE)
    body += node(588, 194, 140, 50, "evaluate", None, col=c.BLUE)
    body += node(768, 194, 130, 50, "register", None, col=c.BLUE)

    body += arrow(188, 175, 228, 175)
    body += arrow(368, 168, 408, 136, col=c.PURPLE)
    body += arrow(368, 182, 408, 214)
    body += arrow(548, 219, 588, 219)
    body += arrow(728, 219, 768, 219)

    body.append(c.t(430, 290, "profile_data and train share an upstream and nothing else "
                              "- so they run at the same time",
                    10.5, c.GREY, "400", "middle"))

    rows = [
        ("Graph", "Boxes with arrows between them. The boxes are tasks."),
        ("Directed", "The arrows point one way. extract -> validate is not the reverse."),
        ("Acyclic", "No path leads back to its own start. This is what makes it runnable: "
                    "there is always something with no unmet dependency."),
    ]
    y = 318
    for k, v in rows:
        body.append(c.rect(24, y, w - 48, 44, fill="#ffffff", stroke=c.BORDER, rx=8))
        body.append(c.rect(24, y, 5, 44, fill=c.BLUE, rx=2.5))
        body.append(c.t(44, y + 27, k, 12, c.TEXT, "700"))
        body.append(c.t(150, y + 27, v, 10.5, c.GREY))
        y += 52

    co, _ = c.callout(24, y + 6, w - 48, [
        "Every orchestrator is a DAG engine - Airflow, Kubeflow, Cloud Build, make, Spark's plan.",
        "\"What depends on what, and what can run at once\" is the only question they answer.",
    ], "ok")
    body += co
    write("cm-01-what-is-a-dag.svg", w, h, body, "What a DAG is")


def fig_crossdag():
    w, h = 940, 620
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Two teams, two DAGs, one dependency", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Push or pull. The difference is who has to know about whom.",
                    11, c.GREY))

    # push
    body.append(c.rect(24, 82, 440, 230, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(44, 108, "PUSH  -  TriggerDagRunOperator", 10.5, c.GREEN, "700"))
    body.append(c.t(44, 126, "recommended", 9.5, c.GREY))
    body += node(44, 142, 190, 46, "DAG A: preprocess", "data eng team", col=c.GREY)
    body += node(44, 200, 190, 46, "trigger_training", "a task in A", col=c.GREEN)
    body.append(c.line(139, 188, 139, 200, c.GREY, 1.4))
    body += node(268, 172, 176, 46, "DAG B: training", "ML team", col=c.GREY)
    body += arrow(234, 223, 268, 202, col=c.GREEN, sw=1.8)
    body.append(c.t(244, 272, "A knows only B's dag_id. No polling. Passes conf.",
                    10, c.GREEN, "700", "middle"))
    body.append(c.t(244, 290, "B needs no schedule of its own.", 10, c.GREY, "400", "middle"))

    # pull
    body.append(c.rect(476, 82, 440, 230, fill="#fff8e6", stroke=c.AMBER, rx=10, sw=1.6))
    body.append(c.t(496, 108, "PULL  -  ExternalTaskSensor", 10.5, c.AMBER, "700"))
    body.append(c.t(496, 126, "for multi-upstream cases", 9.5, c.GREY))
    body += node(496, 172, 176, 46, "DAG A: preprocess", "data eng team", col=c.GREY)
    body += node(722, 142, 190, 46, "DAG B: training", "ML team", col=c.GREY)
    body += node(722, 200, 190, 46, "wait_for_...", "a task in B", col=c.AMBER)
    body.append(c.line(817, 188, 817, 200, c.GREY, 1.4))
    body += arrow(722, 223, 672, 202, col=c.AMBER, sw=1.8, dash="4 3")
    body.append(c.t(696, 272, "B hard-codes a TASK ID inside A. Polls. Dates must align.",
                    10, c.AMBER, "700", "middle"))
    body.append(c.t(696, 290, "A rename in A leaves B waiting forever.",
                    10, c.GREY, "400", "middle"))

    body.append(c.t(24, 348, "And the two that are not answers", 12.5, c.TEXT, "700"))
    rows = [
        ("TaskGroup", c.RED,
         "Visual grouping inside ONE DAG - a collapsible box in the UI.",
         "No separate ownership, deployment, schedule or permissions. Merging loses the boundary."),
        ("SubDagOperator", c.RED,
         "Deprecated in Airflow; Google's docs recommend against it.",
         "Ran a nested DAG inside a task and consumed worker slots in ways that deadlocked."),
        ("Datasets  (Airflow 2.4+)", c.GREEN,
         "A third real option: A declares an outlet, B is scheduled by it.",
         "Coupling is on a shared ARTIFACT, not on either DAG's internals. Cleanest boundary."),
    ]
    y = 366
    for name, col, l1, l2 in rows:
        body.append(c.rect(24, y, w - 48, 56, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 56, fill=col, rx=2.5))
        body.append(c.t(44, y + 23, name, 11.5, c.TEXT, "700"))
        body.append(c.t(232, y + 23, l1, 10, c.TEXT))
        body.append(c.t(44, y + 43, l2, 9.5, c.GREY))
        y += 64

    co, _ = c.callout(24, y + 6, w - 48, [
        "\"Separate logical boundaries for different team ownership\" rules out merging before you",
        "read the rest of the option. TaskGroup draws a box; it does not give a team a repository.",
    ], "warn")
    body += co
    write("cm-02-cross-dag.svg", w, h, body, "Cross-DAG dependency patterns in Airflow")


if __name__ == "__main__":
    print("Generating Composer figures into %s" % HERE)
    fig_dag()
    fig_crossdag()
    print("done.")
