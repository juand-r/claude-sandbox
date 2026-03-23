# Emergence of Agency from Simple Rules: Theoretical Foundations

A survey of frameworks attempting to explain how agents, individuality, and cognition emerge from non-agentive substrates. Covers key theories and recent work (2020--2026).

---

## 1. Free Energy Principle / Active Inference (Karl Friston)

The Free Energy Principle (FEP) posits that any system that persists over time can be described as minimizing variational free energy -- a bound on surprisal (negative log-evidence). A system's boundary is formalized as a **Markov blanket**: a statistical partition into internal states, external states, and the sensory/active states that mediate between them. Agents "emerge" in this framework when a Markov blanket forms such that internal states come to parameterize Bayesian beliefs about external states, and active states change the world to confirm those beliefs. Hierarchical self-organization of nested Markov blankets -- blankets of blankets -- provides a mechanism for multi-scale agency, from single cells to organisms (Palacios et al., 2020). The 2022 MIT Press textbook *Active Inference* (Parr, Pezzulo, Friston) is the first comprehensive treatment. The 2023 paper "The Free Energy Principle Made Simpler but Not Too Simple" (Friston, Da Costa et al.) provides the clearest derivation from Langevin dynamics to Bayesian mechanics. Computational implementations now exist in deep learning (Mazzaglia et al., 2022) and as autonomous agent architectures. Critics (Bruineberg et al., 2022, "The Emperor's New Markov Blankets") argue that the statistical concept of Markov blanket has been stretched beyond its original meaning into something more like a sensorimotor boundary -- a distinct construct they call "Friston blankets."

