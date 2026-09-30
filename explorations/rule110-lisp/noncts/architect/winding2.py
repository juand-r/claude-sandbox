"""Winding test for F-marker registers with crossings from BOTH sides:
Ebars from the right (cross T then P) and C1/C2 from the left (in F's rest
frame they move right: cross P then T). D = seed(T) - seed(P)."""
from collections import deque
from yb import sol_classes, disp
from rx import canonical_reps, cls_of, LIB
from r110lib import class_key

PF, PE = (36, -4), (30, -8)


def movers():
    """[(name, side, SOL, DISP, REP)] side 'R' = from the right (X=F, Y=mover),
    'L' = from the left (X=mover, Y=F)."""
    out = [("Ebar", "R", sol_classes("F", "Ebar"),
            {k: disp("F", "Ebar", k) for k in sol_classes("F", "Ebar")},
            canonical_reps(LIB, "F", "Ebar"))]
    for C in ["C1", "C2"]:
        S = sol_classes(C, "F")
        out.append((C, "L", S, {k: disp(C, "F", k) for k in S},
                    canonical_reps(LIB, C, "F")))
    return out


MOV = movers()


def step(mv, a, D):
    name, side, SOL, DISP, REP = mv
    if side == "R":           # F at origin is T; Ebar at REP[a]; P at -D
        f, e = DISP[a]
        rel = (REP[a][0] + e[0] + D[0], REP[a][1] + e[1] + D[1])
        try:
            b = cls_of("F", (0, 0), name, rel)
        except AssertionError:
            return None
        if b not in SOL:
            return None
        return (D[0] + DISP[a][0][0] - DISP[b][0][0],
                D[1] + DISP[a][0][1] - DISP[b][0][1])
    else:                     # C at origin crosses P first (P at REP[a]); T at P + D
        c, f = DISP[a]        # c = C displacement, f = F displacement
        # C after crossing P sits at c; T seed = REP[a] + D; rel(T - C) = REP[a]+D-c
        rel = (REP[a][0] + D[0] - c[0], REP[a][1] + D[1] - c[1])
        try:
            b = cls_of(name, (0, 0), "F", rel)
        except AssertionError:
            return None
        if b not in SOL:
            return None
        fb = DISP[b][1]
        return (D[0] + fb[0] - f[0], D[1] + fb[1] - f[1])


def analyse(D0):
    key = lambda D: class_key(D, PF, PE)
    V = {key(D0): (0, 0)}
    q = deque([D0])
    wind, edges = [], 0
    while q:
        D = q.popleft()
        for mv in MOV:
            for a in mv[2]:
                D2 = step(mv, a, D)
                if D2 is None:
                    continue
                edges += 1
                v2 = (D2[0] - D0[0], D2[1] - D0[1])
                k2 = key(D2)
                if k2 not in V:
                    V[k2] = v2
                    q.append(D2)
                elif V[k2] != v2:
                    wind.append((mv[0], a, V[k2], v2))
    print(f"D0={D0}: residues {len(V)}, transitions {edges}, winding {len(wind)}",
          wind[:4])


if __name__ == "__main__":
    for D0 in [(0, 43), (0, 71), (2, 49), (0, 57), (0, 29), (0, 99)]:
        analyse(D0)
