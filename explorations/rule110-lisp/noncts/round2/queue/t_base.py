import time
from splice import *
T = 16000
m = Machine("YN", ["YNNNNN"], T)
o = m.origin
for n, a, b in m.blocks:
    if n in "HIJK":
        c = ether_cut(m.row, o + a)
        print(n, a, c - o, len(defects_in(m.row, c, ether_cut(m.row, o + b))))
