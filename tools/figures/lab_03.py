import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

OUT = c.lab_figures()
W = 940

KW, STR, FN, CM = "#1967d2", "#0d652d", "#8430ce", "#9aa0a6"
PL, NUM, ID_ = c.TEXT, "#b06000", "#137333"
JK, JS, JN = "#8430ce", "#0d652d", "#b06000"   # JSON key / string / number


def write(name, w, h, body, title):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-34s %sx%s" % (name, w, h))


def node(x, y, w, h, title, sub=None, col=c.BLUE, fill="#ffffff"):
    out = [c.rect(x, y, w, h, fill=fill, stroke=col, rx=8, sw=1.6)]
    ty = y + h / 2 + (-5 if sub else 4)
    out.append(c.t(x + w / 2, ty, title, 12, c.TEXT, "500", "middle"))
    if sub:
        out.append(c.t(x + w / 2, y + h / 2 + 12, sub, 10, c.GREY, "400", "middle"))
    return out


def arrow(x1, y, x2, col="#9aa0a6", label=None):
    out = [c.line(x1, y, x2 - 7, y, col, 1.6),
           c.path("M %s %s l -7 -4.5 l 0 9 Z" % (x2, y), fill=col)]
    if label:
        out.append(c.t((x1 + x2) / 2, y - 9, label, 9.5, c.GREY, "500", "middle"))
    return out


def fig_00():
    w, h = 940, 372
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Lab 3 architecture — one trained model, three ways to serve it",
                    14, c.TEXT, "500"))
    body += node(24, 138, 176, 82, "churn_model", "Agent Platform registry",
                 col=c.PURPLE, fill="#faf5ff")

    rows = [
        (74, "BATCH", c.BLUE,
         [("Scheduled query", "nightly, in BigQuery"), ("churn_scores", "partitioned table"),
          ("Looker Studio", "watchlist")]),
        (176, "ONLINE", c.GREEN,
         [("Endpoint", "n1-standard-2"), ("REST / gRPC", "~30 ms"),
          ("Your application", "one customer")]),
        (278, "IN-SQL", c.AMBER,
         [("Remote model", "CREATE MODEL REMOTE"), ("ML.PREDICT", "over the endpoint"),
          ("Any BigQuery query", "joinable")]),
    ]
    for y0, tag, col, boxes in rows:
        ty = y0 + 16
        body.append(c.path("M 200 179 C 208 179 206 %s 214 %s" % (ty, ty), stroke=col, sw=1.7))
        body.append(c.rect(214, y0 + 6, 62, 20, fill=col, rx=10, op=0.16))
        body.append(c.t(245, y0 + 20, tag, 9.5, col, "600", "middle"))
        x = 290
        for i, (title, sub) in enumerate(boxes):
            wbox = 180 if i < 2 else 172
            body += node(x, y0 - 4, wbox, 50, title, sub, col=col)
            if i < len(boxes) - 1:
                body += arrow(x + wbox, y0 + 21, x + wbox + 22, col=col)
            x += wbox + 22
    write("l3-00-architecture.svg", w, h, body,
          "Lab 3 architecture: batch, online and in-SQL serving")


def fig_01():
    h = 560
    body, y = c.chrome(W, h, "BigQuery", "Scheduled queries")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 30, "New scheduled query", 16, c.TEXT, "500"))
    body.append(c.line(px, y + 46, px + pw, y + 46, c.BORDER, 1))

    body += c.field(px, y + 80, 340, "Name", "nightly-churn-scoring")
    body += c.dropdown(px + 360, y + 80, 260, "Repeats", "Days")
    body += c.field(px + 640, y + 80, 254, "At time (UTC)", "03:00")

    body += c.dropdown(px, y + 132, 340, "Schedule options", "Start now, no end date")
    body += c.dropdown(px + 360, y + 132, 260, "Service account", "bq-scheduler@…")
    body += c.dropdown(px + 640, y + 132, 254, "Location", "US")

    body.append(c.t(px, y + 196, "Destination", 12, c.GREY, "500"))
    body += c.checkbox(px, y + 208, "Set a destination table for query results", False)
    body.append(c.t(px + 40, y + 244,
                    "Not needed — the query is a MERGE, so it writes its own target.",
                    10.5, c.GREY))

    body.append(c.t(px, y + 286, "Notifications", 12, c.GREY, "500"))
    body += c.checkbox(px, y + 298, "Send email notifications on failure", True)

    b, bw = c.button(px, y + 346, "SAVE")
    body += b
    b2, _ = c.button(px + bw + 12, y + 346, "Cancel", primary=False)
    body += b2

    co, _ = c.callout(px, y + 396, pw, [
        "A scheduled query is the cheapest production ML service there is: no endpoint, no container,",
        "no autoscaling, nothing running between executions. If your consumers read a table or a",
        "dashboard rather than calling an API, stop here — you do not need an endpoint at all.",
    ], "ok")
    body += co
    write("l3-01-scheduled-query.svg", W, h, body,
          "Configuring a nightly scheduled query for batch scoring")


