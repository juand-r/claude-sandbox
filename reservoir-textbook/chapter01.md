# Chapter 1: Introduction to Dynamical Systems

## 1.1 What Is a Dynamical System?

A dynamical system is, at its core, a mathematical framework for describing how things change over time. The "things" in question could be populations of organisms, the positions and velocities of planets, the concentrations of chemicals in a reaction, or the state of the atmosphere. What unifies all of these is the idea that the present state of the system determines its future states according to some fixed rule.

Before giving the formal definition, let us fix some intuition. Imagine tracking a point moving through some space. At each moment, the point occupies a definite position. The rule governing its motion tells us, given the current position, where the point will be at any future time. The space of all possible positions is the **state space** (or **phase space**), and the rule of evolution is the **dynamics**.

**Definition 1.1** (Dynamical System). A *dynamical system* is a triple $(T, X, \Phi)$ where:

1. $T$ is a **time set**, a subset of $\mathbb{R}$ (or $\mathbb{Z}$) that is closed under addition and contains $0$;
2. $X$ is a **state space** (or **phase space**), a set equipped with some structure (typically a metric space, a topological space, or a smooth manifold);
3. $\Phi: T \times X \to X$ is an **evolution operator** satisfying:
   - $\Phi(0, x) = x$ for all $x \in X$ (the identity condition),
   - $\Phi(t + s, x) = \Phi(t, \Phi(s, x))$ for all $t, s \in T$ and $x \in X$ (the semigroup condition).

The semigroup condition encodes a fundamental property: evolving for time $s$ and then for time $t$ is the same as evolving for time $t + s$. This is sometimes called the **deterministic** property — the evolution depends only on the current state, not on the history of how the system arrived there.

When $T$ is the full real line $\mathbb{R}$ or the full integers $\mathbb{Z}$, the system is **invertible**: we can run it backward as well as forward. In this case, for each fixed $t$, the map $\Phi(t, \cdot): X \to X$ is a bijection with inverse $\Phi(-t, \cdot)$, and $\{\Phi(t, \cdot)\}_{t \in T}$ forms a **group** of transformations on $X$. When $T = [0, \infty)$ or $T = \mathbb{N}_0 = \{0, 1, 2, \ldots\}$, the system may not be invertible, and we have only a **semigroup**.

**Remark.** Some authors define a dynamical system more restrictively, requiring $X$ to be a smooth manifold and $\Phi$ to be smooth (or at least continuous). Others work in full generality with measurable spaces. The appropriate level of structure depends on the questions one wishes to ask. We will see all of these flavors in the chapters to come.


## 1.2 Discrete Time vs. Continuous Time

The time set $T$ in Definition 1.1 comes in two fundamental varieties.

**Discrete-time dynamical systems.** Here $T = \mathbb{Z}$ (invertible) or $T = \mathbb{N}_0$ (non-invertible). The evolution operator is determined entirely by the single map $f: X \to X$ defined by $f(x) = \Phi(1, x)$. Then

$$\Phi(n, x) = f^n(x) = \underbrace{f \circ f \circ \cdots \circ f}_{n \text{ times}}(x).$$

A discrete-time dynamical system is thus nothing more than a set $X$ and a map $f: X \to X$, together with the rule of iteration. The study of such systems is sometimes called the **theory of iterated maps**.

Discrete-time systems arise naturally when:
- observations or measurements are made at fixed intervals (e.g., census data taken yearly),
- the dynamics are inherently stepwise (e.g., a generation-based population model),
- one reduces a continuous-time system to a discrete one via a Poincaré section (Chapter 4).

**Continuous-time dynamical systems.** Here $T = \mathbb{R}$ or $T = [0, \infty)$. The evolution is typically specified by an ordinary differential equation (ODE). Given a vector field $F: X \to TX$ on a manifold $X$ (or more concretely, $F: \mathbb{R}^n \to \mathbb{R}^n$), the ODE

$$\frac{dx}{dt} = F(x)$$

determines the evolution by the rule: the trajectory through $x_0$ is the solution $x(t)$ satisfying $x(0) = x_0$. If solutions exist and are unique for all time, the map $\Phi(t, x_0) = x(t)$ defines a **flow** on $X$, meaning a one-parameter group (or semigroup) of transformations $\{\varphi_t\}_{t \in T}$ where $\varphi_t(x) = \Phi(t, x)$.

Continuous-time systems arise naturally when modeling physical processes governed by differential laws — Newton's second law, the Navier-Stokes equations, chemical kinetics, and so on.

**The relationship between the two.** Discrete and continuous dynamics are not separate worlds. They interact in deep ways:

