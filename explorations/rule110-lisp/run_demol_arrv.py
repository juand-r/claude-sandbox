"""Original-v De Mol: A4 arrivals per period at front-1000, t=0..420k."""
import numpy as np
from encoder import assemble, load_blocks
from decoder import _strip_ether
from engine import ETHER, pack, unpack, step_packed

blocks, _ = load_blocks()
B = blocks["B"]
sigs = {_strip_ether(B.bits(r))[0] for r in range(45, 55)}
def rot_of(chunk):
    s = "".join(map(str, chunk))
    return next((r for r in range(14) if ETHER[r:] + ETHER[:r] == s), None)
apps = ["NYNNNNNNYNNN", "YNNNNN", "YNNNNNYNNNNNYNNNNN"] + [""] * 9
bits, placed = assemble("YNNNNN" * 3, apps, left_periods=13, right_periods=7)
bits = bits[:-16]
c0 = -placed[0].gspan(0)[0]
rl, rr = rot_of(bits[:14]), rot_of(bits[-14:])
LPAD = 700_000 // 14 * 14; RPAD = 1_000_000 // 14 * 14
lt = np.array([int(c) for c in ETHER[rl:] + ETHER[:rl]], dtype=np.uint8)
rt = np.array([int(c) for c in ETHER[rr:] + ETHER[:rr]], dtype=np.uint8)
row = np.concatenate([np.tile(lt, LPAD // 14), bits, np.tile(rt, RPAD // 14)])
c0 += LPAD
a = pack(row)
arr = []
prev = False
for t in range(420_001):
    if t % 40 == 0:
        center = c0 + int(round(-8 * t / 30))
        lo = (center - 1100) // 64
        cur = unpack(a[lo:lo + 10], 10 * 64)
        s = cur.tobytes().translate(bytes.maketrans(b"\x00\x01", b"01")).decode()
        p = any(sig in s for sig in sigs)
        if p and not prev:
            arr.append(t)
        prev = p
    a = step_packed(a)
print("arrivals at front-1000:", arr)
