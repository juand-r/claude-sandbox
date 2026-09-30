"""Phase algebra for F-memory registers crossed by Ebars.

A register is two F's, front T and back P (P left of T), with D = seed(T) -
seed(P). Every Ebar crosses T (class a, chosen by where the Ebar is placed)
and then P (class b, determined by a and D mod L_FE). A clean crossing of
class k displaces F by f_k and the Ebar by e_k (from the catalog). So an
Ebar changes D by f_a - f_b. Everything depends only on D mod L_FE, hence
not on the register value if values differ by elements of L_FE.
"""
from functools import lru_cache
from fractions import Fraction
from yb import sol_classes, disp
from rx import canonical_reps, cls_of, LIB

PF, PE = (36, -4), (30, -8)
SOL = sol_classes("F", "Ebar")
DISP = {k: disp("F", "Ebar", k) for k in SOL}        # k -> (f_k, e_k)
REP = canonical_reps(LIB, "F", "Ebar")


def inlat(v, P1=PF, P2=PE):
    (a, b), (c, d) = P1, P2
    det = a * d - b * c
    x = Fraction(v[0] * d - v[1] * c, det)
    y = Fraction(a * v[1] - b * v[0], det)
    return x.denominator == 1 and y.denominator == 1


def class_vs_P(a, D):
    """Class of an Ebar vs P after crossing T in class a (T at origin,
    Ebar at REP[a], P at -D). None if not ether-consistent."""
    f, e = DISP[a]
    rel = (REP[a][0] + e[0] + D[0], REP[a][1] + e[1] + D[1])
    try:
        return cls_of("F", (0, 0), "Ebar", rel)
    except AssertionError:
        return None


def step(a, D):
    """-> (b, D') or None if the crossing of P is not clean."""
    b = class_vs_P(a, D)
    if b is None or b not in SOL:
        return None
    fa, fb = DISP[a][0], DISP[b][0]
    return b, (D[0] + fa[0] - fb[0], D[1] + fa[1] - fb[1])


def reduce(D):
    """Canonical representative of D mod L_FE (small, deterministic)."""
    best = None
    for i in range(-6, 7):
        for j in range(-6, 7):
            v = (D[0] + 36 * i + 30 * j, D[1] - 4 * i - 8 * j)
            key = (abs(v[0]) + abs(v[1]), v)
            if best is None or key < best:
                best = key
    return best[1]


from r110lib import class_key as _ck


def dkey(D):
    """Canonical key of D mod L_FE."""
    return _ck(D, PF, PE)


def find_packets(D0, max_len=8, want=None):
    """BFS over command sequences (classes vs T) from register state D0.
    Returns {net_dD: shortest sequence of (a, b)} for sequences that bring
    D back to D0's class. net_dD is exact (not reduced)."""
    from collections import deque
    k0 = dkey(D0)
    out = {}
    q = deque([(D0, ())])
    seen = {(k0, (0, 0))}
    while q:
        D, seq = q.popleft()
        if len(seq) >= max_len:
            continue
        for a in SOL:
            r = step(a, D)
            if r is None:
                continue
            b, D2 = r
            s2 = seq + ((a, b),)
            net = (D2[0] - D0[0], D2[1] - D0[1])
            if dkey(D2) == k0 and net != (0, 0) and net not in out:
                out[net] = s2
            st = (dkey(D2), net)
            if st in seen or abs(net[0]) > 80:
                continue
            seen.add(st)
            q.append((D2, s2))
    return out
