import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

OUT = c.lab_figures()
W = 940

KW, STR, FN = "#1967d2", "#0d652d", "#8430ce"
PL, NUM, ID_ = c.TEXT, "#b06000", "#137333"
JK, JS, JN = "#8430ce", "#0d652d", "#b06000"


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


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    return [c.line(x1, y1, hx, hy, col, sw),
            c.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
                x2, y2,
                x2 - 9 * math.cos(ang - 0.42), y2 - 9 * math.sin(ang - 0.42),
                x2 - 9 * math.cos(ang + 0.42), y2 - 9 * math.sin(ang + 0.42)), fill=col)]


def poster(x, y, w, h, label, col=c.BLUE):
    """A tiny stylised poster thumbnail."""
    out = [c.rect(x, y, w, h, fill=col, rx=4, op=0.10),
           c.rect(x, y, w, h, fill="none", stroke=col, rx=4, sw=1.2, op=0.55),
           c.circle(x + w / 2, y + h * 0.36, w * 0.17, fill=col, op=0.35),
           c.path("M %s %s L %s %s L %s %s L %s %s Z" % (
               x + w * 0.14, y + h * 0.82, x + w * 0.38, y + h * 0.55,
               x + w * 0.62, y + h * 0.82, x + w * 0.14, y + h * 0.82), fill=col, op=0.30),
           c.path("M %s %s L %s %s L %s %s Z" % (
               x + w * 0.52, y + h * 0.82, x + w * 0.74, y + h * 0.62,
               x + w * 0.92, y + h * 0.82), fill=col, op=0.22)]
    if label:
        out.append(c.t(x + w / 2, y + h + 13, label, 8.5, c.GREY, "400", "middle"))
    return out


def fig_00():
    w, h = 940, 400
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Lab 4 architecture — images in Cloud Storage, everything else in SQL",
                    14.5, c.TEXT, "500"))

    # source
    for i in range(3):
        body += poster(30 + i * 22, 92 + i * 8, 52, 68, None, c.GREY)
    body.append(c.t(64, 200, "Cloud Storage", 11, c.TEXT, "500", "middle"))
    body.append(c.t(64, 216, "a few dozen .jpg", 9.5, c.GREY, "400", "middle"))

    body += node(160, 118, 152, 62, "Object table", "one row per file,\nref column", col=c.BLUE)
    # replace the two-line sub rendered above with explicit lines
    body = body[:-1]
    body.append(c.t(236, 152, "one row per file", 9.5, c.GREY, "400", "middle"))
    body.append(c.t(236, 165, "+ a ref column", 9.5, c.GREY, "400", "middle"))

    body += arrow(120, 149, 160, 149)

    tiers = [
        (60, "ML.ANNOTATE_IMAGE", "Vision API · fixed labels", c.TEAL),
        (140, "AI.GENERATE", "Gemini · your own schema", c.PURPLE),
        (220, "AI.EMBED", "vectors · similarity", c.AMBER),
    ]
    for y0, name, sub, col in tiers:
        body += node(370, y0, 214, 58, name, sub, col=col, fill="#ffffff")
        body.append(c.path("M 312 149 C 340 149 342 %s 370 %s" % (y0 + 29, y0 + 29),
                           stroke=col, sw=1.6))

    body += node(636, 88, 132, 58, "labels", "generic", col=c.TEAL)
    body += node(636, 168, 132, 58, "typed columns", "title, year, genre", col=c.PURPLE)
    body += node(636, 248, 132, 58, "VECTOR_SEARCH", "find similar", col=c.AMBER)
    for y0, y1, col in ((89, 117, c.TEAL), (169, 197, c.PURPLE), (249, 277, c.AMBER)):
        body += arrow(584, y0, 636, y1, col=col)

    body += node(806, 138, 108, 58, "One table", "join, filter,\nchart", col=c.GREEN)
    body = body[:-1]
    body.append(c.t(860, 172, "join, filter, chart", 9.5, c.GREY, "400", "middle"))
    for y0 in (117, 197, 277):
        body.append(c.path("M 768 %s C 790 %s 788 167 806 167" % (y0, y0),
                           stroke=c.GREEN, sw=1.4, op=0.75))

    co, _ = c.callout(24, 322, w - 48, [
        "Nothing is downloaded and nothing is trained. The images stay in Cloud Storage; the object",
        "table is a pointer with metadata, and all three inference paths are function calls in SQL.",
    ], "ok")
    body += co
    write("l4-00-architecture.svg", w, h, body, "Lab 4 architecture: image analysis in BigQuery")


