"""Layer 1 (part): read a cyclic tag system tape off an evolved Rule 110 row.

Moving data N and Y are Cook's blocks E and F: three small gliders whose
spacings encode the symbol. Between collisions a tape symbol's row content
is exactly the block's row at one of its 30 vertical phases, so we scan the
row for each phase's "core" -- the block row stripped of leading/trailing
ether but keeping interior ether gaps (content plus spacing, position-free).
Matches ordered by position spell the tape.
"""

from encoder import load_blocks

# ether-tile rotations, used to strip a core's leading/trailing background
_ETHER = "11111000100110"


def _strip_ether(bits):
    """Remove maximal pure-ether prefix/suffix, keep interior gaps."""
    n = len(bits)
    start, end = 0, n
    # grow the largest prefix that is ether-periodic (period 14)
    p = 0
    while p + 14 <= n and bits[p] == bits[p + 14 % n] and False:
        p += 1
    # simpler: find first/last position where the 14-periodicity breaks
    def periodic_prefix_len(s):
        k = 0
        while k + 14 < len(s) and s[k] == s[k + 14]:
            k += 1
        return k
    a = periodic_prefix_len(bits)
    b = periodic_prefix_len(bits[::-1])
    return bits[a:n - b]


class Decoder:
    def __init__(self):
        blocks, _ = load_blocks()
        self.sigs = []
        seen = set()
        for sym, name in (("N", "E"), ("Y", "F")):
            blk = blocks[name]
            for r in range(35, 65):
                core = _strip_ether(blk.bits(r))
                if len(core) < 60:
                    raise AssertionError(f"suspiciously short core {name}@{r}")
                if core in seen:
                    continue
                seen.add(core)
                self.sigs.append((sym, core))

    def read(self, row):
        """row: uint8 array -> list of (position, 'Y'|'N') sorted by position.

        A short core (a phase where a leading glider merged into the seam)
        can also occur as a substring inside a full block at another offset,
        so hits are resolved longest-first with span-overlap rejection.
        """
        s = row.tobytes().translate(bytes.maketrans(b"\x00\x01", b"01")).decode()
        hits = []
        for sym, sig in self.sigs:
            start = 0
            while True:
                i = s.find(sig, start)
                if i < 0:
                    break
                hits.append((i, i + len(sig), sym))
                start = i + 1
        accepted = []
        for a, b, sym in sorted(hits, key=lambda h: h[0] - h[1]):
            if any(a < b2 and a2 < b for a2, b2, _ in accepted):
                continue
            accepted.append((a, b, sym))
        accepted.sort()
        # tape symbols are > 300 cells apart; closer reads mean a decode bug
        for (a1, b1, s1), (a2, b2, s2) in zip(accepted, accepted[1:]):
            if a2 - a1 < 300:
                raise ValueError(f"implausible symbol pitch at {a1},{a2}")
        return [(a, sym) for a, b, sym in accepted]