- Given a flow $\{\varphi_t\}$, fixing any $\tau > 0$ and setting $f = \varphi_\tau$ yields a discrete-time system. This is called **time-$\tau$ sampling** of the flow.
- Conversely, one might ask whether a given map $f$ can be realized as the time-one map of some flow. This is the **embedding problem**, and the answer is not always yes.
- The Poincaré section technique (Chapter 4) systematically reduces the study of a continuous system to a discrete one, often making the analysis more tractable.

Both settings share much of the same conceptual vocabulary — fixed points, periodic orbits, stability, chaos — though the technical details differ. We develop discrete-time systems in Chapter 2 and continuous-time systems in Chapter 3.


## 1.3 State Space, Orbits, and Trajectories

**Definition 1.2** (Orbit). Let $(T, X, \Phi)$ be a dynamical system. The **orbit** (or **trajectory**) of a point $x \in X$ is the set

$$\mathcal{O}(x) = \{\Phi(t, x) : t \in T\}.$$

When $T = \mathbb{N}_0$ and the dynamics are given by iteration of $f: X \to X$, the **forward orbit** of $x$ is the sequence

$$\mathcal{O}^+(x) = \{x, f(x), f^2(x), f^3(x), \ldots\}.$$

If $f$ is invertible, the **backward orbit** is

$$\mathcal{O}^-(x) = \{x, f^{-1}(x), f^{-2}(x), \ldots\},$$

and the **full orbit** is $\mathcal{O}(x) = \mathcal{O}^+(x) \cup \mathcal{O}^-(x)$.

For continuous-time systems, the orbit of $x_0$ is the curve $\{x(t) : t \in T\}$ traced out in state space by the solution of the ODE passing through $x_0$. This curve is called a **phase curve** or **trajectory**.

The state space $X$ is decomposed by the dynamics into a collection of disjoint orbits. Understanding the geometry and topology of this decomposition — how orbits are arranged in phase space — is one of the central goals of dynamical systems theory.

**Definition 1.3** (Fixed Point). A point $x^* \in X$ is a **fixed point** (or **equilibrium point**) if $\Phi(t, x^*) = x^*$ for all $t \in T$. For a map $f$, this means $f(x^*) = x^*$. For a flow generated by $\dot{x} = F(x)$, this means $F(x^*) = 0$: the vector field vanishes at $x^*$.

**Definition 1.4** (Periodic Orbit). A point $x$ has a **periodic orbit** of period $p > 0$ if $\Phi(p, x) = x$ and $\Phi(t, x) \neq x$ for $0 < t < p$. For a map, $x$ is a **periodic point** of (minimal) period $n$ if $f^n(x) = x$ and $f^k(x) \neq x$ for $0 < k < n$. The orbit $\{x, f(x), \ldots, f^{n-1}(x)\}$ is called an **$n$-cycle**.

Fixed points and periodic orbits are the simplest types of long-term behavior. But as we shall see, dynamical systems can exhibit far more complicated behavior: quasiperiodic orbits, homoclinic tangles, strange attractors, and chaos.

**The phase portrait.** For low-dimensional systems (especially in $\mathbb{R}^2$), one often studies the dynamics by drawing the **phase portrait**: a picture of the state space showing representative orbits, fixed points, periodic orbits, and the arrows indicating the direction of time. Phase portraits are one of the most powerful tools for building intuition about a system's behavior. We will make extensive use of them in Chapters 2 and 3.


## 1.4 Motivating Examples

The best way to appreciate the scope and power of dynamical systems theory is through examples. We present five here, ranging from discrete population models to continuous models of celestial mechanics, ecology, and atmospheric dynamics.

### 1.4.1 The Logistic Map (Discrete Time)

One of the simplest dynamical systems that exhibits astonishingly rich behavior is the **logistic map**:

$$f_r(x) = rx(1 - x), \quad x \in [0, 1], \quad r \in [0, 4].$$

This map was popularized by the biologist Robert May [May, 1976] as a simple model for population dynamics. Here $x_n \in [0, 1]$ represents the population at generation $n$ as a fraction of the maximum carrying capacity, and $r$ is a growth rate parameter. The factor $(1-x)$ provides a density-dependent brake on growth: when the population is near capacity ($x \approx 1$), the growth rate drops to zero.

The dynamics are given by iteration:

$$x_{n+1} = rx_n(1 - x_n).$$

**Fixed points.** Setting $f_r(x) = x$, we get $rx(1-x) = x$, which gives $x = 0$ or $x = 1 - 1/r$ (the latter existing in $[0,1]$ only for $r \geq 1$). Let us denote $x^* = 1 - 1/r$.

