"""Check delayline 00:15: (a) a uniform left stream of train Q = #499
(A-lattice, charge 0, copies 84 cells apart) walks a zero window E by
+11.2 cells per packet (in one E class); (b) a B^3 arriving at the
window's back closes it (E + B^3 -> E^4) and the window then stays put
under the remaining packets; final lone E^4 whose place grows with the
arrival time (11.6 + 11.2 k). Control: without B^3 the window keeps walking.

My construction: Q registered in my library from its cells (period (3,2)
checked by vlib.register), E from my library, B^3 from the collider
definition (clib.ensure, period re-found). Scene built by vlib.build, run
with hrun, read with my typer; the window's worldline intercept is read
against an E-alone (or E^4-alone) run in the same phase."""
import sys
from fractions import Fraction

import numpy as np

import clib
import hrun

vlib = hrun.vlib
QBITS = "100110100110111000100110111000"   # delayline/lgate4.jsonl i = 499, pR = 0
K = 10


def reg_q():
    core = np.array([int(c) for c in QBITS], np.uint8)
    left = vlib.ETHER[np.arange(-56, 0) % 14]
    right = vlib.ETHER[np.arange(len(core), len(core) + 56) % 14]
    vlib.register("Q499", np.concatenate([left, core, right]), (3, 2))


def intercept(name, x, T, cache={}):
    """worldline intercept (cells at t = 0) of a (15,-4) object `name@s` seen
    at x at time T, relative to the same object built at x0 = 0, t0 = 0."""
    base = name.split("@")[0]
    for a in range(15):
        key = (base, T + a)
        if key not in cache:
            row, org, _ = vlib.build([(base, 0, 0)], pad=300)
            h = hrun.HRun(row, org)
            h.goto(T + a)
            cache[key] = h.objects(org - T - 400, org + len(row) + T + 400)[0]
        n, xa, _ = cache[key]
        if n == name:
            return Fraction(x - xa) - Fraction(4 * a, 15)
    raise AssertionError(name)


def run(tE, xE, b3=None, T=12000):
    items = [("Q499", 0, -84 * j) for j in range(K)][::-1] + [("E", tE, xE)]
    if b3 is not None:
        items.append(("B^3", 0, xE + b3))
    row, org, placed = vlib.build(items, pad=400)
    h = hrun.HRun(row, org)
    h.goto(T)
    objs = h.objects(org - T - 400, org + len(row) + T + 400)
    rods = [(n, x) for n, x, w in objs if n.split("@")[0] in ("E", "E^4")]
    others = [n.split("@")[0] for n, x, w in objs if n.split("@")[0] not in ("E", "E^4")]
    return rods, others, placed


def shift(rods, placed, T):
    n, x = rods[0]
    tE, xE = placed[K][1], placed[K][2]
    return intercept(n, x, T) - (xE + Fraction(4 * tE, 15))


if __name__ == "__main__":
    reg_q()
    clib.ensure("B^3")
    T = 12000
    # (a) E seed time 0..14 (3 classes vs the stream), 10 packets, no B^3
    for tE in range(0, 15):
        rods, others, placed = run(tE, 150)
        assert len(rods) == 1 and not others, (rods, others)
        print(f"(a) E seed t={tE} (class {tE % 3}): lone {rods[0][0].split('@')[0]}, "
              f"window moved {float(shift(rods, placed, T)):+.2f} cells", flush=True)
    # (b) class 1 (t = 1), B^3 started b cells right of the window's seed
    res = {}
    for b in range(60, 700, 10):
        rods, others, placed = run(1, 150, b3=b)
        if len(rods) == 1 and not others:
            key = (rods[0][0].split("@")[0], round(float(shift(rods, placed, T)), 2))
        else:
            key = ("debris", tuple(n for n, x in rods) + tuple(others))
        res.setdefault(key, []).append(b)
    for k, v in sorted(res.items(), key=lambda kv: str(kv[0])):
        print("(b)", k, "for B^3 start offsets", v[:6], "..." if len(v) > 6 else "", f"({len(v)})")
    # (c) control: same, the window keeps walking under 20 packets without B^3
