"""Brute-force search (complementary to the SAT searches, which are limited
to train widths 18-32): two-part right-moving trains P1 + P2 (P1, P2 in
A, A^2, A^3, A^4, I_L, Z_L; all period (3,2)), P2 placed BEHIND P1 at
relative seed (dt, dx), dt < 3, dx in 0..DXMAX (snapped, dedup), hitting my
E^n (n = 3..6) in all 3 x 14 placements.  Flag: exactly one E-family counter
left AND at least one left-mover (B, Bbar, or '?' whose velocity family is
B/Bbar) AND nothing else.  Log every flagged (train, n, outcome).
Resumable: appends to refl_brute.log; skips trains already logged as done."""
import os, sys
from collections import defaultdict
import numpy as np
import t1lib as L
import v3, vlib, engine
L.register_IL()

PARTS = ["A", "A^2", "A^3", "A^4", "IL", "ZL"]
NS = [3, 4, 5, 6]
DXMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 70
T = 2500
LOG = "refl_brute.log"
LEFTM = {"B", "Bbar"}


def classify(objs, r, org):
    names = [v3.base(n) for n, x, w in objs]
    cs = [b for b in names if b == "E" or b.startswith("E^")]
    if len(cs) != 1:
        return None
    rest = [b for b in names if not (b == "E" or b.startswith("E^"))]
    if not rest:
        return None
    if all(b in LEFTM or b == "?" for b in rest):
        return " + ".join(names)
    return None


def done_set():
    s = set()
    if os.path.exists(LOG):
        for line in open(LOG):
            if line.startswith("DONE"):
                s.add(line.split()[1])
    return s


if __name__ == "__main__":
    done = done_set()
    log = open(LOG, "a")
    for p1 in PARTS:
        for p2 in PARTS:
            key = f"{p1}|{p2}"
            if key in done:
                continue
            seen = set()
            nflag = 0
            for dt in range(3):
                for dx in range(14, DXMAX):
                    # train: P1 at (0, 0) relative, P2 behind (left) at (dt, -dx)
                    try:
                        _, _, pl = vlib.build([(p2, dt, -dx), (p1, 0, 0)], pad=50)
                    except ValueError:
                        continue
                    rel = (pl[0][1], pl[0][2] - pl[1][2])
                    if rel in seen:
                        continue
                    seen.add(rel)
                    for n in NS:
                        R = f"E^{n}"
                        pseen = set()
                        for t0 in range(3):
                            for ox in range(14):
                                items = [(p2, t0 + rel[0], -100 - ox + rel[1]), (p1, t0, -100 - ox), (R, 0, 0)]
                                try:
                                    _, _, placed = vlib.build_right(items, c_right=0, pad=50)
                                except ValueError:
                                    continue
                                if placed[1][2] - placed[0][2] != -rel[1] or placed[0][1] - placed[1][1] != rel[0]:
                                    continue
                                if (placed[1][1], placed[1][2]) in pseen:
                                    continue
                                objs, r, org, placed = v3.run(items, T)
                                if placed[1][2] - placed[0][2] != -rel[1] or placed[0][1] - placed[1][1] != rel[0]:
                                    continue          # snapping broke the train shape
                                pk = (placed[1][1], placed[1][2])
                                if pk in pseen:
                                    continue
                                pseen.add(pk)
                                c = classify(objs, r, org)
                                if c:
                                    nflag += 1
                                    log.write(f"FLAG {key} rel={rel} n={n} t0={t0} ox={ox}: {c}\n")
                                    log.flush()
            log.write(f"DONE {key} trains={len(seen)} flags={nflag}\n")
            log.flush()
            print(key, len(seen), nflag, flush=True)
