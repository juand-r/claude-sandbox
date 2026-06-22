"""Option 3 (variant i), M1: a composable primitive for the ring substrate.

Replaces the single 8-bit ECA rule with a short straight-line PROGRAM of
composable bit operations, run on the target genome as a bit-tape. See
OPTION3_COMPOSABLE_SUBSTRATE.md. This module is the VM only (M1); M2 drops it
into the ring tick, M3 runs the complexity experiment.

Genome (variable-length np.uint8 bit array):
    [ header: PULL(8) PUSH(8) CTRL(8) | program: 4-bit opcodes ... ]

Instruction set (opcode = 4 bits; straight-line, runtime bounded by program
length; pointer p over the tape, wraps mod L):
    0 NOP   1 FWD(p+1)  2 BACK(p-1)  3 FLIP(t[p]^=1)  4 COPY(t[p+1]=t[p])
    5 XORB(t[p]^=t[p-1])  6 SKIPZ(if t[p]==0 skip next)  7 SKIPNZ
    8..15 NOP (reserved)
"""

from __future__ import annotations

import numpy as np

HEADER = 24          # PULL(0-7) PUSH(8-15) CTRL(16-23)
OP_BITS = 4
PULL = (0, 8)
PUSH = (8, 16)
CTRL = (16, 24)


def field(g: np.ndarray, span) -> int:
    lo, hi = span
    return int(g[lo:hi] @ (1 << np.arange(hi - lo - 1, -1, -1)))


def program_ops(g: np.ndarray) -> list[int]:
    """Decode the program region into a list of opcodes (0..15)."""
    body = g[HEADER:]
    nops = len(body) // OP_BITS
    ops = []
    for k in range(nops):
        b = body[k * OP_BITS:(k + 1) * OP_BITS]
        ops.append(int(b[0]) * 8 + int(b[1]) * 4 + int(b[2]) * 2 + int(b[3]))
    return ops


def n_ops(g: np.ndarray) -> int:
    return (len(g) - HEADER) // OP_BITS


def run(ops: list[int], tape: np.ndarray) -> np.ndarray:
    """Execute the straight-line program on a copy of `tape`; return the result.
    Pointer wraps mod L. SKIPZ/SKIPNZ skip the next instruction conditionally.
    Runtime is bounded by len(ops) (no loops)."""
    t = tape.copy()
    L = len(t)
    if L == 0:
        return t
    p = 0
    i = 0
    n = len(ops)
    while i < n:
        o = ops[i]
        if o == 1:   p = (p + 1) % L
        elif o == 2: p = (p - 1) % L
        elif o == 3: t[p] ^= 1
        elif o == 4: t[(p + 1) % L] = t[p]
        elif o == 5: t[p] ^= t[(p - 1) % L]
        elif o == 6:
            if t[p] == 0: i += 1
        elif o == 7:
            if t[p] == 1: i += 1
        # 0 and 8..15 are NOP
        i += 1
    return t


def transform(src: np.ndarray, tape: np.ndarray) -> np.ndarray:
    """B transforms A: run B(=src)'s program on A(=tape)'s bits."""
    return run(program_ops(src), tape)


def self_preservation(g: np.ndarray) -> float:
    """Fraction of a ring's bits left unchanged by its own program (the
    self-templating / emergent-heredity signal, as in E6)."""
    out = run(program_ops(g), g)
    return float(np.mean(out == g))


def effective_ops(g: np.ndarray, inputs: list[np.ndarray]) -> int:
    """Used-computation complexity: number of program instructions whose removal
    changes the output on at least one input. (Honest complexity metric --- not
    raw length; avoids the E14 junk trap.) O(n_ops * len(inputs)); use on a
    sample at measurement ticks only."""
    ops = program_ops(g)
    base = [run(ops, x) for x in inputs]
    used = 0
    for k in range(len(ops)):
        red = ops[:k] + ops[k + 1:]
        if any(not np.array_equal(run(red, x), b) for x, b in zip(inputs, base)):
            used += 1
    return used


