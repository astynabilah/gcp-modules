import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("git")

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

def fig_setup():
    w, h = 940, 656
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Workbench to GitHub over SSH — the whole setup",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Every step happens INSIDE the instance. Nothing is configured in "
                            "the Google Cloud console.", 11, c.GREY))

    steps = [
        ("1", "Identify yourself", c.BLUE,
         "git config --global user.name  \"you\"",
         "git config --global user.email \"you@example.com\"",
         "Without this, commits are rejected or attributed to nobody."),
        ("2", "Generate a key IN the instance", c.GREEN,
         "ssh-keygen -t ed25519 -C \"you@example.com\"",
         "cat ~/.ssh/id_ed25519.pub",
         "Generate it here. Do not copy a key in from your laptop or a bucket."),
        ("3", "Add the PUBLIC key to GitHub", c.PURPLE,
         "GitHub > Settings > SSH and GPG keys > New SSH key",
         "paste the contents of id_ed25519.pub",
         "The private key never leaves the instance. Only the .pub half travels."),
        ("4", "Clone, commit, push", c.AMBER,
         "git clone git@github.com:org/repo.git",
         "git add -A && git commit -m \"...\" && git push",
         "Or use the preinstalled jupyterlab-git panel for the same operations."),
    ]
    y = 82
    for num, name, col, cmd1, cmd2, note in steps:
        body.append(c.rect(24, y, w - 48, 112, fill="#ffffff", stroke=col, rx=9, sw=1.5))
        body.append(c.rect(24, y, 6, 112, fill=col, rx=3))
        body.append(c.circle(56, y + 28, 14, fill=col, op=0.16))
        body.append(c.t(56, y + 33, num, 13, col, "700", "middle"))
        body.append(c.t(82, y + 33, name, 12.5, c.TEXT, "700"))
        body.append(c.rect(82, y + 46, w - 130, 44, fill=c.PANEL, rx=5))
        body.append(c.mono(96, y + 63, cmd1, 10.5, c.TEXT))
        body.append(c.mono(96, y + 81, cmd2, 10.5, c.TEXT))
        body.append(c.t(82, y + 104, note, 10, c.GREY))
        y += 120

    co, _ = c.callout(24, y + 4, w - 48, [
        "There is no console-based OAuth integration between Workbench and GitHub, and third-party",
        "JupyterLab extensions are not supported. The jupyterlab-git extension is already installed —",
        "you configure credentials with ordinary git commands in the terminal.",
    ], "info")
    body += co
    write("gt-01-setup.svg", w, h, body, "Configuring Git and SSH on a Workbench instance")


def fig_notebooks():
    w, h = 940, 612
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Why notebooks are bad in Git — and the three fixes",
                    15, c.TEXT, "500"))

    body.append(c.rect(24, 62, w - 48, 128, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.5))
    body.append(c.t(44, 86, "THE PROBLEM", 10.5, c.RED, "700"))
    body.append(c.t(44, 108, "A .ipynb file is JSON, not code. One changed cell can produce a "
                             "thousand-line diff.", 10.5, c.TEXT))
    for i, ln in enumerate([
        "Outputs are stored in the file - images become base64 blobs, dataframes become HTML.",
        "Execution counts change on every run, so the file is dirty even when the code is not.",
        "Merge conflicts land inside JSON and are close to unresolvable by hand.",
        "Anything printed is committed - including tokens, connection strings and customer rows.",
    ]):
        body.append(c.t(44, 132 + i * 15, "- " + ln, 10, c.GREY))

    fixes = [
        ("nbstripout", c.GREEN, "strip outputs on commit",
         "A git filter that removes output cells as you commit.",
         "The notebook keeps its outputs locally; the repo only ever sees code.",
         "pip install nbstripout && nbstripout --install"),
        ("jupytext", c.BLUE, "pair with a text file",
         "Keeps a .py or .md twin in sync with the notebook.",
         "You commit the readable twin and can ignore the .ipynb entirely.",
         "jupytext --set-formats ipynb,py:percent notebook.ipynb"),
        ("nbdime", c.PURPLE, "diff notebooks properly",
         "Notebook-aware diff and merge, cell by cell.",
         "Use when you must keep outputs and still review changes.",
         "pip install nbdime && nbdime config-git --enable"),
    ]
    y = 208
    for name, col, tag, l1, l2, cmd in fixes:
        body.append(c.rect(24, y, w - 48, 100, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, 100, fill=col, rx=3))
        body.append(c.mono(46, y + 26, name, 12, c.TEXT))
        ch, cw = c.chip(160, y + 14, tag, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 48, l1, 10.5, c.TEXT))
        body.append(c.t(46, y + 65, l2, 10, c.GREY))
        body.append(c.rect(46, y + 74, w - 94, 20, fill=c.PANEL, rx=4))
        body.append(c.mono(58, y + 88, cmd, 10, col))
        y += 108

    co, _ = c.callout(24, y + 4, w - 48, [
        "The strongest habit is not a tool: keep the real logic OUT of notebooks. SQL in .sql files,",
        "transforms in .py modules, notebooks as thin drivers. Then the notebook diff barely matters",
        "because the notebook barely matters.",
    ], "ok")
    body += co
    write("gt-02-notebooks.svg", w, h, body, "Why notebooks diff badly in Git and how to fix it")


if __name__ == "__main__":
    print("Generating Git figures into %s" % HERE)
    fig_setup()
    fig_notebooks()
    print("done.")
