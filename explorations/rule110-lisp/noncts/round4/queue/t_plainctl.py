import sys
from reads import *
tape, nread = sys.argv[1], int(sys.argv[2])
got, times, m = check(tape, ["YNNNNN"], nread, None)
print(tape, "plain from t=0:", got, reference(tape, ["YNNNNN"], "K" * nread, nread), times)
class Id:
    t_in = 31500
    def __call__(self, m, row): return row
got, times, m = check(tape, ["YNNNNN"], nread, Id())
print(tape, "plain from t_in (identity surgery):", got, times)
