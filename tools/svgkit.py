# -*- coding: utf-8 -*-
"""Shared SVG primitives for the Google Cloud console mockups used in the labs."""
import html
import os

# ---------------------------------------------------------------- locations
# Generators live here in tools/figures/; the SVGs they write live next to the
# documents that embed them. These helpers are the only place that mapping is
# encoded, so moving the path folder does not mean editing 20 scripts.

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_TOOLS)


def _path_dirs():
    """Every learning-path folder: any child dir holding both labs/ and modules/."""
    import glob as _glob
    found = []
    for depth in ("*", "*/*"):
        for cand in sorted(_glob.glob(os.path.join(_REPO, depth))):
            if (os.path.isdir(os.path.join(cand, "modules"))
                    and os.path.exists(os.path.join(cand, "README.md"))
                    and cand not in found):
                found.append(cand)
    if not found:
        raise SystemExit("svgkit: no folder containing labs/ and modules/ under %s" % _REPO)
    return found


def _path_dir():
    return _path_dirs()[0]


def lab_figures():
    """Output directory for lab figures.

    Searches every path folder for an existing labs/figures, so a generator
    keeps working no matter how the path folders sort. Only creates one if no
    path has it yet.
    """
    for base in _path_dirs():
        d = os.path.join(base, "labs", "figures")
        if os.path.isdir(d):
            return d
    d = os.path.join(_path_dirs()[0], "labs", "figures")
    os.makedirs(d, exist_ok=True)
    return d


def asset_dir(name):
    """Output directory for one module's figures, e.g. asset_dir("kfp").

    Searches every path folder, so a generator keeps working when its module
    moves between paths. Creates under the first path only if nowhere has it.
    """
    for base in _path_dirs():
        d = os.path.join(base, "modules", "assets", name)
        if os.path.isdir(d):
            return d
    d = os.path.join(_path_dirs()[0], "modules", "assets", name)
    os.makedirs(d, exist_ok=True)
    return d


# ------------------------------------------------------------------ palette
BLUE = "#1a73e8"
GREY = "#5f6368"
TEXT = "#202124"
BORDER = "#dadce0"
GREEN = "#188038"
RED = "#d93025"
AMBER = "#e37400"
PURPLE = "#8430ce"
TEAL = "#12a4af"
CHIP = "#e8f0fe"
PANEL = "#f8f9fa"

FONT = "'Google Sans','Roboto',-apple-system,'Segoe UI',Arial,sans-serif"
MONO = "'Roboto Mono','Cascadia Mono',Consolas,'Courier New',monospace"

PROJECT = "qwiklabs-gcp-04-7c1e9b2a"


# --------------------------------------------------------------- primitives

def esc(s):
    """XML-escape a string, quotes included."""
    return html.escape("%s" % s)


def t(x, y, s, size=12, fill=TEXT, weight="400", anchor="start", font=None, op=1.0):
    """A line of UI text."""
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" '
            'font-weight="%s" text-anchor="%s" opacity="%s">%s</text>'
            % (x, y, font or FONT, size, fill, weight, anchor, op, esc(s)))


def mono(x, y, s, size=11.5, fill=TEXT, weight="400", anchor="start", op=1.0):
    """A line of monospaced text."""
    return t(x, y, s, size, fill, weight, anchor, MONO, op)


def rect(x, y, w, h, fill="none", stroke="none", rx=0, sw=1, op=1.0):
    return ('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" '
            'stroke-width="%s" rx="%s" opacity="%s"/>'
            % (x, y, w, h, fill, stroke, sw, rx, op))


def line(x1, y1, x2, y2, stroke=BORDER, sw=1, dash=None, op=1.0):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s '
            'opacity="%s"/>'
            % (x1, y1, x2, y2, stroke, sw,
               ' stroke-dasharray="%s"' % dash if dash else "", op))


def circle(cx, cy, rr, fill="none", stroke="none", sw=1, op=1.0):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" '
            'stroke-width="%s" opacity="%s"/>' % (cx, cy, rr, fill, stroke, sw, op))


def path(d, fill="none", stroke="none", sw=1, cap="round", op=1.0, dash=None):
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linecap="%s" stroke-linejoin="%s"%s opacity="%s"/>'
            % (d, fill, stroke, sw, cap, cap,
               ' stroke-dasharray="%s"' % dash if dash else "", op))


def svg(w, h, body, title=""):
    """Wrap a body (string or list of strings) in the document element."""
    if not isinstance(body, str):
        body = "".join(body)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" '
            'viewBox="0 0 %s %s" role="img" aria-label="%s">%s'
            '<rect width="%s" height="%s" fill="#ffffff"/>%s</svg>'
            % (w, h, w, h, esc(title),
               "<title>%s</title>" % esc(title) if title else "",
               w, h, body))


# ------------------------------------------------------------------ widgets

