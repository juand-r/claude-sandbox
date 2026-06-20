# Trajectory --- the tree of explored paths

A living map of the research program. The detailed per-experiment record is in
`EXPERIMENTS.md`; the argument-level synthesis is in `REPORT.md`; this file
tracks **structure**: which paths were taken, why, what they led to, and what
remains open. Reflection rounds are interleaved (every few milestones).

Legend: [done] result in EXPERIMENTS.md | [open] not yet run | [dead] tried,
not fruitful | [branch] spawned sub-paths.

## Trunk so far

- **E1** [done] Baseline is high-entropy churn; no unit of heredity.
- **E2** [done] Heritable trigger -> real but fragile selection. Heredity is
  the enabler.
- **E3** [done] Turnover strengthens selection but substrate too fragile to
  fixate (extinction-prone).
- **E4** [done] Local addressing + heritable rule -> emergent spatial domains
  (Moran ~0.28). First emergent structure.
- **E5** [done] Domains form a dynamic coexisting ecology; but NOT autopoietic
  (invasion test: competitive dominance / passive coexistence).
- **E6** [done] Self-templating -> heredity-compatibility EMERGES (self-pres
  0.52->~1.0, no protection). But limited: frozen clone (mixed) or
  unstructured (local). Gap: individual heredity != collective/spatial.

- **R1** [reflection] **Metric error found.** Moran's I (ordinal) was wrong for
  categorical rule fields and produced a confident false negative for two
  experiments. Switched to neighbour-identity. Overturns E6's conclusion:
  E6-local DOES form emergent genome domains (~16x chance), nothing protected.
- **E7** [done][B1] Templating onto neighbour (overwrite) + local_range.
  Confirms (does not create) E6; isolates self-templating as the mechanism.
  Overwrite alone ~2x, with self-template ~16x.

## Central open problem (UPDATED after R1)

~~Bridge emergent heredity with emergent spatial structure~~ --- **solved at
E6** (they are the same phenomenon, seen with the right metric). New central
question: are the emergent genome domains **self-maintaining** (autopoietic),
or dynamic clusters churned by long-range transformers? And does anything
**open-ended** (sustained novelty) ever arise, or only fixed regimes?

## Active branches (the tree from here)

- **B1 --- neighbourhood agreement (E7+).** Templating onto the neighbour:
  spread one's genome into the neighbourhood so neighbours share a rule. The
  direct attack on the central problem.
- **B2 --- emergent heredity + selection.** Combine self-templating with the
  key trigger / turnover: does emergent heredity make selection robust where
  E3 failed?
- **B3 --- coevolution / frequency dependence.** Make fitness depend on others
  (predation, rock-paper-scissors among rules) to seek non-trivial,
  non-frozen attractors (ecologies that don't collapse).
- **B4 --- open-endedness measurement.** Information/complexity growth over
  long runs; do we ever get sustained novelty vs. a fixed point?
- **B5 --- substrate variations.** Grid size, neighbourhood, N, address range,
  rule-space biasing (ordered rules), genome length. Robustness + regime maps.
- **B6 --- functional reproduction variants.** Other achievable functional
  conditions besides self-consistency (e.g. successfully copying a neighbour;
  surviving N ticks; network participation / death-by-isolation).

## Log of moves

(newest first; each entry: which branch, what was tried, outcome pointer)

- E13 [B4] next: complexity-over-time -- does anything COMPLEXIFY, or just roam
  the self-consistent manifold? (compressibility/entropy of genomes vs time)
- E12 [B4] [done] open-endedness RESOLVED: selftmpl_local novelty plateaus at
  ~0.18 (flat slope over 4000t), cumulative diversity unbounded -> sustainably
  open-ended, not freezing. EXPERIMENTS.md E12.
- E11 [B3] [done] cyclic dominance -> robust 3-way coexistence but NO spirals
  (types have unequal viability, breaks RPS symmetry). Scales to 64x64.
  EXPERIMENTS.md E11.
- E10 [B2] [done] emergent heredity unlocks ROBUST adaptation: key-gate drives
  trait 0.06 -> 0.75 (vs 0.11 imposed, vs extinction in E3). Full chain
  persistence->heredity->adaptation now holds on emergent heredity.
  EXPERIMENTS.md E10.
- R2 [reflection] [done] phase-diagram of regimes; selftmpl_local is the
  richest (structured sustained novelty). Frontier = open-endedness, adaptation,
  autopoiesis-of-dynamic-domains. EXPERIMENTS.md R2.
- E9 [B4] [done] open-endedness: selftmpl_local = sustained structured novelty
  (sweet spot); mixed freezes; baseline = noise. EXPERIMENTS.md E9.
- E8 [B1/B5] [done] local_range sweep: emergent domains are DYNAMIC (flip-rate
  >=0.27 everywhere), not static; no clean short-range stabilization.
  EXPERIMENTS.md E8.
- E7 [B1] [done] overwrite + local_range. Self-templating is the active
  ingredient; overwrite mostly adds turnover. EXPERIMENTS.md E7.
- R1 [reflection] [done] metric correction (Moran -> neighbour-identity);
  overturns E6 "unstructured" -> E6 has ~16x genome domains. EXPERIMENTS.md R1.
- E7-pre [B1] templating onto neighbour -- led to R1.
