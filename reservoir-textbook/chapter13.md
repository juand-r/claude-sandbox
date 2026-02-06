# Chapter 13: From Dynamical Systems to Computation

> *"The purpose of computing is insight, not numbers."*
> — Richard Hamming

---

## Part III: Reservoir Computing

With Parts I and II behind us, the reader now commands a substantial toolkit: topological dynamics, stability theory, invariant measures, ergodicity, mixing, Lyapunov exponents, and the reconstruction theorems of Takens. These were developed in their own right, as the mathematical theory of systems that evolve in time. But dynamical systems theory is not merely descriptive. In Part III, we turn to a question that may at first seem surprising:

*Can a dynamical system compute?*

The answer is yes, and the framework that makes this precise — **reservoir computing** — draws directly on the mathematics we have built. This chapter provides the bridge.

---

## 13.1 Computation with Dynamics: A Historical Perspective

The idea that physical processes can perform computation is as old as computation itself. Before exploring reservoir computing in mathematical detail, it is worth recalling this history, because it reveals that the connection between dynamics and computation is not an analogy — it is an identity.

### 13.1.1 Mechanical and Analog Computers

The earliest computers were dynamical systems in the most literal sense. Charles Babbage's Difference Engine (1822) and Analytical Engine (1837) were mechanical devices: gears rotated, levers translated, and the physical state of the machine encoded the state of a computation. The tide-predicting machines of Lord Kelvin (1876) used systems of pulleys and gears to sum harmonic components — they were analog dynamical systems whose trajectories traced the solution to a computational problem.

The differential analyzers of Vannevar Bush (1931) solved ordinary differential equations by constructing a physical system whose dynamics were governed by those same equations. Here the connection is transparent: the machine does not *simulate* the dynamical system; the machine *is* the dynamical system, and its trajectory *is* the solution.

These examples suggest a principle: **any sufficiently rich dynamical system can, in some sense, compute**. The question is what "sufficiently rich" means.

### 13.1.2 Turing Machines as Dynamical Systems

Even the most abstract model of computation — the Turing machine — is a dynamical system in disguise. Recall the definition: a Turing machine consists of a finite set of states $Q$, a tape alphabet $\Gamma$, a transition function $\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$, and distinguished start, accept, and reject states. At each step, the machine reads a symbol, writes a symbol, changes state, and moves the tape head.

Let us formalize this. The **configuration** of a Turing machine at time $t$ is a triple $c(t) = (q(t), \tau(t), p(t))$, where $q(t) \in Q$ is the current state, $\tau(t): \mathbb{Z} \to \Gamma$ is the tape contents, and $p(t) \in \mathbb{Z}$ is the head position. The set of all configurations forms a (countably infinite) space $\mathcal{C}$, and the transition function induces a map

$$F: \mathcal{C} \to \mathcal{C}, \qquad c(t+1) = F(c(t)).$$

This is a discrete deterministic dynamical system on $\mathcal{C}$. The orbit $\{c(0), c(1), c(2), \ldots\}$ is the computation. A halting computation corresponds to a trajectory that reaches a fixed point (or more precisely, a subset of configurations from which $F$ is undefined or trivially the identity). A non-halting computation corresponds to a trajectory that never enters this set — the orbit wanders indefinitely through $\mathcal{C}$.

From this viewpoint, the halting problem asks whether a given initial condition leads to a trajectory that converges to a fixed point. Undecidability, in dynamical terms, is the statement that there is no algorithm to determine this for all initial conditions. The reader may find this reminiscent of the difficulties we encountered in Part I when asking whether a given point lies in the basin of attraction of an attractor.

### 13.1.3 Neural Networks as Dynamical Systems

The modern resurgence of interest in computation-through-dynamics comes from neural networks. We will treat these in detail in Section 13.2, but the essential observation is this: a recurrent neural network is a parameterized discrete dynamical system on $\mathbb{R}^N$. The parameters (weights, biases) determine the map, and the network's behavior on a given input is the trajectory of this system. Training the network — adjusting the parameters so that the trajectories produce desired outputs — is a problem in the control of dynamical systems.

### 13.1.4 The Central Question

The history above leads us to a central question:

> If dynamical systems can exhibit rich, complex behavior — chaos, sensitive dependence, mixing, strange attractors — can we *harness* that complexity for computation?

The intuition is appealing. A chaotic system explores its state space in an intricate, structured way. A mixing system, as we saw in Part II, forgets initial conditions but retains statistical structure. An ergodic system visits every part of its state space. These properties sound like they could be useful for processing information — but the intuition needs to be made precise.

Reservoir computing is the framework that does this. Before we can introduce it, we need to understand the computational systems it grew out of: neural networks.

---

## 13.2 Neural Networks as Dynamical Systems

We now introduce neural networks with enough precision for mathematical analysis. The reader who has encountered neural networks in a machine learning course will find a different emphasis here: we care about the *dynamics*, not the *implementation*.

### 13.2.1 Feedforward Networks: Static Maps

A **feedforward neural network** is a parameterized function $f_\theta: \mathbb{R}^m \to \mathbb{R}^p$ constructed by composing affine maps with pointwise nonlinearities. A network with $L$ layers takes the form

