# Chapter 7: Cellular Automata as Dynamical Systems

## 7.1 Definition

A **cellular automaton** (CA) consists of the following data:

1. A **lattice** $\Lambda$, typically $\mathbb{Z}$ (one-dimensional) or $\mathbb{Z}^d$ (d-dimensional).
2. A **finite state set** $S$ with $|S| = k \geq 2$. Each cell $i \in \Lambda$ holds a state $s_i \in S$.
3. A **neighborhood** $\mathcal{N} = \lbrace n_1, n_2, \ldots, n_m\rbrace  \subset \mathbb{Z}^d$, a fixed finite set of offset vectors.
4. A **local update rule** $f: S^{|\mathcal{N}|} \to S$ that maps the states of a cell's neighbors to the cell's new state.

A **configuration** is a function $c: \Lambda \to S$, i.e., an element of $S^{\Lambda}$. The **global map** $F: S^{\Lambda} \to S^{\Lambda}$ is defined by applying $f$ synchronously to every cell:

$$F(c)_i = f(c_{i + n_1}, c_{i + n_2}, \ldots, c_{i + n_m})$$

The space $S^{\Lambda}$ is given the product topology (each copy of $S$ is discrete), making it a Cantor set when $\Lambda$ is infinite. The global map $F$ is continuous in this topology and commutes with all lattice translations $\sigma_v$ for $v \in \Lambda$:

$$F \circ \sigma_v = \sigma_v \circ F$$

This translation-invariance is a defining property of CA.


## 7.2 Elementary Cellular Automata

The simplest nontrivial case is the **elementary cellular automaton** (ECA):

- Lattice: $\mathbb{Z}$ (one-dimensional)
- State set: $S = \lbrace 0, 1\rbrace $ (two states)
- Neighborhood: radius $r = 1$, so $\mathcal{N} = \lbrace -1, 0, 1\rbrace $ (three cells: left, center, right)

The local rule $f: \lbrace 0,1\rbrace ^3 \to \lbrace 0,1\rbrace $ is determined by its values on the $2^3 = 8$ possible input triples. Since each output is in $\lbrace 0,1\rbrace $, there are $2^8 = 256$ possible ECA rules.

### 7.2.1 Wolfram's Numbering Scheme

Wolfram (1984) introduced a canonical numbering of these 256 rules. The 8 input triples are listed in descending binary order:

| Input (left, center, right) | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|---|---|---|---|---|---|---|---|---|
| Bit position                 | 7   | 6   | 5   | 4   | 3   | 2   | 1   | 0   |

The outputs for these 8 inputs form an 8-bit binary number, read from bit 7 (MSB) down to bit 0 (LSB). The decimal value of this binary number is the **rule number**.

**Example.** If the outputs are $0, 1, 1, 0, 1, 1, 1, 0$ (for inputs 111 through 000 respectively), the binary string is $01101110_2 = 110_{10}$, giving **Rule 110**.


### 7.2.2 Rule 30

Rule 30 has rule number $30 = 00011110_2$. The lookup table is:

| Input | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|---|---|---|---|---|---|---|---|---|
| Output | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |

An equivalent algebraic expression: $f(l, c, r) = l \oplus (c \lor r)$, where $\oplus$ is XOR and $\lor$ is OR.

### 7.2.3 Rule 110

Rule 110 has rule number $110 = 01101110_2$:

| Input | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|---|---|---|---|---|---|---|---|---|
| Output | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |

### 7.2.4 Rule 90

Rule 90 has rule number $90 = 01011010_2$:

| Input | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|---|---|---|---|---|---|---|---|---|
| Output | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |

Algebraically: $f(l, c, r) = l \oplus r$ (the center cell is ignored; only the XOR of the two neighbors matters).


## 7.3 Worked Examples: Tracing ECA Evolution

### Example 7.1: Rule 90

We trace Rule 90 ($f(l,c,r) = l \oplus r$) from a single live cell on a background of zeros. We use a finite window, padding with 0 outside the shown region.

