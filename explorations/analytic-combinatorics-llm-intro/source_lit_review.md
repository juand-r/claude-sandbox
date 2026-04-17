# Literature Review: Analytic Combinatorics and LLM Output Distributions

**Date**: 2026-04-10 (initial), 2026-04-14 (T5 / WFA-LM section expanded; attribution fix on Suresh et al.)  
**Scope**: Flajolet-Sedgewick framework, weighted formal languages, Boltzmann sampling, entropy/singularity connections, Zipf's law, formal language theory of transformers, statistical mechanics of LLMs

## Section → Thread mapping

Each section below maps to one or more research threads (T1–T5) defined in [`EXPERIMENT_README.md`](EXPERIMENT_README.md) and [`research_plan.md`](research_plan.md):

| Lit section | Topic | Threads |
|---|---|---|
| §1 | Foundational Analytic Combinatorics | T1, T2 |
| §2 | Weighted Automata and Weighted Formal Languages | T5 |
| §3 | Formal Language Theory and Transformers | T5 |
| §4 | Tightness and Language Model Foundations | T1, T3 |
| §5 | Entropy Rate and Information-Theoretic Connections | T1 |
| §6 | Stochastic CFGs and Their Generating Functions | T2 |
| §7 | Boltzmann Sampling | T3 |
| §8 | Zipf's Law and Token Distributions | T4 |
| §9 | Energy-Based Models and Statistical Mechanics of LLMs | T3 |
| §10 | Analytic Combinatorics in Information Theory | T1 |
| §11 | WFA Approximation of Neural Language Models | T5 |

---

## 1. Foundational Analytic Combinatorics
*Threads: T1, T2*


**Flajolet, P. & Sedgewick, R. (2009). *Analytic Combinatorics*. Cambridge University Press.**
The foundational text. Develops the symbolic method connecting combinatorial classes (sequences, trees, formal languages) to generating functions, then extracts asymptotics via singularity analysis. Part A covers symbolic enumeration; Part B covers complex-analytic asymptotics. The framework translates grammars into functional equations for generating functions — the core technique that could apply to LLM-defined distributions.

**Flajolet, P. & Odlyzko, A. (1990). "Singularity Analysis of Generating Functions." *SIAM J. Discrete Math.*, 3(2):216-240.**
Establishes transfer theorems: asymptotic behavior of coefficients is determined by the location and nature of dominant singularities. Exponential growth rate equals $1/R$ where $R$ is the radius of convergence. The main tool for extracting string-length asymptotics from probability generating functions.

**Pemantle, R., Wilson, M.C. & Melczer, S. (2024). *Analytic Combinatorics in Several Variables* (2nd ed.). Cambridge University Press.**
Extends Flajolet-Sedgewick to multivariate generating functions using algebraic topology and Morse theory. Directly relevant: encoding $P(w_1 \ldots w_n)$ as a multivariate GF over a token vocabulary requires exactly these techniques.

**Drmota, M. (2009). *Random Trees: An Interplay between Combinatorics and Probability*. Springer.**
Applies singularity analysis and saddle point methods to derive limit laws for random trees. Parse trees of context-free grammars are a key example — relevant to analyzing distributions over parse structures induced by PCFGs and their neural approximations.

**Drmota, M. & Szpankowski, W. (2024). *Analytic Information Theory: From Compression to Learning*. Cambridge University Press.**
Applies analytic combinatorics (Mellin transforms, depoissonization, singularity analysis) to information theory. Covers entropy computations for digital trees/tries and extends to learning theory. The closest existing bridge between the Flajolet-Sedgewick framework and information-theoretic quantities like entropy.

## 2. Weighted Automata and Weighted Formal Languages
*Thread: T5*


**Droste, M., Kuich, W. & Vogler, H. (eds.) (2009). *Handbook of Weighted Automata*. Springer.**
Comprehensive reference on weighted automata over semirings. When the semiring is $(\mathbb{R}_{\geq 0}, +, \times)$, this directly models probability distributions over strings. Foundational for formalizing LLMs as weighted language generators.

**Berstel, J. & Reutenauer, C. (2011). *Noncommutative Rational Series with Applications*. Cambridge University Press.**
Algebraic theory of noncommutative formal power series recognized by weighted automata. The generating functions of regular weighted languages are rational. Provides the algebraic foundation for understanding what distributions finite-state models can express.

**Icard, T.F. (2020). "Calibrating Generative Models: The Probabilistic Chomsky-Schutzenberger Hierarchy." *J. Mathematical Psychology*, 95:102308.**
Introduces a probabilistic version of the Chomsky hierarchy. Proves the probabilistic hierarchy is strict: more probability distributions become definable at each level. Uses analytic tools to prove non-collapse. Establishes what distributions PCFGs, pushdown automata, etc. can define probabilistically.

**Smith, N.A. & Johnson, M. (2007). "Weighted and Probabilistic Context-Free Grammars Are Equally Expressive." *Computational Linguistics*, 33(4):477-491.**
Proves every distribution defined by a weighted CFG can also be defined by some PCFG. The extra generality of arbitrary positive weights doesn't buy additional distributional expressiveness for context-free models.

**Rabusseau, G., Li, T. & Precup, D. (2019). "Connecting Weighted Automata and Recurrent Neural Networks through Spectral Learning." *AISTATS 2019*.**
Establishes a formal correspondence between WFAs and second-order RNNs, and shows how the classical spectral learning algorithm for WFAs can be applied to learn RNNs. The key bridge between the WFA and RNN-LM literatures: WFAs and 2nd-order RNNs realize the same class of functions when both have the same number of states. Foundational reference for any extraction-based WFA-LM approximation pipeline (T5).

## 3. Formal Language Theory and Transformers
*Thread: T5*


**Strobl, L., Merrill, W., Weiss, G., Chiang, D. & Angluin, D. (2024). "What Formal Languages Can Transformers Express? A Survey." *TACL*, 12:543-561. arXiv:2311.00208.**
Comprehensive survey connecting transformer variants to circuit complexity classes (AC0, TC0). Expressiveness depends critically on architecture. Essential for understanding what LLM output distributions look like from a formal language perspective.

**Merrill, W. & Sabharwal, A. (2022). "Saturated Transformers are Constant-Depth Threshold Circuits." *TACL*, 10:843-856. arXiv:2106.16213.**
Saturated transformers bounded by TC0 in circuit complexity. Constrains which formal languages transformers can recognize and which probability distributions over strings they can represent.

**Merrill, W. & Sabharwal, A. (2024). "The Expressive Power of Transformers with Chain of Thought." *ICLR 2024*.**
Chain-of-thought expands transformer expressiveness beyond TC0. Autoregressive generation with CoT changes the class of distributions a transformer can produce.

