# Experiments Log

Each entry: configuration, prediction, observation, interpretation. Observation
and interpretation are kept visibly separate (per repo report guidelines).
Unless noted, runs use 256 slots; sample sizes are small (often 3--5 seeds, some
single) --- treat magnitudes as indicative, qualitative separations as robust.

Reproduce with: `python3 experiments.py` (battery) and `python3 spatial_probes.py`
(E5/E8 probes). Spatial experiments require `local_addr=True` --- see DESIGN.md
section 3.7 on addressing modes (the grid is only real space in local mode).

## Metrics glossary

All implemented in `analyze.py`. Each is read against a null where possible.

- **turnover** --- (births + deaths) / population per tick. Churn rate.
- **activity** --- bits changed by transformation per tick. Microscopic churn.
- **genotype concentration** --- largest single-genotype share of the
  population. High = takeover/clone.
- **persistence** --- longest run of consecutive ticks any genotype stays
  present.
- **compressibility** --- gzip size of the living population's bits / same for a
  random matrix. <1 means internal structure.
- **self-preservation** --- mean fraction of a ring's bits left unchanged by its
  *own* rule. The emergent-heredity / self-templating signal (E6). Chance ~0.5.
- **neighbour-identity ("genome-domain enrichment")** --- fraction of
  torus-adjacent occupied pairs with the *same* rule (or whole genome), divided
  by the chance rate 1/(distinct types). The **correct categorical metric for
  spatial domains** (E5/R1). The chance baseline is approximate (assumes
  well-mixed types).
- **flip-rate** --- fraction of continuously-occupied slots whose genome changes
  between consecutive ticks. Low = static domains; high = dynamic (E8).
- **novelty** --- fraction of a tick's genomes never seen before. Open-endedness
  signal (E9/E12).
- **key-share** --- fraction of rings whose key (`key_span`) equals a code. The
  directional-selection signal (E2/E10). Chance = 1/16 = 0.0625.
- **Moran's I (DEPRECATED)** --- spatial autocorrelation of the rule *value*.
  **Misleading**: rule numbers are categorical, not ordinal, so a grid of
  categorically-identical domains with scattered rule *numbers* scores ~0. It
  produced a false "unstructured" negative for two experiments (see Reflection
  R1). Retained in output only as a flawed historical reference; use
  neighbour-identity instead.

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

(Metric note, added post-R1: Moran's I is a valid domain signal *here* only
because the rule is **protected** --- every ring in a domain has the identical
rule *value*, which clusters. The categorical neighbour-identity metric
corroborates it: rule-match 15.8x chance. When rules are *not* protected (E6),
Moran fails and only neighbour-identity works. See Reflection R1.)

### What this points to next

The domains are static-ish aggregates. The open question is whether spatial
*and* selective pressure together produce **dynamic** patterns --- travelling
fronts, competition between domains, or coexistence (an ecology) rather than a
single eventual winner. Natural next steps: combine local addressing with the
heritable trigger (H2) and a modest death rate (H2c) to see whether domains
compete and turn over; and probe whether any rule-domain actively maintains
itself (an autopoietic signature) versus merely being inherited.

---

## E5 --- Domain dynamics and an autopoiesis probe

Reproduce: `python3 spatial_probes.py` (local + protected RULE/addr + mut x0.3).

### E5a --- The domains form a dynamic, coexisting ecology

Question: do the E4 domains coarsen to a single winner, freeze, or coexist?

Observation (seed 1, 800 ticks; #domains = connected same-rule components of
size >= 3):

| tick | pop | Moran's I | #domains | largest |
|-----:|----:|----------:|---------:|--------:|
|   0  | 256 |    -0.023 |        0 |       2 |
|  50  | 188 |     0.505 |       14 |      16 |
| 100  | 199 |     0.450 |       16 |      11 |
| 200  | 194 |     0.304 |       17 |      14 |
| 400  | 210 |     0.232 |       15 |      10 |
| 600  | 197 |     0.370 |       20 |       9 |
| 800  | 224 |     0.444 |       18 |      47 |

