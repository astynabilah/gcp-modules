import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("eventdriven")

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

def fig_duplicate():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Why a timeout creates a duplicate", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The failure is not that the call failed. It is that you do not know "
                            "whether it succeeded.", 11, c.GREY))

    # attempt 1
    body.append(c.rect(24, 78, w - 48, 176, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.5))
    body.append(c.t(44, 102, "ATTEMPT 1", 10.5, c.RED, "700"))
    steps = [
        ("File lands", "finalize event", c.GREY, 44),
        ("Function runs", "event id = abc123", c.BLUE, 206),
        ("Vertex API call", "job IS created", c.GREEN, 368),
        ("...timeout", "no response", c.RED, 530),
        ("Function fails", "retry scheduled", c.RED, 692),
    ]
    for name, sub, col, x in steps:
        body += node(x, 120, 148, 52, name, sub, col=col)
    for x in (192, 354, 516, 678):
        body += arrow(x, 146, x + 14, 146, col="#bdc1c6")

    body.append(c.rect(368, 190, 300, 46, fill=c.AMBER, rx=7, op=0.16))
    body.append(c.t(518, 210, "The training job started.", 10.5, c.AMBER, "700", "middle"))
    body.append(c.t(518, 226, "The function has no idea.", 10, c.TEXT, "400", "middle"))

    # attempt 2
    body.append(c.rect(24, 270, w - 48, 150, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.5))
    body.append(c.t(44, 294, "ATTEMPT 2 — the retry", 10.5, c.BLUE, "700"))
    body.append(c.t(180, 294, "same event, SAME event id abc123", 10, c.GREY))
    steps2 = [
        ("Same event", "id = abc123", c.GREY, 44),
        ("Function runs", "again", c.BLUE, 206),
        ("Vertex API call", "job created AGAIN", c.RED, 368),
        ("Firestore write", "second entry", c.RED, 530),
        ("Success", "and now wrong", c.RED, 692),
    ]
    for name, sub, col, x in steps2:
        body += node(x, 312, 148, 52, name, sub, col=col)
    for x in (192, 354, 516, 678):
        body += arrow(x, 338, x + 14, 338, col="#bdc1c6")
    body.append(c.t(470, 396, "two training jobs, two metadata rows, one uploaded file",
                    10.5, c.RED, "700", "middle"))

    co, _ = c.callout(24, 436, w - 48, [
        "Cloud Functions gives AT-LEAST-ONCE execution for event-driven functions, and Cloud Storage",
        "delivers events at-least-once too. Retries are not a bug you enabled by accident — they are the",
        "reliability mechanism. The bug is that the handler is not safe to run twice. The fix is never to",
        "stop retrying; it is to make running twice harmless.",
    ], "warn")
    body += co
    write("ev-01-duplicate.svg", w, h, body,
          "How at-least-once delivery plus a timeout produces duplicate work")


