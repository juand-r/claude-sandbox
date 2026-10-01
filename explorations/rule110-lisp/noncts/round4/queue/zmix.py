"""Screen: Z = object A (right, nearer P) + object B (left), slip(A)+slip(B)
= 0 mod 14, in front of the rejector-prepared reader P_1 (rej path,
t_in = 31500). A tile start in [ALO, AHI), B tile start in
[xA - GAP, xA - 12). Types from TYPES (E^n via splice.glider_tiles / en
names, Ebar). Scores as zscreen (delays 30j, |j| <= 8). The N tape is run
only if the Y tape's right part equals a standard window.
    python zmix.py A_NAME B_NAME ALO AHI GAP out.jsonl"""
import sys, json
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
A, B, alo, ahi, gap, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
TIGHT = len(sys.argv) > 7 and sys.argv[7] == "tight"
def tl(name):
    return ebar_tiles() if name == "Ebar" else glider_tiles(name)
TA, TB = tl(A), tl(B)
S = zscreen.setup()
K0, sc = S["NYYN"][:2]
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + zscreen.RA))
fh = open(outp, "a"); n = 0
for kb, xb, p1 in placements(sc, K0, TB, max(zscreen.RA, alo - gap), ahi - 12, p0):
    for ka, xa, _ in placements(sc, K0, TA, max(alo, xb + (0 if TIGHT else 12)), min(ahi, xb + gap), p1):
        rec = {"A": A, "ka": ka, "xa": xa, "B": B, "kb": kb, "xb": xb}
        for tape in ("NYYN", "NNYY"):
            K0t, sct = S[tape][:2]
            seg = (zscreen.build2 if TIGHT else zscreen.build)(sct, K0t, [(TB, kb, xb), (TA, ka, xa)])
            if seg is None:
                rec[tape] = None; break
            rec[tape] = zscreen.score(S, tape, sct.run(seg, zscreen.T))
            if tape == "NYYN" and min(rec[tape][0], rec[tape][2]) > 0:
                break
        if rec.get("NYYN") is not None:
            fh.write(json.dumps(rec) + "\n"); n += 1
    fh.flush()
print("done", n, flush=True)
