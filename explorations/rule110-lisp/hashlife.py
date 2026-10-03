"""1-D HashLife for Rule 110 (Gosper's algorithm, one dimension).

A node of level k stands for 2^k consecutive cells. Leaves are level 6:
64 cells held as a Python int (bit i = cell i, left to right). Nodes are
hash-consed, so equal subtrees are one object, and results are memoized:
result(n, j) is the centre half of node n (level k) after 2^j steps,
j <= k - 2. Rule 110 has radius 1, so after s steps a block of 2^k cells
determines exactly its cells [s, 2^k - s), and the centre half is
determined for s <= 2^(k-2).

The universe is a finite row embedded in ether. Ether moves by the
lattice vector (1, -4): row(t+1)[x] = row(t)[x + 4] (checked with
engine.step), so an ether block at any place and time is a phase shift of
the ETHER tile and is itself one hash-consed node per (level, phase).
HashRun keeps a root node, expands it with ether nodes of the right phase
before each advance, and fails loudly if non-ether content reaches the
root's outer quarters.
"""

import numpy as np

from engine import ETHER, pack, step_packed, unpack

LEAF = 6                      # leaf level: 64 cells
LEAF_CELLS = 1 << LEAF
_LEAF_MASK = (1 << LEAF_CELLS) - 1
_HALF_MASK = (1 << (LEAF_CELLS // 2)) - 1
TILE = len(ETHER)
ETHER_SHIFT_PER_STEP = 4      # row(t+1)[x] = row(t)[x + 4]


class Node:
    __slots__ = ("k", "a", "b", "v")


_leaves = {}                  # int -> leaf Node
_nodes = {}                   # (id(a), id(b)) -> Node; nodes are never freed
_results = {}                 # (id(node), j) -> Node
_ether = {}                   # (k, phase) -> Node


def leaf(v):
    n = _leaves.get(v)
    if n is None:
        n = Node()
        n.k, n.a, n.b, n.v = LEAF, None, None, v
        _leaves[v] = n
    return n


def join(a, b):
    key = (id(a), id(b))
    n = _nodes.get(key)
    if n is None:
        n = Node()
        n.k, n.a, n.b, n.v = a.k + 1, a, b, None
        _nodes[key] = n
    return n


def _step_bits(x, nbits, steps):
    """Rule 110 on an nbits-cell int (bit i = cell i), zero outside; only
    cells [steps, nbits - steps) of the result are meaningful."""
    mask = (1 << nbits) - 1
    for _ in range(steps):
        left = (x << 1) & mask        # value of cell i-1, at position i
        right = x >> 1                # value of cell i+1, at position i
        x = (x | right) & ~(left & x & right) & mask
    return x


def center(n):
    """Middle half of n (one level down), at the same time."""
    if n.k == LEAF + 1:
        return leaf((n.a.v >> (LEAF_CELLS // 2)) |
                    ((n.b.v & _HALF_MASK) << (LEAF_CELLS // 2)))
    return join(n.a.b, n.b.a)


def result(n, j):
    """Centre half of n after 2^j steps (j <= n.k - 2)."""
    key = (id(n), j)
    r = _results.get(key)
    if r is not None:
        return r
    if j > n.k - 2:
        raise ValueError(f"cannot advance a level-{n.k} node by 2^{j}")
    if n.k == LEAF + 1:
        x = _step_bits(n.a.v | (n.b.v << LEAF_CELLS), 2 * LEAF_CELLS, 1 << j)
        r = leaf((x >> (LEAF_CELLS // 2)) & _LEAF_MASK)
    else:
        a, b = n.a, n.b
        m = join(a.b, b.a)
        if j == n.k - 2:
            r1, r2, r3 = result(a, j - 1), result(m, j - 1), result(b, j - 1)
            r = join(result(join(r1, r2), j - 1), result(join(r2, r3), j - 1))
        else:
            r1, r2, r3 = center(a), center(m), center(b)
            r = join(result(join(r1, r2), j), result(join(r2, r3), j))
    _results[key] = r
    return r


def ether_node(k, phase):
    """Level-k block of ether whose first cell is ETHER[phase]."""
    phase %= TILE
    key = (k, phase)
    n = _ether.get(key)
    if n is None:
        if k == LEAF:
            v = sum(1 << i for i in range(LEAF_CELLS)
                    if ETHER[(phase + i) % TILE] == "1")
            n = leaf(v)
        else:
            half = 1 << (k - 1)
            n = join(ether_node(k - 1, phase), ether_node(k - 1, phase + half))
        _ether[key] = n
    return n


def from_cells(cells):
    """uint8 0/1 array whose length is a power of two >= 64 -> node."""
    size = len(cells)
    if size < LEAF_CELLS or size & (size - 1):
        raise ValueError("length must be a power of two >= 64")
    by = np.packbits(cells.astype(np.uint8), bitorder="little").tobytes()
    step = LEAF_CELLS // 8
    level = [leaf(int.from_bytes(by[i:i + step], "little"))
             for i in range(0, len(by), step)]
    while len(level) > 1:
        level = [join(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def to_cells(n, lo, hi, out, x0):
    """Write cells [lo, hi) of node n (whose first cell is at x0) into out
    (out[0] is cell lo)."""
    size = 1 << n.k
    a, b = max(lo, x0), min(hi, x0 + size)
    if a >= b:
        return
    if n.k == LEAF:
        bits = np.unpackbits(np.frombuffer(n.v.to_bytes(LEAF_CELLS // 8, "little"),
                                           np.uint8), bitorder="little")
        out[a - lo:b - lo] = bits[a - x0:b - x0]
        return
    half = size >> 1
    to_cells(n.a, lo, hi, out, x0)
    to_cells(n.b, lo, hi, out, x0 + half)


DENSE_LEVEL = 16              # node_from_layout materializes blocks this small


def node_from_layout(layout, x0, k):
    """Node for cells [x0, x0 + 2^k) of a casim.Layout's t=0 row."""
    c = layout.gap_at(x0, x0 + (1 << k))
    if c is not None:
        return ether_node(k, c + x0)
    if k <= DENSE_LEVEL:
        return from_cells(layout.cells(x0, x0 + (1 << k)))
    h = 1 << (k - 1)
    return join(node_from_layout(layout, x0, k - 1),
                node_from_layout(layout, x0 + h, k - 1))


class HashRun:
    """A row embedded in ether, advanced with HashLife.

    row: uint8 array that starts and ends with at least one clean ether
    tile (e.g. casim.padded_row); origin: array index of the encoder's
    global column 0. Positions in window() are array coordinates, as in
    casim.Run. Gliders shift the ether's phase (their slip), so the ether
    left and right of the content have separate phase constants cL, cR:
    ether at (t, x) = ETHER[(c + x + 4t) mod 14]."""

    def __init__(self, row, origin):
        n = len(row)
        cL = _rotation(row[:TILE])
        cR = _rotation(row[n - TILE:]) - (n - TILE)
        k = max(LEAF + 2, int(np.ceil(np.log2(n))) + 2)
        size = 1 << k
        x0 = -((size - n) // 2)
        cells = np.empty(size, dtype=np.uint8)
        cells[:-x0] = [int(ETHER[(cL + x) % TILE]) for x in range(x0, 0)]
        cells[-x0:-x0 + n] = row
        cells[-x0 + n:] = [int(ETHER[(cR + x) % TILE])
                           for x in range(n, x0 + size)]
        self._start(from_cells(cells), x0, cL, cR, origin)

    @classmethod
    def from_layout(cls, layout):
        """Run of a casim.Layout (global columns: origin 0). The tree is
        built from the segments and ether gaps, never as one array."""
        n = layout.hi - layout.lo
        k = max(LEAF + 2, int(np.ceil(np.log2(n))) + 2)
        x0 = layout.lo - ((1 << k) - n) // 2
        run = cls.__new__(cls)
        run._start(node_from_layout(layout, x0, k), x0, layout.phases[0],
                   layout.phases[-1], 0)
        return run

    def _start(self, root, x0, cL, cR, origin):
        self.root, self.x0, self.cL, self.cR = root, x0, cL, cR
        self.origin = origin
        self.t = 0

    def _ether(self, k, x, c):
        return ether_node(k, c + x + ETHER_SHIFT_PER_STEP * self.t)

    def _expand(self):
        """Add a quarter of ether on each side: level k -> k + 1."""
        k, x0 = self.root.k, self.x0
        q = 1 << (k - 1)
        self.root = join(join(self._ether(k - 1, x0 - q, self.cL), self.root.a),
                         join(self.root.b, self._ether(k - 1, x0 + (1 << k), self.cR)))
        self.x0 = x0 - q

    def advance(self, j):
        """Advance by 2^j steps."""
        while self.root.k < j + 3:
            self._expand()
        # content must stay inside: the outer quarters must be ether now
        x0, q = self.x0, 1 << (self.root.k - 2)
        if not (self.root.a.a is self._ether(self.root.k - 2, x0, self.cL) and
                self.root.b.b is self._ether(self.root.k - 2, x0 + 3 * q, self.cR)):
            self._expand()
        self._expand()
        size = 1 << self.root.k
        self.root = result(self.root, j)
        self.x0 += size >> 2
        self.t += 1 << j

    def step(self, n):
        """Advance by n steps (binary decomposition, largest first)."""
        for j in range(n.bit_length() - 1, -1, -1):
            if n >> j & 1:
                self.advance(j)

    def history(self, lo, hi, depth):
        """Rows t..t+depth of cells [lo, hi); the run ends at t + depth (the
        contract of casim.Run.history). The rows are stepped locally on a
        window with depth extra cells on each side: the packed engine's
        wrap garbage (and the zero padding to whole words) enters at most
        one cell per step, so [lo, hi) stays exact. The tree then advances
        by depth on its own; the two are compared at the end."""
        width = hi - lo + 2 * depth
        words = pack(self.window(lo - depth, hi + depth))
        rows = [unpack(words, width)[depth:width - depth]]
        for _ in range(depth):
            words = step_packed(words)
            rows.append(unpack(words, width)[depth:width - depth])
        self.step(depth)
        if not np.array_equal(rows[-1], self.window(lo, hi)):
            raise AssertionError(f"t={self.t}: local history disagrees with the tree")
        return np.array(rows)

    def ebar_frame(self, t=None):
        from casim import EBAR_VELOCITY
        t = self.t if t is None else t
        return self.origin + int(round(EBAR_VELOCITY * t))

    def window(self, lo, hi):
        sh = ETHER_SHIFT_PER_STEP * self.t
        xs = np.arange(lo, hi)
        c = np.where(xs < self.x0, self.cL, self.cR)
        out = _ETHER_BITS[(c + xs + sh) % TILE]
        to_cells(self.root, lo, hi, out, self.x0)
        return out


_ETHER_BITS = np.array([int(ch) for ch in ETHER], dtype=np.uint8)


def _rotation(chunk):
    s = "".join(map(str, chunk))
    for r in range(TILE):
        if ETHER[r:] + ETHER[:r] == s:
            return r
    raise ValueError("row does not start/end in clean ether")


def stats():
    return {"leaves": len(_leaves), "nodes": len(_nodes), "results": len(_results)}
