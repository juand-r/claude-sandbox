"""Look at a cone witness: evolve it longer in the background and print
the deviation from the background (D = differs, . = same) in rod-ish frame."""
import sys
import numpy as np
import cone

tile, T, tau, x0, side, TT, step = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
bg = cone.Background(tile)
if side == "left":
    m = cone.ConeModel(bg, tau, x0, x0 + T, T)
else:
    m = cone.ConeModel(bg, tau, x0 - T + 1, x0 + 1, T)
x, row0 = m.extreme(side)
print("extreme", x, "rel", x - x0)
pad = 2 * TT + 50
lo = m.a - pad
full = np.array([m.bgbit(0, y) for y in range(lo, m.b + pad)], np.uint8)
full[m.a - lo:m.b - lo] = row0
rows = cone.simulate_window(full, TT)
for t in range(0, TT + 1, step):
    r = rows[t]
    xs = np.arange(lo + t, lo + t + len(r))
    bgr = np.array([bg.bit(tau + t, y) for y in xs], np.uint8)
    dev = r != bgr
    # window around x0 in a frame moving at -4/15 (rod)
    c = x0 + int(round(-4 * t / 15))
    w0, w1 = c - 110, c + 60
    s = "".join(("X" if r[y - xs[0]] else "o") if dev[y - xs[0]] else ("1" if r[y - xs[0]] else "_") for y in range(w0, w1))
    print(f"{t:5d} {s}")
