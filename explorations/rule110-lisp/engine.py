"""Layer 0: Rule 110 simulator.

Cells are numpy uint8 arrays of 0/1. The boundary is cyclic, so a tape of
width W behaves like an infinite tape of period W. For glider work the width
must be a multiple of 14 (the ether's spatial period) so the background
tiles seamlessly across the wrap.

Rule 110 truth table (neighborhood left,center,right -> new center):
    111->0  110->1  101->1  100->0  011->1  010->1  001->1  000->0
i.e. new = (center OR right) AND NOT (left AND center AND right).
"""

import numpy as np

RULE = 110
# TABLE[n] = output bit for neighborhood value n = 4*left + 2*center + right
TABLE = np.array([(RULE >> n) & 1 for n in range(8)], dtype=np.uint8)

# One spatial period of the ether (the regular background lattice of
# Rule 110), spatial period 14, temporal period 7. Verified empirically in
# tests/test_engine.py, which also measures its horizontal drift per period.
ETHER = "11111000100110"


def parse(s):
    """'0110...' or ' XX .'-style string -> uint8 array. '1'/'X' are alive."""
    return np.array([1 if c in "1X" else 0 for c in s], dtype=np.uint8)


def show(cells):
    """uint8 array -> string, alive cells as 'X'."""
    return "".join("X" if c else "." for c in cells)


def step(cells):
    """One synchronous Rule 110 update with cyclic boundary."""
    left = np.roll(cells, 1)
    right = np.roll(cells, -1)
    return TABLE[(left << 2) | (cells << 1) | right]


def run(cells, n):
    """Evolve n steps, return final row."""
    for _ in range(n):
        cells = step(cells)
    return cells


def history(cells, n):
    """Evolve n steps, return (n+1, width) array of all rows incl. initial."""
    out = np.empty((n + 1, len(cells)), dtype=np.uint8)
    out[0] = cells
    for t in range(n):
        out[t + 1] = step(out[t])
    return out


def ether_tape(width):
    """A pure-ether tape of the given width (must be a multiple of 14)."""
    if width % len(ETHER) != 0:
        raise ValueError(f"width {width} not a multiple of {len(ETHER)}")
    return np.tile(parse(ETHER), width // len(ETHER))


def save_png(hist, path, scale=1):
    """Save a spacetime diagram (rows = time, downward) as a PNG."""
    from PIL import Image
    img = Image.fromarray((1 - hist) * np.uint8(255), mode="L")
    if scale != 1:
        img = img.resize((img.width * scale, img.height * scale),
                         Image.NEAREST)
    img.save(path)