```
t=0:  . . . . 1 . . . .
t=1:  . . . 1 . 1 . . .
t=2:  . . 1 . 0 . 1 . .
t=3:  . 1 . 1 1 1 . 1 .
t=4:  1 . 0 . 0 . 0 . 1
```

Here `.` denotes 0, and we trace a few cells explicitly for $t = 0 \to 1$:

- Cell 4 (center at $t=0$): neighbors are $(0, 1, 0)$. $f(0,1,0) = 0 \oplus 0 = 0$.
- Cell 3: neighbors are $(0, 0, 1)$. $f(0,0,1) = 0 \oplus 1 = 1$.
- Cell 5: neighbors are $(1, 0, 0)$. $f(1,0,0) = 1 \oplus 0 = 1$.

Continuing this process generates the **Sierpinski triangle** modulo 2 -- a self-similar fractal pattern. Each row $t$ corresponds to the binomial coefficients $\binom{t}{j} \mod 2$.


### Example 7.2: Rule 30

We trace Rule 30 ($f(l,c,r) = l \oplus (c \lor r)$) from a single live cell:

```
t=0:  . . . . 1 . . . .
t=1:  . . . 1 1 1 . . .
t=2:  . . 1 1 0 0 1 . .
t=3:  . 1 1 0 1 1 1 1 .
t=4:  1 1 0 0 1 0 0 0 1
```

Verification of $t = 1 \to 2$ for a few cells:

- Cell 3: neighborhood from $t=1$ is $(0, 1, 1)$. $f = 0 \oplus (1 \lor 1) = 0 \oplus 1 = 1$.
- Cell 4: neighborhood is $(1, 1, 1)$. $f = 1 \oplus (1 \lor 1) = 1 \oplus 1 = 0$.
- Cell 5: neighborhood is $(1, 1, 0)$. $f = 1 \oplus (1 \lor 0) = 1 \oplus 1 = 0$.
- Cell 6: neighborhood is $(1, 0, 0)$. $f = 1 \oplus (0 \lor 0) = 1 \oplus 0 = 1$.

The resulting spacetime diagram appears **chaotic**: the pattern shows no discernible regularity, and the center column passes statistical randomness tests. Wolfram used this as the basis of a pseudorandom number generator.


### Example 7.3: Rule 110

We trace Rule 110 from a single live cell, using the table from Section 7.2.3:

```
t=0:  . . . . 1 . . . .
t=1:  . . . 1 1 . . . .
t=2:  . . 1 1 1 . . . .
t=3:  . 1 1 0 1 . . . .
t=4:  1 1 0 0 1 . . . .
```

Verification of $t = 2 \to 3$ for a few cells:

- Cell 2: neighborhood from $t=2$ is $(0, 1, 1)$. Rule 110: $f(0,1,1) = 1$.
- Cell 3: neighborhood is $(1, 1, 1)$. $f(1,1,1) = 0$.
- Cell 4: neighborhood is $(1, 1, 0)$. $f(1,1,0) = 1$.
- Cell 5: neighborhood is $(1, 0, 0)$. $f(1,0,0) = 0$ (but there is right-boundary interaction; on the infinite lattice with zeros, this holds).

From a single seed, Rule 110 produces a leftward-growing triangular region. From random initial conditions on a large lattice, however, it produces **complex** behavior: persistent localized structures ("particles" or "gliders") that move and interact against a periodic background. This complex behavior is the key to its computational universality (see Section 7.8).


## 7.4 Spacetime Diagrams

A **spacetime diagram** displays the evolution of a 1D CA. Space (cell index) runs along the horizontal axis, and time (generation number) runs downward. Each cell is rendered as a pixel colored by its state -- typically black for 1 and white for 0.

The qualitative character of the spacetime diagram is the basis for classification:

- **Rule 30**: The diagram from a single seed produces an irregular, apparently random pattern. No spatial or temporal periodicity is evident, even after millions of steps. The left side develops a nested structure, but the right side and center column appear fully disordered.

