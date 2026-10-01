"""Build block X = K with E2 -> E9 (placement (14,9), no shift) and check:
(1) X built from an UNEDITED row equals K; (2) a machine with X in place of
the first K reproduces the replace_exact run."""
import sys
from splice import *
import encoder as enc
T = 60000
m = Machine("YYNN", ["YNNNNN"], T, left_periods=4, right_periods=3)
_, placed = enc.assemble("YYNN", ["YNNNNN"], 4, 3)
K0 = [p for p in placed if p.block.name == "K"][0]
o = m.origin
Kpos = K0.gspan(0)[0]
blocks, _ = enc.load_blocks()
Xid = make_block("Q", blocks["K"], K0, m.row, o)
same = all(Xid._rows[r] == blocks["K"]._rows[r] for r in range(35, 65))
print("unedited copy equals K:", same)
new = replace_exact(m.row, o + Kpos + 41, o + Kpos + 72, [(en_tiles(9), 14, 9)], 0, 0)
X = make_block("X", blocks["K"], K0, new, o)
seq = enc._right_block_seq(["YNNNNN"]) * 3
seqX = seq.replace("K", "X", 1)
mX = Machine("YYNN", None, T, right_names=seqX, left_names=(enc.OSSIFIER + "A" * 536) * 4)
m2 = Machine("YYNN", None, T, right_names=seq, left_names=(enc.OSSIFIER + "A" * 536) * 4)
K = [a for n, a, b in m2.blocks if n == "K"]
print("X at", [a for n, a, b in mX.blocks if n == "X"], "K at", K[:3])
for name, mm in (("K", m2), ("X", mX)):
    cs = mm.run(mm.row, T, 1100, K[2] + 300)
    print(name, [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in [(1100, K[0]), (K[0], K[1])]])
cs = m.run(new, T, 1100, K[2] + 300)
print("replace_exact", [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in [(1100, K[0]), (K[0], K[1])]])
