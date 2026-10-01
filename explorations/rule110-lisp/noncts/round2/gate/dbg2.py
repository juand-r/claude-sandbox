import sys
from adaptive import build, outcome
v = int(sys.argv[1]); prog = sys.argv[2]; cls = [int(c) for c in sys.argv[3].split(",")]
sc = build(["I"] * v + list(prog), [0] * v + cls)
st, log = outcome(sc)
print(st)
for l in log: print(l)