- **Rule 110**: The diagram from random initial conditions shows a periodic striped background punctuated by localized structures (gliders) that propagate at various speeds. Collisions between gliders produce new gliders or annihilate. This is the hallmark of Class 4 behavior.

- **Rule 90**: The diagram from a single seed produces the Sierpinski triangle -- a self-similar fractal. At scale $2^n$, the pattern repeats exactly. The Hausdorff dimension of the limit set is $\log_2 3 \approx 1.585$.


## 7.5 Wolfram's Four Classes (1984)

Based on extensive computational experiments, Wolfram (1984) proposed a classification of CA into four behavioral classes:

**Class 1: Homogeneous.** Almost all initial conditions rapidly converge to a single uniform fixed point. Example: **Rule 0** (all cells map to 0) and **Rule 32**.

**Class 2: Periodic.** Almost all initial conditions converge to periodic structures (fixed points or limit cycles), possibly with a short transient. The final pattern may be spatially inhomogeneous but is temporally periodic. Examples: **Rule 4**, **Rule 108**, **Rule 184**.

**Class 3: Chaotic.** Almost all initial conditions produce aperiodic, apparently random behavior. The spacetime diagram looks disordered. Statistically, the patterns are indistinguishable from noise by standard tests. Examples: **Rule 30**, **Rule 45**, **Rule 73**.

**Class 4: Complex.** The evolution produces long-lived, localized propagating structures (particles, gliders) on a periodic or quiescent background. These structures interact in complicated ways. Class 4 sits "at the edge of chaos" between Classes 2 and 3. Examples: **Rule 110**, **Rule 54**.

Wolfram conjectured that Class 4 rules are capable of universal computation, and that Class 4 behavior arises at a phase transition between order (Classes 1--2) and chaos (Class 3). While suggestive, this classification is informal: there is no precise mathematical definition of the four classes, and some rules are difficult to assign unambiguously. Wolfram further developed these ideas in *A New Kind of Science* (2002).


## 7.6 Kurka's Topological Classification (1997)

Kurka (1997) proposed a rigorous topological classification of CA based on the theory of equicontinuity in topological dynamics. This gives a mathematically precise refinement of Wolfram's informal scheme.

Let $(X, F)$ be the dynamical system where $X = S^{\mathbb{Z}}$ with the product topology (metrized by the Cantor metric $d$) and $F$ is the CA global map. Define:

- A point $x \in X$ is an **equicontinuity point** if for every $\varepsilon > 0$, there exists $\delta > 0$ such that $d(x, y) < \delta$ implies $d(F^n(x), F^n(y)) < \varepsilon$ for all $n \geq 0$.
- Let $E_F \subseteq X$ denote the set of equicontinuity points.

Kurka defines four classes:

**E1: Equicontinuous.** Every point is an equicontinuity point: $E_F = X$. Equivalently, all orbits are eventually periodic. This corresponds to Wolfram's Class 1 and the trivial end of Class 2.

**E2: Almost equicontinuous (but not equicontinuous).** The set $E_F$ is residual (contains a dense $G_\delta$ set) but $E_F \neq X$. Most points behave regularly, but sensitivity can occur on a meager set. This captures the nontrivial part of Wolfram's Class 2.

**E3: Sensitive (but not positively expansive).** The set $E_F$ is empty -- the system is sensitive to initial conditions -- but is not positively expansive. This corresponds roughly to Wolfram's Classes 3 and 4.

**E4: Positively expansive.** There exists $\varepsilon > 0$ such that for any $x \neq y$, there exists $n \geq 0$ with $d(F^n(x), F^n(y)) > \varepsilon$. This is the strongest form of chaos. Among ECA, positively expansive rules include certain "spreading" rules. Note: positive expansivity is impossible for CA on $\mathbb{Z}^d$ with $d \geq 2$ (Shereshevsky 1993).

**Theorem 7.1** (Kurka 1997). *Every CA on $S^{\mathbb{Z}}$ falls into exactly one of the classes E1--E4. These classes are mutually exclusive and exhaustive.*

