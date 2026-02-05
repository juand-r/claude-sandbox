# Chapter 1: Iterated Maps on Finite Sets

## 1.1 Introduction

Many systems in mathematics and computer science evolve by the repeated application of a fixed rule. A cellular automaton updates its cells according to a local rule; a hash function chains outputs back as inputs; a pseudorandom number generator feeds its output into itself. The simplest abstraction that captures all of these is the **iterated map on a finite set**: given a finite set $X$ and a function $f: X \to X$, we study the sequence $x, f(x), f(f(x)), \ldots$ obtained by repeatedly applying $f$.

Despite the simplicity of this setup, a surprisingly rich theory emerges. Every orbit must eventually cycle. The global structure of the map decomposes into a forest of trees hanging off disjoint cycles. The statistics of random maps connect to the birthday paradox and to the analysis of algorithms. This chapter develops the core theory from scratch.

## 1.2 Basic Definitions

**Definition 1.1 (Discrete Dynamical System).** A *discrete dynamical system* (DDS) on a finite set is a pair $(X, f)$ where $X$ is a finite set and $f: X \to X$ is a function. The *state space* is $X$ and $f$ is the *transition map* (or simply the *map*).

Given an initial state $x_0 \in X$, the system evolves deterministically:

$$x_0, \quad x_1 = f(x_0), \quad x_2 = f(x_1) = f^2(x_0), \quad x_3 = f^3(x_0), \quad \ldots$$

where $f^k$ denotes the $k$-fold composition of $f$ with itself, and $f^0$ is the identity.

**Definition 1.2 (Orbit).** The *orbit* (or *trajectory*) of a point $x_0 \in X$ under $f$ is the sequence

$$\mathcal{O}(x_0) = (x_0, f(x_0), f^2(x_0), \ldots).$$

Since $X$ is finite, this sequence must eventually revisit a state.

**Definition 1.3 (Fixed Points and Periodic Points).**
- A point $x \in X$ is a *fixed point* of $f$ if $f(x) = x$.
- A point $x$ is a *periodic point* of period $k$ if $f^k(x) = x$ and $k \geq 1$ is the smallest such integer. We also say $x$ belongs to a *$k$-cycle*. A fixed point is periodic with period 1.
- A point $x$ is *eventually periodic* if there exist integers $t \geq 0$ and $k \geq 1$ such that $f^{t+k}(x) = f^t(x)$. The smallest such $t$ is the *transient length* (or *tail length*) and the smallest such $k$ is the *cycle length*.

**Proposition 1.4.** Every point in a finite DDS is eventually periodic.

*Proof.* Let $|X| = n$. The sequence $x_0, f(x_0), \ldots, f^n(x_0)$ contains $n+1$ elements drawn from a set of size $n$. By the pigeonhole principle, there exist indices $0 \leq i < j \leq n$ with $f^i(x_0) = f^j(x_0)$. Setting $t = i$ and $k = j - i$, we have $f^{t+k}(x_0) = f^t(x_0)$. $\square$

## 1.3 The Functional Graph

**Definition 1.5 (Functional Graph).** The *functional graph* of a map $f: X \to X$ is the directed graph $G_f = (X, E)$ where the edge set is $E = \lbrace (x, f(x)) : x \in X\rbrace $. Every vertex has out-degree exactly 1.

This is the central combinatorial object of this chapter. A directed graph in which every vertex has out-degree exactly 1 is sometimes called a *functional digraph* or *1-regular digraph*. The structure of such graphs is completely determined by the following theorem.

**Theorem 1.6 (Structure Theorem for Functional Graphs).** Let $G_f$ be the functional graph of $f: X \to X$ where $X$ is finite. Then every weakly connected component of $G_f$ consists of a single directed cycle with directed trees (arborescences) rooted at the cycle nodes, with edges directed toward the roots. Equivalently, every connected component has the shape of the Greek letter $\rho$: a "tail" path leading into a cycle.

*Proof.* Let $C$ be a weakly connected component of $G_f$. We prove the structure in two steps.

