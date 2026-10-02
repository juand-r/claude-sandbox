"""The E^n -> X-rod conversion (fronts_walls.py: front type c=7 or 13 hit by
the (1,9) left wall). Measure the X-rod length as a function of n, and check
the X-rod is (75,-20)-periodic (300,-80 tested) for each n."""
import json, re, sys
import numpy as np
import objlib as O
import fronts_walls as FW

F = FW.fronts()
walls = {}
for l in open("walls_ebg.jsonl"):
    r = json.loads(l)
    if r["found"] and abs(r["v"] + 0.6) < 1e-9:
        g = tuple(r["g"])
        if g not in walls or r["W"] < walls[g]["W"]:
            walls[g] = r
c = int(sys.argv[1]) if len(sys.argv) > 1 else 7


def segs(r, xs):
    s = O.show(r)
    return [(m.start() + xs, m.group()) for m in re.finditer(r"[01]+", s)]


FW.POS = 30
for n in range(30, 61, 3):
    FW.N = n
    T = 300 + 12 * n
    FW.T = T
    sc, x0, fs, wl = FW.build_scene((c, F[c]), walls[(1, 9)])
    sc0, _, _, _ = FW.build_scene((c, F[c]))
    a = O.evolve(sc, T)
    b = O.evolve(a, 300)
    a0 = O.evolve(sc0, T)
    A, B, A0 = segs(a, x0 + T), segs(b, x0 + T + 300), segs(a0, x0 + T)
    per = len(A) == 1 and len(B) == 1 and A[0][1] == B[0][1] and B[0][0] - A[0][0] == -80
    xr = A[0][1] if len(A) == 1 else None
    dens = None if xr is None else round(xr.count("1") / len(xr), 3)
    print(json.dumps({"n": n, "c": c, "rod_alone_len": [len(s) for _, s in A0],
                      "out_len": [len(s) for _, s in A], "periodic_300_80": per,
                      "out_density": dens, "front_shift": None if xr is None else A[0][0] - A0[0][0]}), flush=True)