**Stability of fixed points.** For a one-dimensional map, a fixed point $x^*$ is (locally) stable if $|f'(x^*)| < 1$ and unstable if $|f'(x^*)| > 1$. We have $f_r'(x) = r(1-2x)$.

At $x = 0$: $f_r'(0) = r$. So $x = 0$ is stable for $r < 1$ and unstable for $r > 1$.

At $x^* = 1 - 1/r$: $f_r'(x^*) = r(1 - 2(1 - 1/r)) = r(2/r - 1) = 2 - r$. So $x^*$ is stable when $|2 - r| < 1$, i.e., when $1 < r < 3$.

**What happens for $r > 3$?** As $r$ increases past $3$, the fixed point $x^*$ loses stability, and a stable 2-cycle is born. As $r$ increases further, this 2-cycle loses stability and a 4-cycle appears, then an 8-cycle, and so on in a cascade of **period-doubling bifurcations**. The parameter values at which these bifurcations occur converge geometrically to a limit $r_\infty \approx 3.56995\ldots$, with the ratio of successive intervals converging to the **Feigenbaum constant** $\delta \approx 4.6692\ldots$, a universal constant that appears in a wide class of one-dimensional maps [Feigenbaum, 1978].

For $r > r_\infty$, the dynamics become **chaotic** for many parameter values: orbits are aperiodic, sensitive to initial conditions, and yet confined to a bounded region. At $r = 4$, the logistic map is conjugate to the **tent map** and to the **doubling map** on the circle, and its dynamics can be analyzed completely using symbolic dynamics.

We will study the logistic map in much greater depth in Chapters 2, 5, and 6.

### 1.4.2 The Simple Pendulum (Continuous Time)

Consider a rigid pendulum of length $\ell$ and mass $m$ swinging under gravity $g$ in a plane, with no friction. Let $\theta$ denote the angle from the downward vertical. Newton's second law gives

$$m\ell \ddot{\theta} = -mg \sin\theta,$$

or equivalently,

$$\ddot{\theta} = -\frac{g}{\ell}\sin\theta.$$

This is a second-order ODE. To cast it as a dynamical system in the sense of Definition 1.1, we introduce the angular velocity $\omega = \dot{\theta}$ and write the system as two first-order equations:

$$\dot{\theta} = \omega, \qquad \dot{\omega} = -\frac{g}{\ell}\sin\theta.$$

The state space is the **cylinder** $X = S^1 \times \mathbb{R}$ (since $\theta$ is an angle, periodic modulo $2\pi$, and $\omega$ is unrestricted). The state at any time is the pair $(\theta, \omega)$, which determines the future evolution.

**Fixed points.** Setting $\dot{\theta} = 0$ and $\dot{\omega} = 0$, we get $\omega = 0$ and $\sin\theta = 0$, giving two equilibria:

- $(\theta, \omega) = (0, 0)$: the pendulum hanging straight down (stable equilibrium).
- $(\theta, \omega) = (\pi, 0)$: the pendulum balanced upright (unstable equilibrium).

**Energy and orbits.** The total energy

$$E(\theta, \omega) = \frac{1}{2}\omega^2 - \frac{g}{\ell}\cos\theta$$

is conserved (i.e., $\dot{E} = 0$ along solutions), so orbits lie on level curves of $E$. These level curves give the phase portrait:

- For $E < g/\ell$, the orbits are **closed curves** surrounding $(0,0)$: the pendulum oscillates back and forth (librations).
- For $E = g/\ell$, there are special orbits called **separatrices** (or **homoclinic orbits**) that connect the unstable equilibrium $(\pi, 0)$ to itself.
- For $E > g/\ell$, the orbits are curves that wind all the way around the cylinder: the pendulum spins continuously (rotations).

The pendulum is one of the oldest and most studied dynamical systems. Despite its simplicity, it already illustrates several important themes: the role of conserved quantities (energy), the coexistence of qualitatively different orbit types, and the presence of both stable and unstable equilibria.

### 1.4.3 The Two-Body Problem (Continuous Time)

The motion of two point masses interacting through Newtonian gravitation is one of the great successes of classical mechanics. After reducing to center-of-mass coordinates, the problem reduces to a single body of reduced mass $\mu$ moving in a central force field:

$$\ddot{\mathbf{r}} = -\frac{GM}{|\mathbf{r}|^3}\mathbf{r},$$

where $\mathbf{r} \in \mathbb{R}^3$ is the relative position vector, $M$ is the total mass, and $G$ is the gravitational constant.