Interpretation: the system reaches a **dynamic steady state of ~15--20
coexisting domains**, not a single winner and not a frozen pattern. Moran's I
fluctuates (0.23--0.50) and the largest domain fluctuates (16 -> 9 -> 47),
i.e. domains continually grow, shrink, fragment and occasionally swell. This
is an ecology-like regime, sustained by the balance of heritable rules (which
hold a domain together), birth mutation (which keeps seeding new domains), and
local competition. This is the clearest "interesting dynamic pattern" found so
far, and it is emergent.

### E5b --- Do domains actively maintain themselves? (no clear evidence)

Question: is a domain a self-maintaining structure (resists invasion) or a
passive inherited blob?

Probe: inject a patch of one rule into another domain's territory and watch.

- **Naive version is confounded.** Injecting an arbitrary far-in-bitspace rule
  into a host domain, it always vanished (e.g. 9 -> 0) --- but a control
  planting those same rules as their own block showed they decay on their own
  too (16 -> 0). So the reabsorption was **invader weakness, not host
  resistance.** Most random rules are simply poor reproducers; only a minority
  form persisting domains.
- **Clean version is mixed.** Injecting each of the two largest *distinct*
  domains' rules into half of the other's home, outcomes vary by seed:
  competitive dominance in some (seed 0: rule 151 grows 25->42 while rule 230
  -> 0), co-persistence in others (seed 5: both rules survive, 79->64 and
  61->56), and no signal where domains are small (half-domain patches of a few
  rings die in the noise).

Interpretation: there is **no systematic evidence of autopoietic
self-maintenance**. The mix of competitive dominance and co-persistence is
what passive local reproduction with rule-dependent reproductive rates would
produce; domains do not appear to actively defend their boundaries beyond the
inertia of in-place copying. The natural coexistence of E5a is therefore best
read as maintained by **spatial separation plus mutational renewal**, not by
self-maintenance.

Caveat: the probe is underpowered for small domains and uses a single
perturbation per seed. A stronger test (size-matched domains, many rule pairs,
comparison to a neutral rule-relabeling null) is needed before the
self-maintenance question can be settled.

### Takeaway

Space + heredity gives a genuine emergent dynamic: a coexisting, turning-over
ecology of rule-domains (E5a). But the domains are not (demonstrably)
self-maintaining (E5b) --- coexistence is structural and mutational, not
autopoietic. Getting true self-maintenance, if the substrate allows it,
probably needs reproduction tied to a ring's *function* (e.g. self-templating)
rather than rules competing as passive spatial tags.

---

## E6 --- Self-templating: can heredity *emerge* instead of being imposed?

Reproduce: `selftmpl_local` / `selftmpl_mixed` in `experiments.py`; the
self-preservation signal is `analyze.self_preservation_series`.

### Motivation

Every earlier positive result imposed heredity by protecting bits. The
question this experiment asks is whether the system can *discover* heredity on
its own --- genomes that survive transformation without being protected.

### Design

Tie the right to reproduce to a functional ability: a ring's reproduction is
gated stochastically on its **self-consistency** --- the fraction of its bits
left unchanged when its own CA rule is applied to it (preservation), with
success probability `preservation**power` (power 2 unless noted). No bits are
protected. A feasibility check first confirmed a climbable gradient:
preservation over random genomes is smoothly distributed (mean 0.52, ~0.5%
already perfect, 8% above 0.8), so selection has somewhere to go.

### Prediction

Self-templating should raise mean self-preservation over time (emergent
selection for self-stability). If self-stability is sufficient for heredity,
spatial domains should also form *without* protection.

### Observation

Mean self-preservation (start -> end) and the resulting population, 500 ticks:

| config             | preservation | pop | unique | rules | activity | Moran |
|--------------------|-------------:|----:|-------:|------:|---------:|------:|
| local, no template | 0.52 -> 0.70 | 156 |    145 |    74 |      945 | -0.05 |
| local + template   | 0.52 -> 0.95 | 215 |  84--102|  23--36|    ~1000 | -0.05 |
| local + template p4| 0.52 -> 0.97 | 223 |     90 |    26 |     1101 |  0.12 |
| mixed + template   | 0.52 -> 0.99 | 256 |   4--45 |  2--14 |    9--40 | ~0.00 |

(local/mixed + template ranges are over 4 seeds; both effects are robust.)

### Interpretation

- **Heredity-compatibility emerges --- the open question is answered "yes, in
  principle."** Self-templating reliably drives self-preservation from chance
  (0.52) to 0.95--1.0 with no bits protected: the system discovers genomes
  that are (near) fixed points of their own rule, i.e. that survive their own
  transformation. This is emergent selection, not imposed stability.
- **But emergent self-consistency is necessary, not sufficient, for rich
  organization, and the two regimes are both limited:**
  - *Well-mixed* collapses to a near-frozen, low-diversity clone (preservation
    ~1.0, activity ~9, 2--14 rules). Heredity emerges, but as a trivial single
    fixed point --- a self-perpetuating clone, not an ecology.
  - *Local* stays diverse (23--36 rules) and active (~1000 bits/tick) and
    self-consistent (0.95), but forms **no spatial domains** (Moran ~0).
    **[WRONG --- corrected in Reflection R1: this is a Moran-metric artifact;
    E6-local DOES form strong genome domains, ~16x chance, by neighbour-identity.
    The interpretation in this bullet and the next paragraph is superseded.]**
- **Why self-consistency does not give spatial heredity.** Self-consistency is
  being a fixed point of one's *own* rule, but a ring is transformed by its
  *neighbour's* rule. Self-templating therefore selects for individual
  self-stability, not for neighbours sharing a rule. Well-mixed dynamics reach
  global heredity only by collapsing to one rule everywhere (frozen clone);
  local dynamics cannot collapse globally, so neighbours with different
  (individually self-consistent) rules keep disrupting each other --- active,
  but unstructured.

### Takeaway

This revises the project's central claim. Heredity does *not* have to be
imposed: selection for self-templating makes it emerge (preservation
0.52 -> ~1.0, robust). But emergent self-consistency alone yields either a
trivial frozen clone (well-mixed) or an active but spatially unstructured
population (local) --- not the coexisting domains that imposed protection
produced. Emergent *individual* heredity is not the same as emergent
*collective/spatial* organization.

### What this points to next

The missing ingredient is **neighbourhood agreement**: domains need neighbours
to share a rule, which self-consistency does not select for. The natural E7 is
templating *onto the neighbour* --- a ring reproduces by copying itself onto
its push-target's location --- which spreads a genome to its neighbourhood and
should couple self-stability to spatial agreement, the plausible route to
domains that are heritable *and* emergent (no protection).

> **Correction (see Reflection R1):** the conclusion that E6-local is
> "unstructured" is **wrong** --- an artifact of measuring spatial structure
> with Moran's I on rule *values*. With the correct categorical metric, E6-local
> already forms strong emergent genome domains. The central problem was solved
> here, not at E7.

---

## Reflection R1 --- a metric error and what it overturns

**The error.** Spatial structure was being measured with Moran's I of the RULE
field. Moran's I assumes the variable is *ordinal* --- it sums products of
value deviations, so it treats rule 1 and rule 2 as "close" and rule 1 and rule
255 as "far." But rule numbers are **categorical** (rule 110 and rule 111 are
unrelated behaviours). A grid tiled with domains of categorically-identical
genomes whose rule *numbers* are scattered scores Moran's I ~0 --- exactly the
"unstructured" reading we got for E6.

