# Chapter 2: Discrete Dynamical Systems

In this chapter we study the simplest class of dynamical systems: iteration of a map. Despite the apparent simplicity of the setup — apply a function, then apply it again, then again — the resulting behavior can be extraordinarily rich. We will develop the basic vocabulary (orbits, fixed points, periodic orbits, stability), carry out detailed analysis of the logistic map, introduce the visual tool of cobweb diagrams, and encounter two of the most remarkable theorems in the subject: Sharkovskii's theorem and the Li–Yorke theorem.

## 2.1 Maps and Iteration

**Definition 2.1.** Let $X$ be a set. A *discrete dynamical system* on $X$ is a map $f: X \to X$. The *orbit* of a point $x_0 \in X$ under $f$ is the sequence

$$
\mathcal{O}(x_0) = \{x_0, \, f(x_0), \, f^2(x_0), \, f^3(x_0), \, \ldots\},
$$

where $f^n$ denotes the $n$-th iterate of $f$:

$$
f^0(x) = x, \qquad f^{n+1}(x) = f(f^n(x)).
$$

We write $x_n = f^n(x_0)$ and call $x_n$ the *state at time $n$*. The set $X$ is the *state space* or *phase space*.

**Remark.** The notation $f^n$ always means $n$-fold composition, never the $n$-th power. When we need the $n$-th power of $f(x)$, we write $(f(x))^n$ or $[f(x)]^n$.

Throughout this chapter, unless stated otherwise, we take $X \subseteq \mathbb{R}$ and assume $f$ is continuous. Many definitions extend to higher dimensions and more general spaces, but one-dimensional maps already contain most of the essential phenomena.

**Example 2.2 (Linear map).** Let $f: \mathbb{R} \to \mathbb{R}$ be defined by $f(x) = ax$ for some constant $a \in \mathbb{R}$. Then $f^n(x_0) = a^n x_0$. The orbit of any $x_0 \neq 0$ satisfies:

- If $|a| < 1$: $x_n \to 0$ as $n \to \infty$.
- If $|a| > 1$: $|x_n| \to \infty$ as $n \to \infty$.
- If $a = 1$: every point is fixed. If $a = -1$: every nonzero orbit has period 2.

Simple as it is, this example already illustrates the central question: *given $f$ and $x_0$, what is the long-term behavior of the orbit?*

**Example 2.3 (Rotation on the circle).** Let $X = \mathbb{R}/\mathbb{Z}$ (the unit circle, identified with $[0,1)$) and $f(x) = x + \alpha \pmod{1}$ for some $\alpha \in \mathbb{R}$. If $\alpha = p/q$ is rational (in lowest terms), then every orbit is periodic with period $q$. If $\alpha$ is irrational, then every orbit is dense in $[0,1)$ — a fact we will prove in Chapter 9 using ergodic theory. This dichotomy between rational and irrational rotation is a prototype for many phenomena in dynamics.


## 2.2 Fixed Points and Periodic Orbits

**Definition 2.4.** A point $x^* \in X$ is a *fixed point* of $f$ if $f(x^*) = x^*$.

**Definition 2.5.** A point $x^*$ is a *periodic point* of $f$ with *period* $n$ (or is $n$-periodic) if $f^n(x^*) = x^*$ and $n$ is the smallest positive integer with this property. The set $\{x^*, f(x^*), \ldots, f^{n-1}(x^*)\}$ is the *periodic orbit* (or *cycle*) of $x^*$.

A fixed point is a periodic point of period 1. If $f^n(x^*) = x^*$ but $n$ is not necessarily minimal, we say $x^*$ is an *eventually periodic point of period dividing $n$*, or simply that $x^*$ is a *point of period $n$* (with the understanding that the minimal period may be a proper divisor of $n$). In this text we will be careful to distinguish between the two conventions when it matters.

**Observation.** The periodic points of period $n$ are exactly the fixed points of $f^n$. This is important: to find period-$n$ orbits, solve $f^n(x) = x$.

**Example 2.6.** Consider $f: \mathbb{R} \to \mathbb{R}$, $f(x) = x^2 - 1$. The fixed points satisfy $x^2 - 1 = x$, i.e., $x^2 - x - 1 = 0$, giving

$$
x^* = \frac{1 \pm \sqrt{5}}{2}.
$$

For period-2 orbits, we solve $f^2(x) = x$. We have $f^2(x) = f(x^2-1) = (x^2 - 1)^2 - 1 = x^4 - 2x^2$. Setting $f^2(x) = x$:

$$
x^4 - 2x^2 - x = 0 \implies x(x^3 - 2x - 1) = 0.
$$

Since fixed points of $f$ are also fixed points of $f^2$, the polynomial $x^2 - x - 1$ divides $x^3 - 2x - 1$. Performing the division:

$$
x^3 - 2x - 1 = (x^2 - x - 1)(x + 1).
$$

So the solutions of $f^2(x) = x$ that are *not* fixed points of $f$ are $x = 0$ and $x = -1$. Check: $f(0) = -1$ and $f(-1) = 0$. Thus $\{0, -1\}$ is a period-2 orbit.


## 2.3 Stability of Fixed Points

Not all fixed points are created equal. Some attract nearby orbits; others repel them. Making this precise requires the derivative.

