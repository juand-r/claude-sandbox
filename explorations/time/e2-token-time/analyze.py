"""E2 analysis. Reads results.jsonl (never calls the API).

Builds, per condition, paired (predicted, actual) data and reports calibration:
  - Spearman rho(predicted, actual)        -> ordering / monotonic calibration
  - geometric-mean ratio  gm(predicted/actual) -> systematic bias (1.0 = unbiased)

Conditions and what each predicts vs. its ground truth:
  (a) cond_seconds : predicted seconds   vs  actual latency_s
  (b) cond_tokens  : predicted tokens    vs  actual output_tokens   <- length space
  (c) tokens->sec  : pred_tokens / tps   vs  actual latency_s       (tps measured per model)
  (d) cond_reason  : predicted seconds   vs  actual latency_s

Key comparison: is (b) materially better-correlated than (a)? Does (d) beat (a)?

Two granularities:
  - per (model, task): average over the 3 trials, then correlate across the 12 tasks
    (this is the calibration question: can it rank task sizes?)
  - pooled across all models for an overall number.

Figures:
  scatter_<cond>.png   predicted vs actual (log-log), per condition, colored by model
  rho_by_condition.png bar chart of Spearman rho per condition (overall + per model)
"""

import sys, os, json
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

COND_SECONDS = "cond_seconds"   # (a)
COND_TOKENS  = "cond_tokens"    # (b)
COND_REASON  = "cond_reason"    # (d)
COND_DERIVED = "cond_derived"   # (c) synthetic, built from tokens + tps


def load():
    rows = []
    with open(RESULTS) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def gm_ratio(pred, actual):
    """Geometric mean of predicted/actual over paired arrays (>0 only)."""
    pred = np.asarray(pred, float); actual = np.asarray(actual, float)
    mask = (pred > 0) & (actual > 0) & np.isfinite(pred) & np.isfinite(actual)
    if mask.sum() == 0:
        return float("nan"), 0
    r = pred[mask] / actual[mask]
    return float(np.exp(np.mean(np.log(r)))), int(mask.sum())


def aggregate(rows):
    """Return:
      gen[(model,task)]   = dict(lat=mean latency, tok=mean output_tokens, n=trials)
      est[(model,task,cond)] = mean parsed_estimate over trials (ignoring None)
      tps[model]          = measured tokens/sec = sum(tokens)/sum(latency) over gen rows
    """
    gen_lat = defaultdict(list); gen_tok = defaultdict(list)
    est_vals = defaultdict(list)
    tps_tok = defaultdict(float); tps_lat = defaultdict(float)

    for r in rows:
        if not r.get("ok", True):
            continue
        m, t, cond = r["model"], r["task_id"], r["condition"]
        if cond == "gen":
            if r["latency_s"] > 0:
                gen_lat[(m, t)].append(r["latency_s"])
                gen_tok[(m, t)].append(r["output_tokens"])
                tps_tok[m] += r["output_tokens"]; tps_lat[m] += r["latency_s"]
        else:
            e = r.get("parsed_estimate")
            if e is not None and e > 0:
                est_vals[(m, t, cond)].append(e)

    gen = {k: dict(lat=float(np.mean(v)), tok=float(np.mean(gen_tok[k])), n=len(v))
           for k, v in gen_lat.items()}
    est = {k: float(np.mean(v)) for k, v in est_vals.items() if v}
    tps = {m: (tps_tok[m] / tps_lat[m]) for m in tps_tok if tps_lat[m] > 0}
    return gen, est, tps


