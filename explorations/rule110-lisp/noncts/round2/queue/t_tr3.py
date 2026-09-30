import sys
from splice import *
tape, k, oo, t1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
m = Machine(tape, ["YNNNNN"], t1)
c = ether_cut(m.row, m.origin + 3847)
new = insert_items(m.row, c, [(k, oo)])
for t, cs in trace(m, new, range(7200, t1 + 1, 600), 3000, 7400):
    print(t, sum(1 for x, y, kk in cs if kk == "E" and x >= 3823), sum(1 for x, y, kk in cs if kk == "E" and x >= 4200),
          " ".join(f"{kk}{x}" for x, y, kk in cs if kk != "E"))
