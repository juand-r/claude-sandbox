"""Abstract model of the burst (delay-line) regime between R2 and a
right-side REFLECTOR, in the rod frame, exact rational arithmetic. [model]

Objects: R2 (value y, back at position b), reflector face at f, gap g = f - b.
- Left: a blind program, one op per left slot (period P): 'z' = Z_L
  (y > 0: y -= 1; y = 0: emit one A at R2's back), 'i' = I_L (y += 1).
- A moves right at speed vA; at the reflector it is absorbed, the face
  moves right by aA (g grows), and after a latency `lat` the reflector
  emits a B-train of k units moving left at speed vB.
- A B-train meeting an A in flight loses one unit and the A dies (A + B^k ->
  B^(k-1), single class in Rule 110).
- A B-train of j units arriving at R2's back adds j to y and moves the back
  right by j*aB (g shrinks).
Speeds in the rod frame from Rule 110: A 2/3 + 4/15 = 14/15, B 1/2 - 4/15 = 7/30.
This models a HYPOTHETICAL reflector (gain k); s.7 of THEORY_DL.md.

episode_map(g0) runs from "y just hit zero" to "y hits zero again" and
returns (g1, n_A, y_peak); the test compares it with the closed-form count
n_A = #slots in [0, round trip) (the burst law), and checks that with walking
reflections the zero times are not eventually periodic.
Usage: python burstmodel.py
"""
from fractions import Fraction as Fr
import math

vA, vB = Fr(14, 15), Fr(7, 30)


def simulate(g0, prog="z", P=Fr(150), k=2, lat=Fr(0), aA=Fr(0), aB=Fr(0),
             y0=0, t_end=Fr(10**6), max_events=200000):
    """Event simulation. Returns list of (time, y) at every zero of y
    (start of an episode) and the final gap."""
    b, f = Fr(0), Fr(g0)
    y = y0
    A = []            # positions/emission of A's in flight: (t_emit, x_emit)
    Bs = []           # B trains in flight: [t_emit, x_emit, units]
    t = Fr(0)
    slot = 0
    zeros = []
    in_zero = False
    nA = 0
    events = 0
    pending = []      # (t_fire, units) reflector emissions scheduled
    while t < t_end and events < max_events:
        events += 1
        # next left slot
        t_slot = slot * P
        # next A arrival at f (f fixed between events)
        tA = min(((ta + (f - xa) / vA), i) for i, (ta, xa) in enumerate(A)) if A else (None, None)
        # next B arrival at b
        tB = min(((tb + (xb - b) / vB), i) for i, (tb, xb, u) in enumerate(Bs)) if Bs else (None, None)
        # next A-B meeting: A at xa + vA (t - ta), B at xb - vB (t - tb)
        tM = (None, None)
        for i, (ta, xa) in enumerate(A):
            for j, (tb, xb, u) in enumerate(Bs):
                tm = (xb - xa + vA * ta + vB * tb) / (vA + vB)
                if tm >= max(ta, tb) and (tM[0] is None or tm < tM[0]):
                    tM = (tm, (i, j))
        tP = min(pending)[0] if pending else None
        cands = [(t_slot, 0, None)]
        if tA[0] is not None:
            cands.append((tA[0], 1, tA[1]))
        if tB[0] is not None:
            cands.append((tB[0], 2, tB[1]))
        if tM[0] is not None:
            cands.append((tM[0], 3, tM[1]))
        if tP is not None:
            cands.append((tP, 4, None))
        t, kind, idx = min(cands, key=lambda c: (c[0], c[1]))
        if kind == 0:
            op = prog[slot % len(prog)]
            slot += 1
            if op == 'i':
                y += 1
            elif op == 'z':
                if y > 0:
                    y -= 1
                else:
                    A.append((t, b))
                    nA += 1
            if y == 0 and not in_zero:
                zeros.append((t, f - b, nA))
                in_zero = True
            elif y > 0:
                in_zero = False
        elif kind == 1:
            A.pop(idx)
            f += aA
            pending.append((t + lat, k))
        elif kind == 2:
            tb, xb, u = Bs.pop(idx)
            y += u
            b += u * aB
            if y > 0:
                in_zero = False
        elif kind == 3:
            i, j = idx
            A.pop(i)
            Bs[j][2] -= 1
            if Bs[j][2] == 0:
                Bs.pop(j)
        elif kind == 4:
            pending.sort()
            tp, u = pending.pop(0)
            Bs.append([tp, f, u])
    return zeros, f - b


def burst_law(g, P, lat):
    """Closed form for the first burst from a fresh zero at slot 0 with
    no refill in flight: A's are emitted at slots 0, P, 2P, ... until the
    first B (reflection of the first A) reaches R2 at time g/vA + lat + g/vB
    (gap constant during the first round trip because aA = aB = 0)."""
    rt = Fr(g) / vA + lat + Fr(g) / vB
    return math.floor(rt / P) + 1


if __name__ == "__main__":
    fails = 0
    # 1. burst law (no gap motion): number of A's in the first burst
    for g in (100, 250, 600, 1200, 3000):
        for P in (Fr(150), Fr(165), Fr(300)):
            # k = 2: each A comes back as 2 units, so y rises after the burst
            # and the second zero episode starts later; the A count of the
            # first episode is read off at the start of the second.
            zeros, gend = simulate(g, P=P, k=2, t_end=Fr(40 * g + 20000))
            rt = Fr(g) / vA + Fr(g) / vB
            n_pred = burst_law(g, P, Fr(0))
            n_sim = zeros[1][2] if len(zeros) > 1 else None
            ok = n_sim == n_pred
            fails += not ok
            print(f"g={g} P={P}: burst length sim {n_sim}, law floor(rt/P)+1 = {n_pred} (rt={float(rt):.1f}) {'ok' if ok else 'MISMATCH'}")
    # 2. walking reflection: each absorbed A moves the face right by aA
    #    (a reflector that walks per reflection). Zero times are then not
    #    eventually periodic: the gap grows by a fixed factor per episode.
    zeros, gend = simulate(200, prog="z", P=Fr(150), k=2, aA=Fr(22), aB=Fr(0), t_end=Fr(3 * 10**6))
    gaps = [float(z[1]) for z in zeros[:12]]
    print("walking reflector, gap at successive zero episodes:", [round(x) for x in gaps])
    ratios = [gaps[i + 1] / gaps[i] for i in range(len(gaps) - 1) if gaps[i] > 0]
    print("ratios:", [round(r, 3) for r in ratios])
    # control: a non-walking reflector gives a constant gap
    zeros0, _ = simulate(200, prog="z", P=Fr(150), k=2, aA=Fr(0), t_end=Fr(10**6))
    g0s = {z[1] for z in zeros0}
    print("control (aA = 0): distinct gaps at zero episodes:", sorted(float(x) for x in g0s))
    if len(set(round(x) for x in gaps)) < 5 or len(g0s) != 1:
        fails += 1
    print("FAILURES:", fails)
