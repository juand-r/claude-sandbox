"""Raw leader K (or other block) as an item of the initial moving data:
compare appendant-region outcomes with the plain tape."""
import sys
from splice import *
import encoder as enc
T = int(sys.argv[1])
right = enc._right_block_seq(["YNNNNN"]) * 5
left = (enc.OSSIFIER + "A" * 536) * 8
for central in sys.argv[2:]:
    m = Machine(None, None, T, right_names=right, left_names=left, central="C" + central)
    K = [a for n, a, b in m.blocks if n == "K"]
    G = [a for n, a, b in m.blocks if n == "G"][0]
    bounds = [G] + [k for k in K if k > G]
    cs = m.run(m.row, T, -1000, K[4] + 300)
    print(central, [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in zip(bounds, bounds[1:])],
          [f"{k}{x}" for x, y, k in cs if k != "E"], flush=True)
