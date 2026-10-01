"""Trace a leader variant (K's E2 replaced by E9 at placement k, off)."""
import sys
from splice import *
k, off, tape, T, dt = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
variant = sys.argv[6] if len(sys.argv) > 6 else "all"   # "all": every K modified; "first": only K[0]
m = Machine(tape, ["YNNNNN"], T, left_periods=8, right_periods=6)
K = [a for n, a, b in m.blocks if n == "K"]
o = m.origin
tiles = glider_tiles("E^9")
row = m.row
targets = K[:1] if variant == "first" else K[:5]
for Kx in reversed(targets):          # right to left keeps earlier positions valid
    for s, D in valid_shifts(400):
        if D < 0:
            continue
        new = replace_exact(row, o + Kx + 41, o + Kx + 72, [(tiles, k, off)], s, D)
        if new is not None:
            break
    row = new
    print("K", Kx, "shift", s, D)
# positions of later K's move with the shifts; recompute boundaries from the census instead
bounds = [1100] + K[:5]
for t, cs in trace(m, row, range(dt, T + 1, dt), 1100, K[5] + 300):
    print(t, [sum(1 for x, y, kk in cs if lo <= x < hi and kk == "E") for lo, hi in zip(bounds, bounds[1:])],
          " ".join(f"{kk}{x}" for x, y, kk in cs if kk != "E"))
