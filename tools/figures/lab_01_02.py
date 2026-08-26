import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

OUT = c.lab_figures()

KW  = "#1967d2"   # SQL keyword
STR = "#0d652d"   # string literal
FN  = "#8430ce"   # function name
CM  = "#9aa0a6"   # comment
PL  = c.TEXT      # plain
NUM = "#b06000"   # number
ID_ = "#137333"   # identifier / backticked name

W = 940


def write(name, w, h, body, title):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-34s %sx%s" % (name, w, h))


def explorer(x, y, h, tree, w=200):
    """BigQuery Studio Explorer rail."""
    out = [c.rect(x, y, w, h, fill="#ffffff"), c.line(x + w, y, x + w, y + h, c.BORDER, 1),
           c.rect(x + 12, y + 12, w - 24, 26, fill=c.PANEL, rx=13),
           c.circle(x + 27, y + 25, 4.4, stroke=c.GREY, sw=1.4),
           c.line(x + 30.2, y + 28.2, x + 33, y + 31, c.GREY, 1.4),
           c.t(x + 42, y + 29, "Search resources", 10.5, c.GREY)]
    cy = y + 58
    for depth, label, kind in tree:
        ix = x + 14 + depth * 15
        if kind in ("proj", "ds"):
            out.append(c.path("M %s %s l 5 5 l -5 5" % (ix, cy - 9), stroke=c.GREY, sw=1.5)
                       if kind == "ds" else
                       c.path("M %s %s l 5 5 l -5 5" % (ix, cy - 9), stroke=c.GREY, sw=1.5))
        icon_x = ix + 12
        col = {"proj": c.GREY, "ds": "#5f6368", "tbl": c.BLUE,
               "model": c.PURPLE, "conn": c.TEAL}[kind]
        if kind == "model":
            out.append(c.circle(icon_x + 5, cy - 4, 5, stroke=col, sw=1.6))
            out.append(c.circle(icon_x + 5, cy - 4, 1.8, fill=col))
        elif kind == "conn":
            out.append(c.rect(icon_x, cy - 9, 10, 10, stroke=col, sw=1.5, rx=2))
        else:
            out.append(c.rect(icon_x, cy - 9, 10, 10, fill=col, rx=2,
                              op=0.85 if kind == "tbl" else 0.35))
        weight = "500" if kind in ("tbl", "model") else "400"
        out.append(c.t(icon_x + 18, cy, label, 11, c.TEXT, weight))
        cy += 27
    return out


def _node(x, y, w, h, title, sub=None, col=c.BLUE, fill="#ffffff", dashed=False):
    out = [c.rect(x, y, w, h, fill=fill, stroke=col, rx=8, sw=1.6)]
    if dashed:
        out = [c.rect(x, y, w, h, fill=fill, stroke=col, rx=8, sw=1.4)]
        out[0] = out[0].replace("/>", ' stroke-dasharray="5 4"/>')
    ty = y + h / 2 + ((-5) if sub else 4)
    out.append(c.t(x + w / 2, ty, title, 12, c.TEXT, "500", "middle"))
    if sub:
        out.append(c.t(x + w / 2, y + h / 2 + 12, sub, 10, c.GREY, "400", "middle"))
    return out


def _arrow(x1, y, x2, col="#9aa0a6", label=None):
    out = [c.line(x1, y, x2 - 7, y, col, 1.6),
           c.path("M %s %s l -7 -4.5 l 0 9 Z" % (x2, y), fill=col)]
    if label:
        out.append(c.t((x1 + x2) / 2, y - 9, label, 9.5, c.GREY, "500", "middle"))
    return out


def fig_l1_00():
    w, h = 940, 300
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Lab 1 architecture — sentiment scoring without leaving SQL",
                    14, c.TEXT, "500"))

    body.append(c.rect(150, 62, 640, 150, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.2, op=0.9))
    body.append(c.t(166, 82, "BigQuery  (region: US)", 10.5, c.BLUE, "500"))

    body += _node(24, 108, 112, 58, "Kaggle CSV", "23,486 rows", col=c.GREY)
    body += _node(168, 108, 128, 58, "reviews_raw", "uploaded table", col=c.BLUE)
    body += _node(320, 108, 128, 58, "reviews_clean", "22,641 rows", col=c.BLUE)
    body += _node(472, 108, 148, 58, "AI.GENERATE()", "structured output", col=c.PURPLE)
    body += _node(644, 108, 130, 58, "reviews_scored", "materialised", col=c.BLUE)
    body += _node(812, 108, 108, 58, "Looker Studio", "dashboard", col=c.GREEN)

    body += _arrow(136, 137, 168, label="upload")
    body += _arrow(296, 137, 320, label="SQL")
    body += _arrow(448, 137, 472)
    body += _arrow(620, 137, 644, label="CTAS")
    body += _arrow(774, 137, 812)

    body += _node(472, 226, 148, 50, "Gemini 2.5 Flash", "Agent Platform", col=c.PURPLE,
                  fill="#faf5ff")
    body.append(c.line(546, 166, 546, 226, c.PURPLE, 1.5, dash="4 4"))
    body.append(c.t(556, 200, "BigQuery connection + roles/aiplatform.user", 9.5, c.GREY))
    write("l1-00-architecture.svg", w, h, body, "Lab 1 architecture diagram")


