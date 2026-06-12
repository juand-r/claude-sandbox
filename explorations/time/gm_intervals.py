"""Compute geometric mean and multiplicative (geometric-SD) intervals for every GM ratio
reported in the paper. The interval is [m/s, m*s] where m = exp(mean ln r) is the geometric
mean of the ratios r = predicted/actual, and s = exp(sd ln r) is the geometric standard
deviation (a dimensionless multiplicative factor). Roughly 68% of individual ratios fall in
[m/s, m*s] under a log-normal model -- the multiplicative analogue of mean +/- 1 SD.

Run: python gm_intervals.py
"""
import json
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(exp):
    return [json.loads(l) for l in open(os.path.join(HERE, exp, "results.jsonl")) if l.strip()]


def gm_gsd(ratios):
    r = np.array([x for x in ratios if x and x > 0], float)
    if len(r) < 2:
        return float("nan"), float("nan")
    lg = np.log(r)
    m = float(np.exp(lg.mean()))
    s = float(np.exp(lg.std(ddof=1)))
    return m, s


def show(label, ratios):
    m, s = gm_gsd(ratios)
    if np.isnan(m):
        print(f"  {label:<28} n<2"); return
    print(f"  {label:<28} gm={m:.3f}  gsd={s:.2f}x  interval=[{m/s:.3f}, {m*s:.3f}]  n={len(ratios)}")


def e1():
    print("E1 -- pre-estimate / actual-latency, per model")
    rows = load("e1-self-duration")
    act, pre = {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "task":
            act[k] = r["latency_s"]
        elif r["condition"] == "pre":
            pre[k] = r["parsed_estimate_s"]
    bym = defaultdict(list)
    for k in act:
        if k in pre and pre[k] and act[k]:
            bym[k[0]].append(pre[k] / act[k])
    for m in sorted(bym):
        show(m, bym[m])
    show("OVERALL", [x for v in bym.values() for x in v])


def e2():
    print("E2 -- estimate / actual, per condition (pooled over model-task means)")
    rows = load("e2-token-time")
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
    sec = [mn(es[mt]["cond_seconds"]) / mn(gl[mt]) for mt in gl
           if mn(es[mt]["cond_seconds"]) and mn(gl[mt])]
    tok = [mn(es[mt]["cond_tokens"]) / mn(gt[mt]) for mt in gt
           if mn(es[mt]["cond_tokens"]) and mn(gt[mt])]
    rea = [mn(es[mt]["cond_reason"]) / mn(gl[mt]) for mt in gl
           if mn(es[mt]["cond_reason"]) and mn(gl[mt])]
    show("(a) seconds", sec)
    show("(b) tokens", tok)
    show("(d) reason-then-sec", rea)


def e5():
    print("E5 -- pre-estimate / actual-latency, per type")
    rows = load("e5-latency-decoupled")
    act, pre, typ = {}, {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            act[k] = r["latency_s"]
        elif r["condition"] == "pre":
            pre[k] = r["parsed_estimate_s"]
        typ[(r["model"], r["task_id"])] = r["type"]
    byt = defaultdict(list)
    for k in act:
        if k in pre and pre[k] and act[k]:
            byt[typ[(k[0], k[1])]].append(pre[k] / act[k])
    for t in ["A", "B", "C"]:
        show(f"type {t}", byt[t])


def e6():
    print("E6 -- predicted / actual output tokens, per condition (pooled)")
    rows = load("e6-length-bias")
    actual, est = {}, defaultdict(dict)
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            actual[k] = r["actual_output_tokens"]
        else:
            est[k][r["condition"]] = r["parsed_estimate_tok"]
    for c in ["bare", "anchors", "self_revise"]:
        ratios = [est[k][c] / actual[k] for k in actual
                  if c in est.get(k, {}) and est[k][c] and actual[k]]
        show(c, ratios)


def e10():
    print("E10 -- token estimate / actual reasoning tokens, per model (actual>0)")
    rows = load("e10-reasoning-tokens")
    tok, act = defaultdict(list), defaultdict(list)
    for r in rows:
        k = (r["model"], r["task_id"])
        if r["condition"] == "pre_tokens" and r["parsed_estimate"] is not None:
            tok[k].append(r["parsed_estimate"])
        elif r["condition"] == "gen":
            act[k].append(r["reasoning_tokens"])
    bym = defaultdict(list)
    for k in act:
        a = np.mean(act[k])
        if tok[k] and a > 0:
            bym[k[0]].append(np.mean(tok[k]) / a)
    for m in sorted(bym):
        show(m, bym[m])


if __name__ == "__main__":
    for fn in (e1, e2, e5, e6, e10):
        fn(); print()
