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
    """-> (core, lead): bits with maximal pure-ether prefix/suffix removed
    (interior gaps kept), and the number of leading cells stripped."""
    n = len(bits)
    def periodic_prefix_len(s):
        k = 0
        while k + 14 < len(s) and s[k] == s[k + 14]:
            k += 1
        return k
    a = periodic_prefix_len(bits)
    b = periodic_prefix_len(bits[::-1])
    return bits[a:n - b], a


class Decoder:
    def __init__(self):
        blocks, _ = load_blocks()
        self.sigs = []
        seen = set()
        for sym, name in (("N", "E"), ("Y", "F")):
            blk = blocks[name]
            for r in range(35, 65):
                bits = blk.bits(r)
                core, lead = _strip_ether(bits)
                if len(core) < 60:
                    raise AssertionError(f"suspiciously short core {name}@{r}")
                if core in seen:
                    continue
                seen.add(core)
                # (symbol, core, lead offset, full block-row width): on a
                # match at p the whole block occupies [p-lead, p-lead+width)
                self.sigs.append((sym, core, lead, len(bits)))

    def read(self, row):
        """row: uint8 array -> list of (position, 'Y'|'N') sorted by position.

        A short core (a phase where a leading glider merged into the seam)
        can also occur as a substring inside a full block at another offset,
        so hits are resolved longest-first with span-overlap rejection.
        """
        s = row.tobytes().translate(bytes.maketrans(b"\x00\x01", b"01")).decode()
        hits = []
        for sym, sig, lead, width in self.sigs:
            start = 0
            while True:
                i = s.find(sig, start)
                if i < 0:
                    break
                # blocked extent covers the whole block, so an alias match
                # of a partial core inside another block is rejected
                hits.append((i, len(sig), i - lead, i - lead + width, sym))
                start = i + 1
        accepted = []
        for p, ln, a, b, sym in sorted(hits, key=lambda h: -h[1]):
            if any(a < b2 and a2 < b for _, _, a2, b2, _ in accepted):
                continue
            accepted.append((p, ln, a, b, sym))
        accepted = sorted((p, p + ln, sym) for p, ln, a, b, sym in accepted)
        # Adjacent symbols sit ~340+ cells apart, but core start offsets
        # vary with phase by up to ~80 cells, so true gaps reach down to
        # ~260. Known aliases (partial cores inside a block) sit at <= 226.
        for (a1, b1, s1), (a2, b2, s2) in zip(accepted, accepted[1:]):
            if a2 - a1 < 245:
                raise ValueError(f"implausible symbol pitch at {a1},{a2}")
        return [(a, sym) for a, b, sym in accepted]
