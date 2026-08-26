# -*- coding: utf-8 -*-
"""Builds the whole repository.

  1. regenerates and validates every SVG figure
  2. extracts every SQL block from the labs into mlops-gcp/labs/sql/labNN/
  3. renders every .md into a self-contained HTML page in site/

Layout
------
  tools/              all build code: this file, svgkit, check_svg, figures/
  mlops-gcp/labs/     lab sources (.md), figures/ + sql/ (both generated)
  mlops-gcp/modules/  module sources (.md), assets/ (generated)
  site/               ALL generated HTML, flat (generated)

Nothing outside tools/ is hand-written Python: the content folders hold only
prose, figures and SQL.

Run:  python tools/build.py
"""
import glob
import io
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import markdown

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
SITE = os.path.join(ROOT, "site")


def _discover():
    """Every learning-path folder: any child dir holding both labs/ and modules/.

    Paths are discovered rather than listed, so adding a new one — genai-gcp,
    data-eng-gcp — needs no edit here. Returns them sorted, outermost first.
    """
    found = []
    for depth in ("*", "*/*"):
        for cand in sorted(glob.glob(os.path.join(ROOT, depth))):
            if (os.path.isdir(os.path.join(cand, "modules"))
                    and os.path.exists(os.path.join(cand, "README.md"))
                    and cand not in found):
                found.append(cand)
    if not found:
        raise SystemExit("build.py: no folder containing labs/ and modules/")
    return found


def _title_of(md_path, fallback):
    """A document's title is its first H1. Keeping it in the document means
    adding content never requires editing this file."""
    try:
        for line in io.open(md_path, encoding="utf-8"):
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return fallback


def _docs(directory):
    """Every .md in a directory except its README, as (filename, title)."""
    out = []
    for f in sorted(glob.glob(os.path.join(directory, "*.md"))):
        name = os.path.basename(f)
        if name.lower() == "readme.md":
            continue
        out.append((name, _title_of(f, name[:-3])))
    return out


class Path(object):
    """One learning path: its folders, documents and index pages."""

    def __init__(self, directory):
        self.dir = directory
        self.name = os.path.basename(directory)
        self.labs_dir = os.path.join(directory, "labs")
        self.modules_dir = os.path.join(directory, "modules")
        self.labs = _docs(self.labs_dir)
        self.modules = _docs(self.modules_dir)

    def sql_subdir(self, lab_filename):
        """lab-03-serving-....md -> lab03, matching the existing sql/ layout."""
        m = re.match(r"lab-(\d+)", lab_filename)
        return "lab%s" % m.group(1) if m else None

    def html_for(self, filename):
        """Flat output, prefixed by path name only where paths could collide."""
        return filename[:-3] + ".html"

    @property
    def figure_dirs(self):
        return ([os.path.join(self.labs_dir, "figures")]
                + sorted(glob.glob(os.path.join(self.modules_dir, "assets", "*"))))

    @property
    def indexes(self):
        out = []
        for src, out_html, title in (
                (os.path.join(self.dir, "README.md"), self.name + ".html", self.name),
                (os.path.join(self.dir, "ROADMAP.md"),
                 self.name + "-roadmap.html", "The big picture"),
                (os.path.join(self.labs_dir, "README.md"),
                 self.name + "-labs.html", "The labs"),
                (os.path.join(self.modules_dir, "README.md"),
                 self.name + "-modules.html", "The modules")):
            if os.path.exists(src):
                out.append((src, out_html, _title_of(src, title)))
        return out


PATHS = [Path(d) for d in _discover()]

BUILD_DATE = "23 August 2026"

# The repo README is the global landing page; each path carries its own.
INDEXES = [(os.path.join(ROOT, "README.md"), "index.html",
            "Google Cloud learning material"),
           (os.path.join(TOOLS, "README.md"), "tools.html", "The build system")]
for _p in PATHS:
    INDEXES.extend(_p.indexes)

# every generator in tools/figures/, and the directories they write into
GENERATORS = sorted(glob.glob(os.path.join(TOOLS, "figures", "*.py")))
FIGURE_DIRS = [d for _p in PATHS for d in _p.figure_dirs]
CHECKER = os.path.join(TOOLS, "check_svg.py")

