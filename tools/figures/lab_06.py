import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

OUT = c.lab_figures()
W = 940
PY, KW, STR, CM = c.TEXT, "#1967d2", "#0d652d", "#9aa0a6"


def write(name, w, h, body, title):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-34s %sx%s" % (name, w, h))


def node(x, y, w, h, title, sub=None, col=c.BLUE, fill="#ffffff", size=11.5):
    out = [c.rect(x, y, w, h, fill=fill, stroke=col, rx=8, sw=1.5)]
    ty = y + h / 2 + (-5 if sub else 4)
    out.append(c.t(x + w / 2, ty, title, size, c.TEXT, "500", "middle"))
    if sub:
        out.append(c.t(x + w / 2, y + h / 2 + 12, sub, 9.5, c.GREY, "400", "middle"))
    return out


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6, label=None):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    out = [c.line(x1, y1, hx, hy, col, sw),
           c.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
               x2, y2,
               x2 - 9 * math.cos(ang - 0.42), y2 - 9 * math.sin(ang - 0.42),
               x2 - 9 * math.cos(ang + 0.42), y2 - 9 * math.sin(ang + 0.42)), fill=col)]
    if label:
        out.append(c.t((x1 + x2) / 2, min(y1, y2) - 9, label, 9.5, c.GREY, "500", "middle"))
    return out


def fig_00():
    w, h = 940, 430
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The only question that matters: where does the computation happen?",
                    14.5, c.TEXT, "500"))

    # pull down
    body.append(c.rect(24, 62, 436, 250, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.4))
    body.append(c.t(44, 86, "PULL DOWN — move data to the code", 10.5, c.RED, "600"))
    body += node(44, 104, 130, 54, "BigQuery", "1.7M rows", col=c.GREY)
    body += node(300, 104, 140, 54, "Notebook RAM", "12 GB, free tier", col=c.RED)
    body += arrow(174, 131, 300, 131, col=c.RED, label="every row crosses")
    for i, ln in enumerate([
        "df = client.query('SELECT * ...').to_dataframe()",
    ]):
        body.append(c.mono(56, 190 + i * 16, ln, 9.5, c.TEXT))
    for i, ln in enumerate([
        "Works fine until it doesn't. The failure is",
        "abrupt: the kernel dies with no useful error",
        "at whatever size exceeds your RAM.",
    ]):
        body.append(c.t(44, 222 + i * 17, ln, 10.5, c.GREY))
    body.append(c.t(44, 292, "Good for: < ~1M rows, final plotting", 10.5, c.RED, "600"))

    # push down
    body.append(c.rect(480, 62, 436, 250, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.4))
    body.append(c.t(500, 86, "PUSH DOWN — move the code to the data", 10.5, c.GREEN, "600"))
    body += node(500, 104, 130, 54, "BigQuery", "does the work", col=c.GREEN)
    body += node(756, 104, 140, 54, "Notebook RAM", "results only", col=c.GREY)
    body += arrow(630, 131, 756, 131, col=c.GREEN, label="a few KB")
    body.append(c.mono(512, 190, "df = bpd.read_gbq('...'); df.describe()", 9.5, c.TEXT))
    for i, ln in enumerate([
        "bigframes gives you the pandas API but runs",
        "it as SQL. Nothing is downloaded until you",
        "ask for it with .to_pandas().",
    ]):
        body.append(c.t(500, 222 + i * 17, ln, 10.5, c.GREY))
    body.append(c.t(500, 292, "Good for: any size, all aggregation", 10.5, c.GREEN, "600"))

    co, _ = c.callout(24, 334, w - 48, [
        "Coming from pandas, the instinct is to load the table and then explore. In a warehouse that",
        "instinct is backwards: explore with SQL or bigframes, and pull down only the small result you",
        "actually want to plot. The rule of thumb — if the answer fits on a screen, don't move a table.",
    ], "ok")
    body += co
    write("l6-00-pushdown.svg", w, h, body, "Push-down versus pull-down when exploring BigQuery data")