The state space is (a subset of) $\mathbb{R}^3 \times \mathbb{R}^3$ with coordinates $(\mathbf{r}, \dot{\mathbf{r}})$. Conservation of angular momentum $\mathbf{L} = \mu\mathbf{r} \times \dot{\mathbf{r}}$ restricts the motion to a plane when $\mathbf{L} \neq 0$, reducing the problem to four dimensions. Conservation of energy further constrains orbits to three-dimensional surfaces in phase space. After exploiting all symmetries, the problem is completely integrable, and the solutions are the **conic sections**: ellipses (bound orbits), parabolas, and hyperbolas (unbound orbits).

**Kepler's laws** — (1) orbits are ellipses with the sun at one focus, (2) equal areas are swept in equal times, (3) the square of the period is proportional to the cube of the semi-major axis — are consequences of this analysis.

The two-body problem illustrates the power of conserved quantities (energy, angular momentum) in constraining and solving a dynamical system. It is also a cautionary tale: the three-body problem, obtained by adding just one more mass, is **not** integrable in general and exhibits chaotic dynamics. This was Poincaré's great discovery, which launched much of modern dynamical systems theory (Section 1.5).

### 1.4.4 The Lotka-Volterra Predator-Prey Model (Continuous Time)

In 1925-1926, Alfred Lotka and Vito Volterra independently proposed a simple model for the interaction of a predator species and a prey species:

$$\dot{x} = \alpha x - \beta xy, \qquad \dot{y} = \delta xy - \gamma y,$$

where $x(t) \geq 0$ is the prey population, $y(t) \geq 0$ is the predator population, and $\alpha, \beta, \gamma, \delta > 0$ are parameters representing birth rates, predation rates, and death rates.

The state space is the first quadrant $X = \{(x, y) \in \mathbb{R}^2 : x \geq 0, \, y \geq 0\}$.

**Fixed points.** Setting both equations to zero:
- $(0, 0)$: both species extinct.
- $(x^*, y^*) = (\gamma/\delta, \, \alpha/\beta)$: a coexistence equilibrium.

**Analysis at the coexistence equilibrium.** The Jacobian of the vector field at $(x^*, y^*)$ is

$$J = \begin{pmatrix} 0 & -\beta x^* \\ \delta y^* & 0 \end{pmatrix} = \begin{pmatrix} 0 & -\beta\gamma/\delta \\ \alpha\delta/\beta & 0 \end{pmatrix}.$$

The eigenvalues are $\lambda = \pm i\sqrt{\alpha\gamma}$, which are purely imaginary. The equilibrium is a **center** (in the linear approximation), and a conserved quantity argument shows it is also a center for the nonlinear system: the function

$$H(x, y) = \delta x - \gamma \ln x + \beta y - \alpha \ln y$$

is constant along solutions (verify: $\dot{H} = 0$). Thus, orbits in the interior of the first quadrant are **closed curves** encircling $(x^*, y^*)$, representing periodic oscillations of the predator and prey populations.

This model, while idealized, captures the essential qualitative feature observed in many predator-prey systems: cyclic oscillations in population sizes, with the predator cycle lagging behind the prey cycle.

### 1.4.5 The Lorenz System (Continuous Time)

In 1963, the meteorologist Edward Lorenz published a paper that would reshape our understanding of determinism, predictability, and the nature of chaos [Lorenz, 1963]. Lorenz derived a simplified model for atmospheric convection — a system of three coupled ODEs:

$$\dot{x} = \sigma(y - x), \qquad \dot{y} = x(\rho - z) - y, \qquad \dot{z} = xy - \beta z,$$

where $\sigma$, $\rho$, $\beta > 0$ are parameters. The variables $x$, $y$, $z$ are related to the intensity of convective motion and the temperature distribution. Lorenz used the values $\sigma = 10$, $\rho = 28$, $\beta = 8/3$, which correspond to a physically relevant regime.

The state space is $X = \mathbb{R}^3$.

**Fixed points.** Setting $\dot{x} = \dot{y} = \dot{z} = 0$:

From $\dot{x} = 0$: $y = x$.

From $\dot{y} = 0$: $x(\rho - z) - x = 0$, so $x(\rho - 1 - z) = 0$.

From $\dot{z} = 0$: $x^2 = \beta z$ (using $y = x$).

This gives three equilibria:
- The **origin** $(0, 0, 0)$, which represents no convection.
- The points $C^{\pm} = (\pm\sqrt{\beta(\rho - 1)}, \, \pm\sqrt{\beta(\rho - 1)}, \, \rho - 1)$, which exist for $\rho > 1$ and represent steady convective rolls.