**Definition 2.7.** Let $f: \mathbb{R} \to \mathbb{R}$ be differentiable at a fixed point $x^*$. The quantity $\lambda = f'(x^*)$ is called the *multiplier* (or *eigenvalue*) of the fixed point. We say $x^*$ is:

- *attracting* (or *stable*) if $|\lambda| < 1$,
- *repelling* (or *unstable*) if $|\lambda| > 1$,
- *neutral* (or *indifferent*) if $|\lambda| = 1$.

The neutral case requires further analysis and will not be our main focus.

### 2.3.1 Why the Multiplier Determines Stability

The intuition is straightforward. Near $x^*$, the map $f$ is approximately linear:

$$
f(x) \approx f(x^*) + f'(x^*)(x - x^*) = x^* + \lambda(x - x^*).
$$

Writing $\varepsilon_n = x_n - x^*$ for the displacement from the fixed point, we have $\varepsilon_{n+1} \approx \lambda \, \varepsilon_n$, so $\varepsilon_n \approx \lambda^n \varepsilon_0$. If $|\lambda| < 1$ then $\varepsilon_n \to 0$; if $|\lambda| > 1$ then $|\varepsilon_n| \to \infty$. We now make this rigorous.

**Theorem 2.8 (Stability of fixed points).** Let $f: \mathbb{R} \to \mathbb{R}$ be $C^1$ in a neighborhood of a fixed point $x^*$.

*(a)* If $|f'(x^*)| < 1$, then $x^*$ is asymptotically stable: there exists $\delta > 0$ such that $|x_0 - x^*| < \delta$ implies $f^n(x_0) \to x^*$ as $n \to \infty$.

*(b)* If $|f'(x^*)| > 1$, then $x^*$ is unstable: there exists $\delta > 0$ such that for any $x_0$ with $0 < |x_0 - x^*| < \delta$, the orbit eventually leaves the interval $(x^* - \delta, x^* + \delta)$.

*Proof of (a).* Since $f'$ is continuous and $|f'(x^*)| < 1$, there exists $\mu$ with $|f'(x^*)| < \mu < 1$ and an interval $I = (x^* - \delta, x^* + \delta)$ such that $|f'(x)| \leq \mu$ for all $x \in I$.

Let $x_0 \in I$. By the mean value theorem, there exists $c$ between $x_0$ and $x^*$ such that

$$
|f(x_0) - x^*| = |f(x_0) - f(x^*)| = |f'(c)| \cdot |x_0 - x^*| \leq \mu \, |x_0 - x^*| < |x_0 - x^*| < \delta.
$$

So $f(x_0) \in I$, and by induction $f^n(x_0) \in I$ for all $n \geq 0$. Applying the estimate inductively:

$$
|f^n(x_0) - x^*| \leq \mu^n |x_0 - x^*|.
$$

Since $0 < \mu < 1$, we have $\mu^n \to 0$, so $f^n(x_0) \to x^*$. Moreover, convergence is geometric (exponential) with rate $\mu$. $\square$

*Proof of (b).* Since $|f'(x^*)| > 1$, choose $\mu$ with $1 < \mu < |f'(x^*)|$ and $\delta > 0$ such that $|f'(x)| \geq \mu$ for all $x \in I = (x^* - \delta, x^* + \delta)$. By the mean value theorem, for any $x \in I$ with $x \neq x^*$:

$$
|f(x) - x^*| = |f'(c)| \cdot |x - x^*| \geq \mu \, |x - x^*| > |x - x^*|.
$$

Thus the distance from $x^*$ increases by at least a factor of $\mu > 1$ at each step, as long as the orbit remains in $I$. Since the interval is bounded, the orbit must eventually leave $I$. $\square$

**Remark.** The proof of part (a) is essentially a contraction mapping argument: $f$ restricted to $I$ is a contraction with Lipschitz constant $\mu < 1$, and $x^*$ is the unique fixed point of this contraction.

### 2.3.2 Stability of Periodic Orbits

For a periodic orbit of period $n$, the relevant quantity is the multiplier of the corresponding fixed point of $f^n$. By the chain rule, if $\{x_0, x_1, \ldots, x_{n-1}\}$ is a period-$n$ orbit, then

$$
(f^n)'(x_0) = f'(x_{n-1}) \cdot f'(x_{n-2}) \cdots f'(x_1) \cdot f'(x_0) = \prod_{k=0}^{n-1} f'(x_k).
$$

Note that this product is the same regardless of which point $x_k$ in the cycle we start from (the factors are cyclically permuted). So *stability is a property of the entire orbit, not of individual points on it*.

**Definition 2.9.** A period-$n$ orbit is attracting if $|(f^n)'(x_0)| < 1$, repelling if $|(f^n)'(x_0)| > 1$, and neutral if $|(f^n)'(x_0)| = 1$, where $x_0$ is any point on the orbit.


## 2.4 The Logistic Map

The logistic map

$$
f_r(x) = rx(1-x), \qquad r \in [0,4], \quad x \in [0,1],
$$

is a one-parameter family of maps that serves as the principal example in one-dimensional dynamics. It arises as a simple model of population growth with density-dependent limitation (the factor $(1-x)$ represents the effect of limited resources when the population fraction $x$ is near its carrying capacity). Despite its elementary form — a single quadratic polynomial — the logistic map exhibits the full range of dynamical behaviors, from simple convergence to a fixed point, through period-doubling bifurcations, to chaos.

