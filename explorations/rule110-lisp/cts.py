"""Layer 2 (part): reference cyclic tag system interpreter.

Semantics: at each step, remove the tape's first symbol; if it is Y, append
the current appendant to the tape; advance to the next appendant cyclically.
Halts when the tape is empty.
"""

from collections import deque
from math import lcm

# Cook's glider construction needs appendant lengths that are multiples of 6
# (encoder.py).
LENGTH_UNIT = 6


def run(tape, appendants, max_steps, sample=1):
    """Yield (step, tape, appendant_index) before each step, but only for
    steps divisible by `sample` (tape stringification is O(n), so callers
    doing long runs should sample at their period of interest). Always
    yields the final state. Stops when the tape empties or max_steps is
    reached."""
    tape = deque(tape)
    k = len(appendants)
    for n in range(max_steps):
        if n % sample == 0:
            yield n, "".join(tape), n % k
        if not tape:
            return
        sym = tape.popleft()
        if sym == "Y":
            tape.extend(appendants[n % k])
    yield max_steps, "".join(tape), max_steps % k


def fill_empty_appendants(appendants):
    """Replace every empty appendant by N^m, m = lcm(len(appendants), 6).

    Exact: the junk N's are only ever read as N, which appends nothing,
    and they delay every later symbol by m reads, a multiple of the
    appendant cycle, so each later symbol is still read with the same
    appendant. The Y/N read sequence gains runs of N reads and is
    otherwise unchanged. Purpose: Cook's construction then needs no raw
    short leader (block L), whose glider realization fails (REPORT.md 3.4).
    Cost: each Y read on a formerly empty appendant adds m N reads, and
    the table data (hence v) grows by the junk.
    """
    m = lcm(len(appendants), LENGTH_UNIT)
    return [a if a else "N" * m for a in appendants]
