# Chapter 6: Chaos and Attractors

> *"Chaos is found in greatest abundance wherever order is being sought. It always defeats order, because it is better organized."*
> — Terry Pratchett

In Chapters 2 through 5, we built the machinery of dynamical systems: iteration, fixed points, stability, bifurcations, and the routes by which simple systems can develop complicated behavior. In this chapter, we confront the complicated behavior itself. We give precise mathematical definitions of chaos, develop the tools to measure it (Lyapunov exponents, fractal dimension), study the geometric objects that organize it (strange attractors), and establish a remarkable theorem (Takens' embedding theorem) that will prove essential when we turn to reservoir computing in Part III.

The central tension of this chapter is between *unpredictability* and *structure*. Chaotic systems are deterministic yet practically unpredictable; their trajectories are wildly sensitive to initial conditions yet confined to attractors of intricate, self-similar geometry. Understanding this tension — and making it mathematically precise — is the goal before us.

---

## 6.1 What Is Chaos?

The word "chaos" is used loosely in everyday language, but in dynamical systems it has precise mathematical content. Several competing definitions exist in the literature. We begin with the most widely taught.

### 6.1.1 Devaney's Definition

Let $(X, d)$ be a metric space and $f: X \to X$ a continuous map.

**Definition 6.1 (Chaos in the sense of Devaney).** The map $f$ is said to be *chaotic on $X$* if the following three conditions hold:

1. **Sensitive dependence on initial conditions.** There exists $\delta > 0$ such that for every $x \in X$ and every $\epsilon > 0$, there exists $y \in X$ with $d(x, y) < \epsilon$ and $n \in \mathbb{N}$ such that $d(f^n(x), f^n(y)) > \delta$.

2. **Topological transitivity.** For every pair of nonempty open sets $U, V \subseteq X$, there exists $n \in \mathbb{N}$ such that $f^n(U) \cap V \neq \emptyset$.

3. **Dense periodic orbits.** The set of periodic points of $f$ is dense in $X$.

Condition (1) says that no matter how close two initial conditions are, their orbits eventually separate by at least $\delta$. Condition (2) says that the dynamics cannot be decomposed into two or more invariant pieces — there is a single orbit that comes arbitrarily close to every point. Condition (3) says that periodicity is ubiquitous, even though the generic orbit is aperiodic.

At first glance, these three conditions appear independent. The following remarkable result shows they are not.

**Theorem 6.2 (Banks, Brooks, Cairns, Davis, and Stacey, 1992).** *Let $X$ be an infinite metric space and $f: X \to X$ a continuous map. If $f$ is topologically transitive and has dense periodic orbits, then $f$ has sensitive dependence on initial conditions.*

In other words, conditions (ii) and (iii) together imply condition (i). Chaos, in Devaney's sense, is "simpler" than it first appears: the sensitive dependence comes for free.

*Proof sketch.* Suppose $f$ is topologically transitive and has dense periodic orbits but does *not* have sensitive dependence. Then for every $\delta > 0$, there exists a point $x$ and a neighborhood $U$ of $x$ such that for all $y \in U$ and all $n \geq 0$, $d(f^n(x), f^n(y)) \leq \delta$. Since periodic points are dense, we can find periodic points $p, q \in U$ with distinct orbits (using the fact that $X$ is infinite and topological transitivity prevents all points in a neighborhood from sharing the same eventual behavior). Choose $\delta$ small enough that the orbits of $p$ and $q$ must remain close. But since $p$ and $q$ are periodic, their orbits are finite sets, and topological transitivity forces the existence of points whose orbits wander throughout $X$. One shows this leads to a contradiction: the finite orbits of nearby periodic points, combined with transitivity, force separation beyond any fixed $\delta$. The full proof, which is not long, can be found in Banks et al. (1992). $\square$

**Remark.** The converse fails: sensitive dependence on initial conditions alone, or even combined with one of the other conditions, does not imply chaos. Consider the map $f(x) = 2x$ on $\mathbb{R}$: it has sensitive dependence on initial conditions but is neither topologically transitive (orbits escape to infinity or converge to zero depending on sign) nor does it have dense periodic orbits (the origin is the only fixed point, and there are no other periodic points).

### 6.1.2 Li-Yorke Chaos

An older notion of chaos, predating Devaney's definition, comes from the celebrated paper of Li and Yorke (1975).

**Definition 6.3 (Li-Yorke chaos).** A continuous map $f: I \to I$ on an interval $I \subseteq \mathbb{R}$ is *Li-Yorke chaotic* if there exists an uncountable set $S \subseteq I$ (called a *scrambled set*) such that for every pair $x, y \in S$ with $x \neq y$:

$$\limsup_{n \to \infty} |f^n(x) - f^n(y)| > 0 \quad \text{and} \quad \liminf_{n \to \infty} |f^n(x) - f^n(y)| = 0.$$

The pair $(x, y)$ is called a *Li-Yorke pair*: their orbits come arbitrarily close together infinitely often, yet also separate by a definite amount infinitely often. This captures a notion of *irregular* or *unpredictable* behavior without requiring dense periodic orbits or topological transitivity.

**Theorem 6.4 (Li and Yorke, 1975).** *If $f: I \to I$ is a continuous map of a compact interval and $f$ has a periodic point of period 3, then $f$ is Li-Yorke chaotic.*

This is the famous "period three implies chaos" result (the title of their 1975 paper). We state it here without proof; see Devaney (1989, Ch. 1.7) or the original paper.

**Comparison.** Devaney chaos and Li-Yorke chaos capture different aspects of complicated dynamics:

| | Devaney chaos | Li-Yorke chaos |
|---|---|---|
| Requires dense periodic orbits | Yes | No |
| Requires topological transitivity | Yes | No |
| Requires sensitive dependence | Implied | Not directly |
| Requires scrambled set | No | Yes |
| Applicable to | General metric spaces | Typically interval maps |

It is known that Devaney chaos implies Li-Yorke chaos for interval maps (Huang and Ye, 2002), but the converse does not hold in general. Neither definition is universally accepted as "the" definition of chaos — the appropriate notion depends on the context. In this text, we primarily work with Devaney's definition and the related quantitative tool of Lyapunov exponents.

---

## 6.2 Sensitive Dependence on Initial Conditions

We now examine condition (i) in Devaney's definition more carefully, as it is the aspect of chaos most relevant to applications.

### 6.2.1 Formal Definition

**Definition 6.5 (Sensitive dependence on initial conditions).** Let $(X, d)$ be a metric space and $f: X \to X$. The map $f$ has *sensitive dependence on initial conditions* if there exists a constant $\delta > 0$ (the *sensitivity constant*) such that for every $x \in X$ and every $\epsilon > 0$, there exist $y \in X$ and $n \in \mathbb{N}$ satisfying:

$$d(x, y) < \epsilon \quad \text{and} \quad d(f^n(x), f^n(y)) > \delta.$$

The quantifier structure matters: $\delta$ is *universal* (it does not depend on $x$ or $\epsilon$), while $y$ and $n$ depend on both $x$ and $\epsilon$. In other words, every point has nearby points whose orbits eventually diverge by at least $\delta$, no matter how close "nearby" means.

**Example 6.6 (The doubling map).** Consider $f: [0,1) \to [0,1)$ defined by $f(x) = 2x \pmod{1}$. We claim $f$ has sensitive dependence with $\delta = 1/4$. Given any $x \in [0,1)$ and $\epsilon > 0$, choose $n$ large enough that $2^n \epsilon > 1$. For any $y$ with $|x - y| < \epsilon$ but $y \neq x$, the iterates $f^n(x)$ and $f^n(y)$ differ by $|2^n x - 2^n y| \pmod{1}$. Since $2^n |x - y|$ grows without bound, there exists an iterate for which this distance (mod 1) exceeds $1/4$. A precise argument uses binary expansions; see Section 6.6.

### 6.2.2 The Butterfly Effect

The phrase "butterfly effect" is popularly attributed to Edward Lorenz, though his actual 1972 talk was titled "Does the Flap of a Butterfly's Wings in Brazil Set Off a Tornado in Texas?" The underlying discovery, however, dates to 1961.

Lorenz was running numerical simulations of a simplified atmospheric model (the system we now call the Lorenz equations; see Section 6.4.1). To restart a computation partway through, he entered initial conditions rounded to three decimal places instead of the six his computer stored internally. The resulting trajectory diverged completely from the original within a short time.

This was not a numerical artifact. Lorenz realized that deterministic systems could be *practically unpredictable*: even if the governing equations are known perfectly, unmeasurably small errors in the initial state grow exponentially over time, rendering long-term forecasts impossible. He published this observation in his landmark 1963 paper, "Deterministic Nonperiodic Flow."

**Why this matters for prediction.** Suppose errors grow as $\|\delta(t)\| \approx \|\delta(0)\| \, e^{\lambda t}$ for some $\lambda > 0$. If our initial measurement has precision $\epsilon$ and we need predictions accurate to tolerance $\Delta$, then the *prediction horizon* is approximately:

$$T_{\text{predict}} \approx \frac{1}{\lambda} \ln \frac{\Delta}{\epsilon}.$$

This grows only *logarithmically* with measurement precision. Improving our instruments by a factor of 1000 buys us only $\frac{\ln 1000}{\lambda} \approx \frac{6.9}{\lambda}$ additional time units of prediction. For weather, with $\lambda \approx 1/\text{day}$, this means roughly one extra week — regardless of how much we improve our measurements. This is the fundamental barrier Lorenz identified.

---

## 6.3 Lyapunov Exponents

Sensitive dependence on initial conditions is a qualitative property: either orbits separate or they do not. *Lyapunov exponents* provide a quantitative measure: they tell us the *rate* of exponential divergence (or convergence) of nearby orbits.

### 6.3.1 Definition for One-Dimensional Maps

Let $f: \mathbb{R} \to \mathbb{R}$ be a differentiable map and let $x_0$ be an initial condition with orbit $x_0, x_1 = f(x_0), x_2 = f(x_1), \ldots$

Consider a small perturbation $x_0 + \epsilon$. After one iterate, the perturbed orbit is approximately $f(x_0 + \epsilon) \approx f(x_0) + f'(x_0)\epsilon$, so the perturbation has been multiplied by $|f'(x_0)|$. After $n$ iterates, the chain rule gives:

$$f^n(x_0 + \epsilon) - f^n(x_0) \approx \epsilon \prod_{k=0}^{n-1} f'(x_k).$$

We define the *finite-time Lyapunov exponent* as the average logarithmic stretching rate:

$$\lambda_n(x_0) = \frac{1}{n} \sum_{k=0}^{n-1} \ln |f'(x_k)| = \frac{1}{n} \ln \prod_{k=0}^{n-1} |f'(x_k)|.$$

**Definition 6.7 (Lyapunov exponent for a 1D map).** The *Lyapunov exponent* of $f$ at $x_0$ is

$$\lambda(x_0) = \lim_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} \ln |f'(x_k)|,$$

