"""Creation screen, stage A: table material X (Ebars) inserted just before the
raw leader K0 (gap opened by the machine symmetry (0, D): K0 and everything
right of it shifted D cells, D = 0 mod 56). Scenes are cut at t_c = 6000
(before any answer reaches K0; the table there evolves freely, so the edit
equals a t = 0 edit). Run to t_c + T. Compare with the control (gap, no X):
  right part [K0+D-20, K0+D+WR) (P_1 and the table)  -> must be equal
  left part  [K0-WL, K0+D-20)                         -> recorded (marker?)
for the rejector path (tape NYYN) and the acceptor path (tape YYNN).
    python create.py D NX XLO XHI out.jsonl   (NX = 2: Ebar pairs)"""
import sys, json
import numpy as np
from lscene import *
from engine import ETHER
ETH = np.array([int(c) for c in ETHER], dtype=np.uint8)
TC, T = 6000, 11400         # t_c + T = 17400 = 0 mod 30 (same Ebar time phase as t_in = 31500); acceptor done by then
WL, WR = 1500, 600

def open_gap(sc, K0, D, cut_rel=-20):
    """New seg with everything right of Ebar-frame column K0+cut_rel shifted
    right by D (D = 0 mod 14 keeps the ether phase); far right end dropped."""
    assert D % 56 == 0
    c = sc.ebar_to_seg(K0 + cut_rel)
    # cut must be in ether
    p = phase_at(sc.seg, c - TILE)
    gapcells = ETH[(p + np.arange(c, c + D)) % TILE]
    new = np.concatenate([sc.seg[:c], gapcells, sc.seg[c:len(sc.seg) - D]])
    return new

def setup(D):
    S = {}
    for tape in ("NYYN", "YYNN"):
        m = Machine(tape, ["YNNNNN"], TC + T + 500, left_periods=3, right_periods=2)
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        sc = Scene(m, m.row, TC, K0 - WL, K0 + D + WR, T + 50)
        g = open_gap(sc, K0, D)
        S[tape] = (K0, sc, g, sc.run(g, T))
    return S

def insert(sc, K0, g, items, lo, hi):
    """Write items [(tiles, k, xrel)] into ether region [K0+lo, K0+hi) of g."""
    a, b = sc.ebar_to_seg(K0 + lo), sc.ebar_to_seg(K0 + hi)
    p, pb = phase_at(g, a), phase_at(g, b - TILE)
    new = g.copy(); pos = a
    for tiles, k, xr in items:
        arr, cl, cr = tiles[k]
        x = sc.ebar_to_seg(K0 + xr)
        if x < pos or x + len(arr) > b or (cl - x) % TILE != p:
            return None
        new[pos:x] = ETH[(p + np.arange(pos, x)) % TILE]
        new[x:x + len(arr)] = arr
        pos = x + len(arr); p = (cr - x) % TILE
    if p != pb:
        return None
    new[pos:b] = ETH[(p + np.arange(pos, b)) % TILE]
    return new

def placements(sc, K0, tiles, xlo, xhi, p_in):
    out = []
    for k in range(len(tiles)):
        arr, cl, cr = tiles[k]
        for xr in range(xlo, xhi):
            if (cl - sc.ebar_to_seg(K0 + xr)) % TILE == p_in:
                out.append((k, xr, (cr - sc.ebar_to_seg(K0 + xr)) % TILE))
    return out

if __name__ == "__main__":
    D, NX, xlo, xhi, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    S = setup(D)
    E = ebar_tiles()
    split = D - 20 + WL
    for tape in S:
        K0, sc, g, ref = S[tape]
        print("control", tape, int((sc.run(g, T) != ref).sum()), flush=True)
    K0, sc, g, _ = S["NYYN"]
    lo, hi = -10, D - 10           # insertion region (rel K0); gap is [-20, D-20)
    p0 = phase_at(g, sc.ebar_to_seg(K0 + lo))
    fh = open(outp, "a"); n = 0
    for k2, x2, p1 in placements(sc, K0, E, max(lo, xlo), xhi, p0):
        for k1, x1, _ in placements(sc, K0, E, x2 + 20, xhi, p1):
            rec = {"D": D, "X": [[k2, x2], [k1, x1]]}
            for tape in ("NYYN", "YYNN"):
                K0t, sct, gt, ref = S[tape]
                seg = insert(sct, K0t, gt, [(E, k2, x2), (E, k1, x1)], lo, hi)
                if seg is None:
                    rec[tape] = None; break
                w = sct.run(seg, T)
                rec[tape] = [int((w[split:] != ref[split:]).sum()), int((w[:split] != ref[:split]).sum())]
                if rec[tape][0] > 0:
                    break
            if rec.get("NYYN") is not None:
                fh.write(json.dumps(rec) + "\n"); n += 1
        fh.flush()
    print("done", n, flush=True)
