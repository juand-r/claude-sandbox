"""Decoder-free multi-read check of a machine whose leaders may be
modified. Reference: a queue machine where read i uses appendant i % p and
leader type kinds[i] ('K' normal, 'F' forced-N: consume, append nothing).
Observed: splice.read_outcomes_row on the components region of each
appendant copy. Prints observed vs reference."""
import sys
from collections import deque
from splice import *
import encoder as enc

def reference(tape, apps, kinds, n):
    q = deque(tape); out = ""
    for i in range(n):
        if not q:
            break
        s = q.popleft()
        a = apps[i % len(apps)]
        if kinds[i] == "F":
            out += "N"
        else:
            out += s
            if s == "Y":
                q.extend(a)
    return out

def regions_of(m, nread):
    lead = [(a, b) for n, a, b in m.blocks if n in "GKX"]
    return [(b1, a2) for (a1, b1), (a2, b2) in zip(lead, lead[1:])][:nread]

def check(tape, apps, row_fn, kinds, nread, T=None):
    v = enc._left_v(apps)
    T = T or (nread + 3) * 2 * 30 * v
    m = Machine(tape, apps, T, left_periods=T // (30 * v) + 3,
                right_periods=nread // len(apps) + 3)
    row = row_fn(m)
    regs = regions_of(m, nread)
    got, times = read_outcomes_row(row, m.origin, regs, T,
                                   per_symbol=[len(apps[j % len(apps)]) for j in range(nread)])
    ref = reference(tape, apps, kinds, nread)
    return got, ref, times