def build_pairs(gen, est, tps):
    """Per condition -> dict(model -> list of (predicted, actual, task))."""
    pairs = {c: defaultdict(list) for c in
             (COND_SECONDS, COND_TOKENS, COND_REASON, COND_DERIVED)}
    for (m, t), g in gen.items():
        # (a) seconds
        if (m, t, COND_SECONDS) in est:
            pairs[COND_SECONDS][m].append((est[(m, t, COND_SECONDS)], g["lat"], t))
        # (b) tokens
        if (m, t, COND_TOKENS) in est:
            pairs[COND_TOKENS][m].append((est[(m, t, COND_TOKENS)], g["tok"], t))
        # (d) reason -> seconds
        if (m, t, COND_REASON) in est:
            pairs[COND_REASON][m].append((est[(m, t, COND_REASON)], g["lat"], t))
        # (c) derived seconds = predicted tokens / measured tps[model]
        if (m, t, COND_TOKENS) in est and m in tps and tps[m] > 0:
            derived = est[(m, t, COND_TOKENS)] / tps[m]
            pairs[COND_DERIVED][m].append((derived, g["lat"], t))
    return pairs


def stats_for(pair_lists):
    """pair_lists: model -> [(pred, actual, task)]. Returns per-model and pooled stats."""
    per_model = {}
    pooled_pred, pooled_actual = [], []
    for m, lst in pair_lists.items():
        if not lst:
            continue
        pred = [p for p, a, _ in lst]; actual = [a for p, a, _ in lst]
        rho, _ = spearmanr(pred, actual) if len(lst) >= 3 else (float("nan"), None)
        gm, ngm = gm_ratio(pred, actual)
        per_model[m] = dict(rho=rho, gm=gm, n=len(lst))
        pooled_pred += pred; pooled_actual += actual
    rho_p, _ = spearmanr(pooled_pred, pooled_actual) if len(pooled_pred) >= 3 else (float("nan"), None)
    gm_p, _ = gm_ratio(pooled_pred, pooled_actual)
    pooled = dict(rho=rho_p, gm=gm_p, n=len(pooled_pred))
    return per_model, pooled


CONDS = [
    (COND_SECONDS, "(a) predict SECONDS", "seconds"),
    (COND_TOKENS,  "(b) predict TOKENS",  "tokens"),
    (COND_DERIVED, "(c) tokens/tps->sec", "seconds"),
    (COND_REASON,  "(d) reason then sec", "seconds"),
]

MODEL_ORDER = ["haiku", "sonnet", "opus", "gpt4o-mini", "gpt4o", "gpt5", "gpt5.2", "o4-mini"]
COLORS = plt.cm.tab10(np.linspace(0, 1, 10))


def scatter_figs(pairs):
    for cond, title, unit in CONDS:
        plt.figure(figsize=(6, 6))
        models = [m for m in MODEL_ORDER if m in pairs[cond]] + \
                 [m for m in pairs[cond] if m not in MODEL_ORDER]
        allvals = []
        for i, m in enumerate(models):
            lst = pairs[cond][m]
            if not lst:
                continue
            pred = np.array([p for p, a, _ in lst])
            actual = np.array([a for p, a, _ in lst])
            allvals += list(pred) + list(actual)
            plt.scatter(actual, pred, s=28, alpha=0.7,
                        color=COLORS[i % 10], label=m)
        if allvals:
            lo = max(min(v for v in allvals if v > 0) * 0.5, 1e-3)
            hi = max(allvals) * 2
            plt.plot([lo, hi], [lo, hi], "k--", lw=1, label="perfect")
            plt.xlim(lo, hi); plt.ylim(lo, hi)
            plt.xscale("log"); plt.yscale("log")
        plt.xlabel(f"actual ({unit})"); plt.ylabel(f"predicted ({unit})")
        plt.title(f"E2 {title}: predicted vs actual")
        plt.legend(fontsize=7); plt.tight_layout()
        out = os.path.join(HERE, f"scatter_{cond}.png")
        plt.savefig(out, dpi=110); plt.close()
        print("wrote", out)