def fig_02():
    h = 636
    body, y = c.chrome(W, h, "Agent Platform", "formerly Vertex AI")
    body += c.nav(1, y, h - y - 1, [
        ("BUILD", "head"), ("Models", "norm"),
        ("SCALE", "head"), ("Deployments", "sel"),
        ("GOVERN", "head"), ("Registry", "norm"), ("Monitoring", "norm"),
    ], w=186)
    px = 208
    pw = W - px - 22
    body.append(c.t(px, y + 30, "Deploy model to endpoint", 16, c.TEXT, "500"))
    body.append(c.line(px, y + 46, px + pw, y + 46, c.BORDER, 1))

    body.append(c.t(px, y + 74, "Model", 12, c.GREY, "500"))
    body += c.dropdown(px, y + 86, 330, "Model", "telco-churn-logreg")
    body += c.dropdown(px + 350, y + 86, 200, "Version", "1 (default)")

    body.append(c.t(px, y + 152, "Endpoint", 12, c.GREY, "500"))
    body += c.field(px, y + 164, 330, "Endpoint name", "churn-endpoint")
    body += c.dropdown(px + 350, y + 164, 200, "Access", "Standard (public)")

    body.append(c.t(px, y + 230, "Compute", 12, c.GREY, "500"))
    body += c.dropdown(px, y + 242, 220, "Machine type", "n1-standard-2")
    body += c.field(px + 240, y + 242, 130, "Min replicas", "1", mono_value=True)
    body += c.field(px + 390, y + 242, 130, "Max replicas", "3", mono_value=True)

    body.append(c.t(px, y + 308, "Traffic split", 12, c.GREY, "500"))
    body += c.field(px, y + 320, 130, "This model", "100 %", mono_value=True)
    body.append(c.t(px + 150, y + 342,
                    "Set below 100 to canary a new version against the current one.",
                    10.5, c.GREY))

    body += c.checkbox(px, y + 378,
                       "Enable prediction logging to BigQuery  (required for monitoring)", True)

    b, bw = c.button(px, y + 416, "DEPLOY")
    body += b

    co, _ = c.callout(px, y + 462, pw, [
        "Min replicas = 1 means one node runs 24/7 and bills per node-hour whether or not a single",
        "prediction arrives. This is the line item that surprises people. Use min replicas = 0 for a",
        "lab or dev endpoint so it scales to nothing when idle, and undeploy it when you finish.",
    ], "warn")
    body += co
    write("l3-02-deploy.svg", W, h, body, "Deploying the model to an online endpoint")