provided the limit exists.

**Interpretation.** If $\lambda > 0$, nearby orbits diverge exponentially at rate $e^{\lambda}$ per iterate on average. If $\lambda < 0$, they converge. If $\lambda = 0$, the behavior is sub-exponential (often power-law). A positive Lyapunov exponent is the hallmark of chaos.

**Remark on existence.** The limit need not exist for every orbit. However, when $f$ preserves an ergodic measure $\mu$, the Birkhoff ergodic theorem (Chapter 9) guarantees that $\lambda(x_0)$ exists and equals the same value $\lambda = \int \ln |f'| \, d\mu$ for $\mu$-almost every $x_0$. This connects Lyapunov exponents directly to ergodic theory.

### 6.3.2 Worked Examples

**Example 6.8 (The doubling map).** Let $f(x) = 2x \pmod{1}$ on $[0,1)$. Then $f'(x) = 2$ everywhere (where defined), so:

$$\lambda = \lim_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} \ln|2| = \ln 2 \approx 0.693.$$

The Lyapunov exponent is $\ln 2$ for every orbit. This is consistent with what we already know: the doubling map doubles distances at each step (before the mod operation), and $\ln 2 > 0$ confirms sensitive dependence.

**Example 6.9 (The logistic map at $r = 4$).** Consider $f(x) = 4x(1-x)$ on $[0,1]$. We compute $f'(x) = 4(1-2x)$. Rather than trying to evaluate the sum directly along a generic orbit, we exploit a conjugacy.

The change of variables $x = \sin^2(\pi\theta/2)$ (equivalently, $\theta = \frac{2}{\pi}\arcsin(\sqrt{x})$) conjugates $f$ to the *tent map* $g(\theta) = \min(2\theta, 2-2\theta)$ on $[0,1]$, which is in turn semi-conjugate to the doubling map.

More precisely, $f$ preserves the measure $d\mu = \frac{1}{\pi\sqrt{x(1-x)}} dx$ (the arcsine distribution), and with respect to this measure, the system is ergodic. The Lyapunov exponent is:

$$\lambda = \int_0^1 \ln|f'(x)| \, d\mu(x) = \int_0^1 \ln|4(1-2x)| \cdot \frac{1}{\pi\sqrt{x(1-x)}} \, dx.$$

We evaluate this by substituting $x = \sin^2(\pi\theta/2)$, so $dx = \pi\sin(\pi\theta/2)\cos(\pi\theta/2) \, d\theta$ and $\sqrt{x(1-x)} = \sin(\pi\theta/2)\cos(\pi\theta/2)$. Then:

$$\lambda = \int_0^1 \ln|4\cos(\pi\theta)| \, d\theta = \int_0^1 \ln 4 \, d\theta + \int_0^1 \ln|\cos(\pi\theta)| \, d\theta.$$

The first integral is $\ln 4$. For the second, the classical result (see, e.g., Gradshteyn and Ryzhik, 4.384.1) gives:

$$\int_0^1 \ln|\cos(\pi\theta)| \, d\theta = -\ln 2.$$

Therefore:

$$\lambda = \ln 4 - \ln 2 = \ln 2.$$

The logistic map at $r = 4$ has the same Lyapunov exponent as the doubling map. This is not a coincidence: the two maps are measure-theoretically isomorphic (a fact we will make precise in Chapter 8).

**Example 6.10 (The Hénon map).** The Hénon map (Section 6.4.3) is a two-dimensional system with two Lyapunov exponents. At the classical parameters $a = 1.4$, $b = 0.3$, numerical computation gives:

$$\lambda_1 \approx 0.42, \quad \lambda_2 \approx -1.62.$$

The positive first exponent indicates chaos, while the strongly negative second exponent reflects the area contraction (the Jacobian determinant is $-b = -0.3$, so $\lambda_1 + \lambda_2 = \ln|b| = \ln 0.3 \approx -1.20$). This is consistent with the numerical values above.

### 6.3.3 The Lyapunov Spectrum in Higher Dimensions

For a differentiable map $f: \mathbb{R}^d \to \mathbb{R}^d$, nearby points are separated by the Jacobian matrix $Df(x)$. After $n$ iterates starting from $x_0$, the cumulative effect is captured by the matrix product:

$$M_n(x_0) = Df(x_{n-1}) \cdot Df(x_{n-2}) \cdots Df(x_0),$$

where $x_k = f^k(x_0)$. The Lyapunov exponents are defined as the exponential growth rates of this product. More precisely, they are determined by the singular values of $M_n$.

**Definition 6.11 (Lyapunov spectrum).** The *Lyapunov exponents* $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d$ are defined by:

$$\lambda_i = \lim_{n \to \infty} \frac{1}{n} \ln \sigma_i(M_n(x_0)),$$

where $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_d$ are the singular values of $M_n(x_0)$, provided these limits exist.

Equivalently, $\lambda_1$ is the growth rate of the largest singular value (the rate at which the most-stretched direction stretches), $\lambda_1 + \lambda_2$ is the growth rate of the largest 2D area element, and so on.

