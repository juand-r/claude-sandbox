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
"""

from tm import TM

E = "E"


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
    """Yields (n, word, state); stops on halt."""
    from collections import deque
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


def binarize(delta, word, state0, t):
    """Symbolic clockwise machine -> binary (A/B) clockwise machine.

    Each symbolic cell is a fixed-width binary code. The binary machine
    reads one bit per step into an input buffer and writes bits of the
    previous symbols' codes from an output queue (2-bit writes drain the
    surplus that insertions create; the queue is preloaded with the last
    cell's code so a write is always available).

    Returns (bdelta, bword, bstate0) with bdelta in CWTM form over 'A'/'B'.
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
                    continue          # unused code: unreachable in practice
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
