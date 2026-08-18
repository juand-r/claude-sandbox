"""Layer 2 (part): reference cyclic tag system interpreter.

Semantics: at each step, remove the tape's first symbol; if it is Y, append
the current appendant to the tape; advance to the next appendant cyclically.
Halts when the tape is empty.
"""

from collections import deque


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
