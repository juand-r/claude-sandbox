"""Full-machine multi-read check (surgery at t_in = 31500, rej path, region
[K0-345, K0+37)): Z = items 'name:k:x;name:k:x' (x rel K0, tiles may
overlap in margins).  python t_zfull.py TAPE NREAD ITEMS [KINDS]
Read 0 shows '!' (artifact: the run starts after read 0)."""
import sys
from reads import *
tape, nread, spec = sys.argv[1], int(sys.argv[2]), sys.argv[3]
kinds = sys.argv[4] if len(sys.argv) > 4 else "KF"
items = [(tiles_of(n), int(k), int(x)) for n, k, x in (s.split(":") for s in spec.split(";"))]
apps = ["YNNNNN"]
class Surg:
    t_in = 31500
    def __call__(self, m, row):
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        return rewrite2(row, m.origin, self.t_in, K0 - 345, K0 + 37, [(t, k, K0 + x) for t, k, x in items])
got, times, m = check(tape, apps, nread, Surg())
ref = reference(tape, apps, kinds + "K" * nread, nread)
print(tape, spec, "observed", got, "reference", ref, "MATCH(reads>=1)" if got[1:] == ref[1:] else "DIFFER", times, flush=True)
