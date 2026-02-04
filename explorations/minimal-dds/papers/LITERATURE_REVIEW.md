# Literature Review: Self-Modifying Computation, Reflective Towers, and Universal AI

This review covers foundational and key works on self-modifying computation, organized into five areas. For each entry: full citation, summary, availability, and relevance to dynamical systems on (function, input) pairs where the function itself mutates.

---

## 1. Self-Modifying Turing Machines and Self-Referential Computation

### 1.1 Von Neumann — Theory of Self-Reproducing Automata (1966)

**Citation:** John von Neumann. *Theory of Self-Reproducing Automata*. Edited and completed by Arthur W. Burks. University of Illinois Press, Urbana, 1966.

**Summary:** Von Neumann formalized self-reproducing machines within cellular automata. He showed that a universal constructor can copy both its *program* (interpreted as instructions) and its *description* (copied verbatim), anticipating the dual role of DNA discovered years later. This is the origin of the idea that a machine can treat its own description as both code and data.

**Availability:** Full text at [Internet Archive](https://archive.org/details/theoryofselfrepr00vonn_0). Also [MIT PDF](https://cba.mit.edu/events/03.11.ASE/docs/VonNeumann.pdf).

**Relevance:** Directly models a system where the "program" component self-replicates and potentially mutates. The universal constructor is a concrete (function, tape) pair where the function's output includes a modified copy of itself.

---

### 1.2 Kampis — Self-Modifying Systems in Biology and Cognitive Science (1991)

**Citation:** George Kampis. *Self-Modifying Systems in Biology and Cognitive Science: A New Framework for Dynamics, Information and Complexity*. Pergamon Press (IFSR International Series, Vol. 6), 1991.

**Summary:** Kampis argues that true self-modification involves identity changes in the mathematical sense — the system's "reading frame" or interpretation shifts, not just its state. He distinguishes between systems that merely update state within a fixed dynamics and systems where the dynamics itself changes. He introduces "component-systems" where components transform each other, making the system closed to efficient cause.

**Availability:** Book only (Elsevier/Pergamon). Not freely available. [ScienceDirect page](https://www.sciencedirect.com/book/9780080369792/self-modifying-systems-in-biology-and-cognitive-science).

**Relevance:** Directly relevant. Kampis's central thesis is that in a genuine self-modifying system, the function (dynamics) itself changes, not just the state. He formalizes the distinction between state-update and function-update, which is exactly the (f, x) -> (f', x') pattern.

---

### 1.3 Prokopenko et al. — Self-Referential Basis of Undecidable Dynamics (2017)

**Citation:** Mikhail Prokopenko, Michael Harré, Joseph Lizier, Fabio Boschetti, Pavlos Peppas, Stuart Kauffman. "Self-referential basis of undecidable dynamics: from The Liar Paradox and The Halting Problem to The Edge of Chaos." arXiv:1711.02456, 2017.

**Summary:** Explores the relationship between formal systems, algorithms, and dynamical systems, identifying three factors underlying undecidable dynamics: (i) program-data duality, (ii) access to an infinite computational medium, and (iii) the ability to implement negation. Argues that self-reference and diagonalization are common structural features across all three frameworks.

**Availability:** [arXiv:1711.02456](https://arxiv.org/abs/1711.02456)

**Relevance:** Directly connects program-data duality (the (f, x) pair where f can also be x) to undecidability in dynamical systems. Their "edge of chaos" framing maps naturally to the question of what happens when the function component of a discrete dynamical system is allowed to self-modify.

---

### 1.4 Lano — Towards a Self-Replicating Turing Machine (2023)

**Citation:** Kevin Lano. "Towards a Self-Replicating Turing Machine." arXiv:2306.16872, 2023.

**Summary:** Provides partial implementations of von Neumann's universal constructor and copier as actual Turing machines, built from simple building blocks. Proposes a self-replicating TM that allows for mutations.

**Availability:** [arXiv:2306.16872](https://arxiv.org/abs/2306.16872)

**Relevance:** A concrete construction of a TM that copies and potentially mutates its own transition table — a literal (f, tape) -> (f', tape') system.

---

## 2. Reflective Towers in Programming Languages

### 2.1 Smith — Reflection and Semantics in Lisp (1982, 1984)

**Citation:** Brian Cantwell Smith. *Reflection and Semantics in a Procedural Language*. PhD thesis, MIT, 1982. MIT-LCS-TR-272.

**Citation (conference):** Brian Cantwell Smith. "Reflection and Semantics in LISP." *Proceedings of the 11th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL '84)*, 1984.

**Summary:** Introduces *procedural reflection*: a program can access and modify the data structures of its own interpreter. Smith designed 3-Lisp, where every program is interpreted by a meta-circular interpreter also in 3-Lisp, forming a conceptually infinite tower. A "reflective lambda" executes one level up, gaining access to the interpreter's state (continuations, environments). Reification makes the interpreter's state available as data; reflection injects data back as running interpreter state.

**Availability:** 1984 paper: [UCI mirror (PDF)](https://ics.uci.edu/~jajones/INF102-S18/readings/17_Smith84.pdf). Also [Academia.edu](https://www.academia.edu/79745691/Reflection_and_semantics_in_LISP). Implementation: [GitHub](https://github.com/nikitadanilov/3-lisp).

**Relevance:** The reflective tower is *exactly* a dynamical system on (function, input) pairs where the function can self-modify. Each level's interpreter is the "function" for the level below, and reflective lambdas allow the running program to reach up and mutate the function that is interpreting it. The tower structure formalizes the infinite regress of "who interprets the interpreter."

---

### 2.2 des Rivières & Smith — Implementation of Procedurally Reflective Languages (1984)

**Citation:** Jim des Rivières and Brian Cantwell Smith. "Implementation of Procedurally Reflective Languages." *Conf. Rec. 1984 ACM Symposium on Lisp and Functional Programming*, pp. 331–347, 1984.

**Summary:** Addresses the practical question: you cannot actually run an infinite tower. Shows how to implement the tower by creating meta-levels on demand — synthesizing the interpreter's state only when a reflective lambda is invoked.

**Availability:** ACM Digital Library.

**Relevance:** Shows that the infinite (f, x) tower can be finitely implemented by lazy instantiation, which is analogous to how one might implement an iterated (f, x) -> (f', x') system without pre-computing all future f's.

---

### 2.3 Wand & Friedman — The Mystery of the Tower Revealed (1986/1988)

**Citation:** Mitchell Wand and Daniel P. Friedman. "The Mystery of the Tower Revealed: A Non-Reflective Description of the Reflective Tower." *Proceedings of the 1986 ACM Conference on LISP and Functional Programming*, pp. 298–307. Expanded version: *Lisp and Symbolic Computation* 1, 11–38 (1988).

**Summary:** Gives a denotational (non-reflective) semantics to the reflective tower. Demystifies the circular definition by showing the tower can be understood without using reflection to explain reflection — providing a fixed-point construction of the tower's semantics.

**Availability:** [Springer (1988 journal version)](https://link.springer.com/article/10.1007/BF01806174). [ResearchGate](https://www.researchgate.net/publication/220607034_The_Mystery_of_the_Tower_Revealed_A_Nonreflective_Description_of_the_Reflective_Tower).

**Relevance:** The fixed-point semantics directly connect to the question of what the "steady states" of a self-modifying (f, x) system look like. The tower's semantics is itself a fixed point of an operator on interpretations.

---

### 2.4 Danvy & Malmkjaer — Intensions and Extensions in a Reflective Tower (1988)

**Citation:** Olivier Danvy and Karoline Malmkjaer. "Intensions and Extensions in a Reflective Tower." *Conference Record of the 1988 ACM Symposium on Lisp and Functional Programming*, pp. 327–341, 1988. See also: "A Blond Primer," DIKU Rapport 88/21, University of Copenhagen, 1988.

**Summary:** Presents the language Blond, a reflective Scheme. Models the tower's levels as related *extensionally* (by mutual interpretation) and *intensionally* (by reification and reflection). Formalizes the distinction between what a level computes vs. how it is represented.

**Availability:** [Semantic Scholar](https://www.semanticscholar.org/paper/Intensions-and-extensions-in-a-reflective-tower-Danvy-Malmkj%C3%A6r/13c9e64413c9a2a05c18da8e98a69abb25f12251).

**Relevance:** The intension/extension distinction maps to the (f, x) framework: the extension is the input-output behavior; the intension is the specific representation (code) of f. Self-modification changes the intension while potentially preserving or altering the extension.

---

### 2.5 Amin & Rompf — Collapsing Towers of Interpreters (2018)

**Citation:** Nada Amin and Tiark Rompf. "Collapsing Towers of Interpreters." *Proc. ACM Program. Lang.* 2, POPL, Article 52, January 2018. DOI: 10.1145/3158140.

**Summary:** Shows how to collapse an arbitrary tower of interpreters into a single compiled pass using *stage polymorphism*: an evaluator that, depending on runtime parameters, either interprets or generates code. Develops Pink (a collapsible meta-circular Lisp) and Purple (a reflective language inspired by Black/Brown/Blond where semantics can change dynamically, and the program can be recompiled under modified semantics).

**Availability:** [Purdue PDF](https://www.cs.purdue.edu/homes/rompf/papers/amin-popl18.pdf). [EPFL PDF](https://lampwww.epfl.ch/~amin/pub/collapsing-towers.pdf). Code: [GitHub](https://github.com/TiarkRompf/collapsing-towers/tree/master/popl18).

**Relevance:** Demonstrates that a tower of (f, x) pairs — where each f interprets the level below — can be collapsed via partial evaluation. This is essentially a compiler for self-modifying systems: if you know the trajectory of modifications, you can pre-compute the result.

---

## 3. AIXI and Universal AI Frameworks

### 3.1 Solomonoff — A Formal Theory of Inductive Inference (1964)

**Citation:** Ray J. Solomonoff. "A Formal Theory of Inductive Inference, Part I." *Information and Control* 7(1):1–22, 1964. "Part II." *Information and Control* 7(2):224–254, 1964.

**Summary:** Defines algorithmic probability: the prior probability of a sequence is the sum of 2^{-|p|} over all programs p on a universal TM that output that sequence. This formalizes Occam's razor — shorter programs get higher prior weight. Proves this universal prior M dominates any computable prior, making it optimal for sequence prediction.

**Availability:** [Part I (PDF)](http://raysolomonoff.com/publications/1964pt1.pdf). [Part II (PDF)](http://raysolomonoff.com/publications/1964pt2.pdf). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0019995864902232).

**Relevance:** The Solomonoff prior is defined over programs (functions). When used for prediction, the "hypothesis" is a program that generates the observed data — so the framework is already implicitly reasoning over (function, data) pairs. The prior assigns weights based on program length, which connects to the complexity of the function component.

---

### 3.2 Levin — Universal Sequential Search Problems (1973)

**Citation:** Leonid A. Levin. "Universal Sequential Search Problems." *Problems of Information Transmission* 9(3):265–266, 1973. (Original Russian: *Problemy Peredaci Informacii* 9(3):115–116, 1973.)

**Summary:** Presents Levin Search (universal search): interleave execution of all possible programs, sharing computation time, until one solves the problem. Proves this is optimal up to a multiplicative constant: it solves any inversion problem in time 2^{|p*|} * t*, where p* is the shortest program solving it in time t*.

**Availability:** [PDF with proofs (Fortnow)](https://lance.fortnow.com/papers/files/Levin%20Universal%20with%20Proofs.pdf).

**Relevance:** Levin Search is the computational backbone of computable approximations to AIXI. It searches the space of all programs (functions), which is the space of possible "f" components in an (f, x) system.

---

### 3.3 Hutter — AIXI: Universal Artificial Intelligence (2000–2005)

**Citation (original paper):** Marcus Hutter. "A Theory of Universal Artificial Intelligence based on Algorithmic Complexity." arXiv:cs/0004001, 2000.

**Citation (book):** Marcus Hutter. *Universal Artificial Intelligence: Sequential Decisions based on Algorithmic Probability*. Springer, Berlin, 2005.

**Citation (gentle intro):** Marcus Hutter. "Universal Algorithmic Intelligence: A Mathematical Top→Down Approach." arXiv:cs/0701125, 2007.

**Citation (survey):** Marcus Hutter. "One Decade of Universal Artificial Intelligence." arXiv:1202.6153, 2012.

**Summary:** AIXI combines Solomonoff induction with sequential decision theory. At each step, the agent considers every computable environment (program), weights each by its algorithmic probability, and chooses the action maximizing expected total reward. AIXI is provably optimal but incomputable. The computable approximation AIXItl restricts to programs running in time t and space l, and is provably at least as good as any other agent with the same resource bounds.

**Availability:**
- [arXiv:cs/0004001](https://arxiv.org/abs/cs/0004001)
- [arXiv:cs/0701125](https://arxiv.org/abs/cs/0701125)
- [arXiv:1202.6153](https://arxiv.org/abs/1202.6153)
- [Hutter's page](https://www.hutter1.net/ai/uaibook.htm)

**Relevance:** AIXI models an agent interacting with an environment. The environment *is* a program (function), and the agent maintains a distribution over all possible environment-programs. At each step the agent updates its belief about which function it is interacting with. This is a Bayesian version of a dynamical system on (belief-over-functions, observation-history) pairs. However, AIXI does not model self-modification of the agent itself — it treats the agent as fixed and the environment as the unknown function.

---

### 3.4 Hutter & Quarel & Catt — Introduction to Universal Artificial Intelligence (2024)

**Citation:** Marcus Hutter, David Quarel, Elliot Catt. *Introduction to Universal Artificial Intelligence*. Springer, 2024.

**Summary:** A more accessible textbook treatment of the AIXI framework, with updated material on approximations, environment classes, and connections to modern AI.

**Availability:** Springer (book). See [Hutter's publications page](http://www.hutter1.net/official/bib.htm).

**Relevance:** Same as AIXI above, but with additional discussion of embeddedness and self-reference problems.

---

## 4. Gödel Machines (Schmidhuber)

### 4.1 Schmidhuber — Gödel Machines (2003/2007)

**Citation:** Jürgen Schmidhuber. "Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements." arXiv:cs/0309048, 2003. Book chapter version: *Artificial General Intelligence*, Springer, pp. 199–226, 2007.

**Summary:** A Gödel Machine is a program that can rewrite *any* part of its own code — including the part that searches for rewrites — as soon as it has constructed a formal proof that the rewrite will improve expected future utility. The proof searcher systematically tests all computable proof techniques. This is globally optimal (no local maxima) because the machine must prove that continuing to search for better rewrites is not itself more useful than the proposed rewrite. Limited by Gödel's incompleteness: some provably beneficial rewrites may exist but not be provable within the system's axioms.

**Availability:** [arXiv:cs/0309048](https://arxiv.org/abs/cs/0309048). [IDSIA PDF](https://sferics.idsia.ch/pub/juergen/gmAGI.pdf).

**Relevance:** This is the most direct formalization of the (f, x) -> (f', x') pattern. The Gödel Machine is literally a program (f) operating on data (x) that produces a modified program (f') as part of its output. The key constraint is that f' must be *provably* better than f. The machine's state includes its own source code as data, and the transition function modifies that code.

---

### 4.2 Schmidhuber — Optimal Ordered Problem Solver (OOPS) (2002/2004)

**Citation:** Jürgen Schmidhuber. "Optimal Ordered Problem Solver." *Machine Learning* 54:211–254, 2004. arXiv:cs/0207097.

**Summary:** OOPS is an incremental universal search that reuses solutions to previous tasks. When solving a new problem, it tests programs that invoke/copy-edit previous solutions. If the new problem can be solved faster by reusing old code than from scratch, OOPS discovers this. It is bias-optimal: no other method with the same underlying assumptions can be faster by more than a constant factor.

**Availability:** [arXiv:cs/0207097](https://arxiv.org/abs/cs/0207097). [IDSIA page](https://people.idsia.ch/~juergen/oopsweb/oopsweb.html).

**Relevance:** OOPS is a concrete self-improving system where the "function" (solver) grows by accumulating and recombining code. The trajectory (f_0, f_1, f_2, ...) of increasingly capable solvers is a dynamical system on the space of programs.

---

### 4.3 Schmidhuber — Ultimate Cognition à la Gödel (2009)

**Citation:** Jürgen Schmidhuber. "Ultimate Cognition à la Gödel." *Cognitive Computation* 1:177–193, 2009.

**Summary:** A synthetic overview. Argues that the Gödel Machine framework is the mathematically rigorous blueprint for "ultimate cognition": a program that rewrites itself using Gödel's self-reference trick, constrained only by the limits of provability. Connects to the Speed Prior (Schmidhuber, COLT 2002) and to Hutter's AIXI.

**Availability:** [Springer](https://link.springer.com/article/10.1007/s12559-009-9014-y).

**Relevance:** Provides the theoretical ceiling: what is the best possible self-modifying agent, and what are the limits imposed by incompleteness?

---

## 5. Kleene's Recursion Theorem and Fixed Points of Program Transformations

### 5.1 Kleene — On the Interpretation of Intuitionistic Number Theory (1938/1952)

**Citation:** Stephen C. Kleene. "On Notation for Ordinal Numbers." *Journal of Symbolic Logic* 3:150–155, 1938. Expanded treatment in: S. C. Kleene, *Introduction to Metamathematics*. North-Holland, Amsterdam, 1952.

**Summary:** The Second Recursion Theorem (SRT): for any computable function T(e, x) there exists an index e* such that the program e* computes the same function as T(e*, ·). In other words, any effective transformation of programs has a fixed point — a program whose behavior is unchanged by the transformation. This is the formal foundation of all self-referential computation: quines, viruses, the recursion theorem method in computability proofs, and (indirectly) reflective towers.

**Availability:** Kleene (1952) is a standard textbook, available in many libraries. The theorem and proof are reproduced in all modern computability texts (e.g., Sipser, Rogers, Soare).

**Relevance:** Fundamental. Any dynamical system (f, x) -> (T(f), g(x)) on programs has a fixed point f* such that T(f*) = f* (extensionally). This means: for any rule that transforms the "function" component, there exists a function that is a fixed point of that rule. This constrains the dynamics — every orbit must either reach a fixed point or cycle through extensionally distinct programs.

---

### 5.2 Rogers — Theory of Recursive Functions and Effective Computability (1967)

**Citation:** Hartley Rogers, Jr. *Theory of Recursive Functions and Effective Computability*. McGraw-Hill, 1967. MIT Press reprint, 1987.

**Summary:** The standard graduate textbook on computability theory. Contains Rogers's Fixed-Point Theorem (a reformulation of Kleene's SRT): for any total computable function f, there exists e such that phi_e = phi_{f(e)}. Also develops the theory of acceptable numberings and shows the recursion theorem holds for all of them.

**Availability:** [Internet Archive](https://archive.org/details/theoryofrecursiv00roge). MIT Press (ISBN 9780262680523).

**Relevance:** Rogers's framing is more directly applicable: "given any effective procedure to transform programs, there is always a program that, when modified by the procedure, does exactly what it did before." This is a fundamental constraint on (f, x) -> (T(f), x') systems.

---

### 5.3 Case — Infinitary Self-Reference in Learning Theory (1994)

**Citation:** John Case. "Infinitary Self-Reference in Learning Theory." *Journal of Experimental and Theoretical Artificial Intelligence* 6(1), 1994. See also: John Case and Samuel Moelius. "Characterizing Programming Systems Allowing Program Self-Reference." *Springer LNCS 4497*, pp. 127–138, 2007.

**Summary:** Explores what happens when learning algorithms can access their own source code via the recursion theorem. Shows that self-reference (in the Kleene/Rogers sense) can sometimes strictly increase learning power. The 2007 paper characterizes which programming systems allow effective self-reference (precomplete numberings, per Ershov).

**Availability:** 2007 paper: [Springer](https://link.springer.com/chapter/10.1007/978-3-540-73001-9_13).

**Relevance:** Directly relevant to (f, x) systems where f can read its own code: Case shows this self-reference is not just a curiosity but can provide strictly more computational power in learning-theoretic settings.

---

### 5.4 Kiselyov — Kleene Second Recursion Theorem: A Functional Pearl

**Citation:** Oleg Kiselyov. "Kleene Second Recursion Theorem: A Functional Pearl." Available at okmij.org.

**Summary:** Bridges computability theory and modern metaprogramming. Presents the recursion theorem constructively, showing how it manifests as Y-combinator-like constructions in actual programming languages. Provides a "Rosetta stone" between classical recursion-theoretic notation and practical code.

**Availability:** [PDF](https://okmij.org/ftp/Computation/Kleene.pdf)

**Relevance:** Makes the fixed-point theorem concrete and implementable, connecting the abstract (f, x) -> (T(f), x') framework to actual programs one can run.

---

## Cross-Cutting Themes and Synthesis

| Theme | Key Works | Connection to (f, x) -> (f', x') |
|---|---|---|
| **Self-replication** | von Neumann (1966), Kleene SRT (1938) | f produces a copy of itself (possibly mutated) as part of x' |
| **Reflective towers** | Smith (1984), Wand & Friedman (1986), Danvy (1988), Amin & Rompf (2018) | Infinite stack of (f_i, x_i) pairs where f_i interprets f_{i-1}; programs can modify f_i |
| **Fixed points** | Kleene (1938), Rogers (1967) | Every computable T has an f* with T(f*) = f*; constrains possible trajectories |
| **Provable self-improvement** | Schmidhuber Gödel Machine (2003), OOPS (2004) | f -> f' only when provably better; trajectory is monotonically improving (in utility) |
| **Universal prediction/action** | Solomonoff (1964), Hutter AIXI (2000) | Agent maintains distribution over possible f's; does not self-modify but reasons about unknown f |
| **Component systems** | Kampis (1991) | Components transform each other; f is not fixed but emerges from component interactions |
| **Undecidability of self-modification** | Prokopenko et al. (2017), Gödel (1931) | General properties of (f, x) trajectories are undecidable; incompleteness limits provable self-improvement |

---

## Summary of Open Availability

| Work | Freely Available? | URL |
|---|---|---|
| von Neumann (1966) | Yes | [Internet Archive](https://archive.org/details/theoryofselfrepr00vonn_0) |
| Kampis (1991) | No (book) | — |
| Prokopenko et al. (2017) | Yes | [arXiv:1711.02456](https://arxiv.org/abs/1711.02456) |
| Lano (2023) | Yes | [arXiv:2306.16872](https://arxiv.org/abs/2306.16872) |
| Smith (1984) | Yes | [UCI PDF](https://ics.uci.edu/~jajones/INF102-S18/readings/17_Smith84.pdf) |
| Wand & Friedman (1986/88) | Partial | [Springer](https://link.springer.com/article/10.1007/BF01806174) |
| Danvy & Malmkjaer (1988) | Partial | [Semantic Scholar](https://www.semanticscholar.org/paper/13c9e64413c9a2a05c18da8e98a69abb25f12251) |
| Amin & Rompf (2018) | Yes | [PDF](https://www.cs.purdue.edu/homes/rompf/papers/amin-popl18.pdf) |
| Solomonoff (1964) | Yes | [PDF pt1](http://raysolomonoff.com/publications/1964pt1.pdf) |
| Levin (1973) | Yes | [PDF](https://lance.fortnow.com/papers/files/Levin%20Universal%20with%20Proofs.pdf) |
| Hutter AIXI (2000) | Yes | [arXiv:cs/0004001](https://arxiv.org/abs/cs/0004001) |
| Hutter (2005 book) | No (book) | [Author page](https://www.hutter1.net/ai/uaibook.htm) |
| Hutter (2007 gentle) | Yes | [arXiv:cs/0701125](https://arxiv.org/abs/cs/0701125) |
| Schmidhuber Gödel (2003) | Yes | [arXiv:cs/0309048](https://arxiv.org/abs/cs/0309048) |
| Schmidhuber OOPS (2004) | Yes | [arXiv:cs/0207097](https://arxiv.org/abs/cs/0207097) |
| Schmidhuber (2009) | Paywall | [Springer](https://link.springer.com/article/10.1007/s12559-009-9014-y) |
| Rogers (1967) | Yes | [Internet Archive](https://archive.org/details/theoryofrecursiv00roge) |
| Kiselyov (Kleene pearl) | Yes | [PDF](https://okmij.org/ftp/Computation/Kleene.pdf) |
