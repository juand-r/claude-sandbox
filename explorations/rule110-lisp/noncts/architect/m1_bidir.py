"""M1: bidirectional transport through stored F data.

A rigid train of F gliders (memory, v = -1/9) is crossed
  - from its left by a stationary C2 (a messenger; in the memory frame it
    moves right), and
  - from its right by a periodic stream of Ebars (commands; in the memory
    frame they move left),
at the same time, and everything must come out intact.

All placements are derived from single-crossing displacement vectors
(the "crossing algebra"), not searched:
  C2 x F class 1:   C2 moves (4,13), F moves (2,-11)
  F x Ebar class 8: Ebar moves e8, F moves f8 (read from the catalog run)
  C2 x Ebar class 2: C2 moves (0,7), Ebar moves (6,-13)
Conditions (lattices L_XY = <P_X, P_Y>):
  train vector G  = C2 displacement  (mod L_CF)   [C2 passes every F]
  train vector G  = -e8              (mod L_FE)   [Ebar passes every F]
  stream vector S = f8               (mod L_FE)   [every Ebar in class 8]
  stream vector S = C2 displacement by Ebar (0,7) (mod L_CE)
"""
import sys
from fractions import Fraction
from rx import *

PF, PE, PC = (36, -4), (30, -8), (7, 0)


def inlat(v, P1, P2):
    (a, b), (c, d) = P1, P2
    det = a * d - b * c
    x = Fraction(v[0] * d - v[1] * c, det)
    y = Fraction(a * v[1] - b * v[0], det)
    return x.denominator == 1 and y.denominator == 1


def disp(X, Y, cls):
    """Displacements (dX, dY) of a clean crossing X+Y of class cls."""
    rp = canonical_reps(LIB, X, Y)[cls]
    prods = run([(X, 0, 0), (Y,) + tuple(rp)], 3000)
    assert sorted(p[0] for p in prods) == sorted([X, Y]), prods
    px = [p for p in prods if p[0] == X][0]
    py = [p for p in prods if p[0] == Y][0]
    return (px[1], px[2]), (py[1] - rp[0], py[2] - rp[1])


def main(n_F=3, n_E=8, verbose=True):
    (c2F, fC) = disp("C2", "F", 1)       # C2 disp, F disp
    (f8, e8) = disp("F", "Ebar", 8)
    (c2E, eC) = disp("C2", "Ebar", 2)
    if verbose:
        print("C2xF#1", c2F, fC, " FxEbar#8", f8, e8, " C2xEbar#2", c2E, eC)
    # train vector G: G = c2F mod L_CF and G = -e8 mod L_FE, spatial gap 40..80
    Gs = []
    for i in range(-8, 9):
        for j in range(-8, 9):
            G = (-e8[0] + 36 * i + 30 * j, -e8[1] - 4 * i - 8 * j)
            if abs(G[0]) <= 12 and 40 <= G[1] <= 80 and \
                    inlat((G[0] - c2F[0], G[1] - c2F[1]), PC, PF):
                Gs.append(G)
    G = min(Gs, key=lambda g: (abs(g[0]), g[1]))
    # stream vector S: S = f8 mod L_FE and S = c2E mod L_CE, Ebar spacing ~60-110
    Ss = []
    for i in range(-10, 11):
        for j in range(-10, 11):
            S = (f8[0] + 36 * i + 30 * j, f8[1] - 4 * i - 8 * j)
            if abs(S[0]) <= 15 and 60 <= S[1] <= 130 and \
                    inlat((S[0] - c2E[0], S[1] - c2E[1]), PC, PE):
                Ss.append(S)
    S = min(Ss, key=lambda s: (abs(s[0]), s[1]))
    if verbose:
        print("train vector G", G, " stream vector S", S)
    Fs = [("F", i * G[0], 400 + i * G[1]) for i in range(n_F)]
    # C2 left of the train in class 1 w.r.t. the leftmost F
    rC = canonical_reps(LIB, "C2", "F")[1]
    C2 = ("C2", Fs[0][1] - rC[0], Fs[0][2] - rC[1])
    # first Ebar in class 8 w.r.t. the rightmost F, pushed back by S until
    # it starts right of the train
    r8 = canonical_reps(LIB, "F", "Ebar")[8]
    E0 = (Fs[-1][1] + r8[0], Fs[-1][2] + r8[1])
    Es = [("Ebar", E0[0] + k * S[0], E0[1] + k * S[1]) for k in range(n_E)]
    pl = [C2] + Fs + Es
    prods = run(pl, 6000)
    names = sorted(p[0] for p in prods)
    want = sorted(["C2"] + ["F"] * n_F + ["Ebar"] * n_E)
    return pl, prods, names == want


if __name__ == "__main__":
    pl, prods, ok = main()
    print("placements", pl)
    print("products", prods)
    print("CLEAN" if ok else "NOT CLEAN")
