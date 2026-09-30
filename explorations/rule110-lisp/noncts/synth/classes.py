"""Collision classes of two periodic items. An item placed as a scene piece
(tau, x) has its canonical seed at spacetime (-tau, x). Two placements of
the right item against a fixed left item give the same collision iff the
difference of their seed offsets lies in M = <P_left, P_right> (both
period vectors). Number of classes = |det(P_left, P_right)| / 14."""
from fractions import Fraction


def same_class(o1, o2, P1, P2):
    dt, dx = o1[0] - o2[0], o1[1] - o2[1]
    det = P1[0] * P2[1] - P1[1] * P2[0]
    if det == 0:
        raise ValueError("parallel periods: infinitely many classes")
    u = Fraction(dt * P2[1] - dx * P2[0], det)
    w = Fraction(P1[0] * dx - P1[1] * dt, det)
    return u.denominator == 1 and w.denominator == 1


def n_classes(P1, P2):
    return abs(P1[0] * P2[1] - P1[1] * P2[0]) // 14


def placements_by_class(left_item, left_piece, right_item, x_min, span=120,
                        max_tau=None):
    """One (tau, x) placement per collision class for right_item placed
    right of left_item (left_piece = (tau_L, x_L)), respecting the ether
    phase between them. Prefers small tau, then small x."""
    tL, xL = left_piece
    p_between = (4 * tL + left_item.pR - xL) % 14
    P1, P2 = left_item.period, right_item.period
    n = n_classes(P1, P2)
    p = P2[0]
    max_tau = p - 1 if max_tau is None else max_tau
    cands = [(tau, x) for x in range(x_min, x_min + span) for tau in range(max_tau + 1)
             if (4 * tau - x - p_between) % 14 == 0 and x - tau >= x_min]
    cands.sort(key=lambda c: (c[0] > 6, c[1], c[0]))
    reps = []
    for tau, x in cands:
        o = (-tau - (-tL), x - xL)
        if not any(same_class(o, r[2], P1, P2) for r in reps):
            reps.append((tau, x, o))
        if len(reps) == n:
            break
    if len(reps) != n:
        raise ValueError(f"found {len(reps)} of {n} classes; widen span")
    return [(tau, x) for tau, x, _ in reps]
