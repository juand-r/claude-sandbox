import sys
from splice import *
from t_base2 import classify, T
tape = sys.argv[1]
m = Machine(tape, ["YNNNNN"], T)
o = m.origin
new = replace_region(m.row, o + 2489, o + 2935, [])
for t, cs in trace(m, new, range(600, 16001, 600), 1100, 4400):
    print(t, classify(cs)["A"], classify(cs)["B"], " ".join(f"{k}{x}" for x, y, k in cs if k != "E" or 2400 < x < 3000))
