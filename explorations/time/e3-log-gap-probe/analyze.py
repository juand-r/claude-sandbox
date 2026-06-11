"""E3 — analysis. Reads results.jsonl (never calls the API).

Computes, per (model, scenario):
  - decision at each gap (majority over trials), as FRESH(0) / STALE(1)
  - SENSITIVITY: does the decision change at all across the timed gaps?
  - CORRECTNESS: does it flip at roughly the right threshold? Scored as the
    fraction of timed gaps where the majority decision matches the
    human-sensible expectation (gap < threshold -> FRESH; gap >= -> STALE).
  - control comparison: majority decision with no time info.

Figures:
  - heatmap.png : decision vs gap, per scenario x model (one panel per scenario)
  - sensitivity.png : bar of sensitivity by model (fraction of scenarios where
    the decision responds to the gap)
"""

import json
import os
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

TIMED_GAPS = ["1s", "1min", "1h", "1day", "1week"]
GAP_SECONDS = {"1s": 1, "1min": 60, "1h": 3600, "1day": 86400, "1week": 604800}
ALL_GAPS = TIMED_GAPS + ["control"]


def load():
    rows = []
    with open(RESULTS) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def majority(decisions):
    """Majority label among non-None; None if all None or a tie with no winner."""
    vals = [d for d in decisions if d is not None]
    if not vals:
        return None
    counts = defaultdict(int)
    for v in vals:
        counts[v] += 1
    best = max(counts.values())
    winners = [k for k, c in counts.items() if c == best]
    return winners[0] if len(winners) == 1 else winners[0]  # deterministic


