"""Single extra Ebar before K: the rejector deletes component Ebars one at a
time (D1 + Ebar -> A^3, A^3 + Ebar -> D1), so one extra Ebar should make it
arrive at K in the OTHER form (slips 3 vs 10 differ by 7 = Ebar's slip).
What does K make of it? Gap (0,112) opened before K (machine symmetry) at
t_c = 6000; one Ebar X in the gap; a compensating Ebar (slip 7) put in a
second gap (0,56) opened at K0+D+WR-150 (far right; nothing reaches it
before t_c + TA). Stage A only: census of [K0-50, K0+D+200) after the
answer prepared K, rej path (NYYN) and acc path (YYNN).
    python flip.py"""
import json
import numpy as np
from lscene import *
from create import open_gap, placements
from create2 import build_tight, TC, TA, VV
from census import census, MAX_DT
from engine import ETHER
ETH = np.array([int(c) for c in ETHER], dtype=np.uint8)
D = 112; WR = 900
E = ebar_tiles()
def scene(tape):
    m = Machine(tape, ["YNNNNN"], TC + TA + 500, v=VV, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    sc = Scene(m, m.row, TC, K0 - 1500, K0 + D + WR, TA + 50)
    g = open_gap(sc, K0, D)
    # second gap far right for the compensator
    c = sc.ebar_to_seg(K0 + D + WR - 300)
    for dd in range(0, 60):
        try:
            p = phase_at(g, c + dd - TILE); phase_at(g, c + dd); c += dd; break
        except ValueError:
            continue
    g2 = np.concatenate([g[:c], ETH[(p + np.arange(c, c + 56)) % TILE], g[c:len(g) - 56]])
    return K0, sc, g2, c
def cens(sc, K0, seg, t, lo, hi):
    w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
    for j in range(MAX_DT + 1):
        cc = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + lo, TC + t)
        rows.append(cc[i:i + hi - lo]); w = step_packed_n(w, 1)
    return [(a + lo, k) for a, b, k in census(np.array(rows))]
for tape in ("NYYN", "YYNN"):
    K0, sc, g, c = scene(tape)
    xc = c - sc.ebar_to_seg(K0) + 10          # compensator x rel K0 (tile start)
    print(tape, "control", cens(sc, K0, g, TA, -50, D + 200))
    p0 = phase_at(g, sc.ebar_to_seg(K0 - 10))
    for k, x, p1 in placements(sc, K0, E, -10, D - 50, p0)[::3]:
        seg = build_tight(g, sc, K0, [(E, k, x)], -10, D - 10) if False else None
        # place X (slip 7) and the compensator (slip 7) together: one region from -10 to the compensator gap end
        seg = build_tight(g, sc, K0, [(E, k, x)], -10, D - 10, ) if False else None
        new = g.copy()
        a, b = sc.ebar_to_seg(K0 - 10), sc.ebar_to_seg(K0 + D - 10)
        arr, cl, cr = E[k]; xi = sc.ebar_to_seg(K0 + x)
        if (cl - xi) % TILE != phase_at(g, a): continue
        new[xi:xi + len(arr)] = arr
        # re-phase ether from tile end to b, and everything from b to the compensator by +7: not possible
        # -> instead shift the whole stretch [b, c) by 7 cells (it is free table material)
        pa = (cr - xi) % TILE
        new[xi + len(arr):b] = ETH[(pa + np.arange(xi + len(arr), b)) % TILE]
        stretch = g[b:c].copy()
        new[b + 7:c + 7] = stretch
        new[b:b + 7] = ETH[(pa + np.arange(b, b + 7)) % TILE]
        # compensator: Ebar placed in the far gap right after the stretch
        ok = False
        for kc in range(30):
            arr2, cl2, cr2 = E[kc]
            for xx in range(c + 7, c + 40):
                if (cl2 - xx) % TILE == phase_at(new, xx - TILE + 0) and (cr2 - xx) % TILE == phase_at(g, c + 56 + 2):
                    pass
        print(tape, k, x, cens(sc, K0, new, TA, -50, D + 200)[:12])
        break