For the classical parameter values, all three equilibria are **unstable**. Where, then, do the orbits go? They are attracted to a complicated, fractal-like set now called the **Lorenz attractor** — a **strange attractor** with the following remarkable properties:

1. **Bounded:** All orbits eventually enter and remain within a bounded region of $\mathbb{R}^3$.
2. **Sensitive dependence on initial conditions:** Two orbits starting from nearby points diverge exponentially fast (on average), even though both remain on the attractor.
3. **Aperiodic:** Typical orbits on the attractor never exactly repeat; they are not periodic.
4. **Geometric complexity:** The attractor has a fractal structure with Hausdorff dimension approximately $2.06$, meaning it is "almost" a surface but has fine-scale structure at all magnifications.

The Lorenz system was the first concrete, physically motivated example of deterministic chaos. Lorenz's discovery showed that even simple, deterministic systems can be effectively unpredictable in the long run — not because of any randomness in the equations, but because of the exponential amplification of small uncertainties. This has profound implications for weather prediction and for the foundations of classical mechanics more broadly. We will return to the Lorenz system in Chapter 6.


## 1.5 Historical Context

The theory of dynamical systems has deep roots in classical mechanics, but its development as a distinct mathematical discipline is largely a story of the twentieth century.

**Henri Poincaré (1854--1912)** is widely regarded as the founder of the qualitative theory of dynamical systems. In his work on the three-body problem in celestial mechanics [Poincaré, 1890], Poincaré introduced a battery of concepts and techniques that remain central to the field: the use of topology and geometry (rather than explicit formulas) to understand the structure of solutions; the Poincaré section and first-return map; the notion of homoclinic orbits and their role in generating complicated dynamics; and the concept of recurrence, which he proved in the context of volume-preserving flows (the Poincaré recurrence theorem, Chapter 4). Poincaré recognized that many dynamical systems cannot be solved in closed form, and that the right questions are qualitative: What is the long-term behavior of typical orbits? What structures (fixed points, periodic orbits, invariant surfaces) organize the phase portrait?

**George David Birkhoff (1884--1944)** extended Poincaré's work in several directions. His pointwise ergodic theorem [Birkhoff, 1931] is one of the foundational results of ergodic theory, establishing that time averages of observables along orbits converge for almost every initial condition. This theorem provides the rigorous justification for replacing time averages with space averages — a procedure used routinely in statistical mechanics and throughout the physical sciences. We will prove and study this theorem in Chapter 9.

**The Soviet school.** In the mid-twentieth century, a number of mathematicians in the Soviet Union made fundamental contributions to both dynamical systems and ergodic theory. Andrei Kolmogorov developed the measure-theoretic foundations of probability and introduced the concept of metric entropy (Kolmogorov-Sinai entropy) for dynamical systems. Kolmogorov also proved the first version of the KAM theorem (Chapter 3 of advanced treatments), showing that many quasi-periodic motions in Hamiltonian systems persist under small perturbations. Yakov Sinai carried forward Kolmogorov's work, developing the theory of entropy, establishing deep connections between hyperbolic dynamics and statistical mechanics, and introducing the concept of Sinai-Ruelle-Bowen (SRB) measures.

**Stephen Smale (b. 1930)** brought the tools of differential topology to dynamical systems in the 1960s. His introduction of the horseshoe map [Smale, 1967] provided a clean geometric mechanism for chaos and showed that chaotic dynamics are structurally stable — they persist under small perturbations of the system. Smale's program of classifying dynamical systems up to topological equivalence (the program of **hyperbolic dynamics**) shaped much of the field for decades.

**Edward Lorenz (1917--2008)** was not a mathematician but a meteorologist. His 1963 paper, arising from a numerical experiment on a simplified weather model, provided the first concrete example of sensitive dependence on initial conditions in a physically motivated system. Lorenz's work brought deterministic chaos to the attention of scientists across disciplines and fundamentally changed our understanding of predictability. His description of what is now called the **butterfly effect** — the idea that small perturbations can lead to vastly different outcomes — has become one of the most widely known ideas in all of science.

These are only a few of the many contributors. The field has been enriched by the work of Lyapunov (stability theory), Hadamard (geodesic flows on negatively curved surfaces), Kolmogorov, Arnold, and Moser (the KAM theorem), Ruelle and Takens (turbulence and strange attractors), Milnor (one-dimensional dynamics), and many others. Throughout this textbook, we will encounter their ideas repeatedly.


## 1.6 The Central Questions

Dynamical systems theory organizes itself around a few recurring questions. These questions can be stated simply, but answering them — even for specific, concrete systems — can require the full machinery of analysis, algebra, topology, and measure theory.

**Question 1: What happens in the long run?**