**Hahn, M. (2020). "Theoretical Limitations of Self-Attention in Neural Sequence Models." *TACL*, 8:156-171. arXiv:1906.06755.**
Self-attention cannot model periodic finite-state languages or hierarchical structure unless depth/width grows with input. Establishes fundamental limits on the generating function structure bounded-depth transformers can implement.

**Svete, A. & Cotterell, R. (2023). "Recurrent Neural Language Models as Probabilistic Finite-state Automata." *EMNLP 2023*. arXiv:2310.05161.**
Simple RNNs are equivalent to a subclass of probabilistic finite-state automata. RNN language models define distributions that are a strict subset of those expressible by PFSAs — a key formalization bridging neural sequence models and weighted automata.

**Rizvi-Martel, M. et al. (2024). "Simulating Weighted Automata over Sequences and Trees with Transformers." *AISTATS 2024*. arXiv:2403.09728.**
Transformers with $O(\log T)$ layers can approximately simulate all weighted finite automata at length $T$. Transformers can learn shortcuts to significantly more complex sequence models than DFAs.

**Yun, C., Bhojanapalli, S., Rawat, A.S., Reddi, S.J. & Kumar, S. (2020). "Are Transformers Universal Approximators of Sequence-to-Sequence Functions?" *ICLR 2020*. arXiv:1912.10077.**
Transformers are universal approximators of continuous sequence-to-sequence functions on compact domains. In principle they can approximate any continuous probability mapping over sequences.

## 4. Tightness and Language Model Foundations
*Threads: T1, T3*


**Cotterell, R., Svete, A., Meister, C., Liu, T. & Du, L. (2023). "Formal Aspects of Language Modeling." arXiv:2311.04329.**
Course notes covering theoretical foundations: definitions of language models as distributions over strings, tightness, connections to weighted automata. Bridge document between formal language theory and modern LLM practice.

**Du, L., Hennigen, L.T., Pimentel, T., Meister, C., Eisner, J. & Cotterell, R. (2023). "A Measure-Theoretic Characterization of Tight Language Models." *ACL 2023*. arXiv:2212.10502.**
Addresses whether LM probability mass "leaks" onto infinite strings. Proves many popular LM families are tight. This is the measure-theoretic analog of asking whether the probability generating function evaluates to 1 at $z=1$.

**Booth, T.L. & Thompson, R.A. (1973). "Applying Probability Measures to Abstract Languages." *IEEE Trans. Computers*, C-22:442-450.**
Derives conditions for a PCFG to define a proper probability distribution (consistency). The consistency condition is essentially that the probability generating function of the grammar converges — a foundational connection between GFs and probabilistic grammars.

## 5. Entropy Rate and Information-Theoretic Connections
*Thread: T1*


**Shannon, C.E. (1951). "Prediction and Entropy of Printed English." *Bell System Technical Journal*, 30:50-64.**
Shannon's original entropy rate estimation for English. The foundational reference.

**Kontoyiannis, I., Algoet, P.H., Suhov, Yu.M. & Wyner, A.J. (1998). "Nonparametric Entropy Estimation for Stationary Processes." *IEEE Trans. IT*, 44(3):1319-1327.**
Consistent estimators for entropy rate based on longest match-lengths. Return-time statistics whose generating functions are analyzable by singularity methods.

**Scharringhausen, M. (2026). "Entropy in Large Language Models." arXiv:2602.20052.**
Estimates LLM output entropy rates as limits of conditional entropies with increasing context length. The entropy rate equals $\log(1/R)$ where $R$ is the radius of convergence of the probability generating function — a concrete connection point.

**Takahira, R. et al. (2025). "Large Language Models and the Entropy of English." arXiv:2512.24969.**
Uses LLMs to play Shannon's guessing game; finds correlations spanning entire text length, challenging mean-field models. LLM-estimated entropy converges slowly, which has implications for the singularity structure of the corresponding generating function.

**Giulianelli, M. et al. (2024). "Cross Entropy of Neural Language Models at Infinity." *Entropy*, 22(10):1148.**
Extrapolates neural LM cross-entropy to infinite training data and context, obtaining ~1.12 bits/char for English. Implicitly characterizes the radius of convergence of the probability generating function.

## 6. Stochastic CFGs and Their Generating Functions
*Thread: T2*


**Chi, Z. (1999). "Statistical Properties of Probabilistic Context-Free Grammars." *Computational Linguistics*, 25(1):131-160.**
PCFGs estimated by ML have proper distributions with finite entropy; parse-tree sizes have finite moments of all orders. Uses generating function methods — the GF of parse-tree size satisfies an algebraic equation (by Chomsky-Schutzenberger), and convergence/consistency is determined by its radius of convergence.

**Chomsky, N. & Schutzenberger, M.-P. (1963). "The Algebraic Theory of Context-Free Languages." In *Computer Programming and Formal Systems*, pp. 118-161.**
The foundational theorem: the generating function counting words of length $n$ in an unambiguous CFL is algebraic over $\mathbb{Q}(x)$. CF languages have GFs satisfying polynomial equations, whose singularities are algebraic branch points. The universal asymptotic form $n^{-3/2} \rho^{-n}$ for CF languages. Directly applicable to analyzing length distributions of LLM outputs.

**Corazza, A. & Satta, G. (2006). "Estimation of Consistent Probabilistic Context-free Grammars." *NAACL-HLT 2006*.**
Derivational entropy of PCFGs coincides with cross-entropy when used as estimation objective. Uses generating function analysis to prove consistency.

## 7. Boltzmann Sampling
*Thread: T3*

This section underpins T3, which aims to formalize the relationship between temperature-scaled LLM sampling and the Boltzmann samplers invented by the analytic combinatorics community. Two mostly-disjoint literatures use the word "Boltzmann": one stemming from Duchon, Flajolet, Louchard and Schaeffer's work on random generation of combinatorial structures, and one stemming from the statistical-mechanics / machine-learning tradition most recently revived by Noe et al.'s "Boltzmann generators." They do not cite each other. Part of T3's contribution is to make the bridge explicit.

