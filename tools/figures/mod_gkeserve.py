# -*- coding: utf-8 -*-
"""Diagrams for the GKE LLM serving module.

Run:  python tools/figures/mod_gkeserve.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("gkeserve")

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


def arrow(x1, y1, x2, y2, col="#9aa0a6", sw=1.6, label=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    out = [c.line(x1, y1, hx, hy, col, sw),
           c.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
               x2, y2,
               x2 - 9 * math.cos(ang - 0.42), y2 - 9 * math.sin(ang - 0.42),
               x2 - 9 * math.cos(ang + 0.42), y2 - 9 * math.sin(ang + 0.42)), fill=col)]
    if label:
        out.append(c.t((x1 + x2) / 2, min(y1, y2) - 10, label, 9.5, c.GREY, "500", "middle"))
    return out


# --------------------------------------------------------------------------

def fig_metrics():
    w, h = 940, 720
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Why queue size, and not CPU", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Continuous batching is the mechanism. It is also what makes "
                            "the queue a good signal.", 11, c.GREY))

    # the curve idea: queue flat then sharp
    body.append(c.rect(24, 82, 440, 250, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 108, "QUEUE SIZE under rising load", 10.5, c.BLUE, "700"))
    ax_x, ax_y, ax_w, ax_h = 70, 130, 360, 150
    body.append(c.line(ax_x, ax_y + ax_h, ax_x + ax_w, ax_y + ax_h, "#bdc1c6", 1.4))
    body.append(c.line(ax_x, ax_y, ax_x, ax_y + ax_h, "#bdc1c6", 1.4))
    body.append(c.path("M 70 278 L 150 276 L 230 273 L 280 268 L 310 250 L 335 200 "
                       "L 355 150 L 370 134", stroke=c.BLUE, sw=2.4))
    body.append(c.line(300, 130, 300, 280, c.AMBER, 1.4, dash="4 4"))
    body.append(c.t(300, 124, "batch space runs out", 9.5, c.AMBER, "700", "middle"))
    body.append(c.t(160, 296, "near zero while there is room", 9.5, c.GREY, "400", "middle"))
    body.append(c.t(380, 296, "grows fast", 9.5, c.BLUE, "700", "middle"))
    body.append(c.t(244, 320, "That non-linearity is the spike detector.",
                    10.5, c.TEXT, "500", "middle"))

    # CPU flat
    body.append(c.rect(476, 82, 440, 250, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.6))
    body.append(c.t(496, 108, "CPU UTILISATION under the same load", 10.5, c.RED, "700"))
    ax2 = 522
    body.append(c.line(ax2, 280, ax2 + 360, 280, "#bdc1c6", 1.4))
    body.append(c.line(ax2, 130, ax2, 280, "#bdc1c6", 1.4))
    body.append(c.path("M 522 250 L 600 247 L 680 249 L 760 246 L 840 248 L 882 247",
                       stroke=c.RED, sw=2.4))
    body.append(c.t(696, 296, "barely moves - the work is on the GPU",
                    9.5, c.GREY, "400", "middle"))
    body.append(c.t(696, 320, "Scale on this and you scale late, or never.",
                    10.5, c.TEXT, "500", "middle"))

    body.append(c.t(24, 372, "The signals, in the order the docs recommend them",
                    12.5, c.TEXT, "700"))
    rows = [
        ("Queue size", c.GREEN, "tgi_queue_size  ·  vllm:num_requests_waiting",
         "First choice. Throughput and cost efficiency at once, if it meets your latency target."),
        ("Batch size", c.GREEN, "tgi_batch_current_size  ·  vllm:num_requests_running",
         "When queue-based scaling is not fast enough. Lower latency, harder threshold to find."),
        ("KV cache utilisation", c.AMBER, "vllm:gpu_cache_usage_perc",
         "The inference overview ranks this first for latency-sensitive work."),
        ("GPU duty cycle", c.AMBER, "DCGM_FI_DEV_GPU_UTIL",
         "Measures IF the GPU is busy, not how much work it is doing. Hard to map to latency."),
        ("GPU memory used", c.RED, "DCGM_FI_DEV_FB_USED",
         "TGI and vLLM PRE-ALLOCATE. Scales up and never back down."),
        ("CPU  /  memory  /  RPS", c.RED, "the built-in metrics",
         "Not recommended as sole indicators. RPS also ignores that requests vary hugely in cost."),
    ]
    y = 390
    for name, col, metric, desc in rows:
        body.append(c.rect(24, y, w - 48, 48, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 48, fill=col, rx=2.5))
        body.append(c.t(44, y + 21, name, 11, c.TEXT, "700"))
        body.append(c.mono(44, y + 39, metric, 9.5, c.GREY))
        body.append(c.t(370, y + 28, desc, 10, c.GREY))
        y += 54

    write("gke-01-metrics.svg", w, h, body,
          "Autoscaling signals for GPU inference on GKE")


def fig_pipeline():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Getting a server metric into HPA", 15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Four hops on the classic path. Since March 2026 there is a "
                            "shorter one, in preview.", 11, c.GREY))

    stops = [("model server", "/metrics", 24), ("PodMonitoring", "Managed Prometheus", 210),
             ("Cloud Monitoring", None, 396), ("Metrics adapter", "stackdriver", 582),
             ("HPA", "scales the Deployment", 768)]
    for name, sub, x in stops:
        wdt = 148 if x < 768 else 148
        body += node(x, 100, wdt, 58, name, sub, col=c.BLUE)
        if x < 768:
            body += arrow(x + wdt, 129, x + wdt + 38, 129, col="#bdc1c6", sw=1.4)

    body.append(c.t(24, 196, "And the field that trips people up", 12.5, c.TEXT, "700"))
    body += c.grid(24, 212, ["Metric kind", "HPA type", "Name format", "Selector"],
                   [["server metric", "Pods", "prometheus.googleapis.com|tgi_queue_size|gauge",
                     "none"],
                    ["GPU metric", "External",
                     "kubernetes.io|container|accelerator|duty_cycle",
                     "resource.labels..."],
                    ["DCGM metric", "External",
                     "prometheus.googleapis.com|dcgm_fi_dev_gpu_util|unknown",
                     "must be lowercase"]],
                   [160, 110, 420, 202])

    body.append(c.t(24, 348, "Picking the target value", 12.5, c.TEXT, "700"))
    body.append(c.rect(24, 364, 440, 96, fill="#f2fbf5", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.t(44, 388, "What the docs say", 11, c.GREEN, "700"))
    body.append(c.t(44, 408, "Start between 3 and 5. Load test. Raise it until", 10, c.GREY))
    body.append(c.t(44, 424, "latency reaches your target. Below 10, tune the", 10, c.GREY))
    body.append(c.t(44, 440, "scale-up policy to survive spikes.", 10, c.GREY))

    body.append(c.rect(476, 364, 440, 96, fill="#fff8e6", stroke=c.AMBER, rx=8, sw=1.4))
    body.append(c.t(496, 388, "What people quote", 11, c.AMBER, "700"))
    body.append(c.t(496, 408, "\"The knee where throughput stops growing and", 10, c.GREY))
    body.append(c.t(496, 424, "only latency rises.\" Sound reasoning - but it is in", 10, c.GREY))
    body.append(c.t(496, 440, "Google's BLOG posts, not the documentation.", 10, c.GREY))

    co, _ = c.callout(24, 474, w - 48, [
        "Mind the tolerance: HPA applies a default 0.1 no-action band around the target. With a",
        "target of 4, nothing happens between about 3.6 and 4.4 - a wide range for a small number.",
    ], "warn")
    body += co
    write("gke-02-metric-pipeline.svg", w, h, body,
          "How a model-server metric reaches the Horizontal Pod Autoscaler")


if __name__ == "__main__":
    print("Generating GKE serving figures into %s" % HERE)
    fig_metrics()
    fig_pipeline()
    print("done.")
