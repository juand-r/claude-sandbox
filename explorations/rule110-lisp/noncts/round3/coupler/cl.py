"""coupler toolkit: shared imports from round-2 gate/collider (read-only).

Scenes are lists of (name, t0, x0) seed events (collider conventions:
glider `name` phase 0 with bits[0] at column x0 at time t0).
- gsim(scene, T): glider-level simulation (collider catalog), returns sim
- ca(scene, T): exact Rule 110 (gate fastca moving window, margins checked
  every step) -> list of (name, t0, x0) products identified by collider's
  library (normalised so 0 <= t0 < p).
"""
import sys
sys.dont_write_bytecode = True
import os
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.abspath(os.path.join(HERE, "..", "..", "round2", "gate"))
sys.path.insert(0, GATE)
from common import LIB, CHAIN, canonical_reps, class_key, build_row  # noqa
from stream import build, ALIAS, ZCLASS  # noqa
from glidersim import GliderSim, ThreeBody  # noqa
from r110lib import TILE  # noqa
from collide import products_of  # noqa
from fastca import Window  # noqa
import numpy as np  # noqa


def G(name):
    return LIB.gliders[ALIAS.get(name, name)]


def norm(n, t0, x0):
    g = LIB.gliders[n]
    tt = t0 % g.p
    return (n, tt, x0 - (t0 - tt) // g.p * g.d)


def gsim(scene, T):
    sim = GliderSim(LIB, scene)
    sim.run(T)
    return sim


def window(scene):
    sts = [LIB.gliders[a].state_at(t, x, 0) for a, t, x in scene]
    row, x0 = build_row(sts, pad=200)
    first = min(sts, key=lambda s: s[3])
    last = max(sts, key=lambda s: s[3])
    return Window(row, x0, (first[1] - first[3]) % TILE, (last[2] - last[3]) % TILE)


def ident(w, pad=400):
    cells = w.cells(w.x0 - pad, w.x0 + len(w.row) + pad)
    ok, prods, _ = products_of(LIB, cells, w.x0 - pad, w.t)
    return ok, [norm(*p) if p[1] is not None else p for p in prods]


def ca(scene, T):
    w = window(scene).run(T)
    return ident(w)


def pos(g, t):
    """left column of glider g=(name,t0,x0) at time t"""
    b, l, r, s = LIB.gliders[g[0]].state_at(g[1], g[2], t)
    return s


def place_left_of(scene, name, target_end, t0=0):
    """Seed (t0, x) for `name` LEFT of the leftmost item of scene (at time 0),
    ether-compatible, its right end nearest target_end (>= 40 cells gap)."""
    first = min((LIB.gliders[a].state_at(t, x, 0) for a, t, x in scene), key=lambda s: s[3])
    nb, nl, nr, ns = first
    c = (nl - ns) % TILE
    b, l, r, s_rel = LIB.gliders[name].state_at(t0, 0, 0)
    hi = ns - 40 - len(b) - s_rel
    x = hi - ((hi - (r - s_rel - c)) % TILE)
    k = max(0, round((x + s_rel + len(b) - target_end) / TILE))
    return (t0, x - TILE * k)


_REPS = {}


def cls(X, sX, Y, sY):
    """Collision class index (collider canonical order) of X (left, faster)
    with seed sX against Y with seed sY."""
    if (X, Y) not in _REPS:
        gx, gy = LIB.gliders[X], LIB.gliders[Y]
        PX, PY = (gx.p, gx.d), (gy.p, gy.d)
        _REPS[(X, Y)] = [class_key(r, PX, PY) for r in canonical_reps(LIB, X, Y)], PX, PY
    keys, PX, PY = _REPS[(X, Y)]
    k = class_key((sY[0] - sX[0], sY[1] - sX[1]), PX, PY)
    return keys.index(k)


IL_BITS = "111110111110111110001110"   # leftstream's INC-from-left train (board 05:40)
IL_TAIL = "1110001001101111100011110000110111"  # their claim_inc.py: E at seed (7,44) follows


def train_IL():
    """leftstream's I_L train as a seed in this library, exactly as in
    leftstream/claim_inc.py: cells IL_BITS+IL_TAIL at x=0.., t=0, left ether
    phase 0, right phase 1; the row parses as [train, E(7,44)]."""
    from r110lib import ether_cells
    seg = np.array([int(c) for c in IL_BITS + IL_TAIL], np.uint8)
    row = np.concatenate([ether_cells(0, -300, 0), seg, ether_cells(1, len(seg), len(seg) + 300)])
    ok, prods, _ = products_of(LIB, row, -300, 0)
    prods = [norm(*p) for p in prods]
    assert len(prods) == 2 and prods[1] == ("E", 7, 44), prods
    return prods[0]


def place_right_of(scene, name, target_start, t0=0):
    """Seed (t0, x) for `name` RIGHT of the rightmost item of scene (time 0),
    ether-compatible, start column nearest target_start (>= 40 cells gap)."""
    last = max((LIB.gliders[a].state_at(t, x, 0) for a, t, x in scene), key=lambda s: s[3])
    pb, pl, pr, ps = last
    c = (pr - ps) % TILE
    b, l, r, s_rel = LIB.gliders[name].state_at(t0, 0, 0)
    base = (l - s_rel - c) % TILE
    lo = ps + len(pb) + 40 - s_rel
    x = lo + (base - lo) % TILE
    k = max(0, round((target_start - (x + s_rel)) / TILE))
    return (t0, x + TILE * k)
