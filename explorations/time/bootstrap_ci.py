"""Bootstrap 95% confidence intervals for the load-bearing headline statistics.

Adds honest uncertainty to the N=3 point estimates WITHOUT new API calls. Resampling is done
at the correct independent unit (cluster bootstrap): scenarios for E4, tasks for E5, and
(model,task) units for E1/E2/E6 -- not individual rows, which would understate uncertainty by
ignoring within-cluster correlation across the 3 trials.

Run: python bootstrap_ci.py     (reads each eN-*/results.jsonl)
"""
import json
import os
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(0)
B = 2000


def load(exp):
    return [json.loads(l) for l in open(os.path.join(HERE, exp, "results.jsonl")) if l.strip()]


def gm(xs):
    xs = [x for x in xs if x and x > 0]
    return float(np.exp(np.mean(np.log(xs)))) if xs else float("nan")


def ci(samples):
    s = np.array([x for x in samples if np.isfinite(x)])
    return np.percentile(s, 2.5), np.percentile(s, 97.5)


def cluster_boot(clusters, stat_fn):
    """clusters: dict id -> list of items. Resample cluster ids with replacement."""
    ids = list(clusters)
    out = []
    for _ in range(B):
        pick = RNG.choice(len(ids), size=len(ids), replace=True)
        items = []
        for i in pick:
            items.extend(clusters[ids[i]])
        v = stat_fn(items)
        if v is not None and np.isfinite(v):
            out.append(v)
    return out


def fmt(point, lo, hi):
    return f"{point:+.3f}  [95% CI {lo:+.3f}, {hi:+.3f}]"


def e4():
    rows = load("e4-harness-clock")
    print("E4 -- correct-decision rate by condition (cluster bootstrap over 9 scenarios)")
    for cond in ["none", "text", "harness"]:
        cr = [r for r in rows if r["condition"] == cond]
        clusters = {}
        for r in cr:
            clusters.setdefault(r["scenario_id"], []).append(
                str(r.get("decision_label")).strip().upper() == str(r.get("correct_label")).strip().upper())
        point = np.mean([x for v in clusters.values() for x in v])
        boot = cluster_boot(clusters, lambda items: np.mean(items) if items else None)
        lo, hi = ci(boot)
        print(f"  {cond:8} {point:.3f}  [95% CI {lo:.3f}, {hi:.3f}]")