def fig_l2_00():
    w, h = 940, 320
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Lab 2 architecture — train, evaluate and serve a churn model in SQL",
                    14, c.TEXT, "500"))

    body.append(c.rect(150, 62, 620, 158, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.2, op=0.9))
    body.append(c.t(166, 82, "BigQuery ML  (region: US)", 10.5, c.BLUE, "500"))

    body += _node(24, 112, 112, 58, "Kaggle CSV", "7,043 rows", col=c.GREY)
    body += _node(168, 112, 126, 58, "customers_raw", "uploaded", col=c.BLUE)
    body += _node(316, 112, 126, 58, "customers_ml", "typed + split", col=c.BLUE)
    body += _node(464, 112, 140, 58, "CREATE MODEL", "boosted trees", col=c.PURPLE)
    body += _node(626, 112, 128, 58, "churn_scores", "ML.PREDICT", col=c.BLUE)
    body += _node(792, 112, 126, 58, "Looker Studio", "watchlist", col=c.GREEN)

    body += _arrow(136, 141, 168, label="upload")
    body += _arrow(294, 141, 316, label="SQL")
    body += _arrow(442, 141, 464)
    body += _arrow(604, 141, 626)
    body += _arrow(754, 141, 792)

    body += _node(370, 244, 178, 50, "ML.EVALUATE", "AUC · confusion matrix", col=c.AMBER,
                  fill="#fffaf0")
    body += _node(566, 244, 188, 50, "ML.GLOBAL_EXPLAIN", "feature attributions", col=c.AMBER,
                  fill="#fffaf0")
    body.append(c.line(500, 170, 460, 244, c.AMBER, 1.5, dash="4 4"))
    body.append(c.line(546, 170, 640, 244, c.AMBER, 1.5, dash="4 4"))
    body += _node(772, 244, 146, 50, "Agent Platform", "model registry", col=c.PURPLE,
                  fill="#faf5ff")
    body.append(c.line(604, 141, 845, 141, c.PURPLE, 1.4, dash="4 4"))
    body.append(c.line(845, 141, 845, 244, c.PURPLE, 1.4, dash="4 4"))
    write("l2-00-architecture.svg", w, h, body, "Lab 2 architecture diagram")


# --------------------------------------------------------------------------
# LAB 1
# --------------------------------------------------------------------------

def fig_l1_01():
    h = 670
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    body += explorer(1, y, h - y - 1, [
        (0, c.PROJECT, "proj"),
        (1, "retail_reviews", "ds"),
    ])
    px, pw = 218, 700
    body.append(c.t(px, y + 30, "Create table", 17, c.TEXT, "500"))
    body.append(c.line(px, y + 46, px + pw, y + 46, c.BORDER, 1))

    body.append(c.t(px, y + 74, "Source", 12, c.GREY, "500"))
    body += c.dropdown(px, y + 88, 330, "Create table from", "Upload")
    body += c.field(px + 350, y + 88, 240, "Select file", "Womens_Clothing_Reviews.csv")
    b, _ = c.button(px + 604, y + 88, "BROWSE", primary=False, h=34)
    body += b
    body += c.dropdown(px, y + 136, 330, "File format", "CSV")

    body.append(c.t(px, y + 202, "Destination", 12, c.GREY, "500"))
    body += c.field(px, y + 216, 330, "Project", c.PROJECT, mono_value=True)
    body += c.dropdown(px + 350, y + 216, 330, "Dataset", "retail_reviews")
    body += c.field(px, y + 264, 330, "Table", "reviews_raw", mono_value=True)
    body += c.dropdown(px + 350, y + 264, 330, "Table type", "Native table")

    body.append(c.t(px, y + 330, "Schema", 12, c.GREY, "500"))
    body += c.checkbox(px, y + 342, "Auto detect  (schema and input parameters)", True)

    body.append(c.t(px, y + 392, "Advanced options", 12, c.GREY, "500"))
    body += c.field(px, y + 406, 200, "Header rows to skip", "1", mono_value=True)
    body += c.dropdown(px + 220, y + 406, 240, "Write preference", "Write if empty")

    b, bw = c.button(px, y + 466, "CREATE TABLE")
    body += b
    b2, _ = c.button(px + bw + 12, y + 466, "Cancel", primary=False)
    body += b2

    co, _ = c.callout(px, y + 512, pw, [
        "Auto detect reads the header row for column names. The Kaggle CSV ships an unnamed",
        "index column, so BigQuery names it string_field_0 - you rename it in Task 3.",
    ], "warn")
    body += co
    write("l1-01-create-table.svg", W, h,
          body, "BigQuery Create table panel uploading the reviews CSV")


