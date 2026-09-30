"""Zero test, stage 7: the SEPARATED zero state (gap 24.33, D = (12,23),
standard residue). Packets that are exact identities on separated pairs
(the 17 single identity movers and the 1285 two-packet identities of
ztest3) are applied to it with history-relative placement (xcounter
schedule). Proximity (multi-body) effects at gap 24.33 are the only way
their effect can differ from the identity. Report every non-identity
outcome; wanted: register kept (any clean F pair/compound) + a stationary
messenger, with no right-movers."""
import ast, sys
from fractions import Fraction
sys.path.insert(0, "../collider")
from collide import simulate
from winding3 import movers, apply
from xcounter import schedule
from rx import LIB
from m1_predict import norm_seed

EB = Fraction(-4, 15)


def seqs():
    out = [(mv,) for mv in movers() if apply(mv, (0, 43)) == (0, 43)]
    for l in open("ztest3.log"):
        if l.startswith("("):
            i = l.index(") (") + 1
            j = l.index(") [") + 1
            out.append((ast.literal_eval(l[:i]), ast.literal_eval(l[i + 1:j])))
    return out


if __name__ == "__main__":
    S = seqs()
    print("sequences", len(S), flush=True)
    T0, P0 = (0, 0), (-12, -23)
    for seq in S:
        try:
            pl, T, P = schedule(T0, P0, [list(seq)])
        except AssertionError:
            continue           # not predicted clean at this residue (should not happen)
        r = simulate(LIB, pl, 36 * 20 * len(pl) + 4000)
        prods = r["products"]
        fs = sorted([norm_seed(*p) for p in prods if p[0] == "F"])
        exp = sorted([norm_seed("F", *T), norm_seed("F", *P)])
        other = sorted(p[0] for p in prods if p[0] != "F" and LIB.gliders[p[0]].velocity != EB)
        if fs == exp and not other:
            continue           # identity, as predicted
        right = [n for n in other if LIB.gliders[n].velocity > 0]
        msg = [n for n in other if n in ("C1", "C2", "C3")]
        tag = "CANDIDATE" if msg and not right else ""
        print(seq, "F's", len(fs), "other", other, tag, flush=True)
    print("done", flush=True)