**What a Boltzmann sampler is.** Given a combinatorial class $\mathcal{C}$ with counting sequence $(c_n)_{n \geq 0}$ and ordinary generating function $A(z) = \sum_{n \geq 0} c_n z^n$, pick a real tuning parameter $x \in (0, R)$ inside the disk of convergence. The Boltzmann sampler of parameter $x$, denoted $\Gamma A(x)$, draws an object $\gamma \in \mathcal{C}$ with probability
$$\mathbb{P}_x(\gamma) \;=\; \frac{x^{|\gamma|}}{A(x)},$$
where $|\gamma|$ is the size of $\gamma$. Equivalently, the *size* of the output is a random variable $N$ with $\mathbb{P}_x(N = n) = c_n x^n / A(x)$, and conditioned on $N = n$ the object is uniform among the $c_n$ structures of that size. Two facts give the scheme its power. First, $x$ acts as a dial on the expected size: $\mathbb{E}_x[N] = x A'(x)/A(x)$, and by choosing $x$ near $R$ one can make the sampler produce arbitrarily large objects. Second, because the distribution factors multiplicatively, Boltzmann samplers for sums, products, sequences, sets and cycles can be composed recursively from the symbolic specification of the class, so essentially any class describable in the Flajolet-Sedgewick framework admits a linear-time random generator (once the relevant GF values are precomputed).

**Duchon, Flajolet, Louchard and Schaeffer (2004).** This is the foundational paper of the area. It introduces the free Boltzmann model above, gives explicit samplers for each of the constructions of the symbolic method (union, product, SEQ, SET, CYC, MSET), shows that in the unlabeled setting rejection on $N = n$ produces an exact-size uniform sampler at only polynomial overhead, and proves that for nice (e.g., algebraic) classes the scheme runs in linear expected time. The tuning parameter $x$ is explicitly interpreted as controlling target size: given a desired $n$, one chooses $x = x_n$ so that $\mathbb{E}_{x_n}[N] = n$, which for classes with square-root or logarithmic singularity types yields optimal "singular" samplers. The paper's conceptual move — replacing exact-size uniform generation by size-biased generation with a tunable intensity — is precisely the move that makes energy-weighted sampling tractable, and it is the move a temperature-scaled LLM performs implicitly.

**Duchon, Flajolet, Louchard and Schaeffer (2011).** The longer survey extends the 2004 framework to labeled classes (via exponential generating functions), multi-parameter and multi-type specifications, and recursive classes defined by systems of functional equations, and it catalogues the oracle requirements (how accurately $A(x)$ must be known for the samplers to be correct). For T3 the decisive passage is the explicit statistical-mechanics translation. If one identifies the "size" $|\gamma|$ of a combinatorial object with an energy $E(\gamma)$ and writes $x = e^{-\beta}$, the Boltzmann-sampler distribution becomes
$$\mathbb{P}_\beta(\gamma) \;=\; \frac{e^{-\beta E(\gamma)}}{A(e^{-\beta})} \;=\; \frac{e^{-\beta E(\gamma)}}{Z(\beta)},$$
i.e., the Gibbs-Boltzmann distribution with partition function $Z(\beta) = A(e^{-\beta})$. The generating function *is* the partition function, the radius of convergence corresponds to a phase transition, and the singular tuning $x \to R^-$ corresponds to $\beta \to \beta_c$. This translation — present in the analytic-combinatorics literature but unknown to most of machine learning — is the hinge on which T3 turns.

**Noe, Olsson, Kohler and Wu (2019).** "Boltzmann generators" approach the same sampling problem from the opposite end. The target is a physical Gibbs distribution $p(x) \propto e^{-u(x)/kT}$ over molecular configurations, which is not defined by a combinatorial recursion but by an intractable continuous potential. Instead of building the sampler out of the structure of the target, Noe et al. train an invertible neural network (a normalizing flow) that pushes a simple latent Gaussian onto the equilibrium distribution; importance reweighting and an energy loss correct residual bias. The result is a sampler that draws independent, rare conformational states of small proteins and spin systems, something MD and MCMC cannot do in any reasonable time. For this review the paper matters for two reasons. First, it shows that the Gibbs-Boltzmann objective is tractable by learned, amortized samplers — the same computational posture as an LLM, which is an amortized sampler over strings. Second, and crucially for the historical story: Noe et al. do not cite Duchon et al., and Duchon et al. have nothing to say about neural networks. The two "Boltzmann sampling" literatures developed in parallel.

**The T3 hook.** An autoregressive LLM with base distribution $\mu$ and temperature $T$ generates a string $w$ with probability proportional to $\mu(w)^{1/T} = \exp(\log \mu(w) / T)$. Defining the energy $E(w) := -\log \mu(w)$, this rewrites as
$$\mathbb{P}_T(w) \;\propto\; e^{-E(w)/T},$$
which is structurally a Gibbs-Boltzmann distribution with inverse temperature $\beta = 1/T$ and energy $E$. Matching this against the Duchon et al. form $\mathbb{P}_x(\gamma) \propto x^{|\gamma|}/A(x)$ makes the identification $x = e^{-1/T}$ natural — but only *if* the LLM energy $E(w)$ can be written as a (possibly weighted) size on some combinatorial class whose generating function plays the role of $A(x)$. This is the central open question of T3: is temperature-scaled LLM sampling a Boltzmann sampler in the Duchon-Flajolet sense, and if so, for what combinatorial class $\mathcal{C}$ and what size function $|\cdot|$? The candidate classes — weighted strings, parse trees of an extracted PCFG, paths in an extracted WFA (§2, §6, §11) — are exactly the objects studied elsewhere in this review, which is why T3 sits at the confluence of the other threads rather than as a standalone project. Bridging the Flajolet-Sedgewick and Noe-style literatures is itself a contribution: the analytic-combinatorics side supplies exact enumeration and singularity machinery, the ML side supplies amortized learned samplers, and LLMs sit uncomfortably between them.

## 8. Zipf's Law and Token Distributions
*Thread: T4*


**Piantadosi, S.T. (2014). "Zipf's Word Frequency Law in Natural Language: A Critical Review." *Psychonomic Bulletin & Review*, 21(5):1112-1130.**
Comprehensive review of Zipf's law in language. Frequency distribution has complex structure beyond simple power law. Evaluates information-theoretic, optimization, and random-process explanations.

**Goldwater, S., Griffiths, T.L. & Johnson, M. (2011). "Producing Power-Law Distributions and Damping Word Frequencies with Two-Stage Language Models." *JMLR*, 12:2335-2382.**
Pitman-Yor process adaptors on generative models naturally produce Zipfian power laws. Could the generating function of a Pitman-Yor adapted LM be analyzed via singularity methods to derive Zipf exponents?

**Eliazar, I. (2025). "Random Text, Zipf's Law, Critical Length, and Implications for Large Language Models." arXiv:2511.17575.**
Fully explicit character-level random text model where Zipf's law emerges from pure combinatorics (exponential growth of possible strings vs. exponential decay of individual probabilities). Derives exact Zipf exponents from alphabet size. Directly connects combinatorial generating function analysis to Zipf-like patterns.

