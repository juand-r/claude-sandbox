"""Synthesis of stationary objects with a prescribed reaction:

    O + X  ->  O' + (Y_left on the left side) + (Y_right on the right side)

Unknown: a stationary object O = free cells on [0, W), my-phase 0 ether to
its left, my-phase pR to its right (looped over by the caller), period
(7, 0). Glider X (collider's library) arrives from the left if X.d > 0,
from the right if X.d < 0. At time T2 the row must be exactly:

    ether | Y_left (one of a list, any phase/position, or nothing)
          | O' = anything inside [-mL, W + mR) that is period-(7,0)
          | Y_right (one of a list, or nothing) | ether.

"nothing" = the side is pure ether at T2 (the far-side ether phases are
fixed by the light cone, so the near-side phases follow from the chosen
glider). O' may be empty (pure ether) or equal to O.

A and B have exactly one collision class with any period-7 object
(|det|/14 = 1), so X's placement is WLOG for them. For other X the
result holds for the one placement tried (seed at time-phase 0, gap).

Every SAT answer is re-simulated with ../../engine.py (`verify`).

CLI: python walls.py X W T2 LEFT RIGHT [pR,...]
     LEFT/RIGHT: comma list of glider names, or '-' for "nothing".
"""

import sys
import time

import numpy as np

from lib import load_gliders, place_after, compose, left_phase_of, right_phase_of
from r110sat import CNF, Spacetime, TILE, ether_bit, simulate

G = load_gliders()
PER = 7


def free_state(a, b, p_left, p_right):
    """Placeholder object state (t = 0) for free cells [a, b)."""
    return ("0" * (b - a), (p_left + a) % TILE, (p_right + a) % TILE, a)


def candidates_left_anchored(names, t, lo, hi, p_left, band=14):
    """Rows on [lo, hi) at time t: ether with my-phase p_left at lo, one
    glider from names inside [lo + band, hi - band) (so that both ends of
    the region are ether bands). -> [((name, t0, x0), cells)]."""
    out = []
    for n in names:
        Y = G[n]
        for k in range(Y.p):
            t0, x0 = place_after(Y, t, p_left, lo + band, k)
            while True:
                st = Y.state(t0, x0, t)
                if st[3] + len(st[0]) > hi - band:
                    break
                cells, _, _ = compose([st], t, lo, hi, left_p=p_left)
                out.append(((n, t0, x0), cells))
                x0 += TILE
    return out


def candidates_right_anchored(names, t, lo, hi, p_right):
    out = []
    for n in names:
        Y = G[n]
        pl = (p_right - Y.slip) % TILE
        out += candidates_left_anchored([n], t, lo, hi, pl)
    return out


def build(Xn, W, T2, left_out, right_out, pR, gap=6, mL=12, mR=12,
          cnf=None, shared=None):
    """Build the CNF. Returns a dict with everything needed to decode."""
    X = G[Xn]
    cnf = cnf or CNF()
    shared = shared or {x: cnf.new_var() for x in range(W)}
    # S1: O alone is stationary with period 7, and not pure ether
    s1 = Spacetime(cnf, PER, 0, W, 0, pR, init=shared)
    s1.periodic(0, PER, -PER, W + PER)
    if pR == 0:
        s1.differs(0, 0, W, [ether_bit(0, 0, x) for x in range(W)])
    # S2: O + X
    Ofree = free_state(0, W, 0, pR)
    if X.d > 0:
        pl = (0 - X.slip) % TILE
        t0, x0 = place_after(X, 0, pl, -gap - 60, 0)
        while True:
            nxt = X.state(t0, x0 + TILE, 0)
            if nxt[3] + len(nxt[0]) > -gap:
                break
            x0 += TILE
        sx = X.state(t0, x0, 0)
        states = [sx, Ofree]
        lo, hi = sx[3], W
        pfl, pfr = pl, pR
    else:
        t0, x0 = place_after(X, 0, pR, W + gap, 0)
        sx = X.state(t0, x0, 0)
        states = [Ofree, sx]
        lo, hi = 0, sx[3] + len(sx[0])
        pfl, pfr = 0, (pR + X.slip) % TILE
    cells, _, _ = compose(states, 0, lo, hi)
    init = {x: bool(cells[x - lo]) for x in range(lo, hi)}
    init.update(shared)
    T = T2 + PER
    s2 = Spacetime(cnf, T, lo, hi, pfl, pfr, init=init)
    a_, b_ = -mL, W + mR
    L, R = lo - T2, hi + T2
    # O' region: stationary between T2 and T2 + 7 (light cone shrinks)
    # candidates leave >= 14 ether cells next to [a_, b_), so O' embedded
    # in ether is exactly what is checked here
    s2.periodic(T2, T, a_ - PER, b_ + PER)
    sides = {}
    for side, names, (ylo, yhi) in (("L", left_out, (L, a_)),
                                    ("R", right_out, (b_, R))):
        if not names:
            if side == "L":
                s2.ether_on(T2, ylo, yhi, pfl)
            else:
                s2.ether_on(T2, ylo, yhi, pfr)
            sides[side] = None
            continue
        if side == "L":
            cands = candidates_left_anchored(names, T2, ylo, yhi, pfl)
        else:
            cands = candidates_right_anchored(names, T2, ylo, yhi, pfr)
        if not cands:
            raise ValueError(f"no output candidates fit on side {side}")
        inds = s2.one_of(T2, ylo, yhi, [c for _, c in cands])
        sides[side] = (cands, inds, ylo, yhi)
    return {"cnf": cnf, "s1": s1, "s2": s2, "shared": shared, "X": Xn,
            "W": W, "T2": T2, "pR": pR, "lo": lo, "hi": hi, "pl": pfl,
            "pr": pfr, "a_": a_, "b_": b_, "sides": sides,
            "left_out": left_out, "right_out": right_out}


