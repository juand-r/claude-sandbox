"""SAT (own scene model on synth's r110sat.Spacetime): can something arriving
at the BACK of an E^n rod launch a phase domain (a right-to-left wall) deep
into the rod?

Initial row: ether(c_left) | E^n (library phase 0, built by objlib) | free
region. Two modes:
  --overlap K : the free region starts K cells INSIDE the rod's back and is
                unconstrained (positive control: the influence cone says a
                wall can be launched from inside; must be SAT).
  train mode  : ether gap then a free train Y of period (p, d), width WY,
                (its own isolated spacetime, period-checked, as in synth's
                TrainVar), placed at time phase tau.
Right of the free region: ether of a solver-chosen phase.
Target at T2: the rod segment [back-DEPTH-20, back-DEPTH) (back = back of the
undisturbed rod at T2) equals the E-bg in a phase other than the undisturbed
one. Solutions are re-simulated (whole modelled spacetime).
Usage: python3 launch2.py n T2 DEPTH out [--overlap K WF] [--train p d WY gap tau]
"""
import argparse
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "synth")))
from r110sat import CNF, Spacetime, TILE, ether_bit, neg, make_window   # noqa
import objlib as O   # noqa
import cone          # noqa

EBG = cone.Background(O.EBG)
WIN_VR = float(os.environ.get('WIN_VR', str(-4 / 15)))   # window right-edge speed (2/3 lets A debris leave)
SEG = 20


def rod_row(n):
    b, l, r = O.en_bits(n)
    # place bits at column 0: left absolute phase = l, right = r
    return b, l % 14, r % 14


def build(n, T2, depth, overlap=None, train=None, window_margin=None, target='wall'):
    b, cl, cr = rod_row(n)
    W = len(b)
    cnf = CNF()
    init = {}
    Ycnf = None
    if overlap is not None:
        K, WF = overlap
        xa = W - K
        for x in range(0, xa):
            init[x] = bool(int(b[x]))
        hi = xa + WF
        lo = 0
        # free cells [xa, hi): fresh vars (Spacetime creates them)
    else:
        p, d, WY, gap, tau, pR = train

        from react import TrainVar
        # Y canonical: left ether my-phase 0, right my-phase pR (solver-free:
        # we loop pR outside); here pR given via train tuple length 6

        Y = TrainVar(cnf, WY, p, d, pR, name="Y")
        # piece (Y, tau, xg): left ether my-phase (4 tau - xg) must equal the
        # rod's right absolute phase cr (as my-phase at t=0: ETHER[(c + x)])
        xg = W + gap
        while (4 * tau - xg - cr) % TILE:
            xg += 1
        for x in range(0, W):
            init[x] = bool(int(b[x]))
        for x in range(W, xg - tau):
            init[x] = bool(ether_bit(cr, 0, x))
        for x in range(xg - tau, xg + WY + tau):
            init[x] = Y.st.lit(tau, x - xg)
        lo, hi = 0, xg + WY + tau
        Ycnf = (Y, tau, xg, pR)
    right_phase = None if overlap is not None else (4 * Ycnf[1] + Ycnf[3] - Ycnf[2]) % TILE
    win = None
    if window_margin is not None:
        win = make_window(T2, lo, hi, -0.6, WIN_VR, margin=window_margin)
    st = Spacetime(cnf, T2, lo, hi, cl, right_phase, init=init, window=win)
    # undisturbed rod at T2
    seg_len = W + 2 * T2 + 60
    row = np.concatenate([O.ether(cl, -2 * T2 - 60, 0), np.array([int(c) for c in b], np.uint8),
                          O.ether(cr, W, W + T2 + 30)])
    rT = O.evolve(row, T2)      # covers [-T2 - 60, W + 30)
    x0T = -T2 - 60
    nonE = [x for x in range(x0T, x0T + len(rT)) if rT[x - x0T] != O.ether(cr, x, x + 1)[0]
            and x > 0]
    # ether phase advances 4 per step: absolute phase at time T2 is cr + 4 T2
    crT = (cr + 4 * T2) % 14
    nonE = [x for x in range(x0T, x0T + len(rT)) if rT[x - x0T] != O.ether(crT, x, x + 1)[0]]
    back = max(nonE) + 1
    seg_lo, seg_hi = back - depth - SEG, back - depth
    und = [int(rT[x - x0T]) for x in range(seg_lo, seg_hi)]
    cands = []
    for tt in range(EBG.tper):
        rr = EBG.row_at(tt)
        for sh in range(EBG.p):
            pat = [int(rr[(x - sh) % EBG.p]) for x in range(seg_lo, seg_hi)]
            if pat not in cands:
                cands.append(pat)
    if target == "extend":
        # control target: the 10 cells right of the undisturbed back are E-bg
        # (any phase): the rod has grown by >= 10 cells at the back
        seg_lo, seg_hi = back, back + 10
        others = []
        for tt in range(EBG.tper):
            rr = EBG.row_at(tt)
            for sh in range(EBG.p):
                pat = [int(rr[(x - sh) % EBG.p]) for x in range(seg_lo, seg_hi)]
                if pat not in others:
                    others.append(pat)
    else:
        assert und in cands, "undisturbed segment not E-bg"
        others = [c for c in cands if c != und]
    inds = []
    for pat in others:
        m = cnf.new_var()
        for x, bit in zip(range(seg_lo, seg_hi), pat):
            l = st.lit(T2, x)
            cnf.add([-m, l if bit else neg(l)])
        inds.append(m)
    cnf.add(inds)
    return cnf, st, (seg_lo, seg_hi, back, len(others)), Ycnf


