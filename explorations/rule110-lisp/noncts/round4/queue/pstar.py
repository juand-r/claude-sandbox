"""State = arrival class. In the acceptor path the next symbol crosses E0
(+7 cells) and arrives at the reader in a class differing by one crossing
from the rejector path; Cook's reader P = [Ebar@K0+39][E@K0+68] reads both
normally. Screen modified readers P*: P's E (cells K0+68..72) replaced by a
library object of the same slip (9 mod 14) at any placement with its tile
inside [K0+LO, K0+HI); all four tapes (rej path NYYN/NNYY, acc path
YYNN/YNYN), t_in = 31500. A P* that reads one path normally and the other
forced-N (exact) is a state-dependent reader.
    python pstar.py LO HI SLIP out.jsonl"""
import sys, json
import numpy as np
from lscene import *
from create import placements
from create2 import build_tight
from reads import tiles_of
TIN, T = 31500, 3000
JS = range(-8, 9)
WLO, WHI, SPLIT = -400, 800, 100
lo, hi, slip, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
TAPES = {"rej": ("NYYN", "NNYY"), "acc": ("YYNN", "YNYN")}
S = {}
for path, tps in TAPES.items():
    for t in tps:
        m = Machine(t, ["YNNNNN"], TIN + T + 500, left_periods=3, right_periods=2)
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        sc = Scene(m, m.row, TIN, K0 + WLO, K0 + WHI, T + 30 * 8 + 50)
        S[t] = (K0, sc, {j: sc.run(sc.seg, T - 30 * j) for j in JS})
def score(w, tps):
    s = SPLIT - WLO
    out = []
    for rt in tps:
        R = S[rt][2]
        d = {j: int((w[s:] != R[j][s:]).sum()) for j in JS}
        j = min(d, key=lambda q: (d[q], abs(q)))
        out += [d[j], j]
    return out + [int((w[:s] != S[rt][2][0][:s]).sum()) for rt in tps]
for path, tps in TAPES.items():
    for t in tps:
        print("control", t, score(S[t][1].run(S[t][1].seg, T), tps), flush=True)
gl = json.load(open(NONCTS / "collider" / "gliders.json"))["gliders"]
objs = [g["name"] for g in gl if (g["p"], g["d"]) in ((30, -8), (15, -4)) and g["slip"] % 14 == slip]
fh = open(outp, "w")
for name in objs:
    try:
        tl = tiles_of(name)
    except Exception:
        continue
    K0, sc, _ = S["NYYN"]
    p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + lo))
    for k, x, _ in placements(sc, K0, tl, lo, hi, p0):
        rec = {"obj": name, "k": k, "x": x}
        ok = True
        for path, tps in TAPES.items():
            for t in tps:
                K0t, sct, _ = S[t]
                seg = build_tight(sct.seg, sct, K0t, [(tl, k, x)], lo, hi)
                if seg is None: ok = False; break
                rec[t] = score(sct.run(seg, T), tps)
            if not ok: break
        if ok:
            fh.write(json.dumps(rec) + "\n")
    fh.flush()
print("done")