We restrict to $r \in [0,4]$ because this is the range for which $f_r$ maps $[0,1]$ into itself. (The maximum of $f_r$ on $[0,1]$ occurs at $x = 1/2$ with value $r/4$, so $f_r([0,1]) \subseteq [0,1]$ if and only if $r \leq 4$.)

### 2.4.1 Fixed Points

Setting $f_r(x) = x$:

$$
rx(1-x) = x \implies x[r(1-x) - 1] = 0 \implies x[r - 1 - rx] = 0.
$$

This gives two fixed points:

$$
x_0^* = 0, \qquad x_1^* = 1 - \frac{1}{r} = \frac{r-1}{r}.
$$

The second fixed point $x_1^*$ lies in $(0,1)$ only when $r > 1$. At $r = 1$, the two fixed points collide (both equal 0), and for $r < 1$, the fixed point $x_1^*$ is negative and therefore outside $[0,1]$.

### 2.4.2 Stability of the Fixed Points

The derivative is $f_r'(x) = r(1 - 2x)$.

**At $x_0^* = 0$:** The multiplier is $f_r'(0) = r$.

- For $0 < r < 1$: $|f_r'(0)| = r < 1$, so $x_0^* = 0$ is attracting. (The population dies out.)
- For $r > 1$: $|f_r'(0)| = r > 1$, so $x_0^* = 0$ is repelling.
- At $r = 1$: neutral.

**At $x_1^* = (r-1)/r$:** The multiplier is

$$
f_r'\!\left(\frac{r-1}{r}\right) = r\!\left(1 - \frac{2(r-1)}{r}\right) = r \cdot \frac{r - 2r + 2}{r} = 2 - r.
$$

- For $1 < r < 3$: $|2 - r| < 1$, so $x_1^*$ is attracting. (The population converges to a nonzero equilibrium.)
- For $r > 3$: $|2 - r| = r - 2 > 1$, so $x_1^*$ is repelling.
- At $r = 3$: $f_r'(x_1^*) = -1$ (neutral — a *period-doubling bifurcation* occurs here).

**Summary so far:**

| Parameter range | Attracting fixed point |
|---|---|
| $0 < r < 1$ | $x_0^* = 0$ |
| $1 < r < 3$ | $x_1^* = (r-1)/r$ |
| $r > 3$ | Neither fixed point is attracting |

### 2.4.3 The Period-2 Orbit

For $r > 3$, the fixed point $x_1^*$ loses stability and a period-2 orbit is born. To find it, we solve $f_r^2(x) = x$ and factor out the fixed points.

Compute $f_r^2(x) = f_r(f_r(x)) = r \cdot [rx(1-x)] \cdot [1 - rx(1-x)]$. Setting $f_r^2(x) = x$:

$$
r^2 x(1-x)[1 - rx(1-x)] = x.
$$

The solutions include the fixed points $x = 0$ and $x = (r-1)/r$. Dividing $f_r^2(x) - x$ by $x(x - (r-1)/r)$, we can find the remaining factor. After algebra (which the reader should verify), the period-2 points satisfy the quadratic equation

$$
r^2 x^2 - r(r+1)x + (r+1) = 0.
$$

By the quadratic formula:

$$
x = \frac{r(r+1) \pm r\sqrt{(r+1)(r-3)}}{2r^2} = \frac{(r+1) \pm \sqrt{(r+1)(r-3)}}{2r}.
$$

These are real and distinct when $r > 3$ (since $(r+1)(r-3) > 0$). Denote the two period-2 points by

$$
p = \frac{(r+1) + \sqrt{(r+1)(r-3)}}{2r}, \qquad q = \frac{(r+1) - \sqrt{(r+1)(r-3)}}{2r}.
$$

One verifies that $f_r(p) = q$ and $f_r(q) = p$, so $\{p, q\}$ is indeed a 2-cycle.

**Stability of the 2-cycle.** The multiplier is

$$
(f_r^2)'(p) = f_r'(p) \cdot f_r'(q).
$$

Using $f_r'(x) = r(1-2x)$:

$$
f_r'(p) \cdot f_r'(q) = r^2(1-2p)(1-2q).
$$

From the quadratic $r^2 x^2 - r(r+1)x + (r+1) = 0$, the sum and product of roots are:

$$
p + q = \frac{r+1}{r}, \qquad pq = \frac{r+1}{r^2}.
$$

Therefore:

$$
(1 - 2p)(1 - 2q) = 1 - 2(p+q) + 4pq = 1 - \frac{2(r+1)}{r} + \frac{4(r+1)}{r^2} = 1 - \frac{2(r+1)}{r} + \frac{4(r+1)}{r^2}.
$$

Simplifying with a common denominator of $r^2$:

$$
= \frac{r^2 - 2r(r+1) + 4(r+1)}{r^2} = \frac{r^2 - 2r^2 - 2r + 4r + 4}{r^2} = \frac{-r^2 + 2r + 4}{r^2}.
$$

So the multiplier of the 2-cycle is

$$
(f_r^2)'(p) = r^2 \cdot \frac{-r^2 + 2r + 4}{r^2} = -r^2 + 2r + 4 = -(r^2 - 2r - 4).
$$

