"""Check delayline 23:33 window physics with my builder/typer:
E + GB4 -> E displaced (3 classes: +308/15, 0, +364/15 cells, i.e. per the
(15,-4) motion a shift of the E's worldline), E^2 + GB4 -> E^2 unmoved in
all 3 classes. Displacement = position of the surviving E-object minus its
position in an E-alone run, at the same T and the same phase (measured as
the intercept shift: dx_eff = dx + (4/15) * dt for an object found dt steps
phase-shifted)."""
from fractions import Fraction
import pairscan
import hrun

vlib = hrun.vlib
T = 3000


def intercept(name_at, x):
    """x-intercept at time 0 of the worldline of a (15,-4) object of phase s
    observed at x at time T: x0 = x + 4 T/15 - (phase correction)."""
    return Fraction(x) + Fraction(4 * T, 15)


def main():
    for E in ("E", "E^2", "E^3"):
        alone, _ = pairscan.run_items([(E, 0, 0)], T)
        (n0, x0, w0), = alone
        res = pairscan.classes(E, "GB4", 60, T, n_expected=3)
        for k, (names, objs, placed) in sorted(res.items()):
            surv = [(n, x) for n, x in objs if n.split("@")[0] == E]
            rest = [n for n, x in objs if n.split("@")[0] != E]
            if len(surv) == 1:
                (n1, x1), = surv
                # find a in 0..14 with the E-alone run at T + a in the same phase:
                # survivor(t) = alone(t + a) + (x1 - xa), so the worldline is
                # shifted by (x1 - xa) - 4a/15 cells at fixed time
                for a in range(15):
                    (na, xa, wa), = pairscan.run_items([(E, 0, 0)], T + a)[0]
                    if na == n1:
                        break
                else:
                    raise AssertionError("phase not found")
                sh = Fraction(x1 - xa) - Fraction(4 * a, 15)
                print(f"{E} + GB4 class {k}: {E} survives, worldline shift {sh} = {float(sh):.2f}; others {rest}")
            else:
                print(f"{E} + GB4 class {k}: {list(names)}")


if __name__ == "__main__":
    main()
