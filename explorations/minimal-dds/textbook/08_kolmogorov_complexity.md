# Chapter 8: Kolmogorov Complexity and Algorithmic Information Theory

## 8.1 Motivation: Information Content of Individual Objects

Shannon's information theory (1948) measures the information content of a *source*—a random variable or stochastic process. It tells us, for instance, that a fair coin produces one bit of information per toss on average. But it says nothing about a specific, concrete string like

$$x = 01010101010101010101$$

versus

$$y = 10110100011010001101$$

Shannon entropy is a property of *ensembles*, not individual objects. Yet intuitively, $x$ is "simpler" than $y$: the first has an obvious pattern, the second does not. We need a theory that assigns an information content to *each individual object*.

This is exactly what Kolmogorov complexity provides. Independently developed by Solomonoff (1964), Kolmogorov (1965), and Chaitin (1966), it defines the complexity of a finite object as the length of its shortest effective description. The key insight is that "description" means "program": the complexity of a string is the length of the shortest program that produces it.

---

## 8.2 Definition

Fix a universal Turing machine $U$. For a finite binary string $x \in \{0,1\}^*$, the **Kolmogorov complexity** of $x$ (with respect to $U$) is

$$K_U(x) = \min\{|p| : U(p) = x\}$$

where the minimum is over all binary programs $p$ such that $U$ on input $p$ halts and outputs $x$, and $|p|$ denotes the length of $p$ in bits.

If no such $p$ exists, we set $K_U(x) = \infty$, but since $U$ is universal, every computable function is representable, and every finite string is trivially computable (by a program that simply contains it as a literal), so $K_U(x)$ is always finite.

**Remark.** The definition depends on the choice of $U$. The next theorem shows this dependence is benign.

---

## 8.3 The Invariance Theorem

**Theorem 8.1 (Invariance Theorem, Kolmogorov 1965).** *For any two universal Turing machines $U_1$ and $U_2$, there exists a constant $c$ (depending on $U_1$ and $U_2$ but not on $x$) such that for all $x$:*

$$|K_{U_1}(x) - K_{U_2}(x)| \leq c.$$

*Proof sketch.* Since $U_1$ is universal, there exists a program $s_{21}$ (a "compiler" or "interpreter") such that for all $p$, $U_1(s_{21} \cdot p) = U_2(p)$, where $\cdot$ denotes concatenation. Then if $p^*$ is a shortest program for $x$ on $U_2$, the program $s_{21} \cdot p^*$ produces $x$ on $U_1$. Therefore

$$K_{U_1}(x) \leq |s_{21}| + K_{U_2}(x).$$

By symmetry, $K_{U_2}(x) \leq |s_{12}| + K_{U_1}(x)$, so taking $c = \max(|s_{12}|, |s_{21}|)$ gives the result. $\square$

The invariance theorem justifies writing $K(x)$ without specifying $U$, with the understanding that all statements hold "up to an additive constant $O(1)$." We adopt this convention henceforth.

---

## 8.4 Basic Properties

**Proposition 8.2.** *For all $x \in \{0,1\}^n$:*

$$K(x) \leq n + c$$

*for a constant $c$ independent of $x$.*

*Proof.* Consider the program "print the following $n$ bits: $x$." This program has length $n$ plus a fixed overhead $c$ for encoding the instruction and the length $n$ itself. $\square$

**Proposition 8.3.** *$K_{\text{prefix}}(x) \leq K(x) + O(\log |x|)$.* (More precisely, the prefix-free (self-delimiting) complexity exceeds the plain complexity by at most $O(\log n)$ bits, since the length $n$ can be encoded in $\lceil \log_2 n \rceil + O(\log \log n)$ bits.)

**Theorem 8.4 (Non-computability).** *The function $K : \{0,1\}^* \to \mathbb{N}$ is not computable.*

