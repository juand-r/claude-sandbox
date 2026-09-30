"""Interaction regions of catalog collisions (needed by glidersim.py).

For a catalog entry (X seeded at (0,0), Y at Y_event) let
  t_a = first generation at which the row differs (cell for cell) from
        the freely moving inputs,
  t_b = first generation from which the row equals the freely moving
        products (cell for cell) at every later generation up to the
        settle time + EXTRA_CHECK.
Usually t_a < t_b and [t_a, t_b] is the reaction. If t_b <= t_a, both
descriptions hold on [t_b, t_a) (e.g. A + D2 -> D1: an A adjacent to a D2
IS a D1, so the "fusion" is a juxtaposition). The region is
[t_lo, t_hi] = [min, max] of the two, and x_lo, x_hi are the extreme
defect columns over [t_lo - 1, t_hi].

All in X's frame (X seeded at (0,0)). A third glider that keeps at least
MERGE cells away from this box during [t_start, t_end] cannot have affected
the reaction (conservative: the box contains everything that differs from
ether). Stored in regions.json keyed by "X|Y|cls".

Usage: python regions.py        (computes missing entries)
"""

import json
import os
import sys

import numpy as np

from library import Library
from r110lib import TILE, build_row, ether_cells, obj_key, objects, step_rows

OUT = "regions.json"
EXTRA_CHECK = 60


def free_row(lib, placements, t, x0, W, cL0):
    """Row (global columns x0 .. x0+W) of freely moving gliders at time t,
    far-left ether absolute phase cL0 at time 0; None if two gliders
    overlap or their ether phases disagree (they cannot be free)."""
    sts = sorted((lib.gliders[n].state_at(t0, xx, t) for n, t0, xx in placements),
                 key=lambda s: s[3])
    c = (cL0 + 4 * t) % TILE
    out = ether_cells(c, x0, x0 + W).copy()
    cur = x0
    for bits, l, r, s in sts:
        if s < cur or (l - s) % TILE != c:
            return None
        out[s - x0:s - x0 + len(bits)] = [int(ch) for ch in bits]
        c = (r - s) % TILE
        cur = s + len(bits)
        out[cur - x0:] = ether_cells(c, cur, x0 + W)
    return out


def region(lib, row_entry):
    """-> [t_lo, t_hi, x_lo, x_hi] (see module docstring)."""
    X, Y = row_entry["X"], row_entry["Y"]
    ins = [(X, 0, 0), (Y, *row_entry["Y_event"])]
    prods = [tuple(p) for p in row_entry["products"]]
    T = row_entry["T"] + EXTRA_CHECK
    sts = [lib.gliders[n].state_at(t0, x0, 0) for n, t0, x0 in ins]
    row, x0 = build_row(sts, pad=T + 100)
    W = len(row)
    cL0 = (sts[0][1] - sts[0][3]) % TILE
    t_a = None          # first t at which the row is not the free inputs
    last_bad = -1       # last t at which the row is not the free products
    extents = []
    for t in range(T + 1):
        if t_a is None:
            pred = free_row(lib, ins, t, x0, W, cL0)
            if pred is None or not np.array_equal(pred, row):
                t_a = t
        pred = free_row(lib, prods, t, x0, W, cL0)
        if pred is None or not np.array_equal(pred, row):
            last_bad = t
        objs = objects(row)
        extents.append((objs[0][0] + x0, objs[-1][1] + x0) if objs else None)
        row = step_rows(row)
    t_b = last_bad + 1
    if t_a is None:
        raise AssertionError(f"{X}+{Y}: inputs never interact within T")
    if t_b > row_entry["T"] + 1:
        raise AssertionError(f"{X}+{Y}#{row_entry['cls']}: products not "
                             f"free by the settle time (t_b={t_b})")
    t_lo, t_hi = min(t_a, t_b), max(t_a, t_b)
    ext = [e for e in extents[max(t_lo - 1, 0):t_hi + 1] if e]
    return [t_lo, t_hi, min(e[0] for e in ext), max(e[1] for e in ext)]


def key(r):
    return f"{r['X']}|{r['Y']}|{r['cls']}"


def main():
    lib = Library.load()
    rows = json.load(open("collisions.json"))
    reg = json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo = [r for r in rows if key(r) not in reg and r["settled"]]
    for i, r in enumerate(todo):
        reg[key(r)] = region(lib, r)
        if i % 200 == 0:
            print(i, len(todo), flush=True)
            json.dump(reg, open(OUT, "w"))
    json.dump(reg, open(OUT, "w"))
    print("regions:", len(reg))


if __name__ == "__main__":
    main()
