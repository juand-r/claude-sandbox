"""Yang-Baxter-type compatibility of three mutually crossing families.

For objects X (left), Y (middle), Z (right) that all cross pairwise, the
class of the (X, Z) meeting shifts by (dZ_by_Y - dX_by_Y) for every Y that
both have crossed before they meet. A design is robust to the number of
Y's in between iff the orbit of the intended X-Z class under that shift
stays inside the soliton classes of X-Z.
"""
import json
from rx import *

ROWS = json.load(open('../collider/collisions.json'))


def sol_classes(X, Y):
    return sorted({r['cls'] for r in ROWS if r['X'] == X and r['Y'] == Y
                   and r['kind'] == 'crossing'})


def disp(X, Y, cls):
    rp = canonical_reps(LIB, X, Y)[cls]
    prods = run([(X, 0, 0), (Y,) + tuple(rp)], 3000)
    assert sorted(p[0] for p in prods) == sorted([X, Y]), prods
    px = [p for p in prods if p[0] == X][0]
    py = [p for p in prods if p[0] == Y][0]
    return (px[1], px[2]), (py[1] - rp[0], py[2] - rp[1])


def orbit(X, Z, shift, start, maxn=100):
    r = canonical_reps(LIB, X, Z)[start]
    seen = []
    for n in range(maxn):
        k = cls_of(X, (0, 0), Z, (r[0] + n * shift[0], r[1] + n * shift[1]))
        if seen and k == seen[0]:
            return seen
        seen.append(k)
    raise AssertionError("orbit too long")


if __name__ == "__main__":
    for C in ["C1", "C2"]:
        S_CE = sol_classes(C, "Ebar")
        for kCF in sol_classes(C, "F"):
            cF, fC = disp(C, "F", kCF)
            for kFE in sol_classes("F", "Ebar"):
                fE, eF = disp("F", "Ebar", kFE)
                sh = (eF[0] - cF[0], eF[1] - cF[1])
                for kCE in S_CE:
                    orb = orbit(C, "Ebar", sh, kCE)
                    tag = "ROBUST" if set(orb) <= set(S_CE) else ""
                    print(f"{C}xF#{kCF} FxEbar#{kFE} {C}xEbar#{kCE}: "
                          f"shift {sh} orbit {orb} {tag}")
