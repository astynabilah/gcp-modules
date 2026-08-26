# -*- coding: utf-8 -*-
"""Validates generated SVGs: well-formedness plus a crude overflow check.

Run:  python tools/check_svg.py <dir-or-file> [...]


Text width is estimated at 0.56 em for the UI font and 0.605 em for mono, which
is deliberately generous - it flags anything close to the edge for a manual look.
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
TARGETS = sys.argv[1:]

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def est_width(el):
    txt = "".join(el.itertext())
    size = float(el.get("font-size", 12))
    fam = el.get("font-family", "")
    per = 0.605 if "Mono" in fam or "Consolas" in fam else 0.56
    return len(txt) * size * per


def check(p):
    problems = []
    try:
        root = ET.parse(p).getroot()
    except ET.ParseError as exc:
        return ["XML parse error: %s" % exc]
    W = float(root.get("width"))
    H = float(root.get("height"))

    for el in root.iter():
        tag = el.tag.replace(NS, "")
        if tag == "rect":
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            r = x + float(el.get("width", 0))
            b = y + float(el.get("height", 0))
            if r > W + 0.5 or b > H + 0.5 or x < -0.5 or y < -0.5:
                problems.append("rect out of canvas: x=%.0f y=%.0f -> %.0f x %.0f" % (x, y, r, b))
        elif tag == "text":
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            w = est_width(el)
            anchor = el.get("text-anchor", "start")
            left = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
            right = left + w
            if right > W - 4 or left < 4:
                problems.append("text overflows (%.0f..%.0f of %.0f): %r"
                                % (left, right, W, "".join(el.itertext())[:58]))
            if y > H - 2 or y < 8:
                problems.append("text outside vertically at y=%.0f: %r"
                                % (y, "".join(el.itertext())[:44]))
        elif tag == "line":
            for ax, lim in (("x1", W), ("x2", W), ("y1", H), ("y2", H)):
                v = float(el.get(ax, 0))
                if v > lim + 0.5 or v < -0.5:
                    problems.append("line %s=%.0f exceeds %.0f" % (ax, v, lim))
    return problems


def main():
    if not TARGETS:
        print("usage: python check_svg.py <dir-or-file> [...]")
        return 2
    files = []
    for t in TARGETS:
        files += sorted(glob.glob(os.path.join(t, "*.svg"))) if os.path.isdir(t) else [t]
    bad = 0
    for p in sorted(files):
        probs = check(p)
        name = os.path.basename(p)
        if probs:
            bad += 1
            print("FAIL %s" % name)
            for pr in probs[:12]:
                print("      - %s" % pr)
            if len(probs) > 12:
                print("      ... %d more" % (len(probs) - 12))
        else:
            print("ok   %s" % name)
    print("\n%d file(s) with problems" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
