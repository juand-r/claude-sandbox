"""Lower end of the working range: relative-placement runs that drive reg2
down k units and back up (DN2^k UP2^k), full simulation. F-compounds named
F_k_F by collider's typer are split into their F's (parts) before
comparing, so a close pair is not mistaken for a merger."""
import sys
from fractions import Fraction
import tworeg_abs as T2
from rx import run, norm, LIB


def f_seeds(prods):
    out = []
    for n, t, x in prods:
        g = LIB.gliders[n]
        if n == "F":
            out.append(norm("F", t, x))
        elif n.startswith("F_") and g.parts:
            for nm, pt, px in g.parts:
                out.append(norm(nm, t + pt, x + px))
    return sorted(out, key=T2.xpos)


for k in ([int(a) for a in sys.argv[1:]] if __name__ == "__main__" else []):
    prog = ["DN2"] * k + ["UP2"] * k
    pl, pred, delay = T2.schedule(prog)
    res = run(pl, 36 * (delay + 40) + 6000, must_settle=False)
    fs = f_seeds(res)
    exp = sorted((norm("F", *m) for m in pred), key=T2.xpos)
    junk = sorted({p[0] for p in res if not p[0].startswith("F") and (p[0] not in LIB.gliders or LIB.gliders[p[0]].velocity != Fraction(-4, 15))})
    print("DN2^%d UP2^%d" % (k, k), "min reg2 gap %.2f" % (T2.predicted_gaps(["DN2"] * k)[0]),
          "|", "MATCH" if fs == exp else "MISMATCH", [round(g, 2) for g in T2.gaps_of(fs)], "junk", junk, flush=True)