For continuous-time systems $\dot{x} = F(x)$, the definition is analogous but with $M_n$ replaced by the fundamental matrix solution of the variational equation $\dot{Y} = DF(x(t)) Y$ evaluated at time $t$, and $1/n$ replaced by $1/t$ as $t \to \infty$.

### 6.3.4 The Oseledets Multiplicative Ergodic Theorem

The existence of Lyapunov exponents for the examples above relied on specific computations. In general, one needs a deep theorem to guarantee existence and to relate the exponents to the geometry of the dynamics.

**Theorem 6.12 (Oseledets, 1968).** *Let $f: M \to M$ be a diffeomorphism of a compact Riemannian manifold preserving an ergodic probability measure $\mu$, and suppose $\ln^+ \|Df\| \in L^1(\mu)$. Then there exist numbers $\lambda_1 > \lambda_2 > \cdots > \lambda_s$ (the distinct Lyapunov exponents) and a $\mu$-a.e. defined measurable splitting of the tangent bundle*

$$T_x M = E_1(x) \oplus E_2(x) \oplus \cdots \oplus E_s(x)$$

*such that for $\mu$-almost every $x$ and every nonzero $v \in E_i(x)$:*

$$\lim_{n \to \infty} \frac{1}{n} \ln \|Df^n(x) v\| = \lambda_i.$$

*The subspaces $E_i(x)$ are called the Oseledets subspaces, and $m_i = \dim E_i(x)$ is the multiplicity of $\lambda_i$. The collection $\{(\lambda_i, m_i)\}_{i=1}^s$ is the Lyapunov spectrum.*

**Significance.** The Oseledets theorem is the multiplicative analogue of the Birkhoff ergodic theorem (Chapter 9). While Birkhoff's theorem concerns the convergence of *additive* averages $\frac{1}{n}\sum_{k=0}^{n-1} g(f^k(x))$, the Oseledets theorem concerns the convergence of *multiplicative* averages — products of matrices $Df(x_k)$ — which is a fundamentally harder problem because matrices do not commute.

The theorem tells us that:
- The Lyapunov exponents exist almost everywhere (we are not relying on special orbits).
- The tangent space at each point decomposes into directions of definite exponential growth/decay rates.
- These rates are the same for almost every starting point (by ergodicity).

This theorem is foundational for the ergodic theory of smooth dynamical systems. It underpins Pesin theory (the study of nonuniformly hyperbolic systems), which we will encounter in Chapter 12.

---

## 6.4 Strange Attractors

### 6.4.1 Attractors: Formal Definitions

Informally, an attractor is a set toward which typical orbits converge. Making this precise requires some care.

**Definition 6.13 (Attractor).** Let $f: X \to X$ be a continuous map on a metric space $X$. A compact set $A \subseteq X$ is an *attractor* if:

1. **Invariance.** $f(A) = A$.
2. **Attracting.** There exists an open neighborhood $U$ of $A$ (called the *basin of attraction*) such that for every $x \in U$, $d(f^n(x), A) \to 0$ as $n \to \infty$.
3. **Topological transitivity (indecomposability).** $f|_A$ is topologically transitive: for every pair of nonempty open sets $V, W \subseteq A$ (in the subspace topology), there exists $n$ with $f^n(V) \cap W \neq \emptyset$.

Condition (3) prevents us from calling the union of two disjoint attractors a single "attractor." It ensures that the attractor is dynamically irreducible.

**Definition 6.14 (Basin of attraction).** The *basin of attraction* of an attractor $A$ is:

$$\mathcal{B}(A) = \{x \in X : d(f^n(x), A) \to 0 \text{ as } n \to \infty\}.$$

### 6.4.2 Regular vs. Strange Attractors

**Regular attractors** are the attractors we encountered in earlier chapters:

- **Fixed points.** A stable fixed point $x^*$ is an attractor consisting of a single point.
- **Limit cycles.** A stable periodic orbit $\{x_0, x_1, \ldots, x_{p-1}\}$ (discrete) or a stable closed orbit $\gamma$ (continuous) is an attractor.
- **Invariant tori.** In systems with multiple incommensurate frequencies, the attractor can be a torus $\mathbb{T}^k$, supporting quasiperiodic motion.

These attractors have integer topological dimension (0, 1, or 2 respectively) and the dynamics on them is relatively simple (stationary, periodic, or quasiperiodic).

**Definition 6.15 (Strange attractor, informal).** An attractor is called *strange* if it has fractal structure (non-integer dimension) and supports sensitive dependence on initial conditions.

**Remark.** There is no single universally agreed-upon definition. Some authors use "strange" to refer only to the fractal geometry, regardless of the dynamics (so that a "strange nonchaotic attractor" is possible — and such objects do exist; see Grebogi et al., 1984). Others require both fractal geometry and chaos. We adopt the latter convention: for us, a strange attractor is an attractor with fractal structure on which the dynamics is chaotic.

### 6.4.3 The Lorenz Attractor

The Lorenz system is arguably the most important example in the theory of chaos. It was introduced by the meteorologist Edward Lorenz in 1963 as a drastically simplified model of atmospheric convection, derived from a truncation of the Navier-Stokes equations.

**The equations.** The Lorenz system is:

$$\dot{x} = \sigma(y - x), \quad \dot{y} = x(\rho - z) - y, \quad \dot{z} = xy - \beta z,$$

where $\sigma$, $\rho$, and $\beta$ are positive parameters. The classical values are:

$$\sigma = 10, \quad \rho = 28, \quad \beta = 8/3.$$

Here $x$ represents the intensity of convective motion, $y$ represents the temperature difference between ascending and descending currents, and $z$ represents the deviation of the vertical temperature profile from linearity. The parameters $\sigma$, $\rho$, $\beta$ correspond to the Prandtl number, the Rayleigh number (normalized), and a geometric factor, respectively.

**Symmetry and dissipation.** The system has the symmetry $(x, y, z) \mapsto (-x, -y, z)$, reflecting the physical equivalence of clockwise and counterclockwise convection. It is also dissipative: the divergence of the vector field is:

$$\nabla \cdot F = \frac{\partial \dot{x}}{\partial x} + \frac{\partial \dot{y}}{\partial y} + \frac{\partial \dot{z}}{\partial z} = -\sigma - 1 - \beta < 0.$$

For the classical parameters, $\nabla \cdot F = -10 - 1 - 8/3 \approx -13.67$. By Liouville's theorem, phase-space volumes contract at rate $e^{-13.67 \, t}$, so all trajectories are eventually attracted to a set of zero volume. Yet this set can (and does) have complex geometry.

**Equilibria.** Setting $\dot{x} = \dot{y} = \dot{z} = 0$:

- For $\rho < 1$: the origin is the only equilibrium and is globally attracting.
- For $\rho > 1$: the origin becomes unstable (a pitchfork bifurcation), and two new equilibria appear at $C^{\pm} = (\pm\sqrt{\beta(\rho-1)}, \pm\sqrt{\beta(\rho-1)}, \rho-1)$. For the classical parameters, $C^{\pm} = (\pm 6\sqrt{2}, \pm 6\sqrt{2}, 27)$.
- At $\rho \approx 24.74$ (for the standard $\sigma, \beta$), $C^{\pm}$ lose stability via a subcritical Hopf bifurcation. For $\rho = 28$, all three equilibria are unstable, and trajectories wander in a bounded region without settling down.

**The geometric structure.** The Lorenz attractor has the iconic "butterfly" shape: two wing-like lobes centered near $C^+$ and $C^-$. A typical trajectory spirals outward around one equilibrium, then crosses to the other wing and spirals outward around the other equilibrium, switching back and forth in an aperiodic pattern.

The mechanism producing this behavior is *stretching and folding*. Nearby trajectories on one wing separate exponentially (stretching). When they cross to the other wing, the trajectories from different parts of the wing are brought together (folding). This process, repeated infinitely, produces the fractal layered structure of the attractor.

