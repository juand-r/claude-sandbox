"""One-sided counter demo: E^n driven entirely from the right.

Stream (arrival order): B = INC; G then B^3 = DEC (answer A^3 if the
counter was nonzero, annihilated by the B^3; A^4 if zero, which the B^3
turns into a single A that deletes the next B of the stream).
All items are placed at t = 0 in one row (a FIXED stream, no
history-dependent placement except that the zero-testing G is chosen in
class 0 of E+G). Checked with glidersim (catalog) and with the automaton
cell for cell.
"""
import os
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import engine  # noqa: E402

from collide import canonical_reps  # noqa: E402
from glidersim import GliderSim  # noqa: E402
from predict import LIB  # noqa: E402
from r110lib import TILE, build_row, class_key  # noqa: E402
from regions import free_row  # noqa: E402

VE = Fraction(-4, 15)


def place(prev_state, name, target_x, want_key=None):
    """Seed event (t0 in [0,p), x0) for `name` at t=0 right of prev_state,
    ether-compatible, start column nearest target_x (>= prev end + 40).
    If want_key is given, require class_key(-(t0, x0)) (E at (0,0) as X,
    this glider as Y) to equal it."""
    g = LIB.gliders[name]
    pb, pl, pr, ps = prev_state
    c = (pr - ps) % TILE
    best = None
    for t0 in range(g.p):
        b, l, r, s_rel = g.state_at(-t0, 0, 0)     # seed at (-t0, x)
        base = (l - s_rel - c) % TILE
        lo = ps + len(pb) + 40 - s_rel
        x = lo + (base - lo) % TILE
        for k in range(60):
            xx = x + TILE * k
            if want_key is not None:
                E = LIB.gliders["E"]
                if class_key((-t0, xx), (E.p, E.d), (g.p, g.d)) != want_key:
                    continue
            d = abs(xx + s_rel - target_x)
            if best is None or d < best[0]:
                best = (d, (-t0, xx))
    if best is None:
        raise ValueError(f"cannot place {name}")
    return best[1]


def build(program, gap=400):
    """program: string of 'I' (B) and 'D' (G + B^3). Items are placed at
    t = 0 in arrival order; a faster item behind a slower one (B or B^3
    behind G) is placed far enough back that it cannot catch the G before
    the G has reacted (so spacings grow; see the board post)."""
    E = LIB.gliders["E"]
    G = LIB.gliders["G"]
    key0 = class_key(canonical_reps(LIB, "E", "G")[0], (E.p, E.d), (G.p, G.d))
    scene = [("E", 0, 0)]
    prev = E.state_at(0, 0, 0)
    T_prev = 0
    last_g = None          # (x at t=0, reaction time) of the last G
    n = 1
    for op in program:
        items = ["B"] if op == "I" else ["G", "B^3"]
        for name in items:
            v = LIB.gliders[name].velocity
            T = T_prev + gap
            tx = (VE - v) * T + 15
            if last_g is not None and v < Fraction(-1, 3):
                # must not catch the G (relative speed 1/6) before it reacts
                tx = max(tx, last_g[0] + (last_g[1] + 100) / 6 + 40)
            want = key0 if (name == "G" and n == 1) else None
            ev = place(prev, name, int(tx), want)
            scene.append((name,) + ev)
            prev = LIB.gliders[name].state_at(ev[0], ev[1], 0)
            T_arr = int(prev[3] / (VE - v)) if v != VE else T
            if name == "G":
                last_g = (prev[3], T_arr)
            T_prev = max(T_prev, T_arr)
        if op == "I":
            n += 1
        elif n > 1:
            n -= 1
    return scene, T_prev + 1500


def check(program):
    scene, T = build(program)
    sim = GliderSim(LIB, scene)
    sim.run(T)
    sts = [LIB.gliders[a].state_at(t, x, 0) for a, t, x in scene]
    row, x0 = build_row(sts, pad=T + 200)
    for _ in range(T):
        row = engine.step(row)
    left = min(sts, key=lambda s: s[3])
    pred = free_row(LIB, sim.gl, T, x0, len(row), (left[1] - left[3]) % TILE)
    ok = pred is not None and np.array_equal(pred, row)
    return sim.state(), [(l[2], l[3], l[5]) for l in sim.log], ok


if __name__ == "__main__":
    for prog in sys.argv[1:] or ["D", "DI", "ID", "IDI", "IID", "IIDD", "IIDDD", "IIDDDI"]:
        st, log, ok = check(prog)
        print(prog, "CA==glidersim:", ok, "final:", st)
        print("   log:", log)
