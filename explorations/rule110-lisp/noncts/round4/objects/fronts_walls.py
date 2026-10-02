"""Can ANY front type of an E^n rod absorb a left-moving (-3/5) wall cleanly?

All fronts: (15,-4)-periodic interfaces  ether(phase c) | E-bg(phase 0),
for every left ether phase c (wallsat.InterfaceModel with the ether tile
rotated by c), smallest width <= WMAX. Rod = that front + E-bg + the standard
back (taken from a standard E^N whose interior is aligned to bg phase 0 by a
whole-period shift). Each of the 15 left-wall kinds (walls_ebg.jsonl, left
domain = bg phase 0) is planted POS cells behind the front; after T steps
the scene is typed (long-rod recognition) and compared with the rod alone.
A clean absorption = exactly one rod-like object, nothing else.
Usage: python3 fronts_walls.py N POS T WMAX"""
import json
import sys
import numpy as np
import cone
import objlib as O
import wallsat as WS

N, POS, T, WMAX = (map(int, sys.argv[1:5]) if __name__ == "__main__" else (45, 60, 700, 24))
BG = cone.Background(O.EBG)
ETH = O.ETHER


def fronts():
    out = {}
    for c in range(14):
        tileL = ETH[c:] + ETH[:c]          # ether cell x reads ETHER[(x + c)]
        bL = cone.Background(tileL)
        for W in range(2, WMAX + 1, 2):
            m = WS.InterfaceModel(bL, BG, (0, 0), 15, -4, W)
            r = m.solve()
            if r is not None:
                out[c] = (W, r, m.a[0])
                break
    return out


def standard_rod():
    b, l, r = O.en_bits(N)
    pad = 2 * T + 400
    row, x0, objs, cR = O.build([("raw", b, l, r, 0, "E")], pad=pad)
    s_front = objs[0][1]
    mid = s_front + len(b) // 2
    r0 = [cand for cand in range(10)
          if all(row[y - x0] == BG.bit(0, y - cand) for y in range(mid - 15, mid + 15))]
    assert len(r0) == 1
    return row, x0, s_front, len(b), r0[0]


def one_rod(a, xa):
    """exactly one defect cluster, and it is (15,-4)-periodic"""
    ty = O.types(a, xa)
    if len(ty) != 1:
        return False, [t[0] for t in ty]
    # 20 periods: a slowly eroding rod (seen: -1 cell / 100 steps) must fail
    P, D = 300, -80
    b = O.evolve(a, P)
    m = 40 + P
    seg_a = a[m:len(a) - m]
    xs = np.arange(xa + m, xa + len(a) - m)
    ib = xs + D - (xa + P)
    okb = (ib >= 0) & (ib < len(b))
    return bool(np.array_equal(b[ib[okb]], seg_a[okb])), [t[0] for t in ty]


def build_scene(front, wallrec=None):
    """rod with the given front; coordinates = bg coordinates shifted by r0
    (a multiple-of-10 shift keeps bg phase 0). Returns (row, x0, front_col)."""
    row, x0, s_front, lb, r0 = standard_rod()
    c, (W, fr, a0) = front
    # in bg coords the front window starts at a0; map to rod coords + r0 + 10k
    target = s_front - 10
    k = (target - a0 - r0) // 10
    shift = r0 + 10 * k
    fs = a0 + shift                      # rod column of the front window
    scene = row.copy()
    # left of the window: ether with phase c in bg coords -> cell y reads
    # ETHER[(y - shift + c) % 14]
    for y in range(x0, fs):
        scene[y - x0] = O.EB[(y - shift + c) % 14]
    scene[fs - x0:fs + W - x0] = fr
    # right of the window up to the standard interior: bg phase 0 in bg coords
    for y in range(fs + W, s_front + lb // 2):
        scene[y - x0] = BG.bit(0, y - shift)
    wl = None
    if wallrec is not None:
        w = np.array([int(ch) for ch in wallrec["row0"]], np.uint8)
        tg, sg = wallrec["g"]
        wa0 = wallrec["a0"]
        kk = (fs + W + POS - wa0 - shift) // 10
        wsh = shift + 10 * kk
        wl = wa0 + wsh
        assert wl + len(w) < s_front + lb - 15
        # right domain: the standard rod (valid back) evolved tg, shifted sg
        b, l, r = O.en_bits(N)
        _, _, objs, cR = O.build([("raw", b, l, r, 0, "E")], pad=2 * T + 400)
        src = np.concatenate([row, O.ether(cR, x0 + len(row), x0 + len(row) + 40)])
        Rp = O.evolve(src, tg)
        for y in range(wl + len(w), x0 + len(row)):
            i = y - sg - (x0 + tg)
            scene[y - x0] = Rp[i]
        scene[wl - x0:wl + len(w) - x0] = w
    return scene, x0, fs, wl


if __name__ == "__main__":
    F = fronts()
    print(f"{len(F)} left ether phases admit a front (W <= {WMAX})", flush=True)
    walls = {}
    for l in open("walls_ebg.jsonl"):
        r = json.loads(l)
        if r["found"] and abs(r["v"] + 0.6) < 1e-9:
            g = tuple(r["g"])
            if g not in walls or r["W"] < walls[g]["W"]:
                walls[g] = r
    print(f"{len(walls)} left-wall kinds", flush=True)
    res = []
    for c, fr in sorted(F.items()):
        sc0, x0, fs, _ = build_scene((c, fr))
        a0 = O.evolve(sc0, T)
        ok_alone, base = one_rod(a0, x0 + T)
        for g, wr in sorted(walls.items()):
            sc, x0, fs, wl = build_scene((c, fr), wr)
            a = O.evolve(sc, T)
            clean, ty = one_rod(a, x0 + T)
            rec = {"c": c, "front_W": fr[0], "rod_alone": base, "rod_alone_ok": ok_alone,
                   "wall_g": list(g), "out": ty, "clean": clean}
            print(json.dumps(rec), flush=True)
            res.append(rec)
    print("clean absorptions:", sum(r["clean"] for r in res), "of", len(res))