The 2-cycle is attracting when $|{-r^2 + 2r + 4}| < 1$.

At $r = 3$: the multiplier equals $-9 + 6 + 4 = 1$. (The 2-cycle is born with multiplier $+1$.)

The 2-cycle loses stability when the multiplier reaches $-1$:

$$
-r^2 + 2r + 4 = -1 \implies r^2 - 2r - 5 = 0 \implies r = 1 + \sqrt{6} \approx 3.449.
$$

So the 2-cycle is attracting for $3 < r < 1 + \sqrt{6}$.

**Numerical check at $r = 3.2$:**

$$
p = \frac{4.2 + \sqrt{4.2 \cdot 0.2}}{6.4} = \frac{4.2 + \sqrt{0.84}}{6.4} \approx \frac{4.2 + 0.9165}{6.4} \approx 0.7995.
$$

$$
q \approx \frac{4.2 - 0.9165}{6.4} \approx 0.5130.
$$

Check: $f_{3.2}(0.7995) = 3.2 \cdot 0.7995 \cdot 0.2005 \approx 0.5130$. Correct.

The multiplier: $-(3.2)^2 + 2(3.2) + 4 = -10.24 + 6.4 + 4 = 0.16$. Since $|0.16| < 1$, the 2-cycle is attracting, as expected.

### 2.4.4 Preview of the Period-Doubling Cascade

At $r = 1 + \sqrt{6} \approx 3.449$, the period-2 orbit loses stability and gives birth to a period-4 orbit, which is attracting in a further interval of $r$-values. This period-4 orbit in turn loses stability and creates a period-8 orbit, and so on. This sequence of *period-doubling bifurcations* produces attracting orbits of periods $1, 2, 4, 8, 16, \ldots$ at parameter values $r_1 = 3, \, r_2 = 1 + \sqrt{6}, \, r_3, \, r_4, \ldots$ The sequence $\{r_n\}$ converges to a value $r_\infty \approx 3.5699$, and the ratios of successive intervals converge to a universal constant:

$$
\lim_{n \to \infty} \frac{r_n - r_{n-1}}{r_{n+1} - r_n} = \delta \approx 4.6692\ldots,
$$

the *Feigenbaum constant*. Remarkably, this constant is the same for *every* smooth unimodal map undergoing period-doubling — it is a universal quantity, independent of the specific form of $f$. We will study bifurcations systematically in Chapter 5.

For $r > r_\infty$, the behavior is much more complex: there are infinitely many parameter values with periodic orbits of every period, interspersed with parameter values where the dynamics is chaotic (in a sense we will make precise in Chapter 6). The *bifurcation diagram* — plotting the attractor as a function of $r$ — reveals an intricate structure that repays careful study.


## 2.5 Cobweb Diagrams

A *cobweb diagram* (also called a *staircase diagram*) is a graphical method for visualizing the orbit of a one-dimensional map. It translates the algebraic iteration $x_{n+1} = f(x_n)$ into a geometric construction.

### 2.5.1 Construction

To construct a cobweb diagram for $f: \mathbb{R} \to \mathbb{R}$ starting from $x_0$:

1. Plot the graph $y = f(x)$ and the diagonal $y = x$ in the same coordinate system.
2. Start at the point $(x_0, 0)$ on the $x$-axis. Draw a vertical line up (or down) to the curve $y = f(x)$, reaching the point $(x_0, f(x_0)) = (x_0, x_1)$.
3. Draw a horizontal line from $(x_0, x_1)$ to the diagonal $y = x$, reaching the point $(x_1, x_1)$. This "reflects" the output $x_1$ to the input axis.
4. Repeat: draw a vertical line to the curve, reaching $(x_1, f(x_1)) = (x_1, x_2)$, then horizontal to the diagonal, reaching $(x_2, x_2)$. Continue.

The resulting zigzag pattern between the curve and the diagonal traces out the orbit.

### 2.5.2 Interpretation

The geometry of the cobweb diagram directly reveals the dynamics:

- **Attracting fixed point with $0 < f'(x^*) < 1$:** The cobweb spirals inward in a "staircase" pattern, stepping monotonically toward the fixed point (where the curve and diagonal intersect).

- **Attracting fixed point with $-1 < f'(x^*) < 0$:** The cobweb spirals inward, but now it oscillates — the iterates alternate between sides of $x^*$, converging in a spiral.

- **Repelling fixed point:** The cobweb moves outward, away from the intersection.

- **Period-2 orbit:** The cobweb forms a rectangle (approximately) cycling between the two periodic points.

### 2.5.3 Worked Example: Logistic Map with $r = 2.8$

Consider $f(x) = 2.8\, x(1-x)$ with $x_0 = 0.1$.

The fixed point $x^* = 1 - 1/2.8 = 9/14 \approx 0.6429$, with multiplier $2 - 2.8 = -0.8$. Since $|-0.8| < 1$, the fixed point is attracting and the cobweb should spiral inward.

Computing the first several iterates:

$$
\begin{aligned}
x_0 &= 0.1 \\
x_1 &= 2.8 \cdot 0.1 \cdot 0.9 = 0.2520 \\
x_2 &= 2.8 \cdot 0.2520 \cdot 0.7480 \approx 0.5278 \\
x_3 &= 2.8 \cdot 0.5278 \cdot 0.4722 \approx 0.6980 \\
x_4 &= 2.8 \cdot 0.6980 \cdot 0.3020 \approx 0.5902 \\
x_5 &= 2.8 \cdot 0.5902 \cdot 0.4098 \approx 0.6773 \\
x_6 &\approx 0.6116 \\
x_7 &\approx 0.6651 \\
\end{aligned}
$$

The iterates oscillate around $x^* \approx 0.6429$ with decreasing amplitude, consistent with the multiplier $-0.8$ (negative sign causes oscillation, magnitude less than 1 causes convergence). In the cobweb diagram, the vertical and horizontal line segments form a spiral that converges to the intersection of $y = 2.8\,x(1-x)$ and $y = x$.

### 2.5.4 Worked Example: Logistic Map with $r = 3.2$

Now $f(x) = 3.2\, x(1-x)$. The fixed point $x^* = (r-1)/r = 2.2/3.2 = 0.6875$ has multiplier $2 - 3.2 = -1.2$. Since $|-1.2| > 1$, the fixed point is repelling, and orbits near it are pushed toward the attracting 2-cycle.

Starting from $x_0 = 0.5$:

$$
\begin{aligned}
x_0 &= 0.5000 \\
x_1 &= 0.8000 \\
x_2 &= 0.5120 \\
x_3 &= 0.7995 \\
x_4 &= 0.5131 \\
x_5 &= 0.7994 \\
\end{aligned}
$$

The orbit quickly settles into alternation between approximately $0.5130$ and $0.7995$ — the period-2 cycle we computed in Section 2.4.3. In the cobweb diagram, the pattern is a rectangle whose corners lie on the curve and the diagonal, cycling between the two periodic points.


## 2.6 Topological Conjugacy

When are two dynamical systems "the same"? The right notion of equivalence in dynamics is *topological conjugacy*: two systems are conjugate if there is a continuous invertible change of coordinates that transforms one into the other.

**Definition 2.10.** Let $f: X \to X$ and $g: Y \to Y$ be continuous maps on topological spaces $X$ and $Y$. We say $f$ and $g$ are *topologically conjugate* if there exists a homeomorphism $h: X \to Y$ such that

$$
h \circ f = g \circ h,
$$

or equivalently, $g = h \circ f \circ h^{-1}$. The map $h$ is called a *conjugacy*.

The condition $h \circ f = g \circ h$ means that the following diagram commutes:

$$
\begin{array}{ccc}
X & \xrightarrow{f} & X \\
\downarrow h & & \downarrow h \\
Y & \xrightarrow{g} & Y
\end{array}
$$

**Proposition 2.11.** If $h$ is a conjugacy between $f$ and $g$, then for all $n \geq 1$:
$$h \circ f^n = g^n \circ h.$$

*Proof.* By induction. The base case $n = 1$ is the definition. Assuming $h \circ f^n = g^n \circ h$, then $h \circ f^{n+1} = h \circ f \circ f^n = g \circ h \circ f^n = g \circ g^n \circ h = g^{n+1} \circ h$. $\square$

**Corollary 2.12.** Topological conjugacy preserves:

- Fixed points: $x^*$ is a fixed point of $f$ if and only if $h(x^*)$ is a fixed point of $g$.
- Periodic orbits: $x^*$ has period $n$ under $f$ if and only if $h(x^*)$ has period $n$ under $g$.
- The topology of orbits: dense orbits map to dense orbits, etc.

*Proof.* If $f(x^*) = x^*$, then $g(h(x^*)) = h(f(x^*)) = h(x^*)$, so $h(x^*)$ is fixed under $g$. The period-$n$ statement follows from Proposition 2.11. Density is preserved because $h$ is a homeomorphism. $\square$

Conjugacy is an equivalence relation on dynamical systems. Two conjugate systems have identical orbit structures — they differ only by a continuous change of coordinates. From the viewpoint of dynamics, they are the same system.

**Definition 2.13.** If the map $h$ in the above definition is only required to be a continuous surjection (rather than a homeomorphism), we say $f$ is *semiconjugate* to $g$, and $h$ is a *semiconjugacy*. Semiconjugacy is a weaker relationship: it means $g$ is a "factor" of $f$ (information about orbits of $f$ projects down to orbits of $g$, but not necessarily vice versa).

### 2.6.1 Example: The Doubling Map and the Tent Map

The *doubling map* $D: [0,1) \to [0,1)$ is defined by

$$
D(x) = 2x \pmod{1} = \begin{cases} 2x & \text{if } 0 \leq x < 1/2, \\ 2x - 1 & \text{if } 1/2 \leq x < 1. \end{cases}
$$

The *tent map* $T: [0,1] \to [0,1]$ is defined by

$$
T(x) = \begin{cases} 2x & \text{if } 0 \leq x \leq 1/2, \\ 2 - 2x & \text{if } 1/2 < x \leq 1. \end{cases}
$$

These two maps are *not* topologically conjugate (the tent map is continuous on $[0,1]$ while the doubling map has a discontinuity, and moreover their orbit structures differ in detail). However, there is an important semiconjugacy from the doubling map to a system on symbolic sequences, and the tent map is conjugate to the logistic map at $r = 4$ via an explicit change of coordinates.