def fig_idempotent():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The fix — an idempotent handler keyed on the event id",
                    15, c.TEXT, "500"))

    body += node(24, 74, 150, 50, "Event arrives", "id = abc123", col=c.GREY)
    body += arrow(174, 99, 214, 99)

    body.append(c.rect(214, 62, 470, 236, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(234, 86, "INSIDE A FIRESTORE TRANSACTION", 10.5, c.GREEN, "700"))
    body.append(c.t(234, 104, "read and write happen atomically - nobody can interleave",
                    9.5, c.GREY))

    body += node(234, 118, 200, 48, "Does doc abc123", "already exist?", col=c.GREEN)
    body += node(464, 118, 200, 48, "Write doc abc123", "+ training job id", col=c.GREEN)
    body += arrow(434, 142, 464, 142, col=c.GREEN, label="no")

    body.append(c.rect(234, 186, 430, 44, fill=c.BLUE, rx=8, op=0.10))
    body.append(c.t(449, 206, "yes  ->  return immediately, do nothing", 11, c.BLUE,
                    "700", "middle"))
    body.append(c.t(449, 222, "the retry becomes a no-op", 9.5, c.GREY, "400", "middle"))

    body.append(c.t(234, 258, "Only after the transaction commits do you start the training job.",
                    10, c.TEXT))
    body.append(c.t(234, 276, "Commit first, then act - so a crash mid-way cannot lose the record.",
                    10, c.GREY))

    body += arrow(684, 142, 724, 142, col=c.GREEN)
    body += node(724, 118, 192, 48, "Start training job", "exactly once", col=c.PURPLE)

    body.append(c.t(24, 330, "Why the transaction is not optional", 12.5, c.TEXT, "700"))
    for i, ln in enumerate([
        "A plain read-then-write has a race: two retries can BOTH read 'not found' before either writes,",
        "and both then start a job. Retries can overlap - they are not guaranteed to be sequential.",
        "A transaction makes check-and-write a single atomic step, so exactly one attempt wins.",
    ]):
        body.append(c.t(24, 354 + i * 18, ln, 10.5, c.GREY if i else c.TEXT))

    body.append(c.t(24, 428, "Where to keep the processed-event record", 12.5, c.TEXT, "700"))
    for i, (svc, note) in enumerate([
        ("Firestore", "transactional, durable - the default choice"),
        ("Memorystore", "fast, cheaper at very high volume, less durable"),
        ("Any database", "as long as it supports an atomic check-and-write"),
    ]):
        body.append(c.t(40, 452 + i * 17, "-", 10.5, c.GREY))
        body.append(c.t(56, 452 + i * 17, svc, 10.5, c.TEXT, "600"))
        body.append(c.t(180, 452 + i * 17, note, 10.5, c.GREY))

    co, _ = c.callout(24, 508, w - 48, [
        "Give the record a TTL matching your dedup window, or the collection grows forever.",
    ], "info")
    body += co
    write("ev-02-idempotent.svg", w, h, body,
          "An idempotent handler using a transactional check-and-write")


def fig_keys():
    w, h = 940, 672
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Choosing a deduplication key", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The key decides what counts as 'the same work'. Get this wrong and "
                            "you either duplicate or silently skip.", 11, c.GREY))

    rows = [
        ("CloudEvent id", c.GREEN, "CORRECT",
         "Unchanged across retries of the same event; different for a genuinely new event.",
         "Per the CloudEvents spec, source + id identifies an event uniquely."),
        ("File name", c.RED, "WRONG",
         "Re-uploading the same file for a legitimate second training run is dropped as a duplicate.",
         "It identifies the object, not the event about the object."),
        ("File name + generation", c.AMBER, "SOMETIMES",
         "Distinguishes object versions, so a re-upload is a new key.",
         "Reasonable when you truly want once-per-object-version."),
        ("Content hash", c.AMBER, "SOMETIMES",
         "Same bytes are processed once, ever, even under a different name.",
         "Right for expensive dedup of identical payloads; wrong if reprocessing is valid."),
    ]
    y = 82
    for name, col, verdict, what, why in rows:
        body.append(c.rect(24, y, w - 48, 92, fill="#ffffff", stroke=col, rx=9, sw=1.4))
        body.append(c.rect(24, y, 6, 92, fill=col, rx=3))
        body.append(c.mono(46, y + 28, name, 12, c.TEXT))
        ch, cw = c.chip(w - 148, y + 15, verdict, fill=col, fg=col)
        ch[0] = ch[0].replace('opacity="1"', 'opacity="0.16"')
        body += ch
        body.append(c.t(46, y + 52, what, 10.5, c.TEXT))
        body.append(c.t(46, y + 72, why, 10, c.GREY))
        y += 100

    body.append(c.t(24, y + 24, "Things that look like fixes and are not", 12.5, c.TEXT, "700"))
    for i, (thing, why) in enumerate([
        ("max instances = 1", "Stops CONCURRENCY, not repetition. A sequential retry of the "
                              "same event still duplicates."),
        ("turning retries off", "Removes duplicates by removing reliability. Transient failures "
                                "now silently lose work."),
    ]):
        yy = y + 48 + i * 34
        body.append(c.rect(24, yy - 12, 4, 26, fill=c.RED, rx=2))
        body.append(c.mono(40, yy, thing, 10.5, c.RED))
        body.append(c.t(220, yy, why, 10.5, c.GREY))

    co, _ = c.callout(24, y + 122, w - 48, [
        "Only idempotency solves this. Everything else either reduces throughput, reduces reliability,",
        "or changes the definition of 'the same work' in a way you did not intend.",
    ], "ok")
    body += co
    write("ev-03-dedup-keys.svg", w, h, body, "Choosing a deduplication key")


if __name__ == "__main__":
    print("Generating event-driven figures into %s" % HERE)
    fig_duplicate()
    fig_idempotent()
    fig_keys()
    print("done.")