def chip(x, y, label, fill=CHIP, fg=BLUE, h=20, pad=9, size=10.5, weight="500"):
    """A pill. Returns (parts, width) so callers can lay out what follows."""
    cw = pad * 2 + len(label) * (size * 0.58)
    return [rect(x, y, cw, h, fill=fill, rx=h / 2),
            t(x + pad, y + h / 2 + 3.6, label, size, fg, weight)], cw


_CALLOUT = {
    "info": ("#e8f0fe", BLUE),
    "ok": ("#e6f4ea", GREEN),
    "warn": ("#fef7e0", AMBER),
}


def callout(x, y, w, text_lines, kind="info"):
    """A tinted note with an accent bar. Returns (parts, height)."""
    tint, accent = _CALLOUT.get(kind, _CALLOUT["info"])
    h = 16 * len(text_lines) + 16
    out = [rect(x, y, w, h, fill=tint, rx=6),
           rect(x, y, 3.5, h, fill=accent, rx=1.75)]
    for i, ln in enumerate(text_lines):
        out.append(t(x + 16, y + 20 + i * 16, ln, 11, TEXT))
    return out, h


def bars(x, y, w, h, items, maxv=None, color=BLUE, label_w=150, value_fmt="%.3f"):
    """Horizontal bar chart. items are (label, value) or (label, value, colour)."""
    mx = maxv if maxv else max(it[1] for it in items)
    step = h / len(items)
    bh = step - 8
    tw = w - label_w - 52
    out = []
    for i, it in enumerate(items):
        col = it[2] if len(it) > 2 else color
        by = y + i * step
        out.append(t(x + label_w - 10, by + bh / 2 + 4, it[0], 11, TEXT, "400", "end"))
        out.append(rect(x + label_w, by, tw, bh, fill=PANEL, rx=3))
        out.append(rect(x + label_w, by, tw * (it[1] / mx), bh, fill=col, rx=3))
        out.append(t(x + label_w + tw + 6, by + bh / 2 + 4, value_fmt % it[1],
                     10.5, GREY, "500"))
    return out


def grid(x, y, headers, rows, widths, row_h=26, head_h=28, head_size=10.5,
         cell_size=11, mono_cols=(), align=None, colors=None):
    """A results table. colors maps (row, col) to a text colour."""
    align = align or {}
    colors = colors or {}
    tw = sum(widths)
    th = head_h + row_h * len(rows)
    out = [rect(x, y, tw, head_h, fill=PANEL),
           rect(x, y, tw, th, stroke=BORDER, rx=3)]
    cx = x
    for i, hd in enumerate(headers):
        a = align.get(i, "start")
        out.append(t(cx + widths[i] - 10 if a == "end" else cx + 10,
                     y + 17.8, hd, head_size, GREY, "500", a))
        if i:
            out.append(line(cx, y, cx, y + th, BORDER, 1, op=0.7))
        cx += widths[i]
    out.append(line(x, y + head_h, x + tw, y + head_h, BORDER, 1))
    for r, row in enumerate(rows):
        ry = y + head_h + r * row_h
        if r % 2:
            out.append(rect(x, ry, tw, row_h, fill="#fcfcfd"))
        cx = x
        for i, cell in enumerate(row):
            a = align.get(i, "start")
            fn = mono if i in mono_cols else t
            out.append(fn(cx + widths[i] - 10 if a == "end" else cx + 10,
                          ry + row_h / 2 + 4, cell, cell_size,
                          colors.get((r, i), TEXT), "400", a))
            cx += widths[i]
        if r:
            out.append(line(x, ry, x + tw, ry, BORDER, 1, op=0.55))
    return out


def sql_block(x, y, w, lines, line_h=17, pad=12, title=None):
    """An editor panel. lines are (indent, [(text, colour), ...]).

    Returns (parts, height) because callers stack things underneath.
    """
    top = 22 if title else 0
    h = pad * 2 + line_h * len(lines) + top
    out = [rect(x, y, w, h, fill="#ffffff", stroke=BORDER, rx=6)]
    if title:
        out.append(t(x + 12, y + 24, title, 10.5, GREY, "500"))
    out.append(rect(x + 1, y + 10 + top, 34, h - 14 - top, fill=PANEL))
    for i, (indent, spans) in enumerate(lines):
        ly = y + 24 + top + i * line_h
        out.append(mono(x + 26, ly, str(i + 1), 9.5, "#9aa0a6", anchor="end"))
        cx = x + 44 + indent * 8
        for txt, col in spans:
            out.append(mono(cx, ly, txt, 11.5, col))
            cx += len(txt) * 6.62
    return out, h


