"""Drift switch (DS): R2's zero switches the GAP's drift on.

Layout:  [left stream: I_L^v2 Z_L] -> R2 = E^(v2+1) ... gap ... W = R1 = E^2
         <- [right stream: K uniform NOPs (GB4), rafast slot class c]
- v2 = 0: Z_L at R2's zero emits A to the right; A + E^2 -> E opens W
  (class-free, ledger r3 #8); every later NOP walks the zero window W
  right by 24.27 / 20.53 cells (catalog E+GB4), so the gap grows.
- v2 >= 1: no A; W stays E^2; NOPs on E^2 do nothing; gap constant.
The arrival time of A (set by Z_L's time tz) varies; the walk must depend
only on how many NOPs come after the arrival (delay-insensitivity).
Usage: python ds.py [--noca]
"""
from dl import *  # noqa
import sys

GAP = 1200


def scene(v2, tz, K=10, c=1, v1=1):
    items = r1_program("N" * K, [c] * K)
    sc = r1_scene(v1, items)
    pre = input_prefix(v1)
    r2 = ("E",) + place_left_of(pre, "E", -GAP, 0)
    ls = left_stream("i" * v2 + "z", r2[1:], t0=tz)
    T = 15 * (sc[-1][2] + 4000)
    return ls + [r2] + sc, T


def describe(state):
    return [(g[0], round(float(lat(g)), 2)) for g in sorted(state, key=lambda g: pos(g, 0))]


if __name__ == "__main__":
    do_ca = "--noca" not in sys.argv
    for c in (1, 2, 0):
        for v2 in (0, 1, 2):
            for tz in (2000, 20000, 40000, 60000):
                sc, T = scene(v2, tz, c=c)
                sim, err = run(sc, T)
                st = sim.state()
                line = f"c={c} v2={v2} tz={tz} glider={describe(st)} err={err}"
                if do_ca:
                    ok, prods = ca(sc, T)
                    line += f" ca_eq={sorted(prods) == sorted(st)}"
                print(line, flush=True)
