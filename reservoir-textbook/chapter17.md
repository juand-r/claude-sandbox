# Chapter 17: Applications, Frontiers, and Open Problems

In the preceding chapters, we built a theoretical edifice connecting dynamical systems, ergodic theory, and reservoir computing. We now turn to applications, surveying how these ideas play out in practice, what frontiers are being explored, and what remains unknown. This chapter is necessarily less rigorous than its predecessors — it is a guided tour of a rapidly evolving landscape rather than a sequence of theorems — but we ground each topic in the mathematics developed earlier.

---

## 17.1 Time Series Prediction

The most natural application of reservoir computing is predicting the future of a time series from its past. The mathematical setup is as follows.

### 17.1.1 The Prediction Problem

Let $\mathbf{s}(t) \in \mathbb{R}^d$ be the state of a deterministic dynamical system $\dot{\mathbf{s}} = F(\mathbf{s})$, and let $x(t) = h(\mathbf{s}(t))$ be a scalar observable. Given a sequence of observations $x(1), x(2), \ldots, x(T)$, we wish to predict $x(T + \tau)$ for some lead time $\tau > 0$.

By Takens' embedding theorem (Chapter 6), the delay vector

$$\mathbf{d}(t) = (x(t), x(t - \Delta), x(t - 2\Delta), \ldots, x(t - (m-1)\Delta))$$

generically provides a diffeomorphic embedding of the attractor when $m \geq 2d + 1$. In particular, there exists a smooth function $G: \mathbb{R}^m \to \mathbb{R}$ such that

$$x(t + \tau) = G(\mathbf{d}(t)).$$

The reservoir, driven by the scalar input $x(t)$, creates a high-dimensional nonlinear embedding of the input history — a generalized, learned version of the delay embedding. The readout layer then approximates $G$.

### 17.1.2 Benchmark Systems

**The Mackey-Glass equation.** This delay-differential equation,

$$\dot{x}(t) = \beta \frac{x(t - \tau_d)}{1 + x(t - \tau_d)^n} - \gamma x(t),$$

with standard parameters $\beta = 0.2$, $\gamma = 0.1$, $n = 10$, $\tau_d = 17$, produces a chaotic time series with a strange attractor of dimension approximately 2.1. It has been a standard benchmark since Farmer and Sidorowich (1987). Reservoir computers achieve normalized mean square errors (NMSE) on the order of $10^{-8}$ for one-step prediction on this system (Jaeger & Haas, 2004).

**NARMA systems.** The $k$-th order nonlinear autoregressive moving average (NARMA) system is defined by

$$y(t+1) = \alpha y(t) + \beta y(t) \sum_{i=0}^{k-1} y(t-i) + \gamma u(t-k+1) u(t) + \delta,$$

where $u(t)$ is a random input. NARMA-10 and NARMA-30 are standard benchmarks that test a reservoir's memory capacity and nonlinear processing simultaneously.

**The Lorenz system.** Short-term prediction of the Lorenz attractor is straightforward for reservoir computers. The more interesting challenge is long-term: can the reservoir reproduce the *climate* (the invariant measure) of the Lorenz system? We address this in Section 17.2.

### 17.1.3 Performance Metrics

The normalized mean square error is defined as

$$\text{NMSE} = \frac{\sum_{t} (y(t) - \hat{y}(t))^2}{\sum_{t} (y(t) - \bar{y})^2},$$

where $\hat{y}(t)$ is the prediction and $\bar{y}$ is the mean of the target. An NMSE of 0 is perfect prediction; an NMSE of 1 is no better than predicting the mean.

For chaotic systems, a more informative metric is the **valid prediction time** (or prediction horizon): the time until the prediction error exceeds a threshold, typically one attractor diameter. For the Lorenz system with standard parameters, reservoir computers achieve prediction horizons of several Lyapunov times, where one Lyapunov time is $1/\lambda_{\max} \approx 1/0.9 \approx 1.1$ time units.

---

## 17.2 Chaotic System Modeling and Climate Replication

### 17.2.1 Beyond Short-Term Prediction

For chaotic systems, pointwise prediction necessarily fails after a few Lyapunov times — this is the essence of sensitive dependence on initial conditions. But a more ambitious and subtle goal is to replicate the **climate** of the system: its long-term statistical properties.

