import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("mlmd")

W = 940
KEY, STR, NUM, BOOL, KW = "#8430ce", "#0d652d", "#b06000", "#1967d2", "#1967d2"


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
    import math
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

def fig_struct():
    """The centrepiece: why the filter path is metadata.<field>.number_value."""
    w, h = 940, 620
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Why the path is metadata.<field>.number_value",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Three layers. Each one explains the next.", 11, c.GREY))

    # 1 — what you write
    body.append(c.rect(24, 74, w - 48, 92, fill="#ffffff", stroke=c.BLUE, rx=9, sw=1.5))
    body.append(c.rect(24, 74, 6, 92, fill=c.BLUE, rx=3))
    body.append(c.t(46, 98, "1.  What you write", 11.5, c.BLUE, "600"))
    pairs = [('"accuracy"', ": ", "0.8734", NUM), ('"framework"', ": ", '"xgboost"', STR),
             ('"tuned"', ": ", "true", BOOL), ('"epochs"', ": ", "10", NUM)]
    cx = 46
    body.append(c.mono(cx, 132, "artifact.metadata = {", 11, c.TEXT))
    cx = 46
    for i, (k, sep, v, col) in enumerate(pairs):
        x = 46 + i * 216
        body.append(c.mono(x, 154, k, 11, KEY))
        body.append(c.mono(x + len(k) * 6.62, 154, sep, 11, c.TEXT))
        body.append(c.mono(x + (len(k) + 2) * 6.62, 154, v, 11, col))

    body += arrow(470, 172, 470, 196)
    body.append(c.t(486, 190, "stored by the API as", 9.5, c.GREY, "500"))

    # 2 — how it is stored
    body.append(c.rect(24, 200, w - 48, 176, fill="#faf5ff", stroke=KEY, rx=9, sw=1.5))
    body.append(c.rect(24, 200, 6, 176, fill=KEY, rx=3))
    body.append(c.t(46, 224, "2.  How Vertex stores it — google.protobuf.Struct",
                    11.5, KEY, "600"))
    lines = [
        ("message Struct {", c.TEXT),
        ("    map<string, Value> fields = 1;      // key -> Value", c.GREY),
        ("}", c.TEXT),
        ("", c.TEXT),
        ("message Value {                          // a oneof: exactly one is set", c.GREY),
        ("    oneof kind {", c.TEXT),
        ("        NullValue null_value;   double number_value;   string string_value;", c.TEXT),
        ("        bool bool_value;        Struct struct_value;   ListValue list_value;", c.TEXT),
        ("    }", c.TEXT),
        ("}", c.TEXT),
    ]
    for i, (ln, col) in enumerate(lines):
        body.append(c.mono(46, 248 + i * 13, ln, 10, col))

    body.append(c.rect(636, 244, 278, 60, fill=c.AMBER, rx=7, op=0.14))
    body.append(c.t(775, 266, "There is no int_value.", 11, c.AMBER, "700", "middle"))
    body.append(c.t(775, 284, "number_value is a double —", 10, c.TEXT, "400", "middle"))
    body.append(c.t(775, 297, "epochs 10 comes back as 10.0", 10, c.TEXT, "400", "middle"))

    body += arrow(470, 382, 470, 406)
    body.append(c.t(486, 400, "therefore the filter path is", 9.5, c.GREY, "500"))

    # 3 — how you query it
    body.append(c.rect(24, 410, w - 48, 132, fill="#f2fbf5", stroke=c.GREEN, rx=9, sw=1.5))
    body.append(c.rect(24, 410, 6, 132, fill=c.GREEN, rx=3))
    body.append(c.t(46, 434, "3.  How you query it — metadata.<fieldName>.<typeValue>",
                    11.5, c.GREEN, "600"))
    q = [
        ("metadata.accuracy", ".number_value", " > 0.85", NUM),
        ("metadata.framework", ".string_value", ' = "xgboost"', STR),
        ("metadata.tuned", ".bool_value", " = true", BOOL),
        ("metadata.epochs", ".number_value", " = 10          <- not int_value", NUM),
    ]
    for i, (base, typ, rest, col) in enumerate(q):
        y = 460 + i * 20
        body.append(c.mono(46, y, base, 11, c.TEXT))
        body.append(c.mono(46 + len(base) * 6.62, y, typ, 11, col))
        body.append(c.mono(46 + (len(base) + len(typ)) * 6.62, y, rest, 11, c.GREY))

    co, _ = c.callout(24, 556, w - 48, [
        "The traversal is not a Vertex quirk — it is protobuf's JSON-in-proto representation showing",
        "through the filter grammar. Once you know metadata is a Struct, the path is forced.",
    ], "info")
    body += co
    write("m-01-struct.svg", w, h, body,
          "How protobuf Struct storage produces the number_value filter path")


