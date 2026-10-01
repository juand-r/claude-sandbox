"""Full-machine multi-read check (surgery at t_in = 31500, rej path): Z = one
library object (name, k, x rel K0) in front of P_1.
    python t_forcedZ.py TAPE NREAD NAME k x [KINDS]"""
import sys
from reads import *
tape, nread, name, k, x = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
kinds = sys.argv[6] if len(sys.argv) > 6 else "KF"
apps = ["YNNNNN"]; tiles = glider_tiles(name)
class Surg:
    t_in = 31500
    def __call__(self, m, row):
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        return rewrite(row, m.origin, self.t_in, K0 - 345, K0 + 37, [(tiles, k, K0 + x)])
got, times, m = check(tape, apps, nread, Surg())
ref = reference(tape, apps, kinds + "K" * nread, nread)
print(tape, name, k, x, "observed", got, "reference", ref, "MATCH(reads>=1)" if got[1:] == ref[1:] else "DIFFER", times, flush=True)
