"""1-D HashLife for Rule 110 (Gosper's algorithm, one dimension).

A node of level k stands for 2^k consecutive cells. Leaves are level 6:
64 cells in a uint64 (bit i = cell i, left to right). Nodes are
hash-consed, so equal subtrees are one node, and results are memoized:
result(n, j) is the centre half of node n (level k) after 2^j steps,
j <= k - 2. Rule 110 has radius 1, so after s steps a block of 2^k cells
determines exactly its cells [s, 2^k - s), and the centre half is
determined for s <= 2^(k-2).

The core (node store, hash-consing, memoized result, garbage collection)
is C, in hlc.c, compiled on first import and called through ctypes; here
a node is its integer id, and equal ids mean equal content. (v0.2: the
pure-Python core it replaced is trash/hashlife_py.py; ~50x slower.)

The universe is a finite row embedded in ether. Ether moves by the
lattice vector (1, -4): row(t+1)[x] = row(t)[x + 4] (checked with
engine.step), so an ether block at any place and time is a phase shift of
the ETHER tile and is itself one node per (level, phase). HashRun keeps a
root node, expands it with ether nodes of the right phase before each
advance, and fails loudly if non-ether content reaches the root's outer
quarters.
"""

import ctypes
import os
import subprocess

import numpy as np

from engine import ETHER, pack, step_packed, unpack

LEAF = 6                      # leaf level: 64 cells
LEAF_CELLS = 1 << LEAF
TILE = len(ETHER)
ETHER_SHIFT_PER_STEP = 4      # row(t+1)[x] = row(t)[x + 4]
NONE = 0xFFFFFFFF

_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_DIR, "hlc.c")
_LIB = os.path.join(_DIR, "__pycache__", "hlc.so")


def _load():
    if not os.path.exists(_LIB) or os.path.getmtime(_LIB) < os.path.getmtime(_SRC):
        os.makedirs(os.path.dirname(_LIB), exist_ok=True)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", _LIB, _SRC], check=True)
    lib = ctypes.CDLL(_LIB)
    u32, u64, i32 = ctypes.c_uint32, ctypes.c_uint64, ctypes.c_int
    for name, res, args in (
            ("hl_reset", i32, []), ("hl_failed", i32, []),
            ("hl_leaf", u32, [u64]), ("hl_join", u32, [u32, u32]),
            ("hl_result", u32, [u32, i32]), ("hl_center", u32, [u32]),
            ("hl_level", i32, [u32]), ("hl_a", u32, [u32]), ("hl_b", u32, [u32]),
            ("hl_value", u64, [u32]), ("hl_count", u64, []), ("hl_results", u64, []),
            ("hl_leaves", None, [u32, u64, u64, ctypes.c_void_p]),
            ("hl_from_words", u32, [ctypes.c_void_p, u64]),
            ("hl_gc", u32, [u32]), ("hl_set_frame", i32, [i32]),
            ("hl_frame", i32, []), ("hl_max_j", i32, [i32])):
        f = getattr(lib, name)
        f.restype, f.argtypes = res, args
    if not lib.hl_reset():
        raise MemoryError("hashlife core: initial allocation failed")
    return lib


_lib = _load()
_ether = {}                   # (k, phase) -> node; cleared on collection


def _check(n):
    if n == NONE or _lib.hl_failed():
        raise MemoryError("hashlife core failed (allocation, or a bad level)")
    return n


def leaf(v):
    return _check(_lib.hl_leaf(v))


def join(a, b):
    return _check(_lib.hl_join(a, b))


level = _lib.hl_level
child_a = _lib.hl_a
child_b = _lib.hl_b
value = _lib.hl_value


def center(n):
    """Middle half of n (one level down), at the same time."""
    return _check(_lib.hl_center(n))


def result(n, j):
    """Centre half of n after 2^j steps (j <= level(n) - 2; in the Ebar
    frame, steps of 30 generations and j <= level(n) - 8)."""
    if j > _lib.hl_max_j(level(n)):
        raise ValueError(f"cannot advance a level-{level(n)} node by 2^{j}")
    return _check(_lib.hl_result(n, j))


def set_frame(ebar):
    """Switch the core between the lab frame (False) and the Ebar frame
    (True), where one step is 30 generations followed by a shift of 8 cells
    (hlc.c). Every node id becomes invalid."""
    _ether.clear()
    if not _lib.hl_set_frame(int(ebar)):
        raise MemoryError("hashlife core: allocation failed")


def ether_node(k, phase):
    """Level-k block of ether whose first cell is ETHER[phase]."""
    phase %= TILE
    key = (k, phase)
    n = _ether.get(key)
    if n is None:
        if k == LEAF:
            n = leaf(sum(1 << i for i in range(LEAF_CELLS)
                         if ETHER[(phase + i) % TILE] == "1"))
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
    words = np.packbits(cells.astype(np.uint8), bitorder="little").view(np.uint64)
    words = np.ascontiguousarray(words)
    return _check(_lib.hl_from_words(words.ctypes.data, len(words)))


