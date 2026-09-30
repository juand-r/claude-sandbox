"""The extendible E as a unary counter: E^n (n >= 1) moving at -4/15.

INC: B + E^n -> E^(n+1)   single class, so any B timing works.
DEC: A + E^n -> E^(n-1)   in one of the 3 (A, E^n) classes;
     on n = 1 the same A gives C3 (zero detected, counter consumed).

Bookkeeping (derived from the catalog with predict.py and checked below
by direct simulation): keep the counter's "reference" = the trajectory
the E^n would have if all operations were INCs from the initial E. A DEC
moves the counter off the reference by DEC_SHIFT (mod the E period); INC
does not. So the class that decrements depends on d = number of DECs so
far (mod 3). plan_dec(d) returns an A seed event (relative to the
initial E at (0,0)) that decrements for every n given d.

run(ops) builds the whole scene (initial E, B's from the right, A's from
the left, spaced so that the reactions are sequential) and simulates it
with the reference engine; it returns the final gliders.
Usage: python ecounter.py "IIIDDDD"
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", ".."))
import engine  # noqa: E402

from collide import canonical_reps, products_of  # noqa: E402
from predict import LIB, norm, predict  # noqa: E402
from r110lib import build_row, class_key  # noqa: E402

CHAIN = ["E"] + [f"E^{n}" for n in range(2, 10)]


def chain_events():
    """Reference events of E^n (INC-only history from E at (0,0))."""
    ev = {1: norm("E", 0, 0)}
    e = (0, 0)
    for n in range(1, len(CHAIN)):
        rep = canonical_reps(LIB, CHAIN[n - 1], "B")[0]
        _, prods = predict(CHAIN[n - 1], "B", rep, eX=e)
        assert len(prods) == 1 and prods[0][0] == CHAIN[n]
        e = prods[0][1:]
        ev[n + 1] = prods[0]
    return ev


def dec_table():
    """For each A-class c (relative to the initial E) and each n: the
    outcome of A + E^n at the reference position."""
    ev = chain_events()
    out = {}
    for c, r in enumerate(canonical_reps(LIB, "A", "E")):
        a = (-r[0], -r[1])
        for n, (nm, t, x) in ev.items():
            _, prods = predict("A", nm, (t - a[0], x - a[1]), eX=a)
            out[(c, n)] = (a, prods)
    return ev, out


def main(ops):
    ev, tab = dec_table()
    good = [c for c in range(3)
            if all(tab[(c, n)][1] and tab[(c, n)][1][0][0] == CHAIN[n - 2]
                   for n in range(2, 10))]
    print("A-classes that decrement E^2..E^9 at the reference:", good)
    for c in range(3):
        print(f"  class {c}:", " ".join(
            f"{n}->{'+'.join(p[0] for p in tab[(c, n)][1])}" for n in range(1, 10)))
    # shift of the counter caused by one DEC (reference class)
    c = good[0]
    a, prods = tab[(c, 3)]
    got = prods[0]
    ref = ev[2]
    print("DEC product", got, "reference", ref)


if __name__ == "__main__" and (len(sys.argv) < 2 or sys.argv[1] != "hist"):
    main(sys.argv[1] if len(sys.argv) > 1 else "")


def step(state, op):
    """Symbolic counter step. state = (n, event of E^n (normalized)).
    op 'I' (B from the right) or 'D' (A from the left, in the class that
    decrements). Returns (new state, A-class index relative to the
    REFERENCE E at (0,0) for a D op, or None)."""
    n, e = state
    nm = CHAIN[n - 1]
    if op == "I":
        rep = canonical_reps(LIB, nm, "B")[0]
        _, prods = predict(nm, "B", rep, eX=e)
        assert [p[0] for p in prods] == [CHAIN[n]]
        return (n + 1, prods[0][1:]), None
    want = [CHAIN[n - 2]] if n >= 2 else ["C3"]
    reps = canonical_reps(LIB, "A", nm)
    for rep in reps:
        a = (e[0] - rep[0], e[1] - rep[1])
        _, prods = predict("A", nm, rep, eX=a)
        if [p[0] for p in prods] == want:
            c = a      # the A's seed event (absolute)
            if n == 1:
                return (0, None), c
            return (n - 1, prods[0][1:]), c
    raise AssertionError(f"no decrementing A class for {nm}")


def classes_by_history(max_len=8):
    """For every op sequence (never DEC below zero), the seed events of the
    DEC A's; consecutive A's (a_i then a_(i+1), arriving later, further
    left) have a relative vector a_i - a_(i+1). Returns the set of its
    classes modulo <P_A, P_E> (fractional coordinates), per history."""
    import itertools
    from r110lib import class_key
    PA, PE = (3, 2), (15, -4)
    keys = set()
    first = set()
    for L in range(1, max_len + 1):
        for ops in itertools.product("ID", repeat=L):
            st = (1, (0, 0))
            prev = None
            for op in ops:
                if st[0] == 0 or (op == "I" and st[0] >= 9):
                    break
                st, a = step(st, op)
                if op == "D":
                    if prev is None:
                        first.add(class_key((0 - a[0], 0 - a[1]), PA, PE))
                    else:
                        keys.add(class_key((prev[0] - a[0], prev[1] - a[1]),
                                           PA, PE))
                    prev = a
    return first, keys


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "hist":
    print(classes_by_history(int(sys.argv[2]) if len(sys.argv) > 2 else 8))


def build_scene(ops, gap=250, t0=150):
    """Glider scene realizing the op string on a counter starting as E at
    (0,0): op i reacts at about generation t0 + gap*i. Returns (scene,
    expected final counter (name, t, x) or ('C3', ...))."""
    import json
    from regions import key as rkey
    reg = json.load(open("regions.json"))
    rows = {}
    for r in json.load(open("collisions.json")):
        rows[(r["X"], r["Y"], r["cls"])] = r
    scene = [("E", 0, 0)]
    st = (1, (0, 0))
    for i, op in enumerate(ops):
        target = t0 + gap * i
        n, e = st
        nm = CHAIN[n - 1]
        if op == "I":
            rep = canonical_reps(LIB, nm, "B")[0]
            t_lo = reg[rkey(rows[(nm, "B", 0)])][0]
            # B at e + rep + b*P_E: reaction at e[0] + t_lo + 15b
            b = round((target - e[0] - t_lo) / 15)
            scene.append(("B", e[0] + rep[0] + 15 * b, e[1] + rep[1] - 4 * b))
        else:
            want = [CHAIN[n - 2]] if n >= 2 else ["C3"]
            for k, rep in enumerate(canonical_reps(LIB, "A", nm)):
                _, prods = predict("A", nm, rep, eX=(e[0] - rep[0], e[1] - rep[1]))
                if [p[0] for p in prods] == want:
                    break
            t_lo = reg[rkey(rows[("A", nm, k)])][0]
            # A at e - rep - b*P_E: reaction at e[0] - rep[0] - 15b + t_lo
            b = round((e[0] - rep[0] + t_lo - target) / 15)
            scene.append(("A", e[0] - rep[0] - 15 * b, e[1] - rep[1] + 4 * b))
        st, _ = step(st, op)
    if st[0] == 0:
        return scene, ("C3",)
    return scene, norm(CHAIN[st[0] - 1], *st[1])


def verify_ops(ops, gap=250):
    """Simulate the scene with glidersim (catalog) and with the automaton
    (cell-exact); return the final glider list."""
    import numpy as np
    from glidersim import GliderSim
    from regions import free_row
    from r110lib import TILE
    scene, expect = build_scene(ops, gap)
    T = 150 + gap * len(ops) + 400
    sim = GliderSim(LIB, scene)
    sim.run(T)
    sts = [LIB.gliders[n].state_at(t, x, 0) for n, t, x in scene]
    row, x0 = build_row(sts, pad=T + 200)
    for _ in range(T):
        row = engine.step(row)
    left = min(sts, key=lambda s: s[3])      # far-left ether phase
    pred = free_row(LIB, sim.gl, T, x0, len(row), (left[1] - left[3]) % TILE)
    assert pred is not None and np.array_equal(pred, row), "CA != glidersim"
    return sim.state(), expect


# ---------------------------------------------------------------------------
# One-sided access: INC = B, DEC = G, both from the right.

def gstep(state, op):
    """state = (n, event). 'I' = B, 'G' = G (DEC for n >= 2; for n = 1 the
    zero test, which needs class 0 of E+G: E survives, A^4 answers).
    Returns (new state, answer products)."""
    n, e = state
    nm = CHAIN[n - 1]
    if op == "I":
        rep = canonical_reps(LIB, nm, "B")[0]
        _, prods = predict(nm, "B", rep, eX=e)
        return (n + 1, prods[0][1:]), []
    reps = canonical_reps(LIB, nm, "G")
    outs = []
    for rep in reps:
        _, prods = predict(nm, "G", rep, eX=e)
        outs.append(prods)
    return outs


def g_history_check(max_len=10):
    """For every I/G history (n stays in 1..9): (1) DEC by G gives the same
    E^(n-1) event for every G class; (2) collect the E-trajectory classes
    (mod <P_E, P_G>) at which zero tests happen."""
    import itertools
    PE, PG = (15, -4), (42, -14)
    zero_keys = set()
    for L in range(1, max_len + 1):
        for ops in itertools.product("IG", repeat=L):
            st = (1, (0, 0))
            for op in ops:
                n, e = st
                if op == "I":
                    if n >= 9:
                        break
                    st, _ = gstep(st, "I")
                    continue
                if n == 1:
                    zero_keys.add(class_key(e, PE, PG))
                    break
                outs = gstep(st, "G")
                evs = {tuple(p for p in o if p[0].startswith("E")) for o in outs}
                assert len(evs) == 1, (ops, outs)
                (ev,) = evs
                assert ev[0][0] == CHAIN[n - 2]
                st = (n - 1, ev[0][1:])
    return zero_keys
