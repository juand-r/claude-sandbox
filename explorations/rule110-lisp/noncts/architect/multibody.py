"""Do tight Ebar pairs act on an F differently from two independent
Ebars?  For every catalog collision F + (Ebar pair) whose products are F
plus Ebars only, compare the F's final seed with the sequential prediction
(member 1 crosses, F displaced, then member 2 crosses the displaced F).
A difference is a genuine multi-body effect: the only way around the
no-winding result for crossing-only registers."""
import json, re, sys
from yb import sol_classes, disp
from rx import cls_of, LIB, G as GL
from m1_predict import norm_seed

ROWS = json.load(open("../collider/collisions.json"))
SOL = sol_classes("F", "Ebar")
DISP = {k: disp("F", "Ebar", k) for k in SOL}
pat = re.compile(r"^Ebar@\(0,0\)\+Ebar@\((-?\d+),(-?\d+)\)$")


def seq_predict(y, sp):
    """F at (0,0); Ebar members at y and y+sp. -> F final seed or None
    (if a member is not in a clean class)."""
    F = (0, 0)
    for m in [y, (y[0] + sp[0], y[1] + sp[1])]:
        try:
            k = cls_of("F", F, "Ebar", m)
        except AssertionError:
            return "inconsistent"
        if k not in SOL:
            return f"member class {k} not clean"
        f = DISP[k][0]
        F = (F[0] + f[0], F[1] + f[1])
    return norm_seed("F", *F)


n_same = n_diff = n_bad = 0
for r in ROWS:
    if r["X"] != "F":
        continue
    m = pat.match(r["Y"])
    if not m:
        continue
    names = [p[0] for p in r["products"]]
    if names.count("F") != 1 or not all(n == "F" or n.startswith("Ebar") for n in names):
        continue
    sp = (int(m.group(1)), int(m.group(2)))
    fout = [p for p in r["products"] if p[0] == "F"][0]
    got = norm_seed("F", fout[1], fout[2])
    pred = seq_predict(tuple(r["Y_event"]), sp)
    if pred == got:
        n_same += 1
    elif isinstance(pred, str):
        n_bad += 1
        print("NONCLEAN-MEMBER", r["Y"], r["cls"], pred, "-> catalog F", got, names)
    else:
        n_diff += 1
        print("MULTIBODY", r["Y"], r["cls"], "pred", pred, "got", got, names)
print("same", n_same, "multibody", n_diff, "member-not-clean", n_bad)