**Kawakami, K. et al. (2025). "Zipf's and Heaps' Laws for Tokens and LLM-generated Texts." *EMNLP 2025 Findings*.**
Empirically verifies that LLM-generated text follows Zipf's and Heaps' laws at the token level. Tokenization scheme affects the power-law exponents. Establishes empirical ground truth for LLM token distributions.

**Michaud, E.J. et al. (2024). "AlphaZero Neural Scaling and Zipf's Law: a Tale of Board Games and Power Laws." arXiv:2412.11979.**
"Quantization model" explaining power-law neural scaling via Zipf's law: LLMs learn discrete task quanta in order of frequency. Connects Zipf distributions to neural scaling laws.

## 9. Energy-Based Models and Statistical Mechanics of LLMs
*Thread: T3*


**Gao, A. et al. (2024). "Autoregressive Language Models are Secretly Energy-Based Models." arXiv:2512.15605.**
Explicit bijection between autoregressive models and energy-based models via the soft Bellman equation. The EBM perspective makes the partition function explicit, connecting directly to generating function formalism.

**Kempton, T. & Burrell, S. (2025). "Local Normalization Distortion and the Thermodynamic Formalism of Decoding Strategies for Large Language Models." *EMNLP 2025 Findings*. arXiv:2503.21929.**
Applies thermodynamic formalism from ergodic theory to LLM decoding. Expresses top-k, nucleus, and temperature sampling as equilibrium states and derives their objective functions. Shows local normalization (inherent to autoregressive generation) creates a fundamental distortion. **The most direct existing connection** between the mathematical machinery of statistical mechanics/dynamical systems and LLM sampling — but does not use generating functions.

**Nakaishi, K. et al. (2024). "Phase Transitions in the Output Distribution of Large Language Models." arXiv:2405.17088.**
Adapts statistical physics methods for detecting phase transitions in LLM output distributions. Finds phase-transition-like behavior in Pythia, Mistral, and Llama families. Phase transitions correspond to singularities in generating functions.

**Nakaishi, K. (2024). "Critical Phase Transition in Large Language Models." arXiv:2406.05335.**
GPT-2 exhibits a genuine phase transition under temperature scaling, with energy following scaling laws near a critical temperature. Directly connects the softmax temperature parameter to inverse temperature in statistical mechanics.

**Lin, H.W., Tegmark, M. & Rolnick, D. (2017). "Why Does Deep and Cheap Learning Work So Well?" *J. Statistical Physics*, 168:1223-1247. arXiv:1608.08225.**
Physical laws exhibit symmetry, locality, compositionality, and polynomial log-probability. The "polynomial log-probability" observation suggests GFs of physically-relevant distributions have specific singularity structures.

## 10. Analytic Combinatorics in Information Theory
*Thread: T1*


**Szpankowski, W. (2001). *Average Case Analysis of Algorithms on Sequences*. Wiley.**
Applies analytic combinatorics to algorithms on sequences (tries, suffix trees, compression). The sequences analyzed are precisely the kind of token sequences LLMs generate, and the analytic tools are the same ones proposed here.

**Jacquet, P. & Szpankowski, W. (1991). "Analysis of Digital Tries with Markovian Dependency." *IEEE Trans. IT*, 37(5):1470-1475.**
Analyzes digital tries under Markov source models using analytic methods. Autoregressive LMs define a high-order Markov source over tokens; the generating function analysis of trie-like structures could characterize statistical properties of LLM outputs.

**Nicodeme, P., Salvy, B. & Flajolet, P. (2002). "Motif Statistics." *Theoretical Computer Science*, 287(2):593-617.**
Complete distributional analysis of pattern occurrences in random text using GFs and singularity analysis. Applied to Markov sources. Same techniques could analyze frequency of specific token patterns in LLM-generated text.

## 11. WFA Approximation of Neural Language Models
*Thread: T5*


**Suresh, A.T., Roark, B., Riley, M. & Schogol, V. (2021). "Approximating Probabilistic Models as Weighted Finite Automata." *Computational Linguistics*, 47(2):221-261. arXiv:1905.08701.**
The principled construction for approximating arbitrary probabilistic sequence models (including neural LMs) as WFAs while minimizing KL divergence. Combines a counting step with difference-of-convex optimization. Demonstrated for distilling n-gram models from neural nets, building compact LMs, and open-vocabulary character models. **The most-cited reference across the WFA-LM-approximation literature.** If an LLM can be approximated as a WFA in this principled way, its generating function is rational, and the full Flajolet-Sedgewick machinery for rational GFs applies in principle. But Suresh et al. do not connect to analytic combinatorics, and nobody on either side has asked how the quality of the WFA approximation relates to the accuracy of asymptotic predictions extracted from the rational GF.

**Schwartz, R., Thomson, S. & Smith, N.A. (2018). "Bridging CNNs, RNNs, and Weighted Finite-State Machines." *ACL 2018*. arXiv:1805.05022.**
Introduces *rational recurrences* — a class of RNN architectures whose hidden states correspond to weighted finite-state automata. Shows that several existing RNN variants (e.g., specific gated CNNs and SRUs) compute exactly the same functions as a particular WFSA. A different angle on the LLM ↔ WFA correspondence than Suresh et al.: rather than approximating a black-box LM with a WFA after the fact, identify which neural architectures are *literally equivalent* to WFAs by construction. Useful for T5 because it characterizes a family of trainable LMs whose generating functions are rational by definition.

**Lecorvé, G. & Motlicek, P. (2012). "Conversion of Recurrent Neural Network Language Models to Weighted Finite State Transducers for Automatic Speech Recognition." *Interspeech 2012*.**
The classical RNNLM → WFST distillation paper, predating the deep-learning era. Proposes practical methods for converting an RNN-based LM into a weighted FST suitable for ASR rescoring. Historical anchor for the line of work that culminates in Suresh et al. 2021 and Lacroce et al. 2021/2024. Cited by the VQ-T paper (Shi et al. 2022) as the founding reference for this line.

**Lacroce, C., Panangaden, P. & Rabusseau, G. (2021). "Extracting Weighted Automata for Approximate Minimization in Language Modelling." *15th International Conference on Grammatical Inference (ICGI)*, PMLR vol. 153, pp. 92-112.**
Applies the Adamyan-Arov-Krein (AAK) operator-theoretic framework to black-box language models. Shows that "compactness" (the technical condition that the Hankel operator is bounded and finite-rank-approximable) is automatically satisfied by black-box LMs trained on sequential data, then proposes an AAK-based approximate minimization algorithm in the one-letter setting. **The direct theoretical bridge between the WFA-LM-approximation literature and operator theory** — and a natural place to plug in Flajolet-Sedgewick singularity analysis on the resulting rational GF, which they do not do.

