"""Cross-check fastca.Window against ../../engine.py on random ether
configurations with defects (cyclic row big enough that the wrap is never
reached)."""
import numpy as np
from common import engine
from fastca import Window, ether

rng = np.random.default_rng(1)
for trial in range(5):
    cL0 = int(rng.integers(14))
    W = 14 * 40
    x0 = 1000
    row = ether(cL0, x0, x0 + W).copy()
    row[200:260] = rng.integers(0, 2, 60)          # a random defect
    # right ether phase: same as left (row is ether outside the defect)
    T = 3000
    pad = 14 * 400
    big = np.concatenate([ether(cL0, x0 - pad, x0), row, ether(cL0, x0 + W, x0 + W + pad)])
    for _ in range(T):
        big = engine.step(big)
    w = Window(row, x0, cL0, cL0).run(T)
    lo, hi = x0 - pad + 50, x0 + W + pad - 50
    got = w.cells(lo, hi)
    ref = big[50:len(big) - 50]
    print(trial, "window", len(w.row), "agree:", np.array_equal(got, ref))

# negative control: one flipped cell must change the outcome
row = ether(3, 0, 14 * 30).copy()
row[100:140] = rng.integers(0, 2, 40)
a = Window(row, 0, 3, 3).run(1500).cells(-3000, 3000)
row2 = row.copy()
row2[120] ^= 1
b = Window(row2, 0, 3, 3).run(1500).cells(-3000, 3000)
print("control (flipped cell) differs:", not np.array_equal(a, b))
