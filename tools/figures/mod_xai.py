# -*- coding: utf-8 -*-
"""Diagrams for the explainability module.

Run:  python tools/figures/mod_xai.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import svgkit as c  # noqa: E402

HERE = c.asset_dir("xai")

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


# --------------------------------------------------------------------------

def fig_shapley():
    w, h = 940, 620
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "A Shapley value is an average over every subset",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "How much does adding this feature change the prediction - "
                            "averaged across every group it could join.", 11, c.GREY))

    body.append(c.rect(24, 84, 560, 240, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 110, "MARGINAL CONTRIBUTION OF  tenure", 10.5, c.BLUE, "700"))
    body += c.grid(44, 126, ["Already present", "Prediction", "Adding tenure changes it by"],
                   [["{ }", "0.26", "+0.11"],
                    ["{ charges }", "0.31", "+0.09"],
                    ["{ contract }", "0.42", "+0.04"],
                    ["{ charges, contract }", "0.48", "+0.02"]],
                   [220, 150, 150])
    body.append(c.t(64, 292, "average these, weighted so each group SIZE counts equally",
                    10, c.GREY))
    body.append(c.t(64, 310, "-> that is tenure's Shapley value", 11, c.BLUE, "700"))

    body.append(c.rect(600, 84, 316, 240, fill="#f2fbf5", stroke=c.GREEN, rx=10, sw=1.6))
    body.append(c.t(620, 110, "WHY THIS ONE AND NOT ANOTHER", 10.5, c.GREEN, "700"))
    props = [("Efficiency", "attributions sum to"), ("", "prediction minus baseline"),
             ("Symmetry", "equal contributors,"), ("", "equal credit"),
             ("Dummy", "no effect, zero credit"),
             ("Additivity", "composes across a sum"), ("", "of models - hence ensembles")]
    y = 136
    for k, v in props:
        if k:
            body.append(c.t(620, y, k, 11, c.TEXT, "700"))
            body.append(c.t(716, y, v, 10, c.GREY))
        else:
            body.append(c.t(716, y, v, 10, c.GREY))
        y += 18 if not k else 20
    body.append(c.t(620, 298, "Shapley is the UNIQUE answer", 11, c.GREEN, "700"))
    body.append(c.t(620, 314, "satisfying all four.", 10, c.GREY))

    body.append(c.rect(24, 348, w - 48, 62, fill="#fff8f7", stroke=c.RED, rx=8, sw=1.4))
    body.append(c.rect(24, 348, 5, 62, fill=c.RED, rx=2.5))
    body.append(c.t(44, 370, "And why nobody computes it exactly", 11.5, c.TEXT, "700"))
    body.append(c.t(44, 390, "Every subset means 2^n of them. 10 features = 1,024 model calls "
                             "per prediction. 30 features = over a billion. Per prediction. "
                             "Everything below approximates.", 10, c.GREY))

    body.append(c.t(24, 444, "The baseline is doing more work than it looks",
                    12.5, c.TEXT, "700"))
    body.append(c.rect(24, 460, w - 48, 62, fill="#fff8e6", stroke=c.AMBER, rx=8, sw=1.4))
    body.append(c.rect(24, 460, 5, 62, fill=c.AMBER, rx=2.5))
    body.append(c.t(44, 482, "Attribution is never absolute", 11.5, c.TEXT, "700"))
    body.append(c.t(44, 502, "It answers \"why THIS rather than THAT\" - and \"that\" is the "
                             "baseline. Change it and every attribution changes, with no error "
                             "and no warning.", 10, c.GREY))

    co, _ = c.callout(24, 538, w - 48, [
        "Google's documented progression: start with a baseline of median values, then random",
        "values, then two baselines at the minimum and maximum. A zeros baseline on tabular data",
        "is the classic mistake - a customer with zero tenure and zero charges may not exist.",
    ], "ok")
    body += co
    write("xai-01-shapley.svg", w, h, body, "What a Shapley value is")


def fig_methods():
    w, h = 940, 700
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The method is chosen by the model, not by preference",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Ask one question first: can you take a gradient of this model?",
                    11, c.GREY))

    body += node(370, 84, 200, 50, "Differentiable?", None, col=c.PURPLE, fill="#faf5ff")

    body += node(60, 176, 260, 60, "SAMPLED SHAPLEY", "black box - needs nothing",
                 col=c.GREEN, fill="#f2fbf5")
    body.append(c.path("M 370 118 C 300 130 180 150 180 172", stroke=c.GREEN, sw=2))
    body.append(c.t(250, 152, "NO", 11, c.GREEN, "700", "middle"))

    body += node(620, 152, 260, 50, "Tabular?  INTEGRATED", "GRADIENTS", col=c.BLUE,
                 fill="#f8fbff")
    body += node(620, 216, 260, 50, "Natural image?  XRAI", None, col=c.BLUE, fill="#f8fbff")
    body.append(c.path("M 570 118 C 640 130 700 140 720 148", stroke=c.BLUE, sw=2))
    body.append(c.t(660, 122, "YES", 11, c.BLUE, "700", "middle"))
    body.append(c.line(750, 202, 750, 216, "#bdc1c6", 1.4))

    body.append(c.t(190, 262, "the ONLY option for tree ensembles", 10, c.GREEN, "700",
                    "middle"))
    body.append(c.t(190, 278, "and ensembles of trees + neural nets", 10, c.GREY, "400",
                    "middle"))

    body.append(c.t(24, 322, "Side by side", 12.5, c.TEXT, "700"))
    body += c.grid(24, 338, ["", "Sampled Shapley", "Integrated gradients", "XRAI"],
                   [["Needs", "nothing - black box", "differentiable model",
                     "differentiable model"],
                    ["Modality", "tabular", "tabular AND image", "IMAGE ONLY"],
                    ["Knob", "pathCount", "stepCount", "stepCount"],
                    ["Range", "[1, 50]", "[1, 100]", "[1, 100]"],
                    ["Extra baselines", "FREE - no latency cost", "cost one path integral each",
                     "cost one path integral each"]],
                   [150, 250, 250, 242])

    body.append(c.t(24, 512, "When approximationError exceeds 0.05", 12.5, c.TEXT, "700"))
    body.append(c.rect(24, 528, 440, 82, fill="#f2fbf5", stroke=c.GREEN, rx=8, sw=1.4))
    body.append(c.t(44, 552, "1.  Fix the baseline first", 11.5, c.TEXT, "700"))
    body.append(c.t(44, 572, "Costs nothing. It is a different reference point,", 10, c.GREY))
    body.append(c.t(44, 588, "not more compute - and it is often the cause.", 10, c.GREY))

    body.append(c.rect(476, 528, 440, 82, fill="#fff8e6", stroke=c.AMBER, rx=8, sw=1.4))
    body.append(c.t(496, 552, "2.  Then raise the iteration count", 11.5, c.TEXT, "700"))
    body.append(c.t(496, 572, "Linear runtime: double pathCount, double the", 10, c.GREY))
    body.append(c.t(496, 588, "latency. And it stops helping at the cap.", 10, c.GREY))

    co, _ = c.callout(24, 624, w - 48, [
        "An ensemble containing decision trees is not differentiable - the trees make it",
        "piecewise-constant - so integrated gradients and XRAI are unavailable no matter how you",
        "tune them. That is a capability boundary, not a quality trade-off.",
    ], "warn")
    body += co
    write("xai-02-methods.svg", w, h, body,
          "Choosing an attribution method by model type")


def fig_family():
    w, h = 940, 560
    body = [c.rect(0.5, 0.5, w - 1, h - 1, fill="#ffffff", stroke=c.BORDER, rx=10)]
    body.append(c.t(24, 34, "The relatives, and the split that matters",
                    15, c.TEXT, "500"))
    body.append(c.t(24, 56, "Local answers \"why this prediction\". Global answers \"what does "
                            "the model rely on\". They get swapped constantly.", 11, c.GREY))

    body.append(c.rect(24, 84, 440, 274, fill="#f8fbff", stroke=c.BLUE, rx=10, sw=1.6))
    body.append(c.t(44, 110, "LOCAL  -  about ONE prediction", 10.5, c.BLUE, "700"))
    local = [
        ("Shapley values  /  SHAP", "how much did each feature contribute"),
        ("Integrated gradients", "same question, gradient-based"),
        ("LIME", "what simple model behaves like this one, here"),
        ("Counterfactuals", "what would have had to DIFFER"),
        ("Example-based", "which training examples does this resemble"),
    ]
    y = 130
    for k, v in local:
        body.append(c.rect(44, y, 400, 42, fill="#ffffff", stroke=c.BORDER, rx=6))
        body.append(c.t(58, y + 18, k, 11, c.TEXT, "700"))
        body.append(c.t(58, y + 34, v, 9.5, c.GREY))
        y += 46

    body.append(c.rect(476, 84, 440, 274, fill="#faf5ff", stroke=c.PURPLE, rx=10, sw=1.6))
    body.append(c.t(496, 110, "GLOBAL  -  about the MODEL", 10.5, c.PURPLE, "700"))
    glob = [
        ("Permutation importance", "shuffle a column, watch performance drop"),
        ("Partial dependence  /  ICE", "how the prediction moves as one feature varies"),
        ("Surrogate models", "what simple model approximates this everywhere"),
    ]
    y = 130
    for k, v in glob:
        body.append(c.rect(496, y, 400, 42, fill="#ffffff", stroke=c.BORDER, rx=6))
        body.append(c.t(510, y + 18, k, 11, c.TEXT, "700"))
        body.append(c.t(510, y + 34, v, 9.5, c.GREY))
        y += 46
    body.append(c.t(696, 288, "\"Income matters most in our model\"", 10.5, c.TEXT, "500",
                    "middle"))
    body.append(c.t(696, 306, "is NOT why this applicant was declined.", 10.5, c.PURPLE,
                    "700", "middle"))

    body.append(c.t(24, 392, "Three worth knowing the catch on", 12.5, c.TEXT, "700"))
    rows = [
        ("LIME", c.AMBER,
         "Fast and model-agnostic - and only as good as the neighbourhood you sampled.",
         "No uniqueness guarantee: two LIME runs can disagree."),
        ("Permutation importance", c.AMBER,
         "Cheap, intuitive, global - and it misleads with correlated features.",
         "Shuffle one of two correlated predictors and the other carries the model. Both look useless."),
        ("Example-based", c.RED,
         "Needs a model that produces an EMBEDDING. Tree models are not supported.",
         "The exact inverse of sampled Shapley - and the one thing SHAP and LIME do not replace."),
    ]
    y = 410
    for name, col, l1, l2 in rows:
        body.append(c.rect(24, y, w - 48, 44, fill="#ffffff", stroke=col, rx=8, sw=1.3))
        body.append(c.rect(24, y, 5, 44, fill=col, rx=2.5))
        body.append(c.t(44, y + 19, name, 11, c.TEXT, "700"))
        body.append(c.t(220, y + 19, l1, 10, c.TEXT))
        body.append(c.t(220, y + 35, l2, 9.5, c.GREY))
        y += 50

    write("xai-03-family.svg", w, h, body,
          "Local versus global explanation techniques")


if __name__ == "__main__":
    print("Generating explainability figures into %s" % HERE)
    fig_shapley()
    fig_methods()
    fig_family()
    print("done.")
