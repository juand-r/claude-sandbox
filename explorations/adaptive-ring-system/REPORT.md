# Emergent Self-Organization in the Adaptive Ring System

**An investigation into whether the system produces adaptive self-organization,
and which modifications make it do so.**

Status: in progress (covers experiments E1--E5). This document is the
argument-level synthesis; the per-experiment log with full configurations and
numbers is in `EXPERIMENTS.md`, and the design of the simulator is in
`DESIGN.md`.

---

## Summary

The Adaptive Ring System, run faithfully, does **not** self-organize: it is
high-entropy churn with no stable unit of heredity. The single fact that
governs everything downstream is that the mechanism which makes the system
active --- rings transforming one another --- is also the mechanism that
destroys heredity, because a ring's entire genome (including its identity,
addresses, and control bits) is rewritten every tick by whoever transforms it.

Two modifications change this. **Protecting a heritable core** gives selection
something to act on: a reproduction trigger tied to a heritable tag produces
real, replicable natural selection where the baseline produces none --- though
it is weak and fragile. **Local addressing** (interpreting the wiring as
spatial offsets) plus a heritable rule produces the strongest and most legible
result: an emergent, dynamic *ecology* of ~15--20 coexisting spatial domains
that grow, shrink, and turn over.

A later modification softens what first looked like the system's defining
limitation. Heredity does **not** have to be imposed: gating reproduction on
self-consistency (a ring's ability to survive its own rule) makes
heredity-compatibility *emerge* through selection, with no bits protected
(self-preservation rises from chance, 0.52, to ~1.0). But emergent
self-consistency is necessary, not sufficient: well-mixed it yields a trivial
frozen clone, and spatially it yields an active but unstructured population ---
not the coexisting domains that imposed heredity produced. The real gap is now
between emergent *individual* heredity (shown) and emergent *collective,
spatial* organization (not yet shown). Across every experiment, the substrate
has still produced nothing that both organizes spatially and sustains itself
without some ingredient supplied by us.

---

## 1. The system, in brief

A finite universe of `N = 256` "rings." Each ring is a 36-bit circular string
that is simultaneously: data, an 8-bit elementary cellular-automaton rule, and
a node in a transformation network (it names one ring that transforms it and
one it transforms). The remaining bits are a composition-order field and three
"action" bits: spawn, die, and a 2-bit mutation rate. There is no controller,
no fitness function, no energy, and no separate memory --- by design. Each
tick, rings transform one another (a CA rule swept around the target's bits),
then reproduce, die, and mutate, under a hard population cap.

The full specification and the resolution of its ambiguities are in
`DESIGN.md`.

## 2. Making the question testable

"Self-organization" must be made operational or the project degenerates into
admiring noise. We treat the target as three nested, increasingly demanding
claims:

1. **Persistence** --- some informational structure survives far longer than
   the system's intrinsic rewrite timescale.
2. **Heredity** --- that structure reproduces, and offspring resemble parents
   more than chance.
3. **Adaptation** --- the population's composition shifts in a way not
   explained by neutral drift.

The discriminating metrics (turnover, genotype concentration, persistence,
gzip-compressibility against a random-matrix null, push-graph hubs and cycles,
lineage founders, and spatial autocorrelation) are defined in
`RESEARCH_PLAN.md` and implemented in `analyze.py`. Crucially, each is read
against a null --- a random-matrix baseline, or a drift-only control with
transformation switched off --- so that "structure" means "beats the null,"
not "looks busy."

## 3. Findings

### 3.1 The baseline is churn, not organization

Run faithfully, the system replaces roughly its **entire population every
tick** (turnover ~1.0) while no genotype ever exceeds ~9% of the population.
The early impression of "high diversity" was high entropy, not structure.
Against the nulls this is unambiguous: a drift-only control (transformation
off) freezes near capacity with almost no turnover, and a no-mutation control
collapses to a single clone filling 77% of the universe --- the faithful
baseline sits between these as a maximally churning soup.

> **Evidence.** Turnover 1.00/tick; top-genotype share 0.086; compressibility
> 0.86 of random. Mutation-off: concentration 0.77, compressibility 0.04.
> Transformation-off: turnover 0.01. (E1.)

The mechanism is structural. A living ring is rewritten every tick by its
transformers, so its identity is not conserved across its own lifetime. Worse,
spawn and death are single bits read *after* transformation; since a large
fraction of the 256 CA rules produce roughly balanced output, each ring's
reproduce/die outcome is close to a coin flip driven by whoever transformed
it. Reproduction and death are therefore decoupled from genotype --- they are
noise, and selection has nothing to grip.

One observation from this phase is worth keeping: transformation reliably
builds **hub** structure in the push-graph (a few rings receive far more
transforming edges than chance) but *suppresses directed cycles below chance*.
The mutual-maintenance loops that an autopoietic story would predict are not
forming; if anything they are selected against. This foreshadows the later
autopoiesis negative.

### 3.2 The central tension: transformation is both engine and destroyer

Every subsequent result is a corollary of one tension. Activity in this system
comes from transformation. But transformation overwrites the genome, including
the very bits that would have to be stable for anything to be inherited. You
cannot have lively dynamics and stable heredity from the same unmodified
mechanism.

This is shown most sharply by trying to impose heredity bluntly. If the entire
genotype is protected from transformation so that a heritable tag can survive,
the population **freezes to near-extinction** (~11 rings): with rules frozen,
the spawn bit stops being toggled and reproduction stalls. Protect nothing and
the system stays lively but scrambles any tag every tick. The escape, when it
exists, is always *surgical* protection --- holding stable only the few bits
that must be heritable, and letting transformation churn the rest.

### 3.3 A heritable trigger yields real but fragile selection

Making reproduction conditional on a heritable 4-bit "key" (a ring reproduces
only if its spawn bit is set *and* its key matches a fixed code) produces the
first selection-beyond-drift signal in the system. The key's share of the
population rises above chance --- but only when the key is **heritable**
(protected from transformation). When the identical trigger is applied without
protecting the key, no selection occurs.

> **Evidence.** Key share rises from chance (0.0625) to ~0.10, replicable
> across 5 seeds (0.082--0.110, tightly clustered). The non-heritable control
> scatters around chance (0.00--0.26); its occasional spikes are clonal flukes,
> not selection. (E2.)

The effect is real but modest, and the cause of the modesty is instructive:
the universe saturates with immortal non-reproducing keys, starving selection
of empty slots. Adding turnover (a uniform death rate) does strengthen
selection --- key enrichment climbs to ~5x chance --- but the substrate's
reproduction is too noisy to sustain it, and higher death rates cause
stochastic **extinction** (half of seeds collapse). Selection strength and
viability are in direct tension. (E3.)

The honest reading: imposed-code selection works in principle but is near its
useful ceiling in this substrate. It also names the winner in advance, so its
"success" is partly built in --- which motivated looking for structure the
system discovers on its own.

### 3.4 The win: local addressing gives an emergent spatial ecology

The strongest and most legible result comes from making the system *spatial*.
Interpreting the pull/push addresses as signed (dx, dy) offsets on the 16x16
torus (instead of absolute slot indices), and placing each child next to its
parent, turns the non-spatial slot census into an actual medium.

Locality alone does nothing --- faithful churn is too violent for spatial
structure to survive. But locality **plus a heritable rule** (surgical
protection of the rule field, with moderate mutation) produces clear spatial
domains: contiguous regions of like rule that nucleate from an initially
random grid and grow into coherent patches.

> **Evidence.** Spatial autocorrelation (Moran's I of the rule field) is 0.278
> for local-plus-heritable, versus ~0 for every other configuration
> (non-local: -0.03; local without heredity: 0.04; local clone: ~0). (E4.)

This structure is **emergent** in a way the heritable-trigger selection was
not: nothing in the rules names the domains. They form because local
reproduction copies a lineage's heritable rule into adjacent slots and
like-rules aggregate.

Following the domains over a long run shows they are not a transient on the way
to a single winner, and not frozen, but a **dynamic steady state**: ~15--20
domains coexist and continually grow, shrink, fragment, and occasionally swell.
The largest domain fluctuates (16 -> 9 -> 47 slots over time) and the spatial
autocorrelation breathes between 0.23 and 0.50. This is an ecology-like regime,
held up by three balanced forces: heritable rules (a domain coheres), birth
mutation (new domains are seeded), and local competition. (E5a.)

This is the clearest "interesting dynamic pattern" the investigation has
produced, and it is directly visible in the dashboard's universe grid.

### 3.5 But the domains are not self-maintaining

The natural next claim --- that these domains are autopoietic structures that
defend themselves --- is **not** supported by the evidence.

A first invasion test (inject a foreign rule into a domain; watch it vanish)
looked like resistance, but a control exposed the confound: those rules decay
even when planted as their own block, so the reabsorption was invader
*weakness*, not host resistance. Most random rules are simply poor reproducers;
only a minority form persisting domains.

The clean test --- injecting each of two *viable* (persisting) domains' rules
into half of the other's territory --- is genuinely **mixed**: competitive
dominance in some rule pairs (one rule grows while the other vanishes),
co-persistence in others, and no signal where domains are small enough that a
half-domain patch of a few rings dies in the noise.

> **Interpretation.** There is no systematic self-maintenance signal. The mix
> of dominance and co-persistence is what passive local reproduction with
> rule-dependent reproductive rates would produce. The coexistence of 3.4 is
> therefore best read as maintained by spatial separation plus mutational
> renewal, not by domains actively defending their boundaries. (E5b.)

This conclusion is appropriately hedged: the probe is underpowered for small
domains and uses a single perturbation per seed. A size-matched design with
many rule pairs and a neutral rule-relabeling null is needed before the
self-maintenance question is settled.

### 3.6 Heredity can emerge --- but only as individual self-consistency

Every result to this point imposed heredity by protecting bits. Gating
reproduction on a *functional* ability instead --- a ring may reproduce only
in proportion to how well its own rule preserves its own genome --- makes
heredity-compatibility emerge on its own.

> **Evidence.** With no bits protected, mean self-preservation rises from
> chance (0.52) to 0.95--1.0 over 500 ticks, robustly across seeds. The
> distribution it climbs is smooth (8% of random genomes already preserve >80%
> of their bits), so the gradient is real, not a lucky jump. (E6.)

This is genuine emergent selection: the system discovers genomes that survive
their own transformation. But it does not, by itself, produce rich
organization, because the two regimes are both limited. Well-mixed, the
population collapses to a near-frozen, low-diversity clone (preservation ~1.0,
activity ~9 bits/tick, 2--14 rules) --- heredity emerges, but as a single
trivial fixed point. Local, the population stays diverse and active and
self-consistent, but forms no spatial domains (Moran's I ~0).

The reason is precise and worth stating: self-consistency is being a fixed
point of one's *own* rule, whereas a ring is transformed by its *neighbour's*
rule. Self-templating selects for individual self-stability, not for
neighbours sharing a rule. So well-mixed dynamics can only reach global
heredity by collapsing to one rule everywhere; local dynamics cannot, so
differently-ruled (but each self-consistent) neighbours keep disrupting one
another. Emergent individual heredity is not emergent collective organization.

## 4. Synthesis

Two threads run through every result.

**Heredity is the universal bottleneck.** In the well-mixed system it blocks
selection (3.1, 3.3); in the spatial system its presence is exactly what
distinguishes the configuration that organizes from the ones that do not
(3.4). Wherever the system fails to organize, the proximate cause is that
nothing is stably inherited; wherever it succeeds, heredity has been imposed by
protecting bits.

**Emergent individual heredity, yes; emergent collective organization, not
yet.** Imposed heredity is not strictly necessary --- selection for
self-templating makes self-consistency emerge (3.6). But what emerges that way
is either a trivial frozen clone or a self-consistent yet spatially
unstructured population. Conversely, the one configuration that produced rich
*spatial* organization (the coexisting ecology, 3.4) got its heredity from
imposed protection. No single configuration has yet delivered both at once:
heredity that the system discovers itself *and* the spatial, coexisting
structure that makes it interesting. Bridging the two is the central unsolved
problem, and 3.6 locates exactly why they are separate --- self-consistency
selects over a ring's own rule, while spatial structure needs neighbours to
share rules.

So the answer to the original question, so far: the faithful system does not
self-organize; surgical heredity buys fragile selection; spatial locality plus
imposed heredity buys a genuine emergent ecology of coexisting domains (the
headline success); and self-templating shows heredity can emerge unaided,
though so far only in a limited individual form. True adaptive
self-organization in the strong sense --- structure that is spatial,
coexisting, *and* self-maintained without anything supplied by us --- has not
appeared, and the evidence now points to *coupling self-templating to the
neighbourhood* as the most promising way to reach it.

## 5. Limitations

- **Heredity is imposed, not emergent.** All positive results depend on
  protecting bits from transformation. We have not shown the system can evolve
  its own heredity.
- **The reproduction key reuses the ORDER field's low nibble**, mildly
  conflating composition rank with reproduction eligibility. A dedicated field
  would remove this; deferred until it matters.
- **Sample sizes are small.** Most results are 3--5 seeds. Magnitudes are
  indicative; the qualitative separations (e.g. Moran's I 0.28 vs ~0) are
  robust, fine-grained numbers less so.
- **The autopoiesis probe is underpowered** for small domains (3.5).
- **Mutation-rate magnitudes were chosen, not tuned**, and could shift the
  regime boundaries.

## 6. Open questions and next steps

E6 answered the first open thread (heredity can emerge) but exposed the next:
self-templating selects over a ring's *own* rule, while spatial domains need
*neighbours* to share a rule. The natural next experiment (E7) is **templating
onto the neighbour** --- a ring reproduces by copying itself onto its
push-target's location --- which spreads a genome into its neighbourhood and
should couple self-stability to spatial agreement. That is the most promising
route to domains that are heritable *and* emergent, with nothing protected by
us. If it produces candidate self-maintaining domains, the strengthened
autopoiesis probe (size-matched domains, many rule pairs, a neutral
rule-relabeling null) becomes worth building to test them properly.

## 7. Reproducibility

| file | role |
|------|------|
| `ring_system.py` | simulator; experimental knobs default to the faithful spec |
| `test_ring_system.py` | 12 tests of the load-bearing semantics |
| `analyze.py` | discriminating metrics + nulls |
| `experiments.py` | the E1/E2/E4 config battery and comparison table |
| `spatial_probes.py` | E5 domain-trajectory and invasion probes |
| `EXPERIMENTS.md` | per-experiment log (E1--E5), full configs and numbers |
| `RESEARCH_PLAN.md` | operational definitions, metrics, roadmap |
| `artifact.html` | interactive dashboard with live knobs for every modification |

Headline commands:

```bash
python3 test_ring_system.py            # semantics tests
python3 experiments.py                 # E1/E2/E4 metric table
python3 spatial_probes.py              # E5 domain dynamics + invasion
```

The interactive dashboard (each modification is a live toggle) is at
`artifact.html`; to watch the spatial ecology form, enable "local addressing
(H4)" and "protect RULE+addr" with mutation x ~0.3.
