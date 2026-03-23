# Emergent Behavior in Grid-Based and Cellular Automata Systems

Research report covering systems where complex behavior (self-replication, agent-like behavior, evolution) emerges from simple local rules.

---

## 1. Conway's Game of Life

### Primitives
- 2D grid, binary cell states (alive/dead)
- 4 rules based on neighbor count: underpopulation (<2 dies), survival (2-3 lives), overpopulation (>3 dies), reproduction (exactly 3 births)

### What Emerged
- **Turing completeness**: Conway proved in 1982 that Life contains a universal computer. Paul Rendell built an explicit Turing machine in Life in 2000. Any computable function can be implemented.
- **Gliders and spaceships**: Moving patterns that transport information across the grid. Gliders are the fundamental information carriers enabling logic gates, counters, and memory.
- **Self-replication milestones**:
  - **Gemini (2010)**: Andrew Wade's first self-replicating creature. Two sets of identical structures connected by a glider instruction tape. Replicates every 34 million generations. Technically a spaceship -- it copies its replicator units but not the full pattern simultaneously.
  - **First true replicator (2013)**: Dave Greene built a replicator of 145,306 live cells that creates a complete copy of itself including the instruction tape.
  - **0E0P Metacell (2018)**: Adam P. Goucher's metacell capable of self-replication using construction arms, unlike previous metacells (OTCA metapixel) that required pre-existing copies nearby.
- **Universal constructors**: A universal constructor parameterized solely by the positions of 329 gliders (Goldtiger997, 2018).

### Key Insights
- Complexity and organization emerge from extreme simplicity -- 4 rules on a binary grid produce universal computation.
- Self-replication in Life required decades of engineering effort. The structures are enormous (hundreds of thousands of cells) and slow (millions of generations).
- Daniel Dennett used Life extensively to argue that consciousness and free will could emerge from simple deterministic physical laws.

### Limitations
- Self-replication is engineered, not emergent. Nobody has observed spontaneous evolution within standard Life.
- The discrete, synchronous nature makes natural-looking structures difficult.
- Patterns are brittle -- collisions typically destroy rather than create.

---

## 2. Langton's Loops and Variants

