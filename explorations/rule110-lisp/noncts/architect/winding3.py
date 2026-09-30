"""Winding test with multi-body packets (collider's catalog of F vs Ebar
pairs). Register = two F's, T (front, at origin) and P (back, at -D).
A mover (Ebar or a 2-Ebar packet) crosses T; its outputs (Ebar-speed
gliders only, F must survive) then cross P one by one. The change of D is
recorded; BFS over residues of D mod <P_F, P_Ebar>; a transition winds if
it reaches a known residue with a different exact D. Winding = a
crossing-only counter exists."""
import os, sys, json
from collections import deque
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../collider"))
os.chdir(os.path.join(HERE, "../collider"))
from predict import predict, LIB, _by
_by()
from collide import canonical_reps
from r110lib import class_key
os.chdir(HERE)

PF, PE = (36, -4), (30, -8)
ROWS = json.load(open("../collider/collisions.json"))
EBAR_SPEED = {n for n, g in LIB.gliders.items() if g.p and g.d * 30 == -8 * g.p}
PACKETS = sorted({r["Y"] for r in ROWS if r["X"] == "F" and r["Y"] in EBAR_SPEED})


def cross(Fseed, mover):
    """mover = (name, t, x). -> (F final seed, [ebar-speed outputs]) or None."""
    name, t, x = mover
    try:
        k, prods = predict("F", name, (t - Fseed[0], x - Fseed[1]), eX=Fseed)
    except (ValueError, KeyError, AssertionError):
        return None
    fs = [p for p in prods if p[0] == "F"]
    rest = [p for p in prods if p[0] != "F"]
    if len(fs) != 1 or not all(p[0] in EBAR_SPEED for p in rest) or not rest:
        return None
    return (fs[0][1], fs[0][2]), rest


def lateral(p):
    g = LIB.gliders[p[0]]
    return p[2] - g.velocity * p[1]


def apply(mover, D):
    """Mover crosses T at (0,0), then its outputs cross P at -D."""
    r = cross((0, 0), mover)
    if r is None:
        return None
    T2, outs = r
    P = (-D[0], -D[1])
    for o in sorted(outs, key=lateral):     # leftmost trajectory arrives first
        rr = cross(P, o)
        if rr is None:
            return None
        P = rr[0]
    return (T2[0] - P[0], T2[1] - P[1])     # new D (exact, normalized seeds)


def movers():
    out = []
    for name in PACKETS:
        g = LIB.gliders[name]
        for rep in canonical_reps(LIB, "F", name):
            out.append((name,) + tuple(rep))
    return out


def analyse(D0):
    MV = movers()
    key = lambda D: class_key(D, PF, PE)
    V = {key(D0): D0}
    q = deque([D0])
    wind, edges = [], 0
    while q:
        D = q.popleft()
        for mv in MV:
            D2 = apply(mv, D)
            if D2 is None:
                continue
            edges += 1
            k2 = key(D2)
            if k2 not in V:
                V[k2] = D2
                q.append(D2)
            else:
                d = (D2[0] - V[k2][0], D2[1] - V[k2][1])
                # same trajectory for P? D differs by a multiple of P_F only if
                # the F positions coincide: compare normalized difference
                if d != (0, 0) and not (d[0] % 36 == 0 and d[1] == -4 * (d[0] // 36)):
                    wind.append((mv, V[k2], D2))
    print(f"D0={D0}: movers {len(MV)}, residues {len(V)}, transitions {edges}, "
          f"winding {len(wind)}")
    for w in wind[:8]:
        print("   ", w)
    return wind


if __name__ == "__main__":
    for D0 in [(0, 43), (0, 71), (0, 99)]:
        analyse(D0)


def same_traj(d):
    return d[0] % 36 == 0 and d[1] == -4 * (d[0] // 36)


def find_cycles(D0, max_len=4, max_found=20):
    """Shortest mover sequences returning D to D0's residue with a net
    change that is not a multiple of F's period."""
    MV = movers()
    key = lambda D: class_key(D, PF, PE)
    k0 = key(D0)
    # precompute transitions per residue lazily
    trans = {}

    def moves(D):
        k = key(D)
        if k not in trans:
            lst = []
            for mv in MV:
                D2 = apply(mv, D)
                if D2 is not None:
                    lst.append((mv, (D2[0] - D[0], D2[1] - D[1])))
            trans[k] = lst
        return trans[k]

    found = {}
    q = deque([(D0, ())])
    seen = {(k0, (0, 0))}
    while q and len(found) < max_found:
        D, seq = q.popleft()
        if len(seq) >= max_len:
            continue
        for mv, dD in moves(D):
            D2 = (D[0] + dD[0], D[1] + dD[1])
            net = (D2[0] - D0[0], D2[1] - D0[1])
            s2 = seq + (mv,)
            if key(D2) == k0 and not same_traj(net):
                # canonical net modulo F period for reporting
                if net not in found:
                    found[net] = s2
                continue
            st = (key(D2), net)
            if st in seen or abs(net[1]) > 60:
                continue
            seen.add(st)
            q.append((D2, s2))
    return found
