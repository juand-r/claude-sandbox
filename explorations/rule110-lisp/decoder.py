"""Layer 1 (part): find moving-data symbols in an evolved Rule 110 row.

Moving data N and Y are Cook's blocks E and F. Between collisions a
moving-data symbol's row content is exactly the block's row at one of its
30 vertical phases, so we scan the row for each phase's "core" -- the
block row stripped of leading/trailing ether but keeping interior ether
gaps. Matches ordered by position spell the moving data in flight.

Limits (see REVIEW.md B3): this sees only *moving* data, not the
stationary tape data that the machinery actually reads, and freshly
appended symbols can alias the other symbol before they settle. It is a
diagnostic, not a verified tape reader.
"""

from encoder import BAND_START, load_blocks

# D..L blocks repeat every 30 rows; one period of rows gives every phase.
PHASES = 30
# Every E/F row core is well over this long; a shorter one means the
# ether stripping went wrong, so fail loudly.
MIN_CORE = 60
# Consecutive moving-data symbols start >= 260 cells apart (block widths
# 310-340 minus up to ~80 cells of phase-dependent core offset), while the
# partial-core aliases seen inside a single block sit <= 226 apart.
MIN_PITCH = 245


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
            for r in range(BAND_START[PHASES], BAND_START[PHASES] + PHASES):
                bits = blk.bits(r)
                core, lead = _strip_ether(bits)
                if len(core) < MIN_CORE:
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
        for (a1, b1, s1), (a2, b2, s2) in zip(accepted, accepted[1:]):
            if a2 - a1 < MIN_PITCH:
                raise ValueError(f"implausible symbol pitch at {a1},{a2}")
        return [(a, sym) for a, b, sym in accepted]
