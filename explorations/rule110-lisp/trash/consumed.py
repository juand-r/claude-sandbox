"""Extract the consumed-symbol sequence from a positions log.

The front tape symbol drifts left at -8/30 cells/step between ossifier
hits; when an ossifier consumes it, the leftmost decoded position jumps
right by roughly one symbol pitch (>300 cells). The symbol consumed is the
last clean read of the front before the jump.

A CTS computation is fully determined by its sequence of consumed symbols,
so this is the ground truth we validate against the reference interpreter.
Full-tape decoded strings are only diagnostic: maturing appended symbols
pass through spacings that alias other symbols (see NOTES.md).
"""


def consumed_sequence(log_path, start_front):
    """-> list of (t, symbol) consumption events.

    start_front: front position at t=0 (from the t=0 read). The front is
    tracked by co-moving continuity: among the row's reads, the one nearest
    the predicted position. Reads far to the left are consumption debris
    aliasing a core; reads far right are tape interior. A forward jump of
    roughly one symbol pitch is a consumption event.
    """
    events = []
    prev_t, prev_front, prev_sym = 0, start_front, None
    for line in open(log_path):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3 or parts[1] in ("", "?") or not parts[2]:
            continue
        t = int(parts[0])
        expect = prev_front - 8 * (t - prev_t) / 30
        cands = [(int(p), s) for p, s in
                 zip(parts[2].split(), parts[1])
                 if -250 < int(p) - expect < 800]
        if not cands:
            continue
        front, sym = min(cands, key=lambda c: abs(c[0] - expect))
        if prev_sym is not None and front - expect > 250:
            events.append((prev_t, prev_sym))
        prev_t, prev_front, prev_sym = t, front, sym
    return events
