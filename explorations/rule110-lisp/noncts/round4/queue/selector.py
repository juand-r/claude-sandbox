"""Selector theory test. K's first Ebar (phase 18, tile at K0-25 at t_c =
6000; the cluster 'E-9') is crossed by the acceptor (it survives as E0) and
eaten by the rejector (flipping D1 <-> A^3). Copies of it at V-equivalent
placements (same phase, x - 56 i) should behave the same. Open a gap
(0, D) at K0-20 (machine symmetry for D = 0 mod 56), put N copies at
x = -25 + 56 i (i = 1..N) and run stage A (answer prepares K) and stage B
(next read) for both paths; compare with the gap-only control.
Theory: N = 8 -> acceptor shift 8*7 = 56 = 0, rejector flips 8 times ->
both paths standard, 8 extra E0-like Ebars after an accept.
    python selector.py N [D]"""
import sys, json
import numpy as np
from create2 import *
N = int(sys.argv[1]); D = int(sys.argv[2]) if len(sys.argv) > 2 else 56 * (N + 2)
E = ebar_tiles()
rej = Path(D, "NYYN", ("NYYN", "NNYY"), -345)
acc = Path(D, "YYNN", ("YYNN", "YNYN"), -200)
items = [(E, 18, 31 + 63 * j) for j in range(N)]   # each copy +7 for the acceptor shift
for P_, name in ((rej, "rej"), (acc, "acc")):
    dR0, full0 = P_.stageA([])
    print(name, "control stageA", dR0, "stageB", P_.stageB(full0), flush=True)
    sc, K0 = P_.scA, P_.K0
    seg = build_tight(P_.gA, sc, K0, items, -20, D - 30)
    if seg is None:
        print(name, "items do not fit"); continue
    w = sc.run(seg, TA)
    full = unpack(step_packed_n(pack(seg), TA), len(seg))
    split = (K0 + D - 20) - (K0 - 1500)
    from census import census, MAX_DT
    def cens(s):
        w_ = pack(s); w_ = step_packed_n(w_, TA - MAX_DT); rows = []
        for j in range(MAX_DT + 1):
            c = unpack(w_, len(s)); i = sc.ebar_to_seg(K0 - 300, TC + TA)
            rows.append(c[i:i + D + 500]); w_ = step_packed_n(w_, 1)
        return [f"{k}{a - 300}" for a, b, k in census(np.array(rows))]
    print(name, "N =", N, "stageA right-part diffs", int((w[split:] != P_.refA[split:]).sum()),
          "left-part diffs", int((w[:split] != P_.refA[:split]).sum()))
    print("   control census", cens(P_.gA))
    print("   selector census", cens(seg))
    print(name, "stageB", P_.stageB(full), flush=True)