def to_cells(n, lo, hi, out, x0):
    """Write cells [lo, hi) of node n (whose first cell is at x0) into out
    (out[0] is cell lo)."""
    size = 1 << level(n)
    a, b = max(lo, x0), min(hi, x0 + size)
    if a >= b:
        return
    first = (a - x0) // LEAF_CELLS
    count = (b - x0 - 1) // LEAF_CELLS - first + 1
    words = np.zeros(count, dtype=np.uint64)
    _lib.hl_leaves(n, first, count, words.ctypes.data)
    bits = np.unpackbits(words.view(np.uint8), bitorder="little")
    s = x0 + first * LEAF_CELLS
    out[a - lo:b - lo] = bits[a - s:b - s]


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

    MARGIN = 2                # a level-k node is advanced at most 2^(k-MARGIN)
    SHIFT = ETHER_SHIFT_PER_STEP

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
    def from_layout(cls, layout, align=1):
        """Run of a casim.Layout (global columns: origin 0). The tree is
        built from the segments and ether gaps, never as one array. align:
        the tree's left edge is a multiple of it (a power of two)."""
        n = layout.hi - layout.lo + align
        k = max(LEAF + 2, int(np.ceil(np.log2(n))) + 2)
        x0 = (layout.lo - ((1 << k) - n) // 2) // align * align
        run = cls.__new__(cls)
        run._start(node_from_layout(layout, x0, k), x0, layout.phases[0],
                   layout.phases[-1], 0)
        return run

    def _start(self, root, x0, cL, cR, origin, t=0):
        self.root, self.x0, self.cL, self.cR = root, x0, cL, cR
        self.origin = origin
        self.t = t

    def _ether(self, k, x, c):
        return ether_node(k, c + x + self.SHIFT * self.t)

    def _expand(self):
        """Add a quarter of ether on each side: level k -> k + 1."""
        k, x0 = level(self.root), self.x0
        q = 1 << (k - 1)
        self.root = join(join(self._ether(k - 1, x0 - q, self.cL), child_a(self.root)),
                         join(child_b(self.root), self._ether(k - 1, x0 + (1 << k), self.cR)))
        self.x0 = x0 - q

    def advance(self, j):
        """Advance by 2^j steps."""
        while level(self.root) < j + self.MARGIN + 1:
            self._expand()
        # content must stay inside: the outer quarters must be ether now
        k = level(self.root)
        x0, q = self.x0, 1 << (k - 2)
        if not (child_a(child_a(self.root)) == self._ether(k - 2, x0, self.cL) and
                child_b(child_b(self.root)) == self._ether(k - 2, x0 + 3 * q, self.cR)):
            self._expand()
        self._expand()
        size = 1 << level(self.root)
        self.root = result(self.root, j)
        self.x0 += size >> 2
        self.t += 1 << j

    def step(self, n):
        """Advance by n steps (binary decomposition, largest first)."""
        for j in range(n.bit_length() - 1, -1, -1):
            if n >> j & 1:
                self.advance(j)

    def history(self, lo, hi, depth, advance=True):
        """Rows t..t+depth of cells [lo, hi). With advance (the contract of
        casim.Run.history) the run ends at t + depth; otherwise it stays
        at t. The rows are stepped locally on a window with depth extra
        cells on each side: the packed engine's wrap garbage (and the zero
        padding to whole words) enters at most one cell per step, so
        [lo, hi) stays exact. With advance the tree then steps on its own
        and the two are compared."""
        width = hi - lo + 2 * depth
        words = pack(self.window(lo - depth, hi + depth))
        rows = [unpack(words, width)[depth:width - depth]]
        for _ in range(depth):
            words = step_packed(words)
            rows.append(unpack(words, width)[depth:width - depth])
        if advance:
            self.step(depth)
            if not np.array_equal(rows[-1], self.window(lo, hi)):
                raise AssertionError(f"t={self.t}: local history disagrees with the tree")
        return np.array(rows)

    def ebar_frame(self, t=None):
        from casim import EBAR_VELOCITY
        t = self.t if t is None else t
        return self.origin + int(round(EBAR_VELOCITY * t))

    def window(self, lo, hi):
        sh = self.SHIFT * self.t
        xs = np.arange(lo, hi)
        c = np.where(xs < self.x0, self.cL, self.cR)
        out = _ETHER_BITS[(c + xs + sh) % TILE]
        to_cells(self.root, lo, hi, out, self.x0)
        return out


_ETHER_BITS = np.array([int(ch) for ch in ETHER], dtype=np.uint8)


class FrameRun(HashRun):
    """HashRun in the Ebar frame (set_frame(True) first): t counts F steps
    of 30 generations, column y = lab column + 8 t; ether, table, moving
    data and junk are static. history() and ebar_frame() are lab-frame
    notions and are not provided here."""

    MARGIN = 8
    SHIFT = 0

    def history(self, *a, **k):
        raise NotImplementedError("lab-frame history: use frame_history")

    ebar_frame = history


def _rotation(chunk):
    s = "".join(map(str, chunk))
    for r in range(TILE):
        if ETHER[r:] + ETHER[:r] == s:
            return r
    raise ValueError("row does not start/end in clean ether")


def recanonicalize(root):
    """Garbage collection: keep only root's nodes (they get new ids) and
    drop every memo entry. Every other node id becomes invalid."""
    _ether.clear()
    return _check(_lib.hl_gc(root))


def dump(root):
    """root's DAG as a list, children before parents: a leaf is its int
    value, an inner node the pair of its children's indices."""
    out, index = [], {}

    def rec(n):
        i = index.get(n)
        if i is None:
            item = value(n) if level(n) == LEAF else (rec(child_a(n)), rec(child_b(n)))
            out.append(item)
            i = index[n] = len(out) - 1
        return i
    rec(root)
    return out


def load(items):
    """Inverse of dump."""
    nodes = []
    for item in items:
        nodes.append(leaf(item) if isinstance(item, int) else
                     join(nodes[item[0]], nodes[item[1]]))
    return nodes[-1]


def stats():
    return {"nodes": _lib.hl_count(), "results": _lib.hl_results()}