**Step 1: Every component contains exactly one cycle.** Consider any vertex $v$ in $C$. The sequence $v, f(v), f^2(v), \ldots$ must eventually repeat (Proposition 1.4), so it enters a cycle. Thus $C$ contains at least one cycle. Suppose $C$ contains two distinct cycles $\gamma_1$ and $\gamma_2$. Since $C$ is weakly connected, there is an undirected path between some $u_1 \in \gamma_1$ and $u_2 \in \gamma_2$. But every vertex on a cycle has its successor on the same cycle (since cycles are invariant under $f$), and every vertex not on a cycle has a unique successor that is one step closer to a cycle. Following the forward orbit of any vertex in $C$ must lead to a single cycle. If there were two cycles, some vertex would need to have out-degree 2 (its orbit would need to "choose" which cycle to join), which contradicts the fact that $f$ is a function. Hence there is exactly one cycle per component.

**Step 2: The non-cycle vertices form a forest of trees rooted at cycle nodes.** Let $\gamma$ be the unique cycle in $C$. Remove the edges of $\gamma$. The remaining graph restricted to non-cycle vertices has out-degree 1 everywhere except at cycle nodes (which are now roots), and no cycles. A directed graph with out-degree $\leq 1$ and no cycles is a forest of rooted directed trees. The edge directions point toward the roots (cycle vertices), since iterating $f$ from any non-cycle vertex eventually reaches the cycle. $\square$

**Remark.** The "$\rho$ shape" terminology comes from the visual resemblance: starting from a tail vertex, the orbit traces a path (the stroke of $\rho$) that enters a loop (the bowl of $\rho$). The transient length of a vertex $x$ is the distance from $x$ to the cycle, and the cycle length is the length of that cycle. The *rho length* of a vertex is the sum $\lambda(x) = t(x) + c(x)$, where $t(x)$ is the transient length and $c(x)$ the cycle length.

## 1.4 Worked Examples

### Example 1.7: $f(x) = x^2 \bmod 10$

Let $X = \lbrace 0, 1, 2, \ldots, 9\rbrace $ and $f(x) = x^2 \bmod 10$. We compute the function table:

| $x$    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|--------|---|---|---|---|---|---|---|---|---|---|
| $f(x)$ | 0 | 1 | 4 | 9 | 6 | 5 | 6 | 9 | 4 | 1 |

Now we trace orbits:
- $0 \to 0$. Fixed point. Transient 0, cycle length 1.
- $1 \to 1$. Fixed point.
- $2 \to 4 \to 6 \to 6$. Transient 2, cycle length 1 (6 is a fixed point).
- $3 \to 9 \to 1 \to 1$. Transient 2, cycle length 1.
- $4 \to 6 \to 6$. Transient 1, cycle length 1.
- $5 \to 5$. Fixed point.
- $6 \to 6$. Fixed point.
- $7 \to 9 \to 1 \to 1$. Transient 2, cycle length 1.
- $8 \to 4 \to 6 \to 6$. Transient 2, cycle length 1.
- $9 \to 1 \to 1$. Transient 1, cycle length 1.

The functional graph has four fixed points: $\lbrace 0, 1, 5, 6\rbrace $. No non-trivial cycles exist. The maximum transient length is 2 (attained by $\lbrace 2, 3, 7, 8\rbrace $). The graph has four connected components: $\lbrace 0\rbrace $, $\lbrace 3, 7, 9, 1\rbrace $, $\lbrace 2, 8, 4, 6\rbrace $, and $\lbrace 5\rbrace $. Each conforms to the $\rho$-structure theorem (with trivial cycles of length 1).

### Example 1.8: $f(x) = 2x \bmod 11$

Let $X = \lbrace 0, 1, \ldots, 10\rbrace $ and $f(x) = 2x \bmod 11$. Since $\gcd(2, 11) = 1$, $f$ is a bijection (a permutation) on $X$. We compute:

| $x$    | 0 | 1 | 2 | 3 | 4 | 5 | 6  | 7 | 8 | 9 | 10 |
|--------|---|---|---|---|---|---|----|---|---|---|----|
| $f(x)$ | 0 | 2 | 4 | 6 | 8 | 10| 1  | 3 | 5 | 7 | 9  |