Given an initial state $x_0 \in X$, what can we say about $\Phi(t, x_0)$ as $t \to \infty$? Does the orbit converge to a fixed point? Does it settle onto a periodic orbit or a more complicated attractor? Does it escape to infinity? The **$\omega$-limit set** of $x_0$,

$$\omega(x_0) = \bigcap_{N \geq 0} \overline{\{\Phi(t, x_0) : t \geq N\}},$$

captures the set of accumulation points of the orbit as $t \to \infty$. Understanding $\omega$-limit sets — their structure, their dependence on $x_0$, and how they are organized in phase space — is a central theme.

For the logistic map with $r = 2.5$, every orbit in $(0,1)$ converges to the fixed point $x^* = 0.6$: the $\omega$-limit set is a single point. For the Lotka-Volterra system, the $\omega$-limit set of a typical orbit is a closed curve. For the Lorenz system, the $\omega$-limit set of a typical orbit is a strange attractor.

**Question 2: Are there stable states, and which orbits approach them?**

A fixed point or periodic orbit is **stable** (informally) if nearby orbits remain nearby for all future time, and **asymptotically stable** if nearby orbits actually converge to it. More precisely:

**Definition 1.5** (Lyapunov Stability). A fixed point $x^*$ is **Lyapunov stable** if for every $\epsilon > 0$ there exists $\delta > 0$ such that $d(x_0, x^*) < \delta$ implies $d(\Phi(t, x_0), x^*) < \epsilon$ for all $t \geq 0$.

**Definition 1.6** (Asymptotic Stability). A fixed point $x^*$ is **asymptotically stable** if it is Lyapunov stable and there exists $\delta > 0$ such that $d(x_0, x^*) < \delta$ implies $\Phi(t, x_0) \to x^*$ as $t \to \infty$.

The **basin of attraction** of an asymptotically stable fixed point $x^*$ is the set of all initial conditions whose orbits converge to $x^*$:

$$\mathcal{B}(x^*) = \{x_0 \in X : \Phi(t, x_0) \to x^* \text{ as } t \to \infty\}.$$

Understanding the basins of attraction — their geometry, their boundaries, and how they change as parameters vary — is crucial in applications, where one often wants to know which initial conditions lead to desirable long-term outcomes.

**Question 3: How sensitive is the system to initial conditions?**

This question, sharpened by Lorenz's work, is now understood to be one of the most fundamental. Two initial conditions that are very close in state space may produce orbits that diverge exponentially fast. This is quantified by **Lyapunov exponents**:

**Definition 1.7** (Lyapunov Exponent, Informal). For a differentiable map $f: \mathbb{R}^n \to \mathbb{R}^n$ and an initial condition $x_0$, the **maximal Lyapunov exponent** is

$$\lambda(x_0) = \lim_{n \to \infty} \frac{1}{n} \ln \|Df^n(x_0)\|,$$

when this limit exists. Here $Df^n(x_0)$ is the derivative (Jacobian) of the $n$-th iterate $f^n$ evaluated at $x_0$.

A positive maximal Lyapunov exponent indicates exponential divergence of nearby orbits — the hallmark of chaos. A negative exponent indicates convergence. The precise definition and properties of Lyapunov exponents will be developed in Chapter 6.

For the logistic map at $r = 4$, a computation (or appeal to the theory of Chapter 6) shows that the Lyapunov exponent is $\lambda = \ln 2 > 0$: the system is chaotic. For $r = 2.5$, orbits converge to a stable fixed point and $\lambda < 0$.

**Question 4: How does the behavior change as parameters vary?**

Most dynamical systems of interest depend on parameters (the growth rate $r$ in the logistic map, the Rayleigh number $\rho$ in the Lorenz system, etc.). As these parameters change, the qualitative behavior of the system can change dramatically: fixed points can appear, disappear, or exchange stability; periodic orbits can emerge; and chaos can set in. These qualitative changes are called **bifurcations**, and their systematic study is the subject of Chapter 5.

**Question 5: What can we say about "typical" or "average" behavior?**

Individual orbits of a chaotic system may be unpredictable, but the statistical behavior of an ensemble of orbits can be highly regular. Ergodic theory provides the framework for studying this statistical behavior. The key idea is to equip the state space with a measure (often an invariant measure preserved by the dynamics) and ask about the statistical distribution of orbits with respect to this measure. The ergodic theorems (Chapters 9 and 10) assert that, under appropriate conditions, time averages along individual orbits equal space averages with respect to the invariant measure — giving rigorous meaning to the informal physicist's idea of "typical" or "average" behavior.


## 1.7 Where This Textbook Is Headed

