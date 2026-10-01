"""Exact Rule 110 verification of a FRONT-face record from pert.py, for a
range of rod sizes n: the scene  ether | X | gap | E^n  is simulated from
t = 0 and compared, at time T and T + M, with the expected outcome
Y (as found at time T, evolved in isolation) + E^(n-K) (the rod with its
front moved by K crystal units, back untouched).  Also checks that Y alone
is (pY, dY)-periodic and names it with collider's library."""
import sys
import json
sys.dont_write_bytecode = True
import numpy as np
from rod import TILE, ether_bit, simulate
from pert import BG

M = 300


def ident(row, x0, t):
    """collider names of the objects in a row (time t)."""
    import os
    COLL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "collider")
    sys.path.insert(0, os.path.abspath(COLL))
    from library import Library
    from collide import products_of
    LIB = Library.load()
    ok, prods, _ = products_of(LIB, row, x0, t)
    return ok, prods


def check_front(rec, ns, M=M, verbose=True):
    T, K = rec["T"], rec["K"]
    pY, dY = rec["py"]
    X = np.array([int(c) for c in rec["X"]], np.uint8)
    Ybits = np.array([int(c) for c in rec["Y"]], np.uint8)
    x0, phiL, LT = rec["x0"], rec["phiL"], rec["L_T"]
    yb = LT + len(Ybits)
    results = {}
    for n in ns:
        Ttot = T + M
        span_lo, span_hi = x0 - 2 * Ttot - 100, 4 * n + 2 * Ttot + 100
        bg = BG(n, Ttot + 10, span_lo, span_hi)
        xs = np.arange(span_lo, span_hi)
        row0 = np.array([ether_bit(phiL, 0, x) if x < x0 else
                         (X[x - x0] if x < x0 + len(X) else bg(0, x))
                         for x in xs], np.uint8)
        h = simulate(row0, Ttot)
        # expected at time T: ether(phiL) | Y | bg(T-5K, x-2K)
        mid = bg.front(T) + bg.W // 2      # front region shifted, back untouched
        exp = np.array([ether_bit(phiL, T, x) if x < LT else
                        (Ybits[x - LT] if x < yb else
                         (bg(T - 5 * K, x - 2 * K) if x < mid else bg(T, x)))
                        for x in xs], np.uint8)
        he = simulate(exp, M)
        a, b = Ttot + 50, len(xs) - Ttot - 50     # away from wrap seams
        okT = np.array_equal(h[T, a:b], exp[a:b])
        okM = np.array_equal(h[Ttot, a:b], he[M, a:b])
        results[n] = (okT, okM)
        if verbose:
            print(f"n={n}: match at T {okT}, at T+{M} {okM}")
    # isolated Y
    pr = None
    for p in range(TILE):
        if all(exp_val == ether_bit(p, T, x) for x, exp_val in
               zip(range(yb, yb + 14), [bg(T - 5 * K, x - 2 * K) for x in range(yb, yb + 14)])):
            pr = p
    lo, hi = LT - 600, yb + 600
    xs = np.arange(lo, hi)
    yrow = np.array([ether_bit(phiL, T, x) if x < LT else
                     (Ybits[x - LT] if x < yb else ether_bit(pr, T, x)) for x in xs], np.uint8)
    hy = simulate(yrow, 3 * pY)
    per = all(np.array_equal(hy[k * pY][200:-200], np.roll(hy[(k + 1) * pY], -dY)[200:-200])
              for k in range(2))
    ok, prods = ident(hy[3 * pY][300:-300], lo + 300, T + 3 * pY)
    return results, per, prods


if __name__ == "__main__":
    rec = json.loads(sys.argv[1]) if sys.argv[1].startswith("{") else \
        [json.loads(l) for l in open(sys.argv[1])][int(sys.argv[2])]
    ns = range(int(sys.argv[3]) if len(sys.argv) > 3 else 2, int(sys.argv[4]) if len(sys.argv) > 4 else 20)
    res, per, prods = check_front(rec, ns)
    print("Y periodic:", per, "Y =", prods)