Tracing orbits:
- $0 \to 0$. Fixed point.
- $1 \to 2 \to 4 \to 8 \to 5 \to 10 \to 9 \to 7 \to 3 \to 6 \to 1$. This is a cycle of length 10.

Since $f$ is a permutation, every point is periodic (transient length 0 for all vertices). The cycle structure is: one fixed point at 0, one 10-cycle containing $\lbrace 1, 2, \ldots, 10\rbrace $. The order of 2 in the multiplicative group $(\mathbb{Z}/11\mathbb{Z})^*$ is 10, confirming that 2 is a primitive root modulo 11.

In general, when $f$ is a permutation, the functional graph consists entirely of disjoint cycles with no tails. This is the special case addressed by classical permutation theory.

### Example 1.9: $f(x) = 2x \bmod 12$

Let $X = \lbrace 0, 1, \ldots, 11\rbrace $ and $f(x) = 2x \bmod 12$. Now $\gcd(2, 12) = 2 \neq 1$, so $f$ is not a bijection.

| $x$    | 0 | 1 | 2 | 3 | 4 | 5 | 6  | 7 | 8  | 9 | 10 | 11 |
|--------|---|---|---|---|---|---|----|---|----|---|----|----|
| $f(x)$ | 0 | 2 | 4 | 6 | 8 | 10| 0  | 2 | 4  | 6 | 8  | 10 |

Tracing:
- $0 \to 0$. Fixed point.
- $1 \to 2 \to 4 \to 8 \to 4$. Transient 2, cycle $\lbrace 4, 8\rbrace $ of length 2.
- $3 \to 6 \to 0 \to 0$. Transient 2, cycle length 1.
- $5 \to 10 \to 8 \to 4 \to 8$. Transient 2, cycle $\lbrace 4, 8\rbrace $ of length 2.
- $7 \to 2 \to 4 \to 8 \to 4$. Transient 2, cycle $\lbrace 4, 8\rbrace $ of length 2.
- $9 \to 6 \to 0 \to 0$. Transient 2, cycle length 1.
- $11 \to 10 \to 8 \to 4 \to 8$. Transient 2, cycle $\lbrace 4, 8\rbrace $ of length 2.

This map has two connected components. One is rooted at the fixed point $0$ (with $3, 6, 9$ as tail nodes). The other contains the 2-cycle $\lbrace 4, 8\rbrace $ (with $1, 2, 5, 7, 10, 11$ as tail nodes). The $\rho$-shape is evident: every orbit has a tail of length 1 or 2 leading into a cycle of length 1 or 2.

## 1.5 Counting Functions and Permutations

We now turn to enumerative questions. Let $X = \lbrace 0, 1, \ldots, n-1\rbrace $.

**Proposition 1.10 (Total count).** The number of functions $f: X \to X$ is $n^n$, since each of the $n$ elements of $X$ can be mapped to any of $n$ elements independently.

**Proposition 1.11 (Permutations).** The number of bijections $f: X \to X$ is $n!$. The ratio $n!/n^n$ (the probability that a uniformly random function is a bijection) tends to 0 rapidly: by Stirling's approximation, $n!/n^n \sim \sqrt{2\pi n}\, e^{-n}$.

**Proposition 1.12 (Functions with exactly $k$ fixed points).** The number of functions $f: X \to X$ with exactly $k$ fixed points is

$$\binom{n}{k}(n-1)^{n-k}.$$

*Proof.* Choose the $k$ fixed points in $\binom{n}{k}$ ways. Each of the remaining $n - k$ elements must map to some element other than itself, giving $n - 1$ choices per non-fixed element (it may map to any element of $X$ except itself, including other non-fixed elements). Hence the total is $\binom{n}{k}(n-1)^{n-k}$. $\square$

**Remark.** Setting $k = 0$: the number of fixed-point-free functions is $(n-1)^n$. This is not the same as the number of *derangements* $D_n = n!\sum_{i=0}^{n}(-1)^i/i!$, which counts fixed-point-free *permutations*. The formula $\binom{n}{k}(n-1)^{n-k}$ counts all functions (not just bijections) with exactly $k$ fixed points.

