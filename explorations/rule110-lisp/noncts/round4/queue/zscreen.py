"""Screen: Z = two Ebars placed in front of the rejector-prepared reader
P_1 (Ebar cells K0+39..48, E cells K0+68..72 at t_in): does [Z][P_1] read
the next symbol s_1 differently (forced N, inverted, forced Y)?

Scenes (lscene, exact): tape NYYN (s_1 = Y: C's at K0-488,-443,-398,-359)
and NNYY (s_1 = N: C's at K0-469,-424,-398,-359), t_in = 31500; the region
[K0+RA, K0+RB) is ether in both. Z = Ebar_2 (left) + Ebar_1 (right), tiles
(Ebar evolved k steps, 16-cell ether margins) written into that region with
consistent ether phases (Ebar slip is 7, so two Ebars restore the phase).
Record per placement: for each tape [dY, dN, dL]: diffs in [K0+100, K0+800)
at t_in + T vs the standard Y-read / N-read windows, and diffs in
[K0-400, K0+100) vs the same tape's standard window. The N tape is run
only if the Y tape's right part equals a standard window.
    python zscreen.py X1LO X1HI GAP out.jsonl"""
import sys, json
import numpy as np
from lscene import *
from engine import ETHER
import os
VMULT = int(os.environ.get("VMULT", "1"))
T, TIN = 3000, (31500 if VMULT == 1 else int(os.environ.get("TIN2", "47460")))
WLO, WHI, SPLIT = -400, 800, 100
RA, RB = -345, 37
ETH = np.array([int(c) for c in ETHER], dtype=np.uint8)

JS = range(-4, 5)              # answer delays of 30j steps tolerated

def setup():
    S = {}
    for tape in ("NYYN", "NNYY"):
        import encoder as enc
        m = Machine(tape, ["YNNNNN"], TIN + T + 500, v=enc._left_v(["YNNNNN"]) * VMULT, left_periods=3, right_periods=2)
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        sc = Scene(m, m.row, TIN, K0 + WLO, K0 + WHI, T + 30 * max(abs(j) for j in JS) + 50)
        S[tape] = (K0, sc, sc.run(sc.seg, T), {j: sc.run(sc.seg, T - 30 * j) for j in JS})
    return S

def ether(p, i0, n):
    return ETH[(p + np.arange(i0, i0 + n)) % TILE]

def build(sc, K0, items):
    """items: list of (tiles, k, xrel) left to right (xrel = tile start rel
    K0). Returns new seg or None (overlap / phase mismatch / out of region)."""
    a, b = sc.ebar_to_seg(K0 + RA), sc.ebar_to_seg(K0 + RB)
    seg = sc.seg
    p = phase_at(seg, a)
    pb = phase_at(seg, b - TILE)
    new = seg.copy()
    pos = a
    for tiles, k, xr in items:
        arr, cl, cr = tiles[k]
        x = sc.ebar_to_seg(K0 + xr)
        if x < pos or x + len(arr) > b or (cl - x) % TILE != p:
            return None
        new[pos:x] = ether(p, pos, x - pos)
        new[x:x + len(arr)] = arr
        pos = x + len(arr)
        p = (cr - x) % TILE
    if p != pb:
        return None
    new[pos:b] = ether(p, pos, b - pos)
    return new

def score(S, tape, w):
    """[dY, jY, dN, jN, dLY, dLN]: right-part diffs vs the standard Y / N
    read windows delayed by 30j (min over j, and the j), left-part diffs vs
    the standard Y / N windows (j = 0)."""
    s = SPLIT - WLO
    out = []
    for ref_tape in ("NYYN", "NNYY"):
        R = S[ref_tape][3]
        d = {j: int((w[s:] != R[j][s:]).sum()) for j in JS}
        j = min(d, key=lambda q: (d[q], abs(q)))
        out += [d[j], j]
    out += [int((w[:s] != S["NYYN"][2][:s]).sum()), int((w[:s] != S["NNYY"][2][:s]).sum())]
    return out

def placements(sc, K0, tiles, xlo, xhi, p_in):
    """(k, xrel) with tile start in [xlo, xhi) matching incoming phase p_in;
    returns list of (k, xrel, outgoing phase)."""
    out = []
    for k in range(len(tiles)):
        arr, cl, cr = tiles[k]
        for xr in range(xlo, xhi):
            x = sc.ebar_to_seg(K0 + xr)
            if (cl - x) % TILE == p_in:
                out.append((k, xr, (cr - x) % TILE))
    return out

if __name__ == "__main__":
    x1lo, x1hi, gap, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    S = setup()
    for tape in S:
        K0, sc = S[tape][:2]
        print("control (empty Z)", tape, score(S, tape, sc.run(build(sc, K0, []), T)), flush=True)
    done = set()
    try:
        for line in open(outp):
            r = json.loads(line); done.add((r["k2"], r["x2"], r["k1"], r["x1"]))
    except FileNotFoundError:
        pass
    E = ebar_tiles()
    K0, sc = S["NYYN"][:2]
    p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + RA))
    fh = open(outp, "a")
    n = 0
    for k2, x2, p1 in placements(sc, K0, E, RA, x1hi - 20, p0):
        for k1, x1, _ in placements(sc, K0, E, max(x1lo, x2 + 20), min(x1hi, x2 + gap), p1):
            if (k2, x2, k1, x1) in done:
                continue
            rec = {"k2": k2, "x2": x2, "k1": k1, "x1": x1}
            items = [(E, k2, x2), (E, k1, x1)]
            for tape in ("NYYN", "NNYY"):
                K0t, sct = S[tape][:2]
                seg = build(sct, K0t, items)
                if seg is None:
                    rec[tape] = None; break
                rec[tape] = score(S, tape, sct.run(seg, T))
                if tape == "NYYN" and min(rec[tape][0], rec[tape][2]) > 0:
                    break
            fh.write(json.dumps(rec) + "\n"); n += 1
            if n % 100 == 0:
                fh.flush()
    fh.flush()
    print("done", n, flush=True)


MINGAP = 3   # min ether cells between object cores (tiles carry 16-cell margins)

def build2(sc, K0, items):
    """Like build, but tiles may overlap in their ether margins: only the
    cores (tile[16:-16]) must be >= MINGAP cells apart. Ether phases must
    match across every object (same condition as build)."""
    a, b = sc.ebar_to_seg(K0 + RA), sc.ebar_to_seg(K0 + RB)
    seg = sc.seg
    p = phase_at(seg, a); pb = phase_at(seg, b - TILE)
    new = seg.copy()
    new[a:b] = ether(p, a, b - a)
    core_end = a - MINGAP
    for tiles, k, xr in items:
        arr, cl, cr = tiles[k]
        x = sc.ebar_to_seg(K0 + xr)
        if x + 16 < core_end + MINGAP or x < a or x + len(arr) > b or (cl - x) % TILE != p:
            return None
        s0 = max(0, core_end - x)                 # do not overwrite the previous core
        new[x + s0:x + len(arr)] = arr[s0:]
        core_end = x + len(arr) - 16
        p = (cr - x) % TILE
        new[x + len(arr):b] = ether(p, x + len(arr), b - x - len(arr))
    if p != pb:
        return None
    return new