$$f_\theta(\mathbf{x}) = W_L \,\sigma\!\big(W_{L-1}\,\sigma\!\big(\cdots \sigma(W_1 \mathbf{x} + \mathbf{b}_1) \cdots\big) + \mathbf{b}_{L-1}\big) + \mathbf{b}_L,$$

where $W_\ell \in \mathbb{R}^{n_{\ell} \times n_{\ell-1}}$ are weight matrices, $\mathbf{b}_\ell \in \mathbb{R}^{n_\ell}$ are bias vectors, and $\sigma: \mathbb{R} \to \mathbb{R}$ is a nonlinear **activation function** applied componentwise. Common choices include:

- The **hyperbolic tangent**: $\sigma(x) = \tanh(x)$.
- The **logistic sigmoid**: $\sigma(x) = (1 + e^{-x})^{-1}$.
- The **ReLU** (rectified linear unit): $\sigma(x) = \max(0, x)$.

The parameter vector $\theta$ collects all weights and biases. The universal approximation theorem (Cybenko 1989, Hornik et al. 1989) guarantees that, under mild conditions on $\sigma$, such networks can approximate any continuous function on a compact set to arbitrary accuracy, provided $n_1$ (the width of the hidden layer) is sufficiently large.

**Crucially, a feedforward network is not a dynamical system.** It is a static map: given an input $\mathbf{x}$, it produces an output $f_\theta(\mathbf{x})$. There is no temporal evolution, no state that persists from one input to the next. Feedforward networks have no memory. If we present a sequence of inputs $\mathbf{x}(1), \mathbf{x}(2), \ldots$, the output at time $t$ depends only on $\mathbf{x}(t)$, not on any previous input. For many tasks — image classification, for instance — this is sufficient. But for tasks that involve temporal structure — speech, time series, control — it is not.

### 13.2.2 Recurrent Neural Networks: Dynamics on State Space

A **recurrent neural network** (RNN) introduces a state vector $\mathbf{h}(t) \in \mathbb{R}^N$ that evolves over discrete time:

$$\boxed{\mathbf{h}(t+1) = \sigma\!\big(W\mathbf{h}(t) + W_{\text{in}}\mathbf{u}(t) + \mathbf{b}\big)}$$

where:

- $\mathbf{h}(t) \in \mathbb{R}^N$ is the **hidden state** (or simply the *state*) at time $t$,
- $\mathbf{u}(t) \in \mathbb{R}^m$ is the **input** at time $t$,
- $W \in \mathbb{R}^{N \times N}$ is the **recurrent weight matrix**,
- $W_{\text{in}} \in \mathbb{R}^{N \times m}$ is the **input weight matrix**,
- $\mathbf{b} \in \mathbb{R}^N$ is a **bias vector**,
- $\sigma: \mathbb{R} \to \mathbb{R}$ is a nonlinear activation function, applied componentwise.

The output is typically produced by a **readout** (or output) layer:

$$\mathbf{y}(t) = g\!\big(W_{\text{out}}\mathbf{h}(t) + \mathbf{b}_{\text{out}}\big),$$

where $W_{\text{out}} \in \mathbb{R}^{p \times N}$, and $g$ is an output activation (often the identity for regression tasks).

**This is a dynamical system.** Specifically, it is a **nonautonomous discrete dynamical system** (or, equivalently, a skew-product system driven by the input signal). For each fixed input sequence $\{\mathbf{u}(t)\}_{t \geq 0}$, the state evolves according to time-dependent maps

$$F_t: \mathbb{R}^N \to \mathbb{R}^N, \qquad F_t(\mathbf{h}) = \sigma(W\mathbf{h} + W_{\text{in}}\mathbf{u}(t) + \mathbf{b}).$$

The state at time $t$ is obtained by composition:

$$\mathbf{h}(t) = F_{t-1} \circ F_{t-2} \circ \cdots \circ F_0(\mathbf{h}(0)).$$

When the input is absent ($\mathbf{u}(t) = \mathbf{0}$ for all $t$), we recover an **autonomous** system

$$\mathbf{h}(t+1) = F(\mathbf{h}(t)), \qquad F(\mathbf{h}) = \sigma(W\mathbf{h} + \mathbf{b}),$$

which is exactly the kind of iterated map we studied in Part I. Let us make some observations.

**State space.** If $\sigma = \tanh$, then the image of $F$ lies in $(-1,1)^N$, so the state space is effectively the open hypercube. For $\sigma$ equal to the logistic sigmoid, the state space is $(0,1)^N$. For ReLU activations, the state space is $[0,\infty)^N$, and trajectories can be unbounded.

**Fixed points.** A fixed point of the autonomous system satisfies $\mathbf{h}^* = \sigma(W\mathbf{h}^* + \mathbf{b})$. For $\sigma = \tanh$ and $\mathbf{b} = \mathbf{0}$, the origin $\mathbf{h}^* = \mathbf{0}$ is always a fixed point. Its stability is determined by the Jacobian at $\mathbf{0}$:

$$DF(\mathbf{0}) = \text{diag}(\sigma'(W \cdot \mathbf{0} + \mathbf{b})) \cdot W = \text{diag}(\sigma'(\mathbf{b})) \cdot W.$$

