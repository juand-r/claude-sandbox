"""Layer 2: tag systems and the tag-system -> cyclic-tag-system compiler.

A tag system with deletion number s: each step removes s symbols from the
front of the tape and appends the appendant of the FIRST removed symbol.
It halts when fewer than s symbols remain. (Following Cook 2009, a halting
TM transition compiles to an empty appendant, so a halted computation
drains its tape until this condition holds.)

Symbols can be any hashable values (single characters, strings, tuples).
A rule may map to None to declare a symbol that must never be read; run()
raises if it is.

The TS -> CTS conversion (Cook 2009): order the alphabet, pad with dummy
empty rules until |Phi| is a multiple of 6, unary-encode symbol phi_i as
N^(i-1) Y N^(|Phi|-i). The CTS appendant list is the |Phi| encoded rules
followed by (s-1)|Phi| empty appendants; the CTS tape is the encoded TS
tape. One TS step corresponds to one CTS cycle (s|Phi| CTS steps).
"""

from collections import deque

# Cook's glider construction needs every appendant length to be a
# multiple of 6 (see encoder.py); unary encoding gives appendant lengths
# that are multiples of |Phi|, hence the padding.
CTS_LENGTH_UNIT = 6


def run(rules, tape, s, max_steps):
    """Run a tag system. Yields (step, tape) before each step, where tape
    is the live deque (copy it if you keep it). Stops after the halt
    condition or max_steps steps."""
    tape = deque(tape)
    for n in range(max_steps):
        yield n, tape
        if len(tape) < s:
            return
        head = tape[0]
        for _ in range(s):
            tape.popleft()
        app = rules[head]
        if app is None:
            raise RuntimeError(f"read a never-read symbol {head!r}")
        tape.extend(app)
    yield max_steps, tape


def ts_to_cts(rules, tape, s, order=None):
    """-> (cts_tape, cts_appendants, order). order: alphabet ordering
    (default: sorted); it is returned padded with the dummy symbols.
    Rules mapped to None become empty appendants: such symbols are never
    read, so their appendant content is irrelevant."""
    if order is None:
        order = sorted(rules)
    if set(order) != set(rules):
        raise ValueError("order must list exactly the rule symbols")
    order = list(order)
    rules = dict(rules)
    i = 0
    while len(order) % CTS_LENGTH_UNIT:
        dummy = f"dummy{i}"
        rules[dummy] = ""
        order.append(dummy)
        i += 1
    n = len(order)
    idx = {sym: k for k, sym in enumerate(order)}

    def enc(sym):
        k = idx[sym]
        return "N" * k + "Y" + "N" * (n - k - 1)

    apps = ["".join(enc(sym) for sym in (rules[o] or ())) for o in order]
    apps += [""] * ((s - 1) * n)
    cts_tape = "".join(enc(sym) for sym in tape)
    return cts_tape, apps, order


def decode_cts_tape(cts_tape, order):
    """Inverse of the unary encoding: CTS tape -> list of TS symbols, or
    None if the tape is not currently a whole number of code words (i.e.
    the CTS is mid-cycle)."""
    n = len(order)
    if len(cts_tape) % n:
        return None
    out = []
    for i in range(0, len(cts_tape), n):
        word = cts_tape[i:i + n]
        if word.count("Y") != 1:
            return None
        out.append(order[word.index("Y")])
    return out