def rho_bar_fig(cond_stats):
    """cond_stats: cond -> (per_model dict, pooled dict)."""
    models = MODEL_ORDER
    present = []
    for m in models:
        if any(m in cond_stats[c][0] for c, _, _ in CONDS):
            present.append(m)
    groups = present + ["POOLED"]
    conds = [c for c, _, _ in CONDS]
    labels = {c: lbl for c, lbl, _ in CONDS}

    x = np.arange(len(groups)); w = 0.2
    plt.figure(figsize=(11, 5))
    for j, c in enumerate(conds):
        per_model, pooled = cond_stats[c]
        vals = [per_model.get(m, {}).get("rho", np.nan) for m in present]
        vals.append(pooled["rho"])
        plt.bar(x + (j - 1.5) * w, vals, w, label=labels[c])
    plt.axhline(0, color="k", lw=0.8)
    plt.xticks(x, groups, rotation=20, ha="right")
    plt.ylabel("Spearman rho (predicted vs actual)")
    plt.title("E2 calibration by condition and model (higher = better-ordered)")
    plt.legend(fontsize=8); plt.tight_layout()
    out = os.path.join(HERE, "rho_by_condition.png")
    plt.savefig(out, dpi=110); plt.close()
    print("wrote", out)


def main():
    rows = load()
    n_ok = sum(1 for r in rows if r.get("ok", True))
    print(f"loaded {len(rows)} rows ({n_ok} ok). models="
          f"{sorted(set(r['model'] for r in rows))}\n")

    gen, est, tps = aggregate(rows)
    print("Measured tokens/sec per model (from gen rows):")
    for m in MODEL_ORDER:
        if m in tps:
            print(f"  {m:11s} {tps[m]:6.1f} tok/s")
    print()

    # report parse-failure rate per condition
    fails = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["condition"] in (COND_SECONDS, COND_TOKENS, COND_REASON) and r.get("ok", True):
            fails[r["condition"]][1] += 1
            if r.get("parsed_estimate") is None:
                fails[r["condition"]][0] += 1
    print("Parse failures per condition (None / total):")
    for c in (COND_SECONDS, COND_TOKENS, COND_REASON):
        f, n = fails[c]
        print(f"  {c:13s} {f}/{n}")
    print()

    pairs = build_pairs(gen, est, tps)

    cond_stats = {}
    print("=" * 72)
    print(f"{'condition':22s} {'scope':12s} {'rho':>7s} {'gm(pred/act)':>14s} {'n':>4s}")
    print("-" * 72)
    for cond, title, unit in CONDS:
        per_model, pooled = stats_for(pairs[cond])
        cond_stats[cond] = (per_model, pooled)
        print(f"{title:22s} {'POOLED':12s} {pooled['rho']:7.3f} "
              f"{pooled['gm']:14.2f} {pooled['n']:4d}")
        for m in MODEL_ORDER:
            if m in per_model:
                s = per_model[m]
                print(f"{'':22s} {m:12s} {s['rho']:7.3f} {s['gm']:14.2f} {s['n']:4d}")
        print("-" * 72)

    # headline comparison
    a = cond_stats[COND_SECONDS][1]; b = cond_stats[COND_TOKENS][1]
    c = cond_stats[COND_DERIVED][1]; d = cond_stats[COND_REASON][1]
    print("\nHEADLINE (pooled):")
    print(f"  (a) seconds  : rho={a['rho']:.3f}  gm={a['gm']:.2f}")
    print(f"  (b) tokens   : rho={b['rho']:.3f}  gm={b['gm']:.2f}   <- length space")
    print(f"  (c) tok->sec : rho={c['rho']:.3f}  gm={c['gm']:.2f}")
    print(f"  (d) reason   : rho={d['rho']:.3f}  gm={d['gm']:.2f}")
    print(f"\n  token-space (b) vs second-space (a): "
          f"d_rho = {b['rho'] - a['rho']:+.3f}")
    print(f"  reasoning (d) vs baseline (a):        "
          f"d_rho = {d['rho'] - a['rho']:+.3f}")

    scatter_figs(pairs)
    rho_bar_fig(cond_stats)

    # dump a compact stats json for the report
    out = {cond: {"pooled": cond_stats[cond][1],
                  "per_model": cond_stats[cond][0]} for cond, _, _ in CONDS}
    out["tps"] = tps
    with open(os.path.join(HERE, "stats.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote stats.json")


if __name__ == "__main__":
    main()