def decode(m, sol):
    s1, s2, T2 = m["s1"], m["s2"], m["T2"]
    res = {k: m[k] for k in ("X", "W", "T2", "pR", "lo", "hi", "pl", "pr",
                             "a_", "b_")}
    res["O"] = "".join(map(str, s1.value_row(sol, 0, 0, m["W"])))
    res["row0"] = s2.value_row(sol, 0, m["lo"], m["hi"])
    res["rowT2"] = s2.value_row(sol, T2, m["lo"] - T2, m["hi"] + T2)
    res["Oprime"] = "".join(map(str, s2.value_row(sol, T2, m["a_"], m["b_"])))
    for side in ("L", "R"):
        sd = m["sides"][side]
        res["Y" + side] = None if sd is None else \
            [c[0] for c, i in zip(sd[0], sd[1]) if sol.val(i)][0]
    return res


def search(Xn, W, T2, left_out, right_out, pR, verbose=True, **kw):
    m = build(Xn, W, T2, left_out, right_out, pR, **kw)
    t = time.time()
    sol = m["cnf"].solve()
    if verbose:
        print(f"  X={Xn} W={W} pR={pR:2d} T2={T2} L={left_out or '-'} "
              f"R={right_out or '-'} vars={m['cnf'].nvars} "
              f"{'SAT' if sol else 'UNSAT'} [{time.time() - t:.1f}s]",
              flush=True)
    return None if sol is None else decode(m, sol)


def verify(res, extra=210):
    """Forward simulation with ../../engine.py. Checks: O alone is period
    (7,0); the SAT row at T2 equals simulation; at T2 + extra each output
    glider is exactly where its seed predicts and O' region is period 7."""
    W, pR, T2 = res["W"], res["pR"], res["T2"]
    O = np.array([int(c) for c in res["O"]], np.uint8)
    pad = 3 * (T2 + extra) + 60
    left = np.array([ether_bit(0, 0, x) for x in range(-pad, 0)], np.uint8)
    right = np.array([ether_bit(pR, 0, x) for x in range(W, W + pad)], np.uint8)
    h = simulate(np.concatenate([left, O, right]), 70)
    c = pad
    out = {"O_stationary": all(
        np.array_equal(h[t + 7, c - 20:c + W + 20], h[t, c - 20:c + W + 20])
        for t in range(63))}
    lo, hi, pl, pr = res["lo"], res["hi"], res["pl"], res["pr"]
    left = np.array([ether_bit(pl, 0, x) for x in range(lo - pad, lo)], np.uint8)
    right = np.array([ether_bit(pr, 0, x) for x in range(hi, hi + pad)], np.uint8)
    h2 = simulate(np.concatenate([left, res["row0"], right]), T2 + extra)
    off = pad - lo
    out["sat_matches_sim"] = np.array_equal(
        h2[T2, lo - T2 + off:hi + T2 + off], res["rowT2"])
    Tf = T2 + extra
    a_, b_ = res["a_"], res["b_"]
    out["Oprime_stationary"] = np.array_equal(h2[Tf, a_ + off:b_ + off],
                                              h2[Tf - 7, a_ + off:b_ + off])
    # region left of O' (and right of it) must be ether | Y | ether
    for side in ("L", "R"):
        y = res["Y" + side]
        if side == "L":
            lo2, hi2 = lo - Tf + 5, a_ - 5
            pfar = pl
        else:
            lo2, hi2 = b_ + 5, hi + Tf - 5
            pfar = None
        if y is None:
            st = []
        else:
            n, t0, x0 = y
            st = [G[n].state(t0, x0, Tf)]
        if side == "L":
            exp, _, _ = compose(st, Tf, lo2, hi2, left_p=pl)
        else:
            if st:
                exp, _, _ = compose(st, Tf, lo2, hi2)
            else:
                exp, _, _ = compose([], Tf, lo2, hi2, left_p=pr)
        out["side_" + side] = np.array_equal(h2[Tf, lo2 + off:hi2 + off], exp)
    out["ok"] = all(v for v in out.values())
    return out


def save(r, v, path="walls_results.jsonl"):
    import json
    rec = {k: (list(map(int, r[k])) if k in ("row0", "rowT2") else r[k])
           for k in r}
    rec["verify"] = {k: bool(v[k]) for k in v if k not in ("hist", "off")}
    with open(path, "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def names(arg):
    return [] if arg == "-" else arg.split(",")


if __name__ == "__main__":
    Xn, W, T2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    Ln, Rn = names(sys.argv[4]), names(sys.argv[5])
    pRs = [int(p) for p in sys.argv[6].split(",")] if len(sys.argv) > 6 \
        else range(TILE)
    for pR in pRs:
        r = search(Xn, W, T2, Ln, Rn, pR)
        if r:
            v = verify(r)
            print("   O =", r["O"], "YL =", r["YL"], "YR =", r["YR"],
                  "O' =", r["Oprime"], v)
            if not v["ok"]:
                raise AssertionError("verification failed")
            save(r, v)
