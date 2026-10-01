"""B^2 (placement phase 2, offset 65 relative to the front symbol) hitting
the FRONT of a two-symbol tape cut from a running machine: does it eat
exactly the front symbol, and do the two Ebars then cross the second
symbol? Control: no B's."""
import sys
from splice import *
from slips import groups

def two_symbols(tape="YYYY", t=40000):
    m = Machine(tape, ["YNNNNN"], t + 10, left_periods=4, right_periods=2)
    r = Run(m.row, m.origin)
    r.step(t - MAX_DT)
    lo, hi = m.origin - 8000, m.origin + 3000
    h = r.history(lo, hi, MAX_DT)
    cs = census(h)
    row = h[-1]
    gs = [(a, b) for a, b in groups(row)
          if all(k == "C" for x, y, k in cs if a <= x < b) and sum(1 for x, y, k in cs if a <= x < b) >= 4]
    return row, gs, cs

row, gs, cs = two_symbols()
print("C groups:", gs)