CSS = """
:root{
  --bg:#ffffff; --fg:#202124; --muted:#5f6368; --line:#dadce0; --panel:#f8f9fa;
  --blue:#1a73e8; --blue-bg:#e8f0fe; --green:#188038; --green-bg:#e6f4ea;
  --amber:#b06000; --amber-bg:#fef7e0; --code-bg:#f6f8fa; --code-fg:#24292f;
  --kw:#0550ae; --str:#0a7d33; --com:#6e7781; --num:#953800; --fn:#8250df;
  --shadow:0 1px 3px rgba(60,64,67,.16),0 4px 12px rgba(60,64,67,.10);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#131417; --fg:#e8eaed; --muted:#9aa0a6; --line:#33363b; --panel:#1c1e22;
    --blue:#8ab4f8; --blue-bg:#1c2b45; --green:#81c995; --green-bg:#1b2e21;
    --amber:#fdd663; --amber-bg:#332a12; --code-bg:#1b1d21; --code-fg:#e6e6e6;
    --kw:#79b8ff; --str:#8ddb8c; --com:#8b949e; --num:#ffab70; --fn:#d2a8ff;
    --shadow:0 1px 3px rgba(0,0,0,.5),0 6px 18px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"]{
  --bg:#131417; --fg:#e8eaed; --muted:#9aa0a6; --line:#33363b; --panel:#1c1e22;
  --blue:#8ab4f8; --blue-bg:#1c2b45; --green:#81c995; --green-bg:#1b2e21;
  --amber:#fdd663; --amber-bg:#332a12; --code-bg:#1b1d21; --code-fg:#e6e6e6;
  --kw:#79b8ff; --str:#8ddb8c; --com:#8b949e; --num:#ffab70; --fn:#d2a8ff;
  --shadow:0 1px 3px rgba(0,0,0,.5),0 6px 18px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.68 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Google Sans',Arial,sans-serif;
}
.wrap{max-width:900px;margin:0 auto;padding:40px 22px 100px}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
h1{font-size:2.05rem;line-height:1.22;letter-spacing:-.02em;margin:.2em 0 .5em;font-weight:600}
h2{font-size:1.42rem;line-height:1.3;margin:2.4em 0 .7em;padding-top:1.1em;
   border-top:1px solid var(--line);font-weight:600;letter-spacing:-.01em}
h3{font-size:1.12rem;margin:1.9em 0 .6em;font-weight:600}
h4{font-size:1rem;margin:1.5em 0 .5em;font-weight:600;color:var(--muted)}
h2:first-of-type{border-top:none}
p,li{overflow-wrap:break-word}
ul,ol{padding-left:1.4em}
li{margin:.34em 0}
li input[type=checkbox]{margin-right:.5em}
hr{border:none;border-top:1px solid var(--line);margin:2.6em 0}
blockquote{
  margin:1.5em 0;padding:.85em 1.1em;background:var(--blue-bg);
  border-left:4px solid var(--blue);border-radius:0 8px 8px 0;
}
blockquote p{margin:.4em 0}
blockquote strong:first-child{color:var(--blue)}
code{
  font-family:'Roboto Mono','SF Mono',Consolas,'Cascadia Mono',monospace;
  font-size:.875em;background:var(--panel);padding:.15em .38em;border-radius:4px;
  border:1px solid var(--line);
}
pre{
  background:var(--code-bg);border:1px solid var(--line);border-radius:10px;
  padding:16px 18px;overflow-x:auto;margin:1.3em 0;line-height:1.55;
}
pre code{background:none;border:none;padding:0;font-size:.845rem;color:var(--code-fg)}
table{border-collapse:collapse;width:100%;margin:1.4em 0;font-size:.925rem;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:9px 13px;text-align:left;vertical-align:top}
th{background:var(--panel);font-weight:600;white-space:nowrap}
figure{margin:1.9em 0}
figure svg{
  width:100%;height:auto;display:block;border-radius:10px;box-shadow:var(--shadow);
  background:#fff;
}
figcaption{
  margin-top:.7em;font-size:.83rem;color:var(--muted);text-align:center;font-style:italic;
}
details{
  border:1px solid var(--line);border-radius:10px;padding:.75em 1.05em;margin:.7em 0;
  background:var(--panel);
}
details[open]{background:var(--bg)}
summary{cursor:pointer;font-weight:500}
summary::marker{color:var(--blue)}
details p{margin:.85em 0 .2em}
.hl .k,.hl .kn,.hl .kd,.hl .kt,.hl .kr,.hl .kc{color:var(--kw);font-weight:600}
.hl .s,.hl .s1,.hl .s2,.hl .sb,.hl .se,.hl .sd{color:var(--str)}
.hl .c,.hl .c1,.hl .cm,.hl .cp{color:var(--com);font-style:italic}
.hl .m,.hl .mi,.hl .mf{color:var(--num)}
.hl .nb,.hl .nf{color:var(--fn)}
.hl .o,.hl .p{color:var(--muted)}
.toc{
  background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:8px 20px 16px;margin:1.6em 0 2.4em;font-size:.93rem;
}
.toc>ul{padding-left:1.1em}
.toc ul ul{display:none}
.toc-title{font-weight:600;color:var(--fg);padding-top:12px;display:block}
.nav{font-size:.85rem;color:var(--muted);margin:0 0 1.4em}
.nav a{margin-right:1em}
.footer{margin-top:4em;padding-top:1.4em;border-top:1px solid var(--line);
        font-size:.85rem;color:var(--muted)}
@media (max-width:640px){
  .wrap{padding:26px 15px 70px}
  h1{font-size:1.6rem}
  h2{font-size:1.22rem}
  pre{font-size:.9em}
}
"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<style>%(css)s</style>
</head>
<body>
<div class="wrap">
%(nav)s
%(body)s
<div class="footer">Generated %(date)s · figures are illustrative mockups of the Google Cloud console, not live screenshots.</div>
</div>
</body>
</html>
"""


