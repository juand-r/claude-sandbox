"""W4 candidates: B-speed library packets X whose every class against E^m
gives E^(m+d_c) plus only A-family right-movers (from round-3 coupler's
scan_reflect_M4.jsonl, all 2,523 library left-movers vs E^4). Block =
X followed by k B's (k = max A count over classes; spacing 80) so the A's
are eaten (A + B -> nothing, single class) and surplus B's add to the rod.

A right stream = N blocks, block j at seed (t0 + j dT, d0 + j P). For each
dT (block-to-block time offset; dT mod 3 sets the class shift of the
stream) and each start class (t0 = 0, 1, 2), record the per-block value
changes over N blocks (rodval; None = not one clean rod).
Question: is there a block whose class dynamics has TWO persistent modes
(two start classes that never merge and have different drifts)? With a
single attractor, a phase shift of the back (a wall from the front) is
only a transient.
python3 w4_cands.py [N]"""
import sys

import clib
import hrun
import rodval

vlib = hrun.vlib
CANDS = {  # name: max number of A's emitted over the 3 classes (coupler scan, E^4)
    "Bbar": 5, "B_1_B_13_Bbar": 5, "Bbar_7_B": 4, "Bbar_0_B_17_B": 3, "B_1_B_4_B_15_Bbar": 5,
    "B_14_Bbar": 5, "Bbar_14_B": 4, "Bbar_0_B_20_B": 3, "Bbar_9_B": 4, "B_19_Bbar": 5,
    "B_11_Bbar": 5, "B_2_B_16_Bbar": 5, "Bbar_0_B_5_B_21_B": 2, "B_1_B_22_Bbar": 5,
    "B_2_B_2_B_33_Bbar": 5}
M0, P, D0, S = 20, 700, 60, 80


def stream(X, k, t0, dT, N):
    items = [(f"E^{15}", 0, 0)]
    for j in range(N):
        b = D0 + j * P
        items.append((X, t0 + j * dT, b))
        items += [("B", 0, b + 60 + S * (i + 1)) for i in range(k)]
    row, org, placed = vlib.build(items, pad=400)
    T = (D0 + N * P + 60 + S * k) * 30 // 7 + 1500
    return rodval.value(row, org, T)


def seq(X, k, t0, dT, N):
    vals = [15]
    for n in range(1, N + 1):
        v = stream(X, k, t0, dT, n)
        vals.append(v)
        if v is None:
            break
    return [None if (a is None or b is None) else b - a for a, b in zip(vals, vals[1:])]


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    names = sys.argv[2:] or list(CANDS)
    for X in names:
        if X not in vlib.LIB:
            clib.ensure(X)
        k = CANDS[X]
        for dT in range(3):
            rows = [seq(X, k, t0, dT, N) for t0 in (0, 1, 2)]
            tails = {tuple(r[-3:]) for r in rows if None not in r}
            print(f"{X} (+{k}B) dT={dT}: {rows}  distinct tails {len(tails)}", flush=True)