This chapter has set up the basic language and given a glimpse of the diversity of phenomena that dynamical systems can exhibit. The rest of the textbook develops this material in three parts.

**Part I: Dynamical Systems (Chapters 2--6)** develops the theory systematically. We begin with discrete-time systems (Chapter 2): iterated maps, fixed points, periodic orbits, stability, and the logistic map as a running example. Chapter 3 treats continuous-time systems: flows, vector fields, phase portraits, and the linearization of nonlinear systems near equilibria. Chapter 4 introduces Poincaré sections, which connect the discrete and continuous theories, and proves the Poincaré recurrence theorem. Chapter 5 studies bifurcations: the mechanisms by which qualitative behavior changes as parameters vary. Chapter 6 tackles chaos head-on: sensitive dependence, Lyapunov exponents, strange attractors, and rigorous definitions of what "chaos" means.

**Part II: Ergodic Theory (Chapters 7--12)** introduces the measure-theoretic framework for studying the statistical behavior of dynamical systems. After a concise review of measure theory (Chapter 7), we define measure-preserving transformations and invariant measures (Chapter 8). The ergodic theorems of von Neumann and Birkhoff (Chapter 9) are the cornerstones of the theory. Chapters 10 and 11 develop mixing, spectral theory, and entropy, culminating in Chapter 12 with a synthesis connecting ergodic theory back to the dynamical systems of Part I, particularly through SRB measures and the statistical properties of chaotic systems.

**Part III: Reservoir Computing (Chapters 13--17)** applies the ideas of Parts I and II to a modern topic at the interface of dynamical systems theory and machine learning. Reservoir computing exploits the dynamics of a high-dimensional nonlinear system (the "reservoir") to perform computation, with only a simple readout layer trained by linear regression. The echo state property, which guarantees that the reservoir forgets its initial condition and responds only to its input, is intimately connected to the stability and ergodic-theoretic properties developed in the earlier parts. We will see how Lyapunov exponents, invariant measures, and entropy all play roles in understanding when and why reservoir computers work.

The unifying thread is that dynamical systems are not just objects of mathematical study — they are computational substrates. The same properties that make a system rich enough to exhibit complex, chaotic behavior also make it rich enough to process and represent information. Ergodic theory provides the tools for understanding this connection at a rigorous level.


## 1.8 Exercises

**Exercise 1.1.** Consider the map $f: \mathbb{R} \to \mathbb{R}$ defined by $f(x) = x^2$.

(a) Find all fixed points of $f$.

(b) Determine the orbit $\mathcal{O}^+(x_0)$ for $x_0 = 1/2$, $x_0 = 1$, $x_0 = 2$, and $x_0 = -1$. (You may describe the qualitative behavior rather than listing every element.)

(c) For which initial conditions $x_0 \in \mathbb{R}$ does the orbit converge to $0$? To $\infty$? Describe the basins of attraction.

---

**Exercise 1.2.** Let $R_\alpha: S^1 \to S^1$ be the rotation of the circle by angle $\alpha$, defined by $R_\alpha(\theta) = \theta + \alpha \pmod{2\pi}$.

(a) Show that $R_\alpha$ satisfies the semigroup property: $R_\alpha^n(\theta) = \theta + n\alpha \pmod{2\pi}$.

(b) Show that every point is a periodic point if and only if $\alpha/(2\pi)$ is rational.

(c) Show that if $\alpha/(2\pi)$ is irrational, then the orbit of every point is dense in $S^1$. (Hint: show that the orbit is infinite, and use the pigeonhole principle to find orbit points arbitrarily close together, then use the group structure of the circle.)

---

**Exercise 1.3.** For the logistic map $f_r(x) = rx(1-x)$:

(a) Verify that $f_r$ maps the interval $[0,1]$ into itself for $r \in [0, 4]$.

(b) Find the 2-cycles of $f_r$ by solving $f_r(f_r(x)) = x$ and removing the fixed points. Show that 2-cycles exist for $r > 3$.

(c) Show that the 2-cycle found in (b) is stable for $3 < r < 1 + \sqrt{6}$.

---

**Exercise 1.4.** For the pendulum system $\dot{\theta} = \omega$, $\dot{\omega} = -(g/\ell)\sin\theta$:

(a) Verify that $E(\theta, \omega) = \frac{1}{2}\omega^2 - (g/\ell)\cos\theta$ is a conserved quantity by showing $\dot{E} = 0$ along solutions.

(b) Linearize the system at the equilibrium $(\theta, \omega) = (0, 0)$ and classify the equilibrium of the linearized system. (What are the eigenvalues of the Jacobian?)

