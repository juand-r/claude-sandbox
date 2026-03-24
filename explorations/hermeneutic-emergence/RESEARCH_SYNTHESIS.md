# Research Synthesis: Emergence of Agency from Simple Rules

Consolidated findings from four research surveys covering artificial chemistries,
grid/particle systems, theoretical foundations, and recent ALife (2020-2026).

---

## The Central Unsolved Problem

**No artificial system has achieved open-ended complexification.** Every system
reviewed hits the same wall:

- **Evoloop** only simplifies (smaller loops win)
- **Tierra** stalls after parasites evolve
- **AlChemy's** organizations resist combining into higher-order entities
- **Geb** grows complexity only logarithmically with population size
- **Lenia** creatures have no metabolism, no internal state, no development

The specific failure mode is **major transitions** -- composing lower-level
organizations into higher-level ones (cells into multicellular organisms,
organisms into societies). This is the hardest open problem in ALife and
nobody has cracked it.


---

## Systems Surveyed

### Artificial Chemistries & Digital Evolution

| System | Substrate | Key Finding | Limitation |
|--------|-----------|-------------|------------|
| **AlChemy** (Fontana, 1994) | Lambda calculus expressions in well-stirred reactor | Self-maintaining organizations (autopoietic algebra) emerge | No space, organizations can't compose into higher-order entities |
| **Hutton's Squirm3** (2002) | 2D grid, 6 atom types, 8 reaction rules | Spontaneous self-replication from random soup (~400k iterations) | Converges to minimal replicators (Spiegelman's monster); reaction set too constrained for innovation |
| **Ishida** (2024) | Multiset chemical lattice, 18 molecule types, 2D grid | Claims all four life conditions: bounded structures, replication, metabolism, heritable evolution | 18 types creates interaction space so vast that key reactions can't be identified -- hard to evaluate |
| **Combinatory Chemistry** (Kruszewski & Mikolov, 2020-2024) | Turing-complete rewriting system with conservation laws | Self-reproducing metabolisms from tabula rasa | Still early; open-ended evolution not demonstrated |
| **Tierra** (Ray, 1991) | Machine code in shared memory | Parasites, immunity, hyper-parasitism | Stalls; selects for efficiency only |
| **Avida** (Lenski et al., 2003) | Machine code + logic rewards | Complex functions evolve by building on simpler ones | Innovation space predefined by experimenter |
| **Geb** (Channon, 2001) | Neural networks in spatial world | Only system passing unbounded evolution test | Logarithmic complexity growth; no major transitions |

### Grid-Based & Particle Systems

| System | Substrate | Key Finding | Limitation |
|--------|-----------|-------------|------------|
| **Game of Life** | Discrete binary grid | Turing complete; engineered self-replication | No spontaneous evolution; brittle |
| **Langton's Loops / Evoloop** | Discrete multi-state grid | First evolution in deterministic CA | Only evolves toward simplicity |
| **Lenia** (Chan, 2018) | Continuous field (states, space, time) | 400+ species, naturalistic creatures | No metabolism or genuine evolution (until Flow-Lenia) |
| **Flow-Lenia** (Plantec et al., 2023) | Continuous field + mass conservation | Robust multi-species coexistence, evolutionary dynamics | Still early; no major transitions observed |
| **Primordial Particles** (Schmickl, 2016) | Single-equation particle system | Cell-like structures, membranes, life cycles from ONE equation | No heredity or genuine evolution |
| **ALIEN** (v5, 2024) | GPU particles + neural controllers | Millions of particles, genomes, self-replication | Complex; unclear if emergence or engineering |
| **Neural CA** (Mordvintsev, 2020) | Learned local rules on grid | Self-repair, morphogenesis | Trained, not discovered; limited scale |

### Theoretical Frameworks