LINKS = {}
for _p in PATHS:
    for _name, _t in _p.labs + _p.modules:
        LINKS[_name] = _p.html_for(_name)


PAGE_PATH = [None]


def rewrite_links(html):
    """Everything lands flat in site/, so any .md link becomes a sibling .html."""
    for md, out in LINKS.items():
        # ](anything/NAME.md)  or  ](NAME.md)  , optional #anchor
        html = re.sub(r'\]\((?:[^)"\s]*/)?' + re.escape(md) + r'(#[^)]*)?\)',
                      lambda mo: '](%s%s)' % (out, mo.group(1) or ''), html)
        html = re.sub(r'href="(?:[^"]*/)?' + re.escape(md) + r'(#[^"]*)?"',
                      lambda mo: 'href="%s%s"' % (out, mo.group(1) or ''), html)
    # Index pages aren't in LINKS because several share the name README.md;
    # they're disambiguated by the directory they sit in.
    for _p in PATHS:
        n = re.escape(_p.name)
        html = re.sub(r'href="(?:[^"]*/)?' + n + r'/labs/README\.html',
                      'href="%s-labs.html' % _p.name, html)
        html = re.sub(r'href="(?:[^"]*/)?' + n + r'/modules/README\.html',
                      'href="%s-modules.html' % _p.name, html)
        html = re.sub(r'href="(?:[^"]*/)?' + n + r'/README\.html',
                      'href="%s.html' % _p.name, html)
        html = re.sub(r'href="(?:[^"]*/)?' + n + r'/ROADMAP\.html',
                      'href="%s-roadmap.html' % _p.name, html)
        html = html.replace('href="%s/"' % _p.name, 'href="%s.html"' % _p.name)
    # relative forms, resolved against whichever path the page belongs to
    if PAGE_PATH[0] is not None:
        n = PAGE_PATH[0].name
        html = re.sub(r'href="(?:\.\./)*labs/README\.html',
                      'href="%s-labs.html' % n, html)
        html = re.sub(r'href="(?:\.\./)*modules/README\.html',
                      'href="%s-modules.html' % n, html)
        html = re.sub(r'href="(?:\.\./)*ROADMAP\.html',
                      'href="%s-roadmap.html' % n, html)
    html = re.sub(r'href="(?:[^"]*/)?tools/README\.html', 'href="tools.html', html)
    html = html.replace('href="tools/"', 'href="tools.html"')
    return html


