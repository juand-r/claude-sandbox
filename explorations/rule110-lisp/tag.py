"""Layer 2: tag systems and the tag-system -> cyclic-tag-system compiler.

A tag system here has deletion number s: each step removes s symbols from
the front of the tape and appends the appendant of the FIRST removed
symbol. It halts when the tape has fewer than s symbols or when a rule
with an empty right-hand side marked terminal fires... (we follow Cook
2009: halting rules simply have empty appendants; the system halts when
the tape empties or len(tape) < s).

The TS -> CTS conversion (Cook 2009): order the alphabet, pad with dummy
empty rules until |Phi| is a multiple of 6, unary-encode symbol phi_i as
N^(i-1) Y N^(|Phi|-i). The CTS appendant list is the |Phi| encoded rules
followed by (s-1)|Phi| empty appendants; the CTS tape is the encoded TS
tape. One TS step corresponds to one CTS cycle (s|Phi| CTS steps).
"""


def ts_run(rules, tape, s, max_steps):
    """rules: dict symbol -> appendant string (symbols are single chars).
    Yields (step, tape) before each step; stops on halt."""
    tape = list(tape)
    for n in range(max_steps):
        yield n, "".join(tape)
        if len(tape) < s:
            return
        head = tape[0]
        del tape[:s]
        tape.extend(rules[head])
    yield max_steps, "".join(tape)


def ts_to_cts(rules, tape, s, order=None):
    """-> (cts_tape, cts_appendants, order). order: alphabet ordering."""
    if order is None:
        order = sorted(rules)
    if set(order) != set(rules):
        raise ValueError("order must list exactly the rule symbols")
    # pad alphabet to a multiple of 6 with dummy empty-appendant symbols
    order = list(order)
    i = 0
    while len(order) % 6:
        dummy = f"dummy{i}"
        rules = {**rules, dummy: ""}
        order.append(dummy)
        i += 1
    n = len(order)
    idx = {sym: k for k, sym in enumerate(order)}

    def enc(sym):
        k = idx[sym]
        return "N" * k + "Y" + "N" * (n - k - 1)

    apps = ["".join(enc(sym) for sym in rules[o]) for o in order]
    apps += [""] * ((s - 1) * n)
    cts_tape = "".join(enc(sym) for sym in tape)
    return cts_tape, apps, order