def fig_03():
    h = 628
    body, y = c.chrome(W, h, "Agent Platform", "Deployments")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 28, "churn-endpoint", 16, c.TEXT, "500"))
    ch, cw = c.chip(px + 128, y + 16, "Active", fill="#e6f4ea", fg=c.GREEN)
    body += ch
    body.append(c.t(px + 128 + cw + 14, y + 28,
                    "us-central1  ·  endpoint id 4820193746152357888", 10.5, c.GREY))
    body += c.tabs(px, y + 40, pw, ["DETAILS", "TEST", "METRICS", "MONITORING"], 1)

    req = [
        (0, [("{", PL)]),
        (0, [('  "instances"', JK), (": [{", PL)]),
        (0, [('    "contract"', JK), (": ", PL), ('"Month-to-month"', JS), (",", PL)]),
        (0, [('    "tenure_months"', JK), (": ", PL), ("2", JN), (",", PL)]),
        (0, [('    "internet_service"', JK), (": ", PL), ('"Fiber optic"', JS), (",", PL)]),
        (0, [('    "monthly_charges"', JK), (": ", PL), ("70.7", JN), (",", PL)]),
        (0, [('    "total_charges"', JK), (": ", PL), ("151.65", JN), (",", PL)]),
        (0, [('    "payment_method"', JK), (": ", PL), ('"Electronic check"', JS), ("}]", PL)]),
        (0, [("}", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 92, 452, req, title="Request  ·  instances.json")
    body += blk

    resp = [
        (0, [("{", PL)]),
        (0, [('  "predictions"', JK), (": [{", PL)]),
        (0, [('    "churn_values"', JK), (": [", PL), ('"Yes"', JS), (", ", PL), ('"No"', JS), ("],", PL)]),
        (0, [('    "churn_probs"', JK), (": [", PL), ("0.9412", JN), (", ", PL), ("0.0588", JN), ("],", PL)]),
        (0, [('    "predicted_churn"', JK), (": [", PL), ('"Yes"', JS), ("]", PL)]),
        (0, [("  }]", PL)]),
        (0, [("}", PL)]),
    ]
    blk2, bh2 = c.sql_block(px + 466, y + 92, pw - 466, resp, title="Response  ·  30 ms")
    body += blk2

    ry = y + 92 + max(bh, bh2) + 24
    body.append(c.t(px, ry, "Recent latency", 12, c.TEXT, "500"))
    body += c.grid(px, ry + 12, ["Metric", "p50", "p95", "p99"], [
        ["Prediction latency", "28 ms", "61 ms", "112 ms"],
        ["Requests per second", "14.2", "—", "—"],
        ["Error rate", "0.0 %", "—", "—"],
    ], [340, 180, 180, 196], mono_cols=(1, 2, 3), align={1: "end", 2: "end", 3: "end"})

    co, _ = c.callout(px, ry + 138, pw, [
        "The response mirrors ML.PREDICT: parallel arrays of class labels and probabilities, so",
        "churn_probs[0] belongs to churn_values[0]. Never assume index 0 is the positive class —",
        "read the label array, exactly as the SQL does with WHERE label = 'Yes'.",
    ], "info")
    body += co
    write("l3-03-endpoint-test.svg", W, h, body, "Testing the deployed endpoint")


def fig_04():
    h = 610
    body, y = c.chrome(W, h, "BigQuery", "Studio")
    px, pw = 22, W - 44
    sql = [
        (0, [("CREATE OR REPLACE MODEL", KW), (" `telco_churn.churn_endpoint`", ID_)]),
        (0, [("INPUT", KW), (" (contract ", PL), ("STRING", KW), (", tenure_months ", PL),
             ("INT64", KW), (", monthly_charges ", PL), ("FLOAT64", KW), (")", PL)]),
        (0, [("OUTPUT", KW), (" (predicted_churn ", PL), ("STRING", KW), (", churn_probs ", PL),
             ("ARRAY<FLOAT64>", KW), (")", PL)]),
        (0, [("REMOTE WITH CONNECTION", KW), (" `us.gemini-conn`", ID_)]),
        (0, [("OPTIONS", KW), (" (ENDPOINT = ", PL),
             ("'https://us-central1-aiplatform.googleapis.com/v1/…/endpoints/482…'", STR), (");", PL)]),
    ]
    blk, bh = c.sql_block(px, y + 20, pw, sql)
    body += blk

    sql2 = [
        (0, [("SELECT", KW), (" customer_id, predicted_churn, churn_probs[", PL),
             ("OFFSET", KW), ("(", PL), ("0", NUM), (")] ", PL), ("AS", KW), (" p_churn", PL)]),
        (0, [("FROM", KW), (" ML.PREDICT(", FN)]),
        (0, [("  MODEL", KW), (" `telco_churn.churn_endpoint`", ID_), (",", PL)]),
        (0, [("  (", PL), ("SELECT", KW), (" customer_id, contract, tenure_months, monthly_charges", PL)]),
        (0, [("   ", PL), ("FROM", KW), (" `telco_churn.customers_ml`", ID_),
             (" LIMIT ", KW), ("5", NUM), (")", PL)]),
        (0, [(");", PL)]),
    ]
    blk2, bh2 = c.sql_block(px, y + 20 + bh + 14, pw, sql2)
    body += blk2

    ry = y + 20 + bh + 14 + bh2 + 22
    body += c.grid(px, ry, ["customer_id", "predicted_churn", "p_churn"], [
        ["9237-HQITU", "Yes", "0.941"],
        ["3668-QPYBK", "Yes", "0.812"],
        ["7590-VHVEG", "No", "0.204"],
        ["5575-GNVDE", "No", "0.061"],
    ], [280, 300, 316], mono_cols=(0, 2), align={2: "end"},
        colors={(0, 1): c.RED, (1, 1): c.RED, (2, 1): c.GREEN, (3, 1): c.GREEN})

    co, _ = c.callout(px, ry + 144, pw, [
        "This is the loop closing: the model left BigQuery to become an HTTP endpoint, and now",
        "BigQuery calls that endpoint back as if it were a local model. One deployed artifact serves",
        "your application and your analysts, so both are guaranteed to see identical predictions.",
    ], "ok")
    body += co
    write("l3-04-remote-model.svg", W, h, body,
          "Calling the deployed endpoint back from BigQuery with a remote model")


def fig_05():
    h = 512
    body, y = c.chrome(W, h, "Agent Platform", "Monitoring")
    px, pw = 22, W - 44
    body.append(c.t(px, y + 28, "churn-endpoint — feature drift", 15, c.TEXT, "500"))
    ch, cw = c.chip(px + 252, y + 16, "2 features above threshold", fill="#fce8e6", fg=c.RED)
    body += ch

    gx, gy, gw, gh = px, y + 52, 470, 218
    body.append(c.rect(gx, gy, gw, gh, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(gx + 16, gy + 26, "Distance vs. training baseline", 11.5, c.TEXT, "500"))
    body.append(c.t(gx + 16, gy + 40, "L-infinity for categorical  ·  Jensen-Shannon for numerical",
                    9.5, c.GREY))
    ax, ay, aw, ah = gx + 46, gy + 54, gw - 76, gh - 102
    for i in range(4):
        yy = ay + ah * i / 3
        body.append(c.line(ax, yy, ax + aw, yy, c.BORDER, 1, op=0.6))
        body.append(c.t(ax - 10, yy + 4, "%.1f" % (0.6 - 0.2 * i), 9.5, c.GREY, "400", "end"))
    thy = ay + ah * (1 - 0.30 / 0.6)
    body.append(c.line(ax, thy, ax + aw, thy, c.RED, 1.4, dash="5 4"))
    body.append(c.t(ax + aw - 4, thy - 6, "alert threshold 0.30", 9.5, c.RED, "500", "end"))
    series = [("payment_method", [.05, .07, .09, .14, .22, .31, .38], c.RED),
              ("contract", [.04, .05, .06, .08, .12, .19, .33], c.AMBER),
              ("monthly_charges", [.03, .04, .03, .05, .06, .05, .07], c.BLUE)]
    for name, vals, col in series:
        pts = [(ax + aw * i / (len(vals) - 1), ay + ah * (1 - v / 0.6)) for i, v in enumerate(vals)]
        body.append(c.path("M " + " L ".join("%.1f %.1f" % p for p in pts), stroke=col, sw=2.2))
        body.append(c.circle(pts[-1][0], pts[-1][1], 3.4, fill=col))
    for i, lbl in enumerate(["Aug 17", "18", "19", "20", "21", "22", "23"]):
        body.append(c.t(ax + aw * i / 6, gy + gh - 14, lbl, 9.5, c.GREY, "400", "middle"))

    lx = px + 486
    body.append(c.rect(lx, gy, pw - 486, gh, fill="#ffffff", stroke=c.BORDER, rx=8))
    body.append(c.t(lx + 16, gy + 26, "Monitored features", 11.5, c.TEXT, "500"))
    body += c.grid(lx + 16, gy + 40, ["Feature", "Metric", "Score", "Status"], [
        ["payment_method", "L-inf", "0.38", "Alert"],
        ["contract", "L-inf", "0.33", "Alert"],
        ["monthly_charges", "JS", "0.07", "OK"],
        ["tenure_months", "JS", "0.05", "OK"],
        ["internet_service", "L-inf", "0.04", "OK"],
    ], [148, 56, 60, 72], row_h=26, mono_cols=(2,), align={2: "end"},
        colors={(0, 3): c.RED, (1, 3): c.RED, (2, 3): c.GREEN,
                (3, 3): c.GREEN, (4, 3): c.GREEN})

    co, _ = c.callout(px, y + 290, pw, [
        "Categorical features use L-infinity distance; numerical features use Jensen-Shannon divergence.",
        "Drift is not automatically a bug: two features moving together usually means the business changed",
        "— here a payment-method migration shifted the mix, which also shifted contract types. The model",
        "is not broken; the world it trained on moved. Retrain on recent data and re-check Lab 2 metrics.",
    ], "warn")
    body += co
    write("l3-05-monitoring.svg", W, h, body,
          "Feature drift monitoring on the deployed endpoint")


def fig_06():
    h = 476
    body = [c.rect(0.5, 0.5, W - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 36, "Choosing a serving pattern", 15, c.TEXT, "500"))
    body.append(c.t(24, 58, "The pattern is decided by how the consumer reads the prediction, "
                            "not by how good the model is.", 11.5, c.GREY))

    cols = ["", "Batch (scheduled query)", "Online (endpoint)", "In-SQL (remote model)"]
    rows = [
        ["Latency", "hours — whenever it last ran", "~30 ms per request", "seconds per query"],
        ["Cost when idle", "zero", "per node-hour, always", "zero"],
        ["Setup", "one scheduled query", "endpoint + machine type", "endpoint + CREATE MODEL"],
        ["Scales to", "millions of rows", "requests per second", "millions of rows"],
        ["Use when", "dashboards, CRM lists,\nnightly campaigns",
         "app decides at click time\n(checkout, login, chat)",
         "analysts need the live\nmodel inside a join"],
    ]
    widths = [126, 262, 250, 258]
    x, y0 = 24, 78
    total = sum(widths)
    body.append(c.rect(x, y0, total, 30, fill=c.PANEL))
    body.append(c.rect(x, y0, total, 30 + 44 * len(rows), fill="none", stroke=c.BORDER, rx=4))
    heads = [c.GREY, c.BLUE, c.GREEN, c.AMBER]
    cx = x
    for i, hcell in enumerate(cols):
        body.append(c.t(cx + 12, y0 + 20, hcell, 11, heads[i], "600"))
        if i:
            body.append(c.line(cx, y0, cx, y0 + 30 + 44 * len(rows), c.BORDER, 1, op=.7))
        cx += widths[i]
    body.append(c.line(x, y0 + 30, x + total, y0 + 30, c.BORDER, 1))
    for ri, row in enumerate(rows):
        ry = y0 + 30 + 44 * ri
        if ri % 2:
            body.append(c.rect(x, ry, total, 44, fill="#fcfcfd"))
        if ri:
            body.append(c.line(x, ry, x + total, ry, c.BORDER, 1, op=.55))
        cx = x
        for ci, cell in enumerate(row):
            lines = cell.split("\n")
            for li, ln in enumerate(lines):
                oy = 27 if len(lines) == 1 else 20 + li * 15
                body.append(c.t(cx + 12, ry + oy, ln, 10.5,
                                c.GREY if ci == 0 else c.TEXT, "500" if ci == 0 else "400"))
            cx += widths[ci]

    co, _ = c.callout(24, y0 + 30 + 44 * len(rows) + 18, total, [
        "Most churn work never needs an endpoint. A nightly scheduled query feeding a table costs",
        "nothing between runs and serves dashboards and campaign lists perfectly well. Reach for an",
        "endpoint only when something has to decide inside a user-facing request.",
    ], "ok")
    body += co
    write("l3-06-patterns.svg", W, h, body, "Comparison of the three serving patterns")


if __name__ == "__main__":
    print("Generating lab 3 figures into %s" % OUT)
    for fn in (fig_00, fig_01, fig_02, fig_03, fig_04, fig_05, fig_06):
        fn()
    print("done.")
