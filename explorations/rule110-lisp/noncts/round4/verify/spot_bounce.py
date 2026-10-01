"""Spot-check shuttle's single-wall reflection tables (bounce_table_*.jsonl)
with my own scene assembly (rawscene), runner (hrun) and classification.

Per sampled row: wall (bits, pR) then head (bits, pR) GAP cells to its right
(L side: head moves left into the wall) or head left of the wall (R side).
GAP differs from shuttle's 24 on purpose: by the single-class lemma the
outcome must not depend on it (a test that can fail).
At T (multiple of 420 = lcm of 3,4,7,10,12,15 and of 14) every defect is
typed by velocity: compare the cells around it with the row at T + 420
shifted by v * 420 for v in {0, 2/3, 1/5, -1/2, -4/15, -1/3, -8/30*...}.
kind: one stationary defect + movers all going back = reflect, all
continuing = pass, none = absorbed, else dirty (moving products of mixed
velocity, 0 or >= 2 stationary, unknown velocity).
Also compared: wall_out (bits, pR, dx) in list form at T (T = 0 mod 14, so
a stationary object's row equals its t = 0 row), and the movers' canonical
form (min over P time phases of the list form) vs head_out_canon.

python3 spot_bounce.py TABLE SAMPLE_PER_KIND [seed]"""
import json
import random
import sys
from collections import Counter

import numpy as np

import hrun
import rawscene

vlib = hrun.vlib
ETH = "11111000100110"
T = 840
VEL = {"0": (0, 1), "A": (2, 3), "D": (1, 5), "B": (-1, 2), "E": (-4, 15),
       "G": (-1, 3), "Ebar": (-4, 15), "F": (-1, 9), "C": (0, 1)}
SPEEDS = [(0, 1), (2, 3), (1, 5), (-1, 2), (-4, 15), (-1, 3), (-1, 9), (-18, 92)]


def ether_phase(row, i, x, t):
    for q in range(14):
        if all(row[i + k] == int(ETH[(x + k + 4 * t + q) % 14]) for k in range(14)):
            return q
    return None


def list_form(cells, x0, t, a, b):
    """List form of the object occupying cells[a:b] (indices) of a row whose
    cell 0 is global x0, at time t: (bits, pR, origin)."""
    pl = ether_phase(cells, a - 20, x0 + a - 20, t)
    pr = ether_phase(cells, b + 6, x0 + b + 6, t)
    assert pl is not None and pr is not None
    phi = (x0 + a + 4 * t + pl) % 14
    return ETH[:phi] + "".join(map(str, cells[a:b])), (pr - pl) % 14, x0 + a - phi


def defects_with_velocity(h, lo, hi):
    r0 = h.cells(lo, hi)
    t0 = h.t
    h.goto(t0 + 420)
    r1 = h.cells(lo - 420, hi + 420)
    out = []
    for d in vlib.defects(r0):
        a, b = d["lo"], d["hi"]
        v = None
        for num, den in SPEEDS:
            s = num * 420 // den
            seg1 = r1[a + 420 + s - 3:b + 420 + s + 3]
            if np.array_equal(seg1, r0[a - 3:b + 3]):
                v = (num, den)
                break
        out.append((a, b, v))
    return r0, out


def check(row_rec, gap=40):
    w, hd, side = row_rec["wall"], row_rec["head"], row_rec["side"]
    if side == "L":
        objs = [(w["bits"], w["pR"], 100), (hd["bits"], hd["pR"], gap)]
    else:
        objs = [(hd["bits"], hd["pR"], 100), (w["bits"], w["pR"], gap)]
    row, org, starts = rawscene.assemble(objs)
    wall_x = starts[0] if side == "L" else starts[1]
    h = hrun.HRun(row, org)
    h.goto(T)
    lo, hi = org - T - 200, org + len(row) + T + 200
    r0, ds = defects_with_velocity(h, lo, hi)
    stat = [(a, b) for a, b, v in ds if v == (0, 1)]
    mov = [(a, b, v) for a, b, v in ds if v not in (None, (0, 1))]
    unk = [d for d in ds if d[2] is None]
    back = 1 if side == "L" else -1          # sign of a reflected head's velocity
    if unk or len(stat) != 1:
        kind = "dirty"
    elif not mov:
        kind = "absorbed"
    elif len({v for _, _, v in mov}) != 1:
        kind = "dirty"
    elif all(np.sign(v[0]) == back for _, _, v in mov):
        kind = "reflect"
    elif all(np.sign(v[0]) == -back for _, _, v in mov):
        kind = "pass"
    else:
        kind = "dirty"
    res = {"kind": kind}
    if len(stat) == 1 and kind != "dirty":
        a, b = stat[0]
        bits, pR, origin = list_form(r0, lo, T, a, b)
        res["wall_out"] = (bits, pR, origin - wall_x)
    if kind in ("reflect", "pass"):
        # movers as one row region at T + k, k < P; my canon = min list form
        P = 1
        for _, _, (num, den) in mov:
            P = np.lcm(P, den)            # period multiple of the speed denominator
        P = int(np.lcm(P, row_rec["head_out"]["p"]))
        forms = []
        h2 = hrun.HRun(row, org)
        for k in range(P):
            h2.goto(T + k)
            rk = h2.cells(lo, hi)
            dk = [d for d in vlib.defects(rk)]
            # movers = defects not at the stationary object's place
            mk = [d for d in dk if not (d["lo"] < b + 5 and d["hi"] > a - 5)]
            aa, bb = min(d["lo"] for d in mk), max(d["hi"] for d in mk)
            fb, fp, _ = list_form(rk, lo, T + k, aa, bb)
            forms.append((fb, fp))
        res["head_out_canon"] = min(forms)
    return res


def main(table, per_kind, seed=1):
    rows = [json.loads(l) for l in open(table)]
    by = {}
    for r in rows:
        by.setdefault(r["kind"], []).append(r)
    rnd = random.Random(seed)
    stats = Counter()
    bad = []
    for kind, rs in sorted(by.items()):
        if kind == "unsettled":
            continue
        for r in rnd.sample(rs, min(per_kind, len(rs))):
            m = check(r)
            ok = m["kind"] == kind
            if ok and "wall_out" in r:
                ok = (m["wall_out"] == (r["wall_out"]["bits"], r["wall_out"]["pR"], r["wall_out"]["dx"]))
            if ok and "head_out_canon" in r:
                ok = list(m["head_out_canon"]) == list(r["head_out_canon"])
            stats[(kind, ok)] += 1
            if not ok:
                bad.append((r["head_i"], r["wall_j"], kind, m))
    print(dict(stats))
    for b in bad[:10]:
        print("MISMATCH", b)
    return stats, bad


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1)
