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
# M2: the composable primitive inside the ring dynamics
# ---------------------------------------------------------------------------
AMBIENT_P = np.array([0.0005, 0.002, 0.01, 0.05])
BIRTH_P = np.array([0.005, 0.02, 0.05, 0.15])


def _local_target(byte, slot, side, rng):
    span = 2 * rng + 1
    dx = (byte & 0xF) % span - rng
    dy = ((byte >> 4) & 0xF) % span - rng
    x, y = slot % side, slot // side
    return ((y + dy) % side) * side + (x + dx) % side


def _ctrl(g):
    return field(g, CTRL)


def _mut_level(g):
    return (int(g[18]) << 1 | int(g[19]))


class CUniverse:
    """Ring dynamics with the composable VM as the transformation primitive.
    Variable-length genomes; local addressing; emergent heredity via
    self-templating; indel mutation. Mirrors growth.py but transform = run a
    program (composable) instead of applying ECA rules."""

    def __init__(self, nmax=256, seed=0, init_ops=6, self_template=True,
                 st_power=2.0, mut_scale=1.0, p_indel=0.03, local_range=2,
                 task=False, tpow=3.0, secret_len=8, n_pairs=6, input_len=24,
                 base_death=0.05, transform_off=False):
        self.nmax = nmax
        self.side = int(round(nmax ** 0.5))
        assert self.side * self.side == nmax
        self.rng = np.random.default_rng(seed)
        self.self_template = self_template
        self.st_power = st_power
        self.mut_scale = mut_scale
        self.p_indel = p_indel
        self.lr = local_range
        self.init_ops = init_ops
        self.base_death = base_death
        self.transform_off = transform_off
        # M3 task: program must reproduce target = secret(input). Persistent
        # selective pressure for complexity (the E14 lesson). Fixed across seeds.
        self.task = task
        self.tpow = tpow
        if task:
            tr = np.random.default_rng(98765)
            # target = bit-complement of the input: a strong, monotone gradient
            # (identity scores 0; matching requires flipping all L bits, i.e. a
            # long program), so complexity is genuinely demanded -- unlike a
            # near-identity secret (which left baseline fitness ~0.97).
            self._task = []
            for _ in range(n_pairs):
                inp = tr.integers(0, 2, size=input_len, dtype=np.uint8)
                self._task.append((inp, (1 - inp).astype(np.uint8)))

        self.genomes: list[np.ndarray | None] = [None] * nmax
        self.occupied = np.zeros(nmax, dtype=bool)
        self._moore = [[((s // self.side + dy) % self.side) * self.side
                        + (s % self.side + dx) % self.side
                        for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                        if not (dx == 0 and dy == 0)] for s in range(nmax)]
        self.tick = 0

    def task_fit(self, g):
        ops = program_ops(g)
        return float(np.mean([np.mean(run(ops, inp) == tgt)
                              for inp, tgt in self._task]))

    def _repro_prob(self, g):
        p = 1.0
        if self.self_template:
            p *= self_preservation(g) ** self.st_power
        if self.task:
            p *= self.task_fit(g) ** self.tpow
        return p

    def seed_full(self):
        for s in range(self.nmax):
            self.genomes[s] = self.rng.integers(
                0, 2, size=HEADER + self.init_ops * OP_BITS, dtype=np.uint8)
            self.occupied[s] = True

    def _mutate(self, g):
        p = BIRTH_P[_mut_level(g)] * self.mut_scale
        g = g ^ (self.rng.random(len(g)) < p).astype(np.uint8)
        if self.rng.random() < self.p_indel:        # indel one opcode
            no = n_ops(g)
            if self.rng.random() < 0.5:
                pos = HEADER + int(self.rng.integers(0, no + 1)) * OP_BITS
                g = np.concatenate([g[:pos],
                                    self.rng.integers(0, 2, OP_BITS, dtype=np.uint8),
                                    g[pos:]])
            elif no > 1:
                pos = HEADER + int(self.rng.integers(0, no)) * OP_BITS
                g = np.concatenate([g[:pos], g[pos + OP_BITS:]])
        return g

    def step(self):
        g0 = [None if x is None else x.copy() for x in self.genomes]
        occ0 = self.occupied.copy()
        side, R = self.side, self.lr
        occ_idx = np.where(occ0)[0]
        # transformers per target (pull source + pushers), by source slot order
        targets = {int(t): [] for t in occ_idx}
        for t in occ_idx:
            s = _local_target(field(g0[t], PULL), int(t), side, R)
            if occ0[s]:
                targets[int(t)].append(int(s))
        for s in occ_idx:
            t = _local_target(field(g0[s], PUSH), int(s), side, R)
            if occ0[t]:
                targets[int(t)].append(int(s))
        new = [None if x is None else x.copy() for x in g0]
        if not self.transform_off:
            for t, srcs in targets.items():
                if not srcs:
                    continue
                cur = g0[t]
                for s in sorted(srcs):
                    cur = run(program_ops(g0[s]), cur)
                new[t] = cur
        occ1 = occ0.copy()
        newborns = []
        # births (CTRL spawn bit), self-templating gate, into empty neighbour
        filled = occ0.copy()
        spawners = [int(s) for s in occ_idx if g0[s][16] == 1]
        self.rng.shuffle(spawners)
        for s in spawners:
            # reproduction is viable for all (self-templating gate only, ~free
            # here); the task acts as a SURVIVAL advantage (below), not a
            # reproduction gate -- avoids the E3 extinction trap.
            if self.self_template and \
               self.rng.random() >= self_preservation(g0[s]) ** self.st_power:
                continue
            cands = [n for n in self._moore[s] if not filled[n]]
            if not cands:
                continue
            slot = int(cands[self.rng.integers(len(cands))])
            new[slot] = self._mutate(g0[s].copy())
            occ1[slot] = True; filled[slot] = True; newborns.append(slot)
        # deaths: CTRL death bit + fitness-biased mortality. With a task, low
        # task-fitness rings die MORE (death_prob = base_death*(1 - fit)^tpow),
        # so fitness is a survival advantage -> selection for complexity without
        # gating reproduction (avoids extinction). Without a task: uniform.
        for d in occ_idx:
            if g0[d][17] == 1:
                occ1[d] = False; new[d] = None; continue
            if self.task:
                dp = self.base_death * (1.0 - self.task_fit(g0[d])) ** self.tpow
            else:
                dp = self.base_death
            if self.rng.random() < dp:
                occ1[d] = False; new[d] = None
        # ambient mutation on survivors (not newborns)
        nb = set(newborns)
        for s in np.where(occ1)[0]:
            if s in nb or new[s] is None:
                continue
            p = AMBIENT_P[_mut_level(new[s])] * self.mut_scale
            flips = self.rng.random(len(new[s])) < p
            if flips.any():
                new[s] = new[s] ^ flips.astype(np.uint8)
        self.genomes = new
        self.occupied = occ1
        self.tick += 1

    def stats(self):
        idx = np.where(self.occupied)[0]
        if len(idx) == 0:
            return dict(pop=0, mean_ops=0.0, pres=float("nan"))
        ops = [n_ops(self.genomes[s]) for s in idx]
        pres = np.mean([self_preservation(self.genomes[s]) for s in idx[:120]])
        return dict(pop=len(idx), mean_ops=float(np.mean(ops)), pres=float(pres))


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


def complexity_experiment(seeds=2, ticks=2000):
    """E21: does used-computation complexity grow under a task reward? Compares
    program/data CONFLATED (ring architecture: self-templating, transform on)
    vs SEPARATED (faithful copy, program acts on external task data only).
    Target = bit-complement. Prints used-ops (effective_ops) over time."""
    ref = CUniverse(nmax=256, seed=0, task=True, input_len=16)
    inputs = [i for i, _ in ref._task]

    def used(u, k=40):
        idx = np.where(u.occupied)[0]
        return (float(np.mean([effective_ops(u.genomes[s], inputs)
                               for s in idx[:k]])) if len(idx) else float("nan"))

    configs = {
        "conflated+task  (ring: self-templating, transform on)":
            dict(task=True, self_template=True, transform_off=False,
                 tpow=1.5, base_death=0.2, mut_scale=1.5, p_indel=0.06),
        "separated+task  (faithful copy, program on external data)":
            dict(task=True, self_template=False, transform_off=True,
                 tpow=1.5, base_death=0.2, mut_scale=1.5, p_indel=0.06),
        "separated, NO task (control)":
            dict(task=False, self_template=False, transform_off=True,
                 base_death=0.2, mut_scale=1.5, p_indel=0.06),
    }
    print(f"E21 complexity growth (used-ops; ECA plateaued ~2 in E15), {ticks} ticks")
    for name, kw in configs.items():
        for seed in range(seeds):
            u = CUniverse(nmax=256, seed=seed, init_ops=4, input_len=16, **kw)
            u.seed_full()
            marks = {}
            for t in range(1, ticks + 1):
                u.step()
                if t in (ticks // 4, ticks): marks[t] = used(u)
            pts = "  ".join(f"t{t}:used={marks[t]:.1f}" for t in sorted(marks))
            print(f"  {name:55} s{seed}: {pts}")


if __name__ == "__main__":
    import sys
    if "exp" in sys.argv:
        complexity_experiment()
    else:
        _tests()
