# Chapter 16: Evolution, Discovery, and Open-Ended Systems

## 16.1 Introduction

The preceding chapters developed a framework for understanding LLMs as dynamical systems, with the (f, x) decomposition revealing how prompts encode both functions and data, and how iteration can mutate both. Chapter 15 introduced metrics for measuring novelty within outputs---the diversity, complexity, and originality of what these systems produce.

This chapter extends the framework in two directions that turn out to be deeply connected:

1. **AI-as-scientist**: Systems that autonomously generate hypotheses, design experiments, and make discoveries---treating the scientific method itself as a dynamical system.

2. **Evolutionary computation**: Algorithms that evolve populations of solutions, where LLMs now serve as intelligent mutation operators---treating evolution as a search through function space.

Both domains share a fundamental structure: an iterative process that generates novelty under selection pressure, with the goal of producing not just *good* solutions but *diverse* solutions that explore the space of possibilities. The (f, x) framework applies directly, and the novelty metrics of Chapter 15 become fitness functions.

The synthesis reveals a common challenge: **open-endedness**. How can we design systems that produce unbounded novelty without collapsing into repetitive patterns or diverging into incoherence? This is the "edge of chaos" problem writ large---the search for dynamics that sustain creative exploration indefinitely.

---

## 16.2 Scientific Discovery as a Dynamical System

### 16.2.1 The Scientific Method as Iteration

The scientific method is, at its core, an iterated process:

1. **Observe** phenomena
2. **Hypothesize** explanations
3. **Predict** consequences
4. **Test** predictions experimentally
5. **Revise** hypotheses based on results
6. **Repeat**

**Definition 16.1 (Scientific discovery system).** A **scientific discovery system** is a tuple $(H, E, f, g)$ where:
- $H$ is the space of hypotheses (theories, models, explanations).
- $E$ is the space of evidence (experimental results, observations).
- $f: H \times E \to H$ is the **revision function**: how hypotheses update given evidence.
- $g: H \to E$ is the **prediction function**: what evidence a hypothesis predicts.

The dynamics are:

$$h_{n+1} = f(h_n, e_n), \qquad e_n = g(h_n) + \xi_n,$$

where $\xi_n$ is experimental noise or the "surprise" of nature.

### 16.2.2 The (f, x) Decomposition of Science

Mapping to the framework of Chapter 14:

| Scientific Concept | (f, x) Component |
|---|---|
| Current hypothesis | State $x$ |
| Scientific method / reasoning | Function $f$ |
| Methodology evolution | Meta-rule $\varphi$ |
| Experimental results | External input $\xi$ |
| Paradigm shift | Change in $f$ itself |

**Observation 16.2.** Normal science (Kuhn, 1962) corresponds to fixed $f$: hypotheses evolve but the method stays constant. **Paradigm shifts** correspond to changes in $f$ itself---a new way of doing science.

In the (f, x) framework, a paradigm shift is:

$$(f_{\text{old}}, h) \to (f_{\text{new}}, h'),$$

where $f_{\text{new}}$ may be incommensurable with $f_{\text{old}}$ (different standards of evidence, different ontologies).

### 16.2.3 Attractors in Hypothesis Space

**Definition 16.3 (Scientific attractor).** A hypothesis $h^*$ is an **attractor** of the scientific discovery system if, for hypotheses $h$ in some neighborhood, repeated application of revision converges to $h^*$:

$$f(f(\cdots f(h, e_1), e_2), \ldots, e_n) \to h^*.$$

**Example 16.4.** The heliocentric model is an attractor: sufficiently careful observation and hypothesis revision, starting from various geocentric models, eventually converges to heliocentrism. The Ptolemaic system was a **metastable state**---stable under small perturbations but not a global attractor.

**Proposition 16.5.** Under the Bayesian interpretation, the attractor of rational belief revision is the hypothesis with maximum posterior probability. If the true model is in $H$ and evidence is unbiased, the attractor is the truth.

### 16.2.4 Novelty in Scientific Discovery

Where does novelty enter science?

1. **Hypothesis generation**: Proposing new $h \in H$ not previously considered.
2. **Experimental design**: Choosing which $e$ to seek (not just passively receiving).
3. **Conceptual innovation**: Expanding $H$ itself to include previously inconceivable hypotheses.
4. **Methodological innovation**: Changing $f$ to a more powerful revision procedure.

The metrics of Chapter 15 apply:

- **Distinct-n on hypotheses**: How many qualitatively different hypotheses has the system explored?
- **Relative novelty**: Is the current hypothesis far from all previously considered ones?
- **Cumulative novelty**: Is the trajectory through hypothesis space exploring new regions?

**Definition 16.6 (Scientific creativity).** A scientific discovery system exhibits **creativity** if:
1. It generates hypotheses with high relative novelty (unlike prior hypotheses).
2. Those hypotheses have high coherence (consistent with evidence).
3. The novelty is sustained (cumulative novelty doesn't decay to zero).

This is the (✓, ✓, ✓) corner of the novelty-coherence-reference triangle (Section 15.13.8) applied to hypothesis space.

---

## 16.3 Evolutionary Computation as a Dynamical System

### 16.3.1 Genetic Algorithms

A **genetic algorithm** (GA) evolves a population of candidate solutions:

1. **Initialize** population $P_0 = \{x_1, \ldots, x_N\}$.
2. **Evaluate** fitness $f(x_i)$ for each individual.
3. **Select** parents based on fitness.
4. **Recombine** (crossover) parents to produce offspring.
5. **Mutate** offspring with some probability.
6. **Replace** population: $P_{t+1} = \text{selection}(P_t \cup \text{offspring})$.
7. **Repeat** from step 2.

**Definition 16.7 (GA as DDS).** A genetic algorithm defines a discrete dynamical system on the space of populations:

$$\mathcal{P} = \{\text{finite subsets of } \mathcal{X}\},$$

with transition function:

$$F: \mathcal{P} \to \mathcal{P}, \qquad P_{t+1} = F(P_t).$$

This is a higher-order DDS: the "state" is itself a set of solutions.

### 16.3.2 Fitness Landscapes

**Definition 16.8 (Fitness landscape).** For search space $\mathcal{X}$ with fitness function $f: \mathcal{X} \to \mathbb{R}$ and neighborhood relation $N: \mathcal{X} \to 2^{\mathcal{X}}$, the **fitness landscape** is the graph $(X, E, f)$ where edge $(x, y) \in E$ iff $y \in N(x)$.

**Proposition 16.9 (Landscape structure determines dynamics).**
- **Smooth, unimodal landscape**: GA converges to global optimum. Single attractor.
- **Rugged, multimodal landscape**: GA may get stuck in local optima. Multiple attractors.
- **Deceptive landscape**: Gradient points away from global optimum. Attractor is not optimal.
- **Neutral landscape**: Large plateaus of equal fitness. Random drift dominates.

### 16.3.3 Premature Convergence as Collapse

**Definition 16.10 (Premature convergence).** A GA exhibits **premature convergence** when the population loses diversity and concentrates on a suboptimal solution before finding the global optimum.

This is the evolutionary analogue of **model collapse** (Chapter 14, Section 14.5): self-reinforcing dynamics reduce diversity. In GA terms:

$$\mathrm{Distinct\text{-}1}(P_t) \to 0 \text{ as } t \to \infty,$$

even though the population hasn't found the global optimum.

**Proposition 16.11.** Premature convergence corresponds to the GA being captured by a **spurious attractor**---a local optimum that is stable under the selection-mutation dynamics but not globally optimal.

### 16.3.4 Diversity Maintenance

To prevent premature convergence, GAs employ diversity maintenance:

1. **Fitness sharing**: Reduce fitness of individuals similar to others.
2. **Crowding**: Offspring replace similar parents.
3. **Island models**: Maintain separate subpopulations with occasional migration.
4. **Novelty pressure**: Explicitly reward individuals different from the population.

These correspond to **diversity-regularized objectives** (Section 15.12.4, Strategy 2):

$$\tilde{f}(x) = f(x) + \alpha \cdot \mathrm{Nov}_P(x),$$

where $\mathrm{Nov}_P(x)$ measures novelty of $x$ relative to population $P$.

---

## 16.4 Novelty Search and Quality-Diversity

### 16.4.1 Novelty Search

Lehman and Stanley (2011) proposed a radical idea: **abandon fitness entirely** and search purely for novelty.

**Definition 16.12 (Novelty search).** Let $\mathcal{A}_t$ be the **archive** of previously discovered behaviors. The novelty of individual $x$ is:

$$\mathrm{Nov}(x) = \frac{1}{k} \sum_{i=1}^{k} d(x, \text{$i$-th nearest neighbor in } \mathcal{A}_t),$$

the average distance to the $k$ nearest archived behaviors.

Selection is based on novelty, not fitness:

$$P_{t+1} = \text{select}(P_t, \mathrm{Nov}).$$

**Theorem 16.13 (Lehman & Stanley, 2011, informal).** On deceptive fitness landscapes, novelty search often outperforms fitness-based search. By ignoring the misleading fitness gradient, novelty search explores broadly and stumbles upon the global optimum.

### 16.4.2 The Paradox of Objectives

**Observation 16.14 (The objective paradox).** For complex problems, explicitly optimizing for the objective can prevent finding solutions, while searching for novelty---ignoring the objective---can succeed.

This connects to the exploration-exploitation trade-off. Pure exploitation (greedy fitness optimization) converges prematurely. Pure exploration (random search) is inefficient. Novelty search is a structured form of exploration that can outperform both.

### 16.4.3 Quality-Diversity Algorithms

**Quality-Diversity (QD)** algorithms seek the best of both worlds: collections of solutions that are both **high-quality** and **diverse**.

**Definition 16.15 (MAP-Elites).** **MAP-Elites** (Mouret & Clune, 2015) maintains a grid of cells, each representing a region of **behavior space**. For each cell, the algorithm stores the highest-fitness individual whose behavior falls in that region.

Algorithm:
1. **Initialize**: Randomly generate solutions; place each in the appropriate cell.
2. **Select**: Randomly choose an occupied cell.
3. **Mutate**: Produce offspring from the cell's elite.
4. **Evaluate**: Compute fitness and behavior descriptor of offspring.
5. **Update**: If offspring's cell is empty or offspring has higher fitness, replace.
6. **Repeat**.

**Proposition 16.16.** MAP-Elites simultaneously optimizes for:
- **Quality**: Each cell contains the best solution for that behavior.
- **Diversity**: Different cells represent different behaviors.

The output is a **repertoire**---a diverse collection of high-quality solutions.

### 16.4.4 Connection to Chapter 15 Metrics

Quality-Diversity algorithms operationalize the novelty-coherence-reference triangle:

| QD Concept | Chapter 15 Concept |
|---|---|
| Fitness | Quality $Q(w)$ |
| Behavior distance | Relative novelty $\mathrm{Nov}_{\mathcal{R}}(w)$ |
| Archive coverage | Absolute diversity $D(w)$ |
| MAP-Elites grid | Multi-scale novelty profile |

The QD objective can be written:

$$\max_{P} \sum_{c \in \text{cells}} Q(\text{elite}_c) \cdot \mathbb{1}[\text{cell } c \text{ occupied}],$$

which rewards both quality (high $Q$) and coverage (many cells occupied).

---

## 16.5 LLM-Augmented Evolution

### 16.5.1 Evolution Through Large Models (ELM)

Traditional GAs use random mutation. **Evolution through Large Models (ELM)** (Lehman et al., 2022) replaces random mutation with LLM-guided mutation.

**Definition 16.17 (LLM mutation operator).** Given a program $x$ (or any structured solution), the LLM mutation is:

$$\mathrm{mutate}_{\mathrm{LLM}}(x) = \mathrm{LLM}(\text{"Improve or vary this solution: "} \| x).$$

The LLM uses its training knowledge to propose *intelligent* modifications rather than random changes.

**Proposition 16.18.** LLM mutation has several advantages over random mutation:
1. **Syntax preservation**: The LLM generates syntactically valid programs.
2. **Semantic awareness**: Modifications are more likely to be meaningful.
3. **Knowledge transfer**: The LLM applies patterns from its training data.
4. **Adaptive step size**: The LLM can make small tweaks or large restructurings.

### 16.5.2 FunSearch: LLM + Evolution for Mathematical Discovery

**FunSearch** (Romera-Paredes et al., 2023) applies ELM to mathematical discovery. The key insight: search for **programs that generate solutions** rather than solutions directly.

**Algorithm 16.19 (FunSearch).**
1. **Skeleton**: User provides a program skeleton with a critical function to evolve.
2. **Initialize**: Start with a simple implementation.
3. **Prompt**: Sample high-performing programs from the archive; prompt the LLM to improve.
4. **Evaluate**: Run the generated program; score based on the solutions it produces.
5. **Update**: Add high-scoring programs to the archive.
6. **Iterate** with island-based parallelism.

**Theorem 16.20 (FunSearch results, Nature 2023).** FunSearch discovered:
- New constructions for the **cap set problem** (extremal combinatorics), improving the asymptotic lower bound for the first time in 20 years.
- New heuristics for **online bin packing** that outperform hand-designed baselines.

**Remark.** FunSearch searches in **function space**, not solution space. The programs it discovers are interpretable and generalizable---a scientist can read them and understand the strategy.

### 16.5.3 AlphaEvolve: General-Purpose Algorithm Discovery

**AlphaEvolve** (DeepMind, 2025) extends FunSearch to general-purpose algorithm discovery.

**Key features:**
- **Ensemble of LLMs**: Uses both Gemini 2.0 Flash (high throughput) and Gemini 2.0 Pro (high quality).
- **Multi-objective optimization**: Can optimize for multiple metrics (accuracy, efficiency, etc.).
- **Whole-codebase evolution**: Can modify entire programs, not just single functions.

**Theorem 16.21 (AlphaEvolve results, 2025).** AlphaEvolve achieved:
- First improvement in 56 years to Strassen's algorithm for 4×4 complex matrix multiplication.
- 0.7% recovery of Google's worldwide computing resources via improved scheduling.
- 23--32% speedups in TPU kernel operations.
- Improvements on 20% of 50+ open mathematical problems.

### 16.5.4 The (f, x) View of LLM-Evolution

In the (f, x) framework:

| Evolution Concept | (f, x) Component |
|---|---|
| Current population | State $x = P$ |
| Selection + LLM mutation | Function $f = \mathrm{select} \circ \mathrm{mutate}_{\mathrm{LLM}}$ |
| Prompt engineering | Specification of $f$ |
| Archive/elites | Memory component of $x$ |
| Fitness function | Quality metric $Q$ |
| Behavior descriptor | Novelty metric $D$ |

**Proposition 16.22.** LLM-augmented evolution is a (f, x) system where the mutation operator $f$ is itself a large neural network with rich prior knowledge. The "instruction" component of $f$ (the prompt) can be evolved alongside the population, enabling **meta-learning** of the evolutionary process.

---

## 16.6 Autonomous AI Scientists

### 16.6.1 The AI Scientist

**The AI Scientist** (Lu et al., 2024) automates the full scientific workflow:

1. **Idea generation**: LLM proposes research questions and hypotheses.
2. **Literature review**: Automated search and synthesis of related work.
3. **Experiment design**: LLM writes code to test hypotheses.
4. **Execution**: Automated running of experiments.
5. **Analysis**: LLM interprets results and generates visualizations.
6. **Writing**: LLM produces a complete scientific manuscript.
7. **Review**: Automated peer review evaluates the paper.

**Definition 16.23 (AI Scientist as (f, x) system).** The AI Scientist is a (f, x) system where:
- $x$ = (current manuscript, experimental results, literature context).
- $f$ = the LLM-driven research pipeline (idea → experiment → write → review).
- The output $f(x)$ is a revised manuscript incorporating new experiments.

**Observation 16.24.** The AI Scientist exhibits both **novelty generation** (new ideas, experiments) and **quality control** (automated review). This implements the quality-diversity trade-off at the level of scientific papers.

### 16.6.2 AI Scientist v2 and Agentic Tree Search

**AI Scientist v2** (2025) replaces template-based generation with **agentic tree search**:

**Definition 16.25 (Experiment tree).** The **experiment tree** is a tree where:
- Each node is an experimental state (code, results, manuscript draft).
- Each edge is an action (modify code, run experiment, revise text).
- The tree expands via LLM-proposed actions.
- An **experiment manager agent** guides search.

This is **Monte Carlo Tree Search for science**---balancing exploration of new experimental directions with exploitation of promising results.

**Theorem 16.26 (AI Scientist v2 results, 2025).** AI Scientist v2 produced the first entirely AI-generated peer-review-accepted workshop paper, demonstrating that LLM-driven systems can produce novel, validated scientific contributions.

### 16.6.3 Open-Ended Scientific Discovery

**Definition 16.27 (Open-ended scientific discovery).** A scientific discovery system is **open-ended** if:
1. It generates novel hypotheses indefinitely (no convergence to a fixed set).
2. The novelty is adaptive (hypotheses explain more phenomena over time).
3. Complexity grows unboundedly (explanations become more sophisticated).

**Conjecture 16.28.** Current AI scientist systems are not truly open-ended. They can produce novel papers within the distribution of their training data, but cannot:
- Invent fundamentally new mathematical frameworks.
- Recognize when the entire paradigm needs revision.
- Generate experimental setups requiring physical intuition beyond their training.

True open-ended scientific discovery may require:
- Embodiment (physical experimentation, not just simulation).
- Social embedding (interaction with human scientists).
- Meta-level reflection (questioning the scientific method itself).

---

## 16.7 The Adjacent Possible and Open-Endedness

### 16.7.1 The Adjacent Possible

**Definition 16.29 (Adjacent possible, Kauffman 1996).** The **adjacent possible** is the set of states reachable in one step from the current state. As the system explores and expands, new states become adjacent that were not previously accessible.

**Example 16.30.** In technology evolution:
- Before the wheel, the cart is not in the adjacent possible.
- Once the wheel exists, the cart becomes adjacent.
- Once the cart exists, wheeled vehicles, gears, and pulleys become adjacent.

Each innovation expands the adjacent possible, enabling further innovation.

### 16.7.2 Formalizing Open-Endedness

**Definition 16.31 (Open-ended evolution).** An evolutionary system is **open-ended** if it:
1. **Never converges**: $\lim_{t \to \infty} \mathrm{CumNov}(P_t) \neq 0$.
2. **Increases complexity**: Some measure of complexity grows without bound.
3. **Generates major transitions**: Qualitatively new types of entities emerge.

**Observation 16.32.** Biological evolution on Earth appears open-ended: 3.5 billion years have produced increasing complexity (from prokaryotes to eukaryotes to multicellular life to intelligence) without convergence.

### 16.7.3 Obstacles to Open-Endedness

Why do computational systems fail to be open-ended?

**Obstacle 1: Finite state space.** If $|\mathcal{X}| < \infty$, the system must eventually repeat. Novelty is bounded.

**Obstacle 2: Fixed fitness landscape.** If the fitness function is static, the system converges to optima. No pressure for continued exploration.

**Obstacle 3: Representational limits.** If solutions have fixed complexity (e.g., fixed-length genomes), major transitions are impossible.

**Obstacle 4: Attractor collapse.** As in model collapse (Chapter 14), iterative systems tend toward low-diversity equilibria.

### 16.7.4 Conditions for Open-Endedness

Based on biological analogies and computational experiments:

**Condition 1: Expanding state space.** The set of possible solutions must grow with the system. In biology: new genes, new cell types, new body plans.

**Condition 2: Coevolution.** Entities evolve in response to each other, creating an ever-shifting fitness landscape. Red Queen dynamics: "running just to stay in place."

**Condition 3: Niche construction.** Agents modify their environment, creating new selection pressures. The adjacent possible expands as entities create new niches.

**Condition 4: Open-ended evaluation.** The fitness function itself evolves or is learned, preventing convergence to fixed optima.

**Conjecture 16.33 (Open-endedness requires (f, x) co-evolution).** A system is open-ended only if both the function $f$ (the rules of the game) and the state $x$ (the solutions) co-evolve. Fixed $f$ leads to convergence; only $\varphi \neq \text{id}$ (changing rules) can sustain open-ended novelty.

---

## 16.8 Synthesis: The DDS Framework for Discovery and Evolution

### 16.8.1 Unifying Table

| System | State $x$ | Function $f$ | Meta-rule $\varphi$ | Novelty Metric | Quality Metric |
|---|---|---|---|---|---|
| Scientific discovery | Hypothesis | Revision | Paradigm shift | Distance to prior hypotheses | Posterior probability |
| Genetic algorithm | Population | Selection + mutation | Hyperparameter adaptation | Population diversity | Fitness |
| Novelty search | Population + archive | Selection by novelty | Archive update rule | Distance to archive | (ignored) |
| MAP-Elites | Grid of elites | Mutation + cell update | Behavior space definition | Cell coverage | Per-cell fitness |
| FunSearch | Program archive | LLM mutation + scoring | Prompt evolution | Program novelty | Program score |
| AI Scientist | (paper, results, context) | Research pipeline | Methodology learning | Idea novelty | Review score |
| Open-ended evolution | (population, environment) | Selection + niche construction | Major transitions | Cumulative novelty | (undefined) |

### 16.8.2 The Quality-Diversity Lyapunov Exponent

Extending Section 15.12.3:

**Definition 16.34 (QD Lyapunov exponent).** For a quality-diversity system with quality $Q_t$ and diversity $D_t$ at generation $t$, define:

$$\lambda_{QD} = \lim_{t \to \infty} \frac{1}{t} \log \frac{Q_t \cdot D_t}{Q_0 \cdot D_0}.$$

- $\lambda_{QD} < 0$: System collapses (quality or diversity decreasing).
- $\lambda_{QD} = 0$: Equilibrium (quality-diversity maintained).
- $\lambda_{QD} > 0$: Expansion (both improving)---the open-ended regime.

### 16.8.3 The Role of LLMs

LLMs transform the landscape of evolutionary and discovery systems by:

1. **Informed search**: LLMs encode vast prior knowledge, enabling intelligent exploration rather than blind mutation.

2. **Linguistic interface**: Problems can be specified in natural language; solutions can be programs or text.

3. **Transfer learning**: Strategies that work in one domain (from training data) transfer to new problems.

4. **Scalable creativity**: LLMs can generate many diverse candidates cheaply.

**Proposition 16.35.** LLMs shift the exploration-exploitation balance toward informed exploration. The "adjacent possible" is larger because the LLM can propose solutions that are not merely one mutation away but are semantically related.

However, LLMs also introduce risks:

1. **Mode collapse**: LLMs have their own biases; LLM-driven evolution may converge to LLM-preferred solutions.

2. **Training distribution limits**: LLMs cannot easily generate solutions outside their training distribution.

3. **Hallucination**: LLMs may propose plausible-sounding but invalid solutions.

The combination of LLMs with explicit evaluation (fitness functions, proof checkers, experiments) addresses these risks by grounding creativity in verification.

---

## 16.9 Open Questions

**Question 16.36 (Open-ended AI).** Can we build systems that exhibit biological-like open-ended evolution? What are the minimal conditions? Current systems (MAP-Elites, FunSearch, AI Scientist) seem to plateau rather than generate unbounded novelty.

**Question 16.37 (Paradigm shifts).** Can AI systems generate genuine paradigm shifts---not just new solutions within existing frameworks but entirely new frameworks? This seems to require meta-level reasoning about the problem formulation itself.

**Question 16.38 (Coevolution with humans).** What is the role of human scientists in AI-augmented discovery? The most successful systems (FunSearch, AlphaEvolve) involve human problem specification and result interpretation. Is human-AI coevolution the path to open-endedness?

**Question 16.39 (Evaluation bottleneck).** Autonomous scientific discovery is limited by the ability to evaluate hypotheses. Physical experiments are slow and expensive. Can we develop better "world models" that enable rapid hypothesis testing?

**Question 16.40 (Diversity collapse in LLM-evolution).** Do LLM-driven evolutionary systems suffer from diversity collapse analogous to model collapse? If LLM outputs are fed back as inputs (prompts containing LLM-generated code), does diversity decay?

**Question 16.41 (Measuring scientific novelty).** How should we measure the novelty of scientific discoveries? Citation-based metrics capture impact but not originality. Information-theoretic measures (Section 15.13) could be applied to scientific papers, but the right formalization is unclear.

**Question 16.42 (The creativity spectrum).** Is there a hierarchy of creative capabilities?
1. Generating variations within a known space.
2. Discovering new solutions to known problems.
3. Discovering new problems worth solving.
4. Inventing new frameworks that redefine what counts as a solution.

Where do current AI systems fall? Can LLMs reach level 4?

---

## 16.10 Summary

| Concept | Dynamical Systems View | Key Insight |
|---|---|---|
| Scientific method | Iteration on hypothesis space | Paradigm shifts = changes in $f$ |
| Genetic algorithms | DDS on population space | Premature convergence = spurious attractor |
| Novelty search | Selection by archive distance | Ignoring objectives can help |
| Quality-Diversity | Multi-objective: fitness + coverage | MAP-Elites as grid of local optima |
| LLM mutation | Intelligent, knowledge-based variation | Prior knowledge expands adjacent possible |
| FunSearch | Program space evolution with LLM | Search for programs, not solutions |
| AlphaEvolve | General-purpose algorithm discovery | LLM ensemble + multi-objective |
| AI Scientist | Full research pipeline automation | Science as (f, x) iteration |
| Open-endedness | Unbounded novelty generation | Requires (f, x) co-evolution |

The synthesis reveals that **discovery and evolution are two faces of the same coin**: both involve iterative search through vast spaces, balancing exploration (novelty) with exploitation (quality), and seeking dynamics that sustain creativity without collapse.

LLMs have transformed both domains by providing intelligent mutation operators and automated evaluation. But the deepest challenge---achieving true open-endedness---remains unsolved. Biological evolution achieved it; can we engineer it?

The framework developed in this textbook---discrete dynamical systems, symbolic dynamics, computational mechanics, the (f, x) decomposition, novelty metrics---provides the conceptual tools to analyze these systems. Whether those tools suffice to *design* open-ended systems is the frontier.

---

## References

- Clune, J. (2019). AI-GAs: AI-generating algorithms, an alternate paradigm for producing general artificial intelligence. *arXiv preprint* arXiv:1905.10985.

- DeepMind (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery. *arXiv preprint* arXiv:2506.13131.

- Kauffman, S. A. (1996). *At Home in the Universe: The Search for the Laws of Self-Organization and Complexity*. Oxford University Press.

- Kuhn, T. S. (1962). *The Structure of Scientific Revolutions*. University of Chicago Press.

- Lehman, J. and Stanley, K. O. (2011). Abandoning objectives: Evolution through the search for novelty alone. *Evolutionary Computation*, 19(2):189--223.

- Lehman, J., Gordon, J., Jain, S., Ndousse, K., Yeh, C., and Stanley, K. O. (2022). Evolution through large models. *arXiv preprint* arXiv:2206.08896.

- Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., and Ha, D. (2024). The AI Scientist: Towards fully automated open-ended scientific discovery. *arXiv preprint* arXiv:2408.06292.

- Mouret, J.-B. and Clune, J. (2015). Illuminating search spaces by mapping elites. *arXiv preprint* arXiv:1504.04909.

- Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M. P., Dupont, E., Ruiz, F. J. R., Ellenberg, J. S., Wang, P., Fawzi, O., Kohli, P., and Fawzi, A. (2023). Mathematical discoveries from program search with large language models. *Nature*, 625:468--475.

- Sakana AI (2025). The AI Scientist-v2: Workshop-level automated scientific discovery via agentic tree search.

- Soros, L. B. and Stanley, K. O. (2014). Identifying necessary conditions for open-ended evolution through the artificial life world of Chromaria. *Proceedings of the Artificial Life Conference*.

- Stanley, K. O., Lehman, J., and Soros, L. (2017). Open-endedness: The last grand challenge you've never heard of. *O'Reilly Radar*.

---

## Exercises

**Exercise 16.1.** Model the discovery of Newtonian mechanics as a (f, x) dynamical system. What was the state space $H$? What evidence $E$ drove the revision? When did $f$ change (paradigm shift)?

**Exercise 16.2.** Implement a simple genetic algorithm for symbolic regression (finding a formula that fits data). Track Distinct-1 on the population over generations. Does premature convergence occur? At what generation?

**Exercise 16.3.** Implement novelty search for a simple maze navigation task. Compare with fitness-based search. In which environments does novelty search outperform?

**Exercise 16.4.** Design a prompt for an LLM that acts as a mutation operator for Python functions. Test it: does it produce syntactically valid variations? Are the variations meaningfully different?

**Exercise 16.5.** Propose a metric for "paradigm-shift novelty" in scientific papers. How would you distinguish papers that work within an existing paradigm from papers that establish a new one?

**Exercise 16.6.** (Research) Read the FunSearch paper. What is the role of the "islands" in the evolutionary algorithm? How does this relate to the diversity maintenance techniques of Section 16.3.4?

**Exercise 16.7.** (Research) Can you design an (f, x) system where both $f$ and $x$ co-evolve? Sketch an algorithm where the mutation operator itself is subject to selection.
