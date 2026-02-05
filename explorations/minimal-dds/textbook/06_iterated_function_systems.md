# Chapter 6: Iterated Function Systems

## 6.1 Introduction

An **iterated function system** (IFS) is one of the most elegant constructions in dynamical systems and fractal geometry. The idea is simple: take a finite collection of maps on a space, apply them repeatedly, and ask what sets are invariant under the collective action of all the maps. The resulting theory, initiated by Hutchinson (1981) and popularized by Barnsley (1988), provides a rigorous framework for constructing and analyzing fractals, and connects deeply to probability theory, dimension theory, and—as we shall see—the discrete dynamical systems framework of this text.

## 6.2 Basic Definitions

**Definition 6.1 (Iterated Function System).** Let $(X, d)$ be a complete metric space. An *iterated function system* (IFS) is a finite collection of continuous maps

$$\mathcal{F} = \lbrace f_1, f_2, \ldots, f_k\rbrace $$

where each $f_i : X \to X$.

The system operates by repeatedly choosing one of the maps $f_i$ and applying it. The central question is: what geometric or measure-theoretic structures are invariant under this process?

Before we can answer this, we need the key analytic ingredient.

**Definition 6.2 (Contraction Mapping).** A map $f : X \to X$ on a metric space $(X, d)$ is a *contraction* (or *contraction mapping*) if there exists a constant $0 \le c < 1$ such that

$$d(f(x), f(y)) \le c \cdot d(x, y) \quad \text{for all } x, y \in X.$$

The constant $c$ is called the *contraction ratio* (or *Lipschitz constant*) of $f$. Intuitively, a contraction brings points closer together by at least a factor of $c$ at every step.

The foundational result about contractions is:

**Theorem 6.3 (Banach Fixed-Point Theorem, 1922).** Let $(X, d)$ be a complete metric space and $f : X \to X$ a contraction with ratio $c < 1$. Then:

1. $f$ has a unique fixed point $x^* \in X$, i.e., $f(x^*) = x^*$.
2. For any starting point $x_0 \in X$, the iterates $f^n(x_0) \to x^*$ as $n \to \infty$.
3. The convergence rate is geometric: $d(f^n(x_0), x^*) \le \frac{c^n}{1 - c} \, d(x_0, f(x_0))$.

*Proof sketch.* The sequence $x_n = f^n(x_0)$ is Cauchy because $d(x_{n+1}, x_n) \le c^n \, d(x_1, x_0)$. Completeness gives a limit $x^*$. Continuity of $f$ gives $f(x^*) = x^*$. Uniqueness: if $f(y) = y$ too, then $d(x^*, y) = d(f(x^*), f(y)) \le c \, d(x^*, y)$, which forces $d(x^*, y) = 0$. $\square$

The genius of the IFS construction is to apply the Banach theorem not to individual points, but to *sets*.

## 6.3 The Hutchinson Operator

To study how an IFS acts on sets rather than points, we need a metric on sets.

**Definition 6.4 (Hausdorff Metric).** Let $\mathcal{H}(X)$ denote the collection of all non-empty compact subsets of $(X, d)$. For $A, B \in \mathcal{H}(X)$, define

$$d_H(A, B) = \max\left\lbrace \sup_{a \in A} \inf_{b \in B} d(a, b),\; \sup_{b \in B} \inf_{a \in A} d(a, b)\right\rbrace .$$

This is the *Hausdorff metric*. Informally, $d_H(A, B) \le \epsilon$ means every point of $A$ is within $\epsilon$ of some point of $B$, and vice versa.

**Fact.** If $(X, d)$ is complete, then $(\mathcal{H}(X), d_H)$ is also complete (see Falconer 2003, Ch. 2).

**Definition 6.5 (Hutchinson Operator).** Given an IFS $\mathcal{F} = \lbrace f_1, \ldots, f_k\rbrace $, the *Hutchinson operator* $H : \mathcal{H}(X) \to \mathcal{H}(X)$ is defined by

