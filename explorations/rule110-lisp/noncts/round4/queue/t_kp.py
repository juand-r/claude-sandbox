"""Stage B for an option-(c) witness K' (bits from sat_k.jsonl): write K'
into the Ebar-frame region [K+FL, K+FR) of the full machine at t = 6000
(same time phase as the SAT scenes, nothing has reached K yet) and run the
decoder-free multi-read check on the four tapes (VMULT env, default 2).
    python t_kp.py LINE_NO [NREAD]"""
import sys, json, os
import numpy as np
from reads import *
from r110sat import ether_bit
from sat_k import phase_glob
recs = [json.loads(l) for l in open("/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue/sat_k.jsonl")]
r0 = recs[int(sys.argv[1])]
nread = int(sys.argv[2]) if len(sys.argv) > 2 else 6
bits = np.array([int(c) for c in r0["Kp"]], np.uint8)
FL, FR = r0["FL"], r0["FR"]
class Surg:
    t_in = 6000
    def __call__(self, m, row):
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        sh = ebar_shift(m.origin, self.t_in)
        a, b = K0 + FL + sh, K0 + FR + sh
        pgL = phase_glob(row[a - 14:a], a - 14); pgR = phase_glob(row[b:b + 14], b)
        X = a - ((a + pgL) % 14)
        assert X + len(bits) == b
        new = row.copy(); new[X:b] = bits
        return new
for tape in ("YYNN", "YNYN", "NYYN", "NNYY"):
    got, times, m = check(tape, ["YNNNNN"], nread, Surg())
    print(tape, r0["mode"], FL, FR, "observed", got, "plain reference", reference(tape, ["YNNNNN"], "K" * nread, nread), flush=True)