In the language of ergodic theory, this means reproducing the system's invariant measure (or SRB measure). If the autonomous reservoir (running without teacher forcing, feeding its own predictions back as input) generates a trajectory whose time averages match the space averages of the true system, then by the ergodic theorem, the reservoir has effectively learned the invariant measure.

### 17.2.2 The Pathak et al. Results

Pathak, Hunt, Girvan, Lu, and Ott (2017, 2018) demonstrated that reservoir computers can:

1. **Predict** the short-term evolution of chaotic systems (Lorenz, Rössler, Kuramoto-Sivashinsky).
2. **Replicate the climate**: the autonomous reservoir, running freely, produces trajectories with the correct Lyapunov exponents, attractor dimension, and invariant measure — even though pointwise prediction has long since diverged.

This is a striking result. The reservoir does not merely memorize the training data; it learns the underlying dynamics well enough to reproduce the correct statistical properties. In ergodic-theoretic terms, the reservoir's autonomous dynamics support an invariant measure that closely approximates the SRB measure of the true system.

### 17.2.3 Hybrid Reservoir Computing

When partial knowledge of the governing equations is available, it can be incorporated. Lu, Pathak, Hunt, Girvan, Brockett, and Ott (2017) proposed a hybrid approach:

$$\mathbf{x}(t+1) = f(W\mathbf{x}(t) + W_{in}\mathbf{u}(t+1)),$$
$$\hat{\mathbf{y}}(t) = W_{out}\begin{pmatrix} \mathbf{x}(t) \\ \mathbf{k}(t) \end{pmatrix},$$

where $\mathbf{k}(t)$ is the output of a knowledge-based model (e.g., a coarse or imperfect simulation). The reservoir learns to correct the model's errors. This consistently outperforms either the model or the reservoir alone.

---

## 17.3 Signal Classification

Reservoir computing is naturally suited to temporal pattern recognition. The reservoir transforms a time-varying input signal into a trajectory in a high-dimensional state space. Different input classes produce different trajectories, and the readout layer acts as a classifier on the terminal state (or a time-averaged state).

**Spoken digit recognition** was an early benchmark (Verstraeten et al., 2005). The input is a cochlear-filtered speech signal; the reservoir state at the end of the utterance encodes enough information for a linear classifier to distinguish digits. Performance is competitive with hidden Markov models and recurrent neural networks trained with backpropagation through time, at a fraction of the training cost.

The mathematical picture: the reservoir implements a nonlinear embedding of the space of input signals into $\mathbb{R}^N$. The separation property (Chapter 15) ensures that distinct signal classes are mapped to distinct regions of state space. The linear readout then separates these regions with a hyperplane.

---

## 17.4 Physical Reservoir Computing

One of the most distinctive features of reservoir computing is that the reservoir need not be a simulated neural network. Any sufficiently rich dynamical system can serve as a reservoir. This opens the door to **physical reservoir computing**: using the native dynamics of physical systems for computation.

### 17.4.1 Photonic Reservoirs

Appeltant et al. (2011) demonstrated reservoir computing using a single semiconductor laser with delayed optical feedback. The key idea is **time-multiplexing**: the delay line is divided into $N$ virtual nodes, each corresponding to a time slot within one delay period. The state of these virtual nodes collectively acts as the reservoir state.

The dynamics are governed by a delay-differential equation of the form

$$\epsilon \dot{x}(t) = -x(t) + f\big(\beta x(t - \tau_D) + \gamma J(t)\big),$$

where $\tau_D$ is the delay time, $J(t)$ is the input, and $f$ is a nonlinear function determined by the laser physics. The delay creates effective high-dimensional dynamics from a single physical node.

Photonic reservoirs can operate at GHz rates, orders of magnitude faster than electronic implementations. Larger et al. (2012) and Brunner et al. (2013) further developed this approach.

### 17.4.2 Mechanical Reservoirs

Nakajima and colleagues have demonstrated that soft bodies — silicone arms, mass-spring networks, vibrating plates — can serve as reservoirs. The mechanical response of these systems to input forces creates a rich, high-dimensional state that can be read out for computation.

This has implications for robotics: the body of a robot is itself a dynamical system, and its physics can be harnessed for computation rather than being an obstacle to overcome.

### 17.4.3 Spintronic Reservoirs

Magnetic systems exhibit complex nonlinear dynamics. Torrejon et al. (2017) demonstrated reservoir computing using a single magnetic tunnel junction, exploiting the nonlinear magnetization dynamics governed by the Landau-Lifshitz-Gilbert equation.

### 17.4.4 Quantum Reservoir Computing