def fig_l1_02():
    h = 594
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 32, "External data source", 17, c.TEXT, "500"))
    body.append(c.line(px, y + 48, px + pw, y + 48, c.BORDER, 1))

    body += c.dropdown(px, y + 82, 560, "Connection type",
                       "Agent Platform remote models, remote functions and BigLake")
    body += c.field(px, y + 134, 300, "Connection ID", "gemini-conn", mono_value=True)
    body += c.dropdown(px + 320, y + 134, 240, "Location type", "Multi-region")
    body += c.dropdown(px + 580, y + 134, 140, "Region", "US")
    body += c.field(px, y + 186, 300, "Friendly name (optional)", "Gemini for reviews")
    body += c.field(px + 320, y + 186, 400, "Description (optional)",
                    "Used by AI.GENERATE in lab 1", placeholder=True)

    b, bw = c.button(px, y + 240, "CREATE CONNECTION")
    body += b

    body.append(c.line(px, y + 292, px + pw, y + 292, c.BORDER, 1, dash="4 4"))
    body.append(c.t(px, y + 320, "Connection info  ", 13, c.TEXT, "500"))
    ch, cw = c.chip(px + 118, y + 308, "after creation", fill="#e6f4ea", fg=c.GREEN)
    body += ch
    body += c.grid(px, y + 336, ["Property", "Value"], [
        ["Connection ID", "us.gemini-conn"],
        ["Connection type", "CLOUD_RESOURCE"],
        ["Service account id", "bqcx-481920374658-k2p9@gcp-sa-bigquery-condel.iam.gserviceaccount.com"],
    ], [200, 676], mono_cols=(1,), cell_size=10.5)

    co, _ = c.callout(px, y + 452, pw, [
        "Copy the Service account id - Task 5 grants it the Agent Platform User role.",
    ], "info")
    body += co
    write("l1-02-connection.svg", W, h, body,
          "Creating a CLOUD_RESOURCE connection for Gemini in BigQuery")


def fig_l1_03():
    h = 488
    body, y = c.chrome(W, h, "IAM & Admin", "IAM")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 32, "Grant access to “%s”" % c.PROJECT, 16, c.TEXT, "500"))
    body.append(c.line(px, y + 48, px + pw, y + 48, c.BORDER, 1))

    body.append(c.t(px, y + 78, "Add principals", 12.5, c.TEXT, "500"))
    body.append(c.t(px, y + 96, "Principals are users, groups, domains, or service accounts.",
                    11, c.GREY))
    body += c.rect(px, y + 108, 720, 44, fill="#ffffff", stroke=c.BORDER, rx=4),
    body.append(c.rect(px + 9, y + 102, 76, 12, fill="#ffffff"))
    body.append(c.t(px + 12, y + 110.5, "New principals", 9.5, c.GREY))
    ch, cw = c.chip(px + 12, y + 120, "bqcx-481920374658-k2p9@gcp-sa-bigquery-condel.iam.gserviceaccount.com",
                    fill=c.PANEL, fg=c.TEXT, h=22, size=10)
    body += ch

    body.append(c.t(px, y + 186, "Assign roles", 12.5, c.TEXT, "500"))
    body += c.dropdown(px, y + 204, 400, "Role", "Agent Platform User")
    body.append(c.t(px + 416, y + 226, "roles/aiplatform.user", 11, c.GREY, "400", "start", c.MONO))

    b, bw = c.button(px, y + 262, "SAVE")
    body += b
    b2, _ = c.button(px + bw + 12, y + 262, "Cancel", primary=False)
    body += b2

    co, _ = c.callout(px, y + 314, pw, [
        "Naming note (Aug 2026): this role is listed as “Agent Platform User” since the",
        "Vertex AI → Gemini Enterprise Agent Platform rebrand. The role ID roles/aiplatform.user",
        "is unchanged, so older docs that say “Vertex AI User” refer to the same role.",
    ], "warn")
    body += co
    write("l1-03-iam-grant.svg", W, h, body,
          "Granting Agent Platform User to the BigQuery connection service account")


