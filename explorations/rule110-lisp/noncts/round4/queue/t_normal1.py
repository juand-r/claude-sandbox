"""Control experiment: Z = Ebar pair that leaves read 1 NORMAL; do later reads
stay correct (debris harmless?).  python t_normal1.py TAPE NREAD k2 x2 k1 x1 KINDS"""
import sys
from reads import *
tape, nread = sys.argv[1], int(sys.argv[2]); k2, x2, k1, x1 = map(int, sys.argv[3:7]); kinds = sys.argv[7]
apps = ["YNNNNN"]; E = ebar_tiles()
class Surg:
    t_in = 31500
    def __call__(self, m, row):
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        return rewrite(row, m.origin, self.t_in, K0 - 345, K0 + 37, [(E, k2, K0 + x2), (E, k1, K0 + x1)])
got, times, m = check(tape, apps, nread, Surg())
ref = reference(tape, apps, kinds + "K" * nread, nread)
print(tape, (k2, x2, k1, x1), "observed", got, "reference", ref, "(read 0 '!' = artifact of mid-run start)", times, flush=True)
