"""Answer converters: Z placed RIGHT of the reader P_1, in a gap of D cells
opened at K0+CUT (everything from there on shifted by (0, D), D = 0 mod 56,
which preserves the classes of both answer types against the table).
Rej path scenes (tapes NYYN: s_1 = Y, NNYY: s_1 = N), t_in = 31500, T long
enough for the answer to cross the gap. Classification as zscreen, against
the gap controls; the left part (remnant) is compared exactly.
    python zconv.py D A_NAME B_NAME out.jsonl"""
import sys, json
import numpy as np
import zscreen
from lscene import *
from engine import ETHER
from create import placements
from create2 import build_tight
from reads import tiles_of
ETH = np.array([int(c) for c in ETHER], dtype=np.uint8)
TIN, T = 31500, 4800
JS = range(-8, 9)
CUT = 310
WLO, WHI = -400, 1300

def open_gap_at(sc, K0, D, cut_rel):
    c = sc.ebar_to_seg(K0 + cut_rel)
    p = phase_at(sc.seg, c - TILE)
    return np.concatenate([sc.seg[:c], ETH[(p + np.arange(c, c + D)) % TILE], sc.seg[c:len(sc.seg) - D]])

def setup(D, tapes):
    S = {}
    for tape in tapes:
        m = Machine(tape, ["YNNNNN"], TIN + T + 500, left_periods=3, right_periods=2)
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        sc = Scene(m, m.row, TIN, K0 + WLO, K0 + D + WHI, T + 30 * 8 + 50)
        g = open_gap_at(sc, K0, D, CUT)
        S[tape] = (K0, sc, g, {j: sc.run(g, T - 30 * j) for j in JS})
    return S

def score(S, tapes, tape, w, D):
    s = (CUT + D) - WLO
    out = []
    for rt in tapes:
        R = S[rt][3]
        d = {j: int((w[s:] != R[j][s:]).sum()) for j in JS}
        j = min(d, key=lambda q: (d[q], abs(q)))
        out += [d[j], j]
    out += [int((w[:s] != S[rt][3][0][:s]).sum()) for rt in tapes]
    return out

if __name__ == "__main__":
    D, A, B, outp = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
    tapes = ("NYYN", "NNYY")
    S = setup(D, tapes)
    for t in tapes:
        K0, sc, g, R = S[t]
        print("control", t, score(S, tapes, t, sc.run(g, T), D), flush=True)
    TA, TB = tiles_of(A), tiles_of(B)
    K0, sc, g, _ = S["NYYN"]
    lo, hi = CUT + 5, CUT + D - 5
    p0 = phase_at(g, sc.ebar_to_seg(K0 + lo))
    fh = open(outp, "a"); n = 0
    for kb, xb, p1 in placements(sc, K0, TB, lo, hi, p0):
        for ka, xa, _ in placements(sc, K0, TA, xb, hi, p1):
            rec = {"D": D, "B": B, "kb": kb, "xb": xb, "A": A, "ka": ka, "xa": xa}
            for t in tapes:
                K0t, sct, gt, _ = S[t]
                seg = build_tight(gt, sct, K0t, [(TB, kb, xb), (TA, ka, xa)], lo, hi)
                if seg is None:
                    rec[t] = None; break
                rec[t] = score(S, tapes, t, sct.run(seg, T), D)
                if t == "NYYN" and min(rec[t][0], rec[t][2]) > 0:
                    break
            if rec.get("NYYN") is not None:
                fh.write(json.dumps(rec) + "\n"); n += 1
        fh.flush()
    print("done", n, flush=True)