Quantum systems offer exponentially large Hilbert spaces, suggesting enormous computational capacity. Fujii and Nakajima (2017) proposed quantum reservoir computing, where a quantum system driven by classical inputs serves as the reservoir, and measurements of observables provide the readout.

The measurement problem adds an interesting twist: each measurement partially collapses the quantum state, so the readout strategy becomes part of the reservoir design. The mathematical framework extends naturally — the echo state property becomes a condition on the quantum channel's contractivity.

### 17.4.5 The Unifying Principle

In every case, the mathematical requirements are the same:

1. **Echo state property**: the physical dynamics must be contracting, so that the current state depends on the input history, not the initial condition.
2. **Sufficient dimensionality**: the state space must be rich enough (high-dimensional, nonlinear) to separate different input histories.
3. **Readability**: one must be able to observe enough of the state to train a readout.

The theory from Chapters 14–16 applies uniformly: Lyapunov exponents characterize stability, ergodic properties determine generalization, and information processing capacity quantifies computational power.

---

## 17.5 Next-Generation Reservoir Computing

### 17.5.1 The NGRC Framework

Gauthier, Bollt, Griffith, and Barbosa (2021) introduced **next-generation reservoir computing (NGRC)**, which replaces the random recurrent network with a structured, deterministic feature map based on time-delay embeddings.

The state vector is constructed directly from delayed observations:

$$\mathbf{O}(t) = \big(x(t),\; x(t - \Delta),\; x(t - 2\Delta),\; \ldots,\; x(t - (k-1)\Delta)\big).$$

Nonlinear features are then formed as products:

$$\mathbf{p}(t) = \text{vec}\big(\mathbf{O}(t) \otimes \mathbf{O}(t)\big),$$

where $\otimes$ denotes the outer product (or higher-order tensor products for higher-degree nonlinearities). The combined feature vector $(\mathbf{O}(t), \mathbf{p}(t))$ serves as the "reservoir state," and a linear readout is trained by ridge regression as before.

### 17.5.2 Connection to Takens' Theorem

The connection to Takens' embedding theorem is now explicit and direct. The linear part $\mathbf{O}(t)$ is precisely a delay embedding. The nonlinear part $\mathbf{p}(t)$ enriches this embedding with polynomial features, enabling the readout to approximate nonlinear functions of the attractor coordinates.

In the language of Chapter 15, NGRC constructs the separation and approximation properties by design rather than relying on random connectivity to provide them. The theoretical justification is cleaner, though the universality results are more restrictive (finite polynomial degree).

### 17.5.3 Advantages and Limitations

Advantages:
- No random matrices, hence no sensitivity to random seeds.
- Fewer hyperparameters (delay $\Delta$, number of delays $k$, polynomial degree).
- Often superior performance on standard benchmarks.
- Faster training (the feature matrix is structured and typically smaller).

Limitations:
- The polynomial feature space grows combinatorially with the degree and number of delays.
- For multivariate inputs, the approach becomes expensive.
- The theoretical understanding of when NGRC outperforms classical ESN is incomplete.

---

## 17.6 Deep Reservoirs

Gallicchio and Micheli (2017) proposed **deep echo state networks**: stacking multiple reservoir layers, where each layer processes the output of the previous one:

$$\mathbf{x}^{(\ell)}(t+1) = f\big(W^{(\ell)}\mathbf{x}^{(\ell)}(t) + W_{in}^{(\ell)}\mathbf{x}^{(\ell-1)}(t+1)\big), \quad \ell = 1, \ldots, L,$$

with $\mathbf{x}^{(0)}(t) = \mathbf{u}(t)$ being the input. The readout is trained on the concatenation of states from all layers.

The analogy with deep neural networks suggests that deeper reservoirs create increasingly abstract representations. Empirically, deep reservoirs sometimes outperform single-layer reservoirs of the same total size, particularly on tasks requiring hierarchical temporal features.

**Open questions**: What is the optimal depth? How do the echo state property and Lyapunov exponents behave as a function of depth? Is there a "deep" version of the universal approximation results from Chapter 15? These remain largely unanswered.

---

## 17.7 Spatiotemporal Systems

Many real-world systems — fluid flows, cardiac dynamics, climate — are spatially extended, governed by partial differential equations. Extending reservoir computing to such systems requires handling high-dimensional, spatially structured data.

### 17.7.1 Parallel Reservoir Architectures

