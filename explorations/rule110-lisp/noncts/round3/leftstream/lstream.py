"""Rigid left stream: a program over packets of lpk.PK, built as ONE fixed
row text (packet seeds do not depend on the input), run against the counter
E^(v+1) = E at E0 + v B's from the right, in exact Rule 110.

Placement rule (bookkeeping, no search): packet i of type X is the
reference scene of X translated so that its E sits at the counter's
virtual front e_i = E0 + sum of earlier deltas, then moved m_i * P_E
(same class, later arrival) so that packets arrive GAP steps apart.
Model: I: v+1; D: v-1 (v = 0 -> C3, counter destroyed); Z: v-1 if v > 0,
else v stays 0 and one A leaves to the right (answer).
"""
import sys
from lsl import run, snap, names, nval, row_of
from lpk import PK

PE = (15, -4)
E0 = (0, 0)
GAP = 150          # steps between packet arrivals
T0 = 400           # first arrival after the B's have built E^(v+1)


def place_program(prog, gap=GAP, t0=None):
    """Seeds of the whole stream (independent of v)."""
    t0 = t0 if t0 is not None else T0
    e = E0
    seeds = []
    for i, X in enumerate(prog):
        pk = PK[X]
        tr = (e[0] - pk["e"][0], e[1] - pk["e"][1])
        m = (t0 + i * gap - tr[0]) // PE[0]
        for nm, t, x in pk["seeds"]:
            seeds.append((nm, t + tr[0] + m * PE[0], x + tr[1] + m * PE[1]))
        e = (e[0] + pk["delta"][0], e[1] + pk["delta"][1])
    return seeds


def counter(v, bgap=40):
    pl = [("E",) + E0]
    x = E0[1] + 30
    for i in range(v):
        x = snap(pl, "B", 0, x)
        pl.append(("B", 0, x))
        x += bgap
    return pl


def model(prog, v):
    ans = 0
    for X in prog:
        if X == "I":
            v += 1
        elif X == "D":
            if v == 0:
                return None, ans
            v -= 1
        elif X == "Z":
            if v == 0:
                ans += 1
            else:
                v -= 1
    return v, ans


def run_program(prog, v, gap=GAP, t0=None):
    t0 = t0 if t0 is not None else max(T0, 200 + 180 * v)
    stream = place_program(prog, gap, t0)
    pl = sorted(stream, key=lambda s: s[2]) + counter(v)
    T = t0 + gap * len(prog) + 800
    ok, out = run(pl, T)
    return ok, out


def outcome(out):
    """(counter value or None, number of A's, other products)."""
    Es = [p for p in out if nval(p[0])]
    As = [p for p in out if p[0] == "A"]
    other = [p[0] for p in out if not nval(p[0]) and p[0] != "A"]
    v = nval(Es[0][0]) - 1 if len(Es) == 1 else None
    return v, len(As), other


if __name__ == "__main__":
    prog = sys.argv[1]
    vs = [int(a) for a in sys.argv[2].split(",")]
    bad = 0
    for v in vs:
        ok, out = run_program(prog, v)
        got = outcome(out)
        exp = model(prog, v)
        good = ok and got[2] == [] and (got[0], got[1]) == exp
        bad += not good
        print(f"v={v}: CA value={got[0]} answers={got[1]} other={got[2]} "
              f"| model {exp} {'OK' if good else 'MISMATCH'}")
    print("mismatches:", bad)
