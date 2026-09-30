"""Layer 2: two-way TM -> clockwise TM (multi-symbol, then binary).

The clockwise machine holds the two-way tape as a circular word with the
head as a marked cell and one boundary cell E separating the tape's right
end from its left end. It runs a one-cell delay line: each step consumes
the front cell and appends the previously buffered cell, so a full
rotation shifts nothing -- except at the marked cell, where the two-way
transition is applied locally:

  right move: append buffer, buffer := written symbol, and mark the next
              cell when it passes through the buffer;
  left move:  append MARKED buffer (the left neighbor becomes the head),
              buffer := written symbol.

Growth: when the head mark would cross E, a fresh blank cell is inserted
using the clockwise model's two-symbol write.

Binarization: cells are encoded in fixed-width binary over {A, B}; the
binary machine buffers w bits of input in its state and emits the coded
output cells bit by bit (two-bit writes carry insertions).

Both stages are built by BFS over reachable states; the two-way reference
is tm.TM. Machines must use symbol 1 as the blank background on both
sides (left_bg = right_bg = [1]).

CWTM is the reference interpreter for the binary clockwise model, the
input format of nw.py.
"""

from collections import deque

E = "E"


class CWTM:
    """Binary clockwise Turing machine: circular tape over {'A', 'B'}; each
    step reads the symbol at the head (tape front), removes it, appends the
    1 or 2 written symbols at the tape end, and changes state.
    delta: (state, sym) -> (writes tuple, newstate); a missing key halts."""

    def __init__(self, delta):
        self.delta = delta

    def run(self, state, tape, max_steps):
        """tape: sequence with the head at index 0. Yields (state, tape
        tuple) before each step; stops on halt or after max_steps."""
        tape = list(tape)
        for _ in range(max_steps):
            yield state, tuple(tape)
            key = (state, tape[0])
            if key not in self.delta:
                return
            writes, state = self.delta[key]
            tape = tape[1:] + list(writes)


def cell(v):
    return ("c", v)


def mark(v):
    return ("m", v)


def two_way_to_cw(tm2, q0, left, cur, right):
    """-> (delta, word, state0): a symbolic clockwise machine.
    delta: (state, sym) -> (writes tuple, newstate); missing = halt.
    Tape must sit on blank (symbol 1) backgrounds."""
    word = [mark(cur)] + [cell(v) for v in right] + [E] + \
           [cell(v) for v in left[::-1]]
    b0 = word.pop()                  # predecessor of the head (E if no left)
    state0 = (q0, b0, False)         # (2way state, buffer, mark_next flag)
    delta = {}
    frontier = [state0]
    seen = {state0}
    syms = [cell(v) for v in range(1, tm2.t + 1)] + \
           [mark(v) for v in range(1, tm2.t + 1)] + [E]
    while frontier:
        st = frontier.pop()
        q, b, mn = st
        for sym in syms:
            out = _step(tm2, q, b, mn, sym)
            if out is None:
                continue                      # halt: no transition
            writes, nst = out
            delta[(st, sym)] = (writes, nst)
            if nst not in seen:
                seen.add(nst)
                frontier.append(nst)
    return delta, word, state0


def _step(tm2, q, b, mn, sym):
    """One delay-line step; returns (writes, newstate) or None for halt."""
    kind = "E" if sym == E else sym[0]
    if kind == "m":
        v = sym[1]
        key = (q, v)
        if key not in tm2.write:
            return None                       # halting pair
        u = tm2.write[key]
        mv = tm2.move[key]
        q2 = tm2.nxt[key]
        if mv == "H":
            return None
        if mv == "R":
            # b == E simply means the head is at the leftmost cell; the
            # move is interior either way. Right-end growth is handled
            # when the mark-next flag reaches E below.
            return ((b,), (q2, cell(u), True))
        else:                                 # L
            if b == E:
                # head moving left at the left end: fresh blank cell
                return ((E, mark(1)), (q2, cell(u), False))
            return ((mark(b[1]),), (q2, cell(u), False))
    # unmarked cell or E passing through the delay line
    if mn is True and kind != "E":
        # mark this cell as the new head when it leaves the buffer
        return ((b,), (q, mark(sym[1]), False))
    if mn is True and kind == "E":
        # the head mark must land on a fresh blank inserted before E
        return ((b, mark(1)), (q, E, False))
    return ((b,), (q, sym, False))