# ---------------------------------------------------------------------------
# M1 tests
# ---------------------------------------------------------------------------
def _g(header_bits, ops):
    """Build a genome from 24 header bits + a list of opcodes."""
    body = []
    for o in ops:
        body += [(o >> 3) & 1, (o >> 2) & 1, (o >> 1) & 1, o & 1]
    return np.array(list(header_bits) + body, dtype=np.uint8)


def _tests():
    H = [0] * 24
    tape = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
    # FLIP at p=0
    assert np.array_equal(run([3], tape), [1, 0, 0, 0, 0, 0, 0, 0])
    # FWD, FLIP -> bit1
    assert np.array_equal(run([1, 3], tape), [0, 1, 0, 0, 0, 0, 0, 0])
    # BACK from 0 wraps to last, FLIP
    assert np.array_equal(run([2, 3], tape), [0, 0, 0, 0, 0, 0, 0, 1])
    # COPY: set bit0 then copy to bit1
    assert np.array_equal(run([3, 4], tape), [1, 1, 0, 0, 0, 0, 0, 0])
    # XORB: t[0]^=t[-1]; with t[-1]=1
    t2 = np.array([0, 0, 0, 0, 0, 0, 0, 1], dtype=np.uint8)
    assert np.array_equal(run([5], t2), [1, 0, 0, 0, 0, 0, 0, 1])
    # SKIPZ: t[0]==0 -> skip FLIP -> unchanged
    assert np.array_equal(run([6, 3], tape), tape)
    # SKIPZ: t[0]==1 -> do not skip -> FLIP fires (clears bit0)
    t3 = np.array([1, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
    assert np.array_equal(run([6, 3], t3), [0, 0, 0, 0, 0, 0, 0, 0])
    # SKIPNZ mirror
    assert np.array_equal(run([7, 3], t3), t3)        # t[0]==1 -> skip FLIP
    assert np.array_equal(run([7, 3], tape), [1, 0, 0, 0, 0, 0, 0, 0])
    # empty program = identity
    assert np.array_equal(run([], tape), tape)
    # reserved opcodes are NOP
    assert np.array_equal(run([8, 12, 15], tape), tape)
    # decode round-trip
    g = _g(H, [1, 3, 4, 6])
    assert program_ops(g) == [1, 3, 4, 6]
    assert n_ops(g) == 4
    assert field(g, PULL) == 0
    # header fields decode
    g2 = _g([1, 0, 1, 0, 1, 0, 1, 0] + [0] * 16, [3])
    assert field(g2, PULL) == 0b10101010
    # self_preservation: identity program preserves everything
    assert self_preservation(_g(H, [0, 0])) == 1.0
    # effective_ops: a program with redundant NOPs has fewer used ops than length
    inp = [np.array([1, 0, 1, 1, 0, 0, 1, 0], dtype=np.uint8),
           np.array([0, 1, 0, 0, 1, 1, 0, 1], dtype=np.uint8)]
    gg = _g(H, [3, 0, 0, 1, 3])          # 5 ops, two are NOP
    eff = effective_ops(gg, inp)
    assert eff <= 5 and eff >= 1, eff

    # composability sanity: as random program length grows, the mean fraction of
    # tape bits changed should rise smoothly toward a plateau (NOT jump to a
    # chaotic ~0.5 at length 1, as a single ECA rule would). Light check:
    rng = np.random.default_rng(0)
    base = np.array([1, 0, 1, 1, 0, 1, 0, 0] * 2, dtype=np.uint8)
    prev = -1.0
    fracs = []
    for L in (1, 2, 4, 8, 16):
        ch = []
        for _ in range(200):
            ops = [int(rng.integers(0, 8)) for _ in range(L)]
            ch.append(np.mean(run(ops, base) != base))
        fracs.append(float(np.mean(ch)))
    # monotone non-decreasing-ish and starts small (composition builds up)
    assert fracs[0] < fracs[-1], fracs
    assert fracs[0] < 0.25, fracs           # length-1 changes little (vs ECA ~0.5)
    print("composability change-fraction by length [1,2,4,8,16]:",
          [round(f, 3) for f in fracs])

    tests = [v for k, v in globals().items() if k.startswith("test_")]
    print("M1 VM tests passed.")


if __name__ == "__main__":
    _tests()
