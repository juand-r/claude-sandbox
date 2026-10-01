"""Plant a background domain wall (from wallsat.py results) inside an E^N
rod and see what it does at the face it reaches. Exact Rule 110.

Rod coordinates vs background coordinates: the rod interior at time 0 equals
the E-bg shifted by r0 (found by matching). A wallsat record (g, row0, a0)
lives in bg coordinates: left domain bg(t, x), right domain bg(t+tg, x-sg),
wall cells row0 on [a0, a0+W) at t = 0. In rod coordinates the right domain is
the rod R evolved tg steps and shifted right by sg (R').
"""
import json
import sys
import numpy as np
import cone
import objlib as O

BG = cone.Background(O.EBG)


def plant(N, rec, pos, T):
    """Scene with E^N (phase 0) and wall `rec` about `pos` cells behind the
    rod's front. Returns (scene_row, ref_row, x0, s_front, len_rod)."""
    tg, sg = rec["g"]
    row0 = np.array([int(c) for c in rec["row0"]], np.uint8)
    a0, W = rec["a0"], len(row0)
    b, l, r = O.en_bits(N)
    pad = 2 * T + 400
    row, x0, objs, c = O.build([("raw", b, l, r, 0, f"E^{N}")], pad=pad)
    s_front = objs[0][1]
    mid = s_front + len(b) // 2
    r0 = [cand for cand in range(10)
          if all(row[y - x0] == BG.bit(0, y - cand) for y in range(mid - 15, mid + 15))]
    assert len(r0) == 1
    r0 = r0[0]
    # wall window start in rod coords: a0 + shift, shift = r0 + 10 k
    target = s_front + pos
    shift = r0 + 10 * ((target - a0 - r0) // 10)
    wl = a0 + shift
    assert s_front + 12 < wl and wl + W < s_front + len(b) - 12, "wall too close to a face"
    row_ext = np.concatenate([row, O.ether(c, x0 + len(row), x0 + len(row) + 30)])
    Rp = O.evolve(row_ext, tg)             # covers [x0+tg, ...)
    scene = row.copy()
    for y in range(wl + W, x0 + len(row)):
        i = y - sg - (x0 + tg)
        if 0 <= i < len(Rp):
            scene[y - x0] = Rp[i]
        else:
            raise AssertionError("R' does not cover")
    scene[wl - x0:wl + W - x0] = row0
    # consistency: cells just left of the wall equal the rod (left domain);
    # just right equal R' (they were written from it)
    return scene, row, x0, s_front, len(b), wl


if __name__ == "__main__":
    N, pos, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    sel = sys.argv[4]          # e.g. "-0.6"
    recs = [json.loads(l) for l in open("walls_ebg.jsonl")]
    seen = set()
    for rec in sorted((r for r in recs if r["found"] and abs(r["v"] - float(sel)) < 1e-9),
                      key=lambda r: (r["W"], r["P"])):
        g = tuple(rec["g"])
        if g in seen:
            continue
        seen.add(g)
        sc, ref, x0, sf, lb, wl = plant(N, rec, pos, T)
        a = O.evolve(sc, T)
        aref = O.evolve(ref, T)
        h = (2 * g[0] - 5 * g[1]) % 50
        print(f"g={g} h={h} W={rec['W']} P={rec['P']} D={rec['D']} wall at +{wl - sf}:",
              O.types_rods(a, x0 + T), " ref:", O.types_rods(aref, x0 + T), flush=True)