### 2.6.2 Example: Conjugacy Between the Tent Map and the Logistic Map at $r = 4$

**Claim.** The logistic map $f_4(x) = 4x(1-x)$ on $[0,1]$ is topologically conjugate to the tent map $T$ on $[0,1]$ via the conjugacy

$$
h(x) = \frac{2}{\pi}\arcsin(\sqrt{x}).
$$

To verify this, we need $h \circ f_4 = T \circ h$, i.e., for all $x \in [0,1]$:

$$
\frac{2}{\pi}\arcsin\!\left(\sqrt{4x(1-x)}\right) = T\!\left(\frac{2}{\pi}\arcsin(\sqrt{x})\right).
$$

Let $\theta = \arcsin(\sqrt{x})$, so $x = \sin^2\theta$ with $\theta \in [0, \pi/2]$. Then:

**Left side:**

$$
\frac{2}{\pi}\arcsin\!\left(\sqrt{4\sin^2\theta\cos^2\theta}\right) = \frac{2}{\pi}\arcsin(|\sin(2\theta)|) = \frac{2}{\pi}\arcsin(\sin(2\theta)),
$$

where the last equality uses $\sin(2\theta) \geq 0$ for $\theta \in [0, \pi/2]$.

**Right side:** We have $h(x) = (2/\pi)\theta$, so:
- If $\theta \leq \pi/4$ (i.e., $h(x) \leq 1/2$): $T(h(x)) = 2 \cdot (2\theta/\pi) = 4\theta/\pi$.
- If $\theta > \pi/4$ (i.e., $h(x) > 1/2$): $T(h(x)) = 2 - 4\theta/\pi$.

**Checking the left side:**
- If $\theta \leq \pi/4$: $\arcsin(\sin(2\theta)) = 2\theta$ (since $2\theta \leq \pi/2$), so the left side is $4\theta/\pi$. Matches.
- If $\theta > \pi/4$: $\arcsin(\sin(2\theta)) = \pi - 2\theta$ (since $2\theta > \pi/2$), so the left side is $(2/\pi)(\pi - 2\theta) = 2 - 4\theta/\pi$. Matches.

Thus the conjugacy relation holds. The map $h$ is a homeomorphism of $[0,1]$ (it is continuous, strictly increasing, with $h(0) = 0$ and $h(1) = 1$), so this is a genuine topological conjugacy.

This conjugacy has a profound consequence: every dynamical property of the tent map at full slope transfers to the logistic map at $r = 4$. In particular, the logistic map at $r = 4$ has a dense set of periodic orbits and is topologically transitive — properties we will revisit when we discuss chaos in Chapter 6.


## 2.7 Sharkovskii's Theorem

One of the most striking results in one-dimensional dynamics concerns which periods *must* coexist. Suppose a continuous map $f: \mathbb{R} \to \mathbb{R}$ has a periodic orbit of some period $n$. Does it necessarily have periodic orbits of other periods? The answer is given by Sharkovskii's theorem, which provides a complete ordering.

**Definition 2.14 (Sharkovskii ordering).** Define the following total order on the positive integers:

$$
3 \triangleright 5 \triangleright 7 \triangleright 9 \triangleright \cdots
$$
$$
\triangleright \; 2 \cdot 3 \triangleright 2 \cdot 5 \triangleright 2 \cdot 7 \triangleright \cdots
$$
$$
\triangleright \; 4 \cdot 3 \triangleright 4 \cdot 5 \triangleright 4 \cdot 7 \triangleright \cdots
$$
$$
\triangleright \; 8 \cdot 3 \triangleright 8 \cdot 5 \triangleright 8 \cdot 7 \triangleright \cdots
$$
$$
\triangleright \; \cdots \triangleright 2^n \cdot 3 \triangleright 2^n \cdot 5 \triangleright 2^n \cdot 7 \triangleright \cdots
$$
$$
\triangleright \; \cdots \triangleright 2^3 \triangleright 2^2 \triangleright 2 \triangleright 1.
$$

In words: first all odd numbers $\geq 3$, then $2$ times all odd numbers $\geq 3$, then $4$ times all odd numbers $\geq 3$, and so on, followed by all powers of $2$ in decreasing order ($\ldots, 16, 8, 4, 2, 1$).

**Theorem 2.15 (Sharkovskii, 1964).** Let $f: \mathbb{R} \to \mathbb{R}$ be continuous. If $f$ has a periodic orbit of period $m$, then $f$ has a periodic orbit of period $n$ for every $n$ with $m \triangleright n$ in the Sharkovskii ordering.

**Moreover**, for each $m$, there exists a continuous map having a periodic orbit of period $m$ but no periodic orbit of any period $n$ with $n \triangleright m$.

The theorem says that the set of periods that a continuous map can have is always a "tail" (a downward-closed set) in the Sharkovskii ordering. The number 3 sits at the top of the ordering, so having a period-3 orbit forces orbits of every period. The powers of 2 sit at the bottom: a map can have orbits of periods $1, 2, 4, 8, 16, \ldots$ without having an orbit of period 3 (or 5, or 6, etc.). The logistic map at $r$ values in the period-doubling cascade provides exactly such examples.

**Significance.** Sharkovskii's theorem is remarkable for several reasons:

