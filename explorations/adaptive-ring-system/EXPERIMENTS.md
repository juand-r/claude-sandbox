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

---

## E2 --- Conditional reproduction on a heritable key (H2)

### Design

Reproduction (and death) are gated on a 4-bit **key** --- the low nibble of
the ORDER field. A ring reproduces only if its spawn bit is set *and*
`key == spawn_code`; it dies only if its death bit is set *and*
`key == death_code`, with `spawn_code = 15` and `death_code = 0` (different, so
key-15 rings reproduce and never die, key-0 rings die and never reproduce, the
other 14 keys persist statically). Gating both events keeps birth and death
rates commensurate; gating spawn alone drove the population to ~3 (deaths far
outran the 1/16-throttled births).

Heredity of the key is the variable under test, set by which bits
transformation may overwrite:

| name           | protection          | key heritable? |
|----------------|---------------------|----------------|
| h2_protected   | whole core (0--31)  | yes            |
| h2_key_only    | key bits (28--31)   | yes            |
| h2_unprotected | none                | no (control)   |

Selection signal: the share of living rings with `key == spawn_code` (chance =
1/16 = 0.0625). Reusing ORDER's low nibble as the key mildly conflates
composition rank with reproduction eligibility; a dedicated field would remove
this, deferred until the mechanism is shown to matter.

### Prediction

If a heritable trigger enables selection, the key-15 share rises above chance
when the key is heritable (h2_protected, h2_key_only) and stays at chance when
it is not (h2_unprotected).

### Observation

| config         |   pop | turnover | concentration | key share (start->end) |
|----------------|------:|---------:|--------------:|------------------------:|
| h2_protected   |  10.8 |    0.001 |         0.093 |        0.062 -> 0.100   |
| h2_key_only    | 239.2 |    0.008 |         0.107 |        0.062 -> 0.098   |
| h2_unprotected | 248.8 |    0.011 |         0.883 |        0.062 -> 0.000   |

Key-15 end share across 5 seeds:

- **h2_key_only:** 0.098, 0.082, 0.094, 0.110, 0.103 (mean ~0.097, all above
  chance, tight).
- **h2_unprotected:** 0.000, 0.012, 0.074, 0.258, 0.000 (mean ~0.069 ~ chance,
  high variance).

### Interpretation

- **A heritable trigger produces real selection.** Whenever the key is
  heritable, its share rises consistently to ~1.5x chance and clusters
  tightly across seeds. The non-heritable control scatters around chance ---
  its occasional spikes (seed 3: 0.258) are clonal flukes, not selection.
  This is the first signal in this system of selection acting beyond neutral
  drift, and it is cleanly attributable to **heredity**, since the trigger is
  identical in all three configs and only protection differs.
- **The core tension: transformation is both the engine of activity and the
  destroyer of heredity.** Protecting the whole core makes the key heritable
  but freezes the population to near-extinction (pop 10.8): with RULE fixed,
  the spawn bit stops being toggled and reproduction stalls. No protection
  keeps the system lively but lets transformation scramble the key every tick,
  so selection cannot accumulate (and a limit-cycle clone takes over instead
  --- concentration 0.88 with key share 0). Only **surgical** protection of
  the key alone (h2_key_only) escapes the dilemma: a lively population
  (pop 239) *and* a heritable, selectable tag.
- **Effect size is throttled by saturation.** Enrichment stops near 0.10, not
  1.0, because the universe fills with immortal non-reproducing keys (1--14)
  and key-15 rings can only reproduce into the few slots freed by key-0
  deaths. Selection is real but slot-limited.

### Takeaway

H2 is confirmed in principle: conditioning reproduction on a *heritable* key
yields replicable selection (key-only protection, +~55% over chance across 5
seeds), where the faithful baseline showed none. The decisive ingredient is
heredity, achieved by protecting only the key so transformation stays lively
elsewhere.

### What this points to next

Selection works but is weak because the population saturates with static
non-reproducers, starving selection of free slots. The next lever (H2c) is a
**turnover mechanism** that frees slots without crashing the population ---
e.g. a low uniform death rate, or making the non-reproducing keys mortal ---
so selection can keep operating. Separately, replacing the ORDER-nibble key
with a dedicated field would remove the rank/reproduction conflation before
pushing further.