$$H(A) = \bigcup_{i=1}^{k} f_i(A) = \bigcup_{i=1}^{k} \lbrace f_i(a) : a \in A\rbrace .$$

That is, $H$ applies every map in the IFS to $A$ and takes the union. A set $A$ is *invariant* under the IFS if $H(A) = A$: it can be decomposed into $k$ pieces, each of which is the image of the whole under one of the maps.

## 6.4 Hutchinson's Theorem

The following is the central theorem of IFS theory.

**Theorem 6.6 (Hutchinson, 1981).** Let $(X, d)$ be a complete metric space, and let $\mathcal{F} = \lbrace f_1, \ldots, f_k\rbrace $ be an IFS where each $f_i$ is a contraction with ratio $c_i < 1$. Then:

1. The Hutchinson operator $H$ is a contraction on $(\mathcal{H}(X), d_H)$ with ratio $c = \max_i c_i$.
2. There exists a unique non-empty compact set $A \in \mathcal{H}(X)$ such that $H(A) = A$.
3. For any non-empty compact set $B \in \mathcal{H}(X)$, the iterates $H^n(B) \to A$ in the Hausdorff metric.

The set $A$ is called the **attractor** (or *invariant set*) of the IFS.

*Proof of (1).* Let $A, B \in \mathcal{H}(X)$. For any $a \in A$ and any $i$,

$$\inf_{b \in B} d(f_i(a), f_i(b)) \le c_i \inf_{b \in B} d(a, b).$$

Taking the supremum over $a$ and all $i$, and applying the symmetric argument, yields

$$d_H(H(A), H(B)) \le c \cdot d_H(A, B).$$

Since $c < 1$, $H$ is a contraction. Parts (2) and (3) then follow from the Banach fixed-point theorem applied to $H$ on the complete metric space $(\mathcal{H}(X), d_H)$. $\square$

## 6.5 Classical Examples

### Example 6.7: The Cantor Set

Consider $X = [0, 1]$ with the usual metric, and the IFS

$$f_1(x) = \frac{x}{3}, \qquad f_2(x) = \frac{x}{3} + \frac{2}{3}.$$

Both maps are contractions with ratio $c = 1/3$. The attractor $A$ satisfies

$$A = f_1(A) \cup f_2(A) = \frac{A}{3} \cup \left(\frac{A}{3} + \frac{2}{3}\right).$$

**Worked computation.** Start with $B_0 = [0, 1]$:

- $H(B_0) = [0, 1/3] \cup [2/3, 1] = B_1$ (the first step of the Cantor construction).
- $H(B_1) = [0, 1/9] \cup [2/9, 1/3] \cup [2/3, 7/9] \cup [8/9, 1] = B_2$.
- Continuing, $B_n$ consists of $2^n$ intervals each of length $3^{-n}$.
- The attractor $A = \bigcap_{n=0}^{\infty} B_n$ is the classical **middle-thirds Cantor set**.

The Cantor set is uncountable, has Lebesgue measure zero, and is totally disconnected. Its Hausdorff dimension is $\log 2 / \log 3 \approx 0.631$ (see Section 6.8).

### Example 6.8: The Sierpinski Triangle

Let $X = \mathbb{R}^2$ and fix three vertices of an equilateral triangle, say $p_1 = (0, 0)$, $p_2 = (1, 0)$, $p_3 = (1/2, \sqrt{3}/2)$. Define

$$f_i(x) = \frac{x + p_i}{2}, \qquad i = 1, 2, 3.$$

Each $f_i$ is a contraction with ratio $c = 1/2$. The attractor is the **Sierpinski triangle** (or Sierpinski gasket): the self-similar fractal obtained by repeatedly removing the central triangle from each remaining triangle.

**Worked computation.** Start with $B_0$ = the filled triangle with vertices $p_1, p_2, p_3$:

- $H(B_0)$ consists of three half-scale copies of $B_0$, one anchored at each vertex. The central triangle (with vertices at the midpoints of $B_0$'s edges) is missing.
- $H^2(B_0)$: each of the three sub-triangles has its own central triangle removed, giving $3^2 = 9$ triangles at scale $1/4$.
- At step $n$: $3^n$ triangles at scale $2^{-n}$.
- The attractor $A = \lim_{n \to \infty} H^n(B_0)$ has Hausdorff dimension $\log 3 / \log 2 \approx 1.585$.

### Example 6.9: The Koch Curve

The Koch curve can be described as the attractor of an IFS with four maps on $\mathbb{R}^2$, each a similarity with ratio $c = 1/3$:

$$f_1(x) = \frac{1}{3}x, \qquad f_2(x) = \frac{1}{3}R_{60}(x) + \left(\frac{1}{3}, 0\right),$$
$$f_3(x) = \frac{1}{3}R_{-60}(x) + \left(\frac{1}{2}, \frac{\sqrt{3}}{6}\right), \qquad f_4(x) = \frac{1}{3}x + \left(\frac{2}{3}, 0\right),$$

where $R_\theta$ denotes counterclockwise rotation by $\theta$ degrees. Each map takes the unit interval $[0, 1]$ (embedded in $\mathbb{R}^2$) and maps it to one of the four segments of the Koch generator. The attractor has Hausdorff dimension $\log 4 / \log 3 \approx 1.262$.

## 6.6 The Chaos Game

A remarkable fact about IFS attractors is that they can be generated by a simple stochastic algorithm.

**Algorithm 6.10 (The Chaos Game / Random Iteration Algorithm).**
Given an IFS $\lbrace f_1, \ldots, f_k\rbrace $:

1. Choose an arbitrary starting point $x_0 \in X$.
2. At each step $n$, choose an index $i_n \in \lbrace 1, \ldots, k\rbrace $ uniformly at random (or with specified probabilities).
3. Set $x_{n+1} = f_{i_n}(x_n)$.
4. After discarding a transient (say the first 100 points), the orbit $\lbrace x_n\rbrace $ fills in the attractor $A$.

**Theorem 6.11 (Barnsley & Demko, 1985).** Let $\lbrace f_1, \ldots, f_k\rbrace $ be a contractive IFS on a complete metric space, with probabilities $p_1, \ldots, p_k > 0$ (summing to 1) assigned to the maps. Then for any starting point $x_0$, the empirical distribution of the orbit $\lbrace x_0, x_1, x_2, \ldots\rbrace $ converges almost surely (in the weak topology) to a unique invariant probability measure $\mu$ supported on the attractor $A$.

**Why does this work?** The orbit is a Markov chain on $X$. Because the maps are contractions, the chain "forgets" its initial condition exponentially fast. More precisely, two orbits starting from different points $x_0$ and $y_0$ but driven by the same random sequence of maps satisfy

$$d(x_n, y_n) \le c^n \, d(x_0, y_0) \to 0.$$

This coupling argument shows the stationary measure is unique. The orbit is dense in the support of $\mu$, which is precisely $A$.

**Worked example (Chaos game for the Sierpinski triangle).** Take the three maps from Example 6.8. Start at any point, say $x_0 = (0.5, 0.2)$. At each step, pick one of $f_1, f_2, f_3$ uniformly at random and apply it:

- Step 1: Choose $f_2$. $x_1 = (x_0 + p_2)/2 = (0.75, 0.1)$.
- Step 2: Choose $f_1$. $x_2 = (x_1 + p_1)/2 = (0.375, 0.05)$.
- Step 3: Choose $f_3$. $x_3 = (x_2 + p_3)/2 = (0.4375, 0.4580\ldots)$.

After a few hundred iterations, plotting the points $\lbrace x_n\rbrace $ reveals the Sierpinski triangle. This works regardless of the starting point $x_0$—the first few points may lie outside the attractor, but they rapidly converge to it.

## 6.7 IFS with Probabilities and the Invariant Measure

Assigning probabilities to the maps gives a richer structure than the attractor alone.

**Definition 6.12 (IFS with Probabilities).** An IFS with probabilities is a system $\lbrace (f_1, p_1), \ldots, (f_k, p_k)\rbrace $ where $p_i > 0$ and $\sum_{i=1}^k p_i = 1$. The *transfer operator* (or Markov operator) $M$ acts on probability measures by

$$M(\mu) = \sum_{i=1}^{k} p_i \cdot (f_i)_{*}(\mu),$$

where $(f_i)_{*}(\mu)$ is the pushforward measure: $(f_i)_{*}(\mu)(B) = \mu(f_i^{-1}(B))$.

**Theorem 6.13.** Under the hypotheses of Theorem 6.6, with $p_i > 0$, the operator $M$ has a unique fixed point $\mu^*$—a probability measure satisfying

$$\mu^* = \sum_{i=1}^{k} p_i \cdot (f_i)_{*}(\mu^*).$$

This is the **invariant measure** (or **self-similar measure**) of the IFS. The chaos game orbit converges in distribution to $\mu^*$.

The self-similarity equation says that $\mu^*$ can be decomposed: a fraction $p_i$ of its mass is a scaled copy under $f_i$. Different probability vectors $(p_1, \ldots, p_k)$ produce different measures on the same attractor, concentrating mass on different parts. If all $p_i = 1/k$, the measure is the "most uniform" one on $A$ (though it need not coincide with the Hausdorff measure in the natural dimension).

## 6.8 Hausdorff Dimension of IFS Attractors

For self-similar IFS, there is a clean formula for the fractal dimension.

**Definition 6.14.** An IFS $\lbrace f_1, \ldots, f_k\rbrace $ on $\mathbb{R}^n$ is **self-similar** if each $f_i$ is a similarity: $\|f_i(x) - f_i(y)\| = c_i \|x - y\|$ for some contraction ratio $0 < c_i < 1$.

**Definition 6.15 (Open Set Condition).** The IFS satisfies the *open set condition* (OSC) if there exists a non-empty bounded open set $U \subset \mathbb{R}^n$ such that

$$\bigcup_{i=1}^k f_i(U) \subseteq U \quad \text{and} \quad f_i(U) \cap f_j(U) = \emptyset \text{ for } i \ne j.$$

That is, the images of $U$ under the maps are disjoint and fit inside $U$. This is a controlled-overlap condition ensuring the fractal pieces do not overlap "too much."

**Theorem 6.16 (Moran–Hutchinson).** Let $\lbrace f_1, \ldots, f_k\rbrace $ be a self-similar IFS with contraction ratios $c_1, \ldots, c_k$ satisfying the open set condition. Then the Hausdorff dimension $s$ of the attractor $A$ is the unique solution to the **Moran equation**:

$$\sum_{i=1}^{k} c_i^s = 1.$$

**Worked example.** For the Cantor set (Example 6.7): $k = 2$, $c_1 = c_2 = 1/3$. The Moran equation is

$$2 \cdot (1/3)^s = 1 \implies (1/3)^s = 1/2 \implies s = \frac{\log 2}{\log 3} \approx 0.6309.$$

For the Sierpinski triangle (Example 6.8): $k = 3$, $c_i = 1/2$. Then $3 \cdot (1/2)^s = 1$, giving $s = \log 3 / \log 2 \approx 1.5850$.

For the Koch curve (Example 6.9): $k = 4$, $c_i = 1/3$. Then $4 \cdot (1/3)^s = 1$, giving $s = \log 4 / \log 3 \approx 1.2619$.

When the open set condition fails (excessive overlap), the Hausdorff dimension may be strictly less than the similarity dimension given by the Moran equation. Determining the dimension in such cases is generally difficult.

## 6.9 IFS on Finite and Discrete Sets

On a finite set $X$ with $|X| = n$, every map $f : X \to X$ satisfies $d(f(x), f(y)) \le d(x, y)$ trivially for any discrete metric $d(x, y) = \mathbf{1}[x \ne y]$, but strict contraction ($c < 1$) would require $f$ to be constant. Thus the metric theory of IFS does not directly apply to finite sets—every non-constant map has contraction ratio 1 in the discrete metric.

Instead, the natural objects of study are:

1. **The semigroup** $\langle f_1, \ldots, f_k \rangle$ generated by the maps under composition. For $|X| = n$, this is a sub-semigroup of the full transformation semigroup $T_n$ (which has $n^n$ elements). The size and structure of this semigroup characterize the reachability and complexity of the IFS.

2. **The functional graph** of random iteration. Fix a probability vector $(p_1, \ldots, p_k)$. The state space of the random process is $X$. The transition matrix is

$$P(x, y) = \sum_{i : f_i(x) = y} p_i.$$

This is a Markov chain on $X$. Its stationary distributions, mixing times, and absorbing states are the finite analogues of the invariant measure and attractor.

3. **Eventual periodicity.** Every orbit of a single map on a finite set is eventually periodic (it must enter a cycle). For an IFS with random map selection, the system is a Markov chain and (if irreducible) has a unique stationary distribution. If not irreducible, it decomposes into communicating classes—the analogue of the attractor's connected components.

**Example 6.17.** Let $X = \lbrace 0, 1, 2\rbrace $ and consider the IFS $\lbrace f_1, f_2\rbrace $ where $f_1 = (0, 0, 1)$ and $f_2 = (1, 2, 2)$ (function tables). The semigroup generated by $f_1, f_2$ under composition includes:

- $f_1 \circ f_1 = (0, 0, 0)$ (constant map to 0)
- $f_2 \circ f_2 = (2, 2, 2)$ (constant map to 2)
- $f_1 \circ f_2 = (0, 1, 1)$
- $f_2 \circ f_1 = (1, 1, 2)$

The semigroup eventually includes all compositions; its structure reveals which states are reachable from which, under which sequences of map applications.

## 6.10 Recurrent IFS

Barnsley, Elton, Hardin, and Massopust (1989) introduced a generalization where the choice of map at each step depends on which map was applied in the previous step.

**Definition 6.18 (Recurrent IFS).** A *recurrent IFS* consists of:

- Maps $\lbrace f_1, \ldots, f_k\rbrace $ on $(X, d)$.
- A $k \times k$ transition matrix $T = (t_{ij})$ where $t_{ij} \ge 0$ and $\sum_j t_{ij} = 1$.

The joint state at time $n$ is $(i_n, x_n)$ where $i_n$ is the index of the map just applied. The dynamics are:

1. Given $(i_n, x_n)$, choose $i_{n+1}$ according to the distribution $(t_{i_n, 1}, \ldots, t_{i_n, k})$.
2. Set $x_{n+1} = f_{i_{n+1}}(x_n)$.

This is a Markov chain on $\lbrace 1, \ldots, k\rbrace  \times X$. By restricting which maps can follow which (setting some $t_{ij} = 0$), one obtains attractors that are strict subsets of the standard IFS attractor—only "allowed" compositions contribute.

Recurrent IFS can produce attractors with different connectivity or topology than the standard IFS, and they model situations where the rule for updating depends on context.

## 6.11 The Collage Theorem

A natural inverse problem: given a target shape $T$, find an IFS whose attractor approximates $T$.

**Theorem 6.19 (Collage Theorem; Barnsley 1988).** Let $\lbrace f_1, \ldots, f_k\rbrace $ be a contractive IFS with ratio $c = \max_i c_i < 1$ and attractor $A$. For any non-empty compact set $T \in \mathcal{H}(X)$,

$$d_H(T, A) \le \frac{1}{1 - c} \, d_H(T, H(T)).$$

**Interpretation.** To find an IFS whose attractor is close to $T$, it suffices to find maps such that $H(T) = \bigcup f_i(T)$ is close to $T$ (the "collage" of the pieces approximates the original). The theorem bounds the attractor's distance to $T$ in terms of the collage distance, amplified by $1/(1-c)$.

This is the theoretical basis for **fractal image compression** (Barnsley 1988; Jacquin 1992): encode an image by an IFS whose attractor approximates it. The IFS description (a few maps with their parameters) can be far more compact than the pixel data.

## 6.12 Connection to the (f, x) Framework

The framework developed in earlier chapters studies systems with state $(f, x)$ where $f : X \to X$ and $x \in X$, evolving under a meta-rule $\phi$ that updates the function at each step:

$$(f, x) \mapsto (\phi(f, x), \, f(x)).$$

An IFS is the special case where the "function" component is not updated by a deterministic meta-rule but rather *selected* from a fixed repertoire $\lbrace f_1, \ldots, f_k\rbrace $ at each step, either randomly or according to some schedule. That is, we can view the IFS dynamics as a sequence of states

$$(f_{i_0}, x_0) \to (f_{i_1}, x_1) \to (f_{i_2}, x_2) \to \cdots$$

where $x_{n+1} = f_{i_n}(x_n)$ and the sequence $i_0, i_1, i_2, \ldots$ is determined by:

- **Random IFS**: $i_n$ drawn i.i.d. or as a Markov chain (recurrent IFS).
- **Deterministic schedule**: $i_n = \sigma(n)$ for some fixed sequence $\sigma$, e.g., cyclic application $f_1, f_2, f_1, f_2, \ldots$.
- **State-dependent selection**: $i_n = g(x_n)$ for some selector function $g : X \to \lbrace 1, \ldots, k\rbrace $, making the choice of map depend on the current point. This is a meta-rule: $\phi(f, x) = f_{g(x)}$.

In the discrete (finite $X$) setting, the multi-map system $\lbrace f_1, \ldots, f_k\rbrace $ acting on $X$ generates a semigroup of transformations. The functional graph of the random iteration is a Markov chain whose structure (communicating classes, absorbing sets, stationary distributions) parallels the attractor and invariant measure of the classical theory. The meta-rule $\phi$ that selects which map to apply is the mechanism that ties IFS to the broader framework: **multiple agents (maps) acting on a shared state, with a protocol (meta-rule) governing which agent acts when**.

## 6.13 Summary

| Concept | Continuous setting | Finite/discrete setting |
|---|---|---|
| Maps | Contractions on $(X, d)$ | Arbitrary maps $X \to X$ |
| Invariant object | Attractor $A = H(A)$ | Absorbing sets, recurrent classes |
| Convergence | $H^n(B) \to A$ (Hausdorff) | Markov chain mixing |
| Measure | Invariant measure $\mu^*$ | Stationary distribution $\pi$ |
| Dimension | Hausdorff dim via Moran eq. | Not applicable (dim = 0) |
| Meta-rule | Map selection protocol | $\phi(f, x) = f_{g(x)}$ |

The IFS framework transforms the study of single-map iteration into the far richer study of multi-map interaction. In the continuous setting this yields fractal geometry; in the discrete setting it yields semigroup theory and Markov chains. Both are instances of the general $(f, x)$ dynamical system with a non-trivial meta-rule.

## References

- Banach, S. (1922). Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales. *Fundamenta Mathematicae*, 3, 133–181.
- Barnsley, M. F. (1988). *Fractals Everywhere*. Academic Press. (2nd edition 1993, 3rd edition 2012.)
- Barnsley, M. F. & Demko, S. (1985). Iterated function systems and the global construction of fractals. *Proceedings of the Royal Society of London A*, 399, 243–275.
- Barnsley, M. F., Elton, J. H., Hardin, D. P., & Massopust, P. R. (1989). Hidden variable fractal interpolation functions. *SIAM Journal on Mathematical Analysis*, 20(5), 1218–1242.
- Falconer, K. (2003). *Fractal Geometry: Mathematical Foundations and Applications* (2nd ed.). Wiley.
- Hutchinson, J. E. (1981). Fractals and self-similarity. *Indiana University Mathematics Journal*, 30(5), 713–747.
- Jacquin, A. E. (1992). Image coding based on a fractal theory of iterated contractive image transformations. *IEEE Transactions on Image Processing*, 1(1), 18–30.
- Moran, P. A. P. (1946). Additive functions of intervals and Hausdorff measure. *Mathematical Proceedings of the Cambridge Philosophical Society*, 42(1), 15–23.
