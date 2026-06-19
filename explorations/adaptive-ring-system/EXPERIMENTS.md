# Experiments Log

Each entry: configuration, prediction, observation, interpretation. Observation
and interpretation are kept visibly separate (per repo report guidelines).
All runs single-seed (seed 0, init 16, 256 slots, 400 ticks) unless noted ---
treat magnitudes as indicative, not precise, until replicated across seeds.

Reproduce with: `python3 experiments.py --ticks 400 --init 16 --seed 0`

---

## E1 --- Baseline characterization vs. controls

### Configurations

| name           | change from faithful spec                              |
|----------------|--------------------------------------------------------|
| baseline       | none (faithful)                                        |
| mut_off        | mutation disabled (`mut_scale=0`)                      |
| no_transform   | transformation step skipped (drift-only control)      |
| protect_core   | RULE+PULL+PUSH held fixed under transformation (H1)    |
| protect_lowmut | protect_core + mutation x0.3 (H1+H3)                   |

### Prediction (from RESEARCH_PLAN.md section 2)

The baseline is high-entropy churn with no stable unit of heredity: turnover
near one full population per tick, low genotype concentration (no replicator
takeover), founder fixation explained by drift rather than selection.

### Observation

| config         |   pop | turnover | concentration | persist(max) | compress |
|----------------|------:|---------:|--------------:|-------------:|---------:|
| baseline       | 169.1 |    1.002 |         0.086 |          146 |    0.858 |
| mut_off        | 146.0 |    1.535 |         0.769 |          385 |    0.044 |
| no_transform   | 252.9 |    0.014 |         0.050 |          330 |    0.887 |
| protect_core   | 212.3 |    0.432 |         0.139 |          120 |    0.925 |
| protect_lowmut | 243.4 |    0.098 |         0.173 |          310 |    0.499 |

(turnover = fraction of population replaced per tick; concentration =
top-genotype population share; persist = longest consecutive-tick run of any
genotype; compress = gzip size of the living population / same-shape random
matrix, <1 means structure.)

Push-graph (final tick): every transform-on config has a hub far above the
random functional-graph null (max in-degree 11--126 vs null ~5), but the
fraction of rings on a directed cycle is at or **below** the null (<=0.02 vs
~0.09). Founder share is 1.0 in every transform-on config (single founder
fixed); 0.50 across 6 founders in the drift-only control.

### Interpretation

- **The baseline is churn, as predicted.** Turnover ~1.0/tick means roughly
  the entire population is replaced each tick; concentration 0.086 means no
  genotype ever dominates. The earlier "high diversity" was high entropy, not
  organization. The lead hypothesis (birth/death are near-coin-flips driven by
  whoever transformed a ring, and identity is rewritten every tick) is
  supported.
- **Order is not adaptation.** Turning mutation *off* produces the most
  "order" by far --- one genotype fills 77% of the population, compressibility
  collapses to 0.044 --- but this is a single clonal attractor (a replicator
  flooding the universe), not open-ended adaptation. A metric like
  concentration or compressibility alone would have called this a success; it
  is a trap.
- **The drift-only control freezes.** With transformation off the universe
  fills to near-capacity and stops (turnover 0.014); many genotypes persist
  precisely because nothing changes them. This is the "frozen randomness"
  null --- diversity with no process.
- **Founder fixation is drift, not selection.** Single-founder takeover under
  turnover ~1.0 is the expected neutral outcome, so founder_share=1.0 is *not*
  evidence of adaptation. The drift control keeping 6 founders alive (it
  barely turns over) is consistent with this reading.
- **Network structure is hub-shaped, not loop-shaped.** Transformation
  reliably builds high-in-degree hubs (many rings pushing to one target) but
  *suppresses* directed cycles below chance. Autocatalytic loops --- the kind
  of mutual-maintenance structure autopoiesis would predict --- are not
  forming; if anything they are selected against.
- **H1/H3 partially stabilize but do not organize.** Protecting the core cuts
  turnover (1.0 -> 0.43) and adding low mutation cuts it further (-> 0.10)
  while raising structure (compress 0.50) and producing a strong hub
  (in-degree 56). But concentration stays low (0.17) and nothing resembling a
  selected, reproducing structure appears. Stability is necessary but not
  sufficient.

### Takeaway

Minimum bar met: the baseline is quantitatively churn, confirmed against a
random-matrix null (compressibility) and a drift-only null (no_transform).
The discriminating metrics cleanly separate four regimes --- churn
(baseline), clonal takeover (mut_off), freeze (no_transform), partial
stabilization (protect_*). No configuration yet shows adaptation (selection
beyond drift).

### What this points to next

The unaddressed bottleneck is **H2: birth and death are single post-transform
bits, i.e. coin flips decoupled from genotype.** Stabilizing identity (H1/H3)
without fixing this only buys a quieter soup. The next experiment should make
reproduction/death *conditional* on something a ring could come to "control"
(e.g. a multi-bit code, or a function of the ring's own state), so that
survival and reproduction can correlate with genotype and give selection
something to act on --- ideally combined with a protected heritable core.
