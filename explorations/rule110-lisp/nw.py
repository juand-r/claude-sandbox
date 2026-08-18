"""Layer 2: Neary-Woods-style polynomial simulation -- a 2-deletion tag
system emulating a clockwise binary Turing machine (Cook 2009, section
"A Polynomial Time Simulation"; original method Neary & Woods 2006).

Clockwise binary TM: circular tape over {A, B}; each step reads the symbol
at the head, replaces it with 1 or 2 written symbols appended at the tape
end, and the head advances to the next symbol. delta: (state, sym) ->
(writes, newstate), writes a tuple of 1 or 2 symbols; missing entry halts.

Tag symbols are tuples (letter, stage, tmstate); '-' and '0' are
unsubscripted ('-' is never read, '0' has an empty appendant). Stages 1-6
as in the paper; each stage's transfer table is one function over that
stage's alphabet (capitals and lowercase are distinct rows). Stage 6
performs the TM step: the P/Q appendant emits the written symbols with
stage-6 subscripts (so they are processed at the end of the pass and land
at the tape end in stage 3) followed by the new head marker in stage 3.
The counter (U/V/X/Y) doubles via the [U] option exactly when the fired
transition writes two symbols.
"""

DASH, ZERO = "-", "0"


class CWTM:
    def __init__(self, delta):
        self.delta = delta   # (state, 'A'|'B') -> (writes tuple, newstate)

    def run(self, state, tape, max_steps):
        """tape: list of 'A'/'B' with the head at index 0. Yields
        (state, tape tuple) before each step."""
        tape = list(tape)
        for _ in range(max_steps):
            yield state, tuple(tape)
            key = (state, tape[0])
            if key not in self.delta:
                return
            writes, state = self.delta[key]
            tape = tape[1:] + list(writes)


def sym(letter, stage, q):
    if letter in (DASH, ZERO):
        return letter
    return (letter, stage, q)


