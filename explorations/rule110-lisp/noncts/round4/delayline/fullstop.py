"""Reverse drift switch END TO END (lead 00:16 item 1), exact CA.

Layout (left to right):
  [K copies of left train Q = lscan #499, 14*M cells apart, moving right]
  -> W_L = E (zero left window; walks +11.2 cells per packet)
  ... gap ~GAP ...
  R1 = E + v1 GB5's (round-2 input prefix) <- right program "T" (K3,
  coupler's GB1@(0,0)+GB3@(-18,30)) in its zero class 0.
v1 = 0: K3 passes R1's zero as B^3 (r3 ledger #31), which crosses the gap
  and closes W_L (E + B^3 -> E^4): the window stops walking.
v1 >= 1: K3 adds 3 to R1, nothing is sent; W_L walks with every packet.
The relative placement of Q and W_L is lstop.py's (class 1, train #499).
The whole left part is translated by d cells (d chosen for ether
compatibility; offset parameter `shift` (multiples of 14) varies the
B^3 arrival time).
Usage: python fullstop.py [K] [M] [GAP]"""
import sys
from lscan import right_of, LIB, CHAIN, TILE, VE, Fraction, HERE
import json, os
from dl import input_prefix, r1_program, r1_scene, ALIAS, ident, lat
from r110lib import build_row
from fastca import Window

ALIAS["T"] = "GB1@(0,0)+GB3@(-18,30)"
QI = 499
Q = [json.loads(l) for l in open(os.path.join(HERE, "lgate4.jsonl")) if json.loads(l)["i"] == QI][0]


def left_part(K, M):
    qs = [(Q["bits"], 0, Q["pR"], -14 * M * j) for j in range(K)]
    first = max(qs, key=lambda s: s[3])
    wl, seed = right_of("E", 1, first)
    return qs, wl, seed


def scene(v1, K=40, M=20, GAP=1200, shift=0):
    items = r1_program("T", [0])
    sc = r1_scene(v1, items)
    rstates = [LIB.gliders[n].state_at(t, x, 0) for n, t, x in sc]
    e0 = min(rstates, key=lambda s: s[3])
    qs, wl, seed = left_part(K, M)
    # translate the left part so that W_L's end is ~GAP left of R1's start
    want_end = e0[3] - GAP + 14 * shift
    d = want_end - (wl[3] + len(wl[0]))
    cR1 = (e0[1] - e0[3]) % TILE                     # abs phase left of R1
    cWL = (wl[2] - wl[3]) % TILE                     # abs phase right of W_L
    d += (cWL - d - cR1) % TILE                      # (cWL - d) = cR1 (mod 14)
    tr = lambda s: (s[0], s[1], s[2], s[3] + d)
    states = [tr(s) for s in qs] + [tr(wl)] + rstates
    wl_ref = Fraction(seed[1] + d) - VE * seed[0]    # unhit W_L intercept
    return states, wl_ref


def run(v1, K=40, M=20, GAP=1200, shift=0, T=None):
    states, ref = scene(v1, K, M, GAP, shift)
    row, x0 = build_row(states, pad=200)
    st = sorted(states, key=lambda s: s[3])
    w = Window(row, x0, (st[0][1] - st[0][3]) % TILE, (st[-1][2] - st[-1][3]) % TILE)
    T = T or int(15 * (states[-1][3] + 3000))
    w.run(T)
    ok, prods = ident(w)
    return ok, prods, ref


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    GAP = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    for v1 in (0, 1):
        ok, prods, ref = run(v1, K, M, GAP)
        print(f"v1={v1}:", ok, [(p[0], round(float(lat(p) - ref), 2)) if p[1] is not None else p for p in prods], flush=True)
