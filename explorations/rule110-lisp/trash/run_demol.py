"""The glider-level Collatz run: De Mol's 3x+1 tag system, x=3.

Expected: 4 tag steps (AAA -> ACY -> YCY -> YAAA -> AAAAA), i.e. Collatz
3 -> 5 computed by Rule 110 gliders. One tag step = 12 CTS reads
~ 312k generations; T=1.35M covers the 4 steps plus maturation slack.

Geometry: machinery (13 left periods, 7 right periods, right edge trimmed
16 cells to a verified triple-ether-tile cut) padded with phase-matched
ether: 700k left, 1.0M right. Corruption from the wrap seam chases the
ossifier stream at relative speed 1/3 (safe to t~2.4M) and approaches the
table data at 0.733 (right pad covers T). Decoding samples a co-moving
window around the tape region only.
"""
import sys, time
import numpy as np
from encoder import assemble
from engine import ETHER, pack, unpack, step_packed
from decoder import Decoder

T = int(sys.argv[1]) if len(sys.argv) > 1 else 1_350_000
LOG_EVERY = 2500

def rot_of(chunk):
    s = "".join(map(str, chunk))
    return next((r for r in range(14) if ETHER[r:] + ETHER[:r] == s), None)

tape_cts = "YNNNNN" * 3            # A^3
apps = ["NYNNNNNNYNNN", "YNNNNN", "YNNNNNYNNNNNYNNNNN"] + [""] * 9
bits, placed = assemble(tape_cts, apps, left_periods=13, right_periods=7)
bits = bits[:-16]                  # trim to the verified ether cut
c0 = -placed[0].gspan(0)[0]        # array index of global column 0 (block C)
rl, rr = rot_of(bits[:14]), rot_of(bits[-14:])
assert rl is not None and rr is not None, ("edges not ether", rl, rr)

LPAD = 700_000 // 14 * 14
RPAD = 1_000_000 // 14 * 14
ltile = np.array([int(c) for c in ETHER[rl:] + ETHER[:rl]], dtype=np.uint8)
rtile = np.array([int(c) for c in ETHER[rr:] + ETHER[:rr]], dtype=np.uint8)
row = np.concatenate([np.tile(ltile, LPAD // 14), bits, np.tile(rtile, RPAD // 14)])
c0 += LPAD
W = len(row)
print(f"total width {W}, tape origin {c0}", flush=True)

d = Decoder()
a = pack(row)
log = open("demol_run.log", "w")
t0 = time.time()
WIN_L, WIN_R = 30_000, 90_000
for t in range(T + 1):
    if t % LOG_EVERY == 0:
        center = c0 + int(round(-8 * t / 30))
        lo, hi = max(0, center - WIN_L), min(W, center + WIN_R)
        # unpack only the word range covering the window
        wlo, whi = lo // 64, hi // 64 + 1
        cur = unpack(a[wlo:whi], (whi - wlo) * 64)
        try:
            reads = d.read(cur)
            tape = "".join(s for _, s in reads)
            pos = " ".join(str(p + wlo * 64) for p, _ in reads)
        except ValueError as e:
            tape, pos = "?", str(e)
        log.write(f"{t}\t{tape}\t{pos}\n")
        if t % 100_000 == 0:
            log.flush()
            print(f"t={t} ({time.time()-t0:.0f}s) {tape[:44]}", flush=True)
    a = step_packed(a)
np.save("demol_final.npy", a)
log.close()
print("done", f"{time.time()-t0:.0f}s", flush=True)