(c) Repeat for the equilibrium $(\pi, 0)$.

---

**Exercise 1.5.** Consider the Lotka-Volterra system

$$\dot{x} = \alpha x - \beta xy, \qquad \dot{y} = \delta xy - \gamma y$$

with $\alpha, \beta, \gamma, \delta > 0$.

(a) Verify that $H(x, y) = \delta x - \gamma \ln x + \beta y - \alpha \ln y$ satisfies $\dot{H} = 0$ along solutions, confirming it is a conserved quantity.

(b) Show that the axes $x = 0$ and $y = 0$ are invariant: if an orbit starts on an axis, it remains on that axis. Describe the dynamics on each axis.

(c) Explain why the existence of a conserved quantity implies that orbits in the interior of the first quadrant cannot converge to the equilibrium $(\gamma/\delta, \alpha/\beta)$.

---

**Exercise 1.6.** Consider the Lorenz system with parameters $\sigma = 10$, $\rho = 28$, $\beta = 8/3$.

(a) Find all three equilibrium points.

(b) Compute the Jacobian matrix of the vector field at the origin and find its eigenvalues. Is the origin stable or unstable?

(c) Show that the function $V(x, y, z) = x^2 + y^2 + (z - \rho - \sigma)^2$ satisfies $\dot{V} < 0$ outside a sufficiently large ellipsoid in $\mathbb{R}^3$. (This shows that all orbits eventually enter a bounded region. You do not need to find the optimal ellipsoid.)

---

**Exercise 1.7** (Contraction Mapping and Dynamics). Let $(X, d)$ be a complete metric space and $f: X \to X$ a **contraction**: there exists $c \in [0, 1)$ such that $d(f(x), f(y)) \leq c \cdot d(x, y)$ for all $x, y \in X$.

(a) Show that $f$ has a unique fixed point $x^*$.

(b) Show that for every $x_0 \in X$, the orbit $\{f^n(x_0)\}$ converges to $x^*$.

(c) Show that $d(f^n(x_0), x^*) \leq \frac{c^n}{1 - c} \, d(x_0, f(x_0))$, giving an explicit rate of convergence.

(d) Relate this to the notion of the basin of attraction: what is $\mathcal{B}(x^*)$ for a contraction?


## References

- G. D. Birkhoff, "Proof of the ergodic theorem," *Proceedings of the National Academy of Sciences*, 17(12):656--660, 1931.

- R. L. Devaney, *An Introduction to Chaotic Dynamical Systems*, 3rd edition, CRC Press, 2021.

- M. J. Feigenbaum, "Quantitative universality for a class of nonlinear transformations," *Journal of Statistical Physics*, 19(1):25--52, 1978.

- M. W. Hirsch, S. Smale, and R. L. Devaney, *Differential Equations, Dynamical Systems, and an Introduction to Chaos*, 3rd edition, Academic Press, 2013.

- A. Katok and B. Hasselblatt, *Introduction to the Modern Theory of Dynamical Systems*, Cambridge University Press, 1995.

- E. N. Lorenz, "Deterministic nonperiodic flow," *Journal of the Atmospheric Sciences*, 20(2):130--141, 1963.

- R. M. May, "Simple mathematical models with very complicated dynamics," *Nature*, 261:459--467, 1976.

- H. Poincaré, "Sur le problème des trois corps et les équations de la dynamique," *Acta Mathematica*, 13:1--270, 1890.

- S. Smale, "Differentiable dynamical systems," *Bulletin of the American Mathematical Society*, 73(6):747--817, 1967.

- S. H. Strogatz, *Nonlinear Dynamics and Chaos*, 2nd edition, Westview Press, 2015.


## Recommended Reading

For a first course in dynamical systems, **Strogatz** [2015] is highly recommended: it is clearly written, rich with examples and applications, and assumes minimal prerequisites. **Hirsch, Smale, and Devaney** [2013] provides a more mathematically rigorous treatment of ODEs and dynamical systems, suitable for students with a stronger analysis background. **Devaney** [2021] focuses on discrete dynamical systems and gives a particularly clean treatment of chaos, symbolic dynamics, and the Sarkovskii theorem.

For the more advanced material that we will develop in later chapters, **Katok and Hasselblatt** [1995] is the standard reference for the modern theory of dynamical systems, including ergodic theory, hyperbolic dynamics, and entropy. It is encyclopedic and demanding, but indispensable.

Lorenz's original paper [Lorenz, 1963] is short, readable, and still worth engaging with directly. Smale's survey [Smale, 1967] gives a sweeping overview of the state of dynamical systems theory in the 1960s and remains a landmark of mathematical exposition.