**The fix.** Measure **neighbour identity**: the fraction of adjacent occupied
pairs with the *same* rule (or the same full genome), divided by the chance
rate 1/(distinct types). Implemented as `analyze.neighbour_identity`.

**What it overturns.** Re-measuring the spatial experiments (genome-domain
enrichment = neighbour genome-identity / chance, 5 seeds, 500 ticks):

| config (no bits protected unless noted) | genome-domain enrichment |
|-----------------------------------------|-------------------------:|
| E1 nonlocal faithful                    |                    ~1    |
| E4 local + protected rule + mut (imposed heredity) | ~4 (rule-only) |
| **E6 local + self-templating**          |          **14--18x**     |
| E7 local + self-templating + overwrite  |              ~16x        |
| self-templating, well-mixed (clone)     |          ~4 (uniform)    |

So **E6 already solved the central problem**: local addressing + self-templating
produces emergent domains of *identical, self-consistent genomes* with nothing
protected (genome-match 0.15--0.19 vs chance ~0.012, robust across 5 seeds,
building up over time). Emergent individual heredity (E6's preservation -> 1.0)
and emergent spatial structure are the *same* phenomenon when viewed with the
right metric; they were never separate. The imposed-heredity domains of E4 are,
by contrast, only *rule*-uniform --- their action bits churn, so their
genome-domain enrichment is a mere ~4x.

**Lesson logged:** match the metric to the variable's type. An ordinal
statistic on a categorical field produced a confident, wrong negative that
stood for two experiments. Always sanity-check structure metrics against a
direct categorical measure and against a rendered frame.

---

## E7 --- Templating onto the neighbour

### Design

A ring's child overwrites a random Moore-neighbour (occupied -> replaced, empty
-> filled) instead of only filling empty slots, spreading the genome through
the neighbourhood (`overwrite_birth`). Also adds `local_range`: the max |offset|
for local PULL/PUSH, so interaction can be made genuinely short-range (range 8
= the original half-torus reach; range 1--2 = near-neighbour).

### Prediction

Spreading the genome onto neighbours should reinforce domains; short-range
interaction should let a domain's *transformers* also be domain-mates, reducing
the churn that long-range transformers inflict.

### Observation

With the categorical metric, genome-domain enrichment (seed 3, 500 ticks):

| config | genome-domain enrich | turnover | self-pres |
|--------|---------------------:|---------:|----------:|
| E6 local + self-templating (range 8) |  16   | 0.63 | 0.95 |
| E7 + overwrite, range 2              |  16   | 1.61 | 0.96 |
| overwrite, range 2, *no* self-template |  ~2 | high | 0.88 |

### Interpretation

- **Overwrite is not the active ingredient; self-templating is.** Overwrite
  without self-templating gives almost no genome domains (~2x); with it, ~16x.
  Spreading a genome only builds a domain if the genome is stable enough to
  survive transformation, which self-templating provides. Overwrite mainly
  raises turnover (1.6 vs 0.6) without adding domain structure beyond E6.
- **Short-range interaction did not obviously help** the genome-domain metric
  here (E6 at range 8 already ~16x). It remains worth a clean sweep with the
  correct metric (E8), because the *stability* of domains --- not just their
  presence at a snapshot --- should depend on whether a domain's transformers
  are domain-mates.

### Takeaway

E7 confirms (does not create) the E6 result and isolates self-templating as the
mechanism behind emergent genome domains. The open question shifts from "can
domains form?" (yes, E6) to "are they *stable* self-maintaining structures, or
dynamic clusters that churn?" --- which is what short-range interaction (E8)
and a persistence analysis should settle.

---

## E8 --- Are the emergent domains stable? (no: they are dynamic)

### Design

Sweep `local_range` (transformation reach) for the E6 self-templating
configuration, measuring genome-domain enrichment, self-preservation, and a
**flip-rate** (fraction of continuously-occupied slots whose genome changes
between consecutive ticks; low = stable domains). 3 seeds, 500 ticks.