**Key references:**
- Friston (2019). [A Free Energy Principle for a Particular Physics](https://activeinference.github.io/papers/physics_paper.pdf)
- Friston, Da Costa et al. (2023). [The Free Energy Principle Made Simpler but Not Too Simple](https://www.sciencedirect.com/science/article/pii/S037015732300203X). *Physics of Life Reviews*.
- Parr, Pezzulo, Friston (2022). *Active Inference*. MIT Press.
- Palacios et al. (2020). [On Markov Blankets and Hierarchical Self-Organisation](https://pmc.ncbi.nlm.nih.gov/articles/PMC7284313/). *J. Math. Psych.*
- Bruineberg et al. (2022). [The Emperor's New Markov Blankets](https://philsci-archive.pitt.edu/18467/1/The%20Emperor's%20New%20Markov%20Blankets.pdf). *Behavioral and Brain Sciences*.
- Mazzaglia et al. (2022). [The Free Energy Principle for Perception and Action: A Deep Learning Perspective](https://pmc.ncbi.nlm.nih.gov/articles/PMC8871280/).

---

## 2. Constructor Theory (Deutsch, Marletto)

Constructor theory reformulates physics in terms of which **transformations (tasks) are possible or impossible**, rather than predicting trajectories. A "constructor" is any entity that can cause a transformation repeatedly while retaining the ability to do so again. The central move is from dynamical laws to counterfactual statements about what can and cannot be brought about. Marletto's **Constructor Theory of Life** (2015) shows that accurate self-reproduction via the von Neumann replicator-vehicle logic is the *only* possible logic for self-reproduction under "no-design laws" -- laws that do not encode the design of biological adaptations. The sole non-trivial requirement is that the laws permit digital information to be physically instantiated. This connects agency to information: the emergence of knowledge-bearing "recipes" (digital codes that specify constructions) is what makes open-ended evolution possible. Constructor theory is "close in spirit" to assembly theory (Marletto's phrase), but operates at a more foundational level -- it constrains what *any* physics must look like to permit life, rather than measuring complexity empirically. Recent work (2024--2025) has connected constructor theory to autopoiesis, framing life as a "self-constructor."

**Key references:**
- Deutsch (2013). [Constructor Theory](https://arxiv.org/pdf/1210.7439). *Synthese*.
- Marletto (2015). [Constructor Theory of Life](https://royalsocietypublishing.org/doi/10.1098/rsif.2014.1226). *J. R. Soc. Interface*.
- Marletto (2024). [How Constructor Theory Solves the Riddle of Life](https://aeon.co/essays/how-constructor-theory-solves-the-riddle-of-life). *Aeon*.
- [Constructor Theory research portal](https://www.constructortheory.org/)

---

## 3. Assembly Theory (Lee Cronin)

Assembly theory quantifies the complexity of an object by its **assembly index** -- the minimum number of joining steps needed to build it from basic parts -- combined with its **copy number** (observed abundance). The key claim: objects with high assembly index *and* high copy number cannot arise without selection. Empirically, the Cronin group found that molecules with assembly index above ~15 are not produced by known abiotic processes, proposing this as a biosignature threshold (with implications for detecting life on other planets via mass spectrometry). The 2023 *Nature* paper "Assembly Theory Explains and Quantifies Selection and Evolution" presents the full framework, redefining objects not as point particles but as entities defined by their formation histories. A 2025 paper in *npj Complexity* formally distinguishes the assembly index from Shannon entropy, Huffman encoding, and LZW compression, placing it in a different computational complexity class. The theory has attracted significant criticism: Abrahao et al. (2024) argue it offers nothing beyond algorithmic complexity; Hazen et al. (2024) showed abiotic crystal structures can exceed the MA=15 threshold; and Jaeger (2024) concluded it has merit but is not as revolutionary as claimed. Despite controversy, assembly theory provides a concrete, experimentally testable bridge between physics and biology -- rare among theories of emergence.

**Key references:**
- Cronin, Sharma et al. (2023). [Assembly Theory Explains and Quantifies Selection and Evolution](https://www.nature.com/articles/s41586-023-06600-9). *Nature* 622, 321--328.
- Kempes, Lachmann, Walker, Cronin et al. (2025). [Assembly Theory and Its Relationship with Computational Complexity](https://www.nature.com/articles/s44260-025-00049-9). *npj Complexity*.
- Cronin et al. (2024). [Experimentally Measured Assembly Indices Are Required to Determine the Threshold for Life](https://royalsocietypublishing.org/doi/10.1098/rsif.2024.0367). *J. R. Soc. Interface*.
- [Santa Fe Institute summary](https://www.santafe.edu/news-center/news/new-assembly-theory-unifies-physics-and-biology-explain-evolution-and-complexity)

---

## 4. Autopoiesis (Maturana, Varela)

An autopoietic system is a network of processes that **produces the components which constitute the network itself**, maintaining its own boundary and organization. Maturana and Varela (1973) introduced the concept to define the minimal organization of living systems: a system is autopoietic if it continuously regenerates itself through its own operations, forming a topological boundary (like a cell membrane) that distinguishes self from non-self. Cognition, in this view, *is* the process of maintaining autopoietic organization -- sense-making is inherent to life itself. Recent computational work has renewed interest: Heylighen & Busseniers (2023) formalized autopoiesis using reaction networks, showing how knowledge can be a purely internal construction yet still effectively regulate the system's environment. Kliska & Nehaniv (2024) built a novel 3D molecular dynamics model of minimal autopoiesis, questioning whether a spatial boundary is strictly necessary. In AI, the concept has been applied to LLMs -- a 2025 *Frontiers in Communication* paper argues that without structural coupling to a living body, LLMs lack the perturbations that shape genuine sense-making. A 2025 paper proposes "Computational Autopoiesis" as an architecture for autonomous AI, combining introspective self-correction with the Free Energy Principle. The concept remains central: autopoiesis is arguably the most precise existing definition of what separates living from non-living systems, and any theory of emergent agency must account for it.

**Key references:**
- Maturana & Varela (1980). *Autopoiesis and Cognition: The Realization of the Living*. Springer.
- Heylighen & Busseniers (2023). [Modeling Autopoiesis and Cognition with Reaction Networks](https://www.researchgate.net/publication/371338178_Modeling_autopoiesis_and_cognition_with_reaction_networks). *Biosystems*.
- Kliska & Nehaniv (2024). [Autocatalysis, Autopoiesis, and the Opportunity Cost of Individuality](https://www.mdpi.com/2313-7673/9/6/328). *Biomimetics*.
- Stano, Nehaniv, Ikegami, Damiano & Witkowski (2023). Autopoiesis: Foundations of Life, Cognition, and Emergence of Self/Other. *Biosystems* (special issue editorial).
- Gershenson (2023). [Emergence in Artificial Life](https://direct.mit.edu/artl/article/29/2/153/114834/Emergence-in-Artificial-Life). *Artificial Life*.

---

## 5. Individuality and Agency in Physics (Krakauer, Flack, Fields, Levin)

Krakauer, Bertschinger, Olbrich, Flack & Ay (2020) proposed an **information-theoretic definition of individuality**: an individual is an aggregate that propagates information from its past into its future more than it receives from its environment. This yields three formal types -- organismal (high internal propagation), colonial (shared propagation), and driven (environmentally dependent) -- each quantifiable via mutual information. Individuality exists on a continuum and can be nested. Separately, Michael Levin's group has developed the concept of **basal cognition**: the idea that goal-directed, problem-solving competency exists at every scale of biological organization, from molecular networks to tissues to organisms. The key construct is the "cognitive light cone" -- the scale of the goals a collective can pursue. Cancer, in this framing, is a collapse of the cognitive light cone back to unicellular goals. Fields & Levin (2022, 2025) connect this to physics, applying the Free Energy Principle to generic quantum systems and arguing for a complementarity between "objects" (persistent patterns) and "processes" (transformations). McMillen & Levin (2024) propose collective intelligence as a unifying concept across biological scales and substrates, while Watson & Levin (2023) argue that what makes a collective into an individual is its intelligence -- its competency in solving novel problems. This body of work redefines agency as a graded, scale-free, substrate-independent property detectable through information-theoretic measures.

**Key references:**
- Krakauer, Bertschinger, Olbrich, Flack & Ay (2020). [The Information Theory of Individuality](https://link.springer.com/article/10.1007/s12064-020-00313-7). *Theory in Biosciences*.
- Fields & Levin (2025). [Thoughts and Thinkers: On the Complementarity between Objects and Processes](https://drmichaellevin.org/publications/). *Physics of Life Reviews*.
- McMillen & Levin (2024). [Collective Intelligence: A Unifying Concept for Integrating Biology across Scales and Substrates](https://www.nature.com/articles/s42003-024-06037-4). *Communications Biology*.
- Levin (2025). [The Multiscale Wisdom of the Body](https://onlinelibrary.wiley.com/doi/10.1002/bies.202400196). *BioEssays*.
- Watson & Levin (2023). [The Collective Intelligence of Evolution and Development](https://journals.sagepub.com/doi/10.1177/26339137231168355). *Collective Intelligence*.
- Seifert, Sealander, Marzen & Levin (2024). From Reinforcement Learning to Agency: Frameworks for Understanding Basal Cognition. *BioSystems*.

---

## 6. Hermeneutics and Artificial Life

The connection between hermeneutics (the theory of interpretation) and the emergence of cognition runs through **enactivism**. Before Varela coined "enactive," he called his approach "the hermeneutic approach" (Thompson, 2005) -- emphasizing that cognition is sense-making, not information processing. The hermeneutic circle (understanding the whole requires understanding the parts, and vice versa) maps onto the organism-environment coupling: an organism interprets its world through its embodied history, and that interpretation shapes what it encounters. Gallagher & Allen (2018) distinguish "neural hermeneutics" (the brain as a prediction engine interpreting sensory signals, aligned with the FEP) from "enactivist hermeneutics" (meaning arises from the whole brain-body-environment system, not just neural prediction). Recent AI work has engaged this directly: Demichelis (2024, "The Hermeneutic Turn of AI") asks whether LLMs, which process natural language instructions, genuinely interpret or merely simulate interpretation. Wang (2021) argues from Gadamer that understanding requires openness to context and genuine dialogue -- something no amount of computational power yields. A 2023 paper on emergence in artificial life (Gershenson) notes that without emergence, ALife falls into dualism -- and emergence in living systems is inseparable from the generation of meaning. The implication for agency: a system that merely reacts is not an agent; an agent is a system that *interprets* -- that generates meaning from its interactions with the world. Whether artificial systems can cross this threshold remains the central open question.

**Key references:**
- Gallagher & Allen (2018). [Active Inference, Enactivism and the Hermeneutics of Social Cognition](https://link.springer.com/article/10.1007/s11229-016-1269-8). *Synthese*.
- Demichelis (2024). [The Hermeneutic Turn of AI: Are Machines Capable of Interpreting?](https://arxiv.org/pdf/2411.12517) arXiv.
- Wang (2021). [Is Artificial Intelligence Capable of Understanding?](https://journals.sagepub.com/doi/full/10.1177/20966083211056405) *Cultures of Science*.
- Gershenson (2023). [Emergence in Artificial Life](https://direct.mit.edu/artl/article/29/2/153/114834/Emergence-in-Artificial-Life). *Artificial Life*.
- Varela, Thompson & Rosch (1991). *The Embodied Mind*. MIT Press.

---

## Cross-Cutting Observations

These six frameworks converge on several points:

1. **Agency is graded, not binary.** Every framework treats agency as existing on a continuum -- from minimal (autopoietic cell) to maximal (reflective organism).

2. **Boundaries matter.** Markov blankets (FEP), membranes (autopoiesis), formation histories (assembly theory), and information channels (Krakauer/Flack) all formalize the distinction between self and non-self.

3. **Information is physical.** Constructor theory, assembly theory, and the information theory of individuality all treat information as a physical quantity with causal consequences -- not an abstraction layered on top of physics.

4. **Meaning requires embodiment.** The hermeneutic/enactivist tradition insists that genuine interpretation requires structural coupling to an environment -- a claim that remains the sharpest challenge to artificial agency.

5. **Testability varies enormously.** Assembly theory is directly measurable via mass spectrometry; the FEP is a mathematical principle that cannot be falsified; autopoiesis and hermeneutic sense-making remain difficult to operationalize experimentally. Any synthetic program aiming to build emergent agents must navigate this landscape of varying empirical tractability.
