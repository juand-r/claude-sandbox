"""Screen: Z = ONE library object of slip 0 (Ebar-speed: period (30,-8) or
(15,-4)) at every placement whose tile lies in [K0+RA, K0+RB) in front of
the rejector-prepared reader P_1 (rej path, t_in = 31500, as zscreen).
Scores as zscreen (right part vs standard Y/N reads with 30j delays,
j in [-8, 8]; left part vs the standard Y / N left parts).
    python zlib.py out.jsonl [SLIP]"""
import sys, json
import numpy as np
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from splice import glider_tiles
outp = sys.argv[1]; SLIP = int(sys.argv[2]) if len(sys.argv) > 2 else 0
gl = json.load(open(NONCTS / "collider" / "gliders.json"))["gliders"]
objs = [g["name"] for g in gl if (g["p"], g["d"]) in ((30, -8), (15, -4)) and g["slip"] % 14 == SLIP]
S = zscreen.setup()
for tape in S:
    K0, sc = S[tape][:2]
    print("control", tape, zscreen.score(S, tape, sc.run(sc.seg, zscreen.T)), flush=True)
K0, sc = S["NYYN"][:2]
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + zscreen.RA))
fh = open(outp, "w"); n = 0
for name in objs:
    try:
        tiles = glider_tiles(name)
    except Exception as e:
        print("skip", name, e); continue
    for k, x, _ in placements(sc, K0, tiles, zscreen.RA, zscreen.RB, p0):
        rec = {"obj": name, "k": k, "x": x}
        for tape in ("NYYN", "NNYY"):
            K0t, sct = S[tape][:2]
            seg = zscreen.build(sct, K0t, [(tiles, k, x)])
            if seg is None:
                rec[tape] = None; break
            rec[tape] = zscreen.score(S, tape, sct.run(seg, zscreen.T))
            if tape == "NYYN" and min(rec[tape][0], rec[tape][2]) > 0:
                break
        fh.write(json.dumps(rec) + "\n"); n += 1
    fh.flush()
print("done", n, len(objs))