def fig_01():
    w, h = 940, 500
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Six ways to get BigQuery data into a notebook", 14.5, c.TEXT, "500"))
    body.append(c.t(24, 56, "They are not interchangeable — each one is right at a different "
                            "scale.", 11, c.GREY))

    cols = ["Method", "Moves data?", "Good up to", "Use it for"]
    rows = [
        ["%%bigquery magic", "yes", "~100k rows", "quick look, one cell", c.BLUE],
        ["client.query().to_dataframe()", "yes", "~1M rows", "scripted pulls, full control", c.BLUE],
        ["+ BigQuery Storage API", "yes, fast", "~10M rows", "same, 10-30x faster download", c.TEAL],
        ["pandas_gbq / read_gbq", "yes", "~1M rows", "familiar pandas entry point", c.BLUE],
        ["bigframes (BigQuery DataFrames)", "NO — pushes down", "any size", "the default for exploration", c.GREEN],
        ["EXPORT DATA to GCS -> read", "yes, in bulk", "unbounded", "handing data to another system", c.AMBER],
    ]
    widths = [268, 150, 130, 344]
    x, y0 = 24, 82
    total = sum(widths)
    body.append(c.rect(x, y0, total, 32, fill=c.PANEL))
    body.append(c.rect(x, y0, total, 32 + 40 * len(rows), fill="none", stroke=c.BORDER, rx=4))
    cx = x
    for i, hc in enumerate(cols):
        body.append(c.t(cx + 12, y0 + 21, hc, 11, c.GREY, "600"))
        if i:
            body.append(c.line(cx, y0, cx, y0 + 32 + 40 * len(rows), c.BORDER, 1, op=.7))
        cx += widths[i]
    body.append(c.line(x, y0 + 32, x + total, y0 + 32, c.BORDER, 1))
    for ri, row in enumerate(rows):
        ry = y0 + 32 + 40 * ri
        col = row[4]
        if ri % 2:
            body.append(c.rect(x, ry, total, 40, fill="#fcfcfd"))
        if ri:
            body.append(c.line(x, ry, x + total, ry, c.BORDER, 1, op=.55))
        if ri == 4:
            body.append(c.rect(x, ry, total, 40, fill=c.GREEN, op=0.08))
            body.append(c.rect(x, ry, 4, 40, fill=c.GREEN))
        cx = x
        for ci in range(4):
            body.append(c.t(cx + 12, ry + 25, row[ci], 10.5,
                            c.TEXT if ci == 0 else (col if ci == 1 else c.GREY),
                            "600" if ci == 0 else ("600" if ci == 1 else "400"),
                            font=c.MONO if ci == 0 else None))
            cx += widths[ci]

    co, _ = c.callout(24, y0 + 32 + 40 * len(rows) + 20, total, [
        "'Good up to' is about your notebook's RAM, not BigQuery's limits — BigQuery will happily",
        "return more than your kernel can hold. The free Colab runtime has roughly 12 GB, and a",
        "DataFrame typically needs several times the bytes BigQuery reports for the same data.",
    ], "warn")
    body += co
    write("l6-01-import-options.svg", w, h, body, "Six ways to read BigQuery data into a notebook")


def fig_02():
    w, h = 940, 494
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Where to run the notebook — cheapest first", 14.5, c.TEXT, "500"))

    rows = [
        ("Colab (colab.research.google.com)", c.GREEN, "FREE",
         "Free CPU runtime, no GCP billing for the notebook itself.",
         "Idle timeouts, no VPC, not for sensitive data. This lab uses it."),
        ("BigQuery Studio notebooks", c.BLUE, "runtime billed",
         "Notebooks inside the BigQuery console, Colab Enterprise runtime underneath.",
         "Nice when you already live in BigQuery. You pay for the runtime while it runs."),
        ("Colab Enterprise", c.AMBER, "runtime billed",
         "Managed Colab in your project: VPC, IAM, private data.",
         "The compliance answer. Costs per runtime-hour."),
        ("Vertex AI Workbench", c.RED, "VM billed 24/7 if left on",
         "A full managed JupyterLab VM you control.",
         "Most flexible, most expensive. Idle VMs are the classic surprise bill."),
    ]
    y = 62
    for name, col, price, what, caveat in rows:
        body.append(c.rect(24, y, w - 48, 78, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, 78, fill=col, rx=3))
        body.append(c.t(44, y + 26, name, 12, c.TEXT, "600"))
        ch, cw = c.chip(44 + len(name) * 7.1 + 14, y + 13, price, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(44, y + 46, what, 10.5, c.TEXT))
        body.append(c.t(44, y + 65, caveat, 10, c.GREY))
        y += 86

    co, _ = c.callout(24, y + 4, w - 48, [
        "In every case the BigQuery bill is separate and identical: you pay for bytes scanned by your",
        "queries (1 TB/month free), no matter which notebook issued them. Choosing free Colab saves",
        "the compute, not the query cost — which is why the habits in this lab matter more than the venue.",
    ], "info")
    body += co
    write("l6-02-environments.svg", w, h, body, "Notebook environment options ranked by cost")


if __name__ == "__main__":
    print("Generating lab 6 figures into %s" % OUT)
    for fn in (fig_00, fig_01, fig_02):
        fn()
    print("done.")
