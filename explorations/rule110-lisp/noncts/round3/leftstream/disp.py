"""Displacement bookkeeping for the E^n counter.

Reference: E^n built from an E seed e0 by (n-1) B's arriving from the right
(B's extend E^n at its back; scholar/collider: the front stays on E's
trajectory). ref(e0, n) = seed of that E^n.  For an operation that turns a
counter E^n (built from e0) into E^m with seed r, the displacement is
    disp = r - ref(e0, m)   reduced modulo P_E = (15, -4) to 0 <= dt < 15.
cls(v) = class of an ether-lattice vector v modulo M = <P_A, P_E> (Z_3):
the collision class of a following A-speed packet changes by cls(disp).
"""
from functools import lru_cache
from lsl import run, snap, En, nval

PE = (15, -4)
PA = (3, 2)


def red(v):
    """Reduce (dt, dx) modulo P_E to 0 <= dt < 15."""
    q, r = divmod(v[0], PE[0])
    return (r, v[1] - q * PE[1])


def cls(v):
    """Key change f(v) mod 42, f(dt, dx) = 2 dt - 3 dx. f vanishes on
    P_A = (3,2) and f(P_E) = 42, so for an A-speed packet at p and a counter
    with virtual front e, f(p - e) mod 42 is the collision key; a counter
    displaced by v changes every later packet's key by -f(v)."""
    return (2 * v[0] - 3 * v[1]) % 42


@lru_cache(maxsize=None)
def ref(e0, n, bgap=40):
    """Seed of E^n built from E at seed e0 = (t0, x0) by n-1 B's."""
    pl = [("E",) + tuple(e0)]
    x = e0[1] + 30
    for i in range(n - 1):
        x = snap(pl, "B", 0, x)
        pl.append(("B", 0, x))
        x += bgap
    T = 200 + 220 * n
    ok, out = run(pl, T)
    assert ok and len(out) == 1 and nval(out[0][0]) == n, out
    return out[0][1:]


def disp(e0, m, seed):
    r = ref(e0, m)
    return red((seed[0] - r[0], seed[1] - r[1]))
