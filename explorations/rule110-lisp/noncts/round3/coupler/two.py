"""Two-counter scenes: R2 = E^(m+1) on the left, R1 = E^(v+1) on the right
driven by a fixed G-speed program (round-2 rafast conventions).

R1 input: canonical prefix E(0,0) + v GB5's (round-2 gate rafast.input_prefix);
R1 program: fixed text (rafast.Program, slot classes c = seed-time phase),
x-shifted by rafast.shift_for(prefix) for ether compatibility.
R2: E^(m+1) left of E(0,0); its right end is placed by place_left_of with
target_end = -gap and seed time t0 (search over t0 picks its class).
"""
from cl import *  # noqa
import rafast
from rafast import Program, input_prefix, shift_for

OPNAME = {"I": "GB5", "N": "GB4", "D": "GB3", **{k: v for k, v in ALIAS.items()}}


def r1_program(ops, classes):
    P = Program()
    for op, c in zip(ops, classes):
        P.add(op, c)
    return P.items


def r1_scene(v, items):
    pre = input_prefix(v)
    D = shift_for(pre, items[0])
    return pre + [(n, t, x + D) for n, t, x in items]


def with_r2(scene, m, gap, t0):
    name = CHAIN[m]
    return [(name,) + place_left_of(scene, name, -gap, t0)] + scene


def run(scene, T):
    sim = GliderSim(LIB, scene)
    err = None
    try:
        sim.run(T)
    except ThreeBody as e:
        err = str(e)
    return sim, err


def counters(state):
    return [(CHAIN.index(g[0]), g) if g[0] in CHAIN else (None, g) for g in state]
