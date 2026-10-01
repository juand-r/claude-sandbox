"""Two-register F lane driven by a FIXED stream (no history-dependent
placement). Every instruction is padded with NOP walks (label (0,0)) so
that all instructions drift the front marker T by the same class modulo
L_FE = <P_F, P_Ebar>; slot j is then placed at j*(DELTA + SLOT*P_F),
using only j and the instruction type (architect's xstream principle: a
lattice difference in T's true position only translates collisions).
Verified by full Rule 110 simulation; the predicted register values are
plain arithmetic on the program."""
import sys, random
from fractions import Fraction
import gen
gen.ABSORB = True
from gen import cross_chain, LIB
from lane import KEY
from rx import run, norm
import tworeg_abs as T2

PF = (36, -4)
GAP = T2.GAP
BASE = T2.OPS
NOP_A = BASE["DN2"] + BASE["UP2"]          # label (0,0)
NOP_B = BASE["DN1"] + BASE["UP1"]          # label (0,0)


def drift_and_rel(seq):
    """Relative mover events (to the standard start T=(0,0)) and T drift."""
    m = T2.start_markers()
    rel, delay = [], 0
    for name, t, x in seq:
        delay += GAP
        T = m[0]
        ev = (T[0] + t + delay * PF[0], T[1] + x + delay * PF[1])
        rel.append((name,) + ev)
        m = cross_chain(["F"] * 3, m, (name,) + ev)[0]
    return rel, m[0], delay


def padded(op, pads):
    a, b = pads[op]
    return BASE[op] + NOP_A * a + NOP_B * b


def find_pads():
    """smallest (a, b) per op so that all drift keys coincide."""
    best = None
    for target in BASE:
        pads = {}
        tk = None
        for op in [target] + [o for o in BASE if o != target]:
            for tot in range(0, 9):
                hit = None
                for a in range(0, tot + 1):
                    b = tot - a
                    k = KEY(drift_and_rel(BASE[op] + NOP_A * a + NOP_B * b)[1])
                    if tk is None and op == target and tot == 0:
                        tk = k
                    if k == tk:
                        hit = (a, b)
                        break
                if hit:
                    pads[op] = hit
                    break
        cost = sum(len(padded(o, pads)) for o in pads) if len(pads) == 4 else 10 ** 9
        if best is None or cost < best[0]:
            best = (cost, pads)
    return best[1]


PADS = find_pads()
STD = {op: drift_and_rel(padded(op, PADS)) for op in BASE}
DELTA = STD["DN1"][1]
assert len({KEY(STD[o][1]) for o in STD}) == 1, {o: KEY(STD[o][1]) for o in STD}
# idle F periods between slots: the stream distance between slots must
# exceed the spread of T's drift (kicks move T by up to ~1000 cells per
# slot); only the drift difference of the PREVIOUS slot matters.
EXTRA = 150
SLOT = max(STD[o][2] for o in STD) + GAP + EXTRA


def build(program):
    pl = [("F",) + m for m in T2.start_markers()]
    for j, op in enumerate(program):
        base = (j * (DELTA[0] + SLOT * PF[0]), j * (DELTA[1] + SLOT * PF[1]))
        for name, t, x in STD[op][0]:
            pl.append((name, base[0] + t, base[1] + x))
    return pl


def check(program):
    pl = build(program)
    prods = run(pl, 36 * SLOT * (len(program) + 1) + 8000)
    fs = sorted((norm(*p) for p in prods if p[0] == "F"), key=T2.xpos)
    junk = sorted({p[0] for p in prods if p[0] != "F" and LIB.gliders[p[0]].velocity != Fraction(-4, 15)})
    got = [round(g, 2) for g in T2.gaps_of(fs)]
    want = [round(g, 2) for g in T2.predicted_gaps(program)]
    return got == want and not junk and len(fs) == 3, got, want, junk


if __name__ == "__main__":
    print("pads", PADS, "slot", SLOT, "F periods; movers per op", {o: len(STD[o][0]) for o in STD}, flush=True)
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    L = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    rnd = random.Random(seed)
    ok = 0
    for i in range(n):
        prog = [rnd.choice(list(BASE)) for _ in range(L)]
        good, got, want, junk = check(prog)
        ok += good
        print(" ".join(prog), "->", "OK" if good else "FAIL", "gaps [reg2, reg1]", got, "want", want, "junk", junk, flush=True)
    print(f"{ok}/{n}")


def control_unbalanced(program):
    """Negative control: same fixed-stream construction but WITHOUT the NOP
    padding (drift classes differ between instructions). Must fail for
    programs whose earlier instructions have a different drift class."""
    global STD, DELTA
    saved = (STD, DELTA)
    STD = {op: drift_and_rel(BASE[op]) for op in BASE}
    DELTA = STD["DN1"][1]
    try:
        return check(program)
    finally:
        STD, DELTA = saved