def main():
    rows = load()

    # Index: (model, scenario, gap) -> list of decision labels (per trial)
    by = defaultdict(list)
    labels_of = {}     # scenario -> (fresh, stale)
    thresh_of = {}     # scenario -> threshold_s
    models, scenarios = [], []
    for r in rows:
        by[(r["model"], r["scenario_id"], r["gap_label"])].append(r["decision_label"])
        labels_of[r["scenario_id"]] = tuple(r["labels"])
        thresh_of[r["scenario_id"]] = r["threshold_s"]
        if r["model"] not in models:
            models.append(r["model"])
        if r["scenario_id"] not in scenarios:
            scenarios.append(r["scenario_id"])

    # ordering: keep roster/scenario order as encountered
    n_unparsed = sum(1 for r in rows if r["decision_label"] is None)
    print(f"loaded {len(rows)} records, {n_unparsed} unparsed "
          f"({100*n_unparsed/len(rows):.1f}%)")
    print(f"models: {models}")
    print(f"scenarios: {scenarios}\n")

    def expected(scenario, gap):
        """Human-sensible expected label for a timed gap."""
        fresh, stale = labels_of[scenario]
        return stale if GAP_SECONDS[gap] >= thresh_of[scenario] else fresh

    # ----- per (model, scenario): majority decision per gap ------------------
    # maj[(model,scenario)][gap] = label
    maj = {}
    for model in models:
        for sc in scenarios:
            maj[(model, sc)] = {
                g: majority(by.get((model, sc, g), [])) for g in ALL_GAPS}

    # ----- SENSITIVITY: does decision change across timed gaps? --------------
    # per model: fraction of scenarios where the set of majority labels over the
    # 5 timed gaps has > 1 distinct (non-None) value.
    sens_by_model = {}
    sens_detail = {}  # (model,scenario)->bool
    for model in models:
        flips = 0
        for sc in scenarios:
            vals = {maj[(model, sc)][g] for g in TIMED_GAPS}
            vals.discard(None)
            changed = len(vals) > 1
            sens_detail[(model, sc)] = changed
            flips += int(changed)
        sens_by_model[model] = flips / len(scenarios)

    # ----- CORRECTNESS: fraction of timed gaps matching expectation ----------
    corr_by_model = {}
    corr_detail = {}  # (model,scenario)->frac
    for model in models:
        accs = []
        for sc in scenarios:
            hits, tot = 0, 0
            for g in TIMED_GAPS:
                d = maj[(model, sc)][g]
                if d is None:
                    continue
                tot += 1
                if d == expected(sc, g):
                    hits += 1
            frac = hits / tot if tot else float("nan")
            corr_detail[(model, sc)] = frac
            if tot:
                accs.append(frac)
        corr_by_model[model] = float(np.mean(accs)) if accs else float("nan")

    # ----- print summary -----------------------------------------------------
    print("=== SENSITIVITY (frac of scenarios where decision responds to gap) ===")
    for m in models:
        print(f"  {m:10s} {sens_by_model[m]:.2f}")
    print("\n=== CORRECTNESS (mean frac of timed gaps matching human threshold) ===")
    for m in models:
        print(f"  {m:10s} {corr_by_model[m]:.2f}")

    # control vs timed: does removing time info change the decision?
    print("\n=== CONTROL vs timed (per model: frac of scenarios where control "
          "label differs from the 1s label) ===")
    for m in models:
        diff = 0
        for sc in scenarios:
            c = maj[(m, sc)]["control"]
            s = maj[(m, sc)]["1s"]
            if c is not None and s is not None and c != s:
                diff += 1
        print(f"  {m:10s} {diff/len(scenarios):.2f}")

    # per-scenario sensitivity table
    print("\n=== per-scenario sensitivity (1=decision changed across gaps) ===")
    header = "scenario".ljust(16) + "".join(m[:7].ljust(8) for m in models)
    print(header)
    for sc in scenarios:
        line = sc.ljust(16) + "".join(
            ("1" if sens_detail[(m, sc)] else ".").ljust(8) for m in models)
        print(line)

    # ----- FIGURE 1: heatmap decision vs gap (panel per scenario) -----------
    # encode FRESH=0 (light), STALE=1 (dark), None=nan
    ncols = 3
    nrows = int(np.ceil(len(scenarios) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.2 * ncols, 2.6 * nrows),
                             squeeze=False)
    cmap = plt.cm.RdYlBu_r
    for idx, sc in enumerate(scenarios):
        ax = axes[idx // ncols][idx % ncols]
        fresh, stale = labels_of[sc]
        M = np.full((len(models), len(ALL_GAPS)), np.nan)
        for i, m in enumerate(models):
            for j, g in enumerate(ALL_GAPS):
                d = maj[(m, sc)][g]
                if d == fresh:
                    M[i, j] = 0.0
                elif d == stale:
                    M[i, j] = 1.0
        ax.imshow(M, aspect="auto", cmap=cmap, vmin=0, vmax=1)
        ax.set_xticks(range(len(ALL_GAPS)))
        ax.set_xticklabels(ALL_GAPS, rotation=45, ha="right", fontsize=7)
        ax.set_yticks(range(len(models)))
        ax.set_yticklabels(models, fontsize=7)
        # mark the human threshold boundary among timed gaps
        thr = thresh_of[sc]
        boundary = None
        for j, g in enumerate(TIMED_GAPS):
            if GAP_SECONDS[g] >= thr:
                boundary = j
                break
        if boundary is not None:
            ax.axvline(boundary - 0.5, color="black", lw=1.5, ls="--")
        ax.set_title(f"{sc}\n0={fresh} 1={stale}", fontsize=8)
    # hide unused panels
    for idx in range(len(scenarios), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")
    fig.suptitle("E3: decision vs timestamp gap (dashed = human threshold; "
                 "blue=FRESH, red=STALE)", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(os.path.join(HERE, "heatmap.png"), dpi=130)
    print("\nwrote heatmap.png")

    # ----- FIGURE 2: sensitivity + correctness bars by model ----------------
    fig2, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4))
    x = np.arange(len(models))
    axA.bar(x, [sens_by_model[m] for m in models], color="steelblue")
    axA.set_xticks(x); axA.set_xticklabels(models, rotation=30, ha="right")
    axA.set_ylim(0, 1); axA.set_ylabel("frac scenarios decision responds to gap")
    axA.set_title("Sensitivity by model")
    axA.axhline(0, color="k", lw=0.5)
    axB.bar(x, [corr_by_model[m] for m in models], color="indianred")
    axB.set_xticks(x); axB.set_xticklabels(models, rotation=30, ha="right")
    axB.set_ylim(0, 1); axB.set_ylabel("mean frac gaps matching human threshold")
    axB.set_title("Correctness by model")
    axB.axhline(0.5, color="gray", ls=":", lw=1)
    fig2.tight_layout()
    fig2.savefig(os.path.join(HERE, "sensitivity.png"), dpi=130)
    print("wrote sensitivity.png")

    # ----- spend estimate ----------------------------------------------------
    PRICE = {  # per 1M tokens (in, out), approx 2026
        "haiku": (1, 5), "sonnet": (3, 15), "opus": (15, 75),
        "gpt4o-mini": (0.15, 0.6), "gpt4o": (2.5, 10),
        "gpt5": (1.25, 10), "gpt5.2": (1.25, 10), "o4-mini": (1.1, 4.4),
    }
    tok = defaultdict(lambda: [0, 0])
    for r in rows:
        tok[r["model"]][0] += r.get("input_tokens", 0)
        tok[r["model"]][1] += r.get("output_tokens", 0)
    print("\n=== spend estimate (approx) ===")
    tot_anth, tot_oai = 0.0, 0.0
    for m, (ti, to) in tok.items():
        pi, po = PRICE.get(m, (0, 0))
        cost = ti / 1e6 * pi + to / 1e6 * po
        prov = "anthropic" if m in {"haiku", "sonnet", "opus"} else "openai"
        if prov == "anthropic":
            tot_anth += cost
        else:
            tot_oai += cost
        print(f"  {m:10s} in={ti:6d} out={to:6d}  ${cost:.4f}")
    print(f"  TOTAL anthropic ${tot_anth:.4f}   openai ${tot_oai:.4f}")


if __name__ == "__main__":
    main()
