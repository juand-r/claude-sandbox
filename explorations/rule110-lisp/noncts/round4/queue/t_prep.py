"""P1: prepared leader after a rejected appendant of length L (phase L mod 6).
Census (Ebar frame) around K[0] relative to K[0]'s start."""
import sys
from q import *
L = int(sys.argv[1]); tape = sys.argv[2]
times = list(map(int, sys.argv[3].split(',')))
m = Machine(tape, ["N"*L, "YNNNNN"], max(times)+500, left_periods=3, right_periods=2)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
for t, cs in trace(m, m.row, times, K0 - 1500, K0 + 500):
    print(t, " ".join(f"{k}{a-K0}" for a, b, k in cs))