When $\mathbf{b} = \mathbf{0}$ and $\sigma = \tanh$, we have $\sigma'(0) = 1$, so $DF(\mathbf{0}) = W$. By our stability theorems from Chapter 3, the origin is asymptotically stable if and only if the **spectral radius** $\rho(W) < 1$. If $\rho(W) > 1$, the origin is unstable, and the dynamics may exhibit more complex behavior — limit cycles, quasi-periodic orbits, or chaos.

**Dependence on $W$.** The recurrent weight matrix $W$ is the single most important parameter of the system. It determines the topology and geometry of the dynamics. This will become a recurring theme in Part III.

### 13.2.3 A Remark on Continuous-Time Formulations

The discrete-time RNN described above has a natural continuous-time counterpart. Consider the ODE

$$\tau \dot{\mathbf{h}}(t) = -\mathbf{h}(t) + \sigma\!\big(W\mathbf{h}(t) + W_{\text{in}}\mathbf{u}(t) + \mathbf{b}\big),$$

where $\tau > 0$ is a time constant. This is a system of $N$ coupled first-order ODEs — a continuous-time dynamical system on $\mathbb{R}^N$, driven by the input $\mathbf{u}(t)$. The discrete-time RNN can be viewed as a forward Euler discretization of this ODE with step size $\Delta t = \tau$. This connection to ODEs will be important when we discuss Liquid State Machines in Section 13.5.

---

## 13.3 The Problem of Training Recurrent Neural Networks

To use an RNN for a computational task, one must choose the parameters $\theta = (W, W_{\text{in}}, \mathbf{b}, W_{\text{out}}, \mathbf{b}_{\text{out}})$ so that the network produces desired outputs. This is the **training problem**, and for RNNs it is notoriously difficult. Understanding *why* it is difficult requires dynamical systems thinking — and this understanding will motivate reservoir computing.

### 13.3.1 The Optimization Problem

Suppose we have a training sequence: inputs $\{\mathbf{u}(t)\}_{t=0}^{T-1}$ and desired outputs $\{\mathbf{d}(t)\}_{t=0}^{T-1}$. Define a loss function

$$\mathcal{L}(\theta) = \sum_{t=0}^{T-1} \ell\!\big(\mathbf{y}(t),\, \mathbf{d}(t)\big),$$

where $\ell$ is a per-step loss (e.g., $\ell(\mathbf{y}, \mathbf{d}) = \|\mathbf{y} - \mathbf{d}\|^2$) and $\mathbf{y}(t)$ depends on $\theta$ through the entire trajectory $\mathbf{h}(0), \mathbf{h}(1), \ldots, \mathbf{h}(t)$. The training problem is to minimize $\mathcal{L}(\theta)$ over $\theta$.

### 13.3.2 Backpropagation Through Time

The standard approach is gradient descent: compute $\nabla_\theta \mathcal{L}$ and update $\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}$ for some learning rate $\eta > 0$. To compute the gradient, one "unrolls" the recurrence in time, treating the RNN as a very deep feedforward network with shared weights, and applies the chain rule. This is **backpropagation through time** (BPTT).

Consider the gradient of $\mathcal{L}$ with respect to the recurrent weights $W$. By the chain rule:

$$\frac{\partial \mathcal{L}}{\partial W} = \sum_{t=0}^{T-1} \frac{\partial \ell(t)}{\partial \mathbf{y}(t)} \frac{\partial \mathbf{y}(t)}{\partial \mathbf{h}(t)} \sum_{k=0}^{t} \left(\prod_{j=k}^{t-1} \frac{\partial \mathbf{h}(j+1)}{\partial \mathbf{h}(j)}\right) \frac{\partial^+ \mathbf{h}(k)}{\partial W},$$

where $\frac{\partial^+ \mathbf{h}(k)}{\partial W}$ denotes the "immediate" (direct) partial derivative at time $k$, treating $\mathbf{h}(k-1)$ as fixed. The key term is the product of Jacobians:

$$\prod_{j=k}^{t-1} J(j), \qquad \text{where } J(j) = \frac{\partial \mathbf{h}(j+1)}{\partial \mathbf{h}(j)} = D_j \cdot W,$$

