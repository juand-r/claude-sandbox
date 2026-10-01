"""Put a raw leader K (or other block) into the initial moving data and
watch: does it cross tape data? what does an ossifier do to it?"""
import sys
from splice import *
import encoder as enc
central, T, step_ = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
right = enc._right_block_seq(["YNNNNN"]) * 3
left = (enc.OSSIFIER + "A" * 536) * 6
m = Machine(None, None, T, right_names=right, left_names=left, central="C" + central)
print([(n, a) for n, a, b in m.blocks if n not in "AB"][:8])
for t, cs in lab_trace(m, m.row, range(step_, T + 1, step_), -9000, 1500):
    print(t, " ".join(f"{k}{x}" for x, y, k in cs if k != "A" or True))
