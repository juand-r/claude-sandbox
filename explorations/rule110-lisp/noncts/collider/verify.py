"""Independent re-verification of every catalog reaction.

For each reaction in reactions.json: build the input row (X seeded at
(0,0), Y at Y_event) at time 0, evolve it T generations with the
project's scalar reference engine (../../engine.py `step`, not the
bit-sliced engine used by collide.py), then build the row that the
recorded products predict at time T (r110lib.build_row from the product
seed events) and require the two rows to be identical, cell for cell,
over the whole region the inputs' light cone can reach. For reactions
whose products are compounds the product's own phase data is used.

Usage: python verify.py [limit]
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", ".."))
import engine  # noqa: E402  (the project's reference simulator)

from library import Library  # noqa: E402
from r110lib import build_row, ether_cells, TILE  # noqa: E402


def verify(lib, r):
    gl = lib.gliders
    T = r["T"]
    ins = [gl[r["X"]].state_at(0, 0, 0), gl[r["Y"]].state_at(*r["Y_event"], 0)]
    pad = T + 60
    row, x0 = build_row(ins, pad=pad)
    W = len(row)
    cells = row.copy()
    for _ in range(T):
        cells = engine.step(cells)
    # window: everything within light-cone reach of the inputs, excluding
    # cells the wrap seam's light cone could reach (the wrap is clean, so
    # this is only a margin of safety)
    lo = ins[0][3] - T - 20
    hi = ins[1][3] + len(ins[1][0]) + T + 20
    lo_i, hi_i = max(lo - x0, 0), min(hi - x0, W)
    actual = cells[lo_i:hi_i]
    # predicted: products placed at time T in ether; far-left ether phase is
    # the inputs' far-left phase advanced by T generations
    cL = (ins[0][1] - ins[0][3] + 4 * T) % TILE
    if r["products"]:
        sts = [gl[n].state_at(t0, xx, T) for n, t0, xx in r["products"]]
        sts.sort(key=lambda s: s[3])
        pred_row = ether_cells(cL, x0, x0 + W).copy()
        # fill region by region, as build_row does, but in fixed coordinates
        c = cL
        cur = x0
        for bits, l, rr, s in sts:
            if (l - s) % TILE != c % TILE:
                return False, "ether phase between products inconsistent"
            pred_row[s - x0:s - x0 + len(bits)] = [int(ch) for ch in bits]
            c = (rr - s) % TILE
            nxt = s + len(bits)
            pred_row[nxt - x0:] = ether_cells(c, nxt, x0 + W)
    else:
        pred_row = ether_cells(cL, x0, x0 + W)
    pred = pred_row[lo_i:hi_i]
    if not np.array_equal(actual, pred):
        bad = np.nonzero(actual != pred)[0]
        return False, f"{len(bad)} cells differ, first at {bad[0] + lo_i + x0}"
    return True, ""


def main(limit=None):
    lib = Library.load()
    rows = json.load(open("reactions.json"))
    if limit:
        rows = rows[:limit]
    fails = 0
    for r in rows:
        ok, why = verify(lib, r)
        if not ok:
            fails += 1
            print("FAIL", r["id"], why)
    print(f"verified {len(rows) - fails}/{len(rows)} reactions")
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
