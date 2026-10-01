"""History test for R1 -> R2 couplings: a fixed right program where input
v1 = 0 couples TWICE (J at slots 0 and 9) and v1 = 5 couples only at
slot 9 (both reach R1 = 0 there through Z6 wraps / DECs):
    J I Z Z Z Z Z Z Z J I N N
model (R1, R2 changes): v1 = 0: J(zero: R2 += 2) I (1) echo (0), Z^7: 0
-> 6 -> ... -> 0, J (zero: R2 += 2) I echo -> R1 0, R2 + 4.
v1 = 5: J -> 6, I -> 7, Z^7 -> 0, J (zero: R2 += 2), I, echo -> 0, R2 + 2.
R2 = E raised to v2 by I_L's (left stream, before everything).
Greedy per-slot class choice (rafast text, classes = seed time phase) at
glider level over both inputs; a slot's class is accepted if, after the
packet (and any echo) has acted, every input shows exactly two E-chain
objects with the model's values. Then the final program is run in the
exact CA. Usage: python repeat.py [v2] [PROG V1,V1,..]"""
import sys
from two import *  # noqa

PROG = "JIZZZZZZZJINN"
V1S = (0, 5)


def model(v1, v2, upto):
    r1, r2, pend = v1, v2, False
    for i, op in enumerate(PROG[:upto]):
        if op == "J":
            if r1 == 0:
                r2 += 2
                pend = True       # echo will DEC R1 after the next I
            else:
                r1 += 1
        elif op == "I":
            r1 += 1
            if pend:
                r1 -= 1
                pend = False
        elif op == "Z":
            r1 = r1 - 1 if r1 else 6
        elif op == "N":
            pass
    return r2, r1


def scene(v1, v2, classes):
    items = r1_program(PROG[:len(classes)], classes)
    sc = r1_scene(v1, items)
    r2 = ("E",) + place_left_of(sc, "E", -1500, 2)
    ls = left_stream("i" * v2, r2[1:], t0=400)
    return ls + [r2] + sc, 15 * (sc[-1][2] + 3000)


def outcome(state):
    if len(state) != 2 or any(g[0] not in CHAIN for g in state):
        return None
    a, b = sorted(state, key=lambda g: pos(g, 0))
    return CHAIN.index(a[0]), CHAIN.index(b[0])


def greedy(v2, forced=None):
    """Slot by slot; a J and the I after it are chosen together (the J's
    echo can only be judged after that I)."""
    import itertools
    classes = []
    s = 0
    while s < len(PROG):
        width = 2 if PROG[s] == "J" else 1
        ok_c = None
        opts = [(forced[s],)] if forced and s in forced else itertools.product((0, 1, 2), repeat=width)
        for cs in opts:
            trial = classes + list(cs)
            good = True
            for v1 in V1S:
                sc, T = scene(v1, v2, trial)
                sim, err = run(sc, T)
                if err or outcome(sim.state()) != model(v1, v2, s + width):
                    good = False
                    break
            if good:
                ok_c = cs
                break
        if ok_c is None:
            print("slot", s, PROG[s:s + width], ": no class works", flush=True)
            return classes, False
        classes += list(ok_c)
        print("slot", s, PROG[s:s + width], "classes", ok_c, flush=True)
        s += width
    return classes, True


if __name__ == "__main__":
    extend_chain(24)
    v2 = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    forced = {}
    if len(sys.argv) > 2:
        PROG = sys.argv[2]
        V1S = tuple(int(a) for a in sys.argv[3].split(","))
    if len(sys.argv) > 4:          # forced classes "slot:c,slot:c"
        for kv in sys.argv[4].split(","):
            a, b = kv.split(":")
            forced[int(a)] = int(b)
    cl, ok = greedy(v2, forced)
    print("classes", cl, "OK" if ok else "FAILED")
    if ok:
        for v1 in V1S:
            sc, T = scene(v1, v2, cl)
            okc, prods = ca(sc, T)
            print("CA v1=%d:" % v1, [p[0] for p in prods], "model", model(v1, v2, len(PROG)),
                  "ca", outcome(prods))