**Lyapunov exponents.** Numerical computation gives the Lyapunov spectrum for the classical Lorenz attractor:

$$\lambda_1 \approx 0.906, \quad \lambda_2 \approx 0, \quad \lambda_3 \approx -14.57.$$

The positive exponent confirms chaos. The zero exponent corresponds to the flow direction (a general feature of continuous-time autonomous systems — perturbations along the trajectory neither grow nor shrink). The large negative exponent reflects the strong dissipation.

**Tucker's theorem.** For decades, the existence of the Lorenz attractor as a genuine mathematical object (not merely a numerical artifact) remained an open problem. It was the 14th problem on Smale's list of problems for the 21st century. This was resolved by Warwick Tucker in 1999 (published 2002), using rigorous computer-assisted methods.

**Theorem 6.16 (Tucker, 2002).** *For the classical parameter values $\sigma = 10$, $\rho = 28$, $\beta = 8/3$, the Lorenz equations have a robust strange attractor. Specifically, the flow admits a "geometric Lorenz attractor" — a compact invariant set that is topologically transitive, supports a unique SRB measure, and has sensitive dependence on initial conditions.*

Tucker's proof uses interval arithmetic to rigorously bound all numerical errors, combined with a careful analysis of the return map to a cross-section of the flow. The key idea is to verify the geometric conditions identified by Afraimovich, Bykov, and Shil'nikov (1977) and by Guckenheimer and Williams (1979) that guarantee the existence of a strange attractor for flows with the qualitative features of the Lorenz system.

### 6.4.4 The Rössler Attractor

The Rössler system, introduced by Otto Rössler in 1976, provides a simpler example of a strange attractor in three dimensions:

$$\dot{x} = -y - z, \quad \dot{y} = x + ay, \quad \dot{z} = b + z(x - c),$$

with typical parameters $a = 0.2$, $b = 0.2$, $c = 5.7$.

Unlike the Lorenz attractor, which has the symmetry $(x,y,z) \mapsto (-x,-y,z)$ and two "wings," the Rössler attractor has a single band-like structure that twists and folds. The mechanism is simpler to visualize: trajectories spiral outward in the $(x,y)$-plane, and when $x$ becomes large enough, the $z$-variable activates and "resets" the trajectory back toward the center.

Depending on the parameter $c$, the Rössler attractor exhibits different types:

- **Band type** (e.g., $c = 5.7$): the attractor resembles a Möbius-like band with a single fold. The return map to a cross-section is approximately one-dimensional and unimodal, similar to the logistic map.
- **Funnel type** (e.g., $c = 18$): the attractor has a more complex structure with trajectories making varying numbers of loops before reinjection.

The Rössler system is particularly useful for studying the transition from periodic to chaotic behavior via period-doubling cascades (Chapter 5), because the effectively one-dimensional return map makes the analysis more tractable than for the Lorenz system.

**Lyapunov exponents** for the classical Rössler attractor ($a = b = 0.2$, $c = 5.7$):

$$\lambda_1 \approx 0.07, \quad \lambda_2 \approx 0, \quad \lambda_3 \approx -5.39.$$

### 6.4.5 The Hénon Map

The Hénon map, introduced by Michel Hénon in 1976 as a simplified model of the Poincaré section of the Lorenz system, is a two-dimensional map:

$$x_{n+1} = 1 - ax_n^2 + y_n, \quad y_{n+1} = bx_n,$$

with classical parameters $a = 1.4$, $b = 0.3$.

**Properties.** The Jacobian is

$$D f(x,y) = \begin{pmatrix} -2ax & 1 \\ b & 0 \end{pmatrix}$$

with determinant $\det Df = -b$. For $b = 0.3$, each iterate contracts areas by a factor of $0.3$. For $b \neq 0$, the map is a diffeomorphism (it is invertible):

$$x_n = y_{n+1}/b, \quad y_n = x_{n+1} - 1 + a(y_{n+1}/b)^2.$$

For $b = 0$, the Hénon map reduces to the one-dimensional quadratic map $x_{n+1} = 1 - ax_n^2$, which is conjugate to the logistic map. Thus the Hénon map can be viewed as a "thickened" version of the logistic map.

**The Benedicks-Carleson theorem.** The question of whether the numerically observed Hénon attractor is a genuine strange attractor (as opposed to a very long transient, or a stable periodic orbit of very high period) is subtle. For decades it remained an open problem. The breakthrough came with the following result.

**Theorem 6.17 (Benedicks and Carleson, 1991).** *There exists a set of positive Lebesgue measure in the parameter space $(a,b)$, with $b > 0$ small, such that the Hénon map $f_{a,b}$ has a "genuine" strange attractor: it supports a unique ergodic SRB (Sinai-Ruelle-Bowen) measure with a positive Lyapunov exponent.*

The proof is technically formidable. It extends the methods of Jakobson (1981), who proved the analogous result for the one-dimensional quadratic family, to the two-dimensional setting. The key difficulty is controlling the recurrence of the "critical point" (or rather, the critical region where the map is strongly contracting in one direction), ensuring that the orbit of this region does not return too quickly.

**Remark.** Benedicks and Carleson's result applies for $b$ small and positive. Whether it holds at the "classical" value $b = 0.3$ with $a = 1.4$ is a separate, harder question that remains open, though all numerical evidence supports it.

---

## 6.5 Fractal Dimension

Strange attractors have intricate geometric structure that cannot be captured by integer dimensions. We need a notion of dimension that can take non-integer values.

### 6.5.1 Box-Counting Dimension

**Definition 6.18 (Box-counting dimension).** Let $A \subseteq \mathbb{R}^d$ be a bounded set. For $\epsilon > 0$, let $N(\epsilon)$ be the minimum number of $d$-dimensional cubes (boxes) of side length $\epsilon$ needed to cover $A$. The *box-counting dimension* (also called the *Minkowski dimension* or *capacity dimension*) of $A$ is:

$$\dim_B(A) = \lim_{\epsilon \to 0} \frac{\ln N(\epsilon)}{\ln(1/\epsilon)},$$

provided the limit exists. If the limit does not exist, one defines upper and lower box-counting dimensions using $\limsup$ and $\liminf$.

**Intuition.** For a "smooth" set of dimension $d$, we expect $N(\epsilon) \sim C \epsilon^{-d}$ as $\epsilon \to 0$, so $\frac{\ln N(\epsilon)}{\ln(1/\epsilon)} \to d$. The box-counting dimension generalizes this to sets where the exponent is not an integer.

**Example 6.19 (A line segment).** A line segment of length $L$ in $\mathbb{R}^2$ requires $N(\epsilon) \sim L/\epsilon$ boxes, so $\dim_B = \frac{\ln(L/\epsilon)}{\ln(1/\epsilon)} \to 1$.

**Example 6.20 (A filled square).** A square of side $L$ requires $N(\epsilon) \sim (L/\epsilon)^2$ boxes, so $\dim_B = 2$.

**Example 6.21 (The middle-thirds Cantor set).** The Cantor set $C$ is constructed by iteratively removing the middle third of each interval, starting from $[0,1]$. At stage $n$, the set consists of $2^n$ intervals of length $3^{-n}$. Taking $\epsilon = 3^{-n}$:

$$N(\epsilon) = 2^n, \quad \text{so} \quad \dim_B(C) = \lim_{n \to \infty} \frac{\ln 2^n}{\ln 3^n} = \frac{n \ln 2}{n \ln 3} = \frac{\ln 2}{\ln 3} \approx 0.631.$$

The Cantor set has dimension strictly between 0 and 1: it is "more" than a finite collection of points but "less" than an interval.

### 6.5.2 Hausdorff Dimension

Box-counting dimension is easy to compute but has some mathematical deficiencies. For instance, a countable dense set has box-counting dimension equal to the dimension of the ambient space, which is arguably the "wrong" answer. The Hausdorff dimension, introduced by Felix Hausdorff in 1918, is the more fundamental notion.

