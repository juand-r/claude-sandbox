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

---

## E3 --- Turnover (H2c)

### Design

Add `base_death`, a uniform per-tick death probability applied to all existing
rings, on top of the h2_key_only heritable trigger. Sweep it and ask whether
selection on the key goes to fixation, and whether the population survives.
(seed 0--3, init 16, 500 ticks.)

### Observation

key-15 end share (final population in parentheses); chance = 0.0625:

| base_death | seed0 | seed1 | seed2 | seed3 |
|-----------:|------:|------:|------:|------:|
| 0.00       | 0.11 (256) | 0.08 (256) | 0.09 (256) | 0.11 (256) |
| 0.01       | 0.13 (254) | 0.19 (252) | 0.15 (253) | **0.00 (0)** |
| 0.02       | 0.17 (249) | 0.18 (251) | 0.18 (249) | **0.00 (0)** |
| 0.05       | **0.00 (0)** | 0.20 (246) | 0.26 (243) | **0.00 (0)** |
| 0.10       | **0.00 (0)** | 0.26 (235) | 0.34 (232) | **0.00 (0)** |

### Interpretation

- **Turnover does strengthen selection.** Where the population survives, more
  death raises key-15 enrichment monotonically, from ~1.6x chance at no extra
  death to ~5x (0.34) at base_death 0.10. The saturation diagnosis from E2 is
  confirmed: freeing slots lets selection keep acting.
- **But the substrate is too fragile to reach fixation.** No run approaches
  fixation (max 0.34 at 500 ticks), and higher death rates cause stochastic
  **extinction** (2 of 4 seeds at base_death >= 0.05). The reason is structural:
  reproduction requires a key-15 ring that *also* has its spawn bit toggled on
  by transformation *and* an empty slot --- a low, noisy rate. Early on, when
  key-15 is rare, that rate cannot cover a high uniform death rate, so the
  population death-spirals before selection can enrich it. Selection strength
  and viability are in direct tension.

### Takeaway

H2c confirms the mechanism (turnover -> stronger selection) but also a hard
limit: this substrate's reproduction is too weak and noisy to support robust,
sustained directional selection. Pushing turnover trades selection strength
for extinction risk. This reinforces that imposed-code selection is near its
useful ceiling here, and motivates changing the *kind* of dynamics rather than
tuning this one further.

---

## E4 --- Spatial self-organization (H4)

### Motivation

E2/E3 produced *selection*, but the H2 trigger names the winner in advance, so
its success is partly built in. This experiment seeks structure that is
**emergent** --- not named in the rules --- and visually legible.

### Design

Two changes turn the non-spatial slot census into an actual space (the 16x16
torus the dashboard already draws):

1. **Local addressing** (`local_addr`): PULL/PUSH are read as signed (dx, dy)
   offsets (each -8..7) instead of absolute slot indices, so a ring interacts
   with nearby slots.
2. **Local reproduction:** a child is placed in an empty Moore-neighbour of its
   parent (no teleporting to a random slot).

Grid starts full (256 random rings). Metric: Moran's I of the RULE field over
the torus (occupied slots, Moore weights); >0 means spatial clustering.
Configs (3 seeds, 300 ticks):

| name           | change                                              |
|----------------|-----------------------------------------------------|
| local_faithful | local addressing only, otherwise faithful           |
| local_stable   | local + RULE/addr protected + mutation x0.3         |

### Prediction

Locality alone will not organize a system that churns its whole genome every
tick; but locality **plus a heritable rule** should let each lineage's rule
spread to its neighbours through local reproduction, forming spatial domains
(Moran's I clearly > 0).

### Observation

Moran's I of RULE at the final tick (mean over 3 seeds):

| config            | Moran's I | mean pop |
|-------------------|----------:|---------:|
| nonlocal_faithful |    -0.028 |      144 |
| local_faithful    |     0.038 |      198 |
| local_mutoff      |     0.010 |      137 |
| local_lowmut      |     0.064 |      170 |
| **local_stable**  | **0.278** |      176 |

Visually, `local_stable` develops contiguous coloured domains of similar rule
that nucleate by ~t=30 and grow into large coherent regions by ~t=285,
starting from an initially salt-and-pepper grid. The non-local and
faithful-local runs stay salt-and-pepper.

### Interpretation

- **Spatial self-organization appears, and it is emergent.** Only the
  combination of locality and a heritable rule yields strong clustering
  (Moran's I 0.278, vs ~0 for every other config). The domains are not
  specified anywhere in the rules; they form because local reproduction copies
  a lineage's heritable rule into adjacent slots, and like-rules aggregate.
  This is qualitatively different from the H2 result, where the favoured type
  was named in advance.
- **Heredity is again the enabling ingredient.** `local_faithful` (locality,
  no heredity) barely clusters (0.038): without a stable rule there is nothing
  for space to organize. `local_mutoff` collapses to a clone (no variation, so
  no domain *structure*). Moderate mutation on a protected rule is the sweet
  spot --- enough heredity to hold domains, enough variation to keep them
  distinct.
- **Domains persist despite high action-bit turnover.** local_stable still has
  turnover ~0.7/tick, but the *rule* field (protected) is stable, so the
  spatial pattern lives in the heritable layer while the action bits churn
  underneath.

### Takeaway

This is the strongest self-organization result so far: combining local
addressing with a heritable rule produces emergent spatial domains (Moran's I
~0.28) that the well-mixed baseline cannot. It is also the most legible ---
visible directly in the dashboard's universe grid. Unlike E2, the structure is
discovered by the system rather than named by us.

### What this points to next

The domains are static-ish aggregates. The open question is whether spatial
*and* selective pressure together produce **dynamic** patterns --- travelling
fronts, competition between domains, or coexistence (an ecology) rather than a
single eventual winner. Natural next steps: combine local addressing with the
heritable trigger (H2) and a modest death rate (H2c) to see whether domains
compete and turn over; and probe whether any rule-domain actively maintains
itself (an autopoietic signature) versus merely being inherited.