def fig_datamodel():
    w, h = 940, 470
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The Vertex ML Metadata data model — five resource types",
                    15, c.TEXT, "500"))

    body.append(c.rect(24, 60, w - 48, 250, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.3))
    body.append(c.t(44, 84, "MetadataStore   (one per project + region, named 'default')",
                    10.5, c.BLUE, "600"))

    body.append(c.rect(44, 100, w - 88, 106, fill="#ffffff", stroke=c.PURPLE, rx=9, sw=1.4))
    body.append(c.t(62, 122, "Context   — a queryable grouping: one pipeline run, one experiment",
                    10.5, c.PURPLE, "600"))

    body += node(78, 138, 176, 52, "Execution", "a step that ran", col=c.TEAL)
    body += node(384, 138, 176, 52, "Execution", "a step that ran", col=c.TEAL)

    body += node(238, 236, 176, 52, "Artifact", "dataset / model / metrics", col=c.AMBER)
    body += node(560, 236, 176, 52, "Artifact", "dataset / model / metrics", col=c.AMBER)

    body += arrow(200, 192, 290, 234, col=c.GREY, sw=1.5)
    body.append(c.t(196, 222, "OUTPUT", 8.5, c.GREY, "600"))
    body += arrow(340, 234, 420, 192, col=c.GREY, sw=1.5)
    body.append(c.t(404, 222, "INPUT", 8.5, c.GREY, "600"))
    body += arrow(500, 192, 600, 234, col=c.GREY, sw=1.5)
    body.append(c.t(508, 222, "OUTPUT", 8.5, c.GREY, "600"))

    body.append(c.rect(760, 130, 156, 68, fill=c.GREEN, rx=8, op=0.12))
    body.append(c.t(838, 154, "Event", 11.5, c.GREEN, "700", "middle"))
    body.append(c.t(838, 172, "the arrows themselves —", 9.5, c.TEXT, "400", "middle"))
    body.append(c.t(838, 185, "INPUT or OUTPUT", 9.5, c.TEXT, "400", "middle"))

    body.append(c.t(44, 300, "MetadataSchema — the 'type' of a resource, named in its schema_title "
                             "field (system.Dataset, system.Model, system.Metrics, …)",
                    10, c.GREY))

    co, _ = c.callout(24, 326, w - 48, [
        "Artifacts are nouns, Executions are verbs, Events are the edges between them, and a Context is",
        "the box you draw around one run. Lineage is just walking those edges — which is why the question",
        "'which dataset produced this model?' is answerable at all, and why it survives you leaving the team.",
    ], "ok")
    body += co
    write("m-02-datamodel.svg", w, h, body, "Vertex ML Metadata data model")


def fig_filters():
    w, h = 940, 606
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Filter cheat sheet — the grammar is AIP-160", 15, c.TEXT, "500"))

    rows = [
        ("Attribute", 'display_name = "churn-model"', "name, display_name, uri, state,\nschema_title, create_time, update_time"),
        ("Comparison", 'create_time > "2026-08-01T00:00:00-00:00"', "=  !=  <  >  <=  >=\ntimes are RFC-3339"),
        ("Numeric metadata", "metadata.accuracy.number_value > 0.85", "doubles only — no int_value"),
        ("String metadata", 'metadata.framework.string_value = "xgboost"', "exact match"),
        ("Boolean metadata", "metadata.tuned.bool_value = true", "unquoted true / false"),
        ("Nested metadata", "metadata.cfg.struct_value.lr.number_value = 0.1", "traverse via struct_value\nmax nesting depth 5"),
        ("Special characters", 'metadata."field:1".number_value = 10.0', "quote the field name"),
        ("Context membership", 'in_context("projects/…/contexts/RUN_ID")', "full resource name"),
        ("Combined", 'schema_title = "system.Model" AND\n  metadata.accuracy.number_value >= 0.9', "AND / OR"),
    ]
    y = 62
    for i, (kind, expr, note) in enumerate(rows):
        rh = 50 if "\n" in expr or note.count("\n") else 40
        body.append(c.rect(24, y, w - 48, rh, fill="#fcfcfd" if i % 2 else "#ffffff",
                           stroke=c.BORDER, rx=6))
        body.append(c.t(40, y + (rh / 2 + 4 if "\n" not in kind else 20), kind, 10.5,
                        c.GREY, "600"))
        for j, ln in enumerate(expr.split("\n")):
            body.append(c.mono(180, y + (rh / 2 + 4 if len(expr.split("\n")) == 1
                                         else 20 + j * 15), ln, 10.5, c.BLUE))
        for j, ln in enumerate(note.split("\n")):
            body.append(c.t(614, y + (rh / 2 + 4 if len(note.split("\n")) == 1
                                      else 20 + j * 14), ln, 9.5, c.GREY))
        y += rh + 6

    co, _ = c.callout(24, y + 6, w - 48, [
        "The same grammar works for artifacts, executions and contexts, in the REST API and in the",
        "Python SDK's .list(filter=...). If a filter silently returns nothing, check the type suffix",
        "first — metadata.accuracy = 0.9 without .number_value matches nothing rather than erroring.",
    ], "warn")
    body += co
    write("m-03-filters.svg", w, h, body, "Vertex ML Metadata filter cheat sheet")


if __name__ == "__main__":
    print("Generating ML Metadata figures into %s" % HERE)
    fig_struct()
    fig_datamodel()
    fig_filters()
    print("done.")