**Definition 6.22 (Hausdorff measure and dimension).** For $A \subseteq \mathbb{R}^d$ and $s \geq 0$, define the *$s$-dimensional Hausdorff measure* of $A$ as:

$$\mathcal{H}^s(A) = \lim_{\delta \to 0} \inf \left\{ \sum_{i=1}^{\infty} (\operatorname{diam} U_i)^s : A \subseteq \bigcup_{i=1}^{\infty} U_i, \; \operatorname{diam} U_i \leq \delta \right\}.$$

The infimum is over all countable covers of $A$ by sets of diameter at most $\delta$. The *Hausdorff dimension* of $A$ is:

$$\dim_H(A) = \inf\{s \geq 0 : \mathcal{H}^s(A) = 0\} = \sup\{s \geq 0 : \mathcal{H}^s(A) = \infty\}.$$

**Why this is the "right" definition.** The Hausdorff dimension has several properties that box-counting dimension lacks:

- $\dim_H(\text{countable set}) = 0$ (correct!).
- $\dim_H$ is countably stable: $\dim_H(\bigcup_{i=1}^\infty A_i) = \sup_i \dim_H(A_i)$.
- $\dim_H(A) \leq \dim_B(A)$ always, and equality holds for many "nice" fractal sets (including all self-similar sets satisfying the open set condition).

For the Cantor set, $\dim_H(C) = \ln 2 / \ln 3$, agreeing with the box-counting dimension. For self-similar fractals in general, the Hausdorff dimension is given by the solution of Moran's equation.

### 6.5.3 Information and Correlation Dimensions

For attractors of dynamical systems, we often care not just about the geometry of the set but about how the invariant measure distributes mass on it. This leads to a family of *generalized dimensions*.

**Definition 6.23 (Information dimension).** Let $\mu$ be the natural measure on an attractor. Cover the attractor with boxes of side $\epsilon$ and let $p_i$ be the $\mu$-measure of the $i$-th box. The *information dimension* is:

$$d_1 = \lim_{\epsilon \to 0} \frac{\sum_i p_i \ln p_i}{\ln \epsilon}.$$

The numerator is the Shannon entropy of the partition, so $d_1$ measures the rate at which information is needed to specify a point on the attractor as the resolution increases.

**Definition 6.24 (Correlation dimension).** The *correlation dimension* $d_2$ is defined via the *correlation integral*:

$$C(\epsilon) = \lim_{N \to \infty} \frac{1}{N^2} \#\{(i,j) : \|x_i - x_j\| < \epsilon, \; i \neq j\},$$

where $x_1, x_2, \ldots, x_N$ are points on the attractor (e.g., from a long orbit). Then:

$$d_2 = \lim_{\epsilon \to 0} \frac{\ln C(\epsilon)}{\ln \epsilon}.$$

The correlation dimension was introduced by Grassberger and Procaccia (1983) and is the most commonly used dimension in practice, because it can be estimated efficiently from time series data. One has the general inequality:

$$d_2 \leq d_1 \leq \dim_B.$$

For many "typical" attractors these dimensions are close but not exactly equal.

### 6.5.4 The Kaplan-Yorke Conjecture

There is a beautiful conjectured relationship between the fractal dimension of an attractor and the Lyapunov exponents of the dynamics on it.

**Definition 6.25 (Kaplan-Yorke dimension).** Given the ordered Lyapunov exponents $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d$, let $j$ be the largest integer such that $\sum_{i=1}^j \lambda_i \geq 0$. The *Kaplan-Yorke dimension* (or *Lyapunov dimension*) is:

$$d_{KY} = j + \frac{\sum_{i=1}^j \lambda_i}{|\lambda_{j+1}|}.$$

**Conjecture 6.26 (Kaplan and Yorke, 1979).** *For "typical" attractors, the information dimension $d_1$ equals the Kaplan-Yorke dimension $d_{KY}$.*

This conjecture has been proven in certain cases (e.g., for two-dimensional systems by Young, 1982) and is supported by extensive numerical evidence, but remains open in full generality.

**Example 6.27 (Kaplan-Yorke dimension of the Lorenz attractor).** Using $\lambda_1 \approx 0.906$, $\lambda_2 = 0$, $\lambda_3 \approx -14.57$:

$$j = 2, \quad d_{KY} = 2 + \frac{0.906 + 0}{14.57} \approx 2.06.$$

This is consistent with the numerically estimated fractal dimension of the Lorenz attractor ($\approx 2.06$). The attractor is a "thin" fractal layer — very nearly a surface, but with a dimension slightly above 2 due to the fractal folding structure.

**Example 6.28 (Kaplan-Yorke dimension of the Hénon attractor).** Using $\lambda_1 \approx 0.42$, $\lambda_2 \approx -1.62$:

$$j = 1, \quad d_{KY} = 1 + \frac{0.42}{1.62} \approx 1.26.$$

This agrees well with the numerically estimated box-counting dimension of the Hénon attractor ($\approx 1.26$). The attractor is slightly "thicker" than a curve but much thinner than a surface, consistent with its visual appearance as a system of nearly parallel curves.

---

## 6.6 Symbolic Dynamics

Symbolic dynamics provides a powerful combinatorial framework for analyzing chaotic systems. The idea is to replace a continuous dynamical system with a discrete one on a space of symbol sequences, where the analysis becomes more tractable.

### 6.6.1 Itineraries and Symbol Sequences

Consider a map $f: X \to X$ and a partition of $X$ into finitely many regions $\{P_0, P_1, \ldots, P_{k-1}\}$. Given an initial point $x \in X$, we record which partition element is visited at each time step.

**Definition 6.29 (Itinerary).** The *itinerary* of $x$ with respect to the partition $\{P_i\}$ is the sequence $s(x) = (s_0, s_1, s_2, \ldots)$ where $s_n \in \{0, 1, \ldots, k-1\}$ and $f^n(x) \in P_{s_n}$.

The itinerary is an element of the *sequence space* $\Sigma_k = \{0, 1, \ldots, k-1\}^{\mathbb{N}_0}$, the set of all one-sided infinite sequences over $k$ symbols. We equip $\Sigma_k$ with the metric:

$$d(s, t) = \sum_{n=0}^{\infty} \frac{|s_n - t_n|}{k^n},$$

which makes $\Sigma_k$ a compact metric space. Two sequences are close in this metric if and only if they agree on a long initial segment.

### 6.6.2 The Shift Map

**Definition 6.30 (Shift map).** The *(one-sided) shift map* $\sigma: \Sigma_k \to \Sigma_k$ is defined by:

$$\sigma(s_0, s_1, s_2, \ldots) = (s_1, s_2, s_3, \ldots).$$

It simply discards the first symbol and shifts the rest to the left.

**Proposition 6.31.** *The shift map $\sigma: \Sigma_k \to \Sigma_k$ (for $k \geq 2$) is chaotic in the sense of Devaney.*

*Proof.* We verify each condition.

(i) *Dense periodic orbits.* A sequence $s = (s_0, s_1, \ldots, s_{p-1}, s_0, s_1, \ldots, s_{p-1}, \ldots)$ is periodic with period $p$ under $\sigma$. Given any sequence $t \in \Sigma_k$ and any $\epsilon > 0$, choose $N$ large enough that $k^{-N} < \epsilon$. Define the periodic sequence $s$ by repeating the block $(t_0, t_1, \ldots, t_{N-1})$. Then $d(s, t) \leq \sum_{n=N}^{\infty} (k-1)/k^n < \epsilon$ (after adjusting constants), so $s$ is within $\epsilon$ of $t$. Hence periodic points are dense.

(ii) *Topological transitivity.* We construct a point whose orbit is dense. Enumerate all finite strings of length 1, then length 2, then length 3, etc., and concatenate them into a single infinite sequence $s^*$. Then for any open set $U$ in $\Sigma_k$, any sequence in $U$ must share a long initial block with some iterate of $s^*$ (since that block appears as a substring of $s^*$, and shifting brings it to the front). Thus the orbit of $s^*$ is dense.