def e5():
    rows = load("e5-latency-decoupled")
    act, pre, typ = {}, {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            act[k] = r["latency_s"]
        elif r["condition"] == "pre":
            pre[k] = r["parsed_estimate_s"]
        typ[(r["model"], r["task_id"])] = r["type"]
    print("E5 -- Spearman rho(estimate, actual latency) by type (cluster bootstrap over tasks)")
    for T in ["C", "A", "B"]:
        clusters = {}
        for k in act:
            if k in pre and pre[k] and act[k] and typ[(k[0], k[1])] == T:
                clusters.setdefault(k[1], []).append((act[k], pre[k]))

        def rho_fn(items):
            if len(items) < 3:
                return None
            a = [x[0] for x in items]; e = [x[1] for x in items]
            if len(set(e)) < 2 or len(set(a)) < 2:
                return None
            return spearmanr(a, e)[0]
        point = rho_fn([x for v in clusters.values() for x in v])
        boot = cluster_boot(clusters, rho_fn)
        lo, hi = ci(boot)
        print(f"  type {T}: {fmt(point, lo, hi)}")


def unit_boot_e1():
    rows = load("e1-self-duration")
    act, pre = {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "task":
            act[k] = r["latency_s"]
        elif r["condition"] == "pre":
            pre[k] = r["parsed_estimate_s"]
    units = {}
    for k in act:
        if k in pre and pre[k] and act[k]:
            units.setdefault((k[0], k[1]), []).append((act[k], pre[k]))
    pairs = [x for v in units.values() for x in v]
    point_gm = gm([p / a for a, p in pairs])
    point_rho = spearmanr([a for a, _ in pairs], [p for _, p in pairs])[0]
    gmb, rhob = [], []
    ids = list(units)
    for _ in range(B):
        pick = RNG.choice(len(ids), len(ids), replace=True)
        items = [x for i in pick for x in units[ids[i]]]
        gmb.append(gm([p / a for a, p in items]))
        if len(set(p for _, p in items)) > 1:
            rhob.append(spearmanr([a for a, _ in items], [p for _, p in items])[0])
    print("E1 -- overall self-latency calibration (bootstrap over model-task units)")
    print(f"  gm(pre/act): {point_gm:.3f}  [95% CI {ci(gmb)[0]:.3f}, {ci(gmb)[1]:.3f}]")
    print(f"  rho        : {point_rho:.3f}  [95% CI {ci(rhob)[0]:.3f}, {ci(rhob)[1]:.3f}]")


def e2():
    rows = load("e2-token-time")
    from collections import defaultdict
    gl, gt, es = defaultdict(list), defaultdict(list), defaultdict(lambda: defaultdict(list))
    for r in rows:
        mt = (r["model"], r["task_id"])
        if r["condition"] == "gen":
            gl[mt].append(r["latency_s"]); gt[mt].append(r["output_tokens"])
        else:
            es[mt][r["condition"]].append(r.get("parsed_estimate"))

    def mn(x):
        x = [v for v in x if v is not None]
        return np.mean(x) if x else None
    units = {}
    for mt in gl:
        units[mt] = dict(lat=mn(gl[mt]), tok=mn(gt[mt]),
                         sec=mn(es[mt]["cond_seconds"]), tokest=mn(es[mt]["cond_tokens"]))
    ids = list(units)

    def rho_for(items, akey, pkey):
        P = [(units[i][akey], units[i][pkey]) for i in items
             if units[i][akey] and units[i][pkey]]
        if len(P) < 3 or len(set(p for _, p in P)) < 2:
            return None
        return spearmanr([a for a, _ in P], [p for _, p in P])[0]
    p_sec = rho_for(ids, "lat", "sec"); p_tok = rho_for(ids, "tok", "tokest")
    sb, tb = [], []
    for _ in range(B):
        pick = [ids[i] for i in RNG.choice(len(ids), len(ids), replace=True)]
        v = rho_for(pick, "lat", "sec"); sb.append(v) if v is not None else None
        v = rho_for(pick, "tok", "tokest"); tb.append(v) if v is not None else None
    print("E2 -- seconds vs token-space rho (bootstrap over model-task units)")
    print(f"  seconds rho: {p_sec:.3f}  [95% CI {ci(sb)[0]:.3f}, {ci(sb)[1]:.3f}]")
    print(f"  tokens  rho: {p_tok:.3f}  [95% CI {ci(tb)[0]:.3f}, {ci(tb)[1]:.3f}]")


def e6():
    rows = load("e6-length-bias")
    from collections import defaultdict
    actual, est = {}, defaultdict(dict)
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            actual[k] = r["actual_output_tokens"]
        else:
            est[k][r["condition"]] = r["parsed_estimate_tok"]
    print("E6 -- pooled gm(pred/actual) by condition (bootstrap over model-task units)")
    for c in ["bare", "anchors", "self_revise"]:
        units = {}
        for k in actual:
            if c in est.get(k, {}) and est[k][c] and actual[k]:
                units.setdefault((k[0], k[1]), []).append(est[k][c] / actual[k])
        pts = [x for v in units.values() for x in v]
        point = gm(pts)
        ids = list(units)
        boot = []
        for _ in range(B):
            pick = RNG.choice(len(ids), len(ids), replace=True)
            boot.append(gm([x for i in pick for x in units[ids[i]]]))
        lo, hi = ci(boot)
        print(f"  {c:12} {point:.2f}  [95% CI {lo:.2f}, {hi:.2f}]")


if __name__ == "__main__":
    for fn in (e1 := unit_boot_e1, e2, e4, e5, e6):
        fn(); print()