def run_cw(delta, word, state, max_steps):
    """Run a symbolic clockwise machine. Yields (n, word, state) before each
    step, word being the live deque; stops on halt."""
    w = deque(word)
    for n in range(max_steps):
        yield n, w, state
        sym = w.popleft()
        key = (state, sym)
        if key not in delta:
            return
        writes, state = delta[key]
        w.extend(writes)


def decode_cw(word, state):
    """-> (q, cur, right, left) when the front is the marked head cell.
    The buffer holds the head's predecessor and is appended at the end of
    the circular order for decoding."""
    q, b, mn = state
    if mn:
        return None
    w = list(word)
    if not w or w[0] == E or w[0][0] != "m":
        return None
    w = w + [b]
    cur = w[0][1]
    try:
        ei = w.index(E)
    except ValueError:
        return None
    right = [c[1] for c in w[1:ei]]
    left = [c[1] for c in w[ei + 1:]][::-1]
    return q, cur, right, left


def binarize(delta, word, state0):
    """Symbolic clockwise machine -> binary (A/B) clockwise machine.

    Each symbolic cell is a fixed-width binary code. The binary machine
    reads one bit per step into an input buffer and writes bits of the
    previous symbols' codes from an output queue (2-bit writes drain the
    surplus that insertions create; the queue is preloaded with the last
    cell's code so a write is always available).

    Returns (bdelta, bword, bstate0, width): bdelta in CWTM form over
    'A'/'B', the initial binary tape, the initial state, and the code width.
    """
    syms = sorted({s for (_, s) in delta} |
                  {w for (ws, _) in delta.values() for w in ws} | {E},
                  key=repr)
    w = max(1, (len(syms) - 1).bit_length())
    code = {s: tuple("AB"[(i >> k) & 1] for k in range(w))
            for i, s in enumerate(syms)}

    bword = [b for s in word for b in code[s]]
    outq0 = tuple(bword[-w:])
    bword = bword[:-w]
    bstate0 = (state0, (), outq0)

    bdelta = {}
    frontier = [bstate0]
    seen = {bstate0}
    dec = {v: k for k, v in code.items()}
    while frontier:
        st = frontier.pop()
        sym_state, inbuf, outq = st
        for bit in "AB":
            ib = inbuf + (bit,)
            oq = outq
            if len(ib) == w:
                s = dec.get(ib)
                if s is None:
                    continue          # code of no symbol: never on the tape
                key = (sym_state, s)
                if key not in delta:
                    continue          # halt
                writes, sym_state2 = delta[key]
                for x in writes:
                    oq = oq + code[x]
                ib = ()
            else:
                sym_state2 = sym_state
            if not oq:
                raise AssertionError("output queue underflow")
            nout = 2 if len(oq) > w and len(oq) >= 2 else 1
            emit, oq2 = oq[:nout], oq[nout:]
            nst = (sym_state2, ib, oq2)
            bdelta[(st, bit)] = (emit, nst)
            if nst not in seen:
                seen.add(nst)
                frontier.append(nst)
    return bdelta, bword, bstate0, w


# ---------------------------------------------------------------------------
# Direct binary construction (v0.1.1)
#
# binarize() above carries the symbolic machine's state (which holds the
# buffered cell) AND the code of the previously buffered cell being
# emitted: a product of two cells, ~22M states for the SKI machine. The
# construction below keeps the one-cell delay as raw bits instead: the
# state holds a pending-output queue whose length plus the bits read of
# the current cell is w+1 in steady state, so at most one cell's worth of
# bits is ever buffered.
#
# Binary cell format: w data bits (symbol v in 1..t -> v-1, the boundary
# E -> t; bit 0 first, 'A' = 0, 'B' = 1) followed by a mark bit ('B' on
# the head cell). The mark comes last so that, when the head cell has been
# read completely, the previous cell's mark bit has not yet been emitted
# and a left move can still set it.

