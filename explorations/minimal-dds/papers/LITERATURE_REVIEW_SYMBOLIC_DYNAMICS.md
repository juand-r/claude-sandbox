# Literature Review: Symbolic Dynamics, Tag Systems, IFS, and Related Dynamical Systems

This review covers foundational and key works on symbolic dynamics, tag systems, substitution systems, iterated function systems on discrete spaces, and cellular automata as dynamical systems. For each entry: full citation, summary, availability, and relevance to iterating maps on (function, input) pairs, self-modifying systems, and LLM output fed back as input.

---

## 1. Post Tag Systems

### 1.1 Post — Formal Reductions of the General Combinatorial Decision Problem (1943)

**Citation:** Emil L. Post. "Formal Reductions of the General Combinatorial Decision Problem." *American Journal of Mathematics*, 65(2):197--215, 1943.

**Summary:** Post introduced tag systems -- deterministic string-rewriting systems where at each step, a fixed number of symbols are deleted from the front of a string and a block of symbols (determined by the first symbol read) is appended to the end. He proved the Normal-form Theorem: any Post canonical system can be converted to normal form (possibly enlarging the alphabet) while generating the same set of words. He conjectured these systems were computationally universal but could not prove it, calling this his "major unsolved problem."

**Availability:** PDF at [lib.ysu.am](https://lib.ysu.am/articles_art/63062f3ed126193beb426becc0fbbe33.pdf). Also indexed on [Semantic Scholar](https://www.semanticscholar.org/paper/Formal-Reductions-of-the-General-Combinatorial-Post/6fd197ec4e9495c1940c4c1023d56e721aa00944).

**Relevance:** Tag systems are the simplest known class of string-rewriting systems that achieve Turing completeness. The tag operation -- delete from front, append to back based on a lookup table -- is a minimal model of "read current state, produce new state via a fixed map." This is a concrete (table, string) -> (table, string') system where the table is fixed. The key insight for self-modifying systems: if the table itself were encoded in the string, you would have a self-modifying tag system.

---

### 1.2 Minsky — Recursive Unsolvability of Post's Problem of "Tag" (1961)

**Citation:** Marvin L. Minsky. "Recursive Unsolvability of Post's Problem of 'Tag' and Other Topics in Theory of Turing Machines." *Annals of Mathematics*, second series, 74(3):437--455, 1961.

**Summary:** Minsky proved Post's conjecture by constructing a method to translate any Turing machine into a tag system, thereby showing tag systems are Turing-complete. Specifically, he showed that one-element-dependence tag systems can simulate arbitrary Turing machines, which implies the halting problem for tag systems is undecidable. This resolved a question Post had struggled with for decades.

**Availability:** PDF at [wolframscience.com](https://www.wolframscience.com/prizes/tm23/images/Minsky.pdf). Also on [Semantic Scholar](https://www.semanticscholar.org/paper/Recursive-Unsolvability-of-Post's-Problem-of-%22Tag%22-Minsky/28d9dbee97eba9f11a87edf3b44fabb4a8db082e).

**Relevance:** Establishes that even the simplest string-rewriting systems (delete from front, append based on a lookup) can perform arbitrary computation. For the (f, x) framework: a tag system with a fixed rule table f and string x can simulate any computable trajectory. This means the orbit structure of even "simple" discrete dynamical systems on strings is undecidable in general.

---

### 1.3 Cocke & Minsky — Universality of Tag Systems with P = 2 (1964)

**Citation:** John Cocke and Marvin Minsky. "Universality of Tag Systems with P = 2." *Journal of the ACM*, 11(1):15--20, 1964.

**Summary:** Strengthened Minsky's 1961 result by showing that tag systems with deletion number P=2 (the minimum possible for non-trivial behavior) are already Turing-complete. The proof is a direct, relatively simple construction that simulates arbitrary Turing machines. The representation has a lower degree of exponentiation than Minsky's original proof.

**Availability:** [ACM Digital Library](https://dl.acm.org/doi/10.1145/321203.321206). Preprint at [MIT DSpace](https://dspace.mit.edu/handle/1721.1/6107).

**Relevance:** Shows that universality appears at the absolute minimum threshold of tag system complexity. This is a recurring theme: computation universality is more common than expected. For LLM feedback loops, the analogy is that even very constrained rewriting rules on token sequences can in principle encode arbitrary computation.

---

### 1.4 De Mol — Tag Systems and Collatz-like Functions (2008)

**Citation:** Liesbeth De Mol. "Tag systems and Collatz-like functions." *Theoretical Computer Science*, 390(1):92--101, 2008.

**Summary:** Reduces the Collatz 3n+1 problem to a surprisingly small tag system, demonstrating that the boundary between decidable and undecidable tag systems may be much lower than previously thought. Shows that the halting problem for Turing machines can be reformulated as a question about the iteration of Collatz-like functions, and that these functions arise naturally from tag system dynamics.

**Availability:** [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0304397507007700). Also on [Semantic Scholar](https://www.semanticscholar.org/paper/Tag-systems-and-Collatz-like-functions-Mol/931eeecbcb5a55f31e9aec6c6a628fd348b435c4).

**Relevance:** Connects tag system dynamics to number-theoretic iteration (Collatz-like functions). This bridge between string rewriting and arithmetic iteration is significant: it shows that iterated maps on integers and iterated maps on strings are deeply related. For the (f, x) framework, this means that even integer-valued iterative maps can encode undecidable behavior.

---

### 1.5 De Mol — Study of Limits of Solvability in Tag Systems (2007)

**Citation:** Liesbeth De Mol. "Study of Limits of Solvability in Tag Systems." In *Machines, Computations, and Universality (MCU 2007)*, Lecture Notes in Computer Science, vol. 4664, pp. 170--181. Springer, 2007.

**Summary:** Maps the boundary between decidable and undecidable tag systems in terms of two parameters: the shift number v (deletion number) and the number of symbols mu. Contributes to the program of understanding exactly where universality kicks in for tag systems.

**Availability:** [Springer](https://link.springer.com/chapter/10.1007/978-3-540-74593-8_15). Preprint PDF at [clps.ugent.be](https://www.clps.ugent.be/sites/default/files/publications/MCU07_r.pdf).

**Relevance:** Understanding the exact complexity threshold for universality in rewriting systems informs the question of how complex a self-modifying system needs to be before its behavior becomes undecidable.

---

### 1.6 De Mol — Tracing Unsolvability (PhD Thesis, 2007)

**Citation:** Liesbeth De Mol. *Tracing Unsolvability: A Historical, Mathematical and Philosophical Analysis with a Special Focus on Tag Systems*. PhD thesis, Universiteit Gent, 2007.

**Summary:** Comprehensive historical and mathematical analysis of tag systems, tracing the development from Post's original work through Minsky's universality proof, with philosophical reflections on the nature of unsolvability.

**Availability:** Institutional repository (Universiteit Gent).

**Relevance:** The most thorough single treatment of tag systems as a topic, useful as a secondary source and historical reference.

---

## 2. Symbolic Dynamics — Foundations

### 2.1 Morse & Hedlund — Symbolic Dynamics (1938)

**Citation:** Marston Morse and Gustav A. Hedlund. "Symbolic Dynamics." *American Journal of Mathematics*, 60(4):815--866, 1938.

**Summary:** The founding paper of symbolic dynamics as a field. Introduces the technique of coding continuous dynamical system trajectories as sequences of symbols from a finite alphabet. Proves the Morse-Hedlund theorem: every aperiodic infinite word over a finite alphabet contains at least n+1 distinct factors of each length n. Establishes the shift map on bi-infinite sequences as a fundamental dynamical system.

**Availability:** JSTOR (institutional access). Not freely available online.

**Relevance:** The core framework. Symbolic dynamics encodes the orbit of a dynamical system as a sequence over a finite alphabet. When we iterate an LLM on its own output, the resulting sequence of token strings is exactly a trajectory in a symbolic dynamical system -- though over an enormous alphabet and with a very complex (and stochastic) transition rule.

---

### 2.2 Morse & Hedlund — Symbolic Dynamics II: Sturmian Trajectories (1940)

**Citation:** Marston Morse and Gustav A. Hedlund. "Symbolic Dynamics II. Sturmian Trajectories." *American Journal of Mathematics*, 62(1):1--42, 1940.

**Summary:** Studies sequences of minimal complexity (exactly n+1 factors of each length n), now called Sturmian sequences. Shows these arise from irrational rotations on the circle, connecting symbolic dynamics to number theory and Diophantine approximation.

**Availability:** JSTOR (institutional access).

**Relevance:** Sturmian sequences are the simplest non-periodic symbolic sequences. They represent the boundary between periodic (predictable) and complex (unpredictable) behavior -- a useful reference point for understanding what kinds of orbits a discrete iterated system can produce.

---

### 2.3 Lind & Marcus — An Introduction to Symbolic Dynamics and Coding (1995, 2nd ed. 2021)

**Citation:** Douglas Lind and Brian Marcus. *An Introduction to Symbolic Dynamics and Coding*. Cambridge University Press, 1995. Second edition, 2021.

**Summary:** The standard textbook on symbolic dynamics. Covers shift spaces, shifts of finite type (SFTs), sofic shifts, entropy via Perron-Frobenius theory, finite-state codes (sliding block codes), conjugacy, finite equivalence, almost conjugacy, embeddings, and factor codes. Over 500 exercises. The second edition adds new material on advanced topics.

**Key concepts covered:**
- **Shift of finite type (SFT):** A shift space defined by forbidding a finite set of words. Equivalent to the set of bi-infinite walks on a directed graph. The transition matrix encodes all dynamics.
- **Sofic shift:** The image of an SFT under a sliding block code. Equivalently, the set of labels on bi-infinite walks on a labeled directed graph. Strictly more general than SFTs.
- **Entropy:** For an SFT with adjacency matrix A, the topological entropy is log(lambda), where lambda is the largest eigenvalue of A (Perron-Frobenius). Entropy is a complete invariant for finite equivalence of irreducible SFTs.
- **Sliding block codes:** Maps between shift spaces defined by a local rule applied uniformly. The Curtis-Hedlund-Lyndon theorem says these are exactly the continuous shift-commuting maps.

**Availability:** Cambridge University Press (book, not freely available). Table of contents and frontmatter at [CUP](https://assets.cambridge.org/97811088/20288/frontmatter/9781108820288_frontmatter.pdf).

**Relevance:** Provides the mathematical toolkit for analyzing any discrete-time, finite-alphabet dynamical system. The classification of shift spaces (SFT, sofic, general) gives a hierarchy of complexity for the symbolic dynamics of iterated maps. LLM output iteration, if the vocabulary is finite, falls into this framework -- but the transition rule is far too complex for direct analysis with these tools. The concepts (entropy, forbidden words, conjugacy) are nonetheless the right vocabulary for describing the dynamics.

---

### 2.4 Bowen — Markov Partitions for Axiom A Diffeomorphisms (1970)

**Citation:** Rufus Bowen. "Markov Partitions for Axiom A Diffeomorphisms." *American Journal of Mathematics*, 92:725--747, 1970.

**Summary:** Extended Sinai's construction of Markov partitions from Anosov systems to the broader class of Axiom A diffeomorphisms. This allows the coding of orbits by symbolic sequences constrained by a transition matrix -- a shift of finite type. Connecting smooth dynamics to symbolic dynamics via Markov partitions became one of the central tools of ergodic theory.

**Availability:** JSTOR (institutional access). Indexed on [Semantic Scholar](https://www.semanticscholar.org/paper/MARKOV-PARTITIONS-FOR-AXIOM-A-DIFFEOMORPHISMS.-Bowen/d70389a6bbaccfe79757a9f56639197ca59d600a).

**Relevance:** The prototype for using symbolic dynamics (SFTs) as a model for complicated continuous dynamics. The idea of encoding a complex system's orbits as sequences over a finite alphabet, constrained by a graph, is the same idea behind modeling LLM iteration as a shift space -- though the "Markov partition" for an LLM would be unimaginably large.

---

### 2.5 Bowen — Equilibrium States and the Ergodic Theory of Anosov Diffeomorphisms (1975)

**Citation:** Rufus Bowen. *Equilibrium States and the Ergodic Theory of Anosov Diffeomorphisms*. Lecture Notes in Mathematics, vol. 470. Springer, 1975. Second revised edition (ed. J.-R. Chazottes), 2008.

**Summary:** Classic monograph connecting symbolic dynamics, thermodynamic formalism, and hyperbolic dynamics. Introduces SRB (Sinai-Ruelle-Bowen) measures and proves the variational principle for entropy. The bridge between statistical mechanics and dynamical systems.

**Availability:** PDF at [polytechnique.fr](https://www.cpht.polytechnique.fr/sites/default/files/Bowen_LN_Math_470_second_ed_v2013.pdf). Springer (book).

**Relevance:** The thermodynamic formalism (pressure, equilibrium states, variational principle) provides tools for studying the statistical behavior of symbolic dynamical systems. If one models iterated LLM output as a symbolic system, these tools could in principle characterize the "equilibrium" or typical behavior.

---

## 3. Sliding Block Codes and the Curtis-Hedlund-Lyndon Theorem

### 3.1 Hedlund — Endomorphisms and Automorphisms of the Shift Dynamical System (1969)

**Citation:** Gustav A. Hedlund. "Endomorphisms and Automorphisms of the Shift Dynamical System." *Mathematical Systems Theory*, 3:320--375, 1969.

**Summary:** The foundational paper for the algebraic and topological study of shift spaces. Proves the Curtis-Hedlund-Lyndon theorem: a map between shift spaces is continuous and shift-commuting if and only if it is a sliding block code (i.e., defined by a local rule applied uniformly via a finite window). Establishes that endomorphisms of the full shift form a monoid whose structure is deeply connected to cellular automata theory. Studies invertibility, showing that reversible cellular automata are exactly automorphisms of the shift.

**Availability:** [Springer](https://link.springer.com/article/10.1007/BF01691062) (institutional access). Over 1,100 citations.

**Relevance:** The Curtis-Hedlund-Lyndon theorem is the fundamental structure theorem for morphisms of symbolic dynamical systems. It says: any "nice" (continuous, shift-equivariant) transformation of infinite sequences must be local -- determined by a finite window. This is the symbolic dynamics analogue of saying that any well-behaved rule for transforming an infinite string can only look at a bounded neighborhood. For self-modifying systems, the key question is whether the map (f, x) -> (f', x') can be expressed as a sliding block code, or whether it requires non-local operations.

---

### 3.2 Sobottka & Goncalves — A Note on the Definition of Sliding Block Codes and the Curtis-Hedlund-Lyndon Theorem (2017)

**Citation:** Marcelo Sobottka and Daniel Goncalves. "A note on the definition of sliding block codes and the Curtis-Hedlund-Lyndon Theorem." *Journal of Cellular Automata*, 12(3-4):209--215, 2017. arXiv:1507.02180.

**Summary:** Proposes a refined definition of sliding block codes for shift spaces over countable (possibly infinite) alphabets, under which the Curtis-Hedlund-Lyndon theorem always holds. The classical theorem fails for infinite alphabets under the standard definition because continuous shift-commuting maps may not be locally determined.

**Availability:** [arXiv:1507.02180](https://arxiv.org/abs/1507.02180).

**Relevance:** When modeling LLM token sequences, the effective vocabulary can be very large. This paper addresses exactly the subtlety of whether the Curtis-Hedlund-Lyndon theorem extends to large/infinite alphabets -- it does, under the right definition.

---

## 4. Iterated Function Systems (IFS) on Discrete/Finite State Spaces

### 4.1 Hutchinson — Fractals and Self-Similarity (1981)

**Citation:** John E. Hutchinson. "Fractals and Self Similarity." *Indiana University Mathematics Journal*, 30(5):713--747, 1981.

**Summary:** The foundational paper for iterated function systems. Proves that a finite set of contraction mappings on a complete metric space has a unique compact invariant set (the "attractor") and a unique invariant probability measure. Introduces the Hutchinson operator on the space of compact sets and shows it is itself a contraction under the Hausdorff metric.

**Availability:** PDF at [ANU](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf).

**Relevance:** The IFS framework -- iterate a collection of maps, study the attractor -- is a natural generalization of iterating a single map. For discrete state spaces, the attractor of an IFS is a subset that is invariant under all the maps. The connection to (f, x) iteration: if at each step the "map" is chosen from a finite set (as in a stochastic process or a tag system with multiple rules), this is an IFS. The Hutchinson operator on the power set is a higher-order dynamical system.

---

### 4.2 Barnsley & Demko — Iterated Function Systems and the Global Construction of Fractals (1985)

**Citation:** Michael F. Barnsley and Stephen Demko. "Iterated Function Systems and the Global Construction of Fractals." *Proceedings of the Royal Society of London, Series A*, 399(1817):243--275, 1985.

**Summary:** Introduced the term "iterated function system" (IFS) and the random iteration algorithm (chaos game). Proved existence and uniqueness of p-balanced measures for hyperbolic IFS. Estimated Hausdorff dimension of attractors. Developed moment theory for linear IFS and probabilistic mixtures.

**Availability:** [Royal Society](https://royalsocietypublishing.org/doi/10.1098/rspa.1985.0057). [JSTOR](https://www.jstor.org/stable/2397690).

**Relevance:** The random iteration algorithm is directly relevant: instead of applying all maps to a set, apply one randomly chosen map at each step. The orbit of a single point under random IFS is a Markov chain whose stationary distribution is the invariant measure. This is analogous to stochastic token generation: at each step, one of many possible continuations is chosen, and the long-run distribution over states is the invariant measure of the corresponding IFS.

---

### 4.3 Barnsley — Fractals Everywhere (1988, 2nd ed. 1993)

**Citation:** Michael F. Barnsley. *Fractals Everywhere*. Academic Press, 1988. Second edition, 1993.

**Summary:** The standard textbook on fractal geometry via IFS. Covers metric spaces, contraction mappings, the Hausdorff metric, IFS attractors, the collage theorem (inverse problem: given a target set, find an IFS whose attractor approximates it), fractal interpolation, Julia sets, and the Mandelbrot set. Based on a graduate course at Georgia Tech.

**Availability:** PDF at [lib.ysu.am](http://lib.ysu.am/open_books/418197.pdf). Also [ScienceDirect](https://www.sciencedirect.com/book/9780120790616/fractals-everywhere).

**Relevance:** Textbook treatment of IFS theory. The collage theorem is particularly relevant: it addresses the inverse problem of "given a desired attractor (behavior), find the maps that produce it." For self-modifying systems, this is analogous to asking: what set of local rules would produce a desired global behavior?

---

### 4.4 Barnsley, Elton & Hardin — Recurrent Iterated Function Systems (1989)

**Citation:** Michael F. Barnsley, John H. Elton, and Douglas P. Hardin. "Recurrent Iterated Function Systems." *Constructive Approximation*, 5:3--31, 1989.

**Summary:** Generalizes IFS by allowing the choice of map at each step to depend on the previous map chosen (Markov chain on the maps). Under "average contractivity," proves convergence and ergodic theorems. Extends fractal interpolation theory and derives fractal dimensions for recurrent IFS attractors.

**Availability:** [Springer](https://link.springer.com/article/10.1007/BF01889596).

**Relevance:** Recurrent IFS = IFS driven by a Markov chain. The "state" is (current map index, current point), and the transition depends on both. This is closer to a self-modifying system: the choice of which transformation to apply next depends on which was applied last. The (function-index, state) pair evolves jointly.

---

### 4.5 Ghosh & Marecek — Iterated Function Systems: A Comprehensive Survey (2022)

**Citation:** Ramen Ghosh and Jakub Marecek. "Iterated Function Systems: A Comprehensive Survey." arXiv:2211.14661, 2022.

**Summary:** A broad survey covering the Hutchinson-Barnsley theory, random IFS, recurrent IFS, IFS on non-metric spaces, IFS of non-contractive maps, and recent developments including IFS dynamics formulated as continuous-time systems.

**Availability:** [arXiv:2211.14661](https://arxiv.org/pdf/2211.14661).

**Relevance:** Good overview of the state of IFS theory. Notes the connection between IFS and discrete dynamical systems, and the recent interest in IFS on non-standard spaces (including discrete spaces).

---

### 4.6 Martyn — The Discrete Charm of Iterated Function Systems (2024)

**Citation:** Tomasz Martyn. "The discrete charm of iterated function systems: A computer scientist's perspective on approximation of IFS invariant sets and measures." arXiv:2410.15139, 2024.

**Summary:** Studies IFS defined directly on countable discrete spaces (uniform grids), not as discretizations of continuous IFS but as mathematical objects in their own right. Investigates whether the random iteration algorithm (chaos game) can approximate invariant sets and measures of discrete IFS. These discrete spaces model the spaces in which actual numerical computation takes place.

**Availability:** [arXiv:2410.15139](https://arxiv.org/abs/2410.15139).

**Relevance:** Directly relevant to the question of IFS on finite/discrete state spaces. This is the setting closest to what we care about: maps on finite sets, iterated according to some rule, with the question of what the invariant structures are. The "computer scientist's perspective" is apt -- we are interested in dynamics on finite, discrete objects (strings, programs, token sequences).

---

## 5. Substitution Systems, Morphisms on Words, and Automatic Sequences

### 5.1 Cobham — Uniform Tag Sequences (1972)

**Citation:** Alan Cobham. "Uniform tag sequences." *Mathematical Systems Theory*, 6:164--192, 1972.

**Summary:** Proves that a sequence is k-automatic (computable by a finite automaton reading the base-k expansion of n) if and only if it is the image under a letter-to-letter morphism of the fixed point of a k-uniform morphism (a morphism where every letter maps to a word of length k). This foundational equivalence connects automata theory to the dynamics of iterated morphisms.

**Cobham's theorem on multiplicative independence:** If a sequence is both k-automatic and l-automatic for multiplicatively independent k, l, then it is eventually periodic. This is a deep rigidity result: the base of the numeration system is an essential parameter.

**Availability:** Springer (institutional access).

**Relevance:** Automatic sequences are the fixed points of iterated uniform morphisms -- they are exactly the attractors of a specific class of substitution dynamical systems. The connection to automata means these sequences can be "read off" by a finite-state machine, making them the simplest class of non-trivial substitution-generated objects. For the (f, x) framework, this says: if f is a uniform morphism and we iterate f on a seed, the result (at the limit) is characterized by finite automata.

---

### 5.2 Allouche & Shallit — Automatic Sequences: Theory, Applications, Generalizations (2003)

**Citation:** Jean-Paul Allouche and Jeffrey Shallit. *Automatic Sequences: Theory, Applications, Generalizations*. Cambridge University Press, 2003.

**Summary:** The definitive textbook on automatic sequences. Covers: numeration systems, finite automata, k-automatic sequences, uniform morphisms and their fixed points, the Cobham equivalence, morphic sequences (fixed points of arbitrary morphisms composed with a coding), Christol's theorem (connecting automatic sequences to formal power series over finite fields), k-regular sequences, and numerous applications to number theory, combinatorics, and physics. 460 exercises, 85 open problems, 1600+ references.

**Key concepts:**
- **k-uniform morphism:** sigma(a) has length k for all letters a. Iteration produces words of length k^n.
- **Morphic sequence:** the image under a coding of the fixed point of any morphism (not necessarily uniform). Strictly more general than automatic sequences.
- **Cobham's theorem:** k-automatic + l-automatic (k, l multiplicatively independent) implies eventually periodic.
- **Christol's theorem:** A formal power series over F_q is algebraic over F_q(X) iff its coefficient sequence is q-automatic.

**Availability:** Cambridge University Press (book, not freely available). Full PDF at [lib.ysu.am](http://lib.ysu.am/disciplines_bk/47fe303913ad333b6dea08e0ba2a9fbb.pdf). Author's page at [cs.uwaterloo.ca](https://cs.uwaterloo.ca/~shallit/asas.html).

**Relevance:** Morphic sequences are fixed points of iterated morphisms -- they are the "attractors" of word-level dynamical systems. The hierarchy (k-automatic < morphic < arbitrary) mirrors the hierarchy of complexity in symbolic dynamics (SFT < sofic < general shift). For LLM iteration, the question is: does iterated LLM output converge to something morphic? The attractor cycle results (see Section 7.1 below) suggest it converges to something much simpler -- periodic.

---

### 5.3 Queffelec — Substitution Dynamical Systems: Spectral Analysis (1987, 2nd ed. 2010)

**Citation:** Martine Queffelec. *Substitution Dynamical Systems -- Spectral Analysis*. Lecture Notes in Mathematics, vol. 1294. Springer, 1987. Second edition, 2010.

**Summary:** Studies the dynamical systems obtained by taking the orbit closure of a substitution fixed point under the shift. Analyzes the spectral properties (eigenvalues, spectral measures) of these systems using tools from ergodic theory and harmonic analysis. Covers connections to number theory and aperiodic tilings.

**Availability:** Springer (book, institutional access).

**Relevance:** The spectral analysis of substitution dynamical systems gives invariants that distinguish different types of long-range order. Pure point spectrum corresponds to quasiperiodic behavior (like quasicrystals), while continuous spectrum corresponds to more "random" behavior. This classification could in principle be applied to characterize the dynamics of iterated LLM output.

---

### 5.4 Durand — A Generalization of Cobham's Theorem (1998)

**Citation:** Fabien Durand. "A generalization of Cobham's theorem." *Theory of Computing Systems*, 31:169--185, 1998.

**Summary:** Generalizes Cobham's theorem from automatic sequences to primitive substitutive sequences: if a sequence is both alpha-substitutive and beta-substitutive for multiplicatively independent Perron numbers alpha, beta, then it is ultimately periodic.

**Availability:** Springer (institutional access).

**Relevance:** Extends the rigidity result: the dynamics of iterated morphisms are strongly constrained by the growth rate of the morphism. Two morphisms with incommensurate growth rates cannot produce the same non-periodic sequence. This rigidity contrasts with the flexibility of general (f, x) systems.

---

### 5.5 Durand — Cobham's Theorem for Substitutions (2011)

**Citation:** Fabien Durand. "Cobham's theorem for substitutions." *Journal of the European Mathematical Society*, 13:1799--1814, 2011.

**Summary:** Further extends Cobham's theorem to the case of non-primitive substitutions, completing the generalization program.

**Availability:** [EMS](https://ems.press/journals/jems/articles/1655).

**Relevance:** Completes the picture for substitution-generated sequences, showing the multiplicative independence barrier is fundamental.

---

## 6. Cellular Automata as Dynamical Systems

### 6.1 Wolfram — Universality and Complexity in Cellular Automata (1984)

**Citation:** Stephen Wolfram. "Universality and complexity in cellular automata." *Physica D: Nonlinear Phenomena*, 10(1--2):1--35, 1984.

**Summary:** Based on systematic computational experiments, proposes that all one-dimensional cellular automata fall into four universality classes: (1) evolution to a homogeneous state; (2) evolution to periodic/oscillating structures; (3) evolution to chaotic behavior; (4) complex localized structures capable of universal computation. Introduces entropy and dimension measures to characterize CA evolution. Conjectures that Class 4 CAs (like Rule 110) are computationally universal.

**Availability:** PDF at [content.wolfram.com](https://content.wolfram.com/sw-publications/2020/07/universality-complexity-cellular-automata.pdf). Also [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0167278984902458).

**Relevance:** Wolfram's four classes are an empirical classification of the dynamics of iterated local rules on strings. Class 4 -- complex behavior at the "edge of chaos" -- is where universal computation emerges. The question for LLM iteration: which class does it fall into? The attractor cycle evidence (Section 7) suggests Class 2 (periodic), but with more sophisticated prompting strategies, Class 4 behavior might be accessible.

---

### 6.2 Wolfram — A New Kind of Science (2002)

**Citation:** Stephen Wolfram. *A New Kind of Science*. Wolfram Media, 2002.

**Summary:** Massive (1200+ page) work expanding on the 1984 paper's themes. Catalogs behavior of simple programs across many computational models (CAs, tag systems, Turing machines, substitution systems). Central thesis: simple rules can produce complex behavior, and computation universality is ubiquitous. Contains Cook's proof outline that Rule 110 is Turing-complete (via emulation of cyclic tag systems).

**Availability:** Full text at [wolframscience.com/nks](https://www.wolframscience.com/nks/).

**Relevance:** The most comprehensive catalog of simple iterated systems and their behavior. Directly relevant as a reference for the behavior of tag systems, substitution systems, and cellular automata. The "principle of computational equivalence" -- that most systems capable of non-trivial behavior are computationally universal -- is a strong (if controversial) claim about the dynamics of iterated maps.

---

### 6.3 Cook — Universality in Elementary Cellular Automata (2004)

**Citation:** Matthew Cook. "Universality in Elementary Cellular Automata." *Complex Systems*, 15(1):1--40, 2004.

**Summary:** Rigorous proof that Rule 110 (an elementary CA with 2 states and nearest-neighbor interaction) is Turing-complete. The proof works by constructing glider-like structures within Rule 110 that simulate cyclic tag systems (which simulate 2-tag systems, which simulate Turing machines). Establishes universality at the simplest possible scale for CAs.

**Availability:** PDF at [content.wolfram.com](https://content.wolfram.com/sites/13/2023/02/15-1-1.pdf). Also at [mirror.explodie.org](https://mirror.explodie.org/universality_in_elementary_cellular_automata_by_matthew_cook.pdf).

**Relevance:** Demonstrates the chain: Rule 110 CA -> cyclic tag system -> 2-tag system -> Turing machine. This chain of reductions is a template for showing that simple iterated systems are universal. For the (f, x) framework, it shows that even the simplest local rules, when iterated, can perform arbitrary computation.

---

### 6.4 Kurka — Languages, Equicontinuity and Attractors in Cellular Automata (1997)

**Citation:** Petr Kurka. "Languages, equicontinuity and attractors in cellular automata." *Ergodic Theory and Dynamical Systems*, 17:417--433, 1997.

**Summary:** Proposes a rigorous topological classification of cellular automata based on two orthogonal criteria: (E) equicontinuity classes and (L) language complexity classes. The E-classification: E1 (equicontinuous), E2 (almost equicontinuous but not equicontinuous), E3 (sensitive but not positively expansive), E4 (positively expansive). The L-classification: L1 (bounded periodic language), L2 (regular but not bounded periodic), L3 (not regular). Proves E1 = L1.

**Availability:** Cambridge University Press (institutional access). Also at [cts.cuni.cz](https://www.cts.cuni.cz/~kurka/cantor.pdf).

**Relevance:** Provides a mathematically rigorous alternative to Wolfram's empirical 4-class scheme. Equicontinuity measures sensitivity to initial conditions; language complexity measures the richness of patterns the CA can generate. This classification applies to any shift-commuting continuous map, so it could in principle be applied to characterize the dynamics of iterated transformations on strings.

---

### 6.5 Kurka — Topological and Symbolic Dynamics (2003)

**Citation:** Petr Kurka. *Topological and Symbolic Dynamics*. Cours specialises, vol. 11. Societe Mathematique de France, Paris, 2003.

**Summary:** Comprehensive monograph covering topological dynamics of continuous self-maps of compact metric spaces, with particular focus on cellular automata and symbolic dynamics. Covers equicontinuity, topological entropy, Markov subshifts, sofic subshifts, Sturmian subshifts, Toeplitz subshifts, and positively expansive systems. Unifies the symbolic dynamics and topological dynamics perspectives on CA.

**Availability:** SMF (book). Indexed on [Semantic Scholar](https://www.semanticscholar.org/paper/Topological-and-symbolic-dynamics-Kurka/f0f7e1972a0e25310ce6e9a5d1534a7904421a8f).

**Relevance:** The most thorough treatment of cellular automata from the topological dynamics perspective. Essential reference for the theory connecting CAs to symbolic dynamics.

---

## 7. LLM Output-to-Input Iteration as a Dynamical System

### 7.1 Anonymous (arXiv, Feb 2025) — Unveiling Attractor Cycles in Large Language Models: A Dynamical Systems View of Successive Paraphrasing

**Citation:** "Unveiling Attractor Cycles in Large Language Models: A Dynamical Systems View of Successive Paraphrasing." arXiv:2502.15208, 2025.

**Summary:** Treats LLMs as iterated maps on text space and studies the dynamics of successive paraphrasing. Finds that iterating an LLM on its own output converges to low-order attractor cycles (typically 2-cycles), not fixed points. The LLM's self-reinforcing nature causes it to amplify certain textual forms, reducing linguistic diversity. Analyzes this using dynamical systems concepts: attractors, limit cycles, basins of attraction.

**Availability:** [arXiv:2502.15208](https://arxiv.org/html/2502.15208v1).

**Relevance:** The most directly relevant work. It literally treats the LLM as a discrete dynamical system f: text -> text and studies the orbit structure. Key finding: orbits converge to periodic attractors (not fixed points, not chaos). This connects directly to Wolfram's Class 2 (periodic structures) and to the theory of finite-state dynamical systems where all orbits terminate in cycles.

---

### 7.2 Madani et al. (arXiv, Mar 2023) — Self-Refine: Iterative Refinement with Self-Feedback

**Citation:** Aman Madani et al. "Self-Refine: Iterative Refinement with Self-Feedback." arXiv:2303.17651, 2023.

**Summary:** Proposes using an LLM to iteratively improve its own output: generate -> self-critique -> refine -> repeat. No additional training or RL required. Shows practical improvements across multiple tasks when run for a bounded number of iterations.

**Availability:** [arXiv:2303.17651](https://arxiv.org/abs/2303.17651). Project page: [selfrefine.info](https://selfrefine.info/).

**Relevance:** A practical (f, x) -> (f, x') system where f is fixed (the LLM) and x' is the refined output. The bounded iteration is key -- unbounded iteration leads to the attractors/collapse described in 7.1. This is a fixed-f system; the self-modifying case (where f changes too) remains largely unexplored in practice.

---

### 7.3 Anonymous (arXiv, May 2025) — When Your Own Output Becomes Your Training Data

**Citation:** "When Your Own Output Becomes Your Training Data." arXiv:2505.02888, 2025.

**Summary:** Studies what happens when an LLM is trained on its own generated data (the self-referential training loop). Proves that this process cannot increase mutual information with the true data distribution, by the data processing inequality applied to the Markov chain P -> Q_t -> Q_{t+1}. Describes "model collapse" -- progressive degradation of the model's distribution toward lower entropy and reduced diversity.

**Availability:** [arXiv:2505.02888](https://arxiv.org/pdf/2505.02888).

**Relevance:** This addresses the case where f itself changes (the model is retrained on its own output). The result is a (f_t, x_t) -> (f_{t+1}, x_{t+1}) system where both the model and the data degrade. The information-theoretic proof that mutual information cannot increase is a strong negative result: self-referential training is fundamentally lossy.

---

### 7.4 Anonymous (arXiv, Jan 2025) — On the Limits of Self-Improving in LLMs

**Citation:** "On the Limits of Self-Improving in LLMs." arXiv:2601.05280, 2025.

**Summary:** Formally defines the self-improvement loop for LLMs and proves convergence/collapse results. The "curse of recursion": training on self-generated data causes model collapse. The data processing inequality provides the theoretical bound.

**Availability:** [arXiv:2601.05280](https://www.arxiv.org/pdf/2601.05280).

**Relevance:** Complementary to 7.3. Together they establish that naive self-improvement (where the LLM's output becomes its own training data) is provably limited. This constrains the (f, x) -> (f', x') dynamics: the trajectory must lose information over time unless external data is injected.

---

## 8. Connecting Threads: Transformation Semigroups and Algebraic Automata Theory

### 8.1 Krohn & Rhodes — Algebraic Theory of Machines I (1965)

**Citation:** Kenneth R. Krohn and John L. Rhodes. "Algebraic Theory of Machines I: Prime Decomposition Theorems for Finite Semigroups and Machines." *Transactions of the American Mathematical Society*, 116:450--464, 1965.

**Summary:** Proves the Krohn-Rhodes decomposition theorem: any finite automaton (equivalently, any finite transformation semigroup) can be decomposed into a cascade (wreath product) of "prime" components, which are either finite simple groups or copies of a 3-element flip-flop monoid. This is the semigroup analogue of the Jordan-Holder decomposition for groups. It means every finite-state machine has an algebraic "prime factorization."

**Availability:** [AMS](https://www.ams.org/journals/tran/1965-116-00/S0002-9947-1965-0188316-1/) (institutional access). Also on [ResearchGate](https://www.researchgate.net/publication/243075966_Algebraic_Theory_of_Machines_I_Prime_Decomposition_Theorem_for_Finite_Semigroups_and_Machines).

**Relevance:** Directly relevant to IFS on finite state spaces. If we have a finite set of maps on a finite set (i.e., a finitely generated transformation semigroup), Krohn-Rhodes tells us it can be decomposed into simple components. This gives a structural understanding of how compositions of maps on finite sets behave -- exactly the setting of discrete dynamical systems where the "function" is drawn from a finite repertoire.

---

### 8.2 Margolis, Rhodes & Schilling — Decidability of Krohn-Rhodes Complexity (2024)

**Citation:** Stuart Margolis, John Rhodes, and Anne Schilling. "Decidability of Krohn-Rhodes complexity for all finite semigroups and automata." arXiv:2406.18477, 2024.

**Summary:** Resolves a long-standing open problem by proving that the Krohn-Rhodes complexity of a finite semigroup is decidable. The complexity of a semigroup is the minimum number of group components needed in any Krohn-Rhodes decomposition. This was open for nearly 60 years.

**Availability:** [arXiv:2406.18477](https://arxiv.org/abs/2406.18477).

**Relevance:** Establishes that the algebraic complexity of finite transformation semigroups is computable. This means we can, in principle, determine how "complex" a finite-state iterated system is in terms of its algebraic structure.

---

## Summary Tables

### By Topic

| Topic | Key Works | Core Idea |
|---|---|---|
| **Tag systems** | Post (1943), Minsky (1961), Cocke-Minsky (1964), De Mol (2008) | Simplest string-rewriting systems that are Turing-complete |
| **Symbolic dynamics foundations** | Morse-Hedlund (1938, 1940), Lind-Marcus (1995/2021), Bowen (1970, 1975) | Coding orbits as symbolic sequences; SFTs, sofic shifts, entropy |
| **Sliding block codes** | Hedlund (1969), Sobottka-Goncalves (2017) | Continuous shift-equivariant maps = local rules (Curtis-Hedlund-Lyndon) |
| **IFS on discrete spaces** | Hutchinson (1981), Barnsley-Demko (1985), Barnsley (1988), Martyn (2024) | Iterated maps with invariant sets; attractors of random iteration |
| **Substitution systems** | Cobham (1972), Allouche-Shallit (2003), Queffelec (1987/2010), Durand (1998, 2011) | Fixed points of iterated morphisms; automatic and morphic sequences |
| **CA as dynamical systems** | Wolfram (1984, 2002), Cook (2004), Hedlund (1969), Kurka (1997, 2003) | Local rules iterated globally; four-class behavior; topological classification |
| **LLM iteration dynamics** | arXiv:2502.15208, arXiv:2303.17651, arXiv:2505.02888, arXiv:2601.05280 | Attractor cycles, model collapse, information loss in self-referential loops |
| **Algebraic automata theory** | Krohn-Rhodes (1965), Margolis-Rhodes-Schilling (2024) | Decomposition of finite-state machines into prime components |

### Availability Summary

| Work | Open Access? | URL |
|---|---|---|
| Post (1943) | Yes | [PDF](https://lib.ysu.am/articles_art/63062f3ed126193beb426becc0fbbe33.pdf) |
| Minsky (1961) | Yes | [PDF](https://www.wolframscience.com/prizes/tm23/images/Minsky.pdf) |
| Cocke-Minsky (1964) | Partial | [MIT DSpace](https://dspace.mit.edu/handle/1721.1/6107) |
| De Mol (2008) | Partial | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0304397507007700) |
| De Mol (2007 MCU) | Yes | [PDF](https://www.clps.ugent.be/sites/default/files/publications/MCU07_r.pdf) |
| Morse-Hedlund (1938) | No (JSTOR) | -- |
| Morse-Hedlund (1940) | No (JSTOR) | -- |
| Lind-Marcus (1995/2021) | No (book) | [CUP frontmatter](https://assets.cambridge.org/97811088/20288/frontmatter/9781108820288_frontmatter.pdf) |
| Bowen (1970) | No (JSTOR) | -- |
| Bowen (1975) | Yes | [PDF](https://www.cpht.polytechnique.fr/sites/default/files/Bowen_LN_Math_470_second_ed_v2013.pdf) |
| Hedlund (1969) | No (Springer) | [Springer](https://link.springer.com/article/10.1007/BF01691062) |
| Sobottka-Goncalves (2017) | Yes | [arXiv:1507.02180](https://arxiv.org/abs/1507.02180) |
| Hutchinson (1981) | Yes | [PDF](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf) |
| Barnsley-Demko (1985) | No (Royal Soc) | [DOI](https://royalsocietypublishing.org/doi/10.1098/rspa.1985.0057) |
| Barnsley (1988) | Yes | [PDF](http://lib.ysu.am/open_books/418197.pdf) |
| Barnsley et al. (1989) | No (Springer) | [Springer](https://link.springer.com/article/10.1007/BF01889596) |
| Ghosh-Marecek (2022) | Yes | [arXiv:2211.14661](https://arxiv.org/pdf/2211.14661) |
| Martyn (2024) | Yes | [arXiv:2410.15139](https://arxiv.org/abs/2410.15139) |
| Cobham (1972) | No (Springer) | -- |
| Allouche-Shallit (2003) | Yes | [PDF](http://lib.ysu.am/disciplines_bk/47fe303913ad333b6dea08e0ba2a9fbb.pdf) |
| Queffelec (1987/2010) | No (Springer) | -- |
| Durand (1998) | No (Springer) | -- |
| Durand (2011) | No (EMS) | -- |
| Wolfram (1984) | Yes | [PDF](https://content.wolfram.com/sw-publications/2020/07/universality-complexity-cellular-automata.pdf) |
| Wolfram (2002) | Yes | [wolframscience.com](https://www.wolframscience.com/nks/) |
| Cook (2004) | Yes | [PDF](https://content.wolfram.com/sites/13/2023/02/15-1-1.pdf) |
| Kurka (1997) | Partial | [PDF](https://www.cts.cuni.cz/~kurka/cantor.pdf) |
| Kurka (2003) | No (book) | -- |
| Krohn-Rhodes (1965) | No (AMS) | -- |
| Margolis et al. (2024) | Yes | [arXiv:2406.18477](https://arxiv.org/abs/2406.18477) |
| LLM attractor cycles (2025) | Yes | [arXiv:2502.15208](https://arxiv.org/html/2502.15208v1) |
| Self-Refine (2023) | Yes | [arXiv:2303.17651](https://arxiv.org/abs/2303.17651) |
| Model collapse (2025) | Yes | [arXiv:2505.02888](https://arxiv.org/pdf/2505.02888) |
| Limits of self-improving (2025) | Yes | [arXiv:2601.05280](https://www.arxiv.org/pdf/2601.05280) |

### Relevance to the (f, x) -> (f', x') Framework

The reviewed literature converges on several key insights for self-modifying systems:

1. **Universality is cheap.** Tag systems with deletion number 2 are already Turing-complete (Cocke-Minsky 1964). Rule 110 is universal (Cook 2004). Even minimal rewriting rules can encode arbitrary computation. Implication: self-modifying (f, x) systems need not be complex to exhibit undecidable behavior.

2. **Structure theorems constrain the dynamics.** The Curtis-Hedlund-Lyndon theorem says continuous shift-equivariant maps are local. Krohn-Rhodes says finite transformation semigroups decompose into groups and flip-flops. Cobham's theorem says automatic sequences are rigid under base change. These constrain what iterated maps can do.

3. **Attractors and periodicity dominate in practice.** LLM iteration converges to low-order cycles (arXiv:2502.15208). Substitution fixed points are highly structured (automatic or morphic). IFS have unique attractors under contraction. The generic behavior of iterated maps is convergence to periodic orbits, not chaos or universality.

4. **Self-referential training is lossy.** The data processing inequality proves that model collapse is inevitable when an LLM trains on its own output (arXiv:2505.02888, arXiv:2601.05280). The (f, x) -> (f', x') trajectory loses information monotonically unless external data is injected.

5. **The edge between decidable and undecidable is thin.** De Mol's reduction of Collatz to a small tag system, and the universality of Rule 110, show that the boundary between simple and universal behavior is razor-thin. For discrete dynamical systems on (f, x) pairs, this means: a small increase in system complexity can flip the dynamics from predictable to undecidable.
