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

A later modification removes what first looked like the system's defining
limitation. Heredity does **not** have to be imposed: gating reproduction on
self-consistency (a ring's ability to survive its own rule) makes
heredity-compatibility *emerge* through selection, with no bits protected
(self-preservation rises from chance, 0.52, to ~1.0). And --- once measured
correctly --- this same modification, run spatially, produces emergent
**domains of identical, self-consistent genomes** (neighbour genome-identity
~16x chance, robust across seeds, nothing protected). Emergent individual
heredity and emergent spatial structure turn out to be the *same* phenomenon,
not two halves to be bridged. (An earlier draft reported the spatial version as
"unstructured"; that was a measurement error --- Moran's I on categorical rule
numbers --- corrected in Reflection R1.)

On top of this, emergent heredity unlocks **robust adaptation**: a directional
selective gate that imposed heredity could push only weakly (and fatally ---
E2/E3 went extinct) drives a trait from chance to near-fixation (0.06 -> ~0.75,
every seed, no extinction) once self-templating makes the whole genome reliably
heritable. So the full chain the project set as its success criterion ---
persistence, heredity, adaptation --- now holds, all on emergent (not imposed)
heredity.

The `selftmpl_local` regime is also **sustainably open-ended in novelty**: over
8000 ticks its rate of never-before-seen genomes decays through a transient and
then plateaus near 0.18 (flat, not freezing), with cumulative diversity growing
without bound --- it keeps discovering new self-consistent genomes indefinitely.
But this open-endedness has a hard **ceiling**: complexity does *not* grow. Every
complexity proxy plateaus by ~t=2000 and merely fluctuates thereafter; the
system explores a fixed-complexity manifold forever (E13). Trying to break the
ceiling (B7/B8) revealed it is **layered, with three distinct causes** (E14/E15):
a passive cap (the fixed genome --- removed by allowing variable length); an
active downward gradient (self-consistency selects for *short* programs, so
without counter-pressure complexity collapses to the floor); and, underneath, a
**representational wall** --- even when a task directly rewards complexity, the
length lifts only slightly (1 -> ~2.5 rules) and stalls, because sequences of
elementary CA rules do not *compose smoothly* toward richer behaviour. The deep
cause is the primitive itself (8-bit ECA rules are chaotic and non-composable),
not any tuning. Open-ended complexity growth would require a different,
composable primitive --- essentially a different substrate.

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

### 1.1 Scope note --- what system, and is the grid real? (read this first)

Two points that govern how to read everything below:

- **Most results are about *modified* variants, not the faithful spec.** The
  faithful spec is only the E1 baseline (and it is pure churn). Every later
  finding switches on one or more modifications --- imposed or emergent
  heredity, local addressing, self-templating, and so on. They default off, so
  the faithful system is recovered by turning them all off. The full knob list
  and which experiment introduced each is in `DESIGN.md` section 10.

- **The grid is cosmetic by default and only becomes real space under "local
  addressing."** In the faithful spec, the PULL/PUSH addresses are *absolute
  slot indices*: the universe is 256 arbitrarily-wired slots with no geometry,
  and the 16x16 grid is just a way to draw them (adjacent cells are not
  neighbours). The "H4" modification (`local_addr`) reinterprets addresses as
  **(dx, dy) offsets on a 2-D torus**, at which point the grid is genuine space
  and adjacency drives the dynamics. **Every spatial claim in this report ---
  domains, the neighbour-identity metric, "spirals" --- is from local-addressing
  runs**, where the geometry is real; the metric counts pairs adjacent *on the
  torus*, not in the display. See `DESIGN.md` section 3.7. (Sanity check: the
  same render shows noise with local addressing off and domains with it on, so
  the structure cannot be a display artifact.)

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
their own transformation. Well-mixed, the population collapses to a near-frozen,
low-diversity clone (preservation ~1.0, activity ~9 bits/tick, 2--14 rules) ---
heredity emerges, but as a single trivial fixed point. Spatially (local
reproduction), it does something far more interesting: it forms **emergent
domains of identical, self-consistent genomes**.

> **Evidence (corrected metric).** Neighbour genome-identity is 0.15--0.19
> versus a chance rate ~0.012 --- a 14--18x enrichment, robust across five
> seeds and building up over time, with nothing protected. (E6 re-measured;
> Reflection R1.) The imposed-heredity domains of E4, by contrast, are only
> *rule*-uniform (their action bits churn), enriching genome-identity a mere
> ~4x.

The earlier claim that the spatial case was "unstructured" was a measurement
artifact: Moran's I treats rule numbers as ordinal, so it scores ~0 on a grid
tiled with categorically-identical genomes whose rule *numbers* happen to be
scattered. The lesson --- match the statistic to the variable's type --- is
logged in Reflection R1.

So self-templating delivers both at once: heredity the system discovers itself,
*and* the spatial domain structure that makes it interesting, with nothing
supplied by us.

### 3.7 Adaptation, open-ended novelty --- and a complexity ceiling

Three further results complete the picture of what the emergent-heredity regime
can do.

**Adaptation (E10).** Emergent heredity makes *directional* selection work where
imposed heredity could not. The same heritable-key gate that imposed heredity
pushed only to ~0.11 (and that drove E3 extinct) drives the trait from chance
(0.06) to ~0.75 across every seed, population stable, once self-templating makes
the whole genome reliably heritable. Reliable heredity was the precondition
selection needed all along. With this, the full ladder of section 2 ---
persistence, heredity, adaptation --- holds on emergent heredity.

**Open-ended novelty (E12).** Over 8000 ticks the spatial self-templating regime
keeps producing never-before-seen self-consistent genomes: novelty decays
through a transient and then *plateaus* at ~0.18 (flat slope), with cumulative
diversity growing without bound. It is sustainably open-ended in novelty ---
neither freezing (the well-mixed clone) nor structureless noise (the baseline).

**But not in complexity (E13--E15).** Complexity does not grow. Every complexity
proxy plateaus early; the system roams a fixed-complexity manifold. Pushing on
this (a variable-length "rule program" variant, where transformation is a
sequence of CA rules whose length can mutate) showed the ceiling is **layered**:
allowing genome growth makes program length *collapse* to the floor, because
self-consistency selects for short programs (E14); adding a task that directly
rewards complexity lifts length only slightly and then stalls (E15), because
sequences of chaotic elementary-CA rules do not *compose smoothly* toward a
target. The deepest cause is the primitive itself --- the 8-bit CA rule is not
composable --- so open-ended complexity would require a different substrate, not
a tuning change.

### 3.8 Spatial competition: cyclic coexistence and waves

Beyond domains, the spatial medium supports **frequency-dependent** ecology. With
rock-paper-scissors competition among three *symmetric, heritable* types (each
overwrites the type it beats), the system reaches balanced three-type
coexistence with interlocking domains and travelling boundaries --- the spatial
RPS regime (E16). An earlier attempt (E11) failed to show this only because its
types (rule mod 3) had unequal viability; symmetry was the missing ingredient,
not a substrate limitation. (Crisp large spirals would need a bigger grid and
lower noise; the coexistence-with-waves structure is clear at 64x64.)

## 4. Synthesis

Two threads run through every result.

**Heredity is the universal bottleneck.** In the well-mixed system it blocks
selection (3.1, 3.3); in the spatial system its presence is exactly what
distinguishes the configuration that organizes from the ones that do not
(3.4). Wherever the system fails to organize, the proximate cause is that
nothing is stably inherited; wherever it succeeds, heredity has been imposed by
protecting bits.

**Emergent heredity and emergent spatial structure are one phenomenon.**
Self-templating (selection for surviving one's own rule) makes self-consistency
emerge, and spatially this *is* domain formation: neighbourhoods of identical
self-consistent genomes, nothing protected (3.6). The earlier belief that these
were two separate achievements to be bridged was an artifact of a wrong metric
(Moran's I on categorical rules); the categorical neighbour-identity metric
shows them as the same thing. Imposed protection (3.4) gives a different,
shallower object --- domains uniform in rule but churning in their action bits.

**The substrate climbs the whole ladder except complexity.** The answer to the
original question: the faithful system does not self-organize; surgical heredity
buys fragile selection; and **self-templating in a spatial medium produces
emergent domains of self-consistent genomes, robust directional adaptation, and
sustained open-ended novelty --- heredity the system discovers itself, expressed
as spatial structure, with nothing supplied by us.** It also supports a
frequency-dependent ecology (cyclic coexistence with waves). The one thing it
does *not* do is grow in complexity: it explores a fixed-complexity manifold
forever, and the cause is the non-composable CA primitive, not a missing tweak.
The one strong claim it does not earn is autopoiesis: the domains are dynamic
clusters maintained by spatial separation and renewal, not structures shown to
defend themselves.

## 5. Limitations

- **Complexity does not grow** (E13--E15) --- the substrate's primitive is not
  composable. Every "open-ended" claim here is about *novelty*, not complexity.
- **Autopoiesis is not demonstrated** --- the emergent domains are dynamic
  clusters, not shown to actively self-maintain; the invasion probe is
  underpowered (3.5).
- **The reproduction key reuses the ORDER field's low nibble**, mildly
  conflating composition rank with reproduction eligibility. A dedicated field
  would remove this; deferred until it matters.
- **Sample sizes are small.** Most results are 3--5 seeds. Magnitudes are
  indicative; the qualitative separations are robust, fine-grained numbers less.
- **Mutation-rate magnitudes were chosen, not tuned**, and could shift the
  regime boundaries.
- **Many results use modifications, not the faithful spec** (section 1.1); only
  E1 is the faithful system.

## 6. Conclusions

The investigation set out to ask whether the Adaptive Ring System produces
emergent adaptive self-organization, and what modifications make it do so. After
sixteen experiments and four reflection rounds, the answer is clear and largely
positive, with one sharp boundary.

1. **The faithful system does not self-organize.** It is high-entropy churn with
   no unit of heredity --- a structural consequence of transformation rewriting
   the whole genome every tick (3.1).

2. **Heredity is the master key.** Every capability the system can show is
   unlocked the moment genomes can reliably persist, and blocked whenever they
   cannot (3.2). This single fact organizes every result.

3. **Heredity, spatial structure, adaptation, and open-ended novelty all emerge
   together** from one minimal modification --- *self-templating* (rewarding
   rings that survive their own rule) in a *local* (spatial) medium, with
   nothing protected by us (3.6, 3.7). This is the headline success: the system
   discovers its own heredity and expresses it directly as emergent genome
   domains, supports robust directional adaptation, and sustains open-ended
   novelty.

4. **The substrate has a hard ceiling at complexity** (3.7). It never
   complexifies; the cause is the non-composable elementary-CA primitive, shown
   by removing the other obstacles and watching complexity still refuse to grow.
   Open-ended complexity is beyond this substrate by design.

5. **A methodological lesson** (R1): a wrong metric (Moran's I on categorical
   rule numbers) produced a confident false negative that stood for two
   experiments. Matching the statistic to the variable's type overturned it.
   Logged because it nearly buried the project's central result.

The original question is answered: adaptive self-organization *does* arise, and
the modifications that produce it are, in order of necessity, **locality** and
**heredity** (best supplied emergently, by self-templating). What does not arise
is open-ended complexity growth.

## 7. Future directions

Within the ring system (incremental):

- **Coevolution / escalating pressure** --- replace the static key/task with
  goalposts set by other rings, to seek non-plateauing adaptation.
- **Stronger autopoiesis probe** --- size-matched domains, many rule pairs, a
  neutral rule-relabeling null, to settle whether any emergent domain
  self-maintains.
- **Robustness / regime maps** --- systematic sweeps over grid size,
  neighbourhood, mutation, range.

Beyond the ring system (a deliberate new substrate):

- **A composable primitive** --- the only route to open-ended *complexity* is to
  replace the elementary-CA rule with operations that compose smoothly and
  richly (an Avida-adjacent instruction set). This is a new project, not a
  modification, and should be chosen deliberately (it is the standing "option 3"
  in the project's planning).

## 8. Reproducibility

| file | role |
|------|------|
| `ring_system.py` | fixed-length simulator; knobs default to the faithful spec |
| `growth.py` | variable-length "program ring" variant (E14--E15) |
| `test_ring_system.py` | 12 tests of the load-bearing semantics |
| `analyze.py` | discriminating metrics + nulls (incl. neighbour-identity) |
| `experiments.py` | the E1/E2/E4/E6/E7 config battery and comparison table |
| `spatial_probes.py` | E5/E8 domain-trajectory and invasion probes |
| `EXPERIMENTS.md` | per-experiment log (E1--E16 + R1--R4), full detail |
| `TRAJECTORY.md` | the tree of explored paths |
| `DESIGN.md` | faithful spec + addressing modes + knob table |
| `RESEARCH_PLAN.md` | operational definitions, metrics, roadmap |
| `artifact.html` | interactive dashboard with live knobs + findings guide |

Headline commands:

```bash
python3 test_ring_system.py            # semantics tests
python3 experiments.py                 # E1/E2/E4 metric table
python3 spatial_probes.py              # E5 domain dynamics + invasion
```

The interactive dashboard (each modification is a live toggle) is at
`artifact.html`; to watch the spatial ecology form, enable "local addressing
(H4)" and "protect RULE+addr" with mutation x ~0.3.