def fig_01():
    h = 520
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    sql = [
        (0, [("CREATE OR REPLACE EXTERNAL TABLE", KW), (" `vision_lab.posters`", ID_)]),
        (0, [("  WITH CONNECTION DEFAULT", KW)]),
        (0, [("  OPTIONS", KW), (" (", PL)]),
        (0, [("    object_metadata = ", PL), ("'SIMPLE'", STR), (",", PL)]),
        (0, [("    uris = [", PL),
             ("'gs://cloud-samples-data/vertex-ai/.../classic-movie-posters/*'", STR), ("]);", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 18, pw, sql)
    body += blk

    ry = y + 18 + bh + 20
    body.append(c.t(px, ry, "posters", 14, c.TEXT, "500"))
    ch, cw = c.chip(px + 74, ry - 12, "External · object table", fill="#e8f0fe", fg=c.BLUE)
    body += ch
    body += c.grid(px, ry + 14, ["uri", "content_type", "size", "updated", "ref"], [
        ["…/barque_sortant_du_port.jpeg", "image/jpeg", "48,213", "2024-03-11 09:42", "OBJECTREF"],
        ["…/the_great_train_robbery.jpg", "image/jpeg", "61,904", "2024-03-11 09:42", "OBJECTREF"],
        ["…/little_annie_rooney.jpg", "image/jpeg", "55,120", "2024-03-11 09:42", "OBJECTREF"],
        ["…/brown_of_harvard.jpeg", "image/jpeg", "44,875", "2024-03-11 09:42", "OBJECTREF"],
    ], [300, 120, 90, 180, 206], mono_cols=(0, 2), align={2: "end"},
        colors={(i, 4): c.PURPLE for i in range(4)})

    co, _ = c.callout(px, ry + 152, pw, [
        "The images are not copied into BigQuery. An object table is metadata plus a signed-access",
        "handle: uri, size, content_type, and ref — the ObjectRef you hand to the AI functions.",
        "Storage cost stays in Cloud Storage; BigQuery stores essentially nothing.",
    ], "info")
    body += co
    write("l4-01-object-table.svg", W, h, body, "An object table over images in Cloud Storage")


def fig_02():
    h = 560
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 26, "Tier 1 — pretrained Vision API, no prompt and no training",
                    13, c.TEXT, "500"))

    js = [
        (0, [('{ "label_annotations"', JK), (": [", PL)]),
        (0, [('    { "description"', JK), (": ", PL), ('"Poster"', JS), (', "score"', JK),
             (": ", PL), ("0.9541", JN), (", ", PL), ('"topicality"', JK), (": ", PL), ("0.9541", JN), (" },", PL)]),
        (0, [('    { "description"', JK), (": ", PL), ('"Vintage advertisement"', JS), (', "score"', JK),
             (": ", PL), ("0.9218", JN), (" },", PL)]),
        (0, [('    { "description"', JK), (": ", PL), ('"Illustration"', JS), (', "score"', JK),
             (": ", PL), ("0.8907", JN), (" } ] }", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 40, pw, js, title="ml_annotate_image_result  (JSON)")
    body += blk

    ry = y + 40 + bh + 22
    body.append(c.t(px, ry, "…flattened into columns", 12, c.TEXT, "500"))
    body += c.grid(px, ry + 14, ["uri", "label", "score"], [
        ["barque_sortant_du_port", "Poster", "0.954"],
        ["barque_sortant_du_port", "Vintage advertisement", "0.922"],
        ["the_great_train_robbery", "Poster", "0.961"],
        ["the_great_train_robbery", "Human", "0.887"],
        ["little_annie_rooney", "Poster", "0.949"],
    ], [330, 340, 226], mono_cols=(2,), align={2: "end"})

    co, _ = c.callout(px, ry + 190, pw, [
        "Useful, and also the limitation you need to feel: every poster returns “Poster”. The Vision",
        "API answers from a fixed general vocabulary, so it cannot tell you the film title, the year,",
        "or the genre — it was never trained on your question. That is what Tier 2 is for.",
    ], "warn")
    body += co
    write("l4-02-annotate.svg", W, h, body, "ML.ANNOTATE_IMAGE label detection output")


def fig_03():
    h = 560
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 26, "Tier 2 — a foundation model answering your question, not a fixed one",
                    13, c.TEXT, "500"))
    sql = [
        (0, [("SELECT", KW), (" REGEXP_EXTRACT(uri, ", FN), ("r'([^/]+)$'", STR), (") ", PL),
             ("AS", KW), (" file,", PL)]),
        (0, [("  ", PL), ("AI.GENERATE", FN), ("(", PL)]),
        (0, [("    (", PL), ("'Identify this classic film poster. '", STR), (", ref),", PL)]),
        (0, [("    endpoint => ", PL), ("'gemini-2.5-flash'", STR), (",", PL)]),
        (0, [("    output_schema => ", PL),
             ("'title STRING, year INT64, genre STRING, dominant_colours ARRAY<STRING>'", STR)]),
        (0, [("  ).* ", PL), ("EXCEPT", KW), (" (full_response, status)", PL)]),
        (0, [("FROM", KW), (" `vision_lab.posters`", ID_), (";", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 40, pw, sql)
    body += blk

    ry = y + 40 + bh + 20
    body += c.grid(px, ry, ["file", "title", "year", "genre", "dominant_colours"], [
        ["the_great_train_robbery.jpg", "The Great Train Robbery", "1903", "Western", "sepia, black"],
        ["little_annie_rooney.jpg", "Little Annie Rooney", "1925", "Comedy drama", "red, cream"],
        ["brown_of_harvard.jpeg", "Brown of Harvard", "1926", "Drama", "blue, white"],
        ["barque_sortant_du_port.jpeg", "Barque sortant du port", "1895", "Documentary", "grey, sepia"],
    ], [252, 250, 70, 150, 174], mono_cols=(0, 2), align={2: "end"},
        colors={(i, 1): c.GREEN for i in range(4)})

    co, _ = c.callout(px, ry + 148, pw, [
        "Same images, same table, no training — but now the output columns are the ones you declared.",
        "Coming from Python this is the zero-shot VLM pattern: you replaced a labelled dataset and a",
        "training loop with a prompt and a schema. What you gave up is a measurable training curve.",
    ], "ok")
    body += co
    write("l4-03-gemini-attributes.svg", W, h, body,
          "AI.GENERATE extracting typed attributes from images")


def fig_04():
    h = 500
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 26, "Tier 3 — embeddings: no labels at all, just geometry",
                    13, c.TEXT, "500"))

    body.append(c.t(px, y + 52, "Query image", 10.5, c.GREY, "600"))
    body += poster(px, y + 62, 74, 96, "the_great_train_robbery", c.BLUE)

    body += arrow(px + 96, y + 110, px + 138, y + 110)
    body.append(c.t(px + 117, y + 100, "AI.EMBED", 9, c.GREY, "500", "middle"))

    body.append(c.t(px + 158, y + 52, "Nearest neighbours by cosine distance", 10.5, c.GREY, "600"))
    neigh = [("little_annie_rooney", 0.184, c.GREEN), ("brown_of_harvard", 0.207, c.GREEN),
             ("mighty_like_a_mouse", 0.243, c.AMBER), ("barque_sortant_du_port", 0.398, c.RED)]
    for i, (name, d, col) in enumerate(neigh):
        x = px + 158 + i * 186
        body += poster(x, y + 62, 74, 96, None, col)
        body.append(c.t(x + 37, y + 174, name[:19], 9, c.TEXT, "400", "middle"))
        body.append(c.t(x + 37, y + 189, "%.3f" % d, 10, col, "600", "middle"))

    sql = [
        (0, [("SELECT", KW), (" base.uri, distance", PL)]),
        (0, [("FROM", KW), (" VECTOR_SEARCH(", FN)]),
        (0, [("  TABLE", KW), (" `vision_lab.poster_embeddings`", ID_), (", ", PL),
             ("'embedding'", STR), (",", PL)]),
        (0, [("  query_value => ", PL), ("AI.EMBED", FN), ("(", PL), ("OBJ.MAKE_REF", FN),
             ("(", PL), ("'gs://…/the_great_train_robbery.jpg'", STR), ("),", PL)]),
        (0, [("    endpoint => ", PL), ("'multimodalembedding@001'", STR), (").result,", PL)]),
        (0, [("  top_k => ", PL), ("4", NUM), (");", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 206, pw, sql)
    body += blk

    co, _ = c.callout(px, y + 206 + bh + 16, pw, [
        "No classes, no labels, no training. Similarity is just distance in embedding space — the same",
        "thing you would do with CLIP features and a nearest-neighbour index, minus the index.",
    ], "info")
    body += co
    write("l4-04-vector-search.svg", W, h, body, "Multimodal embeddings and vector search over images")


def fig_05():
    w, h = 940, 500
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 36, "Three tiers of computer vision on GCP — and what each replaces",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 58, "Only the third one is 'training a model'. Two of the three need no "
                            "labelled data at all.", 11.5, c.GREY))

    cols = ["", "Pretrained API", "Foundation model", "Custom training"]
    sub = ["", "ML.ANNOTATE_IMAGE", "AI.GENERATE / AI.EMBED", "AutoML or Vertex custom"]
    rows = [
        ["You supply", "nothing", "a prompt + output schema", "labelled images (100s–1000s)"],
        ["Setup", "one remote model", "one function call", "dataset, budget, hours of training"],
        ["Cost, 40 images", "free tier", "a few cents", "node-hours — dollars, minimum"],
        ["Output", "fixed generic vocabulary", "any schema you declare", "exactly your classes"],
        ["Python analogue", "calling a hosted API", "zero-shot CLIP / VLM prompting",
         "fine-tuning a ResNet"],
        ["Reach for it when", "generic labels, OCR,\nfaces are enough",
         "you need custom attributes\nand have no labels",
         "fixed taxonomy, high volume,\naccuracy you must prove"],
    ]
    widths = [136, 218, 254, 288]
    x, y0 = 24, 82
    total = sum(widths)
    body.append(c.rect(x, y0, total, 44, fill=c.PANEL))
    body.append(c.rect(x, y0, total, 44 + 42 * 5 + 52, fill="none", stroke=c.BORDER, rx=4))
    heads = [c.GREY, c.TEAL, c.PURPLE, c.AMBER]
    cx = x
    for i, hc in enumerate(cols):
        body.append(c.t(cx + 12, y0 + 20, hc, 11.5, heads[i], "600"))
        if sub[i]:
            body.append(c.t(cx + 12, y0 + 35, sub[i], 9, c.GREY, "400", "start", c.MONO))
        if i:
            body.append(c.line(cx, y0, cx, y0 + 44 + 42 * 5 + 52, c.BORDER, 1, op=.7))
        cx += widths[i]
    body.append(c.line(x, y0 + 44, x + total, y0 + 44, c.BORDER, 1))

    ry = y0 + 44
    for ri, row in enumerate(rows):
        rh = 52 if ri == len(rows) - 1 else 42
        if ri % 2:
            body.append(c.rect(x, ry, total, rh, fill="#fcfcfd"))
        if ri:
            body.append(c.line(x, ry, x + total, ry, c.BORDER, 1, op=.55))
        cx = x
        for ci, cell in enumerate(row):
            lines = cell.split("\n")
            for li, ln in enumerate(lines):
                oy = rh / 2 + 4 if len(lines) == 1 else 20 + li * 15
                body.append(c.t(cx + 12, ry + oy, ln, 10.5,
                                c.GREY if ci == 0 else c.TEXT, "500" if ci == 0 else "400"))
            cx += widths[ci]
        ry += rh

    co, _ = c.callout(24, ry + 16, total, [
        "This lab builds tiers 1 and 2 and skips tier 3 deliberately: AutoML image training has a",
        "minimum node-hour budget and takes hours, which buys you nothing you cannot already see.",
        "Know what it costs, and reach for it only when a prompt genuinely stops being good enough.",
    ], "warn")
    body += co
    write("l4-05-tiers.svg", w, h, body, "Three tiers of computer vision on Google Cloud")


if __name__ == "__main__":
    print("Generating lab 4 figures into %s" % OUT)
    for fn in (fig_00, fig_01, fig_02, fig_03, fig_04, fig_05):
        fn()
    print("done.")
