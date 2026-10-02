"""Acceptor-path screen: Z = two objects (A right, B left; slips summing to 0
mod 14; tiles may overlap in margins) ADDED in the pure-ether interval
[K0+LO, K0+HI) between the last moving-data Ebar (cluster K0-118) and E0
(cluster K0+0), t_in = 31500; tapes YYNN (s_1 = Y) / YNYN (s_1 = N).
Scores vs the standard acc-path reads (delays 30j), left part exact.
    python zaccpair.py A B LO HI out.jsonl"""
import sys, json
from accZ_common import *
A, B, lo, hi, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
TA, TB = tiles_of(A), tiles_of(B)
K0, sc, _ = S["YYNN"]
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + lo))
fh = open(outp, "a"); n = 0
for kb, xb, p1 in placements(sc, K0, TB, lo, hi, p0):
    for ka, xa, _ in placements(sc, K0, TA, xb, hi, p1):
        rec = {"A": A, "ka": ka, "xa": xa, "B": B, "kb": kb, "xb": xb}
        for t in ("YYNN", "YNYN"):
            K0t, sct, _ = S[t]
            seg = build_tight(sct.seg, sct, K0t, [(TB, kb, xb), (TA, ka, xa)], lo, hi)
            if seg is None:
                rec[t] = None; break
            rec[t] = score(sct.run(seg, T))
            if t == "YYNN" and min(rec[t][0], rec[t][2]) > 0:
                break
        if rec.get("YYNN") is not None:
            fh.write(json.dumps(rec) + "\n"); n += 1
print("done", n, flush=True)
