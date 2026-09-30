"""M1 robustness: vary the messenger's entry time into a stored F train
while a periodic Ebar stream passes through; count clean outcomes.
For each choice (messenger C in {C1,C2}, C x F soliton class, F x Ebar
soliton class k, C x Ebar soliton class) the train vector G and stream
vector S are derived from the crossing algebra (see m1_bidir.py)."""
import sys
from yb import sol_classes, disp
from m1_bidir import inlat, PF, PE, PC
from rx import *


def lattice_pick(base, P1, P2, cond, rng, key):
    out = []
    for i in range(-rng, rng + 1):
        for j in range(-rng, rng + 1):
            v = (base[0] + P1[0] * i + P2[0] * j, base[1] + P1[1] * i + P2[1] * j)
            if cond(v):
                out.append(v)
    return min(out, key=key) if out else None


def design(C, kCF, kFE, kCE):
    cF, fC = disp(C, "F", kCF)
    fE, eF = disp("F", "Ebar", kFE)
    cE, eC = disp(C, "Ebar", kCE)
    G = lattice_pick((-eF[0], -eF[1]), PF, PE,
                     lambda v: abs(v[0]) <= 12 and 40 <= v[1] <= 90 and
                     inlat((v[0] - cF[0], v[1] - cF[1]), PC, PF), 8,
                     lambda v: (abs(v[0]), v[1]))
    S = lattice_pick(fE, PF, PE,
                     lambda v: abs(v[0]) <= 15 and 60 <= v[1] <= 140 and
                     inlat((v[0] - cE[0], v[1] - cE[1]), PC, PE), 10,
                     lambda v: (abs(v[0]), v[1]))
    return G, S


def trial(C, kCF, kFE, G, S, a, n_F=4, n_E=14):
    Fs = [("F", i * G[0], 600 + i * G[1]) for i in range(n_F)]
    rC = canonical_reps(LIB, C, "F")[kCF]
    M = (C, Fs[0][1] - rC[0] + 36 * a, Fs[0][2] - rC[1] - 4 * a)
    rk = canonical_reps(LIB, "F", "Ebar")[kFE]
    E0 = (Fs[-1][1] + rk[0], Fs[-1][2] + rk[1])
    Es = [("Ebar", E0[0] + k * S[0], E0[1] + k * S[1]) for k in range(n_E)]
    try:
        prods = run([M] + Fs + Es, 9000)
    except Exception as e:
        return False, str(e)[:80]
    names = sorted(p[0] for p in prods)
    return names == sorted([C] + ["F"] * n_F + ["Ebar"] * n_E), names


if __name__ == "__main__":
    for C in ["C2", "C1"]:
        for kCF in sol_classes(C, "F"):
            for kFE in sol_classes("F", "Ebar"):
                for kCE in sol_classes(C, "Ebar"):
                    G, S = design(C, kCF, kFE, kCE)
                    if G is None or S is None:
                        print(C, kCF, kFE, kCE, "no G/S"); continue
                    res = [trial(C, kCF, kFE, G, S, a)[0] for a in range(0, 24, 2)]
                    print(f"{C}xF#{kCF} FxEbar#{kFE} {C}xEbar#{kCE} G={G} S={S}: "
                          f"clean {sum(res)}/{len(res)} {''.join('x' if r else '.' for r in res)}",
                          flush=True)
