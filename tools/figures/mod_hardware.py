# -*- coding: utf-8 -*-
"""Diagrams for the GPUs and TPUs module.

Run:  python tools/figures/mod_hardware.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("hardware")

W = 940


def write(name, w, h, body, title):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(c.svg(w, h, body, title))
    print("  %-30s %sx%s" % (name, w, h))


# --------------------------------------------------------------------------

def fig_machine_name():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Machine type names are systematic, not cryptic",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Three fields, always in the same order.", 11, c.GREY))

    # the name, exploded
    body.append(c.rect(24, 82, w - 48, 130, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.5))
    body.append(c.mono(80, 128, "n1", 30, c.BLUE, "500"))
    body.append(c.mono(148, 128, "-", 30, "#bdc1c6"))
    body.append(c.mono(172, 128, "standard", 30, c.PURPLE, "500"))
    body.append(c.mono(392, 128, "-", 30, "#bdc1c6"))
    body.append(c.mono(416, 128, "4", 30, c.GREEN, "500"))

    body.append(c.line(96, 144, 96, 164, c.BLUE, 1.4))
    body.append(c.t(96, 180, "family", 10.5, c.BLUE, "700", "middle"))
    body.append(c.t(96, 196, "generation + purpose", 9.5, c.GREY, "400", "middle"))

    body.append(c.line(280, 144, 280, 164, c.PURPLE, 1.4))
    body.append(c.t(280, 180, "memory profile", 10.5, c.PURPLE, "700", "middle"))
    body.append(c.t(280, 196, "~3.75 GB per vCPU", 9.5, c.GREY, "400", "middle"))

    body.append(c.line(426, 144, 426, 164, c.GREEN, 1.4))
    body.append(c.t(426, 180, "size", 10.5, c.GREEN, "700", "middle"))
    body.append(c.t(426, 196, "4 vCPUs", 9.5, c.GREY, "400", "middle"))

    body.append(c.t(560, 116, "so:  4 vCPUs, about 15 GB RAM,", 12, c.TEXT, "500"))
    body.append(c.t(560, 136, "general-purpose, no accelerator.", 12, c.TEXT, "500"))

    body.append(c.t(24, 244, "The families worth recognising", 12.5, c.TEXT, "700"))
    body += c.grid(24, 260, ["Prefix", "Family", "Accelerator", "Reach for it when"],
                   [["e2 n1 n2 n4", "general purpose", "attached, optional",
                     "data prep, serving, CPU training"],
                    ["c2 c3 c4", "compute optimised", "none", "CPU-bound work, high clock"],
                    ["m1 m2 m3", "memory optimised", "none", "huge in-memory datasets"],
                    ["g2", "accelerator (L4)", "BUILT IN", "modern mid-tier GPU work"],
                    ["a2 a3 a4", "accelerator (NVIDIA)", "BUILT IN",
                     "A100 / H100 serious training"],
                    ["ct5lp- ct6e-", "Cloud TPU", "IS the TPU",
                     "large TensorFlow / JAX training"]],
                   [126, 190, 158, 342])

    body.append(c.t(24, 462, "Memory suffix", 12.5, c.TEXT, "700"))
    for i, (sfx, mem) in enumerate((("highcpu", "~0.9 GB per vCPU"),
                                    ("standard", "~3.75 GB per vCPU"),
                                    ("highmem", "~6.5 GB per vCPU"))):
        x = 24 + i * 300
        body.append(c.rect(x, 478, 286, 52, fill="#ffffff", stroke=c.BORDER, rx=8))
        body.append(c.mono(x + 16, 502, sfx, 13, c.PURPLE, "500"))
        body.append(c.t(x + 16, 520, mem, 10, c.GREY))

    write("hw-01-machine-names.svg", w, h, body,
          "How to read a Google Cloud machine type name")


def fig_mxu():
    w, h = 940, 660
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "Why 128 is the number that makes a TPU fast",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "The MXU is a 128x128 grid. Work is tiled into it, and "
                            "padding is billed like real work.", 11, c.GREY))

    # aligned
    body.append(c.rect(24, 84, 440, 268, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(44, 110, "DIMENSION 256  -  two full tiles", 10.5, c.GREEN, "700"))
    for i in range(2):
        x = 60 + i * 190
        body.append(c.rect(x, 130, 180, 180, fill="#e6f4ea", stroke=c.GREEN, rx=6, sw=1.4))
        for k in range(1, 6):
            body.append(c.line(x, 130 + k * 30, x + 180, 130 + k * 30, "#a8dab5", 1))
            body.append(c.line(x + k * 30, 130, x + k * 30, 310, "#a8dab5", 1))
        body.append(c.t(x + 90, 226, "128 x 128", 12, c.GREEN, "700", "middle"))
        body.append(c.t(x + 90, 244, "100% used", 10, c.GREY, "400", "middle"))
    body.append(c.t(244, 336, "you pay for 256, you use 256", 11, c.GREEN, "700", "middle"))

    # misaligned
    body.append(c.rect(476, 84, 440, 268, fill="#fff8f7", stroke=c.RED, rx=10, sw=1.6))
    body.append(c.t(496, 110, "DIMENSION 129  -  still two tiles", 10.5, c.RED, "700"))
    x = 512
    body.append(c.rect(x, 130, 180, 180, fill="#e6f4ea", stroke=c.GREEN, rx=6, sw=1.4))
    for k in range(1, 6):
        body.append(c.line(x, 130 + k * 30, x + 180, 130 + k * 30, "#a8dab5", 1))
        body.append(c.line(x + k * 30, 130, x + k * 30, 310, "#a8dab5", 1))
    body.append(c.t(x + 90, 226, "128 x 128", 12, c.GREEN, "700", "middle"))
    body.append(c.t(x + 90, 244, "100% used", 10, c.GREY, "400", "middle"))

    x2 = 702
    body.append(c.rect(x2, 130, 180, 180, fill="#fce8e6", stroke=c.RED, rx=6, sw=1.4))
    body.append(c.rect(x2, 130, 30, 180, fill="#f6aea9"))
    for k in range(1, 6):
        body.append(c.line(x2, 130 + k * 30, x2 + 180, 130 + k * 30, "#f6aea9", 1))
        body.append(c.line(x2 + k * 30, 130, x2 + k * 30, 310, "#f6aea9", 1))
    body.append(c.t(x2 + 105, 226, "1 column used", 11.5, c.RED, "700", "middle"))
    body.append(c.t(x2 + 105, 244, "127 columns of zeros", 10, c.GREY, "400", "middle"))
    body.append(c.t(696, 336, "you pay for 256, you use 129", 11, c.RED, "700", "middle"))

    body.append(c.t(24, 394, "The two levers, and what each is actually for",
                    12.5, c.TEXT, "700"))
    rows = [
        ("Multiples of 128", c.GREEN,
         "Batch size, hidden dim, embedding size, sequence length.",
         "Rounding 200 up to 256 can train FASTER despite being a bigger model."),
        ("bfloat16 activations", c.GREEN,
         "Same exponent range as float32, fewer mantissa bits.",
         "Halves memory traffic. Many ops are bandwidth-bound, not compute-bound."),
        ("TF_XLA_FLAGS", c.RED,
         "Does nothing - XLA is already on for every TPU workload.",
         "TPUs only execute XLA-compiled programs. There is nothing to enable."),
        ("Precision.HIGHEST", c.RED,
         "Actively slower.",
         "It emulates float32 by making MULTIPLE MXU passes. DEFAULT is the fast path."),
        ("Twisted topology / ICI", c.AMBER,
         "Right tool, wrong problem.",
         "Those tune chip-TO-chip traffic. MXU utilisation is inside one chip."),
    ]
    y = 412
    for name, col, l1, l2 in rows:
        body.append(c.rect(24, y, w - 48, 46, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 46, fill=col, rx=2.5))
        body.append(c.t(44, y + 20, name, 11, c.TEXT, "700"))
        body.append(c.t(212, y + 20, l1, 10, c.TEXT))
        body.append(c.t(212, y + 36, l2, 9.5, c.GREY))
        y += 50

    write("hw-02-mxu-tiling.svg", w, h, body,
          "The MXU is a 128x128 systolic array, so dimensions should be multiples of 128")


def fig_topology():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "TPU topology: chips, VMs, and why replicaCount is 1",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "A 4x4 topology really is four VMs. You still ask for one.",
                            11, c.GREY))

    # 4x4 grid of chips, grouped into 4 VMs of 4
    body.append(c.rect(24, 84, 400, 250, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 110, "tpuTopology = 4x4", 11, c.BLUE, "700"))
    body.append(c.t(44, 128, "16 chips, in a 4 x 4 grid", 9.5, c.GREY))
    for r in range(4):
        for col_i in range(4):
            vm = (r // 2) * 2 + (col_i // 2)
            fills = ["#d2e3fc", "#c8e6c9", "#f8d7da", "#fff0c2"]
            x = 60 + col_i * 84
            y = 148 + r * 42
            body.append(c.rect(x, y, 76, 36, fill=fills[vm], stroke=c.GREY, rx=5, sw=1))
            body.append(c.t(x + 38, y + 22, "chip", 9.5, c.TEXT, "400", "middle"))
    body.append(c.t(224, 328, "4 colours = 4 TPU VMs, 4 chips each",
                    10, c.GREY, "400", "middle"))

    # the spec
    body.append(c.rect(452, 84, 464, 250, fill="#ffffff", stroke=c.BORDER, rx=10, sw=1.4))
    body.append(c.t(472, 110, "WorkerPoolSpec", 11, c.TEXT, "700"))
    lines = [
        ('machineType', 'ct5lp-hightpu-4t', c.GREEN),
        ('tpuTopology', '4x4', c.GREEN),
        ('replicaCount', '1', c.RED),
    ]
    y = 138
    for k, v, col in lines:
        body.append(c.rect(472, y, 424, 44, fill="#f8f9fa", stroke=c.BORDER, rx=6))
        body.append(c.mono(488, y + 28, k, 12, c.GREY))
        body.append(c.mono(700, y + 28, v, 13, col, "500"))
        y += 52
    body.append(c.t(472, 314, "NOT 4. You are requesting one SLICE, not four workers.",
                    10.5, c.RED, "700"))

    body.append(c.t(24, 374, "v5e machine types and their topologies", 12.5, c.TEXT, "700"))
    body += c.grid(24, 390, ["machineType", "tpuTopology", "chips", "TPU VMs", "hosts"],
                   [["ct5lp-hightpu-1t", "1x1", "1", "1", "single"],
                    ["ct5lp-hightpu-4t", "2x2", "4", "1", "single"],
                    ["ct5lp-hightpu-8t", "2x4", "8", "1", "single"],
                    ["ct5lp-hightpu-4t", "4x4", "16", "4", "multi"],
                    ["ct5lp-hightpu-4t", "8x16", "128", "32", "multi"]],
                   [260, 200, 140, 160, 132])

    write("hw-03-tpu-topology.svg", w, h, body,
          "TPU v5e topology, VM count, and the replicaCount rule")


if __name__ == "__main__":
    print("Generating hardware figures into %s" % HERE)
    fig_machine_name()
    fig_mxu()
    fig_topology()
    print("done.")