def slugify(text, used):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48] or "step"
    n, out = 2, s
    while out in used:
        out, n = "%s-%d" % (s, n), n + 1
    used.add(out)
    return out


def extract_sql(md_text, outdir, label):
    os.makedirs(outdir, exist_ok=True)
    for old in os.listdir(outdir):
        if old.endswith(".sql"):
            os.remove(os.path.join(outdir, old))
    heading = "intro"
    used, n, written = set(), 0, []
    # DOTALL is needed for the code-block body, so the heading branch must use
    # [^\n]+ rather than .+ or it swallows the whole document.
    pattern = re.compile(r"^(## [^\n]+)$|^```sql\n(.*?)^```$", re.M | re.S)
    for m in pattern.finditer(md_text):
        if m.group(1):
            heading = re.sub(r"^##\s*", "", m.group(1)).strip()
            continue
        sql = m.group(2).rstrip()
        n += 1
        name = "%02d-%s.sql" % (n, slugify(heading, used))
        io.open(os.path.join(outdir, name), "w", encoding="utf-8", newline="\n").write(
            "-- %s\n-- %s\n\n%s\n" % (label, heading, sql))
        written.append(name)
    return written


SVG_IMG = re.compile(r'<p><img alt="([^"]*)" src="([^"]+\.svg)"\s*/?></p>')


def inline_svgs(html, basedir):
    def repl(m):
        alt, src = m.group(1), m.group(2)
        path = os.path.normpath(os.path.join(basedir, src.replace("/", os.sep)))
        if not os.path.exists(path):
            print("      ! missing figure: %s" % src)
            return m.group(0)
        svg = io.open(path, encoding="utf-8").read()
        svg = re.sub(r'\s(width|height)="\d+"', "", svg, count=2)
        cap = ("<figcaption>%s</figcaption>" % alt) if alt else ""
        return "<figure>%s%s</figure>" % (svg, cap)
    return SVG_IMG.sub(repl, html)


def nav_for(pth):
    """The breadcrumb bar. Path pages get their own path's links; the repo
    landing page and tools/ get a link per path instead."""
    items = ['<a href="index.html">Home</a>']
    if pth is not None:
        items.append('<a href="%s.html">%s</a>' % (pth.name, pth.name))
        if os.path.exists(os.path.join(pth.dir, "ROADMAP.md")):
            items.append('<a href="%s-roadmap.html">Roadmap</a>' % pth.name)
        items.append('<a href="%s-labs.html">Labs</a>' % pth.name)
        items.append('<a href="%s-modules.html">Modules</a>' % pth.name)
    else:
        for other in PATHS:
            items.append('<a href="%s.html">%s</a>' % (other.name, other.name))
    return '<div class="nav">%s</div>' % "".join(items)


def render(md_path, title):
    basedir = os.path.dirname(os.path.abspath(md_path))
    text = io.open(md_path, encoding="utf-8").read()
    md = markdown.Markdown(extensions=[
        "fenced_code", "codehilite", "tables", "toc", "attr_list", "md_in_html", "sane_lists",
    ], extension_configs={
        "codehilite": {"css_class": "hl", "guess_lang": False},
        "toc": {"toc_depth": "2-2"},
    })
    body = md.convert(text)
    body = inline_svgs(body, basedir)
    body = rewrite_links(body)
    toc = re.sub(r'<span class="toctitle">.*?</span>', "", md.toc, flags=re.S)
    toc = toc.replace('<div class="toc">',
                      '<div class="toc"><span class="toc-title">On this page</span>')
    parts = body.split("</h1>", 1)
    if len(parts) == 2:
        body = parts[0] + "</h1>" + toc + parts[1]
    return PAGE % {"title": title, "css": CSS, "body": body,
                   "nav": nav_for(PAGE_PATH[0]), "date": BUILD_DATE}



