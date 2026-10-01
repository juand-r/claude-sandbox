"""When does tape symbol s_1 reach the prepared leader P_1 (= K[0])?"""
import sys
from q import *
tape = sys.argv[1]
times = list(range(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))
m = Machine(tape, ["YNNNNN"], max(times)+500, left_periods=3, right_periods=2)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
for t, cs in trace(m, m.row, times, K0 - 1200, K0 + 150):
    print(t, " ".join(f"{k}{a-K0}" for a, b, k in cs))
