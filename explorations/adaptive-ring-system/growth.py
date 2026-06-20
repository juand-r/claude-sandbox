"""Variable-length "program rings" --- the B7 / E14 experiment on whether
complexity can grow (break the E13 ceiling).

Departs from the fixed 36-bit spec (see DESIGN.md section 10): each ring is a
variable-length multiple-of-8 bitstring of GENES (bytes):

    gene 0 = PULL  (local (dx,dy) offset of who transforms me)
    gene 1 = PUSH  (local (dx,dy) offset of who I transform)
    gene 2 = CTRL  (bit0 spawn, bit1 death, bits2-3 mutation level, bits4-7 order)
    genes 3.. = RULE PROGRAM: a sequence of 8-bit ECA rules

"B transforms A" applies B's whole rule program (each gene 3.. in turn) as
successive CA steps over A's circular bits. So the *length of the program* is
the ring's functional complexity, and it can grow/shrink via indel mutation.
Everything else (local torus addressing, Moore-neighbour births, self-templating,
snapshot tick, birth-before-death) mirrors ring_system.

Reuses ring_system.apply_rule and local_target (tested).
"""

from __future__ import annotations

import numpy as np

from ring_system import apply_rule, local_target

GENE = 8
PULL, PUSH, CTRL = 0, 1, 2
HEADER = 3                     # genes 0..2 are header; 3.. are the program
MIN_GENES = 4                 # at least one program rule
AMBIENT_P = np.array([0.0005, 0.002, 0.01, 0.05])
BIRTH_P = np.array([0.005, 0.02, 0.05, 0.15])


def gene(g: np.ndarray, i: int) -> int:
    """Byte value of gene i (MSB-first)."""
    b = g[i * GENE:(i + 1) * GENE]
    return int(b @ (1 << np.arange(GENE - 1, -1, -1)))


def n_genes(g: np.ndarray) -> int:
    return len(g) // GENE


def program(g: np.ndarray) -> list[int]:
    """The list of ECA rules a ring applies (genes 3..)."""
    return [gene(g, i) for i in range(HEADER, n_genes(g))]


def mut_level(g: np.ndarray) -> int:
    c = gene(g, CTRL)
    return (c >> 2) & 0b11


def order_of(g: np.ndarray) -> int:
    return (gene(g, CTRL) >> 4) & 0b1111


def apply_program(prog: list[int], bits: np.ndarray) -> np.ndarray:
    """Apply a sequence of ECA rules as successive CA steps."""
    cur = bits
    for rule in prog:
        cur = apply_rule(rule, cur)
    return cur


def self_preservation(g: np.ndarray) -> float:
    """Fraction of a ring's bits left unchanged by its own program."""
    out = apply_program(program(g), g)
    return float(np.mean(out == g))


