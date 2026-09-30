"""Two F-pair registers in one Ebar lane, addressed by collision class.

Markers T (front, rightmost), M (middle), P (back). reg1 = D1 = T - M,
reg2 = D2 = M - P (seed-event differences). A mover (Ebar-speed glider or
packet, in a chosen class relative to T) crosses T, then its outputs cross
M, then P (catalog-level prediction via architect's cross()).

Search (BFS over residues of D1, D2 mod L_FE, net changes tracked modulo
P_F): mover sequences that return both residues and change exactly one
register by a winding step (net not a multiple of P_F) while the other
register's net is a multiple of P_F (same trajectory = unchanged).
"""
import sys
from collections import deque
import lane
from lane import KEY, cross_chain, same_traj, sub, add

PF = (36, -4)
D0 = (0, 43)


def normP(v):
    """Representative of v modulo P_F with 0 <= t < 36."""
    q = v[0] // 36
    return (v[0] - 36 * q, v[1] + 4 * q)


def residues(base=D0):
    """All ether-compatible residues of an F-F seed difference."""
    out = {}
    for t in range(0, 36):
        for x in range(-60, 60):
            if (x + 4 * t) % 14 == 0:
                D = (base[0] + t, base[1] + x)
                k = KEY(D)
                if k not in out or abs(out[k][1] - 43 * 1) > abs(D[1] - 43):
                    out[k] = D
    return out


MV = lane.movers()
_TR = {}


def transitions(D1, D2):
    """[(mover, dD1, dD2)] for markers T=(0,0), M=-D1, P=-D1-D2; cached by
    residue pair (valid: a lattice shift of D only translates products)."""
    k = (KEY(D1), KEY(D2))
    if k not in _TR:
        T, M = (0, 0), (-D1[0], -D1[1])
        P = (M[0] - D2[0], M[1] - D2[1])
        lst = []
        for mv in MV:
            r = cross_chain([T, M, P], mv)
            if r is None:
                continue
            (T2, M2, P2), _ = r
            lst.append((mv, sub(sub(T2, M2), D1), sub(sub(M2, P2), D2)))
        _TR[k] = lst
    return _TR[k]


def search(D1_0, D2_0, max_len=4, bound=60, max_found=40):
    """BFS; returns dict goal -> list of (net1, net2, sequence)."""
    k0 = (KEY(D1_0), KEY(D2_0))
    found = {"R1": [], "R2": []}
    seen = {(k0, (0, 0), (0, 0))}
    q = deque([(D1_0, D2_0, (), (0, 0), (0, 0))])
    while q:
        D1, D2, seq, n1, n2 = q.popleft()
        if len(seq) >= max_len:
            continue
        for mv, d1, d2 in transitions(D1, D2):
            E1, E2 = add(D1, d1), add(D2, d2)
            m1, m2 = normP(add(n1, d1)), normP(add(n2, d2))
            s2 = seq + (mv,)
            kk = (KEY(E1), KEY(E2))
            if kk == k0 and (m1 != (0, 0) or m2 != (0, 0)):
                if m2 == (0, 0) and len(found["R1"]) < max_found:
                    found["R1"].append((m1, m2, s2))
                elif m1 == (0, 0) and len(found["R2"]) < max_found:
                    found["R2"].append((m1, m2, s2))
                continue
            st = (kk, m1, m2)
            if st in seen or abs(m1[1]) > bound or abs(m2[1]) > bound:
                continue
            seen.add(st)
            q.append((E1, E2, s2, m1, m2))
    return found


if __name__ == "__main__":
    R = residues()
    print("residues:", len(R), sorted(R.values()))
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for D2 in sorted(R.values()):
        f = search(D0, D2, max_len=L)
        print("D1", D0, "D2", D2, "R1-only cycles", len(f["R1"]),
              "R2-only cycles", len(f["R2"]), flush=True)
        for g in ("R1", "R2"):
            for c in f[g][:4]:
                print("   ", g, c)
