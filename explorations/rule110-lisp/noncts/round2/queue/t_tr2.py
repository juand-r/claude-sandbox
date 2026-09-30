import sys
from splice import *
A0 = "HIIJIJIJIJIJ"
REST = "HIIJIJIJIJIJK" * 2
var, tape, t1 = sys.argv[1], sys.argv[2], int(sys.argv[3])
seq = A0 + var + REST
m = Machine(tape, None, t1, right_names=seq)
print([(n, a) for n, a, b in m.blocks if 3000 < a < 9000])
for t, cs in trace(m, m.row, range(1200, t1 + 1, 600), 1100, 9000):
    print(t, sum(1 for x, y, k in cs if k == "E"), " ".join(f"{k}{x}" for x, y, k in cs if k != "E"))
