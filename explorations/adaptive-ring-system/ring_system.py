"""Adaptive Ring System --- core simulator.

A finite universe of self-modifying rings. Each ring is 36 bits and is
simultaneously data, an elementary-CA transformation rule, and a node in a
transformation network. There is no controller, fitness, or energy.

See DESIGN.md for the full specification and the rationale behind every
decision. The load-bearing semantics:

  * A ring is a CIRCULAR 36-bit string (bit 0's left neighbour is bit 35).
  * "B transforms A" = run B's 8-bit elementary CA rule once around A's bits.
  * Transformers of a target form a MULTISET (pull and push are not
    deduplicated) composed in ascending ORDER (ties by slot address).
  * Each tick reads a start-of-tick snapshot, giving death/birth one tick of
    latency (a death sentence is contestable within the tick).
  * Birth resolves before death, so a ring's death never cancels its child.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np

# --------------------------------------------------------------------------
# Bit layout (36 bits; lowest index = most significant bit within a field).
# RULE | PULL | PUSH | ORDER | SPAWN | DEATH | MUTATION
#   8     8      8      8       1       1        2
# --------------------------------------------------------------------------
N_BITS = 36
RULE = (0, 8)
PULL = (8, 16)
PUSH = (16, 24)
ORDER = (24, 32)
SPAWN_BIT = 32
DEATH_BIT = 33
MUT = (34, 36)

# Mutation rate tables, keyed by the 2-bit MUTATION field (0..3). All
# nonzero ("zero mutation does not exist"). Tunable.
AMBIENT_P = np.array([0.0005, 0.002, 0.01, 0.05])   # per ring, per tick
BIRTH_P = np.array([0.005, 0.02, 0.05, 0.15])       # per child bit, once


def get_field(bits2d: np.ndarray, span: tuple[int, int]) -> np.ndarray:
    """Read an integer field from each row (lowest index = MSB)."""
    lo, hi = span
    weights = 1 << np.arange(hi - lo - 1, -1, -1)
    return bits2d[:, lo:hi] @ weights


def mut_level(row: np.ndarray) -> int:
    """The 2-bit MUTATION field of a single ring as an int 0..3."""
    return int(row[MUT[0]]) * 2 + int(row[MUT[0] + 1])


def apply_rule(rule: int, bits: np.ndarray) -> np.ndarray:
    """One elementary-CA step of `rule` (0..255) around the circular `bits`.

    Wolfram convention: neighbourhood (left, center, right) indexes the rule
    as 4*left + 2*center + right; the rule bit at that index is the output.
    All outputs are computed from the input (synchronous single step).
    """
    left = np.roll(bits, 1)     # left[i]  = bits[i-1]
    right = np.roll(bits, -1)   # right[i] = bits[i+1]
    idx = (left << 2) | (bits << 1) | right
    return ((rule >> idx) & 1).astype(np.uint8)


def build_transformers(bits: np.ndarray, occ: np.ndarray):
    """For each occupied target, the ordered multiset of transformer slots.

    Returns (targets, rule) where targets[t] is a list of (order, slot)
    transformer instances sorted ascending by (order, slot), and rule is the
    per-slot RULE value. Pull and push each contribute one instance and are
    NOT deduplicated, so A.push==B with B.pull==A yields B' = A(A(B)).
    """
    nmax = len(occ)
    order = get_field(bits, ORDER)
    pull = get_field(bits, PULL)
    push = get_field(bits, PUSH)
    rule = get_field(bits, RULE)

    targets: dict[int, list[tuple[int, int]]] = {
        t: [] for t in range(nmax) if occ[t]
    }
    # pull edge: target t is transformed by s = pull[t]
    # An address >= nmax (possible only when nmax < 256) names no slot, so it
    # behaves like an empty slot: no edge.
    for t in np.where(occ)[0]:
        s = int(pull[t])
        if s < nmax and occ[s]:
            targets[t].append((int(order[s]), s))
    # push edge: source s transforms t = push[s]
    for s in np.where(occ)[0]:
        t = int(push[s])
        if t < nmax and occ[t]:
            targets[t].append((int(order[s]), s))
    for t in targets:
        targets[t].sort(key=lambda inst: (inst[0], inst[1]))
    return targets, rule


def compose_apply(bits: np.ndarray, targets, rule) -> np.ndarray:
    """Apply each target's composed transformation. Empty targets unchanged.

    For B.order < D.order < C.order the result is C(D(B(A))): the lowest
    order is applied first (innermost). Everything reads from `bits` (the
    snapshot), so the update is synchronous.
    """
    new = bits.copy()
    for t, insts in targets.items():
        if not insts:
            continue
        cur = bits[t]
        for _order, s in insts:
            cur = apply_rule(int(rule[s]), cur)
        new[t] = cur
    return new


@dataclass
class Metrics:
    tick: int
    population: int
    births: int
    deaths: int
    ambient_mutations: int
    activity: int            # total bits changed by transformations
    unique_genotypes: int
    rule_diversity: int      # distinct RULE values among occupied rings
    mean_mut_level: float

    def as_dict(self) -> dict:
        return self.__dict__.copy()

    def summary(self) -> str:
        return (
            f"t={self.tick:>5}  pop={self.population:>3}  "
            f"births={self.births:>3}  deaths={self.deaths:>3}  "
            f"amb={self.ambient_mutations:>3}  act={self.activity:>5}  "
            f"uniq={self.unique_genotypes:>3}  rules={self.rule_diversity:>3}  "
            f"mut={self.mean_mut_level:.2f}"
        )


@dataclass
class Universe:
    """The ring universe and its tick dynamics."""

    nmax: int = 256
    seed: int = 0
    record_history: bool = True
    # --- experimental knobs (defaults reproduce the faithful spec) ---------
    mut_scale: float = 1.0          # multiplies both mutation tables; 0 = off
    protect: tuple = ()             # field spans (lo, hi) held fixed under
                                    # transformation (heredity experiment, H1)
    transform_off: bool = False     # skip the transformation step entirely
                                    # (drift-only control: birth/death/mutation)
    # H2: gate reproduction/death on a heritable multi-bit key. The key is the
    # 4-bit slice `key_span` (low nibble of ORDER by default). When a code is
    # set, the event fires only if the ring's key equals it (in addition to the
    # spawn/death bit). None = ungated (faithful single-bit behaviour).
    spawn_code: int | None = None
    death_code: int | None = None
    key_span: tuple = (28, 32)

    bits: np.ndarray = field(init=False)
    occupied: np.ndarray = field(init=False)
    tick_count: int = field(init=False, default=0)
    history_bits: list = field(init=False, default_factory=list)
    history_occ: list = field(init=False, default_factory=list)
    history_ids: list = field(init=False, default_factory=list)

    def __post_init__(self):
        self.rng = np.random.default_rng(self.seed)
        self.bits = np.zeros((self.nmax, N_BITS), dtype=np.uint8)
        self.occupied = np.zeros(self.nmax, dtype=bool)
        # per-ring identity for lineage tracking (0 = empty slot)
        self.ids = np.zeros(self.nmax, dtype=np.int64)
        self.next_id = 1
        self.births_log: list[tuple[int, int, int]] = []  # (tick, child, parent)
        # boolean mask of protected bit positions
        if self.protect:
            m = np.zeros(N_BITS, dtype=bool)
            for lo, hi in self.protect:
                m[lo:hi] = True
            self._protect_mask = m
        else:
            self._protect_mask = None

    # -- seeding -----------------------------------------------------------
    def seed_random(self, n: int):
        """Place `n` random rings in random distinct slots."""
        slots = self.rng.choice(self.nmax, size=n, replace=False)
        self.bits[slots] = self.rng.integers(0, 2, size=(n, N_BITS), dtype=np.uint8)
        self.occupied[slots] = True
        for s in slots:
            self.ids[s] = self.next_id
            self.next_id += 1
        self._snapshot()

    def place(self, slot: int, row: np.ndarray):
        """Place a specific ring (for tests / hand-built universes)."""
        self.bits[slot] = np.asarray(row, dtype=np.uint8)
        self.occupied[slot] = True
        self.ids[slot] = self.next_id
        self.next_id += 1

    def _snapshot(self):
        if self.record_history:
            self.history_bits.append(self.bits.copy())
            self.history_occ.append(self.occupied.copy())
            self.history_ids.append(self.ids.copy())

    # -- the tick cycle ----------------------------------------------------
    def step(self) -> Metrics:
        bits0 = self.bits
        occ0 = self.occupied

        new_tick = self.tick_count + 1

        # 2-3. transform (synchronous, from the snapshot)
        if self.transform_off:
            bits1 = bits0.copy()
        else:
            targets, rule = build_transformers(bits0, occ0)
            bits1 = compose_apply(bits0, targets, rule)
        # H1: hold protected fields fixed under transformation (empties are 0
        # in both arrays, so a blanket restore is safe).
        if self._protect_mask is not None:
            bits1[:, self._protect_mask] = bits0[:, self._protect_mask]
        activity = int(np.sum(bits1[occ0] != bits0[occ0]))

        occ1 = occ0.copy()

        # 4. births (from S0 spawn bits) -- before deaths, into S0-empty slots
        spawn = (bits0[:, SPAWN_BIT] == 1) & occ0
        if self.spawn_code is not None:
            spawn &= get_field(bits0, self.key_span) == self.spawn_code
        empty_pool = np.where(~occ0)[0].copy()
        self.rng.shuffle(empty_pool)
        ptr = 0
        births = 0
        newborns: list[int] = []
        for s in np.where(spawn)[0]:
            if ptr >= len(empty_pool):
                break
            slot = int(empty_pool[ptr]); ptr += 1
            child = bits0[s].copy()
            p = BIRTH_P[mut_level(bits0[s])] * self.mut_scale
            child ^= (self.rng.random(N_BITS) < p).astype(np.uint8)
            bits1[slot] = child
            occ1[slot] = True
            newborns.append(slot)
            births += 1
            # lineage: child inherits a fresh id, parent is slot s
            self.ids[slot] = self.next_id
            self.births_log.append((new_tick, self.next_id, int(self.ids[s])))
            self.next_id += 1

        # 5. deaths (from S0 death bits)
        death = (bits0[:, DEATH_BIT] == 1) & occ0
        if self.death_code is not None:
            death &= get_field(bits0, self.key_span) == self.death_code
        deaths = int(np.sum(death))
        for d in np.where(death)[0]:
            occ1[d] = False
            bits1[d] = 0
            self.ids[d] = 0

        # 6. ambient mutation on survivors present at tick start (not newborns)
        survivors = occ1.copy()
        survivors[newborns] = False
        amb = 0
        for idx in np.where(survivors)[0]:
            p = AMBIENT_P[mut_level(bits1[idx])] * self.mut_scale
            flips = self.rng.random(N_BITS) < p
            if flips.any():
                bits1[idx] ^= flips.astype(np.uint8)
                amb += 1

        self.bits = bits1
        self.occupied = occ1
        self.tick_count += 1
        self._snapshot()

        return self._metrics(births, deaths, amb, activity)

    def _metrics(self, births, deaths, amb, activity) -> Metrics:
        occ = self.occupied
        pop = int(occ.sum())
        if pop:
            rows = self.bits[occ]
            unique = int(np.unique(rows, axis=0).shape[0])
            rules = int(np.unique(get_field(rows, RULE)).shape[0])
            mut = float(np.mean([mut_level(r) for r in rows]))
        else:
            unique = rules = 0
            mut = 0.0
        return Metrics(self.tick_count, pop, births, deaths, amb,
                       activity, unique, rules, mut)

    # -- driver ------------------------------------------------------------
    def run(self, ticks: int, logger: "Logger | None" = None,
            print_every: int = 0):
        """Run up to `ticks` steps; stop early on extinction."""
        results = [self._metrics(0, 0, 0, 0)]  # tick 0 (initial)
        for _ in range(ticks):
            m = self.step()
            results.append(m)
            if logger:
                logger.log(m)
            if print_every and m.tick % print_every == 0:
                print(m.summary())
            if m.population == 0:
                if print_every:
                    print(f"extinct at t={m.tick}")
                break
        return results

    def save_history(self, path: str):
        """Save the recorded state history for the viewer (.npz)."""
        if not self.history_bits:
            raise RuntimeError("no history recorded (record_history=False)")
        births = (np.array(self.births_log, dtype=np.int64)
                  if self.births_log else np.zeros((0, 3), dtype=np.int64))
        np.savez_compressed(
            path,
            bits=np.stack(self.history_bits),
            occ=np.stack(self.history_occ),
            ids=np.stack(self.history_ids),
            births=births,
        )


class Logger:
    """Append per-tick metrics to a JSONL file (and keep them in memory)."""

    def __init__(self, path: str):
        self.path = path
        self._fh = open(path, "w")
        self.records: list[dict] = []

    def log(self, m: Metrics):
        d = m.as_dict()
        self.records.append(d)
        self._fh.write(json.dumps(d) + "\n")
        self._fh.flush()

    def close(self):
        self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