def button(x, y, label, primary=True, h=30):
    """Returns (parts, width) so the next button can be placed after it."""
    bw = len(label) * 7.2 + 28
    return [rect(x, y, bw, h, fill=BLUE if primary else "#ffffff",
                 stroke="none" if primary else BORDER, rx=4),
            t(x + bw / 2, y + h / 2 + 4.2, label, 12,
              "#ffffff" if primary else BLUE, "500", "middle")], bw


def field(x, y, w, label, value, mono_value=False, placeholder=False, h=34):
    """An outlined text field with its label notched into the top border."""
    out = [rect(x, y, w, h, fill="#ffffff", stroke=BORDER, rx=4),
           rect(x + 9, y - 6, len(label) * 5.5 + 6, 12, fill="#ffffff"),
           t(x + 12, y + 2.5, label, 9.5, GREY)]
    fn = mono if mono_value else t
    out.append(fn(x + 12, y + h / 2 + 4, value, 11.5, GREY if placeholder else TEXT))
    return out


def dropdown(x, y, w, label, value, h=34):
    """A field with a chevron."""
    out = field(x, y, w, label, value, h=h)
    out.append(path("M %s %s l 5 6 l 5 -6" % (x + w - 22, y + h / 2 - 2),
                    stroke=GREY, sw=1.6))
    return out


def checkbox(x, y, label, checked=True, size=15):
    """A material checkbox with its label."""
    if checked:
        out = [rect(x, y, size, size, fill=BLUE, rx=2.5),
               path("M %s %s l 3.2 3.3 l 5.0 -5.8" % (x + 3.5, y + 7.6),
                    stroke="#ffffff", sw=1.9)]
    else:
        out = [rect(x, y, size, size, fill="#ffffff", stroke=GREY, sw=1.5, rx=2.5)]
    out.append(t(x + 23, y + 11.5, label, 11.5, TEXT))
    return out


def chrome(w, h, product, section=""):
    """Console frame: top bar, product title, rules. Returns (parts, content_y)."""
    out = [rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=BORDER, rx=10),
           rect(1, 1, w - 2, 47, fill="#ffffff")]
    for i in range(3):
        out.append(line(18, 18 + i * 5.5, 34, 18 + i * 5.5, GREY, 1.8))
    out.append(t(46, 29, "Google Cloud", 14.5, GREY, "500"))
    out.append(rect(160, 12, 224, 25, fill=PANEL, stroke=BORDER, rx=13))
    out.append(t(174, 28.5, PROJECT, 11, TEXT))
    out.append(path("M 370 21 l 4.5 5.5 l 4.5 -5.5", stroke=GREY, sw=1.5))
    out.append(rect(400, 12, 360, 25, fill=PANEL, rx=13))
    out.append(circle(416, 24, 4.6, stroke=GREY, sw=1.5))
    out.append(line(419.4, 27.4, 422.6, 30.6, GREY, 1.5))
    out.append(t(432, 28.5, "Search (/) for resources, docs, products, and more",
                 10.5, GREY))
    out.append(circle(w - 28, 24, 12, fill="#c5221f"))
    out.append(t(w - 28, 28.5, "S", 12, "#ffffff", "500", "middle"))
    out.append(line(1, 48, w - 1, 48, BORDER, 1))
    out.append(t(18, 76, product, 16.5, TEXT, "500"))
    out.append(t(18 + len(product) * 8.6 + 2, 76, section, 12, GREY))
    out.append(line(1, 92, w - 1, 92, BORDER, 1))
    return out, 92


def nav(x, y, h, items, w=186):
    """Left navigation rail. items are (label, "head"|"norm"|"sel")."""
    out = [rect(x, y, w, h, fill="#ffffff"),
           line(x + w, y, x + w, y + h, BORDER, 1)]
    cy = y + 34
    for label, kind in items:
        if kind == "head":
            out.append(t(x + 16, cy - 8, label, 10, GREY, "500"))
            cy += 26
            continue
        sel = kind == "sel"
        if sel:
            out.append(rect(x + 6, cy - 20, w - 18, 30, fill=CHIP, rx=15))
        out.append(t(x + 40, cy, label, 11.5, BLUE if sel else GREY,
                     "500" if sel else "400"))
        out.append(circle(x + 24, cy - 5, 5.5, stroke=BLUE if sel else GREY,
                          sw=1.6 if sel else 1.4, op=1.0 if sel else 0.75))
        cy += 32
    return out


def tabs(x, y, w, labels, active=0):
    """A row of tabs with an underline on the active one."""
    out = [line(x, y + 34, x + w, y + 34, BORDER, 1)]
    cx = x + 4
    for i, lb in enumerate(labels):
        tw = len(lb) * 7.0 + 24
        out.append(t(cx + tw / 2, y + 22, lb, 11.5,
                     BLUE if i == active else GREY, "500", "middle"))
        if i == active:
            out.append(rect(cx, y + 31, tw, 3, fill=BLUE, rx=1.5))
        cx += tw
    return out