**Example 1.13.** For $n = 3$: there are $3^3 = 27$ total functions. Functions with exactly 0 fixed points: $\binom{3}{0} \cdot 2^3 = 8$. With exactly 1: $\binom{3}{1} \cdot 2^2 = 12$. With exactly 2: $\binom{3}{2} \cdot 2^1 = 6$. With exactly 3 (the identity): $\binom{3}{3} \cdot 2^0 = 1$. Total: $8 + 12 + 6 + 1 = 27$. Check.

## 1.6 Transient Length, Cycle Length, and Rho Length

For a point $x$ in a DDS $(X, f)$, we define:

- **Transient length** $\tau(x)$: the smallest $t \geq 0$ such that $f^t(x)$ is periodic.
- **Cycle length** $\lambda(x)$: the period of the periodic point $f^{\tau(x)}(x)$; equivalently, the smallest $k \geq 1$ such that $f^{\tau(x)+k}(x) = f^{\tau(x)}(x)$.
- **Rho length** $\rho(x) = \tau(x) + \lambda(x)$: the total number of distinct points in the orbit of $x$.

Note that $\rho(x) = |\mathcal{O}(x)|$, the number of distinct elements visited by the orbit.

**Algorithm (Floyd's cycle detection).** Given only the ability to evaluate $f$, one can determine $\tau(x)$ and $\lambda(x)$ using $O(1)$ memory and $O(\tau + \lambda)$ evaluations of $f$, via Floyd's "tortoise and hare" algorithm (Floyd, 1967). This is often used in Pollard's rho factoring algorithm, which derives its name from the $\rho$-shaped orbits of iterated maps.

## 1.7 Product Systems

Given two DDS $(X_1, f_1)$ and $(X_2, f_2)$, the **product system** is $(X_1 \times X_2, f_1 \times f_2)$ where $(f_1 \times f_2)(x_1, x_2) = (f_1(x_1), f_2(x_2))$. The orbit of $(x_1, x_2)$ in the product is determined component-wise: the cycle length of $(x_1, x_2)$ is $\text{lcm}(\lambda(x_1), \lambda(x_2))$ and the transient length is $\max(\tau(x_1), \tau(x_2))$.

More generally, one can consider *coupled* product systems where the components interact:

$$F(x_1, x_2) = (g_1(x_1, x_2), g_2(x_1, x_2)).$$

These are no longer decomposable and can exhibit qualitatively richer dynamics.

A particularly important coupled product system is the **(f, x) framework** studied in subsequent chapters: the state space is $F \times X$ where $F = X^X$ is the set of all maps on $X$, and the transition is

$$(f, x) \longmapsto (\varphi(f, x),\ f(x))$$

where $\varphi: F \times X \to F$ is a "meta-rule" that updates the function itself. When $\varphi$ is the identity (i.e., $\varphi(f,x) = f$ for all $f, x$), this reduces to ordinary iteration of $f$. When $\varphi$ is non-trivial, the system rewrites its own transition rule at each step--a form of self-modification. This product system is itself a DDS on the set $F \times X$ of size $n^n \cdot n = n^{n+1}$, and all the theory of this chapter applies to it. However, the structure of its functional graph can be far more complex than that of a single map $f$.

## 1.8 Random Maps

Perhaps the most remarkable aspect of iterated maps on finite sets is what happens when $f$ is chosen uniformly at random from all $n^n$ functions $X \to X$. The connection to the *birthday problem* is immediate: iterating a random map is analogous to drawing values from $\lbrace 0, \ldots, n-1\rbrace $ where collisions (revisiting a state) are governed by the same probabilistic mechanism.

The foundational results are due to Harris (1960), Mutafchiev (1988), and especially the landmark paper of Flajolet and Odlyzko (1990), who used analytic combinatorics (singularity analysis of generating functions) to derive precise asymptotics for virtually all parameters of random functional graphs.

**Theorem 1.14 (Flajolet & Odlyzko, 1990).** Let $f: X \to X$ be a function chosen uniformly at random from all $n^n$ functions, and let $x \in X$ be a uniformly random starting point. Then:

- The expected tail length is $E[\tau] \sim \sqrt{\pi n / 8} \approx 0.6267\sqrt{n}$.
- The expected cycle length is $E[\lambda] \sim \sqrt{\pi n / 8} \approx 0.6267\sqrt{n}$.
- The expected rho length is $E[\rho] \sim \sqrt{\pi n / 2} \approx 1.2533\sqrt{n}$.

More precisely, Flajolet and Odlyzko prove that if $T_n$ is the tail length of a random point in a random map of size $n$, then

$$E[T_n] = \sqrt{\frac{\pi n}{8}}\left(1 + O\left(\frac{1}{\sqrt{n}}\right)\right).$$

The cycle length has the same asymptotic expectation, $E[\Lambda_n] \sim \sqrt{\pi n / 8}$, but note that this is a different random variable. The rho length $\rho = \tau + \lambda$ has expectation $\sim \sqrt{\pi n/2}$.

**Birthday paradox connection.** The expected rho length $\sqrt{\pi n / 2}$ is exactly the birthday paradox threshold: the expected number of independent uniform draws from $\lbrace 1, \ldots, n\rbrace $ before a collision is $\sqrt{\pi n / 2}$. This is not a coincidence. The orbit of a random map behaves, until it first revisits a state, as a sequence of independent uniform draws (since $f$ was chosen randomly and the orbit has not yet "explored" any previously-seen value of $f$). The first collision ends the tail and initiates the cycle.

**Further statistics.** Flajolet and Odlyzko also establish:
- The expected number of connected components of a random functional graph is $\sim \frac{1}{2}\ln n$.
- The expected number of cyclic points (points lying on a cycle) is $\sim \sqrt{\pi n / 2}$.
- The expected size of the largest tree is $\sim c \cdot n$ for an explicit constant $c$.

These results are obtained by encoding functional graphs as labeled combinatorial structures, writing down their exponential generating functions, and extracting asymptotics via transfer theorems from analytic combinatorics.

## 1.9 Collatz-like Maps on Finite Rings

The Collatz map on $\mathbb{N}$ (send $x$ to $x/2$ if even, $3x+1$ if odd) can be studied modulo $n$ to yield a finite DDS. Define $f: \mathbb{Z}/n\mathbb{Z} \to \mathbb{Z}/n\mathbb{Z}$ by:

$$f(x) = \begin{cases} x/2 \pmod{n} & \text{if } x \text{ is even,} \\ 3x + 1 \pmod{n} & \text{if } x \text{ is odd.} \end{cases}$$

Here "even" and "odd" refer to the residue class of $x$, and $x/2 \bmod n$ requires that $n$ be odd (so that 2 is invertible mod $n$), or a suitable convention when $n$ is even. These finite Collatz-like maps provide test beds for studying the interaction of arithmetic structure with dynamical structure.

**Example 1.15.** Consider the Collatz map modulo $n = 7$. Since 7 is odd, $2^{-1} \equiv 4 \pmod{7}$, so $x/2 \equiv 4x \pmod{7}$ when $x$ is even.

| $x$    | 0 | 1  | 2 | 3  | 4 | 5  | 6 |
|--------|---|----|---|----|---|----|---|
| parity | E | O  | E | O  | E | O  | E |
| $f(x)$ | 0 | 4  | 1 | 3  | 2 | 2  | 3 |

Orbits:
- $0 \to 0$. Fixed point.
- $1 \to 4 \to 2 \to 1$. Cycle of length 3.
- $3 \to 3$. Fixed point.
- $5 \to 2 \to 1 \to 4 \to 2$. Transient 1, cycle $\lbrace 1, 2, 4\rbrace $ of length 3.
- $6 \to 3$. Transient 1, cycle length 1.

The functional graph has three components: $\lbrace 0\rbrace $, $\lbrace 3, 6\rbrace $ (with 6 a tail node), and $\lbrace 1, 2, 4, 5\rbrace $ (cycle $\lbrace 1,2,4\rbrace $ with 5 as a tail node).

## 1.10 Connection to the $(f, x) \to (\varphi(f,x), f(x))$ Framework

The theory of this chapter--orbits, cycles, transients, functional graphs, the $\rho$-structure theorem, and random map statistics--applies directly to the product system $(f, x) \mapsto (\varphi(f,x), f(x))$ on $F \times X$. This system is simply a DDS on the larger state space $F \times X$, with $|F \times X| = n^{n+1}$.

However, the structure of the functional graph depends sensitively on the meta-rule $\varphi$:

- **Identity meta-rule** ($\varphi(f,x) = f$): The $F$-component is constant along each orbit; the system decomposes into $|F| = n^n$ independent copies of the DDS $(X, f)$, one for each $f$. The functional graph is a disjoint union of functional graphs of individual maps.

- **Non-trivial meta-rules**: The function $f$ mutates along the orbit. The orbit in the full space $F \times X$ can visit many different functions before cycling. This breaks the product structure and can produce dramatically longer transients, larger cycles, and richer graph topology than any single map on $X$.

The random map statistics of Section 1.8 provide a baseline: if $\varphi$ and the initial state are "generic" in some sense, the expected transient and cycle lengths on $F \times X$ should scale as $\sqrt{\pi \cdot n^{n+1}/2}$, which grows super-exponentially in $n$. In practice, structured meta-rules produce dynamics far from this generic case, and understanding which meta-rules produce which dynamical signatures is a central question.

## 1.11 Summary

The key takeaways of this chapter are:

1. A DDS on a finite set is determined by a single function $f: X \to X$.
2. Every orbit is eventually periodic (Proposition 1.4).
3. The functional graph has a canonical decomposition: each connected component is a cycle with trees hanging off it (Theorem 1.6).
4. There are $n^n$ functions on an $n$-element set, $n!$ permutations, and $\binom{n}{k}(n-1)^{n-k}$ functions with exactly $k$ fixed points.
5. For random maps, the expected tail and cycle lengths both scale as $\sqrt{\pi n/8}$, and the expected rho length scales as $\sqrt{\pi n/2}$, intimately connected to the birthday paradox.
6. All of this applies to the product system $(f, x) \mapsto (\varphi(f,x), f(x))$ on $F \times X$, which is itself a DDS on a larger state space.

---

## References

- Flajolet, P. and Odlyzko, A. M. (1990). "Random Mapping Statistics." *Advances in Cryptology -- EUROCRYPT '89*, Lecture Notes in Computer Science, vol. 434, pp. 329--354. Springer. The foundational paper on the asymptotic analysis of random functional graphs using analytic combinatorics.

- Harris, B. (1960). "Probability Distributions Related to Random Mappings." *Annals of Mathematical Statistics*, 31(4), pp. 1045--1062. Early probabilistic results on random mappings, including component counts and tree sizes.

- Mutafchiev, L. (1988). "Large Trees in Random Mappings." *European Journal of Combinatorics*, 9(5), pp. 493--504. Asymptotic results on the largest tree component in random functional graphs.

- Flajolet, P. and Sedgewick, R. (2009). *Analytic Combinatorics*. Cambridge University Press. Chapters II and VIII provide the general framework (symbolic method, singularity analysis) underlying the random mapping results.

- Stanley, R. P. (2012). *Enumerative Combinatorics*, Volume 1, 2nd edition. Cambridge University Press. Standard reference for counting functions, permutations, and related combinatorial objects.

- Knuth, D. E. (1998). *The Art of Computer Programming*, Volume 2: *Seminumerical Algorithms*, 3rd edition. Addison-Wesley. Section 3.1 discusses random number generation via iterated maps; Exercise 3.1-12 treats the birthday paradox connection.

- Floyd, R. W. (1967). "Nondeterministic Algorithms." *Journal of the ACM*, 14(4), pp. 636--644. (Note: Floyd's cycle-detection algorithm is often attributed to this paper, though the algorithm appears in unpublished form and in Knuth's TAOCP.)
