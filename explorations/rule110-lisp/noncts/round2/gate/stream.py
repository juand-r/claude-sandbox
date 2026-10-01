"""Build fixed G-speed packet streams against an E counter and run them.

Placement rule (data-independent): the counter starts as E at (0,0). Packets
are placed at t = 0, left to right, `spacing` cells apart (ether-compatible).
A packet P whose predecessors have total slip 0 mod 14 (the only slots where
the counter can be at zero, by slip conservation) is put in its DESIGNATED
class relative to the reference E at (0,0) (class index into
canonical_reps(LIB, "E", P)); other packets go at the nearest position. The input value
v is written by a prefix of v INC packets (GB5, class-free), so the same
program text is placed by the same rule for every v.

run(scene) simulates with collider's glidersim (catalog, exact event
arithmetic) AND with the exact automaton (engine.step, cell for cell), and
checks they agree (as ecounter.run_gb does).
"""
import numpy as np

from common import LIB, CHAIN, engine, canonical_reps, class_key, build_row
from glidersim import GliderSim, ThreeBody  # noqa: F401
from onesided import place
from regions import free_row
from r110lib import TILE

# designated zero classes (index into canonical_reps(LIB, "E", P))
ZCLASS = {
    "GB3": 0,                              # DEC; zero -> E + A
    "GB4": 1,                              # NOP (class-free)
    "GB5": 0,                              # INC (class-free)
    "GB3@(0,0)+GB4@(-25,46)": 0,           # Z6: DEC, zero -> E^7 (wrap)
    "GB3@(0,0)+GB5@(-14,40)": 0,           # W7: NOP, zero -> E^8
    "GB5@(0,0)+GB4@(-4,56)": 2,            # X8: INC, zero -> E^9
    "GB1@(0,0)+GB1@(-1,36)": 1,            # J: INC, zero -> Bbar (left) + E
}
ALIAS = {"I": "GB5", "N": "GB4", "D": "GB3",
         "Z": "GB3@(0,0)+GB4@(-25,46)", "W": "GB3@(0,0)+GB5@(-14,40)",
         "X": "GB5@(0,0)+GB4@(-4,56)", "J": "GB1@(0,0)+GB1@(-1,36)",
         "K": "GB1@(0,0)+GB1@(-31,58)", "L": "GB1@(0,0)+GB1@(-4,34)",
         "M": "GB1@(0,0)+GB1@(-40,52)", "P": "GB1@(0,0)+GB1@(-41,56)"}


def build(program, spacing=450, zclass=None):
    """program: list of packet names (or one-letter aliases)."""
    zc = dict(ZCLASS)
    zc.update(zclass or {})
    E = LIB.gliders["E"]
    scene = [("E", 0, 0)]
    prev = E.state_at(0, 0, 0)
    slip = 0          # total slip of the packets placed so far (mod 14)
    for p in program:
        g = ALIAS.get(p, p)
        G = LIB.gliders[g]
        key = None
        # a packet can meet the zero state E only if the packets before it
        # have total slip 0 mod 14 (slip conservation); only then is its
        # class relative to the reference E meaningful and needed
        if slip % 14 == 0 and zc.get(g) is not None:
            reps = canonical_reps(LIB, "E", g)
            key = class_key(reps[zc[g]], (E.p, E.d), (G.p, G.d))
        ev = place(prev, g, prev[3] + len(prev[0]) + spacing, want_key=key)
        scene.append((g,) + ev)
        prev = G.state_at(ev[0], ev[1], 0)
        slip += G.slip
    return scene


def horizon(scene):
    last = LIB.gliders[scene[-1][0]].state_at(scene[-1][1], scene[-1][2], 0)
    return int(15 * (last[3] + 80)) + 1500   # G closes on E at 1/15 cell/gen


def ca_check(scene, sim, T):
    """Exact automaton (fastca moving window, cross-checked against
    ../../engine.py in test_fastca.py) vs the glidersim prediction at time T,
    cell for cell over the whole non-ether region."""
    from fastca import Window
    sts = [LIB.gliders[a].state_at(t, x, 0) for a, t, x in scene]
    row, x0 = build_row(sts, pad=200)
    first = min(sts, key=lambda s: s[3])
    last = max(sts, key=lambda s: s[3])
    cL0 = (first[1] - first[3]) % TILE
    cR0 = (last[2] - last[3]) % TILE
    # build_row's row is cyclic with a clean wrap; cut it to [x0, x0+W)
    w = Window(row, x0, cL0, cR0).run(T)
    pred_sts = [LIB.gliders[n].state_at(t0, xx, T) for n, t0, xx in sim.gl]
    lo = min([w.x0] + [s[3] for s in pred_sts]) - 100
    hi = max([w.x0 + len(w.row)] + [s[3] + len(s[0]) for s in pred_sts]) + 100
    pred = free_row(LIB, sim.gl, T, lo, hi - lo, cL0)
    return pred is not None and bool(np.array_equal(pred, w.cells(lo, hi)))


def run(scene, T=None, ca=True):
    """-> (final glider list (glidersim), log, CA agrees?)."""
    T = T or horizon(scene)
    sim = GliderSim(LIB, scene)
    sim.run(T)
    ok = None
    if ca == "fast":
        return sim.state(), sim.log, ca_check(scene, sim, T)
    if ca:
        sts = [LIB.gliders[a].state_at(t, x, 0) for a, t, x in scene]
        row, x0 = build_row(sts, pad=T + 200)
        for _ in range(T):
            row = engine.step(row)
        left = min(sts, key=lambda s: s[3])
        pred = free_row(LIB, sim.gl, T, x0, len(row), (left[1] - left[3]) % TILE)
        ok = pred is not None and bool(np.array_equal(pred, row))
    return sim.state(), sim.log, ok


def counter_of(state):
    es = [g for g in state if g[0] in CHAIN]
    return [CHAIN.index(g[0]) for g in es], [g[0] for g in state if g[0] not in CHAIN]