Pathak et al. (2018) proposed a divide-and-conquer approach for the Kuramoto-Sivashinsky (KS) equation,

$$\partial_t u + u\partial_x u + \partial_x^2 u + \partial_x^4 u = 0,$$

which exhibits spatiotemporal chaos. The spatial domain is divided into overlapping regions, each assigned its own reservoir. Each reservoir receives input from its region and its neighbors. The readout produces predictions for the local region.

This architecture scales linearly with domain size (rather than quadratically, as a single large reservoir would). Pathak et al. demonstrated both short-term prediction and long-term climate replication of the KS system with this approach — a striking application of the ideas from Chapter 16 to a PDE setting.

### 17.7.2 Mathematical Perspective

From the dynamical systems viewpoint, the KS equation defines an infinite-dimensional dynamical system on a function space. Its attractor, however, is finite-dimensional (for a finite domain). The parallel reservoir architecture implicitly exploits the spatial locality of the dynamics: the state at a given point depends primarily on nearby points, at least over short times.

The ergodic-theoretic perspective applies as well: the KS equation has an SRB-like measure on its attractor, and the reservoir's ability to replicate the climate corresponds to approximating this measure.

---

## 17.8 Open Theoretical Questions

We collect here the most significant open problems at the interface of dynamical systems, ergodic theory, and reservoir computing.

### 17.8.1 Optimal Reservoir Design

**Problem.** Given a computational task (defined as a target functional on input sequences), what reservoir architecture (topology, weights, nonlinearity) is optimal?

No general theory exists. Current practice relies on hyperparameter search, guided by heuristics (spectral radius near 1, sparse connectivity, etc.). A theory of optimal reservoir design would be a major advance.

### 17.8.2 The Edge of Chaos

**Problem.** Is computation truly optimized at the edge of chaos? If so, for which tasks and in what precise sense?

The evidence is mixed. Bertschinger and Natschläger (2004) showed that the edge of chaos maximizes certain information-theoretic measures. But Verstraeten et al. (2007) found that the optimal spectral radius depends strongly on the task. A rigorous understanding of when and why the edge of chaos is beneficial remains elusive.

### 17.8.3 Capacity and Approximation Bounds

**Problem.** Can we obtain tighter bounds on the information processing capacity and approximation error of specific reservoir architectures?

Dambre et al. (2012) showed that the total IPC is at most $N$ (the reservoir size), but this bound is often not tight. For structured tasks, much smaller reservoirs may suffice. A task-dependent capacity theory would be valuable.

### 17.8.4 Generalization Theory

**Problem.** What are the proper generalization bounds for reservoir computing?

The connection to ergodic theory (Chapter 16) suggests that mixing rates should control generalization. Faster mixing means the training data are "more independent," so generalization should be better. Making this precise — connecting mixing coefficients to PAC-style bounds — is an active area.

Gonon and Ortega (2020) have made progress using tools from statistical learning theory adapted to the time-series setting, but a complete theory is lacking.

### 17.8.5 Ergodicity of Driven Reservoirs

**Problem.** Under what conditions on the input process and reservoir architecture is the driven reservoir system ergodic?

If the input is i.i.d. or a stationary ergodic process, and the reservoir has the echo state property, one expects the driven system to be ergodic. But precise conditions — especially for non-stationary or weakly dependent inputs — are not fully established.

### 17.8.6 Connections to Kernel Methods

The reservoir implicitly defines a kernel on input sequences:

$$K(\mathbf{u}, \mathbf{v}) = \langle \mathbf{x}(\mathbf{u}), \mathbf{x}(\mathbf{v}) \rangle,$$

where $\mathbf{x}(\mathbf{u})$ is the reservoir state driven by input $\mathbf{u}$. This connects reservoir computing to the theory of reproducing kernel Hilbert spaces (RKHS).

**Problem.** Can kernel theory provide new insights into reservoir computing? Can we characterize the RKHS induced by specific reservoir architectures?

Some progress has been made (see Hermans & Schrauwen, 2012), but the full potential of this connection is unexplored.

### 17.8.7 Beyond Fading Memory

**Problem.** Can reservoir computers perform computations that require long-term memory?

By definition, fading-memory systems eventually forget the past. Near the edge of chaos, memory can be very long but still finite. For tasks requiring truly long-term dependencies (e.g., context-free grammars, long-range correlations), standard reservoirs are theoretically limited. Understanding these limitations precisely, and whether they can be overcome by architectural modifications, is an open question.

