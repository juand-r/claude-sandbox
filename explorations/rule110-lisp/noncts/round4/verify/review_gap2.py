"""Review of theory's gap2.py (route 20): does the destination window W_R,
which walks OUT toward its own incoming stream, jump over packets that are
in flight between its old and new position? (Physical glider windows
cannot: a packet in that zone collides with the window.)

Independent event re-implementation of W_R alone: left-moving packets
x_n(t) = -vp (t - nP) (packet n passes x = 0 at t = nP); the window at b
takes a step +u on every kR-th packet it meets. A packet is SKIPPED if its
worldline is strictly between the old and new window position at a step.
Report skipped/met counts for theory's commensurate and incommensurate
geometries, and for a 'physical' geometry (u < vp P)."""
from fractions import Fraction as Fr
import math
import sys


def run(u, vp, P, kR, steps=60):
    b, t, n_next = Fr(0), Fr(0), 0
    met = skipped = 0
    i = 0
    walks = 0
    while walks < steps:
        # packet n meets static window at b at time t_n = nP - b/vp
        n = max(n_next, math.ceil(t / P + b / (vp * P)))
        tn = n * P - b / vp
        t = tn
        met += 1
        n_next = n + 1
        if i % kR == 0:
            nb = b + u
            # packets n' > n with position strictly inside (b, nb) at time t are skipped
            for m in range(n + 1, n + 1000):
                x = -vp * (t - m * P)
                if x >= nb:
                    break
                if x > b:
                    skipped += 1
                    n_next = max(n_next, m + 1)
            b = nb
            walks += 1
        i += 1
    return met, skipped


if __name__ == "__main__":
    for name, u, vp, P in (("theory commensurate", Fr(4), Fr(1, 3), Fr(6)),
                           ("theory incommensurate", Fr(5), Fr(1, 3), Fr(7)),
                           ("glider-like (u < vp P)", Fr(24), Fr(1, 3), Fr(476 * 3))):
        for kR in (2, 3, 5):
            met, sk = run(u, vp, P, kR)
            print(f"{name}, kR={kR}: packets met {met}, skipped while walking out {sk}")


def exactness_scan():
    """theory's own gap2.transfer on geometries WITHOUT skipping (u < vp P):
    is any transfer exact (one constant offset)?"""
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "theory"))
    import gap2
    for u, vp, vs, P in ((Fr(1), Fr(1, 3), Fr(2, 3), Fr(6)), (Fr(1), Fr(1, 3), Fr(1, 2), Fr(6)),
                         (Fr(1), Fr(1, 4), Fr(1, 2), Fr(8)), (Fr(1), Fr(1, 5), Fr(1, 2), Fr(10)),
                         (Fr(2), Fr(1, 3), Fr(2, 3), Fr(12))):
        for kL, kR in ((1, 2), (2, 2), (1, 3), (1, 5)):
            try:
                m, alpha, offs, outs = gap2.period_test(dict(u=u, vp=vp, vs=vs, P=P, kL=kL, kR=kR),
                                                        gmax=300, mmax=150, g0=60)
            except RuntimeError:
                print(f"u={u} vp={vp} vs={vs} P={P} mask={kL, kR}: no end")
                continue
            print(f"u={u} vp={vp} vs={vs} P={P} (u/(vp P) = {u / (vp * P)}) mask={kL, kR}: "
                  f"period {m}, slope {alpha}, {len(offs) if offs else '-'} offsets")


if __name__ == "__main__" and len(sys.argv) > 1:
    exactness_scan()
