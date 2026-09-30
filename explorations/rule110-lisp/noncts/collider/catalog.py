"""Build / extend the collision catalog (collisions.json).

For ordered pairs of library gliders (X, Y) with v_X > v_Y (X starts on
the left), enumerate all |det|/14 distinct collisions (collide.py),
simulate each to completion, and merge the results into collisions.json
(keyed by X, Y, class). Compound gliders met as products are
auto-registered in the library (gliders.json).

Usage:
  python catalog.py base            all pairs of base gliders + A2..A4 as X
  python catalog.py packets         packet inputs vs C1, C2, C3 (packets.py)
  python catalog.py extra           frequent unnamed products as inputs
  python catalog.py fpackets        F vs all 2-glider -4/15 packets
"""

import json
import os
import sys
import time

from collide import collide_pair
from library import BASE_ORDER, Library

OUT = "collisions.json"


def classify(lib, X, Y, res):
    """Coarse reaction type from the product list."""
    if not res["settled"]:
        return "unsettled"
    names = [p[0] for p in res["products"]]
    if not names:
        return "annihilation"
    if sorted(names) == sorted([X, Y]):
        return "crossing"
    if len(names) == 1:
        if names[0] in (X, Y):
            return "absorption"      # one input survives alone
        return "fusion"
    if X in names or Y in names:
        return "emission"            # an input survives, plus new gliders
    return "transmutation"


def run_pairs(lib, pairs):
    rows = []
    t0 = time.time()
    for X, Y in pairs:
        res = collide_pair(lib, X, Y)
        for r in res:
            r["kind"] = classify(lib, X, Y, r)
            rows.append(r)
        print(f"{X}+{Y}: {len(res)} collisions, "
              f"{sum(r['kind'] == 'unsettled' for r in res)} unsettled, "
              f"{time.time() - t0:.0f}s", flush=True)
    return rows


def merge_save(rows):
    old = json.load(open(OUT)) if os.path.exists(OUT) else []
    key = lambda r: (r["X"], r["Y"], r["cls"])
    new = {key(r): r for r in rows}
    merged = [r for r in old if key(r) not in new] + rows
    json.dump(merged, open(OUT, "w"), indent=0)
    return merged


def base_pairs(lib):
    names = BASE_ORDER + ["Aw2", "Aw3", "Aw4"]
    return [(X, Y) for X in names for Y in names
            if lib.gliders[X].velocity > lib.gliders[Y].velocity]


def packet_pairs(lib):
    from packets import enumerate_pairs
    pairs = []
    targets = ["C1", "C2", "C3"]
    right, left = [], []
    for g, h in [("A", "A")]:
        right += enumerate_pairs(lib, g, h, 30)[0]
    right += ["Aw5", "Aw6", "A^5"]
    for g, h in [("B", "B"), ("Ebar", "Ebar"), ("E", "E"), ("E", "Ebar"),
                 ("Ebar", "E")]:
        left += enumerate_pairs(lib, g, h, 30)[0]
    for P in dict.fromkeys(right):
        for C in targets:
            pairs.append((P, C))
    for P in dict.fromkeys(left):
        for C in targets:
            pairs.append((C, P))
    return pairs


EXTRA_OBJECTS = ["A^2", "A^3", "A^5", "A^4",
                 "B^2", "B^3", "v-4/15s1w6"]


def extra_pairs(lib):
    """Frequent unnamed products vs base gliders (+A2..A4) and each other."""
    names = BASE_ORDER + ["Aw2", "Aw3", "Aw4"] + EXTRA_OBJECTS
    return [(X, Y) for X in names for Y in names
            if (X in EXTRA_OBJECTS or Y in EXTRA_OBJECTS)
            and lib.gliders[X].velocity > lib.gliders[Y].velocity]


def fpacket_pairs(lib):
    """F (memory, architect's spec F) vs every -4/15 packet."""
    from packets import enumerate_pairs
    left = []
    for g, h in [("Ebar", "Ebar"), ("E", "E"), ("E", "Ebar"), ("Ebar", "E")]:
        left += enumerate_pairs(lib, g, h, 30)[0]
    return [("F", P) for P in dict.fromkeys(left)]


ECHAIN = ["E"] + [f"E^{n}" for n in range(2, 10)]


def ecount_pairs(lib):
    """Extendible E^n (unary counter candidate) vs A, A^2, B, C1-C3, F,
    D1, D2 and Ebar-speed-free partners."""
    pairs = []
    for En in ECHAIN:
        for X in ["A", "A^2", "A^3", "A^4", "D1", "D2", "C1", "C2", "C3",
                  "F", "H"]:
            pairs.append((X, En))
        for Y in ["B", "B^2", "Bbar", "G"]:
            pairs.append((En, Y))
    return pairs


if __name__ == "__main__":
    lib = Library.load()
    mode = sys.argv[1]
    pairs = {"base": base_pairs, "packets": packet_pairs,
             "extra": extra_pairs, "fpackets": fpacket_pairs,
             "ecount": ecount_pairs}[mode](lib)
    rows = run_pairs(lib, pairs)
    lib.save()
    merge_save(rows)
