"""Acceptor-path screen: in front of the ACCEPTOR-prepared reader P_1 lies
one extra Ebar (cluster at K0+0 at t_in = 31500; moving data at K0-118 and
further left). Replace that Ebar by ONE Ebar at any other placement in
[K0+RA, K0+RB) (slip preserved), or by Ebar + extra pair (mode 3).
Tapes YYNN (s_1 = Y) and YNYN (s_1 = N); scoring as zscreen (windows at
t_in + T: right part vs the standard Y / N read with 30j delays, left part
vs the standard left parts).
    python zacc.py MODE out.jsonl   (MODE = 1: one Ebar; 3: three Ebars)"""
import sys, json
from zscreen import T, TIN, WLO, WHI, SPLIT, JS, ether, placements, ETH
import zscreen
from lscene import *
RA, RB = -95, 37
TAPES = ("YYNN", "YNYN")

def setup():
    S = {}
    for tape in TAPES:
        m = Machine(tape, ["YNNNNN"], TIN + T + 500, left_periods=3, right_periods=2)
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        sc = Scene(m, m.row, TIN, K0 + WLO, K0 + WHI, T + 200)
        S[tape] = (K0, sc, sc.run(sc.seg, T), {j: sc.run(sc.seg, T - 30 * j) for j in JS})
    return S

def score(S, tape, w):
    s = SPLIT - WLO
    out = []
    for ref_tape in TAPES:
        R = S[ref_tape][3]
        d = {j: int((w[s:] != R[j][s:]).sum()) for j in JS}
        j = min(d, key=lambda q: (d[q], abs(q)))
        out += [d[j], j]
    out += [int((w[:s] != S[TAPES[0]][2][:s]).sum()), int((w[:s] != S[TAPES[1]][2][:s]).sum())]
    return out

if __name__ == "__main__":
    mode, outp = int(sys.argv[1]), sys.argv[2]
    zscreen.RA, zscreen.RB = RA, RB
    S = setup()
    E = ebar_tiles()
    for tape in TAPES:
        K0, sc = S[tape][:2]
        print("control (identity)", tape, score(S, tape, sc.run(sc.seg, T)), flush=True)
    K0, sc = S[TAPES[0]][:2]
    p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + RA))
    fh = open(outp, "w")
    n = 0
    combos = []
    if mode == 1:
        combos = [[(k, x)] for k, x, _ in placements(sc, K0, E, RA, RB, p0)]
    else:
        for k3, x3, p1 in placements(sc, K0, E, RA, RB, p0):
            for k2, x2, p2 in placements(sc, K0, E, x3 + 20, RB, p1):
                for k1, x1, _ in placements(sc, K0, E, x2 + 20, RB, p2):
                    combos.append([(k3, x3), (k2, x2), (k1, x1)])
    print("combos", len(combos), flush=True)
    for c in combos:
        rec = {"Z": c}
        for tape in TAPES:
            K0t, sct = S[tape][:2]
            seg = zscreen.build(sct, K0t, [(E, k, x) for k, x in c])
            if seg is None:
                rec[tape] = None; break
            rec[tape] = score(S, tape, sct.run(seg, T))
        fh.write(json.dumps(rec) + "\n"); n += 1
    fh.close()
    print("done", n)