### Primitives
- 2D grid, 8 states (Langton's original), 5-neighbor (von Neumann) neighborhood
- Explicit transition rules (thousands of entries in a lookup table)
- Loops carry an "instruction tape" encoded in cell states that directs arm extension and turning

### What Emerged

#### Langton's Loop (1984)
- A loop of 86 cells that extends an arm, which turns and closes into a copy of the original loop. The copy then repeats the process.
- Langton's key insight: universal construction is *sufficient* for self-replication but *not necessary*. Much simpler machines can replicate if that is their only function.
- Limitation: loops fill the grid and then freeze. No death, no competition, no evolution.

#### Byl's Loop
- Reduced to 6 states and 12 cells. Simpler, same basic behavior.

#### Chou-Reggia Loops
- Further miniaturization. Smallest demonstrated: 5 cells in 6-state space. Most are unsheathed (no protective outer layer), unlike Langton and Byl.

#### Sayama's SDSR Loop (1998)
- Added a "dissolving state" (state 8) to Langton's rules. Loops can now dissolve when they run out of space.
- First time loops showed dynamically stable population behavior rather than just filling up and freezing.

#### Sayama's Evoloop (1999)
- Built on SDSR. Key improvement: enhanced adaptability of the self-reproductive mechanism.
- **Actual evolution occurred**: loops varied through direct phenotype interaction, smaller loops were naturally selected (faster reproduction), and the population gradually evolved toward minimal size.
- No mechanism was explicitly provided to promote evolution -- it emerged from the dynamics.
- Meets both Langton's and von Neumann's criteria for self-reproduction (viable inheritable variation).
- 2024 marked the 25th anniversary; Sayama and Nehaniv published a retrospective in *Artificial Life* (2025).

#### Sexyloop (Oros & Nehaniv)
- Modified evoloop to allow transfer of genetic material between loops -- sexual reproduction in a cellular automaton.

### Key Insights
- There is a clear progression from pure self-replication (Langton) to death-capable (SDSR) to evolving (Evoloop).
- Evolution requires: variation, differential reproduction, and heredity. Evoloop achieved all three in a deterministic CA.
- The evolving populations converge toward simplicity (smallest viable replicator), which is a genuine result of selection pressure for reproductive speed.

### Limitations
- Evolution is one-directional: toward smaller, simpler loops. There is no complexification.
- The loops cannot do anything *other* than replicate. No computation, no sensing, no behavior beyond copying.
- The rule tables are handcrafted and large (hundreds of transition rules). There is no way to discover them from scratch.

---

## 3. Lenia

### Primitives
- Continuous generalization of Game of Life: continuous states (0.0 to 1.0), continuous space, continuous time
- Each cell updates based on a kernel function (weighted sum of neighborhood) passed through a growth function
- Parameters: kernel radius, kernel shape (ring-like), growth function (Gaussian bump), time step

### What Emerged

#### Species Diversity
- Over 400 species in 18 families discovered, many via interactive evolutionary computation
- Families include: Orbidae, Scutidae, Pterifera, Helicidae, Kronidae, Ctenidae, Circidae, Dentidae, Lapillidae, Quadridae, Volvidae, Bullidae, Radiidae, Folidae, Geminidae, Uridae, and others
- **Orbium**: the "glider" of Lenia -- a moving orb, the simplest creature. Not very robust to collisions.
- Complex species show bilateral symmetry, radial symmetry, metameric (segmented) body plans
- Examples: *Asterium rotans* (radial), *Hydrogeminium natans* (bilateral), *Pentapteryx* (long-chain)

#### Behavioral Properties
- **Self-organization**: creatures form spontaneously from random initial conditions
- **Self-repair**: some creatures can recover from perturbation
- **Locomotion**: creatures move through their environment
- **Sensorimotor behavior**: more complex creatures change direction in response to other creatures
- **Self-replication**: some parameter regimes produce replicating patterns
- **Intercommunication**: colonies of creatures show coordinated behavior

#### Parameter Space Structure
- Four landscape classes: (1) homogeneous desert, (2) cyclic savannah, (3) chaotic forest, (4) complex river
- Creatures exist at the boundary between order and chaos (echoing Langton's "edge of chaos")
- Much of parameter space remains unexplored

### Recent Developments

#### Flow-Lenia (2025)
- Mass-conservative extension: matter is neither created nor destroyed, only flows
- Spatial localization is intrinsic (no need to explicitly constrain it)
- Enables multispecies simulations with parameters embedded in the dynamics itself
- Shows emergent evolutionary dynamics measured via evolutionary activity framework
- Authors: Plantec, Hamon, Etcheverry, Chan, Oudeyer, Moulin-Frier (*Artificial Life*, 2025)

#### Asymptotic Lenia (2024)
- Analytically continuous formulation supporting systematic emergence of solitons, oscillators, rotors, chaotic organisms
- Quality-diversity algorithms (MAP-Elites, AURORA) drive sustained discovery of novel patterns
- Interpreted as open-ended evolution in parameter/behavior space

#### ASAL (Sakana AI, 2024)
- Automated Search for Artificial Life using vision-language foundation models
- Applied to Lenia (and other substrates): discovers diverse self-organizing patterns without human guidance
- Found previously unknown lifeforms

### Key Insights
- Continuity matters enormously. The move from discrete to continuous states/space/time produces far more natural, organic-looking creatures.
- Lenia creatures genuinely resemble microscopic organisms (radiolaria, diatoms, amoebae) despite having no biological basis.
- The parameter space is vast and mostly uncharted. Discovery is an ongoing process, not a solved problem.

### Limitations
- Evolution within Lenia is not spontaneous in standard formulations -- creatures don't naturally mutate and compete (until Flow-Lenia).
- Discovery historically required human-guided search or explicit optimization algorithms.
- Creatures are simple compared to biological organisms -- no metabolism, no internal state, no development.

---

## 4. Particle Life / Clusters

### Primitives
- N particles in continuous 2D space, each belonging to a "species" (color)
- Between each pair of species: an attraction/repulsion force as a function of distance
- Parameters per species pair: attraction strength, attraction range, repulsion strength, repulsion range
- Particles move under these forces (with friction/damping)

### Key Systems

#### Clusters (Jeffrey Ventrella)
- Original system. Particles divided into groups with species-specific interaction rules.
- Simple attraction-repulsion produces "breathtaking behaviors" -- organisms that appear alive.

#### Particle Life (Tom Mohr)
- Interactive desktop app inspired by Ventrella's Clusters
- GUI controls for real-time parameter tuning
- Open source (Java)

#### Primordial Particle Systems (Schmickl et al., 2016)
- Published in *Scientific Reports*. Single motion law for self-propelled particles.
- What emerged:
  - **Cell-like structures** with distinct membranes
  - **Spores** that bud off from cells
  - **Life cycles**: cells grow, reproduce, and die
  - **Ecosystems**: populations follow logistic growth models
  - **Homeostasis**: structures self-stabilize over long periods
  - **Nutrient dynamics**: cells intake and lose free particles
- A "Region of Life" exists in parameter space where these structures appear
- Key difference from Life: no spatial discretization, no synchronized time steps -- produces far more natural structures

#### Hunar Ahmad's Particle Life
- Educational implementation showing that "complexity can arise from simplicity"
- Code described as "probably an order of magnitude simpler than any other Artificial Life code"

### What Emerges (across these systems)
- Chains and filaments
- Cell-like enclosed structures with membranes
- Self-reproducing cellular structures
- Predator-prey dynamics between species
- Symbiotic clusters
- Rotating and oscillating structures

### Key Insights
- Continuous space + multiple species + simple force laws = rich emergent ecology
- The Primordial Particle System is notable for producing genuine life cycles and ecosystems from a single equation
- These systems are highly accessible and visually compelling, good for building intuition about emergence

### Limitations
- No genuine heredity or evolution (structures don't have genomes that mutate)
- Behavior is determined entirely by global parameters, not individual variation
- The "Region of Life" in parameter space is not well understood
- Emergent structures, while life-like in appearance, lack internal computation

---

## 5. Neural Cellular Automata (NCA)

### Primitives
- Grid of cells, each with a state vector (multiple channels)
- Update rule is a small neural network (shared across all cells) that takes local neighborhood as input
- The neural network is trained via gradient descent to produce target behaviors
- Each cell perceives only its immediate neighbors

### What Emerged

#### Growing NCA (Mordvintsev et al., 2020)
- Published in *Distill*. A single cell grows into a target image (e.g., a lizard emoji).
- The system shows:
  - **Self-repair**: damage is repaired because each cell locally "knows" what pattern it should be part of
  - **Robustness**: works despite noise, cell death, perturbation
  - **Morphogenesis**: mimics biological development from a single cell

#### Key Properties
- **Self-regeneration**: damaged patterns regrow
- **Generalization**: robustness to unseen perturbations
- **Spontaneous motion**: some NCA produce moving patterns without being trained to

### Recent Developments (2023-2025)

#### Growing Steerable NCA (2023)
- Cells can control their own orientation. Introduces chirality (handedness).

#### MeshNCA (2024)
- Extended to 3D surfaces. Outperforms other methods for 3D texture synthesis.

#### Differentiable Logic Gate NCA (2025)
- Miotti, Niklasson, Randazzo, Mordvintsev showed NCA rules can be implemented with differentiable logic gates
- First successful application of differentiable logic gate networks in recurrent architectures
- Step toward programmable matter and robust computing on standard digital hardware

#### CAX: Cellular Automata Accelerated in JAX (ICLR 2025)
- Framework integrating ML with cellular automata
- Combines NCA with CNNs, Graph Neural Networks, Vision Transformers

#### Path to Universal NCA (2025)
- Work toward NCA that can grow arbitrary target patterns from a single model

### Key Insights
- NCA invert the usual CA paradigm: instead of handcrafting rules and observing what emerges, you specify the *target* and learn the rules.
- The emergent self-repair property is not explicitly trained -- it arises naturally from the local-only communication constraint.
- NCA are a bridge between biological morphogenesis and engineered self-organizing systems.

### Limitations
- Mostly confined to low-resolution grids (128x128 or smaller) due to quadratic training costs
- Strictly local information propagation limits what can be learned
- The relationship between NCA weights and emergent behavior is highly nonlinear -- hard to interpret or predict
- NCA are *trained* systems, not discovery systems. The emergence is in the self-repair and robustness, not in the generation of novel creatures.

---

## 6. Other Notable Systems

### SmoothLife
- Continuous-space, continuous-state generalization of Life (independent from Lenia, but strikingly similar)
- Circular "blobs" with neural network brains
- Blobs that survive longer spread their chromosomes -- genuine evolutionary dynamics

### Swarm Chemistry (Sayama)
- Multiple types of kinetically interacting particles with different properties
- Produces dynamic structures and behaviors spontaneously
- Used as a framework for morphogenetic artifacts that grow, self-organize, and self-repair

### ASAL Framework (Sakana AI, 2024)
- Uses vision-language foundation models to automate ALife discovery across multiple substrates
- Applied to: Boids, Particle Life, Game of Life, Lenia, Neural Cellular Automata
- Found novel CA rules more open-ended than standard Game of Life
- Discovered previously unknown Lenia lifeforms
- Represents a paradigm shift: using AI to search for artificial life, rather than hand-designing it

---

## Cross-Cutting Themes

### The Spectrum from Engineered to Emergent
| System | Rules | Emergence | Evolution |
|--------|-------|-----------|-----------|
| Game of Life | Handcrafted, simple | High (Turing complete) | None (spontaneous) |
| Langton's Loops | Handcrafted, complex tables | Low (only replication) | None |
| Evoloop | Handcrafted, complex tables | Medium | Yes (toward simplicity) |
| Lenia | Parameterized, continuous | High (400+ species) | Emerging (Flow-Lenia) |
| Particle Life | Parameterized force laws | High (cells, ecosystems) | No |
| Primordial Particles | Single motion law | Very high (life cycles) | No |
| Neural CA | Learned via gradient descent | Medium (self-repair) | No |

### Key Recurring Insights

1. **Continuity unlocks naturalism**. Discrete systems (Life, Langton) produce geometric, brittle structures. Continuous systems (Lenia, Particle Life, PPS) produce organic, resilient, natural-looking creatures.

2. **Self-replication is necessary but not sufficient for evolution**. Langton's loops replicate but don't evolve. Evolution requires variation + differential fitness + heredity (Evoloop).

3. **Open-ended evolution remains unsolved**. Even Evoloop only evolves toward simplicity. No system has demonstrated sustained complexification from simple rules. This is considered a grand challenge of ALife.

4. **The edge of chaos**. In nearly every system, interesting behavior occurs in a narrow parameter regime between order and chaos. Lenia's "complex river," PPS's "Region of Life," and Life's rule B3/S23 all sit at this boundary.

5. **Discovery is shifting from human to automated**. ASAL (2024) and quality-diversity algorithms are replacing hand-guided search for finding novel creatures and rules.

6. **Simple rules, complex outcomes -- but the complexity has limits**. None of these systems have produced anything approaching the complexity of even the simplest biological cell. The gap between artificial and biological self-organization remains enormous.

---

## Sources

- [Conway's Game of Life - Wikipedia](https://en.wikipedia.org/wiki/Conway's_Game_of_Life)
- [First Self-Replicating Creature in Life - Slashdot (2010)](https://games.slashdot.org/story/10/06/17/162242/first-self-replicating-creature-spawned-in-conways-game-of-life)
- [Replicator - LifeWiki](https://conwaylife.com/wiki/Replicator)
- [Langton's Loops - Wikipedia](https://en.wikipedia.org/wiki/Langton's_loops)
- [Sayama's SDSR Loop and Evoloop](http://bingdev.binghamton.edu/sayama/sdsr/)
- [Self-Reproduction and Evolution in CA: 25 Years After Evoloops (2025)](https://direct.mit.edu/artl/article/31/1/81/124368/Self-Reproduction-and-Evolution-in-Cellular)
- [Lenia - Wikipedia](https://en.wikipedia.org/wiki/Lenia)
- [Lenia Project Portal](https://chakazul.github.io/lenia.html)
- [Lenia: Biology of Artificial Life (arXiv)](https://arxiv.org/abs/1812.05433)
- [Flow-Lenia (MIT Press, 2025)](https://direct.mit.edu/artl/article/31/2/228/130572/Flow-Lenia-Emergent-Evolutionary-Dynamics-in-Mass)
- [Clusters - Jeffrey Ventrella](https://www.ventrella.com/Clusters/)
- [Particle Life App - Tom Mohr (GitHub)](https://github.com/tom-mohr/particle-life-app)
- [Primordial Particle Systems - Scientific Reports (2016)](https://www.nature.com/articles/srep37969)
- [Growing Neural Cellular Automata - Distill (2020)](https://distill.pub/2020/growing-ca/)
- [Differentiable Logic Gate NCA (2025)](https://arxiv.org/html/2506.22899v1)
- [CAX: Cellular Automata in JAX (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/file/19206a6ed5ed0aaeed440448dfc5cf7e-Paper-Conference.pdf)
- [ASAL: Automating ALife Discovery - Sakana AI (2024)](https://sakana.ai/asal/)
- [Open-Ended Evolution - ALife Encyclopedia](https://alife.org/encyclopedia/introduction/open-ended-evolution/)
- [Softology: Clusters and Particle Life](https://softologyblog.wordpress.com/2018/11/08/clusters-and-particle-life/)