The advantage of Kurka's classification is that it is based on well-defined topological properties. Its limitation is that it does not distinguish between "chaotic" (Class 3) and "complex" (Class 4) within class E3 -- both types of behavior yield an empty equicontinuity set without positive expansivity.


## 7.7 CA as Endomorphisms of the Shift: The Curtis-Hedlund-Lyndon Theorem

The full shift on the alphabet $S$ is the dynamical system $(\Sigma, \sigma)$ where $\Sigma = S^{\mathbb{Z}}$ and $\sigma$ is the left shift map $\sigma(c)_i = c_{i+1}$.

A **sliding block code** (or block map) is a map $F: \Sigma \to \Sigma$ defined by a local rule applied uniformly:

$$F(c)_i = f(c_{i+n_1}, \ldots, c_{i+n_m})$$

for some finite neighborhood $\lbrace n_1, \ldots, n_m\rbrace $ and some function $f: S^m \to S$.

Observe that this is exactly the definition of a CA global map. The following fundamental theorem shows that the converse also holds:

**Theorem 7.2** (Curtis-Hedlund-Lyndon, 1969). *Let $\Sigma = S^{\mathbb{Z}}$ with the product topology, and let $\sigma$ be the shift. A map $F: \Sigma \to \Sigma$ is a sliding block code if and only if $F$ is continuous and commutes with $\sigma$ (i.e., $F \circ \sigma = \sigma \circ F$).*

In the language of symbolic dynamics, the endomorphisms of the full shift $(\Sigma, \sigma)$ are exactly the cellular automata. This places CA theory squarely within the framework of symbolic dynamics. Hedlund (1969) developed many consequences of this perspective.

**Corollary.** The set of all CA on alphabet $S$ forms a monoid under composition: the composition of two sliding block codes is again a sliding block code (with a larger neighborhood).

The Curtis-Hedlund-Lyndon theorem generalizes to subshifts: a continuous shift-commuting map between subshifts of finite type is always a sliding block code. See Lind & Marcus (2021), Chapter 1, for a thorough treatment.


## 7.8 Universality: Rule 110 is Turing-Complete

**Theorem 7.3** (Cook, 2004). *Rule 110 is Turing-complete: it can simulate any Turing machine.*

This was conjectured by Wolfram and proved by Matthew Cook. The proof proceeds in several stages:

1. **Identify particles.** In Rule 110 from typical initial conditions, the background is periodic (with period 14 in space and 7 in time). Against this background, localized structures -- called **gliders** or **particles** -- propagate at rational speeds. Cook catalogued these particles and their collision rules.

2. **Simulate cyclic tag systems.** A **cyclic tag system** is a simple model of computation known to be Turing-universal (due to Cook, building on work of Post). It operates on a binary string by repeatedly applying productions from a fixed cyclic list.

3. **Encode the tag system.** Cook showed how to encode the state and transition rules of an arbitrary cyclic tag system into an initial configuration of Rule 110, using specific arrangements of gliders. The glider collisions implement the tag system's productions.

4. **Verify universality.** Since cyclic tag systems can simulate any Turing machine, Rule 110 inherits Turing-completeness.

The construction requires an infinite (but eventually periodic) initial configuration. Whether Rule 110 is universal from *finite* initial configurations remains open.

This result is remarkable: the simplest class of nontrivial CA (two states, radius 1) already contains a rule capable of universal computation. It supports the view that computational universality is not a rare or delicate property but is widespread among sufficiently complex dynamical rules.


## 7.9 The Garden of Eden Theorem

A configuration $c \in S^{\Lambda}$ is a **Garden of Eden** (GoE) if it has no preimage under the global map $F$: there is no configuration $c'$ with $F(c') = c$. In other words, $c$ can only appear as an initial condition -- it can never be reached by the dynamics.

Two configurations $c, c'$ are **asymptotic** if they differ on only finitely many cells: $\lbrace i \in \Lambda : c_i \neq c'_i\rbrace $ is finite. A CA is **pre-injective** if no two distinct asymptotic configurations have the same image.

**Theorem 7.4** (Moore 1962, Myhill 1963 -- Garden of Eden Theorem). *For a CA on $\mathbb{Z}^d$ with finite state set:*

