"""Validation run 3: {YYYYNN} from tape YYYYNN, v tripled (rejection runs
of length 2 exceed the paper's one-append-per-cycle assumption).
Logs positions for consumed-sequence and quiescent-prefix analysis."""
import time
import numpy as np
from encoder import assemble, _left_v
from engine import step
from decoder import Decoder

TAPE, APPS = "YYYYNN", ["YYYYNN"]
T = 200_000
v3 = 3 * _left_v(APPS)
bits, placed = assemble(TAPE, APPS, left_periods=5, right_periods=25, v_override=v3)
print("width", len(bits), "v", v3, flush=True)
d = Decoder()
log = open("mixed_run.log", "w")
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
    if t % 25000 == 0:
        log.flush(); print(f"t={t} {time.time()-t0:.0f}s", flush=True)
    cur = step(cur)
log.close()
np.save("mixed_final.npy", cur)
print("done")
