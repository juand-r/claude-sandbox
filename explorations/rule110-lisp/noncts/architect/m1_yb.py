"""M1 with a Yang-Baxter-consistent triple: messenger C1, memory F,
stream Ebar with incoming classes C1xF#1, FxEbar#3, C1xEbar#1, which
yb3.py found to give identical classes whichever order the three meet in.

Robustness test: a train of n_F F's (vector G), a C1 messenger and a
stream of n_E Ebars (vector S). The messenger's timing is shifted by
a*(30,-8), which keeps every incoming class but changes how deep inside
the train each Ebar meets the messenger. Every run must come out with
all gliders intact.
"""
from m1_bidir import inlat, PF, PE, PC
from m1_robust import lattice_pick
from yb import disp
from rx import *

M, kMF, kFS, kMS = "C1", 1, 3, 1


def design():
    cF, fC = disp(M, "F", kMF)
    fE, eF = disp("F", "Ebar", kFS)
    cE, eC = disp(M, "Ebar", kMS)
    G = lattice_pick((-eF[0], -eF[1]), PF, PE,
                     lambda v: abs(v[0]) <= 12 and 40 <= v[1] <= 90 and
                     inlat((v[0] - cF[0], v[1] - cF[1]), PC, PF), 8,
                     lambda v: (abs(v[0]), v[1]))
    S = lattice_pick(fE, PF, PE,
                     lambda v: abs(v[0]) <= 15 and 60 <= v[1] <= 140 and
                     inlat((v[0] - cE[0], v[1] - cE[1]), PC, PE), 10,
                     lambda v: (abs(v[0]), v[1]))
    return G, S


def build(G, S, a, n_F=4, n_E=16, x_train=700, b=1):
    """b: stream shift by b*(36,-4) (an F period: keeps FxEbar class,
    selects the C1xEbar incoming class; b=1 is the consistent one for
    n_F=4, G=(0,43), found by experiment and explained by G mod L_CE)."""
    Fs = [("F", i * G[0], x_train + i * G[1]) for i in range(n_F)]
    rC = canonical_reps(LIB, M, "F")[kMF]
    Mm = (M, Fs[0][1] - rC[0] + 30 * a, Fs[0][2] - rC[1] - 8 * a)
    rk = canonical_reps(LIB, "F", "Ebar")[kFS]
    E0 = (Fs[-1][1] + rk[0] + 36 * b, Fs[-1][2] + rk[1] - 4 * b)
    Es = [("Ebar", E0[0] + k * S[0], E0[1] + k * S[1]) for k in range(n_E)]
    return [Mm] + Fs + Es


if __name__ == "__main__":
    G, S = design()
    print("G", G, "S", S, flush=True)
    res = []
    for a in range(0, 40, 2):
        pl = build(G, S, a)
        try:
            prods = run(pl, 12000)
            names = sorted(p[0] for p in prods)
            ok = names == sorted([M] + ["F"] * 4 + ["Ebar"] * 16)
        except Exception as e:
            ok, names = False, str(e)[:100]
        res.append(ok)
        print("a", a, "CLEAN" if ok else names, flush=True)
    print(f"clean {sum(res)}/{len(res)}")