and $D_j = \text{diag}\!\big(\sigma'(W\mathbf{h}(j) + W_{\text{in}}\mathbf{u}(j) + \mathbf{b})\big)$ is the diagonal matrix of activation derivatives at time $j$.

### 13.3.3 The Vanishing and Exploding Gradient Problem

The gradient signal propagating from time $t$ back to time $k$ is scaled by the matrix product $\prod_{j=k}^{t-1} J(j)$. This is a product of $(t-k)$ matrices. The behavior of such products is exactly the subject of **multiplicative ergodic theory** (Chapter 11).

By the Oseledets multiplicative ergodic theorem, for an ergodic system the product $\prod_{j=0}^{n-1} J(j)$ grows (or decays) exponentially at rates determined by the **Lyapunov exponents** $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_N$. More precisely, the norm of the product acting on a "generic" vector $\mathbf{v}$ satisfies

$$\lim_{n \to \infty} \frac{1}{n} \log \left\|\prod_{j=0}^{n-1} J(j) \, \mathbf{v}\right\| = \lambda_1.$$

This has immediate consequences for gradient computation:

- If $\lambda_1 > 0$ (the maximal Lyapunov exponent is positive), then the gradient products grow exponentially. This is the **exploding gradient problem**: the gradient $\partial \mathcal{L}/\partial W$ diverges as $T$ increases, making optimization unstable.

- If $\lambda_1 < 0$ (all Lyapunov exponents are negative), then the gradient products decay exponentially. This is the **vanishing gradient problem**: the gradient contribution from distant time steps is exponentially suppressed, and the network cannot learn long-range temporal dependencies.

The connection to dynamics is direct. Recall from Part I that $\lambda_1 > 0$ characterizes sensitive dependence on initial conditions — chaos. An RNN operating in the chaotic regime has exploding gradients. An RNN in the stable (contracting) regime has vanishing gradients. The boundary between these regimes — the **edge of chaos** — will turn out to be precisely where reservoir computing is most effective.

**Remark 13.1.** This connection was recognized early, though not in the language of Lyapunov exponents. Hochreiter's 1991 diploma thesis identified the fundamental difficulty: the error signal flowing backwards through time either vanishes or explodes. Bengio, Simard, and Frasconi (1994) provided a more detailed analysis and coined the term "vanishing gradient problem." Their analysis was essentially a study of the spectral properties of the Jacobian products — multiplicative ergodic theory in all but name.

### 13.3.4 Attempts to Solve the Problem

The vanishing/exploding gradient problem has driven much of the development of recurrent architectures.

**Gradient clipping.** A pragmatic fix: if $\|\nabla_\theta \mathcal{L}\|$ exceeds a threshold, rescale it. This prevents explosion but does not address vanishing.

**Long Short-Term Memory (LSTM).** Hochreiter and Schmidhuber (1997) introduced a carefully designed architecture with **gating mechanisms** that allow the network to maintain a roughly constant error flow over time. The LSTM cell contains a "memory cell" $c(t)$ governed by

$$\begin{aligned}
\mathbf{f}(t) &= \sigma_g\!\big(W_f \mathbf{h}(t-1) + W_{f,\text{in}} \mathbf{u}(t) + \mathbf{b}_f\big), \\
\mathbf{i}(t) &= \sigma_g\!\big(W_i \mathbf{h}(t-1) + W_{i,\text{in}} \mathbf{u}(t) + \mathbf{b}_i\big), \\
\mathbf{c}(t) &= \mathbf{f}(t) \odot \mathbf{c}(t-1) + \mathbf{i}(t) \odot \tanh\!\big(W_c \mathbf{h}(t-1) + W_{c,\text{in}} \mathbf{u}(t) + \mathbf{b}_c\big),
\end{aligned}$$

where $\sigma_g$ is the logistic sigmoid, $\odot$ denotes the Hadamard (elementwise) product, and $\mathbf{f}(t)$, $\mathbf{i}(t)$ are the "forget" and "input" gates, respectively. The key idea, in dynamical terms, is that when $\mathbf{f}(t) \approx \mathbf{1}$ and $\mathbf{i}(t) \approx \mathbf{0}$, the cell state satisfies $\mathbf{c}(t) \approx \mathbf{c}(t-1)$ — the Jacobian $\partial \mathbf{c}(t)/\partial \mathbf{c}(t-1)$ is close to the identity. This ensures that the Lyapunov exponent along the cell state direction is close to zero, preventing both vanishing and explosion.

**Gated Recurrent Units (GRU).** Cho et al. (2014) proposed a simplified gating architecture with similar properties.

These architectures are effective in practice but come at a cost: they are complex, require careful initialization, and training still involves gradient descent through long unrolled computation graphs. The computational cost scales with $T \times N \times |\theta|$, and convergence can be slow.

This motivates a radical question: *do we need to train the recurrent dynamics at all?*

---

## 13.4 The Key Insight: Separate Dynamics from Readout

The central idea of reservoir computing emerges from a simple but powerful observation.

### 13.4.1 The Separation Principle

Consider again the RNN equation

$$\mathbf{h}(t+1) = \sigma\!\big(W\mathbf{h}(t) + W_{\text{in}}\mathbf{u}(t) + \mathbf{b}\big), \qquad \mathbf{y}(t) = W_{\text{out}}\mathbf{h}(t).$$

The system has two parts:

1. The **dynamics**: the recurrent evolution $\mathbf{h}(t) \mapsto \mathbf{h}(t+1)$, governed by $(W, W_{\text{in}}, \mathbf{b})$.
2. The **readout**: the linear map $\mathbf{h}(t) \mapsto \mathbf{y}(t)$, governed by $W_{\text{out}}$.

All the difficulty of training lies in part (1) — the recurrent dynamics. The readout is a simple linear map. The insight is:

> **Fix the dynamics. Train only the readout.**

That is, choose $W$, $W_{\text{in}}$, and $\mathbf{b}$ randomly (according to certain principles we will develop in Chapter 14), and never modify them. Use the fixed recurrent system as a **reservoir** — a rich source of dynamical features. Then find $W_{\text{out}}$ by solving a linear regression problem:

$$W_{\text{out}} = \arg\min_{W_{\text{out}}} \sum_{t} \|\mathbf{y}(t) - \mathbf{d}(t)\|^2 = \arg\min_{W_{\text{out}}} \sum_{t} \|W_{\text{out}} \mathbf{h}(t) - \mathbf{d}(t)\|^2.$$

This is a standard linear least-squares problem with a closed-form solution. Let $H \in \mathbb{R}^{T \times N}$ be the matrix whose rows are $\mathbf{h}(t)^\top$, and let $D \in \mathbb{R}^{T \times p}$ have rows $\mathbf{d}(t)^\top$. Then

$$W_{\text{out}}^\top = (H^\top H)^{-1} H^\top D = H^+ D,$$

where $H^+$ denotes the Moore-Penrose pseudoinverse. In practice one often uses **Tikhonov regularization** (ridge regression):

$$W_{\text{out}}^\top = (H^\top H + \alpha I)^{-1} H^\top D,$$

for a small $\alpha > 0$, which improves numerical stability and generalization.

### 13.4.2 Why This Might Work

At first glance, this seems too simple. How can a random dynamical system, with no task-specific training, produce useful computations?

The answer lies in the nature of the reservoir dynamics. The state $\mathbf{h}(t)$ depends, through the recurrence, on the entire history of inputs $\mathbf{u}(0), \mathbf{u}(1), \ldots, \mathbf{u}(t)$. The nonlinear recurrence creates a rich, high-dimensional representation of this input history. The reservoir performs a **nonlinear expansion**: it maps the input history into a high-dimensional state space $\mathbb{R}^N$ where different features of the input sequence become linearly separable.

Consider an analogy from linear algebra. The **kernel trick** in machine learning maps data into a high-dimensional feature space where nonlinear relationships become linear. The reservoir does something similar, but *in time*: it maps a temporal input signal into a high-dimensional state space where temporal relationships become accessible to a linear readout.

For this to work, the reservoir must satisfy certain properties:

1. **The input must influence the state.** The reservoir must be driven by the input — it cannot ignore it.
2. **The state must depend on the input history, not just the current input.** The reservoir must have memory.
3. **The state must eventually forget the distant past.** Otherwise the representation is dominated by ancient history and cannot adapt to current inputs.
4. **Different input histories must produce different states.** The reservoir must be able to distinguish inputs.
5. **The state must be sufficiently high-dimensional and nonlinear.** A linear reservoir can only compute linear functionals of the input.

These desiderata translate directly into dynamical systems properties. Property (3) is a form of asymptotic stability — specifically, the **echo state property** that we will formalize in Chapter 14. Properties (1)–(4) together relate to the concept of **observability** from control theory. Property (5) relates to the dimension and nonlinearity of the dynamics.

### 13.4.3 The Computational Advantage

The practical advantages of this approach are significant:

- **Training cost.** Solving a linear regression problem costs $O(N^2 T + N^3)$, compared to $O(N^2 T \cdot \text{epochs})$ for BPTT. For large $T$, this is a dramatic saving.
- **No vanishing/exploding gradients.** There is no backpropagation through time. The gradient problem simply does not arise.
- **Stability.** Linear regression is a convex optimization problem with a unique global minimum (when $H^\top H + \alpha I$ is invertible, which is always the case for $\alpha > 0$). There are no local minima, saddle points, or other pathologies of the loss landscape.
- **Simplicity.** The implementation is straightforward.

The cost, of course, is that we have given up the ability to optimize the dynamics. The reservoir must be "good enough" as drawn from a random distribution. This places the burden on understanding *which* random dynamical systems make good reservoirs — a question that our mathematical toolkit is well-equipped to address.

---

## 13.5 Two Independent Inventions

The reservoir computing paradigm was discovered independently, and nearly simultaneously, by two research groups working in different communities with different motivations. This convergence lends credibility to the idea: the same core principle emerged from different starting points.

### 13.5.1 Echo State Networks (Jaeger, 2001)

Herbert Jaeger, working at the German National Research Center for Information Technology (GMD), introduced **Echo State Networks** (ESNs) in a technical report in 2001. The framework is exactly the discrete-time system described in Section 13.4:

$$\mathbf{h}(t+1) = \tanh\!\big(W\mathbf{h}(t) + W_{\text{in}}\mathbf{u}(t)\big), \qquad \mathbf{y}(t) = W_{\text{out}}\mathbf{h}(t).$$

Jaeger's key contributions were:

1. The formulation of the **echo state property** (ESP): the requirement that the reservoir state $\mathbf{h}(t)$ be asymptotically independent of the initial condition $\mathbf{h}(0)$, depending only on the input history. This is a fading-memory or input-forgetting property.

2. A practical sufficient condition: the ESP holds if the spectral radius $\rho(W) < 1$. (As we shall see in Chapter 14, this condition is sufficient but not necessary.)

3. Empirical demonstrations that ESNs, despite their simplicity, could match or exceed the performance of fully-trained RNNs on benchmark time-series prediction tasks — at a fraction of the computational cost.

The name "echo state" reflects the fading-memory property: the current state is an "echo" of past inputs, with recent inputs echoing more loudly than distant ones.

### 13.5.2 Liquid State Machines (Maass, Natschla\u0308ger, Markram, 2002)

Independently, Wolfgang Maass, Thomas Natschla\u0308ger, and Henry Markram, working at the intersection of computational neuroscience and theoretical computer science, introduced **Liquid State Machines** (LSMs) in 2002. Their motivation was biological: the neocortex appears to process information using networks of spiking neurons that are not precisely tuned, yet are capable of remarkable computational feats. How?

The LSM framework uses a continuous-time dynamical system as the reservoir:

$$\tau_i \dot{v}_i(t) = -v_i(t) + \sum_j w_{ij}\, s_j(t) + \sum_k w_{ik}^{\text{in}}\, u_k(t),$$

where $v_i(t)$ is the membrane potential of neuron $i$, $s_j(t)$ represents the (nonlinear) output of neuron $j$, and the system is driven by the input signal $\{u_k(t)\}$. The neurons may be spiking (integrate-and-fire models) rather than rate-based, and the connections may include synaptic dynamics and delays. Despite the differences in formulation, the underlying principle is identical: a fixed, random, high-dimensional dynamical system driven by input, with a trained linear readout.

Maass et al. introduced the notion of the **separation property**: the requirement that different input streams produce sufficiently different internal states. They proved, under certain conditions, a form of computational universality: any time-invariant filter with fading memory can be approximated by an LSM with a sufficiently large reservoir and an appropriate readout.

### 13.5.3 Unification: Reservoir Computing

For several years, the ESN and LSM communities developed largely in parallel, with different terminology, different implementation details, and different theoretical frameworks. In 2007, Verstraeten, Schrauwen, D'Haene, and Stroobandt proposed the term **reservoir computing** as a unifying label for both approaches, identifying their shared computational principle:

> A fixed, high-dimensional, nonlinear dynamical system (the *reservoir*) transforms input signals into a rich state representation, from which a trained linear readout extracts the desired computation.

This unification was significant because it revealed the essential structure: the choice of reservoir (discrete-time vs. continuous-time, rate-based vs. spiking, small vs. large) is a design choice. The mathematical principles governing performance — the echo state property, separation, approximation capacity — are shared.

The 2009 survey by Lukoševičius and Jaeger provides a comprehensive account of the state of the field at that time and remains an excellent reference.

---

## 13.6 Why This Connects to Parts I and II

We close this chapter by making explicit the connections between reservoir computing and the mathematical theory developed in the first two parts of this book. These connections are not superficial analogies — they are the theoretical foundations on which reservoir computing rests.

### 13.6.1 Stability and the Echo State Property (Part I)

The echo state property requires that the reservoir dynamics be, in a certain sense, **asymptotically stable** with respect to initial conditions. This connects directly to Chapter 3 (stability of fixed points), Chapter 4 (Lyapunov stability), and Chapter 5 (structural stability). The spectral radius condition $\rho(W) < 1$ is a linearization-based stability criterion, just as in our analysis of discrete maps. In Chapter 14, we will formulate the echo state property precisely and prove it using contraction mapping arguments that generalize the stability theory of Part I.

### 13.6.2 Chaos and the Edge of Chaos (Part I)

The vanishing/exploding gradient dichotomy reflects the dichotomy between stable and chaotic dynamics. As we discussed in Chapter 7, the transition to chaos in iterated maps is characterized by the maximal Lyapunov exponent crossing zero. Empirically, reservoirs perform best near this transition — the **edge of chaos** — where the dynamics are rich enough to generate useful features but stable enough to maintain the echo state property. We will make this precise in Chapter 15 using the Lyapunov exponent theory from Part I.

### 13.6.3 Ergodicity and Information Processing (Part II)

The ergodic theory of Part II provides the language for discussing how reservoirs process information statistically. When driven by a stationary ergodic input, the reservoir state process $\{\mathbf{h}(t)\}$ is itself a stationary process (assuming the echo state property holds). The **mixing properties** studied in Chapter 9 determine how quickly the reservoir forgets its past and how effectively it integrates new information. The **entropy** concepts from Chapter 10 quantify the information content of the reservoir state. The **Oseledets theorem** from Chapter 11 governs the growth rates of perturbations and hence the sensitivity of the reservoir to its input.

### 13.6.4 Takens' Theorem and Reconstruction (Part I)

Perhaps the deepest connection is to **Takens' embedding theorem** (Chapter 6). Recall the setup: given a dynamical system on a manifold $M$ with a map $\Phi: M \to M$ and an observation function $h: M \to \mathbb{R}$, the delay-coordinate map

$$\Psi(\mathbf{x}) = \big(h(\mathbf{x}),\, h(\Phi(\mathbf{x})),\, \ldots,\, h(\Phi^{d}(\mathbf{x}))\big)$$

is generically an embedding of $M$ into $\mathbb{R}^{d+1}$ when $d \geq 2\dim(M)$.

Now consider a reservoir driven by scalar observations $u(t) = h(\Phi^t(\mathbf{x}_0))$ of an unknown dynamical system. The reservoir state $\mathbf{h}(t)$ depends on $u(t), u(t-1), \ldots$ — it is a nonlinear function of the delay coordinates of the observed system. If the reservoir has the echo state property and is sufficiently high-dimensional, then $\mathbf{h}(t)$ provides a (nonlinear, learned) embedding of the underlying attractor.

This observation, first made rigorous by several authors in the 2010s, provides a theoretical justification for why reservoir computing is particularly effective for tasks involving dynamical systems: time-series prediction, system identification, attractor reconstruction, and Lyapunov exponent estimation. The reservoir, in effect, performs a generalized Takens embedding.

### 13.6.5 A Roadmap for Part III

The connections identified above will be developed rigorously in the chapters that follow:

- **Chapter 14** defines the echo state property precisely and establishes conditions under which it holds, using the language of contractions and stability from Part I.
- **Chapter 15** analyzes the dynamics of reservoirs — Lyapunov exponents, information dimension, and the edge of chaos — using tools from both Parts I and II.
- **Chapter 16** develops the approximation theory of reservoir computing: what functions can a reservoir compute, and how does this depend on the reservoir's dynamical properties?
- **Chapter 17** connects reservoir computing to Takens' theorem and explores applications to dynamical systems tasks.

The stage is set. We have seen that dynamical systems can compute, that recurrent neural networks are dynamical systems, that training these dynamics is hard, and that one can sidestep the difficulty by fixing the dynamics and training only a linear readout. The remainder of Part III develops the mathematical theory of this idea.

---

## Recommended Reading

1. **H. Jaeger** (2001). "The 'echo state' approach to analysing and training recurrent neural networks." *GMD Technical Report 148*. The foundational paper on Echo State Networks. Remarkably clear and still highly readable.

2. **W. Maass, T. Natschläger, and H. Markram** (2002). "Real-time computing without stable states: A new framework for neural computation based on perturbations." *Neural Computation*, 14(11):2531–2560. The Liquid State Machine paper. More theoretically ambitious than Jaeger's report, with results on computational universality.

3. **S. Hochreiter and J. Schmidhuber** (1997). "Long short-term memory." *Neural Computation*, 9(8):1735–1780. The LSTM paper, essential background for understanding what reservoir computing is an alternative to.

4. **Y. Bengio, P. Simard, and P. Frasconi** (1994). "Learning long-term dependencies with gradient descent is difficult." *IEEE Transactions on Neural Networks*, 5(2):157–166. The definitive early analysis of the vanishing gradient problem.

5. **D. Verstraeten, B. Schrauwen, M. D'Haene, and D. Stroobandt** (2007). "An experimental unification of reservoir computing methods." *Neural Networks*, 20(3):391–403. The paper that coined the term "reservoir computing" and unified ESNs and LSMs.

6. **M. Lukoševičius and H. Jaeger** (2009). "Reservoir computing approaches to recurrent neural network training." *Computer Science Review*, 3(3):127–149. An excellent survey of the field as of 2009, accessible and comprehensive.

7. **S. Hochreiter** (1991). "Untersuchungen zu dynamischen neuronalen Netzen." Diploma thesis, Technische Universität München. The first identification of the vanishing gradient problem, predating the Bengio et al. paper by three years.

For mathematical background on nonautonomous dynamical systems, the reader may consult:

8. **P. Kloeden and M. Rasmussen** (2011). *Nonautonomous Dynamical Systems*. American Mathematical Society. A rigorous treatment of the theory needed for input-driven systems.

---

## Exercises

**Exercise 13.1** (Fixed points and stability). Consider an autonomous RNN with $N = 2$, activation $\sigma = \tanh$, bias $\mathbf{b} = \mathbf{0}$, and recurrent weight matrix

$$W = \begin{pmatrix} 0 & a \\ -a & 0 \end{pmatrix}$$

for $a > 0$.

(a) Show that $\mathbf{h}^* = \mathbf{0}$ is a fixed point.

(b) Compute the Jacobian $DF(\mathbf{0})$ and determine the eigenvalues. For which values of $a$ is the fixed point asymptotically stable?

(c) The eigenvalues of $W$ are $\pm ia$. These are complex with modulus $a$. Explain, in terms of the dynamics, what you expect to observe for $a$ slightly less than 1 versus $a$ slightly greater than 1. Verify your prediction numerically by iterating the map for both cases.

---

**Exercise 13.2** (Vanishing gradients and Lyapunov exponents). Consider an autonomous RNN with $\sigma = \tanh$ and $\mathbf{b} = \mathbf{0}$. Let $\mathbf{h}^* = \mathbf{0}$ be the fixed point and assume $\rho(W) < 1$ so that $\mathbf{h}^*$ is asymptotically stable.

(a) Show that the Jacobian at any point $\mathbf{h}$ satisfies $\|J(\mathbf{h})\|_2 \leq \|W\|_2$, where $\|\cdot\|_2$ denotes the spectral norm (largest singular value). *Hint:* $|\tanh'(x)| \leq 1$ for all $x$.

(b) Conclude that for any trajectory $\mathbf{h}(0), \mathbf{h}(1), \ldots$ converging to the fixed point,

$$\left\|\prod_{j=0}^{n-1} J(j)\right\|_2 \leq \|W\|_2^n.$$

(c) What does this imply about the maximal Lyapunov exponent? What does it imply about the gradient $\partial \mathbf{h}(t)/\partial \mathbf{h}(0)$ as $t \to \infty$?

(d) Explain why the condition $\rho(W) < 1$ is insufficient to guarantee rapid vanishing of gradients, while $\|W\|_2 < 1$ is sufficient. Give an example of $W$ with $\rho(W) < 1$ but $\|W\|_2 > 1$.

---

**Exercise 13.3** (Linear reservoirs and limitations). Suppose we replace $\tanh$ with the identity function, obtaining a linear reservoir:

$$\mathbf{h}(t+1) = W\mathbf{h}(t) + W_{\text{in}}\mathbf{u}(t).$$

(a) Assuming $\rho(W) < 1$ and $\mathbf{h}(0) = \mathbf{0}$, show that

$$\mathbf{h}(t) = \sum_{k=0}^{t-1} W^{t-1-k} W_{\text{in}} \mathbf{u}(k).$$

(b) Show that the output $\mathbf{y}(t) = W_{\text{out}} \mathbf{h}(t)$ is a *linear* functional of the input history $\{\mathbf{u}(k)\}_{k=0}^{t-1}$. Specifically, $\mathbf{y}(t) = \sum_{k=0}^{t-1} C_{t-1-k} \,\mathbf{u}(k)$ for matrices $C_j$ that you should identify.

(c) Explain why a linear reservoir cannot approximate a nonlinear input-output map, no matter how large $N$ is. Why does this demonstrate the necessity of nonlinear activation functions?

---

**Exercise 13.4** (Reservoir computing by hand). Consider a scalar reservoir ($N = 1$) with $\sigma = \tanh$, weight $w = 0.9$, input weight $w_{\text{in}} = 0.5$, and no bias:

$$h(t+1) = \tanh(0.9\, h(t) + 0.5\, u(t)).$$

The task is to learn the identity map $d(t) = u(t)$ from the reservoir state.

(a) For the input sequence $u(t) = \sin(0.3\, t)$ with $t = 0, 1, \ldots, 50$ and $h(0) = 0$, compute the reservoir states $h(0), h(1), \ldots, h(50)$ numerically.

(b) Find $w_{\text{out}}$ by linear regression: $w_{\text{out}} = \arg\min_w \sum_{t=1}^{50} (w \cdot h(t) - u(t))^2$.

(c) How well does the trained readout approximate $u(t)$ on the training data? What about for $t = 51, \ldots, 100$ (generalization)?

(d) Repeat with $u(t) = \sin(0.3\, t) + 0.5\sin(0.7\, t)$. Does performance degrade? Why might a single-neuron reservoir struggle with more complex signals?

---

**Exercise 13.5** (Turing machines and dynamics). Let $M$ be a Turing machine with state set $Q = \{q_0, q_1, q_H\}$ (where $q_H$ is the halt state), tape alphabet $\Gamma = \{0, 1, \sqcup\}$ (where $\sqcup$ is blank), and transition function:

| State | Read | Write | Move | Next State |
|-------|------|-------|------|------------|
| $q_0$ | $0$ | $1$ | $R$ | $q_1$ |
| $q_0$ | $1$ | $0$ | $R$ | $q_0$ |
| $q_0$ | $\sqcup$ | $\sqcup$ | $L$ | $q_H$ |
| $q_1$ | $0$ | $0$ | $R$ | $q_0$ |
| $q_1$ | $1$ | $1$ | $R$ | $q_1$ |
| $q_1$ | $\sqcup$ | $\sqcup$ | $L$ | $q_H$ |

(a) Starting with tape contents $\ldots \sqcup\sqcup 0110 \sqcup\sqcup \ldots$, head at the leftmost $0$, and state $q_0$, trace the trajectory of the dynamical system $F: \mathcal{C} \to \mathcal{C}$ until the machine halts. Record the configuration at each step.

(b) What does this Turing machine compute? Describe its function in terms of the tape contents at start and at halt.

(c) Describe the "phase space" of this dynamical system. Is it finite-dimensional? Is it compact? Compare with the phase spaces of the continuous dynamical systems in Part I.

---

**Exercise 13.6** (Separation property). Consider two input sequences $\mathbf{u}^{(1)}(t)$ and $\mathbf{u}^{(2)}(t)$ that are identical for $t < T_0$ and differ for $t \geq T_0$. Let $\mathbf{h}^{(1)}(t)$ and $\mathbf{h}^{(2)}(t)$ be the corresponding reservoir states, starting from the same initial condition.

(a) Show that $\mathbf{h}^{(1)}(t) = \mathbf{h}^{(2)}(t)$ for all $t \leq T_0$.

(b) For $t > T_0$, define the separation $\delta(t) = \|\mathbf{h}^{(1)}(t) - \mathbf{h}^{(2)}(t)\|$. Show that for $\sigma = \tanh$,

$$\delta(t+1) \leq \|W\|_2 \, \delta(t) + \|W_{\text{in}}\|_2 \, \|\mathbf{u}^{(1)}(t) - \mathbf{u}^{(2)}(t)\|.$$

(c) Discuss the implications: if $\|W\|_2 < 1$, does the reservoir amplify or suppress differences between input signals? What if $\|W\|_2 > 1$? Why is this relevant to the reservoir's ability to distinguish different inputs?

(d) Argue that a good reservoir must balance two competing requirements: separation of different inputs (which benefits from larger $\|W\|_2$) and the echo state property (which requires the dynamics to be contractive in some sense). Relate this to the edge-of-chaos hypothesis.
