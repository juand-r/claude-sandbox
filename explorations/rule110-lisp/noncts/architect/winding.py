"""Can crossings alone pump a distance register?

Register = two markers of type M (front T, back P). An Ebar crosses T in
class a (free choice: where the Ebar is placed), is displaced by e_a, then
meets P in class b (determined), and each marker is displaced by its
crossing's displacement. D = seed(T) - seed(P) changes by m_a - m_b.
We explore all reachable D residues mod L = <P_M, P_Ebar> and test whether
the exact change of D is a function of the residue (a potential). If it
is, any command sequence that returns to the starting residue has zero net
effect: crossings alone cannot store an unbounded count.
"""
import sys
from collections import deque
from yb import sol_classes, disp
from rx import canonical_reps, cls_of, LIB, G as GL
from r110lib import class_key


def analyse(M, D0s):
    PM = (GL[M].p, GL[M].d)
    PE = (30, -8)
    SOL = sol_classes(M, "Ebar")
    DISP = {k: disp(M, "Ebar", k) for k in SOL}
    REP = canonical_reps(LIB, M, "Ebar")

    def step(a, D):
        e = DISP[a][1]
        rel = (REP[a][0] + e[0] + D[0], REP[a][1] + e[1] + D[1])
        try:
            b = cls_of(M, (0, 0), "Ebar", rel)
        except AssertionError:
            return None
        if b not in SOL:
            return None
        ma, mb = DISP[a][0], DISP[b][0]
        return b, (D[0] + ma[0] - mb[0], D[1] + ma[1] - mb[1])

    key = lambda D: class_key(D, PM, PE)
    for D0 in D0s:
        V = {key(D0): (0, 0)}
        q = deque([D0])
        wind = []
        edges = 0
        while q:
            D = q.popleft()
            for a in SOL:
                r = step(a, D)
                if r is None:
                    continue
                edges += 1
                b, D2 = r
                v2 = (D2[0] - D0[0], D2[1] - D0[1])
                k2 = key(D2)
                if k2 not in V:
                    V[k2] = v2
                    q.append(D2)
                elif V[k2] != v2:
                    wind.append((key(D), a, b, V[k2], v2))
        print(f"{M} markers, D0={D0}: residues reached {len(V)}, clean "
              f"transitions {edges}, winding transitions {len(wind)}",
              wind[:3])


if __name__ == "__main__":
    # starting gaps: several same-time spacings (the register's residue)
    analyse("C1", [(t, g) for g in range(37, 120, 14) for t in range(0, 7)])
    analyse("C2", [(t, g) for g in range(31, 120, 14) for t in range(0, 7)])
    analyse("F", [(0, 43), (0, 71), (2, 49), (0, 57)])
