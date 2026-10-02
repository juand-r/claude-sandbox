"""Bouncer reflection graph from bounce.py tables.

Canonical forms (time-phase and translation independent):
  train/object = min over t in [0, P) of (trimmed bits at time t, right
  ether phase - left ether phase), where P = lcm of member periods.
Outgoing heads/walls in the tables are rebuilt from their library keys
(re-identified in this process) and rendered from their seeds.
Edges: R: (head, wall) -> (wall', head' moving left); L: (head, wall) ->
(wall', head' moving right). A perpetual bouncer = a cycle of states
(dir, head, left wall, right wall) in which every step is a clean
reflection (exactly one stationary product + a head on one lattice)."""
import sys, json, math
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
from rod import TILE, ether_bit, simulate
from frontsim import lib
from collide import products_of


def canon_row(row, x0, t, P, p_left=None):
    """canonical form of the single train in `row` (time t)."""
    h = simulate(row, P)
    best = None
    for k in range(P):
        r = h[k]
        n = len(r)
        # left/right ether phases at time t + k
        xs = np.arange(x0, x0 + n)
        e0 = P + 10
        pl = next(q for q in range(TILE) if all(r[i] == ether_bit(q, t + k, x0 + i) for i in range(e0, e0 + 14)))
        pr = next(q for q in range(TILE) if all(r[i] == ether_bit(q, t + k, x0 + i) for i in range(n - e0 - 14, n - e0)))
        le = np.array([ether_bit(pl, t + k, x) for x in xs])
        re = np.array([ether_bit(pr, t + k, x) for x in xs])
        dl = np.nonzero(r[P + 5:n - P - 5] != le[P + 5:n - P - 5])[0]
        dr = np.nonzero(r[P + 5:n - P - 5] != re[P + 5:n - P - 5])[0]
        if len(dl) == 0:
            return ("", 0)
        a, b = dl[0] + P + 5, dr[-1] + P + 6
        # frame form (as trains.py lists): left ether phase 0, first
        # differing cell at frame column phi in [0, 14), trimmed right.
        phi = (x0 + a + 4 * (t + k) + pl) % TILE
        ETH = "11111000100110"
        key = (ETH[:phi] + "".join(map(str, r[a:b])), (pr - pl) % TILE)
        if best is None or key < best:
            best = key
    return best


def canon_bits(bits, pR, P):
    W = len(bits)
    pad = 3 * P + 80
    row = np.array([ether_bit(0, 0, x) if x < 0 else (int(bits[x]) if x < W else ether_bit(pR, 0, x))
                    for x in range(-pad, W + pad)], np.uint8)
    return canon_row(row, -pad, 0, P)


def render(members, t):
    """row at time t of objects given as (name, t0, x0) in this process's LIB."""
    L = lib()
    sts = []
    for nm, t0, x0 in members:
        g = L.gliders[nm]
        sts.append(g.state_at(t0, x0, t))
    sts.sort(key=lambda s: s[3])
    lo = sts[0][3] - 300 - 3 * 42
    hi = sts[-1][3] + len(sts[-1][0]) + 300 + 3 * 42
    # compose (collider convention: cells y < s read ETHER[(lph + y - s) % 14])
    from r110lib import ETHER
    E = [int(c) for c in ETHER]
    row = np.zeros(hi - lo, np.uint8)
    b0, l0, r0, s0 = sts[0]
    for y in range(lo, s0):
        row[y - lo] = E[(l0 + y - s0) % TILE]
    for i, (b, l, r, s) in enumerate(sts):
        for k, c in enumerate(b):
            row[s + k - lo] = int(c)
        end = sts[i + 1][3] if i + 1 < len(sts) else hi
        for y in range(s + len(b), end):
            row[y - lo] = E[(r + y - s - len(b) + len(b)) % TILE] if False else E[(r + y - s) % TILE]
    return row, lo


def name_of_key(key):
    L = lib()
    hit = L.identify((key[0], key[1], key[2]), auto=True)
    return hit[0] if hit else None


def head_canon(prods, t):
    """canonical form of the movers in prods (all same velocity)."""
    mem = [(name_of_key(p["key"]), p["t0"], p["x"]) for p in prods]
    P = 1
    for nm, _, _ in mem:
        P = P * lib().gliders[nm].p // math.gcd(P, lib().gliders[nm].p)
    row, lo = render(mem, 0)
    return canon_row(row, lo, 0, P)


def classify(rec, side):
    """-> ('refl', wall_prod, head_prods) / ('absorb', wall) / ('pass',..) / ('dirty',)"""
    if "err" in rec or not rec.get("ok", False):
        return ("dirty",)
    ps = rec["prods"]
    if any(p["name"] == "?" for p in ps):
        return ("dirty",)
    st = [p for p in ps if p["p"] == 7 and p["d"] == 0]
    movers = [p for p in ps if not (p["p"] == 7 and p["d"] == 0)]
    vel = {Fraction(p["d"], p["p"]) for p in movers}
    # all stationary products together form the new wall (the typer may
    # name two nearby C's as one compound or as two objects)
    if len(st) == 0:
        return ("dirty",)
    if not movers:
        return ("absorb", st)
    if len(vel) != 1:
        return ("dirty",)
    v = vel.pop()
    back = (v < 0) if side == "R" else (v > 0)
    return ("refl" if back else "pass", st, movers)


def load_canons():
    """canonical forms of enumerated heads and walls -> index."""
    import os
    out = {}
    for fn, P in (("heads_L.jsonl", 4), ("heads_R.jsonl", None), ("trains_7_0_20.jsonl", 7)):
        recs = [json.loads(l) for l in open(fn)]
        idx = {}
        for i, r in enumerate(recs):
            p = P or r["p"]
            idx.setdefault(canon_bits(r["bits"], r["pR"], p), i)
        out[fn] = (recs, idx)
    return out


def obj_canon(p):
    nm = name_of_key(p["key"])
    g = lib().gliders[nm]
    row, lo = render([(nm, p["t0"], p["x"])], 0)
    return canon_row(row, lo, 0, g.p)


def heads_canon(movers):
    return head_canon(movers, 0)


if __name__ == "__main__":
    import pickle, os
    C = load_canons()
    Lrecs, Lidx = C["heads_L.jsonl"]
    Rrecs, Ridx = C["heads_R.jsonl"]
    Wrecs, Widx = C["trains_7_0_20.jsonl"]
    print("canon sizes", len(Lidx), len(Ridx), len(Widx), flush=True)
    tables = {}
    stats = {}
    for side, fn in (("L", "bounce_L.jsonl"), ("R", "bounce_R.jsonl")):
        if not os.path.exists(fn):
            continue
        for l in open(fn):
            rec = json.loads(l)
            c = classify(rec, side)
            stats[(side, c[0])] = stats.get((side, c[0]), 0) + 1
            if c[0] != "refl":
                continue
            wc = obj_canon(c[1])
            hc = heads_canon(c[2])
            nxt_idx = Ridx if side == "L" else Lidx
            tables[(side, rec["i"], rec["j"])] = (Widx.get(wc), nxt_idx.get(hc), wc, hc,
                                                 [p["name"] for p in c[2]], c[1]["name"])
    print(stats, flush=True)
    pickle.dump(tables, open("bgraph_tables.pkl", "wb"))
    # summaries
    known = sum(1 for v in tables.values() if v[0] is not None and v[1] is not None)
    print("clean reflections", len(tables), "with known wall' and head'", known)
