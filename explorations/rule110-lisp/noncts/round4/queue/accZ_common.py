import numpy as np
from lscene import *
from create import placements
from create2 import build_tight
from reads import tiles_of
TIN, T = 31500, 3000
JS = range(-8, 9)
WLO, WHI, SPLIT = -400, 800, 100
S = {}
for t in ("YYNN", "YNYN"):
    m = Machine(t, ["YNNNNN"], TIN + T + 500, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    sc = Scene(m, m.row, TIN, K0 + WLO, K0 + WHI, T + 30 * 8 + 50)
    S[t] = (K0, sc, {j: sc.run(sc.seg, T - 30 * j) for j in JS})
def score(w, tapes=("YYNN", "YNYN")):
    s = SPLIT - WLO
    out = []
    for rt in tapes:
        R = S[rt][2]
        d = {j: int((w[s:] != R[j][s:]).sum()) for j in JS}
        j = min(d, key=lambda q: (d[q], abs(q)))
        out += [d[j], j]
    return out + [int((w[:s] != S[rt][2][0][:s]).sum()) for rt in tapes]
