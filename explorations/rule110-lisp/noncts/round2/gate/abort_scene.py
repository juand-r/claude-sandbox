"""Step 1 of the F-lane ABORT [exact CA]: a stationary C1 messenger eats k
Ebar-pair packets and is then removed by a GATE packet.

Neutral eaters (c1_algebra.py): C1 + Ebar@(0,0)+Ebar@(-4,23) #3 -> C1 moved
by (3,16), and C1 + Ebar@(0,0)+Ebar@(-22,39) #3 -> C1 moved by (1,24); both
displacements lie in L = <(7,0),(30,-8)>, so the C1 keeps its class relative
to the stream. Hence the packets can be placed ONCE, each in class 3
relative to the ORIGINAL C1 (a fixed stream), and every one of them is
eaten however many were eaten before it. The gate Ebar@(0,0)+E@(-9,29) #3
then removes the C1, leaving one Ebar.

Packets are spaced by multiples of (0,56) (in L, class-preserving).
Usage: python abort_scene.py SEQ [--noc1] [--shift i:dt,dx]
  SEQ letters: a = (-4,23) pair, b = (-22,39) pair, g = gate.
"""
import sys
import common  # noqa: F401
from common import LIB, canonical_reps
from stream import run, ca_only
from glidersim import ThreeBody

TYPES = {"a": ("Ebar@(0,0)+Ebar@(-4,23)", 3), "b": ("Ebar@(0,0)+Ebar@(-22,39)", 3),
         "g": ("Ebar@(0,0)+E@(-9,29)", 3)}
STEP = 56 * 3


def build(seq, c1=True, shifts=None):
    shifts = shifts or {}
    scene = [("C1", 0, 0)] if c1 else []
    for i, ch in enumerate(seq):
        Y, c = TYPES[ch]
        rep = canonical_reps(LIB, "C1", Y)[c]
        dt, dx = shifts.get(i, (0, 0))
        scene.append((Y, rep[0] + dt, rep[1] + STEP * (i + 1) + dx))
    return scene


if __name__ == "__main__":
    seq = sys.argv[1]
    shifts = {}
    if "--shift" in sys.argv:
        a, b = sys.argv[sys.argv.index("--shift") + 1].split(":")
        dt, dx = map(int, b.split(","))
        shifts[int(a)] = (dt, dx)
    sc = build(seq, c1="--noc1" not in sys.argv, shifts=shifts)
    print("scene", sc)
    try:
        st, log, ok = run(sc, ca="fast")
        print("final", [g[0] for g in st], "CA==glidersim", ok)
        print("events", [(e[2][:14], e[3][:24], e[4], e[5]) for e in log])
    except ThreeBody as e:
        names, settled = ca_only(sc)
        print("glidersim 3-body:", str(e)[:80], "| exact CA objects:", names)
