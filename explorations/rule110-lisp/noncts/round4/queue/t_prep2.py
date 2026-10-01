"""P1: exact prepared core after rejection of N^L (phase L mod 6) or acceptance.
Window in Ebar frame; aligned in SPACETIME by the untouched table to the right
(time offset j in 0..29, space shift d)."""
import sys
import numpy as np
from q import *
T = int(sys.argv[1])
def wins(L, tape, n):
    m = Machine(tape, ["N"*L, "YNNNNN"], T+500, left_periods=3, right_periods=2)
    K0 = [a for n_, a, b in m.blocks if n_ == "K"][0]
    r = Run(m.row, m.origin); r.step(T)
    out = []
    for j in range(n):
        sh = r.ebar_frame(T + j)
        out.append(r.window(K0 - 200 + sh, K0 + 700 + sh).copy())
        r.step(1)
    return out
ref = wins(6, "NYYN", 1)[0]
for L, tape in [(12,"NYYN"),(8,"NYYN"),(10,"NYYN"),(14,"NYYN"),(6,"YYNN"),(8,"YYNN")]:
    ws = wins(L, tape, 30)
    found = None
    for j, w in enumerate(ws):
        for d in range(-100, 101):
            if np.array_equal(ref[450:850], w[450+d:850+d]):
                found = (j, d); break
        if found: break
    diff = None
    if found:
        j, d = found; w = ws[j]
        lo = max(0, -d); hi = min(len(ref), len(w)-d)
        dd = np.nonzero(ref[lo:hi] != w[lo+d:hi+d])[0] + lo
        diff = (len(dd), (int(dd.min())-200, int(dd.max())-200) if len(dd) else None)
    print(L, tape, "align(j,d)", found, "diff", diff, flush=True)
