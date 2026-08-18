"""Validation run 2: always-append grower {YYYYYY}, tape Y.
Every read appends, so the paper's default v is legitimate. Any decoded N
is an error; decoded tape length should march up the reference sequence."""
import sys, time
import numpy as np
from encoder import assemble
from engine import step
from decoder import Decoder

T = int(sys.argv[1]) if len(sys.argv) > 1 else 70_000
bits, placed = assemble("Y", ["YYYYYY"], left_periods=4, right_periods=24)
print("width", len(bits), flush=True)
d = Decoder()
log = open("grower_run.log", "w")
cur = bits
t0 = time.time()
for t in range(T + 1):
    if t % 50 == 0:
        try:
            reads = d.read(cur)
            tape = "".join(s for _, s in reads)
            pos = " ".join(str(p) for p, _ in reads)
        except ValueError as e:
            tape, pos = "?", str(e)
        log.write(f"{t}\t{tape}\t{pos}\n")
    if t % 20000 == 0:
        log.flush(); print(f"t={t} {time.time()-t0:.0f}s", flush=True)
    cur = step(cur)
np.save("grower_final.npy", cur)
log.close()
print("done")
