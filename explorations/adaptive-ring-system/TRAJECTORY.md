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

- B10/B11 next (LARGE departures): a composable primitive (replace ECA rules
  with a smoothly-composable instruction set) and/or endogenous escalating
  (coevolutionary) pressure -- the only routes left to open-ended complexity.
  Or deliberately accept the boundary. See R4.
- R4 [reflection] [done] complexity ceiling is REAL and 3-layered: passive cap
  (E13, removed by B7), active parsimony (E14), representational ruggedness of
  ECA-rule programs (E15). Deep cause = the ECA primitive. EXPERIMENTS.md R4.
- E15 [B8] [done] reward complexity via a task: length lifts 1->~2.5 then
  PLATEAUS (task-fit ~0.77); ECA-rule programs don't compose smoothly.
  EXPERIMENTS.md E15. growth.py (task support).
- E14 [B7] [done] genome growth: program length COLLAPSES to floor (parsimony);
  self-consistency selects against complexity. growth.py (new var-length module).
  EXPERIMENTS.md E14.
- R3 [reflection] [done] the arc (E1->E13) and the wall: heredity is the master
  key; novelty is open-ended but COMPLEXITY is not (plateaus). Next branches
  B7 (genome growth), B8 (changing environment), B9 (complexity metrics).
- E13 [B4] [done] complexity-over-time: all proxies PLATEAU by t~2000 ->
  open-ended in novelty (E12) but NOT in complexity. The substrate's ceiling.
  EXPERIMENTS.md E13.
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