def _bits(value, w):
    return tuple("AB"[(value >> k) & 1] for k in range(w))


def two_way_to_binary_cw(tm2, q0, left, cur, right):
    """Two-way TM (blank 1 on both sides) -> binary clockwise TM directly.

    Returns (bdelta, bword, bstate0, w) in the same form as binarize():
    bdelta: (state, bit) -> (emitted bits, newstate), missing = halt.
    decode_binary_cw() recovers two-way configurations from a run.
    """
    t = tm2.t
    w = max(1, t.bit_length())          # t + 1 codes: symbols and E
    code = {v: _bits(v - 1, w) for v in range(1, t + 1)}
    code[E] = _bits(t, w)
    dec = {c: v for v, c in code.items()}

    def cellbits(v, marked):
        return code[v] + ("B" if marked else "A",)

    word = [(cur, True)] + [(v, False) for v in right] + [(E, False)] + \
           [(v, False) for v in left[::-1]]
    b0, m0 = word.pop()                 # the head's predecessor
    bword = [b for v, m in word for b in cellbits(v, m)]
    # state: (q, mark_next, prev_is_E, pending bits, bits of current cell)
    st0 = (q0, False, b0 == E, cellbits(b0, m0), ())

    def step(st, x):
        q, mark_next, prev_is_E, pend, cb = st
        cb = cb + (x,)
        if len(cb) == w + 1:            # current cell complete
            v = dec.get(cb[:w])
            if v is None:
                return None             # not a code: never on the tape
            head = cb[w] == "B"
            if head:
                key = (q, v)
                if v == E or key not in tm2.write or tm2.move[key] == "H":
                    return None         # halt
                u, mv, q2 = tm2.write[key], tm2.move[key], tm2.nxt[key]
                if mv == "R":
                    pend = pend + cellbits(u, False)
                    mark_next = True
                elif prev_is_E:
                    # left move off the left end: fresh blank head cell
                    # between E and the old head
                    pend = pend + cellbits(1, True) + cellbits(u, False)
                    mark_next = False
                else:
                    pend = pend[:-1] + ("B",) + cellbits(u, False)
                    mark_next = False
                q, prev_is_E = q2, False
            elif mark_next:
                if v == E:
                    # right move onto the boundary: fresh blank head cell
                    # before E
                    pend = pend + cellbits(1, True) + cellbits(E, False)
                    prev_is_E = True
                else:
                    pend = pend + cellbits(v, True)
                    prev_is_E = False
                mark_next = False
            else:
                pend = pend + cb
                prev_is_E = v == E
            cb = ()
        # emit 2 bits while an insertion's surplus drains, else 1
        nout = 2 if len(pend) + len(cb) > w + 2 else 1
        return pend[:nout], (q, mark_next, prev_is_E, pend[nout:], cb)

    bdelta = {}
    frontier, seen = [st0], {st0}
    while frontier:
        st = frontier.pop()
        for x in "AB":
            out = step(st, x)
            if out is None:
                continue
            bdelta[(st, x)] = out
            if out[1] not in seen:
                seen.add(out[1])
                frontier.append(out[1])
    return bdelta, bword, st0, w


def decode_binary_cw(bword, state, w, t):
    """-> (q, cur, right, left) at a cell boundary with the head marked
    and no move in flight, else None."""
    q, mark_next, _, pend, cb = state
    if cb or mark_next:
        return None
    bits = list(bword) + list(pend)
    if len(bits) % (w + 1):
        return None
    cells = []
    for i in range(0, len(bits), w + 1):
        c = bits[i:i + w + 1]
        v = sum(1 << k for k in range(w) if c[k] == "B")
        cells.append((E if v == t else v + 1, c[w] == "B"))
    heads = [i for i, (_, m) in enumerate(cells) if m]
    if len(heads) != 1:
        return None
    h = heads[0]
    cells = cells[h:] + cells[:h]
    vals = [v for v, _ in cells]
    ei = vals.index(E)
    return q, vals[0], vals[1:ei], vals[ei + 1:][::-1]
