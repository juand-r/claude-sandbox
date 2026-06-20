# Adaptive Ring System --- Design & Implementation Plan

Status: **implemented and signed off.** This document specifies the **faithful
spec** --- the system as originally agreed. The simulator (`ring_system.py`)
implements exactly this when all experimental knobs are at their defaults; the
research that followed layers *modifications* on top (see section 10 and
`EXPERIMENTS.md`). Read this for the base mechanics; read `REPORT.md` for what
the modified variants do.

The original specification was provided by the project owner in conversation at
the start of the project (there is no separate spec file --- **this document is
its authoritative written capture**). Where the original was silent or
ambiguous, the resolution and its rationale are recorded here so the decision is
easy to revisit later. The defining requirements from the original spec were:
36-bit rings that are at once data / CA-rule / network-node; transformation by
elementary CA rule; pull/push wiring; order composition; reproduction, mutation,
death under a hard cap; the "Minimal Philosophy" (no controller, fitness,
energy, or separate memory); and "zero mutation does not exist."

---

## 1. Purpose and scope

A finite universe of self-modifying "rings." Each ring is simultaneously
data, a transformation rule, and a node in a transformation network. There
is no controller, no fitness function, no energy variable, no separate
memory. All behavior emerges from rings transforming one another and
themselves, plus reproduction, mutation, and death under a hard population
cap.

