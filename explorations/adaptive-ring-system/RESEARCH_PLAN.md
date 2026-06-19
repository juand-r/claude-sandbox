# Research Plan --- Toward Emergent Self-Organization in the Ring System

Status: living document. Guides the iteration requested ("see what
modifications might be needed to get interesting patterns and emerging
adaptive self-organization to arise").

## 1. The question, stated carefully

Does the Adaptive Ring System, as specified, produce **emergent adaptive
self-organization** --- and if not, what minimal modifications make it do so?

The phrase has to be made operational or the project degenerates into
admiring pretty noise. We will treat the target as three nested, testable
claims, weakest to strongest:

1. **Persistence.** Some informational structure (a genotype, a sub-network,
   a spatial pattern) survives far longer than the system's intrinsic
   rewrite timescale. Without this, nothing else is possible.
2. **Heredity.** That structure reproduces, and offspring resemble parents
   more than chance. This is the precondition for selection.
3. **Adaptation.** The population's composition shifts over time in a way
   that is *not* explained by neutral drift --- i.e. selection does
   measurable work.

We will not claim "self-organization" on the strength of diversity,
liveliness, or visual appeal alone.

## 2. The central skeptical worry (lead hypothesis)

The substrate as specified probably has **no stable unit of heredity**, for a
structural reason:

- A living ring is **rewritten every tick** by whatever transforms it. Its
  RULE, addresses, spawn/death and mutation bits are all inside the same
  36-bit circular string the CA sweeps. Identity is not conserved across a
  ring's own lifetime.
- Spawn and death are **single bits read after transformation**. Since a
  large fraction of the 256 ECA rules produce roughly balanced output, each
  ring's spawn/death outcome is close to a coin flip driven by whoever
  transformed it. Reproduction and death are therefore largely **decoupled
  from genotype** --- they are noise, not selection.

If this is right, the baseline is high-entropy churn: ~half the population
replaced per tick, near-maximal genotype diversity, and nothing heritable.
That would look superficially "alive" while satisfying none of the three
claims above.

This worry is the first thing to test with data, before any redesign.

## 3. Measurement (build before intervening)

Add instrumentation, then characterize the baseline against null models.

### Metrics

- **Turnover** --- (births + deaths) / population per tick. Churn indicator.
- **Activity** --- fraction of bits changed by transformation per tick.
- **Genotype concentration** --- largest single-genotype share of the
  population, and Simpson diversity. Takeover by a replicator shows up here
  as concentration *rising*; pure churn keeps it near zero.
- **Persistence** --- for each distinct genotype that ever appears, the
  longest run of consecutive ticks it stays present. Headline number: the
  longest-lived genotype, and how many genotypes live longer than k ticks.
- **Genome non-randomness** --- gzip-compressed size of the living
  population's bit matrix divided by that of a uniform-random matrix of the
  same shape. < 1 means structure (low entropy / motifs) has emerged.
- **Push-graph structure** --- in-degree distribution of the push graph
  (are there hubs?) and the fraction of rings lying on a directed cycle
  (candidate autocatalytic loops), versus a random-address null.
- **Lineage** --- via per-ring unique IDs and birth(parent, tick) records:
  clade-size distribution and max lineage depth.

### Null models (so we know what "no organization" looks like)

- **Random-matrix null** for non-randomness: a uniform-random bit matrix of
  the same shape as the living population.
- **Identity-rule control** (all rings rule 204, no transformation): isolates
  what birth/death/mutation drift alone produces, for persistence and graph
  metrics.
- **Neutral-drift caveat for lineage.** Founder fixation happens under pure
  drift too, so clade dominance alone is *not* evidence of selection; it must
  beat the identity-rule control to count.

## 4. Hypothesised modifications (to try only after the baseline is measured)

Ordered by how directly they attack the heredity bottleneck of section 2.

- **H1 --- protect a heritable core.** Let transformations modify only a
  "data" region; keep RULE and the addresses (the "genotype") stable, so
  identity can persist and be inherited. Knob: `protect_fields`.
- **H2 --- make birth/death conditional, not coin flips.** Require a specific
  multi-bit code or a threshold rather than a single post-transform bit, so
  turnover stops swamping selection.
- **H3 --- lower the mutation / transformation intensity.** Too much change
  destroys structure. Knobs: `mut_scale`; biasing initial rules toward
  ordered (Wolfram class 1/2) rules.
- **H4 --- locality in addressing.** Interpret pull/push as relative offsets
  so neighbourhoods and spatial patterns can form, instead of absolute
  random wiring.

Each modification is an **opt-in config flag**; the faithful baseline stays
intact and is always the control.

## 5. Success criteria

- **Minimum bar (this iteration):** the baseline is quantitatively
  characterised and the section-2 worry is confirmed or refuted with numbers,
  against at least the random-matrix and identity-rule nulls.
- **Real progress:** at least one modification moves a persistence or
  heredity metric clearly above its null while not collapsing the system to a
  frozen or empty state.
- **Strong result (aspirational):** a modification yields adaptation ---
  population composition shifting beyond neutral drift, ideally a visible
  replicator or stable pattern.

## 6. Process

- Baseline characterization first; redesign second. No tuning before
  measuring.
- Every experiment logged in `EXPERIMENTS.md`: config, what was predicted,
  what happened, interpretation kept separate from observation.
- Report negative results. A clean refutation (e.g. "H1 did not help, here is
  why") is a result.
- Keep variants minimal and toggleable; do not build a framework ahead of
  need.