| Framework | Core Idea | Relevance to Emergence |
|-----------|-----------|----------------------|
| **Free Energy Principle** (Friston) | Persistent systems minimize surprisal; Markov blankets define agent boundaries | Explains HOW agents emerge but not from WHAT minimal substrate |
| **Constructor Theory** (Deutsch, Marletto) | Physics as possible/impossible transformations; von Neumann replicator logic is unique solution | Constrains what ANY physics must look like to permit life |
| **Assembly Theory** (Cronin) | Assembly index + copy number; high values require selection | Empirically testable complexity measure; controversial |
| **Autopoiesis** (Maturana, Varela) | Self-producing network maintaining its own boundary | Most precise definition of life; cognition IS self-maintenance |
| **Info-Theoretic Individuality** (Krakauer, Flack) | Individual = aggregate propagating info from past to future | Three formal types; quantifiable; scale-free |
| **Basal Cognition** (Levin) | Goal-directed competency at every biological scale | Cognitive light cones; agency is graded and substrate-independent |
| **Enactivism / Hermeneutics** (Varela, Thompson) | Cognition is sense-making, not information processing | Meaning requires embodiment and structural coupling |
| **Chemoton** (Gánti, 1971) | Three stoichiometrically coupled subsystems: autocatalytic metabolism (A₁→A₂→…→2A₁), template polymer (replicates via polycondensation), self-assembling membrane | The clearest architectural template for minimal life. Coupling is purely chemical, no enzymes needed. Metabolic cycle produces precursors for both template and membrane; template replication produces byproduct needed for membrane precursor conversion; membrane growth increases volume until osmotic pressure triggers division. Produces oscillatory dynamics with a stable limit cycle. |
| **Autocatalytic Sets / RAF Theory** (Kauffman; Hordijk & Steel) | Self-sustaining autocatalytic networks undergo a sharp phase transition from absent to almost-certain when each molecule catalyzes ~1-2 reactions. Threshold scales only logarithmically with system size. | Provides a quantitative threshold for when autocatalytic closure becomes likely. RAF theory proves hierarchically nested irreducible subsets (irrRAFs) provide a scaffold for incremental complexity growth. Experimentally validated: Vaidya et al. demonstrated 3-member autocatalytic RNA sets. |
| **Closure of Constraints** (Montévil & Mossio, 2015) | Distinguishes fast thermodynamic processes from slower constraint structures. A constraint acts on a process while being conserved at the process's timescale (e.g., enzyme constrains reaction but remains intact). Closure = constraints are mutually dependent. | Formalizes multi-scale circular causality as what distinguishes biological organization from mere physics. Key insight: biological symmetries are inherently unstable -- unlike physical conservation laws, biological constraints are contingent and historically constituted, which is the basis for genuine novelty. |
| **Chemical Organization Theory** (Dittrich & Speroni di Fenizio, 2007) | An "organization" is a set of molecular species that is algebraically closed (reactions produce only members) and self-maintaining (every species has non-negative production rate). | Every stationary state of a chemical dynamical system corresponds to an organization. Organizations form a lattice; qualitative transitions = movements through this lattice. |

---

## Ten Recurring Failure Modes

A systematic cross-cutting diagnosis of why artificial systems fail to achieve
open-ended evolution:

1. **Reductive evolution** toward minimal replicators (Spiegelman's monster effect)
2. **Organizational closure blocking complexification** (AlChemy's "barrier of objects")
3. **Absence of genotype-phenotype separation** (no dual information role as in von Neumann's architecture)
4. **Missing conservation laws** eliminating resource competition
5. **Homogeneous global rules** preventing species differentiation
6. **No spatial containment** for individuation
7. **Externally defined fitness** (experimenter picks what matters)
8. **Insufficient chemical complexity** (too few reaction types)
9. **Computational limits** (system too small for emergent phenomena)
10. **Gap between self-replication and functional innovation** (copying structure ≠ creating function)

---

## Five Recurring Design Lessons

1. **Continuity matters enormously.** Discrete systems (Life, Langton) produce
   brittle, geometric structures. Continuous systems (Lenia, Primordial Particles)
   produce organic, resilient, naturalistic creatures.

2. **Constructive representations are necessary.** Systems where entities can BUILD
   new kinds of things (AlChemy, Avida) outperform those with fixed possibility
   spaces (Tierra, Particle Life). Open-endedness requires an open-ended space
   of possible entities.

3. **Spatial individuation is necessary.** You need locality to get boundaries,
   membranes, bodies. AlChemy's well-stirred reactor gets organizations but not
   bodies. Hutton's grid gets bodies but not rich algebra.

4. **Conservation laws help a lot.** Flow-Lenia showed that mass conservation
   alone dramatically simplifies the search for interesting patterns. Conservation
   forces trade-offs and prevents entities from appearing/disappearing arbitrarily.

5. **Endogenous fitness beats exogenous.** Tierra/Geb (survive or die) produce
   more naturalistic dynamics than explicit fitness functions. But coevolution
   (parasites, competition) is the most reliable driver of ongoing novelty.

---

## Theoretical Convergences

All six theoretical frameworks agree on:

- **Agency is graded, not binary.** From minimal autopoietic cell to reflective
  organism. No sharp threshold.

- **Boundaries are fundamental.** Markov blankets (FEP), membranes (autopoiesis),
  formation histories (assembly theory), information channels (Krakauer/Flack).
  The self/non-self distinction is where agency begins.

- **Information is physical.** Constructor theory, assembly theory, and
  info-theoretic individuality all treat information as having causal
  consequences -- not an abstraction on top of physics.

- **Meaning requires embodiment.** The enactivist/hermeneutic tradition insists
  genuine interpretation requires structural coupling to an environment.
  Varela originally called enactivism "the hermeneutic approach."

---

## Origins-of-Life Validation

Real chemistry provides three lessons that abstract artificial chemistries
have historically ignored:

**1. Boundaries come cheap, coupling is hard.** Szostak's protocell research
shows fatty acid vesicles self-assemble spontaneously above critical micelle
concentration, grow by incorporating micelles, and divide under modest shear
forces without losing internal contents. Fatty acid membranes are naturally
permeable to charged nucleotides. Rasmussen's "Los Alamos Bug" shows even a
simple oil droplet suffices as a container. The hard part is not making
boundaries but coupling boundary production to an internal reaction network.

**2. Autocatalytic sets emerge more easily than intuition suggests.** Hordijk
and Steel's RAF theory proves self-sustaining networks undergo a sharp phase
transition when catalytic probability exceeds ~1/n² (n = number of molecule
types). For 10-20 molecule types, each molecule needs to catalyze only 1-2
reactions. Experimentally validated: Vaidya et al. demonstrated 3-member
autocatalytic RNA sets where each ribozyme catalyzes the next.

**3. The metabolism-first vs. replicator-first debate resolves in favor of
coupling.** Pure metabolism-first (Kauffman, Wächtershäuser) creates
self-sustaining but potentially non-evolvable systems -- Vasas et al. (2010)
proved compositional inheritance in autocatalytic networks is too inaccurate
for Darwinian selection. Pure replicator-first (RNA world) creates evolvable
but fragile systems. The chemoton resolves this by integrating metabolic
closure for robustness with template replication for evolvability, connected
through a self-produced boundary.

---

## Computational Search Methodology

The meta-problem -- how to navigate the vast space of possible artificial
chemistries -- has shifted from intractable to merely difficult.

### Quality-Diversity Algorithms

MAP-Elites and AURORA (unsupervised QD) can evolve diverse populations of
artificial life forms. Leniabreeder (Faldor & Cully, ALIFE 2024) applied
AURORA to Lenia, using a VAE to automatically learn a latent descriptor space
(eliminating human-defined diversity metrics). Population of 32,768 evolved
via QDax framework on GPU-accelerated JAX. Discovered patterns that random
search and human exploration missed.

### Foundation-Model-Driven Search (ASAL)

Sakana AI's ASAL uses CLIP as a proxy for "interestingness." Three modes:
supervised target search (optimizing toward text prompts), open-endedness
search (finding systems with persistently novel CLIP trajectories), and
illumination search (maximizing diversity). Discovered CAs more open-ended
than Game of Life and previously unknown Lenia lifeforms. Substrate-agnostic:
works across Boids, Particle Life, GoL, Lenia, Neural CA.

### Curiosity-Driven Goal Exploration (IMGEP)

Oudeyer group (Inria). Algorithm self-generates goals in behavioral metric
space, selects similar past configurations, mutates parameters, discovers
diverse behaviors. Applied to Flow-Lenia: discovered feeding behaviors,
allopatric speciation analogues, complex ecology that random search missed.
Key innovation: CPPNs for structured initialization (avoids white-noise
initial conditions that produce only dead or global patterns).

### JAX Ecosystem

JAX has become the dominant framework for scalable ALife. Key tools:
- **CAX** (ICLR 2025 Oral): GPU-accelerated CA library, up to 2,000x speedup
- **JAX MD**: differentiable molecular dynamics, spatial partitioning primitives
- **Leniax**: JAX-powered, fully differentiable, supports QD search
- **Flow Lenia**: JAX, mass-conservative, parameter localization
- **ALIEN**: C++/CUDA, millions of particles, won ALIFE 2024 Virtual Creatures
- **DiffTaichi**: 188x faster than TensorFlow for differentiable physics

Differentiability is a major advantage -- JAX auto-differentiation through
simulation steps enables meta-optimization of interaction rules and
gradient-based search through parameter space.

### Measuring "Interestingness"

No single metric suffices (Hickinbotham & Stepney, 2024). Hintze (2019) showed
a trivial system can satisfy all proposed OEE requirements while remaining
subjectively uninteresting. Most productive approach combines: evolutionary
activity statistics (Bedau), compression-based complexity, transfer entropy,
and assembly-index-like construction complexity. Foundation model embeddings
(CLIP, DINOv2) outperform pixel-level metrics for capturing human notions of
diversity but introduce their own biases.

---

## The Design Gap

No existing system satisfies all the conditions needed for rich emergence:

| Condition | AlChemy | Lenia | Particles | Tierra | Geb |
|-----------|---------|-------|-----------|--------|-----|
| Composability | Yes | No | No | Partial | Partial |
| Locality | No | Yes | Yes | No | Yes |
| Conservation | No | Flow-Lenia | No | Yes (CPU) | No |
| Continuity | No | Yes | Yes | No | No |
| Constructiveness | Yes | No | No | Partial | Partial |
| Endogenous fitness | Yes | N/A | N/A | Yes | Yes |

**The gap**: composable computations + locality + conservation + continuity +
constructiveness + endogenous fitness. No system combines all six.

---

## Possible Substrate Directions

Based on the research, several abstract substrates could potentially fill the gap:

1. **Lambda calculus on a dynamic graph** (AlChemy + topology) -- programs that
   interact locally based on graph distance, with the graph itself evolving.
   Gets composability + locality, but unclear how to add continuity.

2. **Interaction combinators** (Lafont) -- computation IS graph rewriting with
   built-in locality. Close to Wolfram's hypergraph physics but at a higher
   abstraction level. Composable by construction.

3. **Continuous particle chemistry** -- particles carrying internal state
   (programs/automata) that interact based on proximity and exchange/transform
   state. Like Primordial Particles but with constructive internal computation.
   Gets continuity + locality + conservation.

4. **Rewriting systems on metric spaces** -- abstract rewriting rules operating
   on entities embedded in a continuous space with conserved quantities.
   Geometry emerges from interaction patterns.

5. **Token economies on graphs** -- entities exchange abstract tokens according
   to local rules. Conservation built into exchange. Composability from
   combining token-processing strategies.

### The geometry question

Do we need geometry at all?

- **AlChemy proves**: autopoiesis doesn't require geometry (pure algebra suffices)
- **Wolfram shows**: geometry CAN emerge from pure topology
- **Lenia shows**: continuity dramatically enriches dynamics
- **Primordial Particles show**: even one equation in continuous space gets cells

Conclusion: we probably need at minimum a **topology** (connectivity structure)
that can support locality. A fixed metric geometry is likely too rigid; a
dynamic topology with emergent metric properties may be the sweet spot.

---

## Key References

### Artificial Chemistries
- Fontana & Buss, "The Arrival of the Fittest" (1994)
- Mathis et al., "Return to AlChemy" (Chaos, 2024)
- Hutton, "Evolvable Self-Replicating Molecules" (Artificial Life, 2002)
- Ishida, "Multiset Chemical Lattice Model" (2024)
- Kruszewski & Mikolov, "Combinatory Chemistry" (2020-2024)
- Gánti, "The Principles of Life" (1971/2003)
- Ono & Ikegami, "Artificial chemistry: computational studies on the emergence of self-reproducing units" (2001)

### Grid/Particle Systems
- Chan, "Lenia: Biology of Artificial Life" (arXiv, 2018)
- Plantec et al., "Flow-Lenia" (ALIFE 2023 Best Paper; Artificial Life, 2025)
- Schmickl et al., "Primordial Particle Systems" (Scientific Reports, 2016)
- Mordvintsev et al., "Growing Neural Cellular Automata" (Distill, 2020)
- Sayama & Nehaniv, "25 Years After Evoloops" (Artificial Life, 2025)

### Digital Evolution
- Ray, "An Approach to the Synthesis of Life" (1991)
- Lenski et al., "Evolutionary Origin of Complex Features" (Nature, 2003)
- Channon, "Maximum Individual Complexity is Indefinitely Scalable" (Artificial Life, 2019)

### Theoretical Foundations
- Friston, "A Free Energy Principle for a Particular Physics" (2019)
- Marletto, "Constructor Theory of Life" (J. R. Soc. Interface, 2015)
- Cronin et al., "Assembly Theory Explains Selection and Evolution" (Nature, 2023)
- Maturana & Varela, "Autopoiesis and Cognition" (1980)
- Krakauer et al., "Information Theory of Individuality" (Theory in Biosciences, 2020)
- Fields & Levin, "Thoughts and Thinkers" (Physics of Life Reviews, 2025)
- Gallagher & Allen, "Active Inference, Enactivism and Hermeneutics" (Synthese, 2018)
- Montévil & Mossio, "Biological organisation as closure of constraints" (J. Theoretical Biology, 2015)
- Dittrich & Speroni di Fenizio, "Chemical Organisation Theory" (Bulletin of Mathematical Biology, 2007)
- Kauffman, "The Origins of Order" (1993)
- Hordijk & Steel, "Detecting autocatalytic, self-sustaining sets in chemical reaction systems" (J. Theoretical Biology, 2004)
- Vasas et al., "Evolution before genes" (Biology Direct, 2010)

### Origins of Life
- Szostak, "Protocell models" (various, 2001-2020)
- Rasmussen et al., "Transitions from Nonliving to Living Matter" (Science, 2004)
- Vaidya et al., "Spontaneous network formation among cooperative RNA replicators" (Nature, 2012)

### Computational Search
- Faldor & Cully, "Leniabreeder" (ALIFE, 2024)
- Hickinbotham & Stepney, "Measuring open-endedness" (Artificial Life, 2024)
- Hintze, "Open-ended evolution and trivial systems" (2019)
- Oudeyer et al., IMGEP / curiosity-driven exploration (various)

### Recent ALife
- Kumar et al., "ASAL: Automated Search for Artificial Life" (arXiv, 2024)
- Rosas et al., "Software in the Natural World" (arXiv, 2024)
- ALIEN project: https://www.alien-project.org/

### Surveys
- Bedau et al., "Open Problems in Artificial Life" (Artificial Life, 2000)
- Channon et al., "OEE Special Issue" (Artificial Life, 2024)
- Gershenson, "Emergence in Artificial Life" (Artificial Life, 2023)

---

*Compiled 2026-03-23 from four parallel research surveys. Updated 2026-03-24
with chemoton architecture, coupling thesis, Kauffman/RAF thresholds, closure
of constraints, origins-of-life validation, computational search methodology,
and ten failure modes (sourced from "Designing Minimal Artificial Chemistries"
report).*
