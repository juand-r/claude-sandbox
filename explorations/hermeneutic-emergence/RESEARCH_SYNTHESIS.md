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
| **Hutton's Squirm3** | 2D grid atoms with bonds | Self-reproducing cells with membranes | Evolution plateaus quickly |
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

### Recent ALife
- Kumar et al., "ASAL: Automated Search for Artificial Life" (arXiv, 2024)
- Rosas et al., "Software in the Natural World" (arXiv, 2024)
- ALIEN project: https://www.alien-project.org/

### Surveys
- Bedau et al., "Open Problems in Artificial Life" (Artificial Life, 2000)
- Channon et al., "OEE Special Issue" (Artificial Life, 2024)
- Gershenson, "Emergence in Artificial Life" (Artificial Life, 2023)

---

*Compiled 2026-03-23 from four parallel research surveys.*