### Observation

| local_range | genome-domain | flip-rate | self-pres |
|------------:|--------------:|----------:|----------:|
| 1           |        19.5x  |     0.31  |     0.96  |
| 2           |        11.3x  |     0.43  |     0.93  |
| 3           |         5.0x  |     0.75  |     0.81  |
| 4           |        14.6x  |     0.30  |     0.95  |
| 8           |        15.5x  |     0.27  |     0.95  |

### Interpretation

- **Domains are dynamic, not static, at every range.** Flip-rate never drops
  below ~0.27 --- at least a quarter of the population changes genome each
  tick even where genome-domain enrichment is ~16--19x. The domains exist as
  snapshots but continually churn and reform; they are not frozen structures.
- **No clean short-range stabilization.** The hypothesis that short-range
  transformation (a domain's transformers being domain-mates) would stabilize
  domains is not supported: the range dependence is non-monotonic and noisy
  (ranges 3 and 6 are notably worse on only 3 seeds), with no trend toward low
  flip-rate at small range. Whatever stabilizes a domain, it is not simply the
  locality of its transformers.

### Takeaway

The emergent domains are **dynamic clusters maintained through flux**, not
static crystals. This is consistent either with a self-maintaining
process-structure (interesting) or with turbulent coarsening (mundane); E8
alone does not distinguish them. It reframes the autopoiesis question as one
about *pattern* persistence under substrate churn, not slot-level stability.

---

## E9 --- Open-endedness: does novelty persist or freeze?

### Design

Run 2000 ticks and measure **novelty** (fraction of a tick's genomes never seen
in any previous tick) and cumulative distinct genomes. The question: does the
system keep generating new structure, settle to a fixed point, or just emit
noise?

### Observation

| config | novelty @150 / 950 / 1950 | cumulative distinct @500/1000/2000 |
|--------|---------------------------|-------------------------------------|
| baseline churn            | 0.71 / 0.69 / 0.66 | 49k / 100k / 195k |
| self-templating, mixed    | 0.65 / 0.006 / 0.002 | 30k / 36k / 36k |
| self-templating, **local**| 0.35 / 0.30 / 0.22 | 19k / 33k / 56k |

### Interpretation

Three qualitatively distinct fates:

- **Baseline churn** sustains high novelty, but it is meaningless --- pure
  mutational noise with no heredity or structure (cumulative diversity diverges
  linearly at ~100/tick).
- **Self-templating, well-mixed** *freezes*: novelty collapses to ~0 and
  cumulative diversity saturates. The system finds a self-consistent clone (a
  fixed point) and stops.
- **Self-templating, local** sits between: **sustained, structured novelty**
  (0.2--0.35) with cumulative diversity still growing ~linearly (~23/tick),
  while maintaining genome domains and heredity. New self-consistent genomes
  keep arising and forming domains.

### Takeaway

The `selftmpl_local` regime is the most life-like found: neither frozen
(well-mixed) nor structureless noise (baseline), but ongoing generation of new
self-consistent genomes organized into domains --- an edge-of-chaos sweet spot.
Caveat: the novelty *rate* is slowly declining over 2000 ticks, so whether this
is genuinely open-ended or merely freezing very slowly is unresolved; it needs
much longer runs and a saturation test. The novelty is also *exploratory* (it
roams the self-consistent manifold) rather than *directional* (self-preservation
has already plateaued at ~0.95), so it is not yet adaptation in the strong
sense.

---

## Reflection R2 --- where the program stands (after E9)

**Map of regimes (the substrate's phase diagram, informally):**

- *Faithful / well-mixed* -> high-entropy churn (no heredity).
- *Imposed heredity (protect bits)* -> rule-domains, an ecology, but heredity
  supplied by us and not self-maintaining (E4/E5).
- *Self-templating, well-mixed* -> emergent heredity but a frozen clone (E6/E9).
- *Self-templating, local* -> **emergent self-consistent genome domains with
  sustained structured novelty** (E6/E7/E9). The richest regime.

**What is established:** heredity and spatial structure emerge together from
self-templating in a local medium, with nothing protected (R1). This is a solid,
reproducible positive answer to "can adaptive self-organization arise, and what
makes it." The enabling modifications, in order of necessity: locality,
heredity (here emergent via self-templating), and a balance of
mutation/turnover that avoids both freeze and noise.

**What remains genuinely open (the live frontier):**

1. **Open-endedness** --- is `selftmpl_local` novelty sustained or slowly
   freezing? (needs 10k+ tick runs; B4)
2. **Adaptation vs exploration** --- can a *directional* selective gradient act
   on the emergent domains, giving improvement rather than neutral roaming?
   Combine self-templating with a functional task or competition (B2/B3).
3. **Autopoiesis, re-asked** --- are the dynamic domains self-maintaining
   patterns or turbulent coarsening? (a pattern-persistence test, not the
   slot-level one of E8)

**Next moves:** B2/B3 (couple emergent heredity to a directional/competitive
pressure to seek adaptation) looks higher-value than more B5 substrate sweeps,
because structure now exists and the missing element is *direction*. I will
pursue adaptation next (E10+), then return to a long open-endedness run.

---

## E10 --- Emergent heredity unlocks robust directional adaptation

### Motivation

In E2/E3 directional selection on a heritable key was *fragile*: it plateaued
near 0.10 and pushing it caused extinction, because heredity was imposed by
freezing bits while the rest of the genome (and reproduction) stayed noisy. Now
that self-templating supplies *emergent* heredity, does the same directional
gate work?

### Design

Local addressing; reproduction gated on `key == 15` (directional pressure),
death on `key == 0`. Compare the heredity mechanism: imposed (protect the key
bits, E2-style) vs emergent (self-templating). Key-15 share is the adaptation
signal (chance = 0.0625). 4 seeds, 600 ticks.

### Observation

| heredity mechanism (local, key-gated) | key-15 end share | population |
|---------------------------------------|-----------------:|-----------:|
| imposed (protect key bits)            | 0.10--0.12       | ~250 |
| **emergent (self-templating)**        | **0.70--0.77**   | 254--256 |
| emergent + short range (range 2)      | 0.74--0.76       | 256 |
| *control:* self-templating, **no gate** | 0.10--0.15     | --- |

### Interpretation

- **Emergent heredity makes directional selection strong and robust.** The
  identical key-gate that imposed heredity could push only to ~0.11 reaches
  ~0.75 (12x chance) under self-templating, across every seed, with the
  population full and stable --- none of E3's extinction.
- **The gate is what drives it.** Self-templating without the gate leaves
  key-15 at ~0.12 (mild drift enrichment from domain formation), so the rise
  to 0.75 is selection on the imposed gradient, not an artifact of
  self-templating.
- **Why imposed heredity failed and emergent heredity works.** Protecting the
  key makes the *tag* heritable but leaves the rest of the genome and the spawn
  machinery noisy, and the universe saturates with immortal non-reproducers
  (E2/E3) --- so a key-15 ring is not reliably a good replicator. Self-templating
  makes the *whole* genome viable and self-consistent, so key-15 rings
  reproduce reliably, form domains, and spread. Reliable heredity is the
  precondition selection needed all along.

### Takeaway

This is the project's first instance of strong, robust **adaptation**:
directional selection driving a trait from chance (0.06) to fixation-approaching
(0.75) without fragility, built on emergent heredity. Together with E6
(emergent heredity + domains) and E9 (sustained novelty), self-templating in a
local medium now supports the full chain --- persistence, heredity, and
adaptation --- that the project set out (RESEARCH_PLAN section 1) as the
operational definition of adaptive self-organization. The remaining frontier is
*open-ended* adaptation (a gradient the system never finishes climbing) rather
than this single imposed target.

---

## E11 --- Cyclic dominance: coexistence without spirals

### Design

Add competitive, frequency-dependent dynamics to avoid freezing and seek
striking spatial patterns. Type = rule mod 3; a ring may overwrite an occupied
neighbour only if its type *beats* the neighbour's (rock-paper-scissors:
0>1>2>0) (`cyclic_dominance`, on top of local + overwrite + self-templating).
Tested at 16x16 and, to give spirals room, 64x64 (4096 slots --- local
addressing uses offsets, so the grid can grow without changing the genome).

### Observation

- **Three-way coexistence is robust.** All three types persist for 600+ ticks
  with fluctuating abundances (e.g. one seed's type counts move
  [45,15,10] -> [54,74,22] -> [64,53,86]); none fixes, unlike ordinary
  competition which would let one type win.
- **No clean spirals.** At 64x64 the spatial pattern is *patchy* coexistence,
  with one type (rule%3 == 0) noticeably dominant in area, not the symmetric
  rotating spirals of textbook spatial RPS.

### Interpretation

The cyclic rule successfully prevents takeover and sustains a non-freezing
three-type ecology --- a different route to "not frozen" than E9's novelty. But
the spirals fail to form because the three types are **not symmetric** in this
substrate: rule%3 classes differ in self-consistency and viability, so the
competition is unbalanced (one type is intrinsically stronger), which breaks
the rotational symmetry that spiral formation requires. Imposing a clean
cyclic *label* does not impose clean cyclic *dynamics* when the underlying types
have heterogeneous fitness.

### Takeaway

Frequency-dependent cyclic dominance buys robust three-way coexistence (a
non-freezing ecology) and demonstrates the substrate scales to larger grids,
but not the striking spiral patterns, because the substrate's types have
unequal viability. Getting spirals would require equalizing type fitness (e.g.
defining types so all three are equally self-consistent) --- a tuning exercise
deferred in favour of the open-endedness question (E12).

(Infrastructure note: this established that local-addressing runs work at
nmax = 4096 (64x64); larger grids are now available for any spatial experiment.)

---

## E12 --- Open-endedness resolved: novelty plateaus, it does not freeze

### Design

E9 left it unresolved whether `selftmpl_local` novelty is sustained or slowly
freezing (the rate was declining over 2000 ticks). Settle it with a long run:
8000 ticks, novelty measured online, and the novelty slope over the second half.

### Observation

| t ~ | 100 | 1000 | 2000 | 4000 | 6000 | 7900 |
|-----|----:|-----:|-----:|-----:|-----:|-----:|
| novelty | 0.50 | 0.29 | 0.21 | 0.17 | 0.20 | 0.18 |

- Novelty slope over the last 4000 ticks: **-0.003 per 1000 ticks** (flat).
- Cumulative distinct genomes: 168,577, still growing ~linearly (~21/tick).

### Interpretation

The declining novelty of E9 was an **initial transient**, not a slide toward
freezing. After ~t=4000 the novelty rate **plateaus at ~0.18--0.20 and holds**:
roughly a fifth of the population is a never-before-seen self-consistent genome
every tick, indefinitely, while the system keeps its domain structure and
heredity. Cumulative diversity grows without bound at a steady rate.

### Takeaway

`selftmpl_local` is **sustainably open-ended** over the horizon tested (8000
ticks): it neither freezes (contrast self-templating well-mixed, E9) nor emits
structureless noise (contrast baseline). It continuously generates new
self-consistent genomes organized into domains --- ongoing structured novelty
at a stable positive rate. This is the strongest "alive" result of the project:
emergent heredity (E6), emergent spatial domains (E6/R1), robust adaptation when
a gradient is present (E10), and sustained open-ended novelty (E12), all from
self-templating in a local medium with nothing protected. The novelty is still
*exploratory* (roaming the self-consistent manifold) rather than *directionally
complexifying*; whether complexity itself grows over time is the next question
(B4, a complexity-over-time measure).

---

## E13 --- The ceiling: novelty without complexification

### Design

E12 showed sustained novelty. Does anything *complexify*, or does the system
roam a fixed-complexity manifold? Over 6000 ticks (`selftmpl_local`), track
crude complexity proxies: number of distinct rules, population compressibility
(gzip vs random; lower = more internal structure), mean bits-set per genome,
and self-preservation.

### Observation

| tick | rules | compressibility | mean bits-set | self-pres |
|-----:|------:|----------------:|--------------:|----------:|
|    0 |    79 |           0.997 |          17.9 |     0.62  |
| 1000 |    32 |           0.512 |          11.6 |     0.96  |
| 2000 |    22 |           0.442 |           9.7 |     0.93  |
| 3000 |    25 |           0.449 |          10.8 |     0.96  |
| 4000 |    38 |           0.503 |           9.4 |     0.93  |
| 6000 |    22 |           0.443 |           9.0 |     0.99  |

### Interpretation

Every complexity proxy **plateaus by ~t=1000--2000 and then fluctuates around a
stable level** --- it does not trend upward. Structure appears fast
(compressibility 1.0 -> ~0.45, genomes settle sparse at ~10 of 36 bits, rules
contract to a stable 20--40) and then holds. The sustained novelty of E12
happens *within* this fixed-complexity manifold: the system keeps finding new
self-consistent genomes of roughly constant complexity, not progressively more
complex ones.

### Takeaway

This is the project's **ceiling result**, and an honest negative on the hardest
ALife goal. `selftmpl_local` is open-ended in *novelty* but **not in
complexity**: there is no complexity growth, no sign of major transitions or
escalating sophistication. The substrate supports persistence, heredity,
adaptation, spatial self-organization, and sustained exploratory novelty --- but
not open-ended *complexification*. The latter likely needs ingredients this
substrate lacks: composability/hierarchy (rings made of rings), a reason for
complexity to pay (a richer, changing selective environment), or
genome growth (a fixed 36-bit genome caps attainable complexity from the
start).

---

## Reflection R3 --- the arc, and the wall

**The arc (E1->E13).** Starting from a faithful system that is pure churn, a
short chain of modifications --- locality, self-templating (emergent heredity),
balanced mutation --- climbs the full ladder set out in RESEARCH_PLAN section 1:
persistence -> heredity -> adaptation, plus emergent spatial structure and
sustained open-ended novelty. Almost all of it is *emergent* (nothing protected
by us) once self-templating is in. The one repeated lesson is that **heredity is
the master key**: every capability unlocked the moment genomes could reliably
persist, and self-templating is the minimal way to make that emerge.

**The wall (E13).** Novelty is sustained but complexity is not. The system
reaches a fixed-complexity manifold and explores it forever. This looks like a
real ceiling of the substrate, not a tuning failure --- consistent with the
sparse, ~10-bit self-consistent attractor genomes E13 finds.

**What would test the wall (the next branches):**

- **B7 --- genome growth / composability.** The 36-bit genome bounds complexity
  a priori. Allowing variable-length rings, or rings whose "rule" is itself
  built from other rings, is the principled way to ask whether complexity *can*
  grow. This is the most fundamental and most promising remaining direction.
- **B8 --- a changing environment.** Static selection plateaus. A selective
  pressure that itself moves (coevolution that does not collapse, or an
  exogenous environment that drifts) might keep complexity paying off. E11's
  cyclic dominance was a first, symmetric-but-unbalanced attempt; a coevolving
  predator-prey coupling is the stronger version.
- **B9 --- better complexity metrics.** "Compressibility of the population" is
  crude. Logical depth, or the functional diversity of what rings *do* to one
  another, would measure complexity more faithfully before concluding the wall
  is real.

I will pursue B7 (genome growth / composability) next --- it is the direction
most likely to break the ceiling, and the most interesting if it does.