def fig_l1_04():
    h = 525
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body += c.tabs(px, y + 4, pw, ["Untitled query", "reviews_raw", "reviews_scored"], 0)

    sql = [
        (0, [("SELECT", KW), ("  review_id, rating, department,", PL)]),
        (0, [("  ", PL), ("AI.GENERATE", FN), ("(", PL)]),
        (0, [("    ", PL), ("prompt", PL), (" => (", PL), ("'Classify the sentiment of this review. '", STR), (",", PL)]),
        (0, [("               ", PL), ("'Reply strictly as JSON.'", STR), (", review_text),", PL)]),
        (0, [("    ", PL), ("connection_id", PL), (" => ", PL), ("'us.gemini-conn'", STR), (",", PL)]),
        (0, [("    ", PL), ("endpoint", PL), (" => ", PL), ("'gemini-2.5-flash'", STR), (",", PL)]),
        (0, [("    ", PL), ("output_schema", PL), (" => ", PL), ("'sentiment STRING, confidence FLOAT64, themes ARRAY<STRING>'", STR)]),
        (0, [("  ).* ", PL), ("EXCEPT", KW), (" (full_response, status)", PL)]),
        (0, [("FROM", KW), (" `retail_reviews.reviews_clean`", ID_), (" LIMIT ", KW), ("5", NUM), (";", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 50, pw, sql)
    body += blk

    ry = y + 50 + bh + 14
    body.append(c.t(px, ry, "Query results", 13, c.TEXT, "500"))
    ch, cw = c.chip(px + 104, ry - 12, "Job complete", fill="#e6f4ea", fg=c.GREEN)
    body += ch
    body.append(c.t(px + 104 + cw + 12, ry, "8 sec elapsed  ·  1.4 MB processed  ·  5 rows",
                    11, c.GREY))

    rows = [
        ["1042", "5", "Dresses", "POSITIVE", "0.97", "fit, colour"],
        ["1077", "2", "Tops", "NEGATIVE", "0.93", "sizing, fabric"],
        ["1080", "3", "Bottoms", "NEUTRAL", "0.68", "length, price"],
        ["1095", "5", "Jackets", "POSITIVE", "0.95", "warmth, quality"],
        ["1101", "1", "Tops", "NEGATIVE", "0.99", "sheer, shipping"],
    ]
    sc = {"POSITIVE": c.GREEN, "NEGATIVE": c.RED, "NEUTRAL": c.AMBER}
    colors = {(i, 3): sc[r[3]] for i, r in enumerate(rows)}
    body += c.grid(px, ry + 16, ["review_id", "rating", "department", "sentiment",
                                 "confidence", "themes"],
                   rows, [90, 70, 110, 110, 100, 416],
                   mono_cols=(0, 1, 4), align={1: "end", 4: "end"}, colors=colors)
    write("l1-04-results.svg", W, h, body,
          "AI.GENERATE query results with sentiment, confidence and themes columns")


def fig_l1_05():
    h = 480
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 30, "Validation — model sentiment vs. star rating", 14, c.TEXT, "500"))

    cards = [("Reviews scored", "22,641", c.BLUE),
             ("Agreement with rating", "84.3%", c.GREEN),
             ("Disagreements to review", "3,559", c.AMBER),
             ("3-star (ambiguous) rows", "2,823", c.GREY)]
    cw = (pw - 36) / 4
    for i, (lbl, val, col) in enumerate(cards):
        cx = px + i * (cw + 12)
        body.append(c.rect(cx, y + 46, cw, 78, fill="#ffffff", stroke=c.BORDER, rx=8))
        body.append(c.rect(cx, y + 46, cw, 3.5, fill=col, rx=1.75))
        body.append(c.t(cx + 16, y + 76, lbl, 11, c.GREY))
        body.append(c.t(cx + 16, y + 106, val, 22, c.TEXT, "500"))

    body.append(c.t(px, y + 158, "Confusion matrix — rows: star rating band, columns: model sentiment",
                    12, c.GREY, "500"))
    mrows = [
        ["1–2 stars (negative)", "1,904", "341", "118"],
        ["3 stars (neutral)", "742", "1,286", "795"],
        ["4–5 stars (positive)", "402", "1,161", "15,892"],
    ]
    strong = {(0, 1): c.GREEN, (1, 2): c.GREEN, (2, 3): c.GREEN}
    body += c.grid(px, y + 172, ["", "NEGATIVE", "NEUTRAL", "POSITIVE"], mrows,
                   [230, 180, 180, 180], row_h=30,
                   align={1: "end", 2: "end", 3: "end"}, colors=strong, mono_cols=(1, 2, 3))

    co, _ = c.callout(px, y + 306, pw, [
        "Sample output — your figures will differ by a few tenths of a percent because Gemini is",
        "non-deterministic even at temperature 0. The diagonal should dominate; the 3-star row is",
        "expected to spread, since a middling star rating rarely maps cleanly to one sentiment label.",
    ], "info")
    body += co
    write("l1-05-validation.svg", W, h, body,
          "Agreement between model sentiment and the reviewer star rating")


def fig_l1_06():
    h = 580
    body, y = c.chrome(W, h, "Looker Studio", "Review sentiment — Aug 2026")
    px, pw = 22, W - 44

    # donut
    body.append(c.rect(px, y + 20, 280, 210, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(px + 16, y + 44, "Sentiment mix", 12, c.TEXT, "500"))
    cx, cy, R = px + 96, y + 138, 62
    import math
    segs = [("POSITIVE", 0.74, c.GREEN), ("NEGATIVE", 0.14, c.RED), ("NEUTRAL", 0.12, c.AMBER)]
    a0 = -math.pi / 2
    for lbl, frac, col in segs:
        a1 = a0 + frac * 2 * math.pi
        large = 1 if frac > 0.5 else 0
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        body.append(c.path("M %.2f %.2f A %s %s 0 %s 1 %.2f %.2f" % (x0, y0, R, R, large, x1, y1),
                           stroke=col, sw=26))
        a0 = a1
    for i, (lbl, frac, col) in enumerate(segs):
        ly = y + 96 + i * 26
        body.append(c.rect(px + 176, ly, 11, 11, fill=col, rx=2.5))
        body.append(c.t(px + 194, ly + 10, "%s  %d%%" % (lbl, round(frac * 100)), 11, c.TEXT))

    # bar by department
    body.append(c.rect(px + 292, y + 20, pw - 292, 210, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(px + 308, y + 44, "Negative share by department", 12, c.TEXT, "500"))
    body += c.bars(px + 308, y + 58, pw - 324, 156, [
        ("Trend", 24, c.RED), ("Tops", 16, c.RED), ("Bottoms", 14, c.AMBER),
        ("Dresses", 13, c.AMBER), ("Intimate", 11, c.BLUE), ("Jackets", 10, c.BLUE),
    ], maxv=28, label_w=110, value_fmt="%.0f%%")

    # theme table
    body.append(c.rect(px, y + 244, pw, 226, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(px + 16, y + 268, "Top themes in negative reviews", 12, c.TEXT, "500"))
    body += c.grid(px + 16, y + 282, ["Theme", "Mentions", "Share of negatives", "Avg rating"], [
        ["sizing runs small", "1,884", "61.8%", "2.1"],
        ["fabric feels cheap", "1,203", "39.5%", "2.4"],
        ["sheer / see-through", "846", "27.8%", "2.0"],
        ["colour differs from photo", "731", "24.0%", "2.6"],
        ["poor stitching / seams", "402", "13.2%", "2.8"],
    ], [420, 130, 170, 176], row_h=27, mono_cols=(1, 2, 3),
        align={1: "end", 2: "end", 3: "end"})
    write("l1-06-dashboard.svg", W, h, body,
          "Looker Studio dashboard built on the scored review table")


# --------------------------------------------------------------------------
# LAB 2
# --------------------------------------------------------------------------

def fig_l2_01():
    h = 464
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    body += explorer(1, y, h - y - 1, [
        (0, c.PROJECT, "proj"),
        (1, "telco_churn", "ds"),
        (2, "customers_raw", "tbl"),
    ])
    px = 218
    pw = W - px - 22
    body.append(c.t(px, y + 28, "customers_raw", 16, c.TEXT, "500"))
    ch, cw = c.chip(px + 128, y + 16, "7,043 rows  ·  977 KB", fill=c.PANEL, fg=c.GREY)
    body += ch
    body += c.tabs(px, y + 40, pw, ["SCHEMA", "DETAILS", "PREVIEW", "LINEAGE", "DATA PROFILE"], 2)

    body += c.grid(px, y + 90, ["customerID", "tenure", "Contract", "MonthlyCharges",
                                "TotalCharges", "Churn"], [
        ["7590-VHVEG", "1", "Month-to-month", "29.85", "29.85", "No"],
        ["5575-GNVDE", "34", "One year", "56.95", "1889.5", "No"],
        ["3668-QPYBK", "2", "Month-to-month", "53.85", "108.15", "Yes"],
        ["7795-CFOCW", "45", "One year", "42.30", "1840.75", "No"],
        ["9237-HQITU", "2", "Month-to-month", "70.70", "151.65", "Yes"],
        ["9305-CDSKC", "8", "Month-to-month", "99.65", "820.5", "Yes"],
    ], [130, 80, 150, 130, 120, 90], mono_cols=(0, 1, 3, 4),
        align={1: "end", 3: "end", 4: "end"},
        colors={(2, 5): c.RED, (4, 5): c.RED, (5, 5): c.RED})

    co, _ = c.callout(px, y + 290, 700, [
        "TotalCharges arrives as STRING, not FLOAT64: 11 rows for brand-new customers hold a",
        "single blank space instead of a number. Auto-detect therefore types the whole column as",
        "STRING. Task 3 fixes this with SAFE_CAST — leaving it unfixed silently drops a real feature.",
    ], "warn")
    body += co
    write("l2-01-preview.svg", W, h, body, "Preview of the raw Telco churn table in BigQuery")


def fig_l2_02():
    h = 552
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    body += explorer(1, y, h - y - 1, [
        (0, c.PROJECT, "proj"),
        (1, "telco_churn", "ds"),
        (2, "customers_raw", "tbl"),
        (2, "customers_ml", "tbl"),
        (2, "churn_model", "model"),
    ])
    px = 218
    pw = W - px - 22
    sql = [
        (0, [("CREATE OR REPLACE MODEL", KW), (" `telco_churn.churn_model`", ID_)]),
        (0, [("OPTIONS", KW), (" (", PL)]),
        (0, [("  MODEL_TYPE            = ", PL), ("'BOOSTED_TREE_CLASSIFIER'", STR), (",", PL)]),
        (0, [("  INPUT_LABEL_COLS      = [", PL), ("'churn'", STR), ("],", PL)]),
        (0, [("  AUTO_CLASS_WEIGHTS    = ", PL), ("TRUE", KW), (",", PL)]),
        (0, [("  DATA_SPLIT_METHOD     = ", PL), ("'AUTO_SPLIT'", STR), (",", PL)]),
        (0, [("  ENABLE_GLOBAL_EXPLAIN = ", PL), ("TRUE", KW), (",", PL)]),
        (0, [("  MODEL_REGISTRY        = ", PL), ("'VERTEX_AI'", STR), (")", PL)]),
        (0, [("AS SELECT", KW), (" * ", PL), ("EXCEPT", KW), ("(customer_id) ", PL),
             ("FROM", KW), (" `telco_churn.customers_ml`", ID_), (";", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 16, pw, sql)
    body += blk

    ry = y + 16 + bh + 18
    ch, cw = c.chip(px, ry - 12, "Model created", fill="#e6f4ea", fg=c.GREEN)
    body += ch
    body.append(c.t(px + cw + 12, ry, "1 min 42 sec elapsed  ·  50 iterations  ·  early stop at 31",
                    11, c.GREY))

    body.append(c.t(px, ry + 34, "ML.TRAINING_INFO", 12, c.TEXT, "500"))
    body += c.grid(px, ry + 46, ["iteration", "loss", "eval_loss", "duration_ms", "learning_rate"], [
        ["0", "0.6412", "0.6455", "2,118", "0.30"],
        ["10", "0.4187", "0.4361", "1,904", "0.30"],
        ["20", "0.3902", "0.4188", "1,877", "0.30"],
        ["30", "0.3761", "0.4172", "1,860", "0.30"],
        ["31", "0.3754", "0.4174", "1,851", "0.30"],
    ], [110, 130, 130, 140, 190], mono_cols=(0, 1, 2, 3, 4),
        align={0: "end", 1: "end", 2: "end", 3: "end", 4: "end"},
        colors={(4, 2): c.AMBER})
    body.append(c.t(px, ry + 226, "eval_loss stops improving at iteration 31 — EARLY_STOP halts training there.",
                    11, c.GREY))
    write("l2-02-training.svg", W, h, body,
          "CREATE MODEL statement and ML.TRAINING_INFO output for the churn model")


def fig_l2_03():
    h = 624
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 28, "churn_model", 16, c.TEXT, "500"))
    ch, cw = c.chip(px + 100, y + 16, "BOOSTED_TREE_CLASSIFIER", fill="#f3e8fd", fg=c.PURPLE)
    body += ch
    body += c.tabs(px, y + 40, pw, ["DETAILS", "TRAINING", "EVALUATION", "SCHEMA"], 2)

    cards = [("Threshold", "0.50", c.GREY), ("ROC AUC", "0.847", c.GREEN),
             ("Accuracy", "0.830", c.BLUE), ("Precision", "0.663", c.BLUE),
             ("Recall", "0.727", c.BLUE), ("F1 score", "0.693", c.BLUE),
             ("Log loss", "0.417", c.GREY)]
    cwid = (pw - 6 * 10) / 7
    for i, (lbl, val, col) in enumerate(cards):
        cx = px + i * (cwid + 10)
        body.append(c.rect(cx, y + 92, cwid, 66, fill="#ffffff", stroke=c.BORDER, rx=8))
        body.append(c.t(cx + cwid / 2, y + 116, lbl, 10.5, c.GREY, "400", "middle"))
        body.append(c.t(cx + cwid / 2, y + 142, val, 18, col, "500", "middle"))

    # ROC curve
    gx, gy, gw, gh = px, y + 186, 420, 250
    body.append(c.rect(gx, gy, gw, gh, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(gx + 16, gy + 26, "ROC curve", 12, c.TEXT, "500"))
    ax, ay, aw, ah = gx + 58, gy + 46, gw - 90, gh - 96
    for i in range(5):
        yy = ay + ah * i / 4
        body.append(c.line(ax, yy, ax + aw, yy, c.BORDER, 1, op=0.7))
        body.append(c.t(ax - 10, yy + 4, "%.2f" % (1 - i / 4), 9.5, c.GREY, "400", "end"))
    body.append(c.line(ax, ay + ah, ax + aw, ay, c.GREY, 1.2, dash="4 4", op=0.8))
    pts = [(0, 0), (.04, .28), (.09, .45), (.16, .60), (.25, .71), (.36, .80),
           (.50, .87), (.66, .93), (.82, .97), (1, 1)]
    d = "M " + " L ".join("%.1f %.1f" % (ax + aw * a, ay + ah * (1 - b)) for a, b in pts)
    body.append(c.path(d, stroke=c.BLUE, sw=2.4))
    body.append(c.path(d + " L %.1f %.1f L %.1f %.1f Z" % (ax + aw, ay + ah, ax, ay + ah),
                       fill=c.BLUE, op=0.10))
    body.append(c.t(ax + aw / 2, gy + gh - 16, "False positive rate", 10.5, c.GREY, "400", "middle"))
    body.append(c.t(ax + aw - 8, ay + 22, "AUC = 0.847", 11, c.BLUE, "500", "end"))

    # confusion matrix
    mx = px + 436
    mwid = pw - 436
    body.append(c.rect(mx, gy, mwid, gh, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(mx + 16, gy + 26, "Confusion matrix  (threshold 0.50)", 12, c.TEXT, "500"))
    cells = [("True negative", "897", c.GREEN, 0, 0), ("False positive", "138", c.AMBER, 1, 0),
             ("False negative", "102", c.RED, 0, 1), ("True positive", "272", c.GREEN, 1, 1)]
    bx, by, bw2, bh2 = mx + 96, gy + 62, (mwid - 130) / 2, 76
    body.append(c.t(bx + bw2 / 2, gy + 54, "Predicted: No", 10, c.GREY, "500", "middle"))
    body.append(c.t(bx + bw2 * 1.5 + 10, gy + 54, "Predicted: Yes", 10, c.GREY, "500", "middle"))
    body.append(c.t(mx + 88, by + bh2 / 2 + 4, "Actual: No", 10, c.GREY, "500", "end"))
    body.append(c.t(mx + 88, by + bh2 * 1.5 + 14, "Actual: Yes", 10, c.GREY, "500", "end"))
    for lbl, val, col, cc, rr in cells:
        cx = bx + cc * (bw2 + 10)
        cy2 = by + rr * (bh2 + 10)
        body.append(c.rect(cx, cy2, bw2, bh2, fill=col, rx=6, op=0.12))
        body.append(c.t(cx + bw2 / 2, cy2 + 34, val, 19, col, "500", "middle"))
        body.append(c.t(cx + bw2 / 2, cy2 + 56, lbl, 10, c.GREY, "400", "middle"))

    co, _ = c.callout(px, y + 450, pw, [
        "Sample output on the 1,409-row eval split. AUTO_CLASS_WEIGHTS = TRUE is why recall (0.727)",
        "stays close to precision (0.663) on a dataset that is only 26.5% churners. Without it the model",
        "scores similar accuracy while missing most churners — which is why you read recall, not accuracy.",
    ], "info")
    body += co
    write("l2-03-evaluation.svg", W, h, body,
          "Model evaluation tab: metrics, ROC curve and confusion matrix")


def fig_l2_04():
    h = 510
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 28, "ML.GLOBAL_EXPLAIN  —  which features drive churn", 14, c.TEXT, "500"))
    body.append(c.t(px, y + 48, "Mean absolute attribution across the evaluation set (higher = more influence).",
                    11, c.GREY))
    body += c.bars(px, y + 66, pw, 250, [
        ("contract", 0.412, c.BLUE),
        ("tenure_months", 0.288, c.BLUE),
        ("internet_service", 0.191, c.BLUE),
        ("total_charges", 0.147, c.TEAL),
        ("payment_method", 0.121, c.TEAL),
        ("monthly_charges", 0.098, c.TEAL),
        ("tech_support", 0.076, c.GREY),
        ("online_security", 0.064, c.GREY),
    ], maxv=0.44, label_w=190)

    co, _ = c.callout(px, y + 336, pw, [
        "Read this as a retention brief, not just a model diagnostic: contract type dominates, and it is",
        "one of the few features the business can actually change. That is the argument for the",
        "month-to-month → annual upgrade offer you cost out in Task 8.",
    ], "ok")
    body += co
    write("l2-04-global-explain.svg", W, h, body,
          "Global feature attributions from ML.GLOBAL_EXPLAIN")


def fig_l2_05():
    h = 380
    body, y = c.chrome(W, h, "Agent Platform", "formerly Vertex AI")
    body += c.nav(1, y, h - y - 1, [
        ("BUILD", "head"), ("Models", "norm"), ("Agents", "norm"),
        ("SCALE", "head"), ("Deployments", "norm"),
        ("GOVERN", "head"), ("Registry", "sel"), ("Monitoring", "norm"),
    ], w=186)
    px = 208
    pw = W - px - 22
    body.append(c.t(px, y + 30, "Registry", 16, c.TEXT, "500"))
    body.append(c.t(px, y + 50, "Models registered from BigQuery ML appear here automatically when the "
                                "CREATE MODEL statement", 11, c.GREY))
    body.append(c.t(px, y + 66, "sets MODEL_REGISTRY = 'VERTEX_AI'.", 11, c.GREY))
    body += c.grid(px, y + 84, ["Name", "Version", "Source", "Region", "Created"], [
        ["churn_model", "1 (default)", "BigQuery ML", "us-central1", "Aug 23, 2026, 10:14"],
        ["churn_model", "2", "BigQuery ML", "us-central1", "Aug 23, 2026, 11:02"],
    ], [180, 100, 120, 120, 190], row_h=30,
        colors={(0, 0): c.BLUE, (1, 0): c.BLUE})

    co, _ = c.callout(px, y + 190, pw, [
        "Console path changed in 2026: Vertex AI was reorganised into the Gemini Enterprise Agent",
        "Platform on 22 Apr 2026 and the old Vertex AI entry left the console navigation on 21 May 2026.",
        "Model Registry now lives under Agent Platform → Govern → Registry. The API surface",
        "(aiplatform.googleapis.com), the IAM role IDs and the BigQuery ML SQL are all unchanged.",
    ], "warn")
    body += co
    write("l2-05-registry.svg", W, h, body,
          "The BigQuery ML churn model registered in the Agent Platform registry")


def fig_l2_06():
    h = 520
    body, y = c.chrome(W, h, "Looker Studio", "Churn watchlist — week of 23 Aug 2026")
    px, pw = 22, W - 44

    cards = [("Customers scored", "7,043", c.BLUE),
             ("High risk (p ≥ 0.60)", "884", c.RED),
             ("Revenue at risk / mo", "$71,240", c.AMBER),
             ("Model ROC AUC", "0.847", c.GREEN)]
    cwid = (pw - 36) / 4
    for i, (lbl, val, col) in enumerate(cards):
        cx = px + i * (cwid + 12)
        body.append(c.rect(cx, y + 20, cwid, 80, fill="#ffffff", stroke=c.BORDER, rx=8))
        body.append(c.rect(cx, y + 20, cwid, 3.5, fill=col, rx=1.75))
        body.append(c.t(cx + 16, y + 50, lbl, 11, c.GREY))
        body.append(c.t(cx + 16, y + 82, val, 21, c.TEXT, "500"))

    # decile chart
    body.append(c.rect(px, y + 116, 452, 214, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(px + 16, y + 140, "Actual churn rate by predicted-risk decile", 12, c.TEXT, "500"))
    vals = [.02, .04, .07, .11, .15, .22, .31, .42, .56, .75]
    bx, by, bw2, bh2 = px + 40, y + 156, 392, 132
    for i, v in enumerate(vals):
        w1 = bw2 / len(vals) - 7
        x1 = bx + i * (bw2 / len(vals))
        col = c.GREEN if v < .15 else (c.AMBER if v < .35 else c.RED)
        body.append(c.rect(x1, by + bh2 - bh2 * v / .8, w1, bh2 * v / .8, fill=col, rx=3))
        body.append(c.t(x1 + w1 / 2, by + bh2 + 14, str(i + 1), 9.5, c.GREY, "400", "middle"))
    body.append(c.line(bx, by + bh2, bx + bw2, by + bh2, c.BORDER, 1))
    body.append(c.t(px + 16 + 200, y + 322, "risk decile (10 = highest predicted risk)",
                    10, c.GREY, "400", "middle"))

    # watchlist table
    body.append(c.rect(px + 464, y + 116, pw - 464, 214, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(px + 480, y + 140, "Top of the retention queue", 12, c.TEXT, "500"))
    body += c.grid(px + 480, y + 154, ["customer_id", "p(churn)", "MRR", "Top driver"], [
        ["9237-HQITU", "0.94", "$70.70", "month-to-month"],
        ["9305-CDSKC", "0.91", "$99.65", "fiber, no support"],
        ["1452-KIOVK", "0.88", "$89.10", "month-to-month"],
        ["6713-OKOMC", "0.85", "$29.75", "tenure < 3 mo"],
        ["7892-POOKP", "0.83", "$104.80", "electronic check"],
    ], [104, 70, 70, 152], row_h=27, mono_cols=(0, 1, 2),
        align={1: "end", 2: "end"},
        colors={(i, 1): c.RED for i in range(5)})

    co, _ = c.callout(px, y + 346, pw, [
        "The decile chart is the plot to put in front of a stakeholder: it says nothing about AUC and",
        "everything about targeting. Decile 10 churns at nearly 40x the rate of decile 1, so a campaign",
        "aimed at the top two deciles reaches most of the churn for a fifth of the contact cost.",
    ], "ok")
    body += co
    write("l2-06-dashboard.svg", W, h, body,
          "Looker Studio churn watchlist built on the prediction table")


if __name__ == "__main__":
    print("Generating lab figures into %s" % OUT)
    for fn in (fig_l1_00, fig_l2_00, fig_l1_01, fig_l1_02, fig_l1_03, fig_l1_04, fig_l1_05, fig_l1_06,
               fig_l2_01, fig_l2_02, fig_l2_03, fig_l2_04, fig_l2_05, fig_l2_06):
        fn()
    print("done.")