---

## 17.9 Conclusion: Looking Back and Forward

This textbook has traced a path through three deeply interconnected subjects.

In **Part I**, we developed the theory of dynamical systems: the geometry of phase spaces, the stability of fixed points and periodic orbits, the structure of bifurcations, and the emergence of chaos. We saw that even simple deterministic systems can exhibit bewilderingly complex behavior, and we developed tools — Lyapunov exponents, Poincaré maps, symbolic dynamics — to make sense of this complexity.

In **Part II**, we brought measure theory and ergodic theory to bear on dynamical systems. The ergodic theorems gave us a rigorous framework for the statistical properties of deterministic systems: time averages equal space averages for ergodic systems, mixing quantifies how fast correlations decay, and entropy measures the rate of information creation. These are not merely abstract tools — they provide the "right" language for understanding chaotic dynamics.

In **Part III**, we saw how these mathematical ideas converge in reservoir computing. A reservoir is a dynamical system used as a computational substrate. Its echo state property is a stability condition (Part I). Its ability to generalize from finite training data is governed by ergodic theory (Part II). Its computational capacity is measured by information-theoretic quantities rooted in entropy. The deep connections are not accidental: reservoir computing works *because* of the rich structure that dynamical systems and ergodic theory reveal.

The field is young and full of open problems. The questions listed in Section 17.8 are not idle curiosities — they are fundamental challenges whose resolution would deepen our understanding of computation, dynamics, and their interplay. We hope that the mathematical foundations laid in this book will equip the reader to engage with these questions.

---

## Exercises

**Exercise 17.1.** Consider the Mackey-Glass system with $\tau_d = 17$, sampled at intervals of $\Delta t = 6$. The attractor dimension is approximately 2.1. What is the minimum delay embedding dimension guaranteed by Takens' theorem to reconstruct the attractor? In practice, reservoir computers with $N = 300$ neurons achieve excellent predictions. Discuss why the practical requirement is so different from the Takens bound.

**Exercise 17.2.** In the hybrid reservoir computing approach (Section 17.2.3), suppose the knowledge-based model perfectly captures the linear dynamics but misses the nonlinear terms. Argue, using the universal approximation results of Chapter 15, that the reservoir can in principle learn the correction term. What properties must the reservoir have for this to work?

**Exercise 17.3.** Consider a delay-based photonic reservoir with delay time $\tau_D$ and $N$ virtual nodes separated by $\theta = \tau_D / N$. The input is held constant over each interval $\theta$.

(a) Write the state update equation for the virtual nodes $x_i(t)$, $i = 1, \ldots, N$, in terms of $x_{i-1}(t)$ and $x_N(t-1)$ (the delayed feedback).

(b) Identify the recurrent weight matrix $W$ implicitly defined by this architecture. What is its structure?

(c) Under what conditions on the nonlinearity $f$ and the feedback strength $\beta$ does this system satisfy the echo state property?

**Exercise 17.4 (Research-oriented).** The NGRC method uses polynomial features of delay embeddings. Suppose the target system has an attractor of dimension $d$ and the observable is generic.

(a) What is the minimum number of delays $k$ required by Takens' theorem?

(b) If we use polynomial features of degree $p$, how many total features are there as a function of $k$ and $p$?

(c) Discuss the curse of dimensionality: for what values of $d$ and $p$ does the feature space become impractically large? How might this be mitigated?

**Exercise 17.5 (Open-ended).** Choose a physical reservoir computing platform from Section 17.4 (photonic, mechanical, spintronic, or quantum). For your chosen platform:

(a) Identify the governing dynamical equations.

(b) Discuss what the echo state property means physically for this system.

(c) Identify the relevant Lyapunov exponents and discuss what regime (ordered, edge of chaos, chaotic) the system should operate in for optimal computation.

(d) What are the practical limitations of this platform (speed, noise, scalability)?

**Exercise 17.6 (Open-ended).** The parallel reservoir architecture for spatiotemporal systems (Section 17.7.1) divides space into overlapping regions. Consider the overlap width $w$ as a parameter.

(a) Argue that $w$ must be at least as large as the spatial correlation length of the system for the architecture to work.

(b) For the Kuramoto-Sivashinsky equation, estimate the spatial correlation length from the known properties of the attractor.

(c) What happens if $w$ is too small? Too large?

---

## Recommended Reading

This section provides an extended reading list, organized by topic, for readers who wish to go further.