1. It applies to *every* continuous map $\mathbb{R} \to \mathbb{R}$ (or $I \to I$ for a closed interval $I$), with no smoothness assumptions.
2. The ordering is far from obvious. Why should period 3 force period 5? Why should period 6 force period 4 but not conversely? The proof, while elementary (it uses only the intermediate value theorem), requires a delicate combinatorial argument tracking how intervals map over each other.
3. It connects to the onset of chaos: the appearance of a period-3 orbit signals the presence of all other periods.

The original proof appears in Sharkovskii (1964). Accessible English-language proofs can be found in Devaney (1989, Chapter 1.11) and in Block and Coppel (1992). The theorem holds for continuous self-maps of an interval; it does *not* hold for maps of the circle, for discontinuous maps, or in dimensions higher than one.


## 2.8 The Li–Yorke Theorem: "Period Three Implies Chaos"

The special case of Sharkovskii's theorem that received the most attention is due to Li and Yorke (1975), published a decade after Sharkovskii's original work (which was not widely known outside the Soviet Union at the time).

**Theorem 2.16 (Li–Yorke, 1975).** Let $f: [a,b] \to [a,b]$ be continuous. If $f$ has a periodic point of period 3, then:

1. For every positive integer $n$, $f$ has a periodic point of period $n$.
2. There exists an uncountable set $S \subseteq [a,b]$ (called a *scrambled set*) such that for every pair $x, y \in S$ with $x \neq y$:

$$
\limsup_{n \to \infty} |f^n(x) - f^n(y)| > 0 \qquad \text{and} \qquad \liminf_{n \to \infty} |f^n(x) - f^n(y)| = 0,
$$

and for every periodic point $p$ of $f$ and every $x \in S$:

$$
\limsup_{n \to \infty} |f^n(x) - f^n(p)| > 0.
$$

Part (1) follows immediately from Sharkovskii's theorem (since 3 is first in the Sharkovskii ordering). The real novelty of Li and Yorke's paper is part (2): the existence of an uncountable scrambled set. This means there is a large set of initial conditions whose orbits are neither eventually periodic nor convergent to each other — they are perpetually drawn together and pushed apart, never settling into a regular pattern. This is a rigorous (though relatively weak) form of chaos.

**The meaning of "chaos" here.** The Li–Yorke definition of chaos (existence of an uncountable scrambled set) is one of several competing definitions. It is weaker than the definition due to Devaney (which additionally requires topological transitivity and density of periodic orbits). A system can be Li–Yorke chaotic without exhibiting the strong mixing behavior one might expect from "chaos" in the colloquial sense. Nevertheless, the title of their paper — "Period Three Implies Chaos" — became one of the most famous slogans in mathematics, and did much to bring the study of chaos to a broad audience.

**A concrete illustration.** The logistic map $f_r(x) = rx(1-x)$ has a period-3 orbit for $r = 1 + 2\sqrt{2} \approx 3.8284$ (this is the value at which a period-3 window opens in the bifurcation diagram). For this and all larger values of $r$ at which a 3-cycle exists, the Li–Yorke theorem guarantees periodic orbits of every period and an uncountable scrambled set.

To see a period-3 orbit concretely, consider $r \approx 3.8319$. Numerical iteration from $x_0 = 0.5$ yields an orbit that settles into the approximate cycle $0.1561 \to 0.5047 \to 0.9563 \to 0.1561 \to \cdots$. This orbit visits three distinct values cyclically, confirming the presence of a 3-cycle.


## 2.9 Bibliographical Notes

The study of iteration of maps goes back at least to Cayley and Schröder in the 19th century, but the modern theory was shaped by the work of Fatou and Julia (in the complex setting), Sharkovskii (1964), and Li and Yorke (1975). The logistic map was popularized as a model of population dynamics by Robert May (1976), whose influential paper in *Nature* brought the richness of nonlinear dynamics to the attention of scientists across disciplines.

The universality of the Feigenbaum constant was discovered independently by Feigenbaum (1978) and Coullet and Tresser (1978). Rigorous proofs of universality came later, notably by Lanford (1982) using computer-assisted methods.

The conjugacy between the logistic map at $r = 4$ and the tent map is a classical result; see Devaney (1989, Section 1.7) for a textbook treatment. The connection to symbolic dynamics (which we will develop in later chapters) provides a powerful framework for understanding such conjugacies.


## Recommended Reading

- **R. L. Devaney**, *An Introduction to Chaotic Dynamical Systems*, 3rd edition, CRC Press, 2021. The standard undergraduate text on discrete dynamical systems. Chapters 1–4 and 11–12 cover the material of this chapter in greater depth. Contains a proof of Sharkovskii's theorem.

- **S. H. Strogatz**, *Nonlinear Dynamics and Chaos*, 3rd edition, CRC Press, 2024. An outstanding textbook emphasizing continuous systems but with excellent chapters on one-dimensional maps (Chapter 10) and the logistic map in particular. More applied in flavor.

- **K. T. Alligood, T. D. Sauer, and J. A. Yorke**, *Chaos: An Introduction to Dynamical Systems*, Springer, 1996. A well-balanced text covering both discrete and continuous systems with many computational exercises. The treatment of the logistic map and period-doubling (Chapters 1–3 and 12) is particularly thorough.