*(Moore) If the CA is surjective, then it is pre-injective.*

*(Myhill) If the CA is pre-injective, then it is surjective.*

*Equivalently: the CA is surjective if and only if it is pre-injective. Gardens of Eden exist if and only if there exist distinct asymptotic configurations with the same image ("mutually erasable patterns").*

The proof uses a counting argument: both the number of patterns that can appear in a finite region in the image and the number of "orphan" patterns (that cannot appear in any image) are related to the injectivity properties of the local rule on finite blocks. The Myhill direction is typically proved using a compactness argument or a direct combinatorial argument involving the pigeonhole principle on finite approximations.

**Example 7.4.** Consider the ECA "majority rule" on $\mathbb{Z}$ with $S = \lbrace 0,1\rbrace $ and neighborhood $\lbrace -1, 0, 1\rbrace $:

$$f(l, c, r) = \begin{cases} 1 & \text{if } l + c + r \geq 2 \\ 0 & \text{otherwise} \end{cases}$$

This is Rule 232. Consider the two asymptotic configurations $c = \ldots 000 \ldots$ and $c' = \ldots 0010 \ldots$ (differing only at one cell). We have $F(c) = \ldots 000 \ldots$. For $c'$, the cell with state 1 has neighborhood $(0,1,0)$, giving $f(0,1,0) = 0$, and its neighbors have neighborhoods $(0,0,1)$ and $(1,0,0)$, both giving 0. So $F(c') = \ldots 000 \ldots = F(c)$.

Since we found distinct asymptotic configurations with the same image, Rule 232 is **not** pre-injective, hence by the Garden of Eden theorem, it is **not** surjective. Gardens of Eden exist for this rule.


## 7.10 Reversible Cellular Automata

A CA is **reversible** if its global map $F: S^{\mathbb{Z}^d} \to S^{\mathbb{Z}^d}$ is bijective (both injective and surjective). By the Curtis-Hedlund-Lyndon theorem, if $F$ is bijective and continuous and shift-commuting, then its inverse $F^{-1}$ is also continuous and shift-commuting, hence also a CA. Thus:

**Theorem 7.5.** *A bijective CA has an inverse that is also a CA.*

The Garden of Eden theorem gives a powerful consequence for CA on $\mathbb{Z}^d$:

**Corollary.** *For a CA on $\mathbb{Z}^d$, injectivity implies surjectivity.* Hence an injective CA on $\mathbb{Z}^d$ is automatically bijective, and therefore reversible.

The converse (surjectivity implies injectivity) is **false** in general for $d \geq 1$. There exist surjective CA that are not injective.

Reversible CA are important in physics because they conserve information (no Garden of Eden states) and can model time-reversible microscopic dynamics. The **Margolus neighborhood** provides a practical construction method: partition the lattice into blocks and apply a bijection to each block, alternating the partition at each time step.

**Remark.** The statement "injectivity implies surjectivity" fails for CA on lattices other than $\mathbb{Z}^d$ -- for instance, on free groups or on trees, counterexamples exist. This is related to the amenability of the group; the Garden of Eden theorem in its full form holds exactly for amenable groups (Ceccherini-Silberstein, Machi, and Scarabotti 1999; Bartholdi 2010).


## 7.11 Topological Entropy of a CA

Since the CA global map $F$ is a continuous self-map of the compact metrizable space $S^{\mathbb{Z}}$, one can define its **topological entropy** $h(F)$ in the standard sense of dynamical systems theory.

For a CA with state set $S$, the maximum possible topological entropy is $\log |S|$ (the entropy of the full shift). Heuristically, maximal entropy means the CA "preserves all the randomness" in the configuration space.

**Theorem 7.6** (Hedlund 1969). *A surjective CA on $S^{\mathbb{Z}}$ has topological entropy $h(F) = \log |S|$.*

Non-surjective CA can have strictly lower entropy, since the image $F(S^{\mathbb{Z}})$ is a proper subshift (a closed, shift-invariant subset of $S^{\mathbb{Z}}$).

For the **column subshift** -- the subshift of $S^{\mathbb{Z}}$ obtained by intersecting the images $\bigcap_{n \geq 0} F^n(S^{\mathbb{Z}})$ -- the entropy can decrease under iteration and converge to a limit, which measures the "effective" long-time entropy of the CA.

Computing the topological entropy of a CA is in general undecidable (Hurd, Kari, and Culik 1992). Even for specific ECA rules, exact values are known only in special cases (e.g., additive rules like Rule 90, where the entropy can be computed via the associated matrix over $\mathbb{F}_2$).


## 7.12 Two-Dimensional CA: Conway's Game of Life

The **Game of Life** (Conway, 1970) is a 2D CA on $\mathbb{Z}^2$ with $S = \lbrace 0, 1\rbrace $ (dead/alive) and the Moore neighborhood (the 8 surrounding cells). The local rule is:

- A **live** cell with 2 or 3 live neighbors **survives**; otherwise it **dies**.
- A **dead** cell with exactly 3 live neighbors becomes **alive**; otherwise it stays dead.

This rule is denoted **B3/S23** in the standard "birth/survival" notation.

Despite the simplicity of this rule, the Game of Life exhibits extraordinary complexity:

- **Still lifes**: stable configurations (e.g., the $2 \times 2$ "block", the "beehive").
- **Oscillators**: configurations that cycle through a finite sequence of states (e.g., the "blinker" with period 2, the "pulsar" with period 3).
- **Gliders**: small configurations that translate across the lattice while oscillating. The simplest glider is a 5-cell pattern that moves one cell diagonally every 4 generations.
- **Glider guns**: configurations that periodically emit gliders (discovered by Gosper, 1970).

**Theorem 7.7** (Berlekamp, Conway, Guy, 1982; fully proved via later constructions). *The Game of Life is Turing-complete.*

The proof uses glider guns to construct logic gates (AND, OR, NOT) by arranging glider streams to collide in appropriate ways. From logic gates, one builds arbitrary circuits, and hence a universal Turing machine.

The Game of Life is not surjective (Gardens of Eden exist, as shown by early computer searches) and not injective (many configurations can evolve into the all-dead state).


## 7.13 Connection to Our Framework

Throughout this series, we have studied discrete dynamical systems of the form $(f, x_0)$ where $f: X \to X$ is an iterated map and $x_0 \in X$ is an initial state.

A cellular automaton with a **finite lattice** $\Lambda = \lbrace 0, 1, \ldots, n-1\rbrace $ (with periodic boundary conditions) is exactly such a system:

- The state space is $X = S^n$, a finite set of size $|S|^n$.
- The global map $F: S^n \to S^n$ is our iterated map $f$.
- An initial configuration $c_0 \in S^n$ is our initial state $x_0$.
- The orbit $c_0, F(c_0), F^2(c_0), \ldots$ is a sequence in a finite set, so it is eventually periodic. The transient length and cycle length are the quantities we have studied.

All the tools from the theory of finite dynamical systems apply: functional graphs, cycle structure, fixed points, Garden of Eden configurations (the non-image elements of $F$), and so on.

For ECA on a lattice of $n$ cells with periodic boundary, the state space has $2^n$ configurations. The functional graph of the global map $F$ is a union of $\rho$-shaped components (tails leading into cycles). The Garden of Eden configurations are the roots of the trees -- the configurations with in-degree zero in the functional graph.

**Non-autonomous CA.** If the local rule itself changes at each time step -- say we apply $f_0$ at time 0, $f_1$ at time 1, and so on -- we obtain a **non-autonomous CA**, which is a sequence of maps $F_0, F_1, F_2, \ldots$ composed in order. This corresponds directly to our non-autonomous DDS framework. If the sequence of rules is periodic with period $p$, the long-term dynamics are governed by the composite map $F_{p-1} \circ \cdots \circ F_1 \circ F_0$.


## 7.14 Summary

Cellular automata are a natural and far-reaching class of discrete dynamical systems. Despite their simple definition -- a lattice of cells updated synchronously by a local rule -- they exhibit the full spectrum of dynamical behavior, from trivial convergence to Turing-complete computation. The Curtis-Hedlund-Lyndon theorem embeds CA theory into symbolic dynamics, giving access to powerful topological and algebraic tools. The Garden of Eden theorem reveals deep connections between local injectivity and global surjectivity. And the finite-lattice restriction recovers exactly the iterated maps on finite sets that form the core of our study.


## References

- Bartholdi, L. (2010). *Gardens of Eden and amenability on cellular automata.* Journal of the European Mathematical Society, 12(1), 241--248.
- Berlekamp, E., Conway, J., and Guy, R. (1982). *Winning Ways for Your Mathematical Plays*, Vol. 2. Academic Press.
- Ceccherini-Silberstein, T., Machi, A., and Scarabotti, F. (1999). Amenable groups and cellular automata. Annales de l'Institut Fourier, 49(2), 673--685.
- Cook, M. (2004). Universality in elementary cellular automata. Complex Systems, 15(1), 1--40.
- Hedlund, G. A. (1969). Endomorphisms and automorphisms of the shift dynamical system. Mathematical Systems Theory, 3(4), 320--375.
- Hurd, L. P., Kari, J., and Culik, K. (1992). The topological entropy of cellular automata is uncomputable. Ergodic Theory and Dynamical Systems, 12(2), 255--265.
- Kurka, P. (1997). Languages, equicontinuity and attractors in cellular automata. Ergodic Theory and Dynamical Systems, 17(2), 417--433.
- Kurka, P. (2003). *Topological and Symbolic Dynamics.* Cours Specialises 11, Societe Mathematique de France.
- Lind, D. and Marcus, B. (2021). *An Introduction to Symbolic Dynamics and Coding*, 2nd ed. Cambridge University Press.
- Moore, E. F. (1962). Machine models of self-reproduction. Proceedings of Symposia in Applied Mathematics, 14, 17--33.
- Myhill, J. (1963). The converse of Moore's Garden-of-Eden theorem. Proceedings of the American Mathematical Society, 14(4), 685--686.
- Shereshevsky, M. A. (1993). Expansiveness, entropy and polynomial growth for groups acting on subshifts by automorphisms. Indagationes Mathematicae, 4(2), 203--210.
- Wolfram, S. (1984). Universality and complexity in cellular automata. Physica D, 10(1--2), 1--35.
- Wolfram, S. (2002). *A New Kind of Science.* Wolfram Media.

---

## Recommended Reading

For an accessible introduction:

- **Wolfram (2002)**, *A New Kind of Science*, is polarizing but contains extensive empirical data and beautiful figures. Best used as a source of examples rather than proofs.

- **Schiff, J.** (2008). *Cellular Automata: A Discrete View of the World*. Wiley. Undergraduate-level textbook with clear exposition and many exercises.

For the mathematical foundations:

- **Kurka (2003)** is the definitive mathematical treatment, covering the topological dynamics perspective thoroughly.

- **Lind & Marcus (2021)**, Chapter 1, places CA in the broader context of symbolic dynamics and gives clean proofs of the Curtis-Hedlund-Lyndon theorem.

For universality and computation:

- **Cook (2004)** is the original proof of Rule 110's universality. Technical but important.

- **Ollinger, N.** (2012). "Universalities in cellular automata." In *Handbook of Natural Computing*, Springer. Comprehensive survey of universality results across different CA.

For the Game of Life specifically:

- **Berlekamp, Conway, and Guy (1982)**, *Winning Ways*, Chapter 25, remains the classic exposition of Life's basic structures and logical universality.

- **Adamatzky, A.** (ed.) (2010). *Game of Life Cellular Automata*. Springer. Collection of articles on Life's properties and applications.

For connections to physics and reversible CA:

- **Toffoli, T. and Margolus, N.** (1987). *Cellular Automata Machines*. MIT Press. Pioneering work on using CA for physics simulation, with emphasis on reversible rules.