(iii) *Sensitive dependence on initial conditions.* Take $\delta = 1$ (or any constant less than 1 for the normalized metric). Given any $s \in \Sigma_k$ and $\epsilon > 0$, choose $N$ with $k^{-N} < \epsilon$ and define $t$ by $t_n = s_n$ for $n < N$ and $t_N \neq s_N$. Then $d(s, t) < \epsilon$ but $d(\sigma^N(s), \sigma^N(t)) \geq |s_N - t_N|/k^0 \cdot (\text{leading term}) > 0$. More precisely, since the first symbols of $\sigma^N(s)$ and $\sigma^N(t)$ differ, $d(\sigma^N(s), \sigma^N(t)) \geq 1/k$.

By Theorem 6.2, conditions (ii) and (iii) alone suffice, but we have verified all three directly. $\square$

### 6.6.3 Conjugacy with Chaotic Maps

The power of symbolic dynamics lies in the following idea: if we can find a topological conjugacy (or semi-conjugacy) between a chaotic map $f$ and a shift map $\sigma$, then the symbolic dynamics of $\sigma$ completely describes the dynamics of $f$.

**Definition 6.32 (Topological conjugacy).** Two dynamical systems $f: X \to X$ and $g: Y \to Y$ are *topologically conjugate* if there exists a homeomorphism $h: X \to Y$ such that $h \circ f = g \circ h$, i.e., the following diagram commutes:

$$X \xrightarrow{f} X$$
$$\downarrow h \qquad \downarrow h$$
$$Y \xrightarrow{g} Y$$

If $h$ is merely a continuous surjection (not necessarily a homeomorphism), we say $f$ and $g$ are *semi-conjugate*.

### 6.6.4 The Doubling Map and Binary Expansions

The doubling map $f(x) = 2x \pmod{1}$ on $[0,1)$ provides the cleanest example of the connection to symbolic dynamics.

Every $x \in [0,1)$ has a binary expansion $x = 0.b_1 b_2 b_3 \ldots$ (in base 2), where $b_i \in \{0, 1\}$. The action of the doubling map on this expansion is:

$$f(0.b_1 b_2 b_3 \ldots) = 0.b_2 b_3 b_4 \ldots$$

This is exactly the shift map! More precisely, define the *coding map* $h: [0,1) \to \Sigma_2$ by $h(x) = (b_1, b_2, b_3, \ldots)$, the binary expansion of $x$. Then:

$$h \circ f = \sigma \circ h.$$

The map $h$ is not quite a homeomorphism (binary expansions are not unique for dyadic rationals, e.g., $0.0111\ldots = 0.1000\ldots$), so this is a semi-conjugacy. However, the set of dyadic rationals is countable (hence negligible for most purposes), and the correspondence is otherwise one-to-one.

**Consequences.** Since the shift map on $\Sigma_2$ is chaotic (Proposition 6.31), and semi-conjugacy preserves many dynamical properties, the doubling map is chaotic. More concretely:

- *Dense periodic orbits.* Periodic orbits of the doubling map correspond to eventually repeating binary expansions, i.e., rational numbers with odd denominators. These are dense in $[0,1)$.
- *Topological transitivity.* The orbit of the point $x^*$ whose binary expansion concatenates all finite binary strings (the Champernowne-like construction) is dense.
- *Sensitive dependence.* Two points that agree in the first $n$ binary digits but differ in the $(n+1)$-st will have $f^n$-images that differ in the first digit, hence are at least $1/4$ apart.

**Example 6.33 (Counting periodic orbits).** How many periodic orbits of period $n$ does the doubling map have? A periodic orbit of period $n$ corresponds to a repeating binary block of length $n$: $x = 0.\overline{b_1 b_2 \ldots b_n}$. The number of binary strings of length $n$ is $2^n$, and each period-$n$ orbit contains exactly $n$ points, so the number of orbits of *exact* period $n$ is:

$$\frac{1}{n}\sum_{d \mid n} \mu(n/d) \, 2^d,$$

where $\mu$ is the Möbius function (this counts primitive necklaces). For large $n$, this is approximately $2^n/n$, confirming that the number of periodic orbits grows exponentially.

---

## 6.7 Takens' Embedding Theorem

We close this chapter with a theorem that bridges the gap between theory and applications, and which will play a central role in Part III when we discuss reservoir computing.

### 6.7.1 The Problem

Suppose a deterministic dynamical system $f: M \to M$ on a $d$-dimensional manifold $M$ produces complicated (possibly chaotic) behavior. In practice, we rarely observe the full state $x \in M$. Instead, we measure a single scalar observable $\phi: M \to \mathbb{R}$ (e.g., one component of the state, or a temperature reading, or a voltage signal). The resulting data is a scalar time series:

$$\phi(x_0), \; \phi(x_1), \; \phi(x_2), \; \ldots$$

where $x_n = f^n(x_0)$.

**The question.** Can we reconstruct the geometry and dynamics of the attractor from this scalar time series alone?

The answer, remarkably, is *yes* — under generic conditions.

### 6.7.2 Delay Coordinate Embedding

Given the scalar time series $\{y_n\} = \{\phi(f^n(x_0))\}$, we form *delay vectors*:

$$\mathbf{y}_n = (y_n, y_{n+\tau}, y_{n+2\tau}, \ldots, y_{n+(m-1)\tau}) \in \mathbb{R}^m,$$

where $\tau \geq 1$ is the *delay* (or *lag*) and $m$ is the *embedding dimension*. The collection of delay vectors $\{\mathbf{y}_n\}$ traces out a set in $\mathbb{R}^m$.

**Theorem 6.34 (Takens, 1981).** *Let $M$ be a compact manifold of dimension $d$, let $f: M \to M$ be a $C^2$ diffeomorphism, and let $\phi: M \to \mathbb{R}$ be a $C^2$ function. For generic pairs $(f, \phi)$ (i.e., an open and dense set in the $C^2$ topology), the delay coordinate map*

$$\Phi_{\phi, f}: M \to \mathbb{R}^{2d+1}, \quad \Phi_{\phi, f}(x) = (\phi(x), \phi(f(x)), \phi(f^2(x)), \ldots, \phi(f^{2d}(x)))$$

*is an embedding (i.e., a homeomorphism onto its image whose derivative is injective at every point).*

**Interpretation.** If we take $m = 2d + 1$ delays (with $\tau = 1$, or more generally, with a "generic" delay $\tau$), then the delay coordinate map is one-to-one on $M$ and preserves the topology and differentiable structure. The attractor reconstructed in $\mathbb{R}^{2d+1}$ from the scalar time series is diffeomorphic to the original attractor in $M$.

The bound $2d + 1$ is analogous to the Whitney embedding theorem, which states that any $d$-dimensional manifold can be embedded in $\mathbb{R}^{2d+1}$. The extra $+1$ (compared to $2d$) is needed to ensure injectivity generically.

### 6.7.3 Practical Considerations

**Embedding dimension.** The theorem requires $m \geq 2d + 1$, but $d$ is the dimension of the ambient manifold $M$. In practice, what matters is the dimension of the *attractor* $A \subseteq M$, which may be much smaller than $d$. The question of whether $m \geq 2 \dim_B(A) + 1$ suffices was addressed by Sauer, Yorke, and Casdagli (1991).

**Theorem 6.35 (Sauer, Yorke, and Casdagli, 1991).** *The delay coordinate map $\Phi_{\phi, f}$ is generically one-to-one on a compact set $A \subseteq M$ provided $m > 2 \dim_B(A)$, where $\dim_B(A)$ is the box-counting dimension of $A$.*

This "fractal" version of Takens' theorem is essential in practice. For example, the Lorenz attractor has $\dim_B \approx 2.06$, so $m \geq 5$ should suffice for reconstruction, rather than $m \geq 7$ (which would be required if we only knew $M = \mathbb{R}^3$, giving $2 \cdot 3 + 1 = 7$).

