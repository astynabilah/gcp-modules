import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("cicd")

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

def fig_privilege():
    w, h = 940, 660
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The default service account is the whole problem",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Three ML teams, three repositories. What each build can actually "
                            "reach.", 11, c.GREY))

    # ---- default
    body.append(c.rect(24, 78, 440, 220, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.6))
    body.append(c.t(44, 102, "DEFAULT CLOUD BUILD SERVICE ACCOUNT", 10.5, c.RED, "700"))
    body.append(c.t(44, 120, "Permissions granted at the PROJECT level.", 10, c.GREY))

    body += node(44, 136, 150, 44, "Team A trigger", None, col=c.GREY)
    body += node(44, 188, 150, 44, "Team B trigger", None, col=c.GREY)
    body += node(44, 240, 150, 44, "Team C trigger", None, col=c.GREY)
    body += node(232, 188, 106, 44, "default SA", None, col=c.RED)
    for yy in (158, 210, 262):
        body.append(c.path("M 194 %s C 212 %s 214 210 232 210" % (yy, yy),
                           stroke=c.GREY, sw=1.4))
    for i, yy in enumerate((136, 188, 240)):
        body += node(360, yy, 84, 44, "repo %s" % "ABC"[i], None, col=c.RED)
        body.append(c.path("M 338 210 C 350 210 348 %s 360 %s" % (yy + 22, yy + 22),
                           stroke=c.RED, sw=1.6))
    body.append(c.t(244, 306, "every build can push to every repository",
                    10.5, c.RED, "700", "middle"))

    # ---- least privilege
    body.append(c.rect(476, 78, 440, 220, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(496, 102, "PER-TRIGGER SERVICE ACCOUNTS", 10.5, c.GREEN, "700"))
    body.append(c.t(496, 120, "artifactregistry.writer on ONE repository each.", 10, c.GREY))

    for i, yy in enumerate((136, 188, 240)):
        t = "ABC"[i]
        body += node(496, yy, 138, 44, "Team %s trigger" % t, None, col=c.GREY)
        body += node(652, yy, 116, 44, "sa-team-%s" % t.lower(), None, col=c.GREEN)
        body += node(786, yy, 84, 44, "repo %s" % t, None, col=c.GREEN)
        body += arrow(634, yy + 22, 652, yy + 22, col="#bdc1c6", sw=1.3)
        body += arrow(768, yy + 22, 786, yy + 22, col=c.GREEN, sw=1.6)
    body.append(c.t(696, 306, "a compromised build reaches exactly one repository",
                    10.5, c.GREEN, "700", "middle"))

    body.append(c.t(24, 350, "Why the alternatives do not isolate", 12.5, c.TEXT, "700"))
    rows = [
        ("VPC Service Controls", c.RED,
         "A network perimeter, not an IAM boundary. It stops data leaving the perimeter;",
         "it does not stop Team A's build pushing into Team B's repo inside it."),
        ("One repo, folder per team", c.RED,
         "Artifact Registry grants IAM per REPOSITORY. Paths inside one repository share",
         "its bindings, so a path is a naming convention, not an access boundary."),
        ("A project per team", c.AMBER,
         "Genuinely isolates - and is real overhead: quotas, billing, networking, IAM",
         "in triplicate. Justified by org structure, not by wanting separate repos."),
    ]
    y = 374
    for name, col, l1, l2 in rows:
        body.append(c.rect(24, y, w - 48, 62, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 62, fill=col, rx=2.5))
        body.append(c.t(44, y + 22, name, 11.5, c.TEXT, "700"))
        body.append(c.t(44, y + 40, l1, 10, c.GREY))
        body.append(c.t(44, y + 54, l2, 10, c.GREY))
        y += 70

    co, _ = c.callout(24, y + 4, w - 48, [
        "Least privilege here is two settings: a custom service account on the trigger, and a",
        "repository-scoped role binding rather than a project-scoped one. Neither needs new projects.",
    ], "ok")
    body += co
    write("ci-01-least-privilege.svg", w, h, body,
          "Default versus per-trigger service accounts for Artifact Registry")


def fig_pipeline():
    w, h = 940, 520
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "What an ML build actually does — two pipelines, not one",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "App CI ships code. ML CI ships code AND may retrain a model. "
                            "Keep them separate.", 11, c.GREY))

    # code pipeline
    body.append(c.rect(24, 78, w - 48, 150, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.5))
    body.append(c.t(44, 102, "1. CODE PIPELINE — on every push", 10.5, c.BLUE, "700"))
    steps = [("Lint + test", 44), ("Build image", 216), ("Push to AR", 388),
             ("Compile pipeline", 560), ("Upload YAML", 732)]
    for name, x in steps:
        body += node(x, 122, 156, 46, name, None, col=c.BLUE)
        if x < 700:
            body += arrow(x + 156, 145, x + 172, 145, col="#bdc1c6", sw=1.3)
    body.append(c.t(44, 200, "Fast, runs constantly, and never touches production data. "
                             "This is ordinary CI.", 10, c.GREY))

    # model pipeline
    body.append(c.rect(24, 244, w - 48, 168, fill="#faf5ff", stroke=c.PURPLE, rx=10, sw=1.5))
    body.append(c.t(44, 268, "2. MODEL PIPELINE — on a schedule, or on new data",
                    10.5, c.PURPLE, "700"))
    steps2 = [("Rebuild features", 44), ("Train", 216), ("Evaluate", 388),
              ("Quality gate", 560), ("Register", 732)]
    for name, x in steps2:
        col = c.AMBER if name == "Quality gate" else c.PURPLE
        body += node(x, 288, 156, 46, name, None, col=col)
        if x < 700:
            body += arrow(x + 156, 311, x + 172, 311, col="#bdc1c6", sw=1.3)
    body.append(c.t(44, 366, "Slow, expensive, and the gate decides whether the model is "
                             "allowed to exist.", 10, c.GREY))
    body.append(c.t(44, 384, "This is a Vertex AI Pipeline - CI submits it, CI does not "
                             "contain it.", 10, c.TEXT))

    co, _ = c.callout(24, 428, w - 48, [
        "Conflating the two is the usual mistake: a code push should not retrain a model, and a",
        "retrain should not wait on a linter. Cloud Build compiles and submits the pipeline; the",
        "pipeline does the ML. Keeping the boundary means a broken test cannot block a retrain, and",
        "a bad model cannot be shipped by a green build.",
    ], "warn")
    body += co
    write("ci-02-two-pipelines.svg", w, h, body,
          "The code pipeline and the model pipeline are separate")


if __name__ == "__main__":
    print("Generating CI/CD figures into %s" % HERE)
    fig_privilege()
    fig_pipeline()
    print("done.")
