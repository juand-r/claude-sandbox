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


PE = (15, -4)
IL_DELTA = (7, -8)     # leftstream: I_L front displacement (lpk.py)
ZL_DELTA = (9, 0)      # leftstream: Z_L front displacement, both branches
A_DELTA = (5, 2)       # leftstream: A (DEC) front displacement


def left_packets():
    """leftstream's packets in THIS library: name -> (seeds, E seed, delta)."""
    il, ile = train_from_record("sat_inc_results.jsonl", 6)
    zl, zle = train_from_record("sat_zero_results.jsonl", 1)
    return {"i": (il, ile, IL_DELTA), "z": (zl, zle, ZL_DELTA),
            "d": ([("A", 1, -64)], (0, 7), A_DELTA)}


def left_stream(prog, e0, t0, gap=150, pk=None):
    """leftstream's rigid placement rule (lstream.place_program), in this
    library: packet i = its reference scene translated so that its E sits
    at the virtual front e (e0 + earlier deltas), then moved m*P_E so it
    arrives about t0 + i*gap. Seeds do not depend on the counter value."""
    pk = pk or left_packets()
    e = tuple(e0)
    out = []
    for i, X in enumerate(prog):
        seeds, pe, dl = pk[X]
        tr = (e[0] - pe[0], e[1] - pe[1])
        m = (t0 + i * gap - tr[0]) // PE[0]
        for nm, t, x in seeds:
            out.append(norm(nm, t + tr[0] + m * PE[0], x + tr[1] + m * PE[1]))
        e = (e[0] + dl[0], e[1] + dl[1])
    return out
