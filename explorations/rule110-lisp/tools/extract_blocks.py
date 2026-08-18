"""Extract Cook's 12 bit-blocks from the arXiv source of:

    M. Cook, "A Concrete View of Rule 110 Computation", EPTCS 1 (2009),
    arXiv:0906.3248.

The paper's figures figBitBlocks{1..9,A,B,C} are Mathematica grayscale
rasters, one pixel per CA cell: 0x00 = alive, 0xFF = dead, 0x80 = outside
the block's zig-zag boundary, 0xB3 = the marked t=0 row (block C only,
flanking the row's content).

Writes data/blocks.json:
    {"blocks": {"A": ["  10110...", ...], ...},   # ' '=outside, chars 0/1
     "t0_row": {"C": 51}}

Usage: python tools/extract_blocks.py <dir-with-eps-files>
(Fetch the sources with:
    curl -L -o cook2009.tar.gz https://arxiv.org/e-print/0906.3248
    mkdir cook2009 && tar xzf cook2009.tar.gz -C cook2009)
"""

import json
import os
import re
import sys

# figure file suffix -> block name, in the paper's order A..L
FIGS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C"]
NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
SYM = {0x00: "1", 0xFF: "0", 0x80: " "}


def extract(eps_path):
    """-> (rows, t0_row or None); rows are strings of '0'/'1'/' '."""
    src = open(eps_path).read()
    m = re.search(r"(\d+) string\s+(\d+) (\d+) 8 ", src)
    if not m:
        raise ValueError(f"no raster found in {eps_path}")
    w, h = int(m.group(2)), int(m.group(3))
    tail = src[src.index("}  Mimage"):]
    hexdata = "".join(re.findall(r"^([0-9A-Fa-f]+)$", tail, re.M))
    vals = bytes.fromhex(hexdata)
    if len(vals) < w * h:
        raise ValueError(f"raster truncated in {eps_path}")
    rows, t0 = [], None
    for r in range(h):
        raw = vals[r * w:(r + 1) * w]
        if 0xB3 in raw:
            if t0 is not None:
                raise ValueError(f"two marker rows in {eps_path}")
            t0 = r
            raw = bytes(0x80 if b == 0xB3 else b for b in raw)
        rows.append("".join(SYM[b] for b in raw))
    # The EPS prolog applies "1 -1 scale": raster storage order is
    # bottom-to-top of the displayed figure. Reverse so that increasing row
    # index = increasing time (verified by single-stepping Rule 110 on
    # patch rows in tests/test_encoder.py).
    rows.reverse()
    if t0 is not None:
        t0 = h - 1 - t0
    return rows, t0


def main(eps_dir):
    blocks, t0_rows = {}, {}
    for fig, name in zip(FIGS, NAMES):
        rows, t0 = extract(os.path.join(eps_dir, f"figBitBlocks{fig}.eps"))
        blocks[name] = rows
        if t0 is not None:
            t0_rows[name] = t0
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "data", "blocks.json")
    with open(out, "w") as f:
        json.dump({"blocks": blocks, "t0_row": t0_rows}, f)
    print(f"wrote {out}: " +
          ", ".join(f"{n}({len(b[0])}x{len(b)})" for n, b in blocks.items()) +
          f", t0_row={t0_rows}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