### Reservoir Computing: Foundational Papers

- H. Jaeger, "The 'echo state' approach to analysing and training recurrent neural networks," GMD Technical Report 148, 2001. *The paper that started echo state networks.*
- W. Maass, T. Natschläger, and H. Markram, "Real-time computing without stable states: A new framework for neural computation based on perturbations," *Neural Computation* 14(11), 2002. *The liquid state machine paper.*
- M. Lukoševičius and H. Jaeger, "Reservoir computing approaches to recurrent neural network training," *Computer Science Review* 3(3), 2009. *The standard survey — an excellent entry point.*

### Reservoir Computing: Theory

- L. Grigoryeva and J.-P. Ortega, "Echo state networks are universal," *Neural Networks* 108, 2018. *The definitive universality result.*
- J. Dambre, D. Verstraeten, B. Schrauwen, and S. Massar, "Information processing capacity of dynamical systems," *Scientific Reports* 2, 2012. *Introduces and analyzes IPC.*
- L. Gonon and J.-P. Ortega, "Reservoir computing universality with stochastic inputs," *IEEE Transactions on Neural Networks and Learning Systems* 31(1), 2020. *Generalization bounds.*
- A. Hart, J. Hook, and J. Dawes, "Embedding and approximation theorems for echo state networks," *Neural Networks* 128, 2020. *Connects Takens' theorem to reservoir computing rigorously.*
- G. Manjunath and H. Jaeger, "Echo state property linked to an input: Exploring a fundamental characteristic of recurrent neural networks," *Neural Computation* 25(3), 2013. *Lyapunov exponent characterization of ESP.*

### Reservoir Computing: Applications

- J. Pathak, B. Hunt, M. Girvan, Z. Lu, and E. Ott, "Model-free prediction of large spatiotemporally chaotic systems from data: A reservoir computing approach," *Physical Review Letters* 120, 2018. *Climate replication and spatiotemporal prediction.*
- D. J. Gauthier, E. Bollt, A. Griffith, and W. A. S. Barbosa, "Next generation reservoir computing," *Nature Communications* 12, 2021. *The NGRC framework.*
- H. Jaeger and H. Haas, "Harnessing nonlinearity: Predicting chaotic systems and saving energy in wireless communication," *Science* 304, 2004. *An influential early demonstration.*

### Physical Reservoir Computing

- L. Appeltant et al., "Information processing using a single dynamical node as complex system," *Nature Communications* 2, 2011. *The first delay-based photonic reservoir.*
- L. Larger et al., "Photonic information processing beyond Turing: an optoelectronic implementation of reservoir computing," *Optics Express* 20(3), 2012. *Photonic RC at high speed.*
- K. Nakajima and I. Fischer (eds.), *Reservoir Computing: Theory, Physical Implementations, and Applications*, Springer, 2021. *A comprehensive edited volume on physical RC.*
- G. Tanaka et al., "Recent advances in physical reservoir computing: A review," *Neural Networks* 115, 2019. *A thorough survey of physical implementations.*

### Dynamical Systems and Ergodic Theory (General)

- S. Strogatz, *Nonlinear Dynamics and Chaos*, 2nd ed., Westview Press, 2015. *The standard undergraduate textbook on dynamical systems.*
- A. Katok and B. Hasselblatt, *Introduction to the Modern Theory of Dynamical Systems*, Cambridge University Press, 1995. *The comprehensive graduate reference.*
- P. Walters, *An Introduction to Ergodic Theory*, Springer, 1982. *The standard introduction to ergodic theory.*
- V. I. Arnold, *Ordinary Differential Equations*, MIT Press, 1978. *A classic with geometric insight.*

### Further Directions

- N. Bertschinger and T. Natschläger, "Real-time computation at the edge of chaos in recurrent neural networks," *Neural Computation* 16(7), 2004. *The edge-of-chaos hypothesis for reservoir computing.*
- C. Gallicchio and A. Micheli, "Deep echo state network (DeepESN): A brief survey," arXiv:1712.04323, 2017. *Deep reservoir architectures.*
- M. Hermans and B. Schrauwen, "Recurrent kernel machines: Computing with infinite echo state networks," *Neural Computation* 24(1), 2012. *The kernel perspective on reservoir computing.*
- K. Fujii and K. Nakajima, "Harnessing disordered-ensemble quantum dynamics for machine learning," *Physical Review Applied* 8, 2017. *Quantum reservoir computing.*
