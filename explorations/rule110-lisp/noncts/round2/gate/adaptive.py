"""Greedy choice of one designated zero-class per program slot so that a
FIXED program works for every input v in 0..VMAX (glider level).

Program = list of ops (letters, see stream.ALIAS). Input v = prefix of v
GB5's. Each program slot gets a class index c in {0,1,2} (relative to the
reference E at (0,0), applied only where the predecessors' slip is 0 mod 14,
i.e. where the counter can be at zero). The same c is used for every v, so
the program is data-independent; only physics (ether compatibility) shifts
positions with the prefix.

For slot s we try c = 0, 1, 2 and accept the first one for which every v
gives, after the packet has reacted, exactly one E-chain object with the
value predicted by the semantic model and only allowed garbage (objects
left of E moving left faster than E). Usage:
  python adaptive.py PROGRAM VMAX            -> prints the class list
"""
import sys
from common import LIB, CHAIN
from glidersim import GliderSim, Catalog, ThreeBody
from onesided import place
from r110lib import class_key
from collide import canonical_reps
from stream import ALIAS, horizon
from test_prog import OPS
from behave import velocity, VE

SPACING = 450
CAT = Catalog(LIB)


def place_phase(prev_state, name, target_x, t0):
    """Like onesided.place, but with the seed time fixed to -t0: the three
    choices t0 = 0, 1, 2 fall in the three different classes relative to
    any E (E vs G-speed has 3 classes; canonical reps differ by one step in
    t0), which is what we need when the E at zero has been displaced by left
    garbage and the reference-E class key is meaningless."""
    from r110lib import TILE
    g = LIB.gliders[name]
    pb, pl, pr, ps = prev_state
    c = (pr - ps) % TILE
    b, l, r, s_rel = g.state_at(-t0, 0, 0)
    base = (l - s_rel - c) % TILE
    lo = ps + len(pb) + 40 - s_rel
    x = lo + (base - lo) % TILE
    best = None
    for k in range(80):
        xx = x + TILE * k
        d = abs(xx + s_rel - target_x)
        if best is None or d < best[0]:
            best = (d, (-t0, xx))
    return best[1]


def build(ops, classes):
    E = LIB.gliders["E"]
    scene = [("E", 0, 0)]
    prev = E.state_at(0, 0, 0)
    slip = 0
    for op, c in zip(ops, classes):
        g = ALIAS[op]
        G = LIB.gliders[g]
        target = prev[3] + len(prev[0]) + SPACING
        if slip % 14 == 0 and c is not None:
            reps = canonical_reps(LIB, "E", g)
            key = class_key(reps[c], (E.p, E.d), (G.p, G.d))
            ev = place(prev, g, target, want_key=key)
        else:
            ev = place_phase(prev, g, target, c or 0)
        scene.append((g,) + ev)
        prev = G.state_at(ev[0], ev[1], 0)
        slip += G.slip
    return scene


def outcome(scene):
    """Final state after everything reacted, or None on 3-body/debris."""
    sim = GliderSim(LIB, scene, cat=CAT)
    try:
        sim.run(horizon(scene))
    except ThreeBody:
        return None, sim.log
    return sim.state(), sim.log


def good(state, expect):
    if state is None:
        return False
    es = [i for i, g in enumerate(state) if g[0] in CHAIN]
    if len(es) != 1 or CHAIN.index(state[es[0]][0]) != expect:
        return False
    # sim.state() is sorted by name, so check garbage by velocity only
    return all(velocity(g[0]) < VE for g in state if g[0] not in CHAIN)


def e_key(state):
    """(value, class key of the counter's seed event mod <P_E, P_G>)."""
    from r110lib import class_key as ck
    (g,) = [g for g in state if g[0] in CHAIN]
    return CHAIN.index(g[0]), ck((g[1], g[2]), (15, -4), (42, -14))


_REF = {}


def ref_key(n):
    """Class key of E^n's reference trajectory: E^n after I^(n-1) (GB5
    INCs, designated class) from E at (0,0), glider level."""
    if n not in _REF:
        st, _ = outcome(build(["I"] * (n - 1), [0] * (n - 1)))
        _REF[n] = e_key(st)[1]
    return _REF[n]


def search(prog, vmax, strict=False):
    classes = []
    for s, op in enumerate(prog):
        for c in (0, 1, 2):
            trial = classes + [c]
            ok = True
            seen = {}
            for v in range(vmax + 1):
                ops = ["I"] * v + list(prog[:s + 1])
                cls = [0] * v + trial
                exp = v
                for o in prog[:s + 1]:
                    exp = OPS[o](exp)
                st, log = outcome(build(ops, cls))
                if not good(st, exp):
                    ok = False
                    break
                if strict and op not in "JKLMP":
                    # the counter's trajectory class must depend on its value
                    # only (not on the history), else a fixed stream cannot
                    # serve later zero meetings of every history
                    n, k = e_key(st)
                    if k != ref_key(n + 1):
                        ok = False
                        break
            if ok:
                classes.append(c)
                print(f"slot {s} op {op}: class {c}", flush=True)
                break
        else:
            print(f"slot {s} op {op}: NO class works (v={v}, last log {log[-3:]})")
            return classes, False
    return classes, True


if __name__ == "__main__":
    prog = sys.argv[1]
    vmax = int(sys.argv[2])
    cl, ok = search(prog, vmax, strict="--strict" in sys.argv)
    print("classes", cl, "OK" if ok else "FAILED")
