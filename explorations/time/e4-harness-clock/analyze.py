"""E4 analysis — reads results.jsonl, computes correct-decision rates by condition,
the marginal value of the harness clock (c-b) and text timestamps (b-a), and writes
figures. Never calls the API.
"""

import os, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

COND_ORDER = ["none", "text", "harness"]
COND_LABEL = {"none": "(a) no time", "text": "(b) text timestamps", "harness": "(c) harness clock"}
MODEL_ORDER = ["haiku", "sonnet", "opus", "gpt4o", "o4-mini"]


def load():
    rows = []
    with open(RESULTS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    return df


def main():
    df = load()
    n_total = len(df)
    n_fail = int((~df["ok"]).sum()) if "ok" in df else 0
    n_unparsed = int((df["ok"] & ~df["parsed"]).sum())
    print(f"rows: {n_total}  api_failures: {n_fail}  unparsed(ok): {n_unparsed}")

    # Keep only successfully parsed rows for accuracy.
    good = df[df["ok"] & df["parsed"]].copy()
    good["correct"] = (good["decision_label"] == good["correct_label"]).astype(int)

    # --- Overall accuracy by condition ---
    print("\n=== Overall correct-decision rate by condition ===")
    overall = good.groupby("condition")["correct"].agg(["mean", "count"])
    overall = overall.reindex(COND_ORDER)
    for c in COND_ORDER:
        print(f"  {COND_LABEL[c]:24s}: {overall.loc[c,'mean']:.3f}  (n={int(overall.loc[c,'count'])})")
    a, b, cc = [overall.loc[c, "mean"] for c in COND_ORDER]
    print(f"\n  marginal value of text timestamps (b - a): {b - a:+.3f}")
    print(f"  marginal value of harness clock   (c - b): {cc - b:+.3f}")
    print(f"  harness vs no-time                (c - a): {cc - a:+.3f}")

    # --- Per-model accuracy by condition ---
    print("\n=== Per-model correct-decision rate by condition ===")
    pivot = good.pivot_table(index="model", columns="condition", values="correct", aggfunc="mean")
    pivot = pivot.reindex(index=[m for m in MODEL_ORDER if m in pivot.index], columns=COND_ORDER)
    print(pivot.round(3).to_string())
    print("\n  per-model (c - b) and (c - a):")
    for m in pivot.index:
        bb, ccc, aa = pivot.loc[m, "text"], pivot.loc[m, "harness"], pivot.loc[m, "none"]
        print(f"    {m:9s}  c-b={ccc-bb:+.3f}   c-a={ccc-aa:+.3f}")

    # --- Accuracy split by fresh vs stale side of threshold ---
    print("\n=== Accuracy by condition x side-of-threshold ===")
    good["side"] = np.where(good["gap_seconds"] < good["threshold_s"], "fresh", "stale")
    side = good.pivot_table(index="side", columns="condition", values="correct", aggfunc="mean")
    side = side.reindex(columns=COND_ORDER)
    print(side.round(3).to_string())

    # --- Figure 1: grouped bar accuracy by condition x model ---
    fig, ax = plt.subplots(figsize=(10, 5.5))
    models = list(pivot.index)
    x = np.arange(len(models))
    w = 0.26
    colors = {"none": "#bdbdbd", "text": "#6baed6", "harness": "#31a354"}
    for i, c in enumerate(COND_ORDER):
        vals = [pivot.loc[m, c] for m in models]
        ax.bar(x + (i - 1) * w, vals, w, label=COND_LABEL[c], color=colors[c])
    # overall bars on the right
    ax.axhline(0.5, ls="--", lw=0.8, color="k", alpha=0.4, label="chance (0.5)")
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel("correct-decision rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("E4: accuracy by presentation condition x model")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    f1 = os.path.join(HERE, "fig_accuracy_by_condition.png")
    fig.savefig(f1, dpi=130)
    print(f"\nwrote {f1}")

    # --- Figure 2: overall accuracy by condition (the headline) ---
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    vals = [overall.loc[c, "mean"] for c in COND_ORDER]
    bars = ax2.bar([COND_LABEL[c] for c in COND_ORDER], vals,
                   color=[colors[c] for c in COND_ORDER])
    for bar, v in zip(bars, vals):
        ax2.text(bar.get_x() + bar.get_width() / 2, v + 0.01, f"{v:.2f}",
                 ha="center", va="bottom", fontsize=10)
    ax2.axhline(0.5, ls="--", lw=0.8, color="k", alpha=0.4)
    ax2.set_ylabel("correct-decision rate")
    ax2.set_ylim(0, 1.05)
    ax2.set_title("E4: overall accuracy by condition")
    plt.xticks(rotation=12, fontsize=8)
    fig2.tight_layout()
    f2 = os.path.join(HERE, "fig_overall_by_condition.png")
    fig2.savefig(f2, dpi=130)
    print(f"wrote {f2}")

    # --- Figure 3: accuracy vs gap (normalized to threshold) per condition ---
    # x-axis = log10(gap / threshold); <0 fresh, >0 stale.
    good["log_ratio"] = np.log10(good["gap_seconds"] / good["threshold_s"])
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    # bin the ratio so a few discrete points per condition
    for c in COND_ORDER:
        sub = good[good["condition"] == c]
        # group by the (scenario,gap) ratio value, average accuracy
        g = sub.groupby("log_ratio")["correct"].mean().reset_index().sort_values("log_ratio")
        ax3.plot(g["log_ratio"], g["correct"], "o-", label=COND_LABEL[c],
                 color=colors[c], alpha=0.85)
    ax3.axvline(0, ls=":", color="k", alpha=0.5)
    ax3.text(0.02, 0.02, "threshold", transform=ax3.get_xaxis_transform(), fontsize=8)
    ax3.set_xlabel("log10(gap / threshold)   (<0 = fresh, >0 = stale)")
    ax3.set_ylabel("correct-decision rate")
    ax3.set_ylim(0, 1.05)
    ax3.set_title("E4: accuracy vs distance from threshold, by condition")
    ax3.legend(fontsize=8)
    fig3.tight_layout()
    f3 = os.path.join(HERE, "fig_accuracy_vs_gap.png")
    fig3.savefig(f3, dpi=130)
    print(f"wrote {f3}")

    # --- Spend estimate ---
    print("\n=== Token usage / spend estimate (approx 2026 prices) ===")
    PRICES = {  # per 1M tokens (input, output)
        "haiku": (1, 5), "sonnet": (3, 15), "opus": (15, 75),
        "gpt4o-mini": (0.15, 0.6), "gpt4o": (2.5, 10),
        "gpt5": (1.25, 10), "gpt5.2": (1.25, 10), "o4-mini": (1.1, 4.4),
    }
    tok = df.groupby("model")[["input_tokens", "output_tokens"]].sum()
    total_cost = 0.0
    anth_cost = 0.0
    oai_cost = 0.0
    anth_models = {"haiku", "sonnet", "opus"}
    for m in tok.index:
        pin, pout = PRICES[m]
        cin = tok.loc[m, "input_tokens"] / 1e6 * pin
        cout = tok.loc[m, "output_tokens"] / 1e6 * pout
        c = cin + cout
        total_cost += c
        if m in anth_models:
            anth_cost += c
        else:
            oai_cost += c
        print(f"  {m:9s} in={int(tok.loc[m,'input_tokens']):7d} out={int(tok.loc[m,'output_tokens']):6d}  ~${c:.4f}")
    print(f"\n  Anthropic ~${anth_cost:.3f}   OpenAI ~${oai_cost:.3f}   TOTAL ~${total_cost:.3f}")


if __name__ == "__main__":
    main()
