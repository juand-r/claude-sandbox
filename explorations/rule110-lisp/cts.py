"""Layer 2 (part): reference cyclic tag system interpreter.

Semantics: at each step, remove the tape's first symbol; if it is Y, append
the current appendant to the tape; advance to the next appendant cyclically.
Halts when the tape is empty.
"""


def run(tape, appendants, max_steps):
    """Yield (step, tape, appendant_index) before each step; stop when the
    tape empties or max_steps is reached."""
    tape = list(tape)
    i = 0
    for n in range(max_steps):
        yield n, "".join(tape), i % len(appendants)
        if not tape:
            return
        sym = tape.pop(0)
        if sym == "Y":
            tape.extend(appendants[i % len(appendants)])
        i += 1
    yield max_steps, "".join(tape), i % len(appendants)
