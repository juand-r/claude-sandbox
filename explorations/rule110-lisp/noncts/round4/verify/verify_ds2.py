"""My own variations of delayline's first drift-switch scene (c=2, v2=0,
tz=20000): keep only the first K of the 10 GB4 NOPs (K = 0..10) and also
remove the Z_L (no A: control). R1's worldline intercept at time 0 is read
by matching against an E-alone run in the same phase (as verify_window.py).
Expect: with Z_L, each kept NOP after the A's arrival walks R1 by 24.27 or
20.53 (alternating); without Z_L, R1 stays E^2 and never moves."""
from fractions import Fraction

import clib
import hrun
import xlate
from verify_ds import FIRST

vlib = hrun.vlib
T = FIRST["T"]


def r1_intercept(seeds):
    clib.ensure_scene(seeds)
    items, c0, same = xlate.check(seeds)
    assert same
    row, org, placed = vlib.build(items, c0=c0, pad=400)
    h = hrun.HRun(row, org)
    h.goto(T)
    objs = h.objects(org - T - 400, org + len(row) + T + 400)
    n1, x1, _ = objs[-1]
    # E-alone reference in my builder at the origin, same phase
    for a in range(15):
        (na, xa, _), = vlib_alone(n1.split("@")[0], T + a)
        if na == n1:
            return [n for n, x, w in objs], Fraction(x1 - xa) - Fraction(4 * a, 15) + Fraction(items[2][2])
    raise AssertionError


_cache = {}


def vlib_alone(name, t):
    if (name, t) not in _cache:
        row, org, _ = vlib.build([(name, 0, 0)], pad=400)
        h = hrun.HRun(row, org)
        h.goto(t)
        _cache[(name, t)] = h.objects(org - t - 400, org + len(row) + t + 400)
    return _cache[(name, t)]


if __name__ == "__main__":
    clib.register_auto("ZL")
    seeds = [tuple(s) for s in FIRST["seeds"]]
    prev = None
    for K in range(0, 11):
        sc = seeds[:4 + K]
        names, icpt = r1_intercept(sc)
        d = "" if prev is None else f" step {float(icpt - prev):+.2f}"
        print(f"K={K:2d} with Z_L: {names} R1 intercept {float(icpt):.2f}{d}", flush=True)
        prev = icpt
    for K in (0, 10):
        names, icpt = r1_intercept(seeds[1:4 + K])
        print(f"K={K:2d} control without Z_L: {names} R1 intercept {float(icpt):.2f}")