class Universe:
    def __init__(self, nmax=256, seed=0, init_genes=5,
                 self_template=True, st_power=2.0, mut_scale=1.0,
                 p_indel=0.02, local_range=2,
                 task=False, tpow=4.0, task_secret_len=6, task_pairs=8,
                 task_input_len=24):
        self.nmax = nmax
        self.side = int(round(nmax ** 0.5))
        assert self.side * self.side == nmax
        self.rng = np.random.default_rng(seed)
        self.self_template = self_template
        self.st_power = st_power
        self.mut_scale = mut_scale
        self.p_indel = p_indel
        self.local_range = local_range
        self.genomes: list[np.ndarray | None] = [None] * nmax
        self.occupied = np.zeros(nmax, dtype=bool)
        self.init_genes = init_genes
        self._moore = self._build_moore()
        self.tick_count = 0
        # E15: a fixed computational task. Targets are produced by a length-N
        # "secret" program, so matching them rewards comparable program length.
        self.task = task
        self.tpow = tpow
        if task:
            trng = np.random.default_rng(12345)   # fixed task across seeds/runs
            secret = [int(trng.integers(0, 256)) for _ in range(task_secret_len)]
            self._task = []
            for _ in range(task_pairs):
                inp = trng.integers(0, 2, size=task_input_len, dtype=np.uint8)
                self._task.append((inp, apply_program(secret, inp)))

    def task_fit(self, g: np.ndarray) -> float:
        """Mean bit-match of a ring's program against the task pairs (0..1)."""
        prog = program(g)
        return float(np.mean([np.mean(apply_program(prog, inp) == tgt)
                              for inp, tgt in self._task]))

    def _repro_prob(self, g: np.ndarray) -> float:
        p = 1.0
        if self.self_template:
            p *= self_preservation(g) ** self.st_power
        if self.task:
            p *= self.task_fit(g) ** self.tpow
        return p

    def _build_moore(self):
        side = self.side; nb = []
        for s in range(self.nmax):
            x, y = s % side, s // side
            nb.append([((y + dy) % side) * side + (x + dx) % side
                       for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                       if not (dx == 0 and dy == 0)])
        return nb

    def seed_full(self):
        for s in range(self.nmax):
            self.genomes[s] = self.rng.integers(
                0, 2, size=self.init_genes * GENE, dtype=np.uint8)
            self.occupied[s] = True

    # -- mutation -----------------------------------------------------------
    def _mutate(self, g: np.ndarray) -> np.ndarray:
        p = BIRTH_P[mut_level(g)] * self.mut_scale
        g = g ^ (self.rng.random(len(g)) < p).astype(np.uint8)
        # indel: insert or delete a whole gene
        if self.rng.random() < self.p_indel:
            ng = n_genes(g)
            if self.rng.random() < 0.5:                      # insert
                pos = self.rng.integers(HEADER, ng + 1) * GENE
                newgene = self.rng.integers(0, 2, size=GENE, dtype=np.uint8)
                g = np.concatenate([g[:pos], newgene, g[pos:]])
            elif ng > MIN_GENES:                              # delete
                pos = self.rng.integers(HEADER, ng) * GENE
                g = np.concatenate([g[:pos], g[pos + GENE:]])
        return g

    # -- tick ---------------------------------------------------------------
    def step(self):
        g0 = [None if x is None else x.copy() for x in self.genomes]
        occ0 = self.occupied.copy()
        side, R = self.side, self.local_range
        occ_idx = np.where(occ0)[0]

        # build transformers per target: (order, source)
        targets: dict[int, list[tuple[int, int]]] = {t: [] for t in occ_idx}
        for t in occ_idx:
            s = local_target(gene(g0[t], PULL), int(t), side, R)
            if occ0[s]:
                targets[t].append((order_of(g0[s]), s))
        for s in occ_idx:
            t = local_target(gene(g0[s], PUSH), int(s), side, R)
            if occ0[t]:
                targets[t].append((order_of(g0[s]), s))

        # compose: apply each transformer's program in ORDER order
        new = [None if x is None else x.copy() for x in g0]
        for t, insts in targets.items():
            if not insts:
                continue
            insts.sort(key=lambda z: (z[0], z[1]))
            cur = g0[t]
            for _o, s in insts:
                cur = apply_program(program(g0[s]), cur)   # lengths match (both t's)
            new[t] = cur

        occ1 = occ0.copy()
        newborns = []
        # births (snapshot spawn bit), local, before deaths
        spawners = [int(s) for s in occ_idx if gene(g0[s], CTRL) & 1]
        self.rng.shuffle(spawners)
        filled = occ0.copy()
        for s in spawners:
            if (self.self_template or self.task):
                if self.rng.random() >= self._repro_prob(g0[s]):
                    continue
            cands = [n for n in self._moore[s] if not filled[n]]
            if not cands:
                continue
            slot = int(cands[self.rng.integers(len(cands))])
            new[slot] = self._mutate(g0[s].copy())
            occ1[slot] = True; filled[slot] = True; newborns.append(slot)

        # deaths (snapshot death bit)
        for d in occ_idx:
            if gene(g0[d], CTRL) & 0b10:
                occ1[d] = False; new[d] = None

        # ambient mutation on survivors (not newborns)
        nb = set(newborns)
        for s in np.where(occ1)[0]:
            if s in nb or new[s] is None:
                continue
            p = AMBIENT_P[mut_level(new[s])] * self.mut_scale
            flips = self.rng.random(len(new[s])) < p
            if flips.any():
                new[s] = new[s] ^ flips.astype(np.uint8)

        self.genomes = new
        self.occupied = occ1
        self.tick_count += 1

    # -- metrics ------------------------------------------------------------
    def stats(self):
        idx = np.where(self.occupied)[0]
        if len(idx) == 0:
            return dict(pop=0, mean_genes=0, mean_prog=0, pres=float("nan"))
        gns = [n_genes(self.genomes[s]) for s in idx]
        pres = np.mean([self_preservation(self.genomes[s]) for s in idx[:120]])
        return dict(pop=len(idx), mean_genes=float(np.mean(gns)),
                    mean_prog=float(np.mean(gns)) - HEADER, pres=float(pres),
                    max_genes=int(np.max(gns)))
