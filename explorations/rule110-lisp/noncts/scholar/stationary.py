"""Enumerate every stationary (7,0)-invariant object of bounded width in the
Rule 110 ether, by the de Bruijn method (McIntosh, Martinez), and hit each
one with a single A from the left.

Purpose: independent check of synth's SAT bound (BOARD 05:10) that no
stationary period-7 object of width <= 24 lets an A pass through and come
out as an A-train on the right.

Method. A row is invariant under 7 generations iff every 15-cell window W
satisfies f7(W) == W[7], where f7 maps 15 cells to the centre cell after 7
steps. Such rows are bi-infinite paths in the de Bruijn graph on 14-cell
windows restricted to valid 15-windows. A localized object is a path that
starts in an ether window and returns to ether windows. We DFS from each of
the 14 ether rotations, track the length of the current non-ether stretch,
and record a candidate each time the path is back in ether for 14
consecutive windows (so the object is complete and followed by clean ether).

Width is measured as the number of cells between the last ether-matching
window on the left and the first on the right (the defect region), which is
how census.clusters measures defects.

Run: python stationary.py [max_width]   (default 24)
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engine import ETHER, parse, step  # noqa: E402
import r110check as r  # noqa: E402

TILE = 14
ROTS = [ETHER[k:] + ETHER[:k] for k in range(TILE)]
ROT_CODE = {int(s, 2): k for k, s in enumerate(ROTS)}


def valid_windows():
    """valid[w] for 15-bit w (bit 14 = leftmost cell)."""
    n = 1 << 15
    cells = ((np.arange(n)[:, None] >> np.arange(14, -1, -1)) & 1).astype(np.uint8)
    # evolve 7 steps without wrap: width shrinks by 2 per step
    x = cells
    for _ in range(7):
        l, c, rr = x[:, :-2], x[:, 1:-1], x[:, 2:]
        x = ((c | rr) & (1 - (l & c & rr))).astype(np.uint8)
    return x[:, 0] == cells[:, 7]


def enumerate_objects(max_width):
    valid = valid_windows()
    found = {}
    mask14 = (1 << 14) - 1
    for k in range(TILE):
        start = int(ROTS[k], 2)          # 14-cell window as int, MSB leftmost
        # stack: (window, cells_so_far(list), defect_start or None, ether_run)
        stack = [(start, list(ROTS[k]), None, 0)]
        while stack:
            w, cells, dstart, erun = stack.pop()
            for bit in (0, 1):
                w15 = (w << 1) | bit
                if not valid[w15]:
                    continue
                w2 = w15 & mask14
                c2 = cells + [str(bit)]
                in_ether = w2 in ROT_CODE
                if dstart is None:
                    if in_ether:
                        # a defect starting later is found from another rotation
                        continue
                    stack.append((w2, c2, len(c2) - TILE, 0))
                    continue
                # inside or after a defect
                if in_ether:
                    erun2 = erun + 1
                    if erun2 >= TILE:
                        end = len(c2) - TILE - erun2 + 1
                        width = end - dstart
                        s = "".join(c2)
                        found.setdefault(s[max(0, dstart - TILE):], width)
                        continue
                    stack.append((w2, c2, dstart, erun2))
                else:
                    if len(c2) - TILE - dstart > max_width + 2 * TILE:
                        continue
                    stack.append((w2, c2, dstart, 0))
    return found


def defect_width(seg):
    """Width of the defect as census measures it (gap/overlap between the
    ether runs on the two sides), after padding seg with ether."""
    from census import clusters
    first = ROT_CODE[int(seg[:TILE], 2)]
    last = ROT_CODE[int(seg[-TILE:], 2)]
    left = "".join(ETHER[(first - 3 * TILE + i) % TILE] for i in range(3 * TILE))
    right = "".join(ETHER[(last + TILE + i) % TILE] for i in range(3 * TILE))
    row = parse(left + seg + right)
    cl = clusters(row)
    if not cl:
        return 0, None
    a, b = cl[0][0], cl[-1][1]
    slip = r.width(row, a, b)          # ether offset across the defect
    return b - a, ((left + seg + right)[a:b], slip)


def canonical(objs, max_width):
    """Keep objects with census width <= max_width, deduplicated by their
    defect cells (translation)."""
    out = {}
    for seg in objs:
        w, core = defect_width(seg)
        if core is not None and w <= max_width:
            out.setdefault(core, seg)
    return out


def hit_with_A(seg, T=700, pad=200):
    """seg starts with a full ether window (some rotation) and ends in ether.
    Place A(f1_1) far to the left in tile-aligned ether, then seg."""
    first = int(seg[:TILE], 2)
    rot = ROT_CODE[first]
    left = ETHER * pad + r.PHASES["A(f1_1)"] + ETHER * 12 + ETHER[:rot]
    # continue seg's right ether for pad tiles
    last = seg[-TILE:]
    rrot = ROT_CODE[int(last, 2)]
    right = "".join(ETHER[(rrot + TILE + i) % TILE] for i in range(pad * TILE))
    row = parse(left + seg + right)
    h = r.evolve(row, T)
    lo, hi = T + 20, len(row) - T - 20
    before = r.objects(h, 60, lo, hi)
    after = r.objects(h, T, lo, hi)
    after2 = r.objects(h, T - 120, lo, hi)
    return before, after, after2


def main(max_width=24):
    raw = enumerate_objects(max_width)
    objs = canonical(raw, max_width)
    print(f"{len(raw)} raw segments, {len(objs)} distinct stationary objects "
          f"of census width <= {max_width}")
    results = {}
    for core, seg in sorted(objs.items(), key=lambda kv: len(kv[0])):
        width = len(core[0])
        b, a, a2 = hit_with_A(seg)
        names_b = tuple(o[2] for o in b)
        names_a = tuple(o[2] for o in a)
        settled = names_a == tuple(o[2] for o in a2)
        key = (names_b, names_a, settled)
        results.setdefault(key, []).append(width)
    passes = []
    for (nb, na, st), ws in sorted(results.items(), key=lambda kv: min(kv[1])):
        moving_right = [n for n in na if n.startswith("A")]
        stationary = [n for n in na if n.startswith("C") or n.startswith("?(7,0")]
        flag = "PASS-THROUGH?" if moving_right and stationary else ""
        if flag:
            passes.append((nb, na))
        print(f"widths {sorted(set(ws))[:6]} n={len(ws)}  {nb} + A -> {na}"
              f"{'' if st else ' UNSETTLED'} {flag}")
    print("candidate pass-throughs:", passes)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 24)


def hit_with_B(seg, T=700, pad=200):
    """seg as in hit_with_A; B(f1_1) placed to the right in tile-aligned
    ether, 12 tiles after the segment."""
    first = int(seg[:TILE], 2)
    rot = ROT_CODE[first]
    left = "".join(ETHER[(rot - pad * TILE + i) % TILE] for i in range(pad * TILE))
    last = seg[-TILE:]
    rrot = ROT_CODE[int(last, 2)]
    # continue seg's ether to the next tile boundary
    # the cell after seg reads ETHER[rrot]; continue up to a tile boundary
    k = (TILE - rrot) % TILE
    cont = "".join(ETHER[(rrot + i) % TILE] for i in range(k))
    right = cont + ETHER * 12 + r.PHASES["B(f1_1)"] + ETHER * pad
    row = parse(left + seg + right)
    h = r.evolve(row, T)
    lo, hi = T + 20, len(row) - T - 20
    return r.objects(h, 60, lo, hi), r.objects(h, T, lo, hi), r.objects(h, T - 120, lo, hi)


def main_B(max_width=24):
    objs = canonical(enumerate_objects(max_width), max_width)
    print(f"{len(objs)} distinct stationary objects of census width <= {max_width}")
    results = {}
    for core, seg in sorted(objs.items(), key=lambda kv: len(kv[0][0])):
        b, a, a2 = hit_with_B(seg)
        key = (tuple(o[2] for o in b), tuple(o[2] for o in a),
               tuple(o[2] for o in a) == tuple(o[2] for o in a2))
        results.setdefault(key, []).append((len(core[0]), core[0], int(core[1])))
    for (nb, na, st), cores in sorted(results.items(), key=lambda kv: min(c[0] for c in kv[1])):
        right = [n for n in na if n.startswith("A")]
        stat = [n for n in na if n.startswith("C") or n.startswith("?(7,0")]
        flag = ""
        if right and stat:
            flag = "REFLECT(stationary kept)"
        elif right:
            flag = "REFLECT(object consumed)"
        print(f"n={len(cores)} e.g. {cores[0]}  {nb} + B -> {na}"
              f"{'' if st else ' UNSETTLED'} {flag}")
