"""Diagnose the forced-N (E9) leader: first K only modified; full read check."""
from verify_lead import *
def e9_first(m):
    K = [a for n, a, b in m.blocks if n == "K"][0]
    return replace_exact(m.row, m.origin + K + 41, m.origin + K + 72, [(en_tiles(9), 14, 9)], 0, 0)
for tape in ("YYNN", "YNYN"):
    for name, fn, kinds in (("plain", lambda m: m.row, "KKKKKKK"), ("E9", e9_first, "KFKKKKK")):
        got, ref, times = check(tape, ["YNNNNN"], fn, kinds, 6)
        print(tape, name, "obs", got, "ref", ref, times, flush=True)