*Proof sketch (Berry's paradox).* Suppose for contradiction that $K$ is computable. Then consider the following program $p$: "Enumerate all strings in shortlex order. Output the first string $x$ such that $K(x) > |p| + c_0$." This program has some fixed length $|p| = L$. It outputs a string $x$ with $K(x) > L + c_0$. But $p$ itself is a description of $x$, so $K(x) \leq L$, a contradiction for sufficiently large $c_0$.

This is the formalization of Berry's paradox: "the smallest positive integer not definable in fewer than twelve words" is defined in eleven words. $\square$

**Proposition 8.5 (Upper semi-computability).** *$K(x)$ is upper semi-computable: there exists a computable function $\phi(x, t)$ with $\phi(x, t) \geq \phi(x, t+1)$ and $\lim_{t \to \infty} \phi(x, t) = K(x)$.* We can approximate $K(x)$ from above by running all programs in parallel and tracking the shortest one found so far that outputs $x$. We can never know when we have found the true minimum, but any program we find gives a valid upper bound.

---

## 8.5 Incompressible Strings

**Definition.** A string $x \in \{0,1\}^n$ is **$c$-incompressible** if $K(x) \geq n - c$. A string is **incompressible** if it is $0$-incompressible, i.e., $K(x) \geq |x|$.

**Theorem 8.6 (Counting argument).** *For every $n$ and every $c \geq 0$:*

1. *There exists at least one incompressible string of length $n$.*
2. *The fraction of strings of length $n$ that are $c$-compressible (i.e., $K(x) < n - c$) is at most $2^{-c}$.*

*Proof.* There are $2^n$ binary strings of length $n$. The total number of programs of length less than $n - c$ is at most

$$\sum_{k=0}^{n-c-1} 2^k = 2^{n-c} - 1 < 2^{n-c}.$$

Each such program produces at most one output. Therefore, at most $2^{n-c}$ strings of length $n$ have $K(x) < n - c$. The fraction is at most $2^{n-c}/2^n = 2^{-c}$.

In particular, for $c = 0$: at most $2^n - 1$ strings have descriptions shorter than $n$ bits, so at least one string of length $n$ is incompressible. For $c = 10$: at least 99.9\% of strings of length $n$ satisfy $K(x) \geq n - 10$. $\square$

**Interpretation.** Incompressible strings are "random"—they have no exploitable pattern. Most strings are nearly incompressible. This gives an algorithmic definition of randomness for finite objects.

---

## 8.6 Conditional and Joint Complexity

**Definition.** The **conditional Kolmogorov complexity** of $x$ given $y$ is

$$K(x \mid y) = \min\{|p| : U(p, y) = x\}$$

where $U(p, y)$ means running $U$ with program $p$ and auxiliary input $y$.

**Definition.** The **joint Kolmogorov complexity** of $x$ and $y$ is $K(x, y)$, defined as the shortest program that outputs the pair $(x, y)$ (under some standard pairing function).

**Theorem 8.7 (Chain rule for Kolmogorov complexity).** *For all strings $x, y$:*

$$K(x, y) = K(x) + K(y \mid x) + O(\log n)$$

*where $n = |x| + |y|$.*

The logarithmic term arises from the need to encode the boundary between the descriptions of $x$ and $y \mid x$ within a joint program. This is analogous to Shannon's chain rule $H(X, Y) = H(X) + H(Y \mid X)$, but with an unavoidable $O(\log n)$ "overhead."

**Theorem 8.8 (Symmetry of algorithmic information).** *For all strings $x, y$:*

$$K(x \mid y) = K(y \mid x) + O(\log n)$$

*where $n = \max(|x|, |y|)$.*

*Proof sketch.* From the chain rule applied in both orders:

$$K(x) + K(y \mid x) + O(\log n) = K(x, y) = K(y) + K(x \mid y) + O(\log n)$$

Rearranging: $K(y \mid x) - K(x \mid y) = K(y) - K(x) + O(\log n)$.

A more refined version (Kolmogorov, Levin) shows $K(x \mid y, K(y)) + K(y) = K(x, y) + O(\log n)$ and similarly with roles swapped, yielding symmetry up to $O(\log n)$. $\square$

---

## 8.7 Prefix-Free Complexity

The "plain" Kolmogorov complexity $K(x)$ defined above has an inconvenient property: the set of valid programs need not be prefix-free, so the sum $\sum_x 2^{-K(x)}$ can diverge. This prevents a clean connection to probability.

**Definition.** A **prefix-free Turing machine** is one whose domain (the set of inputs on which it halts) is a prefix-free set: no valid input is a proper prefix of another. The **prefix-free Kolmogorov complexity** is

$$K_{\text{prefix}}(x) = \min\{|p| : U_{\text{prefix}}(p) = x\}$$

where $U_{\text{prefix}}$ is a universal prefix-free Turing machine.

**Theorem 8.9 (Kraft inequality for prefix-free complexity).**

$$\sum_{x \in \{0,1\}^*} 2^{-K_{\text{prefix}}(x)} \leq 1.$$

*Proof.* Since the domain of $U_{\text{prefix}}$ is prefix-free, the Kraft inequality applies directly:

$$\sum_{p \in \text{dom}(U_{\text{prefix}})} 2^{-|p|} \leq 1.$$

Grouping by output: each $x$ may be produced by multiple programs, but

$$\sum_x 2^{-K_{\text{prefix}}(x)} \leq \sum_x \sum_{p: U(p) = x} 2^{-|p|} = \sum_{p \in \text{dom}(U)} 2^{-|p|} \leq 1.$$

(The first inequality is actually an equality in the lower bound direction since we only take the minimum-length program, but the upper bound suffices.) $\square$

The prefix-free version satisfies $K_{\text{prefix}}(x) \geq K(x)$ and $K_{\text{prefix}}(x) \leq K(x) + O(\log K(x))$, so the two notions agree up to logarithmic terms. For the remainder of this chapter, we use $K(x)$ to denote prefix-free complexity unless otherwise stated.

---

## 8.8 Algorithmic Probability and Solomonoff's Prior

**Definition.** The **algorithmic probability** (or universal a priori probability) of $x$ is

$$\mathbf{m}(x) = \sum_{\substack{p : U(p) = x}} 2^{-|p|}$$

where the sum is over all programs $p$ in the domain of a universal prefix-free Turing machine $U$ that output $x$.

By the Kraft inequality, $\mathbf{m}$ is a semi-measure: $\sum_x \mathbf{m}(x) \leq 1$. Intuitively, $\mathbf{m}(x)$ is the probability that a random program (generated by fair coin flips for each bit, halting when the machine accepts) produces $x$.

**Theorem 8.10 (Coding theorem, Levin 1974).**

$$K(x) = -\log_2 \mathbf{m}(x) + O(1).$$

**Connection to Solomonoff's prior.** Solomonoff (1964) proposed $\mathbf{m}$ as a universal prior for prediction: given an observed sequence $x_1 \ldots x_n$, predict the next bit by

$$P(x_{n+1} = 1 \mid x_1 \ldots x_n) = \frac{\mathbf{m}(x_1 \ldots x_n 1)}{\mathbf{m}(x_1 \ldots x_n)}.$$

This prior is *universal* in the sense that it dominates every computable measure: for every computable probability distribution $\mu$, there exists $c_\mu > 0$ such that $\mathbf{m}(x) \geq c_\mu \cdot \mu(x)$ for all $x$. It thus converges (in a precise sense) to the true distribution at a rate depending only on the complexity of the true distribution.

---

## 8.9 Martin-Löf Randomness

Algorithmic randomness formalizes the intuition that a random string should pass every conceivable statistical test.

**Definition (Martin-Löf, 1966).** An **effective statistical test** is a uniformly computably enumerable sequence $\{V_m\}_{m=1}^{\infty}$ of open sets $V_m \subseteq \{0,1\}^\omega$ (in Cantor space) such that $\mu(V_m) \leq 2^{-m}$, where $\mu$ is the fair-coin measure.

An infinite sequence $\omega \in \{0,1\}^\omega$ is **Martin-Löf random** if for every effective statistical test, $\omega \notin \bigcap_{m=1}^{\infty} V_m$.

**Theorem 8.11 (Schnorr-Levin theorem).** *An infinite binary sequence $\omega = \omega_1 \omega_2 \omega_3 \ldots$ is Martin-Löf random if and only if*

$$K_{\text{prefix}}(\omega_1 \ldots \omega_n) \geq n - O(1) \quad \text{for all } n.$$

This gives a clean equivalence: an infinite sequence is random if and only if its initial segments are all (nearly) incompressible.

---

## 8.10 Brudno's Theorem: Complexity Meets Ergodic Theory

Kolmogorov complexity connects to dynamical systems through a beautiful theorem due to Brudno (1983).

**Theorem 8.12 (Brudno, 1983).** *Let $(X, T, \mu)$ be an ergodic measure-preserving system on a compact metric space, with a finite generating partition $\mathcal{P}$. Let $x_1 x_2 x_3 \ldots$ be the symbolic itinerary of a point $x$ with respect to $\mathcal{P}$. Then for $\mu$-almost every $x$:*

$$\lim_{n \to \infty} \frac{K(x_1 \ldots x_n)}{n} = h_\mu(T)$$

*where $h_\mu(T)$ is the Kolmogorov-Sinai (metric) entropy of the system.*

**Interpretation.** The Kolmogorov complexity growth rate of a typical orbit equals the dynamical entropy. This is a profound link between computation theory and ergodic theory: the "algorithmic compressibility" of typical trajectories is determined by the dynamical entropy of the system.

---

## 8.11 Worked Examples

### Example 8.1: Complexity of a constant string

Let $x = 0^n$ (the string of $n$ zeros). A program to produce this is:

```
print '0' repeated n times
```

The program needs to encode the instruction (constant overhead) and the number $n$ (requiring $\lceil \log_2 n \rceil$ bits). Therefore

$$K(0^n) \leq \log_2 n + O(1).$$

A matching lower bound (up to $O(\log \log n)$) can be shown: any program producing $0^n$ must somehow specify $n$, which requires $\Omega(\log n)$ bits. We conclude

$$K(0^n) = \Theta(\log n).$$

Contrast this with $|0^n| = n$. The string $0^n$ is highly compressible; its complexity grows only logarithmically in its length.

### Example 8.2: Complexity of the digits of $\pi$

Let $x = \pi_n$ denote the first $n$ digits (or bits) of $\pi$. There exist short programs that compute $\pi$ to arbitrary precision (e.g., using the Chudnovsky algorithm). Such a program takes as input only the desired precision $n$. Therefore

$$K(\pi_n) \leq \log_2 n + O(1).$$

Despite $\pi$ being irrational and "looking random," it is *algorithmically simple*—the entire infinite expansion is generated by a short, fixed program. The complexity of a finite prefix is dominated by the cost of specifying how many digits to output.

### Example 8.3: Complexity of an incompressible string

Let $r$ be a specific string of length $n$ produced by a true random number generator (e.g., radioactive decay). By Theorem 8.6, with probability at least $1 - 2^{-c}$, such a string satisfies

$$K(r) \geq n - c.$$

Consider $n = 1000$. With probability $\geq 1 - 1/1024 \approx 99.9\%$, we have $K(r) \geq 990$. No program shorter than 990 bits can produce $r$. The string is essentially its own shortest description.

To verify the counting argument concretely: among all $2^{1000}$ strings of length 1000, at most $2^{990} - 1$ have a program shorter than 990 bits. The fraction of "10-compressible" strings is at most $2^{990}/2^{1000} = 2^{-10} < 0.001$.

### Example 8.4: The chain rule in action

Consider two strings: $x = 0^{500}$ (500 zeros) and $y$ = the binary encoding of $x$ repeated three times, i.e., $y = 0^{1500}$.

We have:
- $K(x) = O(\log 500) = O(1)$ (about 9 bits plus overhead).
- $K(y \mid x) = O(1)$: given $x$, the program "concatenate $x$ three times" is a short, fixed program.
- $K(x, y) = K(x) + K(y \mid x) + O(\log n) = O(\log n)$.

By contrast, if $x$ and $y$ were independent incompressible strings of length 500 and 1500 respectively:
- $K(x) \approx 500$, $K(y \mid x) \approx 1500$ (knowing $x$ gives no information about $y$).
- $K(x, y) \approx 500 + 1500 = 2000$.

The chain rule $K(x, y) = K(x) + K(y \mid x) + O(\log n)$ mirrors the Shannon relation $H(X, Y) = H(X) + H(Y \mid X)$ but at the level of individual objects.

---

## 8.12 Practical Approximation

Since $K(x)$ is not computable, we cannot calculate it exactly. However, any lossless compression algorithm provides an *upper bound*:

$$K(x) \leq |\text{gzip}(x)| + c_{\text{gzip}}$$

where $c_{\text{gzip}}$ is the constant overhead of encoding the gzip decompression algorithm.

**Normalized Compression Distance (NCD).** Li et al. (2004) proposed a practical similarity metric based on compression:

$$\text{NCD}(x, y) = \frac{C(xy) - \min(C(x), C(y))}{\max(C(x), C(y))}$$

where $C(x)$ is the compressed size of $x$ and $C(xy)$ is the compressed size of the concatenation. This approximates the *normalized information distance*

$$\text{NID}(x, y) = \frac{\max(K(x \mid y), K(y \mid x))}{\max(K(x), K(y))}$$

which is a universal metric (it minorizes every computable metric, up to a vanishing additive term). NCD has been applied successfully to clustering, classification, plagiarism detection, phylogenetics, and music analysis.

---

## 8.13 Connection to Discrete Dynamical Systems

Consider a discrete dynamical system $(X, f)$ and a point $x_0 \in X$ with orbit $x_0, f(x_0), f^2(x_0), \ldots$. Under a symbolic encoding, the orbit becomes a string $\sigma = s_0 s_1 s_2 \ldots s_{n-1}$.

The Kolmogorov complexity $K(\sigma)$ measures the intrinsic information content of this orbit segment. Three regimes emerge:

1. **Trivially simple orbits** ($K(\sigma) = O(\log n)$): Fixed points, periodic orbits, and orbits converging to simple attractors. The entire orbit can be specified by the rule, the initial condition, and the length. Example: the orbit $0 \to 0 \to 0 \to \cdots$ under the identity map.

2. **Maximally complex orbits** ($K(\sigma) \approx n$): These are algorithmically random orbits indistinguishable from fair coin flips. They carry maximal information but no discernible structure. By Brudno's theorem, for an ergodic system with entropy $h_\mu$, typical orbits have $K(\sigma) \approx h_\mu \cdot n$.

3. **Intermediate complexity orbits** ($O(\log n) \ll K(\sigma) \ll n$): These are the most interesting from the standpoint of structure and emergence. They are neither trivially predictable nor indistinguishable from noise. They exhibit regularities that can be partially but not fully compressed. In our framework, these are "creative" orbits: they encode genuine structural information.

Brudno's theorem makes the connection precise for ergodic systems. For non-ergodic systems or transient behavior, the relationship between orbit complexity and dynamical properties remains an active area of research.

---

## 8.14 Summary of Key Results

| Result | Statement |
|--------|-----------|
| Definition | $K(x) = \min\{|p| : U(p) = x\}$ |
| Invariance | $|K_{U_1}(x) - K_{U_2}(x)| \leq c$ |
| Upper bound | $K(x) \leq |x| + O(1)$ |
| Non-computability | $K$ is not computable |
| Upper semi-computability | $K$ can be approximated from above |
| Incompressibility | Most strings satisfy $K(x) \geq |x| - O(1)$ |
| Chain rule | $K(x,y) = K(x) + K(y \mid x) + O(\log n)$ |
| Symmetry | $K(x \mid y) = K(y \mid x) + O(\log n)$ |
| Coding theorem | $K(x) = -\log_2 \mathbf{m}(x) + O(1)$ |
| Schnorr-Levin | ML-random $\iff$ $K_{\text{prefix}}(x_{1:n}) \geq n - O(1)$ |
| Brudno | $K(x_{1:n})/n \to h_\mu$ a.s. for ergodic systems |

---

## References

- Chaitin, G. J. (1966). On the length of programs for computing finite binary sequences. *Journal of the ACM*, 13(4), 547--569.
- Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory*, 2nd edition. Wiley. Chapter 14.
- Kolmogorov, A. N. (1965). Three approaches to the quantitative definition of information. *Problems of Information Transmission*, 1(1), 1--7.
- Li, M. & Vitányi, P. (2019). *An Introduction to Kolmogorov Complexity and Its Applications*, 4th edition. Springer.
- Li, M., Chen, X., Li, X., Ma, B., & Vitányi, P. (2004). The similarity metric. *IEEE Transactions on Information Theory*, 50(12), 3250--3264.
- Martin-Löf, P. (1966). The definition of random sequences. *Information and Control*, 9(6), 602--619.
- Brudno, A. A. (1983). Entropy and the complexity of the trajectories of a dynamical system. *Transactions of the Moscow Mathematical Society*, 44, 127--151.
- Solomonoff, R. J. (1964). A formal theory of inductive inference. *Information and Control*, 7(1), 1--22 and 7(2), 224--254.
- Levin, L. A. (1974). Laws of information conservation (nongrowth) and aspects of the foundation of probability theory. *Problems of Information Transmission*, 10(3), 206--210.
- Schnorr, C. P. (1973). Process complexity and effective random tests. *Journal of Computer and System Sciences*, 7(4), 376--388.
