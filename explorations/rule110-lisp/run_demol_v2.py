"""De Mol with balance-corrected v: period time (v*30) must match the time
for 4 reads at the leader cadence (right period width * 30/8 per 12 reads).
right period ~ 19029 cells -> cycle 71.4k steps -> period 23.8k -> v ~ 790.
Try v=790 (and log A4 arrivals + tape reads)."""
import sys
import numpy as np
from encoder import assemble, load_blocks
from decoder import Decoder, _strip_ether
from engine import ETHER, pack, unpack, step_packed

V = int(sys.argv[1]) if len(sys.argv) > 1 else 790
T = int(sys.argv[2]) if len(sys.argv) > 2 else 300_000

blocks, _ = load_blocks()
B = blocks["B"]
a4sigs = {_strip_ether(B.bits(r))[0] for r in range(45, 55)}

def rot_of(chunk):
    s = "".join(map(str, chunk))
    return next((r for r in range(14) if ETHER[r:] + ETHER[:r] == s), None)

apps = ["NYNNNNNNYNNN", "YNNNNN", "YNNNNNYNNNNNYNNNNN"] + [""] * 9
nperiods = T // int(V * 30) + 4
bits, placed = assemble("YNNNNN" * 3, apps, left_periods=nperiods,
                        right_periods=T // 71000 + 4, v_override=V)
# trim the right edge back to a clean triple-ether-tile cut
for back in range(0, 4000):
    j = len(bits) - back
    if all(rot_of(bits[j - k - 14:j - k]) is not None for k in (0, 14, 28)):
        bits = bits[:j]
        break
else:
    raise AssertionError("no clean right ether cut found")
c0 = -placed[0].gspan(0)[0]
rl, rr = rot_of(bits[:14]), rot_of(bits[-14:])
assert rl is not None and rr is not None
LPAD = (T + 50000) // 14 * 14
RPAD = (T + 100_000) // 14 * 14
lt = np.array([int(c) for c in ETHER[rl:] + ETHER[:rl]], dtype=np.uint8)
rt = np.array([int(c) for c in ETHER[rr:] + ETHER[:rr]], dtype=np.uint8)
row = np.concatenate([np.tile(lt, LPAD // 14), bits, np.tile(rt, RPAD // 14)])
c0 += LPAD
print("width", len(row), "v", V, "left periods", nperiods, flush=True)

d = Decoder()
a = pack(row)
log = open(f"demol_v{V}.log", "w")
prev_a4 = False
arrivals = []
for t in range(T + 1):
    if t % 50 == 0:
        center = c0 + int(round(-8 * t / 30))
        lo = (center - 700) // 64
        cur = unpack(a[lo:lo + 12], 12 * 64)
        s = cur.tobytes().translate(bytes.maketrans(b"\x00\x01", b"01")).decode()
        p = any(sig in s for sig in a4sigs)
        if p and not prev_a4:
            arrivals.append(t)
        prev_a4 = p
    if t % 2500 == 0:
        center = c0 + int(round(-8 * t / 30))
        lo, hi = (center - 5000) // 64, (center + 60000) // 64
        cur = unpack(a[lo:hi], (hi - lo) * 64)
        try:
            tape = "".join(sym for _, sym in d.read(cur))
        except ValueError:
            tape = "?"
        log.write(f"{t}\t{tape}\n")
        if t % 50000 == 0:
            log.flush()
            print(f"t={t} arrivals={len(arrivals)} tape={tape[:40]}", flush=True)
    a = step_packed(a)
log.close()
print("A4 arrivals:", arrivals, flush=True)
