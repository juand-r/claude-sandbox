"""Screen: Z = two Ebars placed in front of the rejector-prepared reader
P_1 (Ebar@K0+39, E@K0+68): does [Z][P_1] read s_1 differently?

Scenes (lscene, exact): tape NYYN (s_1 = Y) and NNYY (s_1 = N), t_in =
31500; s_1's four C's are at K0-486..K0-357 then, the region
[K0-340, K0+25) is ether. Z replaces that region by ether + Ebar_2 + Ebar_1
(slip 0 total, phases matched; splice.replace_region). Placements (k, o):
Ebar evolved k steps (0..29), tile start at offset o (one residue mod 14
per k). Ebar_1 tile start in [X1LO, X1HI) rel K0; Ebar_2 tile start in
[x1 - GAP, x1 - 20).
Record: for each tape, diffs of the window at t_in + T in [K0+100, K0+800)
vs the standard Y-read and N-read windows, and diffs in [K0-400, K0+100)
vs the same tape's standard window. The N tape is run only when the Y tape
is "interesting" (right part equal to either standard).
    python zscreen.py X1LO X1HI GAP out.jsonl"""
import sys, json
import numpy as np
from lscene import *
T, TIN = 3000, 31500
WLO, WHI, SPLIT = -400, 800, 100
RA, RB = -340, 25

def setup():
    S = {}
    for tape in ("NYYN", "NNYY"):
        m = Machine(tape, ["YNNNNN"], TIN + T + 500, left_periods=3, right_periods=2)
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        sc = Scene(m, m.row, TIN, K0 + WLO, K0 + WHI, T + 100)
        S[tape] = (K0, sc, sc.run(sc.seg, T))
    return S

def valid_offsets(seg, a, k):
    arr, cl, cr = ebar_tiles()[k]
    c = phase_at(seg, a)
    # tile at a+o needs (cl - (a+o)) % 14 == c_running; the running phase
    # changes after Ebar_2, so only the FIRST tile's residue is fixed here
    return (cl - c - a) % TILE

def score(S, tape, w):
    K0, sc, ref = S[tape]
    s = SPLIT - WLO
    rY, rN = S["NYYN"][2], S["NNYY"][2]
    return [int((w[s:] != rY[s:]).sum()), int((w[s:] != rN[s:]).sum()),
            int((w[:s] != ref[:s]).sum())]

if __name__ == "__main__":
    x1lo, x1hi, gap, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    S = setup()
    # positive control: identity (empty Z) reproduces the standard windows
    for tape in S:
        K0, sc, ref = S[tape]
        a, b = sc.ebar_to_seg(K0 + RA), sc.ebar_to_seg(K0 + RB)
        seg = replace_region(sc.seg, a, b, [])
        print("control", tape, score(S, tape, sc.run(seg, T)), flush=True)
    done = set()
    try:
        for line in open(outp):
            r = json.loads(line); done.add((r["k1"], r["x1"], r["k2"], r["x2"]))
    except FileNotFoundError:
        pass
    fh = open(outp, "a")
    K0, sc, _ = S["NYYN"]
    a, b = sc.ebar_to_seg(K0 + RA), sc.ebar_to_seg(K0 + RB)
    n = 0
    for k1 in range(30):
        for x1 in range(x1lo, x1hi):
            for k2 in range(30):
                for x2 in range(x1 - gap, x1 - 20):
                    if x2 < RA or (k1, x1, k2, x2) in done:
                        continue
                    pl = [(k2, x2 - RA), (k1, x1 - RA)]
                    rec = {"k1": k1, "x1": x1, "k2": k2, "x2": x2}
                    ok = True
                    for tape in ("NYYN", "NNYY"):
                        K0, sc, ref = S[tape]
                        aa, bb = sc.ebar_to_seg(K0 + RA), sc.ebar_to_seg(K0 + RB)
                        seg = replace_region(sc.seg, aa, bb, pl)
                        if seg is None:
                            ok = False; break
                        rec[tape] = score(S, tape, sc.run(seg, T))
                        if tape == "NYYN" and min(rec[tape][:2]) > 0:
                            break
                    if not ok:
                        continue
                    fh.write(json.dumps(rec) + "\n"); n += 1
                    if n % 200 == 0:
                        fh.flush()
    fh.flush()
    print("done", n)