**Choice of delay $\tau$.** The theorem holds for generic $\tau$ (or $\tau = 1$), but in practice the choice of $\tau$ matters for the quality of the reconstruction. If $\tau$ is too small, consecutive delays are highly correlated and the reconstructed attractor is "squashed" along the diagonal. If $\tau$ is too large, consecutive delays become effectively independent and the structure is lost. Common heuristics include choosing $\tau$ as the first zero of the autocorrelation function, or the first minimum of the mutual information.

### 6.7.4 Significance for Reservoir Computing

Takens' theorem guarantees that the geometry and topology of a chaotic attractor can be faithfully reconstructed from a single scalar measurement, using only time-delayed copies of that measurement.

This is directly relevant to reservoir computing (Part III). A reservoir computer processes an input time series through a high-dimensional dynamical system (the "reservoir"), producing a high-dimensional state that encodes the input history. If the reservoir dynamics creates a delay embedding of the input, then the reservoir state faithfully represents the underlying attractor, and a simple linear readout can extract predictions.

More precisely, if the reservoir state at time $n$ depends on the recent input history $(u_n, u_{n-1}, \ldots, u_{n-k})$ in a sufficiently rich way, this is analogous to a delay embedding. The connection between Takens' theorem and the information-processing capacity of reservoirs has been made precise by several authors (see Chapter 16).

This is a deep and somewhat surprising connection: the same theorem that allows physicists to reconstruct attractors from experimental data also explains why reservoir computers can learn to predict chaotic systems.

---

## 6.8 Worked Examples

We consolidate the ideas of this chapter with several extended examples.

**Example 6.36 (Verifying chaos for the doubling map — complete analysis).** We assemble the results obtained throughout this chapter into a complete characterization.

Let $f(x) = 2x \pmod{1}$ on $[0,1)$.

1. *Lyapunov exponent:* $\lambda = \ln 2 > 0$ (Example 6.8).
2. *Sensitive dependence:* with $\delta = 1/4$ (Example 6.6).
3. *Dense periodic orbits:* periodic points are rationals of the form $p/(2^n - 1)$, which are dense.
4. *Topological transitivity:* follows from ergodicity with respect to Lebesgue measure (to be proved in Chapter 9), or directly from the symbolic dynamics (Section 6.6.4).
5. *Fractal dimension of the "attractor":* the map acts on the full interval $[0,1)$, which has dimension 1. The attractor is the entire interval (for Lebesgue-a.e. initial condition).
6. *Symbolic dynamics:* semi-conjugate to the full shift on two symbols.

The doubling map is the "simplest" chaotic system: it exemplifies every concept in this chapter in its most transparent form.

**Example 6.37 (Estimating the correlation dimension from data).** Suppose we generate $N = 10{,}000$ iterates of the Hénon map at $a = 1.4$, $b = 0.3$ and wish to estimate the correlation dimension.

Procedure:
1. Discard the first 1000 iterates as transient.
2. For the remaining points $\{(x_i, y_i)\}_{i=1}^{N'}$, compute the correlation integral:
$$C(\epsilon) = \frac{2}{N'(N'-1)} \sum_{i < j} \mathbf{1}[\|(x_i - x_j, y_i - y_j)\| < \epsilon].$$
3. Plot $\ln C(\epsilon)$ versus $\ln \epsilon$ for a range of $\epsilon$.
4. The slope of the linear region gives $d_2$.

In practice, one finds a slope of approximately $1.21$ to $1.26$, consistent with the Kaplan-Yorke estimate of $\approx 1.26$.

If we instead work with a scalar time series (observing only the $x$-coordinate) and use delay embedding with $m = 3$ and $\tau = 1$, we form vectors $(x_n, x_{n+1}, x_{n+2}) \in \mathbb{R}^3$ and repeat the Grassberger-Procaccia algorithm. The estimated correlation dimension converges to the same value $\approx 1.26$ (provided $m > 2 d_2 \approx 2.52$, which is satisfied since $m = 3$). This is Takens' theorem in action.

**Example 6.38 (Symbolic dynamics of the tent map).** The tent map $T: [0,1] \to [0,1]$ is defined by:

$$T(x) = \begin{cases} 2x & \text{if } x \leq 1/2, \\ 2(1-x) & \text{if } x > 1/2. \end{cases}$$

Partition $[0,1]$ into $P_0 = [0, 1/2)$ and $P_1 = [1/2, 1]$. The itinerary of $x$ is $s(x) = (s_0, s_1, s_2, \ldots)$ where $s_n = 0$ if $T^n(x) < 1/2$ and $s_n = 1$ if $T^n(x) \geq 1/2$.

*Claim:* the itinerary map $s: [0,1] \to \Sigma_2$ is a semi-conjugacy between $T$ and the shift $\sigma$.

To see this, note that $T$ maps $P_0$ linearly onto $[0,1]$ (stretching by a factor of 2) and $P_1$ linearly onto $[0,1]$ (stretching by 2 and reflecting). Thus the symbolic dynamics is equivalent to the full shift on two symbols, confirming that the tent map is chaotic with the same symbolic structure as the doubling map.