**Lacroce, C., Balle, B., Panangaden, P. & Rabusseau, G. (2024). "Optimal Approximate Minimization of One-Letter Weighted Finite Automata." *Mathematical Structures in Computer Science*, 34:807-833.**
First *optimal* approximate minimization of WFAs (in the spectral norm of the Hankel matrix), restricted to one-letter alphabets and irredundant WFAs ($\rho(A) < 1$). Closed-form, $O(n^3)$ in WFA state count. Crucial machinery: identifies the WFA's output sequence with a rational function $f(k) = \alpha^\top A^k \beta = \alpha^\top(zI - A)^{-1}\beta$ — literally the rational generating function of the sequence — and uses AAK theory to find its best low-rank Hankel approximation. The poles of the GF are the eigenvalues of $A$. They use this structure operationally for the AAK construction but **never extract asymptotics from the pole structure** — their bibliography is entirely operator theory and $H^\infty$ control (Adamyan-Arov-Krein, Glover, Antoulas, Nikol'skii, Peller); zero references to Flajolet, Sedgewick, Drmota, or Wilf. **The "one-letter" restriction is less fatal than it first looks**: if we project LLM output to a scalar sequence (e.g., output length per step, frequency of a marker token, count of a parameter), the projected sequence lives in one-letter territory and the AAK machinery applies directly. This is a key methodological insight for T5.

**Weiss, G., Goldberg, Y. & Yahav, E. (2018). "Extracting Automata from Recurrent Neural Networks Using Queries and Counterexamples." *ICML 2018*.**
Different line: extracts a *deterministic* finite automaton from a trained RNN using L*-style learning with queries and counterexamples. Not probabilistic, so the resulting automaton doesn't directly give a generating function over a distribution, but characterizes what regular language the RNN classifier represents. Useful background for understanding what RNNs can or cannot represent as finite-state objects.

---

## Key Gaps — Where the Research Opportunity Lies

1. **No one has explicitly constructed the probability generating function of an LLM's output distribution and analyzed its singularity structure.** The pieces exist individually but have never been connected.

2. **The entropy rate = $\log(1/R)$ connection is unstated.** Entropy rate estimation for LLMs is active, and the relationship between entropy and radius of convergence is well-known in analytic combinatorics, but no one has exploited this to derive entropy rate bounds from GF singularity analysis.

3. **Boltzmann sampling and LLM temperature sampling have never been formally connected.** The structural parallel is obvious but no paper establishes the formal correspondence.

4. **Multivariate generating functions for token-level distributions are unexplored.** The Pemantle-Wilson-Melczer machinery has never been applied to the multivariate GF encoding $P(w_1 \ldots w_n)$ over a token vocabulary.

5. **The Chomsky-Schutzenberger algebraic GF structure has not been connected to LLM approximations.** If LLMs approximately implement CF-like structure, their output GFs should be approximately algebraic, with square-root-type singularities yielding $n^{-3/2} \rho^{-n}$ asymptotics. Nobody has checked this.

6. **Limit law derivation for LLM outputs via analytic combinatorics is completely open.** The framework routinely derives Gaussian limit laws, large deviations, etc. from GF structure.

7. **The thermodynamic formalism paper (Kempton & Burrell 2025) does not use generating functions.** Combining their equilibrium-state framework with GF/singularity analysis would be novel.

8. **No systematic study of which singularity types arise in LLM-induced GFs.** Rational (poles), algebraic (branch points), and exotic singularities yield qualitatively different asymptotics. Characterizing which types LLMs produce is open.

9. **The WFA approximation path is underexploited.** If LLMs are well-approximated by WFAs, their GFs are approximately rational — but nobody has tested whether the resulting asymptotic predictions are accurate.

10. **Phase transitions as singularity phenomena.** Nakaishi et al. (2024) empirically observe phase transitions; in analytic combinatorics, phase transitions correspond to confluent singularities. The formal connection is unstated.

