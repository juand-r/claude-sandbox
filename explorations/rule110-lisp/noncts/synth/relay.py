"""Relay search (architect's spec R).

Find a left-moving packet P (free (p, d)-train, e.g. (30,-8) = Ebar speed)
such that, for a stationary cell O0 (default C2) and one class k of P
against O0:
  X1 (idle):   O0 + P          -> O0 + P            (clean crossing)
  X2 (relay):  A + O0, then P  -> O0 + P + A        (A released to the right)
with the cell left in the SAME place and phase in X1 and X2 (so the cell
is fully transparent: later packets see no difference), and P leaving on
the same trajectory in both. Optionally P may be consumed in X2
(--consume).

A + O0 happens in one class only (A vs any period-7 object), and the
resulting O1 (C1 for O0 = C2) sits at a position independent of the A's
arrival time, so one placement of A covers all cases.

Usage: python relay.py WP p d k T2 [--consume] [--cell C2] [--pR list]
"""

import argparse
import json
import time

from lib import load_gliders
from r110sat import CNF, TILE
from react import ObjectVar, TrainVar, fixed_from_glider
from scene import Scene

G = load_gliders()
# X2 pre-roll: A + C2 settles by t = 26 (measured); PRE >= 30, multiple of 7


def placements_right(item_w, x_min, p_right_of_left, p_train, n, span=60):
    """(tau, x) placements of a train (period p_train) right of an object
    whose right ether phase is p_right_of_left, with x - tau >= x_min,
    one per class k = (x / 2) mod n (relative to the first valid
    placement), preferring small tau (narrow light cone at t = 0)."""
    cands = []
    for x in range(x_min, x_min + span):
        for tau in range(p_train):
            if (4 * tau - x - p_right_of_left) % TILE or x - tau < x_min:
                continue
            cands.append((tau, x))
    base = min(x for _, x in cands)
    out = {}
    # prefer tau <= 6 (narrow cone), then the smallest x
    for tau, x in sorted(cands, key=lambda c: (c[0] > 6, c[1], c[0])):
        k = ((x - base) // 2) % n
        if k not in out:
            out[k] = (tau, x)
    if len(out) != n:
        raise ValueError("not all classes placed")
    return out


def preroll(tauP, p, min_pre=30, max_tau=6):
    """Smallest PRE = 7m >= min_pre with (tauP - PRE) mod p <= max_tau."""
    for m in range(-(-min_pre // 7), 200):
        if (tauP - 7 * m) % p <= max_tau:
            return 7 * m
    raise ValueError("no pre-roll")


def build(WP, p, d, pRP, k, T2, consume=False, cell="C2", gap=4, nclass=4,
          only_x2=False):
    cnf = CNF()
    if cell.startswith("free"):
        # free stationary cell: "free:W:pR"
        _, w, pr = cell.split(":")
        O0 = ObjectVar(cnf, int(w), int(pr), name="O0")
    else:
        O0 = fixed_from_glider(cnf, G[cell], 16)
    A = fixed_from_glider(cnf, G["A"], 8)
    P = TrainVar(cnf, WP, p, d, pRP, name="P")
    pl = placements_right(WP, O0.W + gap, O0.pR, p, nclass)
    if k not in pl:
        raise ValueError("class not available")
    tauP, xP = pl[k]
    # A left of O0: right phase 4 tau + pR_A - x == 0
    xA = None
    for x in range(-gap - A.W - 20, -gap - A.W + 1):
        if (A.pR - x) % TILE == 0:
            xA = x
    T = T2
    X1 = Scene(cnf, T, [(O0, 0, 0), (P, tauP, xP)], name="X1")
    # X2 starts PRE generations earlier (a multiple of 7, so the cell is in
    # the same phase), with A placed so that A + O0 has fully settled
    # (C2: by t = 26) long before P arrives; P is placed at its X1-time
    # -PRE configuration, so it follows the same trajectory as in X1.
    PRE = preroll(tauP, p)
    q, tau2 = divmod(tauP - PRE, p)
    # Tr(qp + tau2, z) = Tr(tau2, z - q d)  ->  piece (tau2, xP + q d)
    x2 = xP + q * d
    X2 = Scene(cnf, T + PRE, [(A, 0, xA), (O0, 0, 0), (P, tau2, x2)], name="X2")
    a, b = -10, O0.W + 10
    TT = T2 + PRE
    if only_x2:
        # diagnostic: the relay reaction alone (no idle-crossing scene,
        # no ties): A + O0, then P -> O0 (anywhere) + (P | nothing) + A
        if consume:
            X2.ether(TT, X2.lo - TT, a, X2.p_left)
        else:
            X2.is_item(TT, X2.lo - TT, a, P, far_left=X2.p_left)
        X2.is_item(TT, a, b, O0)
        X2.is_item(TT, b, X2.hi + TT, A, far_right=X2.p_right)
        return cnf, P, X1, X2
    # X1: P left, O0 middle, ether right
    X1.is_item(T2, X1.lo - T2, a, P, far_left=X1.p_left)
    X1.is_item(T2, a, b, O0)
    X1.ether(T2, b, X1.hi + T2, X1.p_right)
    # X2 (at its time T2 + PRE = X1 time T2): P (or ether) left, same
    # middle, A right
    if consume:
        X2.ether(TT, X2.lo - TT, a, X2.p_left)
    else:
        X2.is_item(TT, X2.lo - TT, a, P, far_left=X2.p_left)
        X2.tie(X1, TT, X1.lo - T2, a, t2=T2)
    X2.tie(X1, TT, a, b, t2=T2)
    X2.is_item(TT, b, X2.hi + TT, A, far_right=X2.p_right)
    return cnf, P, X1, X2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("WP", type=int)
    ap.add_argument("p", type=int)
    ap.add_argument("d", type=int)
    ap.add_argument("T2", type=int)
    ap.add_argument("--k", default="0,1,2,3")
    ap.add_argument("--pR", default=",".join(map(str, range(TILE))))
    ap.add_argument("--consume", action="store_true")
    ap.add_argument("--cell", default="C2")
    ap.add_argument("--only-x2", action="store_true")
    args = ap.parse_args()
    for k in map(int, args.k.split(",")):
        for pRP in map(int, args.pR.split(",")):
            t = time.time()
            cnf, P, X1, X2 = build(args.WP, args.p, args.d, pRP, k, args.T2,
                                   args.consume, args.cell,
                                   only_x2=args.only_x2)
            sol = cnf.solve()
            rec = {"WP": args.WP, "p": args.p, "d": args.d, "k": k,
                   "pRP": pRP, "T2": args.T2, "consume": args.consume,
                   "cell": args.cell, "only_x2": args.only_x2,
                   "sat": sol is not None,
                   "vars": cnf.nvars, "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["P"] = "".join(map(str, P.decode(sol)))
                rec["O0"] = "".join(map(str, X1.row(sol, 0, 0, 16 if not args.cell.startswith("free") else int(args.cell.split(":")[1]))))
                rec["X1_sim"] = True if args.only_x2 else X1.check_sat_vs_sim(sol)
                rec["X2_sim"] = X2.check_sat_vs_sim(sol)
                rec["X2_row0"] = "".join(map(str, X2.row(sol, 0)))
                rec["X2_lo"], rec["X2_pl"], rec["X2_pr"] = X2.lo, X2.p_left, X2.p_right
                if not (rec["X1_sim"] and rec["X2_sim"]):
                    raise AssertionError("SAT model disagrees with simulation")
            print(json.dumps({k2: v for k2, v in rec.items() if k2 != "X2_row0"}),
                  flush=True)
            with open("relay_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")


if __name__ == "__main__":
    main()
