# Discrete Dynamical Systems with Evolving Rules: A Framework for Understanding LLM Self-Interaction

## Abstract

We introduce a formal framework for studying self-interacting language models through the lens of discrete dynamical systems. An LLM prompt simultaneously encodes a function $f$ and an input $x$; feeding output back as input creates iteration on the space of (function, state) pairs. We formalize this as the transition $(f, x) \mapsto (\varphi(f, x), f(x))$, where $\varphi$ is a *meta-rule* that governs how the function itself evolves. This framework unifies disparate phenomena---model collapse, self-improvement, attractor convergence, and multi-agent emergence---under a single dynamical systems umbrella. We survey the mathematical foundations from symbolic dynamics, Kolmogorov complexity, and computational mechanics, and identify the key questions: When do self-interacting systems converge to fixed points or cycles? When do they collapse to degenerate attractors? What distinguishes "creative" transients from trivial or random dynamics? Our framework provides both conceptual clarity and a foundation for rigorous analysis of increasingly autonomous AI systems.

---

## 1. Introduction

Large language models have become capable of extended autonomous operation: generating text, critiquing their own outputs, refining solutions, and interacting with other agents. This raises a fundamental question: **what happens when an LLM's output becomes its own input?**

Empirically, the answer depends on the task. Successive paraphrasing converges to 2-cycles [Wang et al., 2025]. Self-training on generated data leads to *model collapse*---progressive loss of distributional diversity [Shumailov et al., 2024]. Self-refinement improves quality up to a saturation point [Madaan et al., 2023]. Self-rewarding training produces models that improve across multiple generations [Yuan et al., 2024]. Multi-agent systems exhibit emergent social behaviors [Park et al., 2023].

These observations are currently understood in isolation. Model collapse is analyzed via information theory [Alemohammad et al., 2023]. Self-improvement is studied empirically without formal convergence guarantees [Huang et al., 2023]. Attractor formation is noted but not systematically characterized [Perez et al., 2024].

We propose that all of these phenomena are manifestations of a single underlying structure: **discrete dynamical systems with evolving rules**. The key observation is:

> *A prompt encodes both a function $f$ (what the LLM should do) and an input $x$ (what it should do it to). The LLM's output is approximately $f(x)$. When outputs are fed back as inputs, we obtain iteration---but crucially, the function component may also change.*

This leads to the transition rule:

$$(f, x) \longmapsto (\varphi(f, x), \; f(x))$$

where $\varphi: F \times X \to F$ is the **meta-rule** that governs how the function evolves. When $\varphi(f, x) = f$ for all $x$, we recover ordinary iteration of a fixed map. When $\varphi$ is nontrivial, the system *rewrites its own rules*.

### 1.1 Why This Framework?

The (f, x) framework provides three key advantages:

**1. Unification.** Model collapse, self-improvement, attractor convergence, and multi-agent emergence all correspond to different choices of the meta-rule $\varphi$:
- Model collapse: $\varphi$ is *destructive*---each generation degrades the function.
- Self-improvement: $\varphi$ is *constructive*---each generation improves the function.
- Attractor convergence: $\varphi = \text{id}$, and the state $x$ converges to fixed points or cycles.
- Multi-agent systems: the state space is a product, and $\varphi$ couples multiple interacting maps.

**2. Mathematical tools.** The framework connects LLM dynamics to well-developed mathematical theories:
- *Symbolic dynamics* (Chapters 2--3): LLMs with finite context windows are sliding block codes.
- *Kolmogorov complexity* (Chapter 8): Orbit complexity measures the information content of trajectories.
- *Logical depth* (Chapter 9): "Creative" orbits are those with short descriptions but long computation times.
- *Computational mechanics* (Chapter 10): Epsilon-machines characterize the minimal predictive structure of orbits.
- *Kleene's recursion theorem* (Chapter 11): Fixed points of self-modifying programs are mathematically inevitable.

**3. Computational universality.** Transformers with chain-of-thought are Turing-complete [Merrill & Sabharwal, 2024], and prompting alone suffices for universality [Qiu et al., 2024]. This means the (f, x) framework can realize *any* computable dynamical system---including all the complex behaviors observed empirically.

### 1.2 Key Questions

The framework raises several fundamental questions, which this work begins to address:

1. **Fixed points and cycles.** Under what conditions does the iterated system $(f, x) \mapsto (\varphi(f,x), f(x))$ converge to fixed points or periodic orbits? The empirical observation of 2-cycles in paraphrasing [Wang et al., 2025] suggests robust attractor structure.

2. **Model collapse vs. improvement.** What distinguishes a destructive meta-rule (leading to collapse) from a constructive one (leading to improvement)? The difference is not merely empirical---it should have a formal characterization.