def audit():
    """Catch the drift that silently accumulates: a module that exists but is
    listed nowhere, or a MODULES entry whose file was renamed.

    Deliberately does NOT assert on counts written into prose. Those go stale by
    design and chasing them is busywork; the numbers below are printed as a
    report, not a test."""
    problems = []

    for pth in PATHS:
        mod_readme_p = os.path.join(pth.modules_dir, "README.md")
        mod_readme = (io.open(mod_readme_p, encoding="utf-8").read()
                      if os.path.exists(mod_readme_p) else "")
        path_readme_p = os.path.join(pth.dir, "README.md")
        path_readme = (io.open(path_readme_p, encoding="utf-8").read()
                       if os.path.exists(path_readme_p) else "")
        for name, _t in pth.modules:
            if mod_readme and name not in mod_readme:
                problems.append("%s: not linked from modules/README.md" % name)
            if path_readme and name not in path_readme:
                problems.append("%s: not linked from the path README" % name)

    # two paths must not produce the same output page
    seen = {}
    for pth in PATHS:
        for name, _t in pth.labs + pth.modules:
            out = pth.html_for(name)
            if out in seen:
                problems.append("output collision: %s and %s both -> %s"
                                % (seen[out], pth.name + "/" + name, out))
            seen[out] = pth.name + "/" + name

    labs = sum(len(pth.labs) for pth in PATHS)
    mods = sum(len(pth.modules) for pth in PATHS)
    svgs = sum(len(glob.glob(os.path.join(d, "*.svg"))) for d in FIGURE_DIRS
               if os.path.isdir(d))
    sqls = sum(len(glob.glob(os.path.join(pth.labs_dir, "sql", "*", "*.sql")))
               for pth in PATHS)

    # Nothing hand-written should live outside tools/. One-off migration and
    # patch scripts belong in a scratch directory, not the repository.
    for f in sorted(glob.glob(os.path.join(ROOT, "*.py"))):
        problems.append("stray script at the repo root: %s"
                        % os.path.basename(f))
    for pth in PATHS:
        for f in sorted(glob.glob(os.path.join(pth.dir, "**", "*.py"), recursive=True)):
            problems.append("python outside tools/: %s" % os.path.relpath(f, ROOT))

    # A figure nothing embeds is dead weight: wire it in, or delete the
    # generator that emits it.
    md_files = [f for pth in PATHS
                for f in glob.glob(os.path.join(pth.dir, "**", "*.md"), recursive=True)]
    embedded = set()
    for f in md_files:
        body = io.open(f, encoding="utf-8").read()
        base = os.path.dirname(f)
        for m in re.finditer(r"[(\"]([^()\"\s]+\.svg)[)\"]", body):
            embedded.add(os.path.normpath(os.path.join(base, m.group(1))))
    for d in FIGURE_DIRS:
        for svg in sorted(glob.glob(os.path.join(d, "*.svg"))):
            if os.path.normpath(svg) not in embedded:
                problems.append("figure embedded nowhere: %s"
                                % os.path.relpath(svg, ROOT))

    # Source material must not be identifiable in the prose. This has leaked
    # twice via plurals and compounds, hence the deliberately loose pattern.
    LEAK = re.compile(r"\bexams?\b|\bquiz\w*\b|certification|multiple.choice"
                      r"|\bdistractors?\b|lose marks"
                      r"|a question (may|might|will|could) ask"
                      r"|the (question|answer) (says|asks|is asking)", re.I)
    for f in sorted(md_files):
        text = io.open(f, encoding="utf-8").read()
        for i, line in enumerate(text.splitlines(), 1):
            if LEAK.search(line):
                problems.append("source-material language in %s:%d"
                                % (os.path.relpath(f, ROOT), i))

    # Cross-file links and heading anchors. Relative depth is easy to get wrong
    # between a path root and its modules/ subdirectory, and a stale anchor is
    # invisible until someone clicks it. Both have shipped broken before.
    def _slug(heading):
        t = re.sub(r"^#{1,6}\s+", "", heading).strip()
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)      # link text only
        t = re.sub(r"[`*_]", "", t).lower()
        t = re.sub(r"[^a-z0-9\s-]", "", t)
        return re.sub(r"\s+", "-", t).strip("-")

    anchors = {}
    for f in md_files:
        found, fenced = set(), False
        for line in io.open(f, encoding="utf-8").read().splitlines():
            if line.lstrip().startswith("```"):
                fenced = not fenced
            elif not fenced and re.match(r"^#{1,6}\s", line):
                found.add(_slug(line))
        anchors[os.path.normpath(f)] = found

    for f in sorted(md_files):
        here = os.path.relpath(f, ROOT).replace("\\", "/")
        text = io.open(f, encoding="utf-8").read()
        for rel, anc in re.findall(
                r"\]\((?!https?:|mailto:)([^)\s#]*)(?:#([a-z0-9-]+))?\)", text):
            target = os.path.normpath(
                os.path.join(os.path.dirname(f), rel)) if rel else os.path.normpath(f)
            if rel and not os.path.exists(target):
                problems.append("broken link in %s -> %s" % (here, rel))
            elif anc and target in anchors and anc not in anchors[target]:
                problems.append("broken anchor in %s -> %s#%s" % (here, rel or "", anc))

    if problems:
        print("   %d PROBLEM(S):" % len(problems))
        for pr in problems:
            print("      - %s" % pr)
    else:
        print("   %d paths, %d labs, %d modules, %d figures, %d sql -- all indexed"
              % (len(PATHS), labs, mods, svgs, sqls))
    return problems