11. **The WFA-LM-approximation literature and analytic combinatorics work on the same object but never cite each other.** Suresh et al. (2021), Lacroce et al. (2021), Lacroce et al. (2024), and the broader Rabusseau / Balle / Panangaden line build WFA approximations of LMs and analyze them via Hankel-operator theory, AAK theorems, and $H^\infty$ control machinery (Adamyan-Arov-Krein, Glover, Antoulas, Nikol'skii, Peller). The Flajolet-Sedgewick line works on identical mathematical objects — rational generating functions $f(k) = \alpha^\top A^k \beta = \alpha^\top(zI - A)^{-1}\beta$ with poles inside the unit disc — and extracts term-by-term asymptotics from singularity structure. **Neither side cites the other.** Lacroce et al. (2024) do not reference Flajolet, Sedgewick, Drmota, or Wilf; the FS line does not reference AAK theory or operator-theoretic model reduction. Building this bridge — applying singularity analysis to the rational GFs that come out of WFA-LM approximations — is a clean unexplored research opportunity for T5 and a substantive contribution if executed properly.

12. **The "one-letter" restriction in operator-theoretic WFA minimization is a feature, not a bug, when combined with scalar-projection of LLM output.** The most powerful results in WFA approximate minimization (Lacroce et al. 2024, AAK-based, optimal in spectral norm, closed-form) are restricted to one-letter alphabets, which seems to rule out direct application to LLM token sequences. But projecting the LLM output to *any scalar sequence* — output length per step, frequency of a specific token, depth of a syntactic structure, distance from the prompt embedding — collapses the problem to a one-letter setting where the AAK machinery applies in full. T5's measurement design should explicitly target scalar projections that make this collapse work.

---

## Literature Gaps (Expanded)

### Ten open problems at the frontier of analytic combinatorics and LLMs

To our knowledge, all ten research gaps discussed below remain open: a search across arXiv, Google Scholar, Semantic Scholar, and ACL Anthology did not turn up any paper that addresses any of them, even partially. The pattern is consistent: rich, mature bodies of work exist on both sides (Flajolet–Sedgewick analytic combinatorics on one side, LLM analysis on the other), but the specific mathematical bridges between them have not been constructed. What follows is a gap-by-gap discussion with the closest related work identified for each.

**Scope note.** This expansion covers the first ten items of the Key Gaps list above. Gaps #11 and #12, added during the April 2026 lit-review expansion, are specific to the T5 (WFA approximation) thread and are discussed in §§2 and 11 of [`literature_deep_dive.md`](literature_deep_dive.md) rather than repeated here.

---

#### Gaps 1 and 2: the foundational PGF and entropy-rate connection

**Gap 1 — Explicit GF construction and singularity analysis.** No paper constructs and analyzes the generating functions naturally associated with an LLM's output distribution. Two distinct GFs are relevant here and should not be conflated. (a) The *length probability generating function* $P(z) = \sum_n p_n z^n$, with $p_n$ the probability the model emits a string of length $n$, is itself a probability distribution (satisfying $P(1)=1$ for a tight model, so its radius of convergence is at least $1$). Its singularity structure near $z=1$ encodes the *shape of the length tail* — polynomial vs. exponential decay, the exponent of any polynomial prefactor, and the critical rate of exponential decay. (b) A separate *counting-type* GF — over typical strings of length $n$, over effective-vocabulary counts, or over Rényi-type moments of the model's distribution — has exponential growth rate tied to the entropy rate (Gap 2) and is a different object. Neither has been written down for a neural language model, let alone analyzed. The classical framework is well-established for formal languages — regular languages yield rational GFs (Chomsky–Schützenberger), unambiguous CFLs yield algebraic GFs — but this machinery has not been applied to neural language model output distributions. The closest related work is Zhang, Wang & Giles (2021, *Entropy*), which uses GFs of regular grammars to define an entropy metric for classifying grammar difficulty for RNN learning. That paper works with formal regular grammars, not with the output distribution of a trained neural model. Singular Learning Theory (Watanabe; Lau et al., arXiv:2308.12108) studies singularities in a completely different sense — parameter-space geometry of loss landscapes, not analytic properties of output-distribution GFs.

**Gap 2 — Entropy rate $= \log(1/R)$ for LLMs.** For a stationary source, the entropy rate $h$ is the exponential growth rate of the typical set: there are roughly $2^{nh}$ typical strings of length $n$, each with probability $\approx 2^{-nh}$. Packaging those counts into a generating function $A(z) = \sum_n a_n z^n$ yields a radius of convergence $R = 2^{-h}$, so $h = \log_2(1/R)$. This identity is standard in symbolic dynamics and analytic combinatorics for Markov chains and finite automata. Separately, a substantial literature estimates LLM entropy rates via cross-entropy and extrapolation (Takahashi & Tanaka-Ishii 2018; Braverman et al. 2020, arXiv:1906.05664). But to our knowledge no paper bridges these two worlds. Han & Marcus (2006, arXiv:math/0507235) proved the entropy rate of hidden Markov chains is analytic in model parameters, but that concerns analyticity of $h(\theta)$ in the *parameters*, not the $h = \log(1/R)$ relationship for any GF on the output side. Note that this connection is *not* about the length PGF of Gap 1(a) — that object is a probability distribution with $P(1)=1$ and radius at least $1$, so $\log_2(1/R)$ is at most $0$ and cannot encode a positive entropy rate. Exploiting $h = \log(1/R)$ for LLMs requires constructing a counting-type or typical-set GF (Gap 1(b)) specifically, and showing that its dominant singularity lies at $R = 2^{-h}$.

---

#### Gaps 3 and 6: sampling and distributional results remain unlinked

**Gap 3 — Boltzmann sampling ↔ LLM temperature sampling.** The informal analogy is obvious — both use exponential weighting — but no paper formally establishes the mathematical correspondence between Flajolet-style Boltzmann sampling (Duchon–Flajolet–Louchard–Schaeffer 2004, where objects of size $n$ receive probability $\propto x^n/A(x)$) and temperature-scaled softmax sampling in LLMs. Yang (2024, arXiv:2407.21092) interprets LLMs through the *statistical mechanics* Boltzmann distribution, defining partition functions and free energy, but uses physics thermodynamics rather than combinatorial Boltzmann sampling and does not involve generating functions. Bodini & Ponty (2010, arXiv:1002.0046) apply combinatorial Boltzmann sampling to context-free languages — the right framework, but for formal grammars rather than neural models. The two "Boltzmann" traditions (combinatorics vs. physics) have not been reconciled in the LLM context.

**Gap 6 — Limit laws for LLM outputs via analytic combinatorics.** To our knowledge no paper derives Gaussian limit laws, large deviations, or any distributional result for LLM output statistics using GF/singularity analysis. Hwang's quasi-power theorem (1998), the standard tool for deriving CLTs from GF asymptotics, has never been applied to language model outputs. Classical results show that terminal-symbol distributions in context-free languages are asymptotically normal (Drmota's work, Bender's multivariate CLT), but these apply to formal grammars under uniform random generation. Even for simpler models like PCFGs or $n$-gram models, no paper uses GF singularity analysis to derive distributional results for generated-text statistics such as sentence length, token frequency, or syntactic depth.

---

#### Gaps 5 and 9: algebraic structure and the WFA pipeline

**Gap 5 — Chomsky–Schützenberger algebraic GF structure for LLMs.** The Drmota–Lalley–Woods theorem (extended by Banderier & Drmota 2015) establishes that strongly connected CFGs yield the universal asymptotic form $C \cdot \rho^{-n} \cdot n^{-3/2}$ from square-root singularities in algebraic GFs. Separately, a growing body of work shows transformers can learn CFG-like structure: Allen-Zhu & Li (2023, arXiv:2305.13673) demonstrated GPT-2 learning synthetic CFGs with near-perfect accuracy and attention patterns resembling dynamic programming; Delétang et al. (2023, ICLR) tested neural architectures across the Chomsky hierarchy; Strobl et al. (2024, *TACL*) surveyed transformer expressivity through formal language theory. Yet none of these papers, to our knowledge, examines whether the output distributions have approximately algebraic GFs, tests for the $n^{-3/2}$ signature, or uses GF asymptotics as a diagnostic for context-free-like behavior.

**Gap 9 — WFA approximation → rational GF → asymptotic predictions.** The WFA extraction pipeline is well-developed. Suresh, Roark, Riley & Schogol (2021, *Computational Linguistics* 47(2)) approximate LSTM language models as WFAs by minimizing KL divergence. Okudono et al. (2020, AAAI) extract WFAs from RNNs via regression on state spaces. Svete & Cotterell (2023, EMNLP) establish formal equivalences between Heaviside Elman RNNs and deterministic probabilistic FSAs. The mathematical step from WFA to rational GF is textbook-trivial: $G(z) = \alpha \cdot (I - zA)^{-1} \cdot \beta$, yielding poles whose locations determine asymptotic behavior. What is missing is the *application* of this equivalence to LLM-extracted WFAs: we are aware of no paper that takes a WFA approximation of a modern LM, computes its rational GF, applies Flajolet–Sedgewick dominant-pole singularity analysis, and compares the resulting asymptotic predictions against samples from the original model. WFA-extraction work evaluates using perplexity or classification accuracy, never through GF singularity analysis.

---

#### Gaps 4 and 7: advanced machinery awaiting application

**Gap 4 — Pemantle–Wilson–Melczer ACSV for token distributions.** The ACSV machinery (Pemantle–Wilson 2013; second edition with Melczer, Cambridge 2024) provides powerful tools for extracting asymptotics from multivariate generating functions via Cauchy integrals and Morse-theoretic methods. Its applications span lattice path enumeration, queueing theory, random graphs, and statistical mechanics. The closest application to information/coding theory is Lenz, Melczer, Rashtchian & Siegel (2025, *IEEE Trans. Inf. Theory* 71(11):8223), which applies ACSV to cost-constrained channels. We could not find an application of ACSV to natural language, NLP, or token-level distributions, nor a citation of the ACSV textbook from a language-modeling paper.

**Gap 7 — Thermodynamic formalism + GF analysis for LLM decoding.** Kempton & Burrell (2025, arXiv:2503.21929) is confirmed as applying thermodynamic formalism to LLM decoding. They express top-$k$, nucleus, and temperature sampling as *equilibrium states* in Bowen's ergodic theory framework, analyzing "local normalization distortion" from repeated renormalization of truncated distributions. Their follow-up (Kempton, Burrell & Cheverall, AISTATS 2025) applies this to AI-text detection. However, both papers operate entirely within the ergodic theory tradition — no generating functions, no singularity analysis, no Flajolet–Sedgewick or Pemantle–Wilson machinery — and we are not aware of any other paper combining thermodynamic formalism with GF analysis in a language/text context.

---

#### Gaps 8 and 10: singularity classification and phase transitions

**Gap 8 — Singularity type classification for LLM-induced GFs.** The classification of singularity types by formal language class is well-established: regular → rational (poles), unambiguous CFL → algebraic (branch points), and indexed grammars can produce natural boundaries (Bousquet-Mélou, arXiv:1102.1779). But LLMs using attention mechanisms and continuous representations do not correspond to any standard formal language class. To our knowledge no paper has formulated the precise mathematical framework for defining "the generating function of an LLM" in a way amenable to singularity classification, let alone characterized whether such GFs are rational, algebraic, or exotic. Lin & Tegmark (2017, arXiv:1606.06737) connected formal language classes to criticality and noted that deep models can exhibit critical behavior, but did not classify GF singularity types.

**Gap 10 — Phase transitions as confluent singularities.** Nakaishi, Nishikawa & Hukushima (2024, arXiv:2406.05335) demonstrated a phase transition in GPT-2 at critical temperature $T_c \approx 1.0$, with power-law correlation decay and critical slowing down. This has been replicated and extended: Bölte et al. (arXiv:2405.17088) detected transitions across Pythia, Mistral, and Llama families; Mikhaylovskiy (arXiv:2503.06330) confirmed universality across Qwen and Phi models; Li et al. (arXiv:2501.16241) mapped transformers to $\mathrm{O}(N)$ lattice models. On the analytic combinatorics side, Flajolet–Sedgewick (Ch. VI.9) and subsequent work (Banderier–Kuba–Wallner, arXiv:2103.03751) characterize phase transitions as coalescence of singularities in composition schemes $F(z) = G(H(z))$. But to our knowledge no paper connects these two perspectives. The LLM phase transition literature uses exclusively statistical physics frameworks (Ising, $\mathrm{O}(N)$, Potts models), never GF singularity analysis.

---

### Why all ten gaps remain open simultaneously

The pattern across all ten gaps is not coincidental. It reflects a **structural disconnect between two research communities**. Analytic combinatorics has deep tools for extracting asymptotic information from generating functions but has historically applied them to formal languages and discrete structures with clean combinatorial specifications. The LLM research community analyzes neural models using information-theoretic, statistical, and empirical methods but does not engage with GF-based approaches. The few researchers who work at the boundary — studying transformer expressivity through formal language theory (Merrill 2021; Strobl et al. 2024) or applying thermodynamic formalism to decoding (Kempton & Burrell 2025) — stop short of the generating-function bridge.

The most tractable entry point is likely **Gap 9** (the WFA pipeline), since each component step is individually well-understood and the rational GF from a WFA extraction is immediately computable. Success there would feed directly into Gaps 1, 2, and 8: rational GFs give poles, which yield length-distribution asymptotics (Gap 1), an entropy-rate read via the dominant pole (Gap 2), and an immediate singularity-type classification (Gap 8). Gap 9 does *not* address Gap 5, however: the $n^{-3/2}$ signature is a consequence of square-root branch points in *algebraic* GFs, which a rational WFA approximation cannot produce. A WFA that fits an LLM well would, if anything, be evidence that the LLM sits in the rational regime rather than the algebraic one, and the two diagnostics are mutually exclusive rather than complementary. Gap 10 is also ripe, given the growing empirical evidence for LLM phase transitions and the well-developed theory of confluent singularities.

### Conclusion

The intersection of Flajolet–Sedgewick analytic combinatorics and large language model analysis appears to us to be a largely unexplored research territory. The closest related works operate on one side of the divide: either analyzing formal languages with GF methods, or analyzing LLMs with non-GF methods. The mathematical tools on each side are mature. What is missing is the construction of explicit bridges, beginning with the foundational step of defining and computing generating functions for LLM output distributions — choosing the *right* generating function for the question being asked — in a form amenable to singularity analysis.

---

### References for Literature Gaps (Expanded)

**Gap 1 — PGF construction**
- Zhang, K., Wang, Q. & Giles, C.L. (2021). "An Entropy Metric for Regular Grammar Classification and Learning with Recurrent Neural Networks." *Entropy*, 23(1), 127. [mdpi.com/1099-4300/23/1/127](https://www.mdpi.com/1099-4300/23/1/127)
- Lau, E. et al. (2023). "The Local Learning Coefficient: A Singularity-Aware Complexity Measure." [arXiv:2308.12108](https://arxiv.org/abs/2308.12108)
- Flajolet, P. (2003). "Singular Combinatorics." [arXiv:math/0304465](https://arxiv.org/abs/math/0304465)
- Bousquet-Mélou, M. (2006). "Rational and Algebraic Series in Combinatorial Enumeration." [arXiv:1102.1779](https://arxiv.org/abs/1102.1779) (referenced for singularity types by formal language class, including natural boundaries for indexed grammars)

**Gap 2 — Entropy rate $= \log(1/R)$**
- Takahashi, S. & Tanaka-Ishii, K. (2018). "Cross Entropy of Neural Language Models at Infinity — A New Bound of the Entropy Rate." *Entropy*, 20(11), 839. [researchgate.net/publication/328739594](https://www.researchgate.net/publication/328739594)
- Braverman, M. et al. (2019). "Calibration, Entropy Rates, and Memory in Language Models." [arXiv:1906.05664](https://arxiv.org/abs/1906.05664)
- Han, G. & Marcus, B. (2006). "Analyticity of Entropy Rate of Hidden Markov Chains." [arXiv:math/0507235](https://arxiv.org/abs/math/0507235)

**Gap 3 — Boltzmann sampling ↔ LLM temperature**
- Duchon, P., Flajolet, P., Louchard, G. & Schaeffer, G. (2004). "Boltzmann Samplers for the Random Generation of Combinatorial Structures." *Combinatorics, Probability and Computing* 13:577–625. [informs-sim.org/wsc11papers/011.pdf](https://www.informs-sim.org/wsc11papers/011.pdf)
- Yang, Z. (2024). "Entropy Function, Partition Function, Geometrization and Boltzmann Manifold of Language Models." [arXiv:2407.21092](https://arxiv.org/abs/2407.21092)
- Bodini, O. & Ponty, Y. (2010). "Multi-dimensional Boltzmann Sampling of Languages." *DMTCS Proceedings* (AofA'10). [arXiv:1002.0046](https://arxiv.org/abs/1002.0046)

**Gap 4 — Multivariate ACSV for token distributions**
- Pemantle, R., Wilson, M.C. & Melczer, S. (2024). *Analytic Combinatorics in Several Variables* (2nd ed.). Cambridge University Press. [cambridge.org](https://www.cambridge.org/core/books/analytic-combinatorics-in-several-variables/634B6B5753C341C0A848077912E9612D)
- Pemantle, R. & Wilson, M.C. (2005). "Twenty Combinatorial Examples of Asymptotics Derived from Multivariate Generating Functions." [arXiv:math/0512548](https://arxiv.org/abs/math/0512548)
- Lenz, A., Melczer, S., Rashtchian, C. & Siegel, P.H. (2025). "Multivariate Analytic Combinatorics for Cost Constrained Channels." *IEEE Trans. Information Theory* 71(11):8223. [arXiv:2111.06105](https://arxiv.org/abs/2111.06105)

**Gap 5 — Chomsky–Schützenberger algebraic GF for LLMs**
- Banderier, C. & Drmota, M. (2015). "Formulae and Asymptotics for Coefficients of Algebraic Functions." *Combinatorics, Probability and Computing* 24(1):1–53. [cambridge.org](https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/abs/formulae-and-asymptotics-for-coefficients-of-algebraic-functions/873FE8063D1BA21058EA82A9F33D659F)
- Allen-Zhu, Z. & Li, Y. (2023). "Physics of Language Models: Part 1, Context-Free Grammar." [arXiv:2305.13673](https://arxiv.org/abs/2305.13673)
- Delétang, G. et al. (2023). "Neural Networks and the Chomsky Hierarchy." ICLR 2023. [arXiv:2207.02098](https://arxiv.org/abs/2207.02098)
- Strobl, L., Merrill, W., Weiss, G., Chiang, D. & Angluin, D. (2024). "What Formal Languages Can Transformers Express? A Survey." *TACL* 12:543–561. [MIT Press](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00663/120983)

**Gap 6 — Limit laws via analytic combinatorics**
- Hwang, H.-K. (1998). "On the Higher Dimensional Quasi-Power Theorem and a Berry-Esseen Inequality." [researchgate.net/publication/301848742](https://www.researchgate.net/publication/301848742)

**Gap 7 — Thermodynamic formalism + GF analysis**
- Kempton, T. & Burrell, S. (2025). "Local Normalization Distortion and the Thermodynamic Formalism of Decoding Strategies for Large Language Models." EMNLP 2025 Findings. [arXiv:2503.21929](https://arxiv.org/abs/2503.21929)
- Kempton, T., Burrell, S. & Cheverall, C. (2025). "TempTest: Local Normalization Distortion and the Detection of Machine-Generated Text." AISTATS 2025. [arXiv:2503.20421](https://arxiv.org/abs/2503.20421)

**Gap 8 — Singularity type classification**
- Lin, H.W. & Tegmark, M. (2017). "Criticality in Formal Languages and Statistical Physics." [arXiv:1606.06737](https://arxiv.org/abs/1606.06737)

**Gap 9 — WFA → rational GF pipeline**
- Suresh, A.T., Roark, B., Riley, M. & Schogol, V. (2021). "Approximating Probabilistic Models as Weighted Finite Automata." *Computational Linguistics* 47(2):221–254. [MIT Press](https://direct.mit.edu/coli/article/47/2/221/98517)
- Okudono, T., Waga, M., Sekiyama, T. & Hasuo, I. (2020). "Weighted Automata Extraction from Recurrent Neural Networks via Regression on State Spaces." AAAI 2020. [arXiv:1904.02931](https://arxiv.org/abs/1904.02931)
- Svete, A. & Cotterell, R. (2023). "Recurrent Neural Language Models as Probabilistic Finite-state Automata." EMNLP 2023. [ACL Anthology](https://aclanthology.org/2023.emnlp-main.502.pdf)

**Gap 10 — Phase transitions as confluent singularities**
- Nakaishi, K., Nishikawa, Y. & Hukushima, K. (2024). "Critical Phase Transition in Large Language Models." [arXiv:2406.05335](https://arxiv.org/abs/2406.05335)
- Bölte et al. (2024). "Phase Transitions in the Output Distribution of Large Language Models." [arXiv:2405.17088](https://arxiv.org/abs/2405.17088) / [OpenReview](https://openreview.net/pdf?id=dq3keisMjT)
- Mikhaylovskiy, N. (2025). "States of LLM-generated Texts and Phase Transitions between them." [arXiv:2503.06330](https://arxiv.org/abs/2503.06330)
- Li, J. et al. (2025). "Phase Transitions in Large Language Models and the O(N) Model." [arXiv:2501.16241](https://arxiv.org/abs/2501.16241)
- Banderier, C., Kuba, M. & Wallner, M. (2021). "Phase Transitions of Composition Schemes: Mittag-Leffler and Mixed Poisson Distributions." [arXiv:2103.03751](https://arxiv.org/abs/2103.03751)