def check(st, sol, T2):
    lo, hi = st.lo, st.hi
    row0 = np.array([sol.val(st.lit(0, x)) for x in range(lo, hi)], np.uint8)
    pad = 2 * T2 + 40
    rp = st.value_right_phase(sol)
    full = np.concatenate([O.ether(st.left_phase, lo - pad, lo), row0, O.ether(rp, hi, hi + pad)])
    h = O.history(full, T2)
    for t in range(T2 + 1):
        L, R = st.bounds[t]
        xs0 = lo - pad + t
        for x in range(L, R):
            if h[t][x - xs0] != sol.val(st.lit(t, x)):
                return False, full, lo - pad
    return True, full, lo - pad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("T2", type=int)
    ap.add_argument("depth", type=int)
    ap.add_argument("out")
    ap.add_argument("--overlap", nargs=2, type=int, default=None)
    ap.add_argument("--train", nargs=4, type=int, default=None, help="p d WY gap")
    ap.add_argument("--taus", default=None)
    ap.add_argument("--classes", action="store_true", help="one tau per collision class (vs the rod, lattice <(15,-4),(p,d)>)")
    ap.add_argument("--pRs", default=None)
    ap.add_argument("--win", type=int, default=None)
    ap.add_argument("--target", default="wall")
    A = ap.parse_args()
    jobs = []
    if A.overlap:
        jobs = [dict(overlap=tuple(A.overlap))]
    else:
        p, d, WY, gap = A.train
        taus = range(p) if A.taus is None else [int(v) for v in A.taus.split(",")]
        if A.classes:
            from classes import same_class
            b_, cl_, cr_ = rod_row(A.n)
            reps = []
            for tau in range(p):
                xg = len(b_) + gap
                while (4 * tau - xg - cr_) % TILE:
                    xg += 1
                o = (-tau, xg)
                if not any(same_class(o, r, (15, -4), (p, d)) for r in reps):
                    reps.append(o)
            taus = [-o[0] for o in reps]
            print("class representatives (tau):", taus, flush=True)
        pRs = range(TILE) if A.pRs is None else [int(v) for v in A.pRs.split(",")]
        jobs = [dict(train=(p, d, WY, gap, tau, pR)) for tau in taus for pR in pRs]
    for job in jobs:
        t0 = time.time()
        cnf, st, info, Yinfo = build(A.n, A.T2, A.depth, window_margin=A.win, target=A.target, **job)
        sol = cnf.solve()
        rec = {"n": A.n, "T2": A.T2, "depth": A.depth, "win": A.win, "target": A.target, **{k: list(v) for k, v in job.items()},
               "sat": sol is not None, "secs": round(time.time() - t0, 1), "nphases": info[3]}
        if sol is not None:
            ok, full, x_lo = check(st, sol, A.T2)
            rec["sim_ok"] = ok
            rec["full"] = "".join(map(str, full))
            rec["x_lo"] = x_lo
            assert ok, "SAT/sim mismatch"
        print(json.dumps({k: v for k, v in rec.items() if k != "full"}), flush=True)
        with open(A.out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
