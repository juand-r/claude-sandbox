"""SAT: can a free left-moving train Y, arriving at the BACK of an E_n rod,
launch a right-to-left domain wall into the rod?

Scene (synth's Scene/TrainVar/en_item, imported read-only): E_n at piece
(0, 0), Y (period (p, d), width WY, right ether phase s) right of it, one
placement per collision class. Target at time T2: a 20-cell segment of the
rod interior, DEPTH cells left of the undisturbed back, equals the E-bg in
some phase other than the undisturbed one (a phase domain that reached
DEPTH cells into the rod). With the rod moving at -4/15 and walls only at
-3/5, +2/5 and -4/15 (wallsat, W<=40), only a left wall (or something
wider/chaotic) can do this; every solution is re-simulated and classified.

Controls (same code path):
  --free   Y is unconstrained cells (no train condition): the cone says SAT.
Usage: python3 launch_sat.py n p d WY T2 DEPTH out.jsonl [--free] [--k K] [--s S]
"""
import argparse
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SYNTH = os.path.abspath(os.path.join(HERE, "..", "..", "synth"))
sys.path.insert(0, SYNTH)
from r110sat import CNF, TILE, make_window, neg   # noqa: E402
from react import TrainVar, ObjectVar             # noqa: E402
from scene import Scene                           # noqa: E402
from classes import placements_by_class, n_classes  # noqa: E402
from en import en_item                            # noqa: E402
import cone                                       # noqa: E402

EBG = cone.Background("1101011100")
SEG = 20


class FreeVar:
    """Unconstrained cells (control): canonical frame like TrainVar."""

    def __init__(self, cnf, W, pR, period):
        from r110sat import Spacetime
        self.cnf, self.W, self.pR, self.name = cnf, W, pR, "Free"
        self.period = period
        self.st = Spacetime(cnf, period[0], 0, W, 0, pR)

    def extent(self, tau):
        return (-tau, self.W + tau)


def build(n, p, d, WY, T2, depth, k, s, free=False):
    cnf = CNF()
    E = en_item(cnf, n)
    Y = FreeVar(cnf, WY, s, (p, d)) if free else TrainVar(cnf, WY, p, d, s, name="Y")
    tau, x = placements_by_class(E, (0, 0), Y, E.W + 6)[k]
    lo, hi = 0, x + Y.W + tau
    win = make_window(T2, lo, hi, d / p, -4 / 15, margin=24)
    S = Scene(cnf, T2, [(E, 0, 0), (Y, tau, x)], window=win)
    # undisturbed rod at T2, by forward simulation of E alone
    from r110sat import run_embedded, ether_bit
    h, hx0 = run_embedded(E.bits, 0, 0, E.pR, T2)
    rowT = h[T2]
    xs_all = range(-T2 - 20, E.W + 20)
    nonE = [xx for xx in xs_all if rowT[xx - hx0] != ether_bit(E.pR, T2, xx)]
    back = max(nonE) + 1
    seg_lo = back - depth - SEG
    seg_hi = back - depth
    und = [int(rowT[xx - hx0]) for xx in range(seg_lo, seg_hi)]
    # E-bg phases matching `und`: find bg alignment, then all 50 phases
    cand = []
    for tt in range(EBG.tper):
        rr = EBG.row_at(tt)
        for sh in range(EBG.p):
            pat = [int(rr[(xx - sh) % EBG.p]) for xx in range(seg_lo, seg_hi)]
            cand.append(pat)
    base = [c for c in cand if c == und]
    assert base, "undisturbed segment is not E-bg (depth too large?)"
    others = []
    for c in cand:
        if c != und and c not in others:
            others.append(c)
    inds = []
    for pat in others:
        m = cnf.new_var()
        for xx, b in zip(range(seg_lo, seg_hi), pat):
            l = S.lit(T2, xx)
            cnf.add([-m, l if b else neg(l)])
        inds.append(m)
    cnf.add(inds)
    return cnf, S, Y, (seg_lo, seg_hi), len(others), back


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for a in ("n", "p", "d", "WY", "T2", "depth"):
        ap.add_argument(a, type=int)
    ap.add_argument("out")
    ap.add_argument("--free", action="store_true")
    ap.add_argument("--k", default=None)
    ap.add_argument("--s", default=None)
    A = ap.parse_args()
    nc = n_classes((15, -4), (A.p, A.d))
    ks = range(nc) if A.k is None else [int(v) for v in A.k.split(",")]
    ss = range(TILE) if A.s is None else [int(v) for v in A.s.split(",")]
    for k in ks:
        for s in ss:
            t0 = time.time()
            cnf, S, Y, seg, nother, back = build(A.n, A.p, A.d, A.WY, A.T2, A.depth, k, s, A.free)
            sol = cnf.solve()
            rec = {"n": A.n, "p": A.p, "d": A.d, "WY": A.WY, "T2": A.T2,
                   "depth": A.depth, "k": k, "s": s, "free": A.free,
                   "sat": sol is not None, "secs": round(time.time() - t0, 1),
                   "nphases": nother}
            if sol is not None:
                ok = S.check_sat_vs_sim(sol)
                rec["sim_ok"] = ok
                rec["Y"] = "".join(map(str, Y.st.value_row(sol, 0, 0, Y.W))) if hasattr(Y.st, "value_row") else None
                rec["row0"] = "".join(map(str, S.row(sol, 0)))
                rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
                if not ok:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
            with open(A.out, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