3. **Creativity and depth.** Can we formalize "creativity" as a property of orbits? Bennett's logical depth (Chapter 9) suggests an answer: creative orbits are *deep*---they have compact descriptions but require substantial computation to unfold. This is precisely the regime "between order and chaos" that Crutchfield identifies as maximally complex [Crutchfield, 2012].

4. **External input and escape.** Fresh data prevents model collapse [Alemohammad et al., 2023]. In dynamical systems terms, external input perturbs the system away from degenerate attractors. What is the minimum rate of external input needed to maintain distributional diversity?

5. **Multi-agent phase transitions.** As the number of agents and their interaction topology change, do collective dynamics exhibit phase transitions? Generative Agents [Park et al., 2023] suggests emergent social structures arise above some complexity threshold.

---

## 2. Problem Formulation

### 2.1 The Basic Framework

Let $X$ be a finite set of **states** and $F = X^X$ the set of all functions $f: X \to X$. A **discrete dynamical system with evolving rules** is a triple $(X, F, \varphi)$ where $\varphi: F \times X \to F$ is the meta-rule.

The dynamics proceed as:
$$
(f_0, x_0) \to (f_1, x_1) \to (f_2, x_2) \to \cdots
$$
where $f_{n+1} = \varphi(f_n, x_n)$ and $x_{n+1} = f_n(x_n)$.

**Proposition 2.1.** The state space $F \times X$ is finite with $|F \times X| = |X|^{|X|} \cdot |X|$. Every orbit is eventually periodic.

This is immediate from finiteness. The transient length $\tau$ and cycle length $\lambda$ are the standard invariants.

### 2.2 Special Cases

**Case 1: Fixed function ($\varphi(f, x) = f$).** The dynamics reduce to ordinary iteration: $x_{n+1} = f(x_n)$. This is the setting of Chapter 1.

**Case 2: State-independent meta-rule ($\varphi(f, x) = \psi(f)$).** The function component evolves independently of the state. The dynamics factor into iteration of $\psi$ on $F$ and a time-varying iteration on $X$.

**Case 3: Full coupling ($\varphi$ depends on both $f$ and $x$).** The most general case. The function and state co-evolve, and neither can be analyzed in isolation.

### 2.3 The LLM Instantiation

For a language model with vocabulary $\Sigma$ and context window $k$:
- $X = \Sigma^*$ (finite strings, bounded by maximum generation length)
- $F$ is the space of "functions" encodable by prompts
- The meta-rule $\varphi$ extracts the function component from the LLM's output

The key empirical observation [Qiu et al., 2024] is that prompts can encode arbitrary computable functions. Thus $F$, while nominally finite (bounded by prompt length), is computationally universal.

**Theorem 2.2** (Computational universality). For any computable function $g: X \to X$, there exists a prompt $p$ such that the LLM instantiation with $f = g$ computes $g(x)$ for all $x$ (with chain-of-thought).

This means the (f, x) framework inherits the full complexity of general computation. Questions about convergence, fixed points, and orbit structure are, in general, undecidable.

### 2.4 Complexity Measures for Orbits

Given an orbit $(f_0, x_0), (f_1, x_1), \ldots$, we define several complexity measures:

**Transient length $\tau$:** Steps before entering a cycle. High $\tau$ indicates the system "explores" before settling.

**Cycle length $\lambda$:** Length of the eventual periodic orbit. $\lambda = 1$ is a fixed point; $\lambda = 2$ is a 2-cycle.

**Function mutation rate:** Fraction of steps where $f_{n+1} \neq f_n$. High mutation indicates active self-modification.

**Lempel-Ziv complexity:** Compressibility of the orbit sequence. Normalized LZ complexity estimates the entropy rate.

**Statistical complexity $C_\mu$:** From the epsilon-machine of the orbit (Chapter 10). Measures memory required for optimal prediction.

**Logical depth proxy:** Transient length serves as a finite-system proxy for Bennett's logical depth. Deep orbits have short rule descriptions but long transients.

### 2.5 The "Creativity" Criterion

We propose that *creative* orbits are characterized by:

1. **Moderate entropy rate:** Neither zero (trivially periodic) nor maximal (indistinguishable from random).
2. **High statistical complexity:** Rich predictive structure.
3. **Long transients:** Extended exploration before convergence.
4. **Low degeneracy:** The attractor is not a trivial fixed point.

This corresponds to Crutchfield's "between order and chaos" regime [Crutchfield, 2012] and Bennett's "neither trivial nor random" criterion for logical depth [Bennett, 1988].

---

## 3. Related Work

### 3.1 LLM Self-Interaction

**Model collapse** [Shumailov et al., 2024; Alemohammad et al., 2023] demonstrates that iterated self-training is a contractive map in distribution space. Variance shrinks as $O(1/n)$; tails erode; the distribution collapses to a point mass.