We are building a faithful, minimal simulator of this system and some basic
instrumentation to watch what it does. We are explicitly **not** adding any
external selection or control machinery (per the spec's "Minimal
Philosophy").

---

## 2. Ring structure

Each ring is exactly **36 bits**, laid out as:

```
RULE | PULL | PUSH | ORDER | SPAWN | DEATH | MUTATION
  8     8      8      8       1       1        2
```

Bit-index layout (positions 0..35, lowest index = most significant bit
within each field):

| field    | bits  | meaning                                            |
|----------|-------|----------------------------------------------------|
| RULE     | 0–7   | an 8-bit elementary CA rule (Wolfram rule number)  |
| PULL     | 8–15  | address of the ring that transforms me             |
| PUSH     | 16–23 | address of the ring I transform                    |
| ORDER    | 24–31 | composition rank when several rings hit one target |
| SPAWN    | 32    | reproduce this tick                                |
| DEATH    | 33    | die this tick                                      |
| MUTATION | 34–35 | mutation-rate level (00/01/10/11)                  |

A ring's **address is not stored** in the ring; it is the slot it occupies.

---

## 3. Core semantics

### 3.1 Rings are circular bitstrings

The 36 bits form a **ring** (circular): bit 0's left neighbor is bit 35, and
bit 35's right neighbor is bit 0. The CA rule is interpreted over this
circular string. Field boundaries are irrelevant to the CA --- a
transformation can alter any field, including RULE, PULL, PUSH, DEATH, etc.
That is the point: rings rewrite each other's genotypes wholesale.

### 3.2 What "B transforms A" means

B's RULE (read as a Wolfram rule number 0–255) is applied **once across A's
36 circular bits**, standard elementary-CA convention:

```
for each position i in A:
    left   = A[(i-1) mod 36]
    center = A[i]
    right  = A[(i+1) mod 36]
    idx    = 4*left + 2*center + 1*right        # 0..7
    A'[i]  = (B.RULE >> idx) & 1
```

All output bits are computed from the **input** A (a single synchronous CA
step), not in place.

### 3.3 Pull / push edges (multiset, no dedup)

Each ring declares its own two edges:

- `PULL`  = "who transforms me"
- `PUSH`  = "who I transform"

The transformers acting on a target T are a **multiset**: one instance per
ring `s` with `s.PUSH == addr(T)`, **plus** one instance per ring `s` with
`T.PULL == addr(s)`. These are **not** deduplicated. If `A.PUSH == B` and
`B.PULL == A`, then A transforms B **twice**: `B' = A(A(B))`.

### 3.4 Order composition

When several transformer instances target one ring, sort them **ascending by
the transformer's ORDER field**, then apply **lowest-order first as the
innermost function**:

```
B.order < D.order < C.order   ⟹   A' = C(D(B(A)))
```

Ties (equal ORDER) are broken by **ascending slot address**. Two instances
of the same transformer (from the push+pull case) land adjacent and identical,
so their relative order is moot.

### 3.5 Self-application

A ring may address itself (`PULL == own addr` and/or `PUSH == own addr`). A
self-transformation participates in the ordered composition like any other,
ranked by the ring's own ORDER. If both self-edges are set, the ring applies
its rule to itself twice: `A' = A(A(A))`.

### 3.6 Empty slots

- **Push to empty:** no-op (the target does not exist).
- **Pull from empty:** identity (`A' = A`); contributes no transformer
  instance.

Both fall out naturally because we only ever build transformer instances
from **occupied** slots.

### 3.7 Addressing modes --- IS THE GRID REAL? (important)

PULL/PUSH are 8-bit numbers, but there are **two ways to interpret them**, and
they give completely different topologies. This is the single most important
thing to be clear about when reading any spatial claim.

- **Absolute addressing (the faithful spec; default `local_addr=False`).**
  PULL/PUSH are *absolute slot indices* 0..255. A ring addresses slot #173
  wherever #173 is. There is **no geometry**: the universe is a set of 256
  labelled slots wired arbitrarily to one another. The 16x16 grid drawn by the
  viewer is **pure visual convenience** (slot = row*16 + col); two cells
  adjacent in the picture are *not* neighbours in any dynamical sense. Births
  go to a **uniformly random empty slot**. Faithful-spec runs (the E1 baseline)
  use this mode, and they correctly look like spatial noise.

- **Local addressing (the H4 modification; `local_addr=True`).** PULL/PUSH are
  reinterpreted as signed **(dx, dy) offsets on a 2-D torus** of side
  `sqrt(nmax)` (16 for nmax=256). A ring at (x, y) is transformed by the ring
  at (x+dx, y+dy); each nibble maps to `-local_range .. +local_range`. Now the
  grid is **real space** --- Euclidean adjacency is the actual interaction
  topology --- so domains, fronts and "spirals" are genuine spatial structure,
  not display artifacts. Births go to an **empty Moore-neighbour** of the
  parent (local reproduction). Every spatial result in `EXPERIMENTS.md` (E4
  onward) uses this mode.

Two details that are easy to miss:

- **Birth radius and transformation range are decoupled.** Local births are
  always to the immediate Moore neighbourhood (radius 1). `local_range` controls
  only how far PULL/PUSH *transformation* reaches; with the default 8 on a
  16-wide torus, "local" transformation can reach halfway across, so it is only
  loosely local until `local_range` is made small (E7/E8).
- **Two different "circular" things.** The 36-bit genome is a *ring* (circular
  bitstring) for the CA; the universe is (under local addressing) a *torus*.
  These are unrelated wrap-arounds.

The dashboard's "local addressing (H4)" checkbox toggles between these modes,
which is a direct demonstration that the grid is cosmetic in one mode and real
in the other: the same render shows noise with it off and domains with it on.

---

## 4. Tick cycle

All per-tick decisions read a **start-of-tick snapshot `S0`**. This gives
death and birth a **one-tick latency**: a transformation that sets a ring's
death (or spawn) bit takes effect on the *next* tick, not the tick it was
set.

Per tick:

1. **Snapshot** the universe as `S0` (bits + occupancy).
2. **Determine transformations** for every occupied target, from `S0`
   (section 3.3), as ordered multisets (section 3.4).
3. **Compose** each target's transformers (section 3.4) and **apply
   updates** synchronously: every target's new bits are computed from `S0`,
   then written together to produce `S1`. (A ring that will die this tick
   still acts as a transformer on others, since it was alive at tick start.)
4. **Resolve births** (from `S0.SPAWN`): each spawning ring, if an empty slot
   exists, places a **mutated copy of its `S0` bits** (birth mutation,
   section 5) into a **uniformly random empty slot**. Births are resolved
   **before** deaths, so a ring's death never cancels its reproduction.
5. **Resolve deaths** (from `S0.DEATH`): each dying ring's slot becomes empty.
6. **Ambient mutation** (section 5) on the surviving rings.

### Rationale for the snapshot / latency choice

The system has no controller; transformations are the *only* control
mechanism. Reading death/birth from `S0` makes a death sentence
**contestable within the tick**: several rings transform A's death bit, and
only the *net* value at the next snapshot decides A's fate. Death becomes the
outcome of the transformation war over that bit (with one tick of latency),
rather than an instant same-tick execution. This fits the "rings fight it
out" spirit better than an immediate kill.

### Documented consequence (vetoable)

Because births resolve before deaths, newborns this tick can only occupy
slots that were **empty at tick start**; slots freed by this tick's deaths
become available **next** tick. Near full capacity this slightly throttles
turnover. Accepted for now to honor "birth before death."

---

## 5. Mutation

Two independent mutation events, both **per-bit independent flips**, both
keyed by the 2-bit MUTATION field, all rates nonzero ("zero mutation does not
exist"). All values tunable.

| field      | ambient p (per ring, per tick) | birth p (per child bit, once) |
|------------|--------------------------------|-------------------------------|
| 00 rare    | 0.0005                         | 0.005                         |
| 01 low     | 0.002                          | 0.02                          |
| 10 medium  | 0.01                           | 0.05                          |
| 11 high    | 0.05                           | 0.15                          |

- **Ambient mutation** uses **each ring's own** MUTATION field (section 4,
  step 6).
- **Birth mutation** uses the **parent's** MUTATION field, applied once to
  the child's copied bits (section 4, step 4).
- "Per-bit independent flip with probability p" means each of the 36 bits is
  flipped independently. Because the MUTATION field is part of the 36 bits,
  the mutation rate can itself mutate.

---

## 6. Universe parameters

- `Nmax = 256`, so the 8-bit PULL/PUSH addresses map **1:1** to slots --- no
  modulo, no truncation.
- **Initial condition: deferred.** Decided at run time --- one ring or
  several. Implemented as a parameter (count + RNG seed); random 36-bit rings
  by default.
- RNG is seeded for reproducibility; the only nondeterminism is mutation and
  random child placement.

---

## 7. Implementation plan

Language: **Python + NumPy** (CA sweep and bit ops are natural and fast on
arrays). Kept deliberately small.

Files under `explorations/adaptive-ring-system/`:

- `DESIGN.md` --- this document.
- `ring_system.py` --- the simulator (one module):
  - bit-field get/set helpers (section 2 layout),
  - `apply_rule(rule, bits)` --- one circular ECA step (section 3.2),
  - `build_transformers(snapshot)` --- multiset edges (3.3),
  - `compose_and_apply(snapshot)` --- ordered composition + synchronous
    write (3.4, step 3),
  - `resolve_births`, `resolve_deaths`, `ambient_mutate` (sections 4–5),
  - `tick(state, rng)` --- the full cycle (section 4),
  - `seed(n, rng)` and a small `Universe` container,
  - metrics: population, unique genotypes, rule diversity, per-tick activity
    (bits changed).
- `run.py` --- a thin demo: build a universe, run N ticks, print/plot basic
  metrics. (Plotting optional; start with printed stats.)
- `NOTES.md` --- running log of observations, surprises, and any course
  corrections (per repo process rules).
- `README.md` --- 1–2 line summary + how to run.

Build order (each step verified before the next):

1. Bit-field helpers + `apply_rule`, with **unit tests** against a known
   elementary CA (e.g. rule 110 / rule 30 on a small circular string).
2. Transformer construction + composition, with tests for: pull-from-empty =
   identity, push-to-empty = no-op, the `A(A(B))` double-apply case, and
   ORDER/tie-break correctness.
3. Full tick cycle, with tests for: synchronous update, one-tick death/birth
   latency, birth-before-death (both bits set → child created then parent
   dies), random placement into empty slots only.
4. Mutation, with a statistical sanity test (observed flip frequency ≈ table
   rate over many trials).
5. `run.py` + metrics; a first exploratory run; record observations in
   `NOTES.md`.

Testing philosophy: real tests of the semantics above --- no placeholder
assertions. CA correctness and the tick-ordering invariants are the
load-bearing parts.

---

## 8. Explicitly out of scope

Per the spec's Minimal Philosophy, we are **not** adding: a controller, a
fitness function, an energy variable, or separate memory. The starting
ingredients are exactly: state + transformation + reproduction + mutation +
deletion.

---

## 9. Open items for sign-off

1. The mutation rate tables (section 5) --- magnitudes are guesses; fine to
   tune after first runs.
2. The near-capacity turnover consequence (section 4) --- accepted to honor
   birth-before-death; flag if you'd rather free death slots first.
3. Everything else above is considered settled per our discussion.

---

## 10. Experimental modifications (beyond the faithful spec)

**Important:** sections 1--8 describe the faithful spec. The research program
(`EXPERIMENTS.md`, `REPORT.md`) studies *modified* variants, switched on by the
knobs below. **All knobs default to values that reproduce the faithful spec**,
so `Universe()` with no arguments is the spec. Only the **E1 baseline** is the
faithful spec; **every later result uses one or more of these modifications** ---
do not read E4+ findings as properties of the original system.

| knob | default (= faithful) | what it changes | first used |
|------|----------------------|-----------------|-----------|
| `mut_scale` | 1.0 | scales both mutation tables; 0 disables mutation | E1 (mut_off) |
| `protect` | () | field spans held fixed under transformation (imposed heredity) | E1 (H1) |
| `transform_off` | False | skip the transformation step (drift-only control) | E1 |
| `spawn_code` / `death_code` | None | gate reproduction/death on a heritable key (`key_span`, default ORDER's low nibble) | E2 (H2) |
| `base_death` | 0.0 | extra uniform per-tick death probability (tunable turnover) | E3 (H2c) |
| `local_addr` | False | **addressing mode** (section 3.7): absolute -> local 2-D torus | E4 (H4) |
| `local_range` | 8 | max |offset| for local PULL/PUSH (small = truly short-range) | E7 |
| `self_template` / `self_template_power` | False / 2.0 | gate reproduction on self-consistency (emergent heredity) | E6 |
| `overwrite_birth` | False | child overwrites a Moore neighbour (spreads genome) | E7 |
| `cyclic_dominance` | False | overwrite only a type it beats (rule%3 rock-paper-scissors) | E11 |

Deviations from the *letter* of the faithful spec worth flagging explicitly:

- **`mut_scale=0` violates "zero mutation does not exist"** --- used only as a
  control, never as a claimed faithful run.
- **The reproduction key reuses ORDER's low nibble** (`key_span=(28,32)`),
  mildly conflating composition rank with reproduction eligibility. A dedicated
  field would remove this; deferred (see E2).
- **Lineage tracking** (per-ring ids, birth records) is always on but is pure
  instrumentation --- it does not affect dynamics.
- **Ambient mutation skips this-tick newborns** (a one-tick grace), a small
  implementation choice not in the spec text; immaterial to results.

The interactive dashboard (`artifact.html`) exposes the most important knobs
(mutations on/off + scale, protect, transform-off, H2 trigger, local
addressing, self-templating) as live toggles; a few engine-only knobs
(`overwrite_birth`, `cyclic_dominance`, `local_range`) are not in the UI.