def build_rules(tm, states):
    """-> dict tag-symbol -> appendant list."""
    R = {DASH: None, ZERO: []}   # '-' must never be read

    for q in states:
        def s(letter, stage, q=q):
            return sym(letter, stage, q)

        # stage 2 -> 3
        R[s("H", 2)] = [s("H", 3), DASH]
        R[s("h", 2)] = [DASH, s("H", 3), DASH]
        for c in "ABCD":
            R[s(c, 2)] = [s(c, 3), s(c, 3)]
        R[s("U", 2)] = [s("U", 3)]
        R[s("u", 2)] = [s("V", 3)]
        R[s("X", 2)] = [s("X", 3), s("X", 3)]
        R[s("x", 2)] = [s("Y", 3), s("Y", 3)]
        R[s("V", 2)] = [s("V", 3)]
        R[s("Y", 2)] = [s("Y", 3), s("Y", 3)]

        # stage 3 -> 4
        R[s("H", 3)] = [s("H", 4), s("h", 4)]
        for c in "ABCD":
            R[s(c, 3)] = [s(c, 4), s(c.lower(), 4)]
        R[s("U", 3)] = [s("U", 4), s("u", 4), s("X", 4), s("x", 4)]
        R[s("V", 3)] = [s("V", 4), s("v", 4), s("Y", 4), s("y", 4)]
        R[s("X", 3)] = [s("X", 4), s("x", 4)]
        R[s("Y", 3)] = [s("Y", 4), s("y", 4)]

        # stage 4 -> 1 (capitals) and -> 5 (lowercase)
        R[s("H", 4)] = [s("H", 1), DASH]
        R[s("A", 4)] = [s("A", 1), s("a", 1), ZERO]
        R[s("B", 4)] = [s("B", 1), s("b", 1), ZERO]
        R[s("C", 4)] = [s("C", 1), s("C", 1)]
        R[s("D", 4)] = [s("D", 1), s("D", 1)]
        R[s("U", 4)] = [s("U", 1), s("U", 1)]
        R[s("V", 4)] = [s("V", 1), s("V", 1)]
        R[s("X", 4)] = [s("X", 1), s("X", 1)]
        R[s("Y", 4)] = [s("Y", 1), s("Y", 1)]
        R[s("h", 4)] = []
        R[s("a", 4)] = [DASH, s("P", 5), DASH]
        R[s("b", 4)] = [DASH, s("Q", 5), DASH]
        R[s("c", 4)] = [s("A", 5), DASH]
        R[s("d", 4)] = [s("B", 5), DASH]
        R[s("u", 4)] = []
        R[s("v", 4)] = []
        R[s("x", 4)] = [s("U", 5), s("x", 4)]   # mixed-stage row
        R[s("y", 4)] = [s("V", 5), s("y", 4)]

        # stage 1 -> 2
        R[s("H", 1)] = [s("H", 2), s("h", 2)]
        R[s("A", 1)] = [s("A", 2), s("A", 2)]
        R[s("a", 1)] = [s("C", 2), s("C", 2)]
        R[s("B", 1)] = [s("B", 2), s("B", 2)]
        R[s("b", 1)] = [s("D", 2), s("D", 2)]
        R[s("C", 1)] = [s("C", 2), s("C", 2)]
        R[s("D", 1)] = [s("D", 2), s("D", 2)]
        R[s("U", 1)] = [s("U", 2), s("u", 2)]
        R[s("V", 1)] = [s("V", 2), s("V", 2)]
        R[s("X", 1)] = [s("X", 2), s("x", 2)]
        R[s("Y", 1)] = [s("Y", 2), s("Y", 2)]

        # stage 5 -> 6
        R[s("P", 5)] = [s("P", 6), DASH]
        R[s("Q", 5)] = [s("Q", 6)]
        R[s("A", 5)] = [s("A", 6), s("a", 6)]
        R[s("B", 5)] = [s("B", 6), s("b", 6)]
        R[s("U", 5)] = [s("U", 6), s("u", 6)]
        R[s("V", 5)] = [s("V", 6), s("v", 6)]

        # stage 6 -> 3 (the TM step)
        def step_app(read):
            key = (q, read)
            if key not in tm.delta:
                return []            # halt: emit nothing
            writes, q2 = tm.delta[key]
            out = []
            for w in writes:
                out += [sym(w, 6, q), sym(w.lower(), 6, q)]
            head = [sym("H", 3, q2), DASH]
            if read == "B":
                head = [DASH] + head
            return out + head
        R[s("P", 6)] = step_app("A")
        R[s("Q", 6)] = step_app("B")
        for letter, read in (("A", "A"), ("a", "B"), ("B", "A"), ("b", "B")):
            key = (q, read)
            if key in tm.delta:
                _, q2 = tm.delta[key]
                base = letter.upper()
                R[s(letter, 6)] = [sym(base, 3, q2), sym(base, 3, q2)]
            else:
                R[s(letter, 6)] = []
        for letter, read in (("U", "A"), ("u", "B")):
            key = (q, read)
            if key in tm.delta:
                writes, q2 = tm.delta[key]
                app = [sym("U", 3, q2)]
                if len(writes) == 2:
                    app.append(sym("U", 3, q2))
                R[s(letter, 6)] = app
            else:
                R[s(letter, 6)] = []
        for letter, read in (("V", "A"), ("v", "B")):
            key = (q, read)
            if key in tm.delta:
                _, q2 = tm.delta[key]
                R[s(letter, 6)] = [sym("U", 3, q2)]
            else:
                R[s(letter, 6)] = []
    return R


def initial_tape(state, tm_tape, counter):
    """Stage-2 tape: H h, counter Uu pairs, then doubled tape symbols."""
    out = [sym("H", 2, state), sym("h", 2, state)]
    for _ in range(counter):
        out += [sym("U", 2, state), sym("u", 2, state)]
    for c in tm_tape:
        out += [sym(c, 2, state), sym(c, 2, state)]
    return out


def tag_run(rules, tape, max_steps):
    """2-deletion tag run; yields (n, tape list) before each step."""
    from collections import deque
    tape = deque(tape)
    for n in range(max_steps):
        yield n, tape
        if len(tape) < 2:
            return
        head = tape.popleft()
        tape.popleft()
        app = rules[head]
        if app is None:
            raise RuntimeError("read a '-' symbol: parity broken")
        tape.extend(app)
    yield max_steps, tape


def decode_stage2(tape):
    """If the front is H@2, decode (tmstate, tape letters); else None.
    C/D count as A/B; counter and padding symbols are dropped."""
    if not tape:
        return None
    front = tape[0]
    if front in (DASH, ZERO) or front[0] != "H" or front[1] != 2:
        return None
    q = front[2]
    letters = []
    for t in list(tape)[2:]:
        if t in (DASH, ZERO):
            continue
        letter = t[0]
        if letter in "AB":
            letters.append(letter)
        elif letter in "CD":
            letters.append("A" if letter == "C" else "B")
        # skip counter (U/u/V/v/X/x/Y/y) and any h
    # letters are doubled pairs; halve them
    if len(letters) % 2:
        return None
    return q, tuple(letters[0::2])
