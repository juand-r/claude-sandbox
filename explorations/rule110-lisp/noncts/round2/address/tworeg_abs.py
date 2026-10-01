"""Two independently addressable registers in ONE F lane (3 F markers),
using movers that may be ABSORBED by a marker (F + Ebar pair -> F).

Markers T (front) > M > P. reg1 = gap T-M, reg2 = gap M-P. Start residues
D1 ~ (20,61), D2 ~ (13,61) (absorb graph node), plus slack.
Instructions (closed walks of absorb_walks*.py, labels in P_Ebar units;
label +1 = gap -4.67 cells):
  DN2 = (0,+4)   UP2 = (0,-4)   DN1 = (+4,0)   UP1 = (-4,0)
Each mover is placed relative to the CURRENT T (catalog prediction), GAP
F periods after the previous one (relative placement, as architect's
xcounter.schedule). Verified by full Rule 110 simulation (collider
simulate): the three F's must be exactly where predicted, and the only
other products must be Ebar-speed gliders."""
import sys, random
from fractions import Fraction
import gen
gen.ABSORB = True
from gen import cross_chain, LIB
from rx import run, norm

PF, PE = (36, -4), (30, -8)
GAP = 20
K0 = ('Ebar@(0,0)+Ebar@(-9,29)', 0, 55)
W12 = [('Ebar@(0,0)+Ebar@(-12,27)', -17, 67), ('Ebar@(0,0)+Ebar@(-16,29)', -16, 63),
       ('Ebar@(0,0)+Ebar@(-26,27)', -7, 55)]                       # (0,-12)
W_4m4 = [('Ebar@(0,0)+Ebar@(-27,45)', -17, 67), ('Ebar@(0,0)+Ebar@(-12,27)', -12, 61),
         ('Ebar@(0,0)+Ebar@(-16,29)', -16, 63), ('Ebar', -12, 61), K0]  # (4,-4)
W_m4m8 = [('Ebar@(0,0)+Ebar@(-17,47)', -17, 67), ('Ebar@(0,0)+Ebar@(-26,27)', -7, 55),
          ('Ebar@(0,0)+Ebar@(-12,27)', -16, 63), ('Ebar@(0,0)+Ebar@(-16,29)', -16, 63),
          ('Ebar@(0,0)+Ebar@(-26,27)', -7, 55)]                     # (-4,-8)
OPS = {
    "DN2": [K0],                         # (0, 4)
    "UP2": W12 + [K0, K0],               # (0,-4)
    "DN1": W_4m4 + [K0],                 # (4, 0)
    "UP1": W_m4m8 + [K0, K0],            # (-4, 0)
}
LABEL = {"DN2": (0, 4), "UP2": (0, -4), "DN1": (4, 0), "UP1": (-4, 0)}
R1, R2 = (20, 61), (13, 61)
SLACK = 12                               # initial extra P_E units (gap +56 cells)


def start_markers(slack=SLACK):
    D1 = (R1[0] - slack * PE[0], R1[1] - slack * PE[1])
    D2 = (R2[0] - slack * PE[0], R2[1] - slack * PE[1])
    T = (0, 0)
    M = (-D1[0], -D1[1])
    P = (M[0] - D2[0], M[1] - D2[1])
    return [T, M, P]


def schedule(prog, markers=None):
    markers = markers or start_markers()
    pl = [("F",) + m for m in markers]
    delay = 0
    for op in prog:
        for name, t, x in OPS[op]:
            delay += GAP
            T = markers[0]
            ev = (T[0] + t + delay * PF[0], T[1] + x + delay * PF[1])
            r = cross_chain(["F"] * 3, markers, (name,) + ev)
            assert r is not None, (op, name)
            markers = r[0]
            pl.append((name,) + ev)
    return pl, markers, delay


def xpos(s):
    return s[2] + Fraction(s[1], 9)          # position at t = 0 (v = -1/9)


def gaps_of(fs):
    xs = sorted(xpos(s) for s in fs)
    return [float(b - a) for a, b in zip(xs, xs[1:])]


def simulate(prog, markers=None):
    pl, pred, delay = schedule(prog, markers)
    prods = run(pl, 36 * (delay + 40) + 6000)
    fs = sorted((norm(*p) for p in prods if p[0] == "F"), key=xpos)
    exp = sorted((norm("F", *m) for m in pred), key=xpos)
    junk = [p[0] for p in prods if p[0] != "F" and LIB.gliders[p[0]].velocity != Fraction(-4, 15)]
    return fs, exp, junk, len(prods)


def predicted_gaps(prog):
    g0 = gaps_of([norm("F", *m) for m in start_markers()])   # [reg2, reg1]
    u = Fraction(-8) + Fraction(30, 9)                       # gap change per P_E unit
    d1 = sum(LABEL[o][0] for o in prog)
    d2 = sum(LABEL[o][1] for o in prog)
    return [g0[0] + float(d2 * u), g0[1] + float(d1 * u)]


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    rnd = random.Random(seed)
    progs = [["DN2"], ["UP2"], ["DN1"], ["UP1"]]
    for _ in range(n):
        progs.append([rnd.choice(list(OPS)) for _ in range(6)])
    ok = 0
    for prog in progs:
        fs, exp, junk, np_ = simulate(prog)
        good = fs == exp and not junk and len(fs) == 3
        ok += good
        print(" ".join(prog), "|", "MATCH" if fs == exp else "MISMATCH",
              "sim gaps [reg2, reg1]", [round(g, 2) for g in gaps_of(fs)],
              "arith", [round(g, 2) for g in predicted_gaps(prog)],
              "junk", sorted(set(junk)), flush=True)
    print(f"{ok}/{len(progs)} exact")