def main():
    print("paths: %s" % ", ".join(pth.name for pth in PATHS))
    print("\n1. figures")
    for gen in GENERATORS:
        subprocess.run([sys.executable, gen], check=True, stdout=subprocess.DEVNULL)
    print("   %d generators ran" % len(GENERATORS))

    dirs = [d for d in FIGURE_DIRS if os.path.isdir(d)]
    rc = subprocess.run([sys.executable, CHECKER] + dirs, stdout=subprocess.DEVNULL)
    n = sum(len(glob.glob(os.path.join(d, "*.svg"))) for d in dirs)
    print("   %d svg validated%s" % (n, "" if rc.returncode == 0 else "  -- FAILURES:"))
    if rc.returncode:
        subprocess.run([sys.executable, CHECKER] + dirs)
        return 1

    print("\n2. sql extraction")
    for pth in PATHS:
        for name, title in pth.labs:
            sub = pth.sql_subdir(name)
            if not sub:
                continue
            files = extract_sql(
                io.open(os.path.join(pth.labs_dir, name), encoding="utf-8").read(),
                os.path.join(pth.labs_dir, "sql", sub), title)
            if files:
                print("   %s/labs/sql/%s/  %d files" % (pth.name, sub, len(files)))

    print("\n3. html -> site/")
    os.makedirs(SITE, exist_ok=True)
    for old in glob.glob(os.path.join(SITE, "*.html")):
        os.remove(old)

    n = 0
    for pth in PATHS:
        PAGE_PATH[0] = pth
        for directory, docs in ((pth.labs_dir, pth.labs), (pth.modules_dir, pth.modules)):
            for name, title in docs:
                io.open(os.path.join(SITE, pth.html_for(name)), "w", encoding="utf-8",
                        newline="\n").write(render(os.path.join(directory, name), title))
                n += 1
        for src, out, title in pth.indexes:
            io.open(os.path.join(SITE, out), "w", encoding="utf-8",
                    newline="\n").write(render(src, title))
            n += 1
    PAGE_PATH[0] = None
    for src, out, title in INDEXES:
        if os.path.exists(src) and not any(src == i[0] for pth in PATHS
                                           for i in pth.indexes):
            io.open(os.path.join(SITE, out), "w", encoding="utf-8",
                    newline="\n").write(render(src, title))
            n += 1
    print("   %d pages" % n)

    print("\n4. consistency audit")
    if audit():
        return 1

    print("\nbuild complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
