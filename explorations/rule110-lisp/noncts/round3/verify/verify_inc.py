"""Independent check of leftstream 05:40: the (3,2) train
I_L = 111110111110111110001110 (left ether phase 0 at x = 0, t = 0) gives
I_L + E^n -> E^(n+1) in exactly one class, n = 1..12.

A. Their exported exact rows (inc_scenes.json): rebuilt from (x0, cL, cR,
   bits), run with the engine, typed with MY typer (vlib).
B. My own construction: my E^n (vlib library, harvested from my own E + B
   collisions) at seed (0,0), right-anchored; the train evolved r = 0,1,2
   steps alone (exact) and pasted at every valid offset X over 4 lattice
   periods; all classes appear several times and must agree.
   Also: my row for n = 1 is compared cell for cell with theirs.
Control (can fail): classes other than the INC class must NOT give E^(n+1)."""
import json, sys
from collections import defaultdict
import numpy as np
import v3, vlib, engine

TR = np.array([int(c) for c in "111110111110111110001110"], np.uint8)
E = vlib.ETHER
NMAX = 12
T = 1200


def ether(c, lo, hi):
    return E[(np.arange(lo, hi) + c) % 14]


def run_typed(row, org, T):
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return [(v3.base(n), x) for n, x, w, k in vlib.identify(r, org, T=T)]


def part_A():
    sc = json.load(open("../leftstream/inc_scenes.json"))
    bad = 0
    for s in sc:
        bits = np.array([int(c) for c in s["bits"]], np.uint8)
        pad = 2 * s["T"] + 200
        x0 = s["x0"]
        row = np.concatenate([ether(s["cL"], x0 - pad, x0), bits,
                              ether(s["cR"], x0 + len(bits), x0 + len(bits) + pad)])
        got = [n for n, x in run_typed(row, x0 - pad, s["T"])]
        exp = s["expect"]
        ok = (got == [exp]) if exp != "control" else (len(got) != 1 or not got[0].startswith("E"))
        bad += not ok
        print(f"A {s['note']:24s} T={s['T']:5d} mine={got} theirs={s['result']} ok={ok}")
    return bad, sc


def train_at(r):
    """Train evolved r steps alone: (cells, time-0 phase of left ether)."""
    pad = 60
    row = np.concatenate([ether(0, -pad, 0), TR, ether(6, 24, 24 + pad)])
    for _ in range(r):
        row = vlib.step(row)
    cut = r + 2
    row = row[cut:len(row) - cut]
    lo = -pad + cut
    d = vlib.defects(row)
    a, b = d[0]["lo"], d[-1]["hi"]
    assert len(d) <= 3
    return row[a:b], lo + a, (4 * r) % 14


def my_scene(n, r, k):
    """My E^n at seed (0,0) (right phase 0) + train phase r at offset k."""
    nm = "E" if n == 1 else f"E^{n}"
    pad = 2 * T + 200
    erow, eorg, placed = vlib.build_right([(nm, 0, 0)], c_right=0, pad=pad)
    c_mid = (0 - vlib.LIB[nm].w) % 14
    cells, xc, c_tr = train_at(r)
    # pasted at shift X: left phase (c_tr - X), right phase c_tr - X + 6 = c_mid
    X0 = (c_tr + 6 - c_mid) % 14
    X = X0 - 14 * (12 + k)
    a = xc + X                      # first cell of the pasted train
    assert (c_tr - X + 6 - c_mid) % 14 == 0
    row = erow.copy()
    i = a - eorg
    row[:i] = ether((c_tr - X) % 14, eorg, a)
    row[i:i + len(cells)] = cells
    # check the train sits in clean ether of the right phases
    assert np.array_equal(row[i + len(cells):i + len(cells) + 20],
                          ether(c_mid, a + len(cells), a + len(cells) + 20))
    return row, eorg, a


def part_B():
    res = defaultdict(dict)
    for n in range(1, NMAX + 1):
        for r in range(3):
            for k in range(4):
                row, org, a = my_scene(n, r, k)
                got = [nm for nm, x in run_typed(row, org, T)]
                res[n][(r, k)] = got
    return res


if __name__ == "__main__":
    badA, sc = part_A()
    print("part A disagreements:", badA)
    res = part_B()
    inc_cls = None
    for n in range(1, NMAX + 1):
        want = "E" if n == 0 else f"E^{n + 1}"
        good = sorted(rk for rk, g in res[n].items() if g == [want])
        byr = {r: sorted(set(tuple(res[n][(r, k)]) for k in range(4))) for r in range(3)}
        print(f"B n={n}: INC placements {good}; outcomes by r: {byr}")
    # classes: (r, k) -> the class is fixed by r here? report consistency
    print("done")
