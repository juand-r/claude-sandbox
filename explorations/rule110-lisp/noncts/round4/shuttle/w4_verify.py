"""Exact check of a w4 record on long rods (no typer, so any length):
for rod E^N and class k (rod shifted by (k,-4k)), simulate T_end steps and
find the unit change d with  row(x) == bg(T_end + k, x - 4k)  left of the
rod's middle and  == bg(T_end + k - 5d, x - 4k - 2d)  right of it, with
pure ether (phase of X's right side) beyond, i.e. ONE clean rod, nothing
else, in the whole valid row. Reports d per class or None."""
import sys, json
sys.dont_write_bytecode = True
import numpy as np
from rod import ether_bit
from pert import BG
from frontsim import run_row


def check(rec, N, Tend=900, drange=range(-10, 20)):
    X = [int(c) for c in rec["X"]]
    x0, phiR = rec["x0"], rec["phiR"]
    bg = BG(N, Tend + 120, -3 * Tend - 600, 4 * N + 3 * Tend + 600)
    out = []
    for k in range(3):
        lo, hi = -2 * Tend - 300, x0 + len(X) + 2 * Tend + 300
        xs = np.arange(lo, hi)
        row = np.array([bg(k, x - 4 * k) if x < x0 else (X[x - x0] if x < x0 + len(X) else ether_bit(phiR, 0, x))
                        for x in xs], np.uint8)
        rT = run_row(row, Tend)
        a, b = lo + Tend + 5, hi - Tend - 5
        mid = bg.front(Tend + k) + 4 * k + bg.W // 2
        found = None
        left_ok = all(rT[x - lo] == bg(Tend + k, x - 4 * k) for x in range(a, mid))
        if left_ok:
            for d in drange:
                if all(rT[x - lo] == bg(Tend + k - 5 * d, x - 4 * k - 2 * d) for x in range(mid, b)):
                    found = d
                    break
        out.append(found)
    return out


if __name__ == "__main__":
    fn = sys.argv[1]
    Ns = [int(v) for v in sys.argv[2].split(",")]
    for l in open(fn):
        rec = json.loads(l)
        if "X" not in rec:
            continue
        # right ether phase must match: use N's with the same right phase
        print(rec["d"], {N: check(rec, N) for N in Ns}, rec["X"], flush=True)
