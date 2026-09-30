"""The crossing counter driven by a FIXED stream.

Instructions (packets relative to T at the start of the slot):
  INC' = INC + one lane Ebar      DEC = DEC      NOP = c + 7 lane Ebars
All three drift T by the same element modulo L_FE = <P_F, P_Ebar>
(architect NOTES ~13:00), so in a periodic stream slot j can be placed at
T0 + j*delta for a fixed representative delta, independent of which
instructions ran before: the true T differs from the assumed one by a
lattice vector, which leaves every collision class unchanged.

Test: random programs; the placement uses only the slot index and the
instruction type; the prediction of the final register value is plain
arithmetic on n. Verified by full Rule 110 simulation."""
import random
import sys
from fractions import Fraction
from xcounter import INC, DEC
from winding3 import cross, lateral
from rx import run, LIB
from m1_predict import norm_seed
from r110lib import class_key

PF, PE = (36, -4), (30, -8)
LANE = ("Ebar", -14, 55)
C_ID = ("Ebar@(0,0)+Ebar@(-1,25)", -17, 67)
PROG = {"INC": INC + [LANE], "DEC": list(DEC), "NOP": [C_ID] + [LANE] * 7}
GAP = 20          # F periods between consecutive movers


def slot_plan(name, T_start, P_start):
    """Relative mover events for one instruction, computed from a standard
    start; returns (movers relative to T_start, T drift, P drift)."""
    T, P = T_start, P_start
    rel = []
    k = 0
    for mv in PROG[name]:
        k += GAP
        ev = (T[0] + mv[1] + k * PF[0], T[1] + mv[2] + k * PF[1])
        rel.append((mv[0], ev[0] - T_start[0], ev[1] - T_start[1]))
        r = cross(T, (mv[0],) + ev)
        assert r is not None
        T, outs = r
        for o in sorted(outs, key=lateral):
            rr = cross(P, o)
            assert rr is not None, (name, mv, o)
            P = rr[0]
    return rel, (T[0] - T_start[0], T[1] - T_start[1]), k


# standard plans from the value-0 state
STD = {nm: slot_plan(nm, (0, 0), (0, -43)) for nm in PROG}
DRIFT = {nm: STD[nm][1] for nm in PROG}
assert len({class_key(d, PF, PE) for d in DRIFT.values()}) == 1, DRIFT
DELTA = DRIFT["DEC"]
SLOT_LEN = max(STD[nm][2] for nm in PROG) + GAP     # in F periods


def build(program, n0=0):
    U = (-24, 12)
    D = (n0 * U[0], 43 + n0 * U[1])
    placements = [("F", 0, 0), ("F", -D[0], -D[1])]
    for j, nm in enumerate(program):
        base = (j * DELTA[0] + j * SLOT_LEN * PF[0], j * DELTA[1] + j * SLOT_LEN * PF[1])
        for name, dt, dx in STD[nm][0]:
            placements.append((name, base[0] + dt, base[1] + dx))
    return placements


def check(program, n0=0):
    n = n0 + program.count("INC") - program.count("DEC")
    pl = build(program, n0)
    prods = run(pl, 36 * (SLOT_LEN + 5) * len(program) + 8000)
    fs = sorted([norm_seed(*p) for p in prods if p[0] == "F"], key=lambda s: s[1] - s[0] / 9)
    junk = [p for p in prods if p[0] != "F" and LIB.gliders[p[0]].velocity != Fraction(-4, 15)]
    if len(fs) != 2 or junk:
        return False, f"F's {fs} junk {junk[:3]}"
    (tp, xp), (tt, xt) = fs
    D = (tt - tp, xt - xp)
    want = (n * -24, 43 + n * 12)
    same = class_key((D[0] - want[0], D[1] - want[1]), PF, (36, -4)) == (0, 0) or \
        ((D[0] - want[0]) % 36 == 0 and (D[1] - want[1]) == -4 * ((D[0] - want[0]) // 36))
    return same, f"n={n} D={D} want {want}"


if __name__ == "__main__":
    print("drifts", DRIFT, "slot length", SLOT_LEN, "F periods", flush=True)
    rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    ok = 0
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for i in range(trials):
        prog = []
        n = 0
        for _ in range(8):
            choices = ["INC", "NOP"] + (["DEC"] if n > 0 else [])
            c = rnd.choice(choices)
            n += (c == "INC") - (c == "DEC")
            prog.append(c)
        good, msg = check(prog)
        ok += good
        print(" ".join(prog), "->", "OK" if good else "FAIL", msg, flush=True)
    print(f"{ok}/{trials}")