- **A. N. Sharkovskii**, "Co-existence of cycles of a continuous mapping of the line into itself," *Ukrainian Mathematical Journal* **16** (1964), 61–71. The original paper proving Theorem 2.15 (in Ukrainian; English translations are available).

- **T.-Y. Li and J. A. Yorke**, "Period three implies chaos," *American Mathematical Monthly* **82** (1975), 985–992. The paper that introduced the term "chaos" to mathematics and proved Theorem 2.16. Remarkably short and readable.

- **R. May**, "Simple mathematical models with very complicated dynamics," *Nature* **261** (1976), 459–467. A landmark expository paper on the logistic map as a model in population biology.


## Exercises

**Exercise 2.1.** Let $f(x) = \cos(x)$. Show that $f$ has a unique fixed point $x^* \in [0,1]$, and determine whether it is attracting or repelling. Starting from $x_0 = 0$, compute the first 10 iterates numerically and verify your stability conclusion.

*Hint:* The fixed point satisfies $\cos(x^*) = x^*$. This equation has a unique solution $x^* \approx 0.7391$.

**Exercise 2.2.** Consider the logistic map $f_r(x) = rx(1-x)$.

(a) Verify that for $r = 2$, the fixed point $x^* = 1/2$ is attracting by computing the multiplier.

(b) Sketch a cobweb diagram (or describe the cobweb geometry) for $r = 2$, $x_0 = 0.1$. Is the convergence to $x^*$ monotone or oscillatory?

(c) For $r = 3.5$, compute the first 20 iterates starting from $x_0 = 0.4$. What is the eventual behavior? What is the period of the attracting cycle?

**Exercise 2.3.** Let $f(x) = x^2$.

(a) Find all fixed points and determine their stability.

(b) Find all period-2 orbits. (*Hint:* Solve $f^2(x) = x$ and remove the fixed points.)

(c) Describe the orbit of $x_0$ for each of the following cases: $x_0 \in (0,1)$; $x_0 = 1$; $x_0 > 1$; $x_0 \in (-1,0)$; $x_0 = -1$; $x_0 < -1$.

**Exercise 2.4 (Conjugacy).** Let $f(x) = 4x(1-x)$ and $g(x) = 1 - 2x^2$, both considered as maps on appropriate intervals.

(a) Find a linear change of variables $h(x) = ax + b$ such that $h \circ f = g \circ h$, where $f$ maps $[0,1]$ to itself and $g$ maps $[-1,1]$ to itself. (*Hint:* The conjugacy should map $[0,1]$ onto $[-1,1]$, so try $h(x) = 1 - 2x$ or $h(x) = 2x - 1$.)

(b) Verify the conjugacy relation explicitly by computing both sides for general $x \in [0,1]$.

(c) Use this conjugacy to transfer the period-3 orbit of $f$ at $r = 4$ (if one exists) to $g$. What are the coordinates of the corresponding period-3 orbit of $g$?

**Exercise 2.5 (Sharkovskii ordering).** Consider the Sharkovskii ordering $\triangleright$.

(a) List the first 20 elements of the Sharkovskii ordering (i.e., the 20 "largest" positive integers in this order).

(b) Where does the number 12 fall in the ordering? List five periods that must exist if a continuous map has a period-12 orbit, and five periods that are *not* guaranteed by having a period-12 orbit.

(c) A continuous map $f: [0,1] \to [0,1]$ has periodic orbits of periods $1, 2, 4$, and $8$, but no others. Is this consistent with Sharkovskii's theorem? Why or why not?

**Exercise 2.6 (Stability via the chain rule).** Let $f(x) = rx(1-x)$ with $r = 3.84$. At this parameter value, the logistic map has a period-3 orbit. Find the three points of this orbit numerically (to at least four decimal places) and compute the multiplier $(f^3)'$ at one of them using the chain rule formula from Section 2.3.2. Is the 3-cycle attracting or repelling?

**Exercise 2.7 (A non-standard map).** Define $f: [0,1] \to [0,1]$ by

$$
f(x) = \begin{cases} 2x + 1/2 & \text{if } 0 \leq x < 1/4, \\ 3/2 - 2x & \text{if } 1/4 \leq x \leq 1/2, \\ f(1-x) & \text{if } 1/2 < x \leq 1. \end{cases}
$$

(a) Sketch the graph of $f$ and verify that it is a continuous map from $[0,1]$ to $[0,1]$.

(b) Find all fixed points of $f$.

(c) Show that $f$ has a periodic orbit of period 2. Does Sharkovskii's theorem guarantee a periodic orbit of period 3?

(d) Does $f$ have a periodic orbit of period 4? Justify your answer.

**Exercise 2.8 (Proof).** Let $f: [a,b] \to [a,b]$ be a continuous map with a fixed point $x^*$, and suppose $f$ is differentiable on $(a,b)$ with $|f'(x)| \leq L$ for all $x \in (a,b)$, where $0 < L < 1$. Prove that $x^*$ is the *unique* fixed point of $f$ in $[a,b]$, and that $f^n(x_0) \to x^*$ for every $x_0 \in [a,b]$.

*Hint:* This is the Banach fixed-point theorem (contraction mapping theorem) applied to the complete metric space $[a,b]$. Prove it directly using the mean value theorem.
