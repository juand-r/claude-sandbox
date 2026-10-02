import numpy as np
from lscene import *
from create2 import TC, VV
from census import clusters
m = Machine("NYYN", ["YNNNNN"], TC + 500, v=VV, left_periods=3, right_periods=2)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
sc = Scene(m, m.row, TC, K0 - 300, K0 + 400, 100)
E = ebar_tiles()
hits = []
for k in range(30):
    arr = E[k][0]
    cl = clusters(arr)[0]
    n = cl[1] + 1            # left margin + core (+1)
    for x in range(-40, 60):
        i = sc.ebar_to_seg(K0 + x)
        if np.array_equal(sc.seg[i:i + n], arr[:n]):
            hits.append((k, x, n))
print(hits)
