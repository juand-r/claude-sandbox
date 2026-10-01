"""clib.py - bring collider-library objects into MY vlib library.

The object's DEFINITION necessarily comes from the teammate's data
(collider/gliders.json). Everything after that is mine: I harvest the
object's base row from a single-object row, find its period with my own
search (vlib.find_period) and assert it equals the catalog's (p, d); then
placements, runs and typing use vlib only. xlate.check (round 2) asserts
that my rebuilt scene rows equal collider's build_row cell for cell.

ensure(name) registers the object (idempotent).  Call ensure() again after
anything that runs libgen.load() (it clears vlib.LIB)."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R2V = os.path.abspath(os.path.join(HERE, "..", "..", "round2", "verify"))
sys.path.insert(0, R2V)
import hrun      # noqa: E402,F401  (sets up paths, imports v3 -> vlib, libgen)
import vlib      # noqa: E402
import xlate     # noqa: E402

CLIB = xlate.CLIB


def ensure(name):
    if name in vlib.LIB:
        return vlib.LIB[name]
    g = CLIB.gliders[name]
    row, x0 = xlate.their_row([(name, 0, 0)])
    ds = vlib.defects(row)
    lo, hi = min(d["lo"] for d in ds), max(d["hi"] for d in ds)
    base = vlib.extract_base(row, lo, hi)
    per = vlib.find_period(base, maxP=max(200, g.p))
    if per != (g.p, g.d):
        raise ValueError(f"{name}: my period {per} != catalog {(g.p, g.d)}")
    return vlib.register(name, base, per)


def ensure_scene(scene):
    for g, _, _ in scene:
        ensure(g)


def rebuild(scene, T):
    """Collider scene [(name, t, x)] (left to right) -> my rebuilt row (asserted
    equal to theirs on the common span), evolved T steps, typed by my typer.
    Returns (objects [(name@phase, x, w)], row_T, origin)."""
    ensure_scene(scene)
    items, c0, same = xlate.check(scene, T=T)
    assert same, f"my rebuilt row differs from collider's for {scene}"
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = vlib.evolve(row, T)
    objs = [(n, x, w) for n, x, w, k in vlib.identify(r, org, T=T)]
    return objs, r, org


# Left-stream trains of round 3 (leftstream 05:40/05:46), as cells with left
# ether phase 0. Collider's Library auto-registers them under names
# v<v>s<slip>w<width> when it types a row containing them; teammates' seeds
# use those names. register_auto() reproduces that registration in CLIB
# (the definition is the cell string below, which I also hold in my own
# library as round-3 t1lib IL / ZL).
TRAINS = {"ZL": ("111110111110111000111011", 8),
          "IL": ("111110111110111110001110", 6)}


def register_auto(key):
    import collide
    from r110lib import ether_cells
    bits, slip = TRAINS[key]
    seg = np.array([int(c) for c in bits], np.uint8)
    row = np.concatenate([ether_cells(0, -300, 0), seg,
                          ether_cells(slip, len(seg), len(seg) + 300)])
    ok, prods, _ = collide.products_of(CLIB, row, -300, 0)
    assert ok and len(prods) == 1, prods
    return prods[0][0]
