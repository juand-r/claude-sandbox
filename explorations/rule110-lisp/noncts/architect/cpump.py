"""Can stationary C pairs pump an F pair (upstream register B)?

In the lab an F pair (T left, P right, gap D) drifts left over a
stationary C pair (Ca left, Cb right). T meets the pair first, then P meets
whatever the pair has become. We simulate each stage (no catalog) and run
the winding BFS over residues of D mod <P_F, P_E-ish>: here the relevant
lattice for C vs F is <(7,0),(36,-4)>, and a mover 'C pair' is placed by
the class of Cb vs T and the internal gap.
Outputs: winding transitions (a crossing-only counter operated from the
left) or none."""
import sys
from collections import deque
from rx import run, chain, G as GL, cls_of, canonical_reps, LIB
from m1_predict import norm_seed
from r110lib import class_key

PF = (36, -4)
LCF = ((7, 0), (36, -4))


def pair_seeds(a, b, gap, t0=0):
    """C pair Ca at (0, 0), Cb (time phase t0) placed right of it,
    ether-consistent."""
    p = chain((a, 0, 0), [(b, t0, gap)])
    return p[0], p[1]


def stage(Fseed, Cs, T=3000):
    """F at Fseed crosses stationary C's Cs (list of seeds, left of F).
    -> (F', Cs') or None if not clean (F must survive, only C's left)."""
    pl = list(Cs) + [("F",) + Fseed]
    try:
        prods = run(pl, T)
    except Exception:
        return None
    fs = [p for p in prods if p[0] == "F"]
    cs = [p for p in prods if p[0] in ("C1", "C2", "C3")]
    if len(fs) != 1 or len(cs) != len(Cs) or len(prods) != len(Cs) + 1:
        return None
    return (fs[0][1], fs[0][2]), sorted(cs, key=lambda c: c[2])


def movers(max_gap=40):
    out = []
    for a in ("C1", "C2"):
        for b in ("C1", "C2"):
            for gap in range(6, max_gap):
                for t0 in range(7):
                    try:
                        ca, cb = pair_seeds(a, b, gap, t0)
                    except Exception:
                        continue
                    out.append((ca, cb))
    # dedupe by (types, relative vector)
    seen, res = set(), []
    for ca, cb in out:
        k = (ca[0], cb[0], cb[1] - ca[1], cb[2] - ca[2])
        if k not in seen:
            seen.add(k)
            res.append((ca, cb))
    return res


def apply(mv, D, T0=(0, 200)):
    """Place the C pair so that Cb is in each of the 2 classes vs T.
    T at T0, P at T0 + D (P is right of T). Returns list of (cls, D')."""
    ca, cb = mv
    res = []
    for k, rep in enumerate(canonical_reps(LIB, cb[0], "F")):
        # rep = F relative to Cb; we want Cb relative to T: Cb = T - rep
        cbp = (T0[0] - rep[0], T0[1] - rep[1])
        shift = (cbp[0] - cb[1], cbp[1] - cb[2])
        Cs = [(ca[0], ca[1] + shift[0], ca[2] + shift[1]), (cb[0],) + cbp]
        s1 = stage(T0, Cs)
        if s1 is None:
            continue
        T1, Cs1 = s1
        P0 = (T0[0] + D[0], T0[1] + D[1])
        s2 = stage(P0, [tuple(c) for c in Cs1])
        if s2 is None:
            continue
        P1, _ = s2
        res.append((k, (P1[0] - T1[0], P1[1] - T1[1])))
    return res


if __name__ == "__main__":
    MV = movers(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
    print("C-pair movers:", len(MV), flush=True)
    D0 = (0, 43)
    key = lambda D: class_key(D, (36, -4), (30, -8))   # finer: must also stay lane for stream Ebars
    V = {key(D0): D0}
    q = deque([D0])
    wind = 0
    while q:
        D = q.popleft()
        for mv in MV:
            for k, D2 in apply(mv, D):
                kk = key(D2)
                if kk not in V:
                    V[kk] = D2
                    q.append(D2)
                    print("new residue", kk, D2, "via", mv, k, flush=True)
                else:
                    d = (D2[0] - V[kk][0], D2[1] - V[kk][1])
                    if not (d[0] % 36 == 0 and d[1] == -4 * (d[0] // 36)):
                        wind += 1
                        print("WINDING", mv, k, "from", D, "->", D2, "known", V[kk], flush=True)
    print("residues", len(V), "winding", wind)
