"""Identify K's first Ebar (tile phase k, tile start x rel K0) at t_c = 6000,
and check which objects of K are Ebars."""
import numpy as np
from lscene import *
from create2 import TC, TA, VV
m = Machine("NYYN", ["YNNNNN"], TC + 500, v=VV, left_periods=3, right_periods=2)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
sc = Scene(m, m.row, TC, K0 - 300, K0 + 400, 100)
E = ebar_tiles()
from census import clusters
i0 = sc.ebar_to_seg(K0)
print([(a - i0, b - i0) for a, b in clusters(sc.seg[i0 - 100:i0 + 350])][:12], "(offsets rel K0 - 100)")
hits = []
for k in range(30):
    arr = E[k][0]
    core = arr[16:-16]
    for x in range(-100, 350):
        i = sc.ebar_to_seg(K0 + x) + 16
        if np.array_equal(sc.seg[i:i + len(core)], core):
            hits.append((k, x))
print("Ebar tile matches (k, x):", hits)
