# NOTES --- Adaptive Ring System

Running log of observations and decisions made during **implementation** (the
E1 era). This is a historical log, kept for the record; the "First runs"
interpretation below describes the faithful-spec baseline, which later work
(`EXPERIMENTS.md`, `REPORT.md`) characterises as high-entropy churn rather than
organization. For the current picture read `REPORT.md`; for the path tree read
`TRAJECTORY.md`.

## Implementation

- Built in the order set out in `DESIGN.md` section 7: ECA core -> edges /
  composition -> tick cycle -> mutation -> viewer. Each layer tested before
  the next.
- Two bugs caught by tests during the build:
  1. `mut_level` indexed the MUTATION field's *exclusive* upper bound (36)
     instead of the second bit (35). Fixed.
  2. An 8-bit address can point past `nmax` when `nmax < 256` (only in
     small test universes; never at the real Nmax=256). `build_transformers`
     now treats an out-of-range address as an empty slot (no edge), which is
     consistent with the empty-slot semantics.
- Lesson for testing the transformation semantics: do **not** go through
  `step()`, because ambient mutation is never zero and adds bit noise, and a
  default address of 0 creates an unintended self-edge. The edge/composition
  tests call `build_transformers` + `compose_apply` directly on hand-built
  universes instead.

## First runs (seed 0, init 16, 400 ticks)

Observation (measured):
- Population rises from 16 and self-stabilises around 150--185 of 256.
- Births and deaths both run ~70--110 per tick: high, balanced turnover.
- Unique genotypes ~140--175; distinct RULE values ~70--95.
- Mean mutation level hovers ~1.5--1.8 (of 0--3), i.e. the population does
  not collapse to the lowest mutation rate.

Interpretation:
- The system sits in a non-degenerate regime --- neither the freeze
  (all-empty / all-static) nor the saturation (all-full) failure mode I
  flagged as the main risk in `DESIGN.md`. The hard cap plus contestable,
  one-tick-latency death appears to be enough to sustain churn without
  external selection.

Caveat / not yet tested:
- This is a single seed. Robustness across seeds and initial conditions
  (notably `--init 1`, a single ancestor) is not yet characterised.
- "Diversity stays high" is a genotype count, not evidence of *adaptation* or
  any selected structure. Whether anything heritable and functional emerges
  (the autopoiesis / open-ended-search targets) is an open question that
  these metrics do not answer. Would need lineage tracking and
  structure-level probes.

## Possible next steps (not done)

- Lineage / ancestry tracking to ask whether persistent "species" form.
- Sweep mutation-rate tables and initial conditions; characterise the regime
  boundaries (where it does freeze or saturate).
- A fixed-slot genome raster (current viewer restacks occupied rings each
  frame, which flickers).