**Self-improvement** [Madaan et al., 2023; Yuan et al., 2024] shows that carefully designed feedback loops can improve model quality. The contrast with model collapse lies in the feedback mechanism: self-rewarding includes an explicit quality signal, while self-consuming loops do not.

**Attractor convergence** [Wang et al., 2025; Perez et al., 2024] provides empirical evidence that LLM iteration converges to fixed points or short cycles. The 2-periodicity observed in paraphrasing is a robust structural finding.

### 3.2 Formal Dynamical Systems Treatments

**Tacheny (2025)** provides a geometric framework identifying contractive (converging to attractors) and expansive (diverging) regimes in LLM iteration.

**Merrill & Sabharwal (2024)** establish that single transformer forward passes lie in TC$^0$, but chain-of-thought elevates computational power to Turing completeness.

**Qiu et al. (2024)** prove that prompting alone is Turing-complete: the prompt encodes the program, the transformer is the universal machine.

### 3.3 Classical Dynamical Systems Theory

The mathematical foundations draw from:
- Symbolic dynamics and subshifts [Lind & Marcus, 2021]
- Kolmogorov complexity [Li & Vitányi, 2019]
- Logical depth [Bennett, 1988]
- Computational mechanics [Crutchfield & Young, 1989; Shalizi & Crutchfield, 2001]
- Kleene's recursion theorem [Rogers, 1967]
- AIXI and Gödel Machines [Hutter, 2005; Schmidhuber, 2003]

---

## 4. Contributions and Organization

This work makes the following contributions:

1. **A unifying framework** for understanding LLM self-interaction as discrete dynamical systems with evolving rules.

2. **Synthesis of relevant literature** from dynamical systems, complexity theory, and LLM research.

3. **Identification of key questions** about fixed points, model collapse, creativity, and multi-agent dynamics.

4. **Complexity measures** adapted for characterizing orbit structure in finite systems.

5. **A textbook treatment** (Chapters 1--14) developing the mathematical foundations from iterated maps through AIXI to LLMs as dynamical systems.

The framework provides both conceptual clarity---revealing that disparate LLM phenomena are instances of a single dynamical structure---and a foundation for rigorous analysis as AI systems become increasingly autonomous and self-referential.

---

## References

- Alemohammad, S. et al. (2023). Self-consuming generative models go MAD. *arXiv:2307.01850*.
- Bennett, C.H. (1988). Logical depth and physical complexity. In *The Universal Turing Machine*, pp. 227--257.
- Crutchfield, J.P. (2012). Between order and chaos. *Nature Physics*, 8:17--24.
- Crutchfield, J.P. & Young, K. (1989). Inferring statistical complexity. *Phys. Rev. Lett.*, 63:105--108.
- Huang, J. et al. (2023). Large language models cannot self-correct reasoning yet. *arXiv:2310.01798*.
- Hutter, M. (2005). *Universal Artificial Intelligence*. Springer.
- Li, M. & Vitányi, P. (2019). *An Introduction to Kolmogorov Complexity and Its Applications*, 4th ed. Springer.
- Lind, D. & Marcus, B. (2021). *An Introduction to Symbolic Dynamics and Coding*, 2nd ed. Cambridge.
- Madaan, A. et al. (2023). Self-Refine: Iterative refinement with self-feedback. *arXiv:2303.17651*.
- Merrill, W. & Sabharwal, A. (2024). The expressive power of transformers with chain of thought. *arXiv:2310.07923*.
- Park, J.S. et al. (2023). Generative agents: Interactive simulacra of human behavior. *arXiv:2304.03442*.
- Perez, C.R. et al. (2024). When LLMs play the telephone game: Cultural attractors. *arXiv:2407.04503*.
- Qiu, L. et al. (2024). Ask, and it shall be given: Turing completeness of prompting. *arXiv:2411.01992*.
- Rogers, H. (1967). *Theory of Recursive Functions and Effective Computability*. McGraw-Hill.
- Schmidhuber, J. (2003). Gödel machines: Self-referential universal problem solvers. *arXiv:cs/0309048*.
- Shalizi, C.R. & Crutchfield, J.P. (2001). Computational mechanics: Pattern and prediction. *J. Stat. Phys.*, 104:817--879.
- Shumailov, I. et al. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631:755--759.
- Tacheny, N. (2025). Dynamics of agentic loops in LLMs: A geometric theory. *arXiv:2512.10350*.
- Wang, S. et al. (2025). Successive paraphrasing converges to fixed cycles. *arXiv:2502.15208*.
- Yuan, W. et al. (2024). Self-rewarding language models. *arXiv:2401.10020*.
