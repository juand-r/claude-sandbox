"""Answer converters in the EXISTING ether between the reader core P_1
(cells K0+39..72 at t_in) and K's tail (K0+129..): no gap. Z = Ebar pairs
(tiles may overlap in margins, cores >= 3 apart) with tiles inside
[K0+LO, K0+HI). Rej path tapes NYYN / NNYY, t_in = 31500, T = 4800.
Classify right part [K0+SPLIT, ...) vs standard Y/N reads (delays 30j),
left part [K0-400, K0+SPLIT) vs standard left parts (exact).
    python zconv2.py LO HI SPLIT out.jsonl [A B]"""
import sys, json
import numpy as np
from lscene import *
from create import placements
from create2 import build_tight
from reads import tiles_of
TIN, T = 31500, 4800
JS = range(-8, 9)
WLO, WHI = -400, 1200
lo, hi, SPLIT, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
A, B = (sys.argv[5], sys.argv[6]) if len(sys.argv) > 6 else ("Ebar", "Ebar")
tapes = ("NYYN", "NNYY")
S = {}
for t in tapes:
    m = Machine(t, ["YNNNNN"], TIN + T + 500, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    sc = Scene(m, m.row, TIN, K0 + WLO, K0 + WHI, T + 30 * 8 + 50)
    S[t] = (K0, sc, {j: sc.run(sc.seg, T - 30 * j) for j in JS})
def score(w):
    s = SPLIT - WLO
    out = []
    for rt in tapes:
        R = S[rt][2]
        d = {j: int((w[s:] != R[j][s:]).sum()) for j in JS}
        j = min(d, key=lambda q: (d[q], abs(q)))
        out += [d[j], j]
    return out + [int((w[:s] != S[rt][2][0][:s]).sum()) for rt in tapes]
for t in tapes:
    print("control", t, score(S[t][1].run(S[t][1].seg, T)), flush=True)
TA, TB = tiles_of(A), tiles_of(B)
K0, sc, _ = S["NYYN"]
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + lo))
fh = open(outp, "a"); n = 0
for kb, xb, p1 in placements(sc, K0, TB, lo, hi, p0):
    for ka, xa, _ in placements(sc, K0, TA, xb, hi, p1):
        rec = {"B": B, "kb": kb, "xb": xb, "A": A, "ka": ka, "xa": xa}
        for t in tapes:
            K0t, sct, _ = S[t]
            seg = build_tight(sct.seg, sct, K0t, [(TB, kb, xb), (TA, ka, xa)], lo, hi)
            if seg is None:
                rec[t] = None; break
            rec[t] = score(sct.run(seg, T))
        if rec.get("NYYN") is not None:
            fh.write(json.dumps(rec) + "\n"); n += 1
print("done", n, flush=True)