The Lyapunov exponent is $\lambda = \ln 2$ (since $|T'(x)| = 2$ wherever $T$ is differentiable), matching the doubling map.

---

## 6.9 Summary

This chapter established the mathematical foundations of chaos and strange attractors.

**Key ideas:**

- *Chaos* (Devaney) requires topological transitivity, dense periodic orbits, and sensitive dependence — but the Banks et al. result shows the first two conditions suffice.
- *Lyapunov exponents* quantify the rate of divergence of nearby orbits. A positive maximal Lyapunov exponent is the signature of chaos. The Oseledets theorem guarantees their existence in the ergodic setting.
- *Strange attractors* are invariant sets with fractal geometry supporting chaotic dynamics. The Lorenz, Rössler, and Hénon attractors are the canonical examples.
- *Fractal dimension* (box-counting, Hausdorff, correlation) quantifies the geometric complexity of attractors. The Kaplan-Yorke conjecture links dimension to Lyapunov exponents.
- *Symbolic dynamics* reduces the study of continuous chaotic systems to combinatorics on symbol sequences.
- *Takens' embedding theorem* guarantees that attractors can be reconstructed from scalar time series, providing the theoretical foundation for data-driven methods including reservoir computing.

**Looking ahead.** We now have the dynamical systems tools needed to study chaos. But we have repeatedly invoked ergodic-theoretic ideas (invariant measures, the Birkhoff ergodic theorem, ergodicity) without proving them. Part II develops this machinery properly, beginning with measure theory in Chapter 7.

---

## Exercises

**Exercise 6.1.** Let $f(x) = 3x \pmod{1}$ on $[0,1)$.
(a) Compute the Lyapunov exponent.
(b) Find the number of fixed points and the number of period-2 orbits.
(c) Show that $f$ is semi-conjugate to the one-sided shift on 3 symbols.
(d) Conclude that $f$ is chaotic in the sense of Devaney.

**Exercise 6.2.** Consider the logistic map $f_r(x) = rx(1-x)$ on $[0,1]$.
(a) Show that $f_r$ has sensitive dependence on initial conditions for $r = 4$ by explicitly constructing, for any $x \in (0,1)$ and any $\epsilon > 0$, a point $y$ with $|x - y| < \epsilon$ and an iterate $n$ with $|f^n(x) - f^n(y)| > 1/4$.
*Hint:* Use the conjugacy to the tent map (or the doubling map) via $x = \sin^2(\pi\theta/2)$.
(b) Compute numerically the Lyapunov exponent $\lambda(r)$ as a function of $r$ for $r \in [2.5, 4]$. Where is $\lambda = 0$? Where is $\lambda > 0$? How does this relate to the bifurcation diagram from Chapter 5?

**Exercise 6.3 (Fractal dimension practice).**
(a) Compute the box-counting dimension of the Sierpinski triangle. *Hint:* At each stage, there are $3^n$ triangles of side length $2^{-n}$.
(b) Compute the box-counting dimension of the Koch curve. *Hint:* At each stage, there are $4^n$ segments of length $3^{-n}$.
(c) Prove that $\dim_H(A) \leq \dim_B(A)$ for any bounded set $A \subseteq \mathbb{R}^d$.

**Exercise 6.4 (Lyapunov exponents and invariant measures).** Consider the map $f(x) = 4x(1-x)$ on $[0,1]$ with invariant measure $d\mu = \frac{1}{\pi\sqrt{x(1-x)}} dx$.
(a) Verify that $\mu$ is a probability measure (i.e., $\mu([0,1]) = 1$).
(b) Verify computationally (by numerical integration or otherwise) that $\int_0^1 \ln|f'(x)| \, d\mu = \ln 2$.
(c) The Birkhoff ergodic theorem implies that for $\mu$-a.e. $x_0$, $\frac{1}{n}\sum_{k=0}^{n-1}\ln|f'(x_k)| \to \ln 2$. Verify this numerically: pick a "random" initial condition, compute $10^6$ iterates, and plot the running average of $\ln|f'(x_k)|$.

**Exercise 6.5 (Takens' embedding).** Consider the Lorenz system with classical parameters. Suppose you observe only the $x$-coordinate, obtaining a time series $\{x(t_n)\}$.
(a) What is the minimum embedding dimension $m$ guaranteed by Takens' theorem (using $d = 3$, the ambient dimension)?
(b) What is the minimum embedding dimension suggested by the Sauer-Yorke-Casdagli theorem (using $\dim_B \approx 2.06$)?
(c) Explain qualitatively why using too small or too large a delay $\tau$ leads to poor reconstructions.

**Exercise 6.6 (Symbolic dynamics and counting).**
(a) For the shift map on $\Sigma_2$, find all periodic orbits of period 4. How many are there?
(b) Show that the number of periodic points of period $n$ (not necessarily with minimal period $n$) of the shift on $\Sigma_k$ is $k^n$.
(c) Use the Möbius inversion formula to derive the exact number of orbits of *minimal* period $n$.
(d) Compute the *topological entropy* of the shift on $\Sigma_k$, defined as $h_{\text{top}} = \lim_{n \to \infty} \frac{1}{n} \ln (\text{number of period-}n \text{ points})$.

**Exercise 6.7 (The Kaplan-Yorke formula).** A four-dimensional system has Lyapunov exponents $\lambda_1 = 0.5$, $\lambda_2 = 0.1$, $\lambda_3 = -0.3$, $\lambda_4 = -1.8$.
(a) Compute the Kaplan-Yorke dimension $d_{KY}$.
(b) What does the sign of $\sum_{i=1}^4 \lambda_i$ tell you about the system? Is it dissipative or conservative?
(c) Is the system chaotic? How do you know?

**Exercise 6.8 (Sensitive dependence is not enough for chaos).** Construct a continuous map $f: [0,1] \to [0,1]$ that has sensitive dependence on initial conditions but is *not* topologically transitive. *Hint:* Consider a map with an attracting fixed point and a repelling fixed point, where orbits between them separate before converging.

---

## References

- Afraimovich, V. S., Bykov, V. V., and Shil'nikov, L. P. (1977). On the origin and structure of the Lorenz attractor. *Dokl. Akad. Nauk SSSR*, 234:336–339.

- Banks, J., Brooks, J., Cairns, G., Davis, G., and Stacey, P. (1992). On Devaney's definition of chaos. *American Mathematical Monthly*, 99(4):332–334.

- Benedicks, M. and Carleson, L. (1991). The dynamics of the Hénon map. *Annals of Mathematics*, 133(1):73–169.

- Devaney, R. L. (1989). *An Introduction to Chaotic Dynamical Systems*. 2nd ed. Addison-Wesley.

- Grassberger, P. and Procaccia, I. (1983). Measuring the strangeness of strange attractors. *Physica D*, 9(1–2):189–208.

- Guckenheimer, J. and Williams, R. F. (1979). Structural stability of Lorenz attractors. *Publications Mathématiques de l'IHÉS*, 50:59–72.

- Hénon, M. (1976). A two-dimensional mapping with a strange attractor. *Communications in Mathematical Physics*, 50:69–77.

- Huang, W. and Ye, X. (2002). Devaney's chaos or 2-scattering implies Li-Yorke's chaos. *Topology and its Applications*, 117:259–272.

- Jakobson, M. V. (1981). Absolutely continuous invariant measures for one-parameter families of one-dimensional maps. *Communications in Mathematical Physics*, 81:39–88.

- Kaplan, J. L. and Yorke, J. A. (1979). Chaotic behavior of multidimensional difference equations. In Peitgen, H.-O. and Walther, H.-O., editors, *Functional Differential Equations and Approximation of Fixed Points*, Lecture Notes in Mathematics 730, pages 204–227. Springer.

- Katok, A. and Hasselblatt, B. (1995). *Introduction to the Modern Theory of Dynamical Systems*. Cambridge University Press.

- Li, T.-Y. and Yorke, J. A. (1975). Period three implies chaos. *American Mathematical Monthly*, 82(10):985–992.

- Lorenz, E. N. (1963). Deterministic nonperiodic flow. *Journal of the Atmospheric Sciences*, 20(2):130–141.

- Oseledets, V. I. (1968). A multiplicative ergodic theorem. Lyapunov characteristic numbers for dynamical systems. *Trudy Moskovskogo Matematicheskogo Obshchestva*, 19:179–210.

- Ott, E. (2002). *Chaos in Dynamical Systems*. 2nd ed. Cambridge University Press.

- Rössler, O. E. (1976). An equation for continuous chaos. *Physics Letters A*, 57(5):397–398.

- Sauer, T., Yorke, J. A., and Casdagli, M. (1991). Embedology. *Journal of Statistical Physics*, 65(3–4):579–616.

- Strogatz, S. H. (2015). *Nonlinear Dynamics and Chaos*. 2nd ed. Westview Press.

- Takens, F. (1981). Detecting strange attractors in turbulence. In Rand, D. and Young, L.-S., editors, *Dynamical Systems and Turbulence*, Lecture Notes in Mathematics 898, pages 366–381. Springer.

- Tucker, W. (2002). A rigorous ODE solver and Smale's 14th problem. *Foundations of Computational Mathematics*, 2(1):53–117.

- Young, L.-S. (1982). Dimension, entropy, and Lyapunov exponents. *Ergodic Theory and Dynamical Systems*, 2:109–124.

---

## Recommended Reading

For a first pass through the ideas of chaos, Strogatz (2015) is excellent — readable, well-motivated, and full of examples, though lighter on proofs. Devaney (1989) provides the standard rigorous introduction to chaos in one-dimensional maps, including a thorough treatment of symbolic dynamics; it is the natural companion to this chapter.

For a deeper treatment, Katok and Hasselblatt (1995) is the definitive graduate reference on dynamical systems and ergodic theory; it is demanding but comprehensive. Ott (2002) strikes a balance between rigor and physical intuition, with excellent coverage of fractal dimensions and Lyapunov exponents.

On the Lorenz attractor specifically, the short survey by Viana (2000), "What's new on Lorenz strange attractors?" (*The Mathematical Intelligencer*, 22(3):6–19), is an accessible overview of the mathematics surrounding Tucker's theorem. Tucker's original paper (2002) is surprisingly readable for a computer-assisted proof.

For Takens' embedding theorem and its applications, the original paper (Takens, 1981) is concise and worth reading. The extension by Sauer, Yorke, and Casdagli (1991) is essential for understanding the practical aspects. Kantz and Schreiber (2003), *Nonlinear Time Series Analysis*, gives an excellent treatment of the practical aspects of attractor reconstruction from data.

For the connections between these ideas and reservoir computing — the subject of Part III — the reader may wish to look ahead to Chapter 16, or consult Lukoševičius and Jaeger (2009), "Reservoir computing approaches to recurrent neural network training" (*Computer Science Review*, 3(3):127–149).
