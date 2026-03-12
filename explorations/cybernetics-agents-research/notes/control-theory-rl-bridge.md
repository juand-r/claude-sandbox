# Control Theory and Reinforcement Learning: The Formal Bridge

## Research Notes — March 2026

These notes document the formal connections between control theory (rooted in cybernetics) and reinforcement learning (the optimization engine of modern AI). This is arguably the most direct mathematical bridge between Wiener's cybernetics and contemporary agent design.

---

## 1. The Formal Parallels

The two fields developed largely in parallel — control theory from engineering (Bellman, Kalman, Pontryagin, 1950s-60s) and RL from AI/psychology (Sutton, Barto, 1980s-90s) — but share deep mathematical structure.

### 1.1 Terminology Mapping

| Reinforcement Learning | Control Theory | Notes |
|---|---|---|
| State s | State x | Both represent the system's configuration at time t |
| Action a | Control input u | The agent's/controller's influence on the system |
| Reward r(s,a) | Negative cost -c(x,u) | RL maximizes reward; control minimizes cost. Mathematically: r = -c |
| Policy π(a\|s) | Control law / feedback controller u = μ(x) | Mapping from observations to actions |
| Value function V(s) | Cost-to-go J(x) / Lyapunov function V(x) | Expected cumulative future reward/cost from state s/x |
| Q-function Q(s,a) | Action-value / Hamiltonian H(x,u) | Value of taking action a in state s, then following policy |
| Transition model P(s'\|s,a) | State dynamics x_{k+1} = f(x_k, u_k) | RL: stochastic; control: often deterministic |
| Discount factor γ | Exponential weighting e^{-αt} | Both discount future costs/rewards |
| Bellman equation | Hamilton-Jacobi-Bellman (HJB) equation | Same principle of optimality, different domains |
| Episode | Trajectory / horizon | A sequence of state-action pairs |

### 1.2 The Bellman Equation ↔ HJB Equation

This is the deepest formal connection.

**Discrete-time Bellman equation (RL):**
```
V*(s) = max_a [ r(s,a) + γ Σ_{s'} P(s'|s,a) V*(s') ]
```

**Continuous-time HJB equation (control):**
```
-∂V/∂t = min_u [ c(x,u) + (∂V/∂x)^T f(x,u) ]
```

The HJB equation is obtained from the Bellman recursion by taking the limit as the time step dt → 0. The discrete Bellman equation *is* a discretization of the HJB PDE. This was first recognized by Rudolf Kalman, who connected Bellman's dynamic programming to Hamilton-Jacobi theory from classical mechanics.

The continuous-time Q-function Q(x,u) — the inner expression being minimized in the HJB — maps directly to the Q-function in RL. This makes Q-learning a discrete approximation to solving the HJB equation.

**Key insight:** Both equations encode Bellman's **principle of optimality** — the optimal policy from any state must also be optimal from all successor states. The difference is domain: discrete stochastic (RL) vs. continuous deterministic or stochastic (control).

### 1.3 The MDP Framework ↔ State-Space Framework

**MDP (RL):** (S, A, P, R, γ)
- S: state space
- A: action space
- P(s'|s,a): transition probabilities
- R(s,a): reward function
- γ: discount factor

**State-space model (control):**
- x_{k+1} = f(x_k, u_k, w_k) (dynamics, possibly with noise w)
- y_k = g(x_k, v_k) (observation, possibly with noise v)
- J = Σ c(x_k, u_k) (cost to minimize)

The MDP is a **stochastic generalization** of the state-space model. The deterministic state-space equation x_{k+1} = Ax_k + Bu_k is a special case of the MDP transition kernel P(s'|s,a) where the distribution is a Dirac delta at Ax + Bu.

Conversely, every finite MDP can be written as a controlled stochastic difference equation with appropriate noise.

The partial observability extension (POMDP) maps to the output-feedback control problem where x is not directly observed and must be estimated (via Kalman filter in the linear case, or belief-state MDP in the general case).

---

## 2. Where the Parallels Break Down

Despite the deep structural equivalence, the two fields diverge in important ways. Understanding *where* they break down is as important as understanding where they agree.

### 2.1 Known vs. Unknown Dynamics

**Control theory** traditionally assumes the dynamics f(x,u) are known (or at least their structure is known, with uncertain parameters). Design proceeds analytically: given the model, compute the optimal controller.

**RL** assumes the dynamics are unknown. The agent must learn about the environment through interaction. This is both RL's great strength (it can handle unknown systems) and its weakness (it requires enormous amounts of data and provides few guarantees during learning).

**The gap narrows:** Adaptive control and system identification have long addressed unknown dynamics in control theory, but with stronger structural assumptions (e.g., linearity, known order). Data-driven control (Willems' fundamental lemma, De Persis & Tesi, 2020) and model-based RL increasingly occupy the same methodological space.

### 2.2 Stability vs. Optimality

**Control theory** prioritizes **stability** — the system must not diverge, oscillate unboundedly, or crash. The first question a control engineer asks is "is it stable?" Optimality is secondary; a stable suboptimal controller is infinitely preferable to an optimal but unstable one.

**RL** prioritizes **optimality** — finding the policy that maximizes cumulative reward. Stability is not even a concept in the standard MDP formulation. An RL agent can learn a policy that performs well on average but has catastrophic failure modes.

This is perhaps the most consequential difference for agent design. RL agents deployed in the real world need stability guarantees that the standard RL framework does not provide.

### 2.3 Formal Guarantees

**Control theory** offers:
- Lyapunov stability proofs (the system will converge)
- Robust stability margins (how much uncertainty can the system tolerate before becoming unstable)
- Gain and phase margins (frequency-domain robustness measures)
- Small-gain theorems, passivity theorems
- H∞ robustness bounds

**RL** offers:
- Asymptotic convergence of Q-learning (under strong assumptions: tabular, infinite visits to all state-action pairs)
- PAC-learning bounds (sample complexity for near-optimal policies)
- Regret bounds (how much worse than optimal during learning)

RL's guarantees are statistical and asymptotic. Control theory's guarantees are deterministic and finite-time. For safety-critical systems, this difference matters enormously.

### 2.4 Continuous vs. Discrete (Historical)

Control theory developed in the continuous-time domain (ODEs, PDEs, Laplace transforms, frequency response). RL developed in the discrete-time, discrete-state domain (MDPs, tabular methods).

This is largely a historical artifact. Modern control handles discrete systems (digital control, sampled-data systems), and modern RL handles continuous state/action spaces (deep RL, continuous control). But the cultural and mathematical traditions still differ. Control engineers think in transfer functions and Bode plots; RL researchers think in episodes and reward curves.

### 2.5 Function Approximation

Control theory's analytical solutions (Riccati equations, pole placement) work exactly for linear systems and provide local guarantees for nonlinear systems (via linearization). When function approximation is needed, control theory uses well-understood basis functions (polynomials, wavelets) with known approximation properties.

RL relies heavily on neural network function approximation, which provides powerful representation but introduces convergence instabilities (the "deadly triad" of function approximation, bootstrapping, and off-policy learning — Sutton & Barto, Ch. 11). Deep RL can diverge, oscillate, or converge to poor solutions with no warning.

---

## 3. Adaptive Dynamic Programming (ADP): The Formal Bridge

ADP is the most explicit attempt to unify control theory and RL. It goes by several names: adaptive/approximate dynamic programming, neuro-dynamic programming (Bertsekas & Tsitsiklis, 1996), and reinforcement learning for control.

### 3.1 Core Idea

ADP applies RL algorithms (value iteration, policy iteration, actor-critic methods) to solve optimal control problems for dynamical systems, particularly when the dynamics are partially or fully unknown.

The key equation is the Bellman equation applied to a continuous-time or discrete-time dynamical system:

```
V*(x) = min_u [ c(x,u) + γ V*(f(x,u)) ]    (discrete-time)
0 = min_u [ c(x,u) + (∇V*)^T f(x,u) ]       (continuous-time, infinite horizon)
```

ADP approximates V* using parametric function approximators (neural networks, polynomials) and iteratively improves the approximation using data from the system.

### 3.2 Actor-Critic Architecture in ADP

Lewis, Vrabie & Vamvoudakis (2012) showed how the actor-critic architecture from RL maps naturally to control design:

- **Critic** (value function approximator) ↔ solves the Bellman/HJB equation ↔ evaluates the cost-to-go
- **Actor** (policy approximator) ↔ implements the control law ↔ computes u = μ(x)

The critic learns V(x) ≈ V*(x); the actor learns μ(x) ≈ μ*(x). They train alternately:
1. **Policy evaluation** (critic update): given current policy μ, solve for V^μ
2. **Policy improvement** (actor update): given current V, compute improved μ

This is exactly policy iteration from RL, but applied to continuous dynamical systems with convergence analysis using control-theoretic tools.

### 3.3 What ADP Adds Beyond Standard RL

- **Stability analysis** during learning (not just at convergence)
- **Continuous-time formulations** that avoid discretization artifacts
- **Online learning** with convergence guarantees for the closed-loop system
- **Handling of continuous state/action spaces** without the ad-hoc discretization common in early RL

### 3.4 The Game-Algebraic Riccati Equation (GARE)

For linear systems with quadratic costs (the LQR case), ADP reduces to solving the GARE. Lewis et al. (2012) showed that online RL methods can solve the GARE without knowing the system matrices A and B — only requiring input-output data. This is a striking result: optimal control without a model, with convergence guarantees.

### 3.5 Key ADP References

- **Lewis, Vrabie & Vamvoudakis (2012).** "Reinforcement Learning and Feedback Control." *IEEE Control Systems*, 32(6), 76-105. The foundational bridge paper.
- **Bertsekas (2019).** *Reinforcement Learning and Optimal Control.* Athena Scientific. The definitive textbook treatment.
- **Wang, Gao, Liu, Li & Lewis (2024).** "Recent Progress in RL and ADP for Advanced Control Applications." *IEEE/CAA J. Automatica Sinica*, 11(1). State-of-the-art survey.
- **Liu et al. (2021).** "ADP for Control: A Survey." *IEEE Trans. SMC: Systems*, 51(1). Comprehensive overview.

---

## 4. Stability Analysis in RL: Why It Is Hard

### 4.1 The Problem

In standard RL, there is no concept of "stability." The MDP framework assumes:
- The environment is stationary (transition probabilities don't change)
- The state space is finite or well-behaved
- The objective is purely about maximizing cumulative reward

None of these assumptions guarantee that the learned policy will keep the system in a safe region of state space, avoid oscillations, or converge to a steady state. A policy can be "optimal" in the RL sense while being catastrophically unstable in the control-theoretic sense.

### 4.2 Why Standard RL Lacks Stability

1. **No notion of equilibrium.** RL does not require or identify equilibrium points. Control theory is built around them.
2. **Reward shaping is fragile.** You can encode stability preferences in the reward function, but there is no guarantee the learned policy will satisfy them.
3. **Function approximation breaks Bellman convergence.** The "deadly triad" means that even if the optimal policy is stable, the learning process may not converge to it.
4. **Exploration can be destabilizing.** RL requires exploration, which by definition means trying untested actions. In physical systems, exploration can damage equipment or violate safety constraints.
5. **No worst-case analysis.** RL optimizes expected performance, not worst-case. A policy that works well 99% of the time may catastrophically fail 1% of the time.

### 4.3 Recent Progress

**Lyapunov-based safe RL (Chow et al., 2018; Berkenkamp et al., 2017):** Construct Lyapunov functions alongside the policy to guarantee stability. Formulate safety as a constraint in a constrained MDP (CMDP). The Lyapunov function provides a certificate that the system state will remain in a safe set.

**Control Lyapunov-Barrier Functions (Wang, 2024; Du et al., 2023):** Combine Lyapunov functions (for stability) with barrier functions (for constraint satisfaction) to simultaneously ensure stable and safe RL policies.

**Stability-Certified RL (Chang, Roohi & Gao, 2019):** Use input-output gradient analysis of neural network policies to formulate stability certification as a semidefinite programming (SDP) feasibility problem. Can certify a large set of stabilizing controllers by exploiting problem structure.

**Generalized Lyapunov Functions (NeurIPS 2025):** Replace the strict stepwise decrease condition with a multi-step weighted decrease criterion. This relaxation makes certification feasible for a broader class of learned policies, including those from PPO and SAC.

**Critic as Lyapunov Function (CALF) (Osinenko et al., CDC 2024):** Use the critic network itself as a Lyapunov function, providing model-free stability guarantees directly from the value function approximation.

**Off-Policy Lyapunov Stability (Gill, 2025):** Learn Lyapunov functions off-policy (rather than on-policy), dramatically improving sample efficiency for stability certification.

### 4.4 Remaining Challenges

- Lyapunov function construction for high-dimensional nonlinear systems is NP-hard in general
- Certified regions of attraction are often small, not covering the full operating range
- Neural network Lyapunov functions are hard to verify formally (requires solving optimization over the NN)
- Transfer of stability guarantees across environments remains unsolved

---

## 5. Lyapunov Stability and RL

### 5.1 What Lyapunov Stability Is

A Lyapunov function V(x) for a dynamical system x_{k+1} = f(x_k) at equilibrium x* = 0 satisfies:
1. V(0) = 0
2. V(x) > 0 for all x ≠ 0
3. V(f(x)) - V(x) < 0 for all x ≠ 0 (the value decreases along trajectories)

If such a V exists, the equilibrium is asymptotically stable. V acts as a "generalized energy" that provably decreases over time.

### 5.2 Connection to Value Functions

The value function in RL, V^π(s), shares structural properties with Lyapunov functions:
- Both assign scalar values to states
- Both encode long-term behavior from a given state
- For a well-designed reward function, the negative value function -V^π can serve as a Lyapunov candidate

**Key insight (Perkins & Barto, 2002):** If the reward function is designed as r(s,a) = -c(s) where c(s) > 0 for s ≠ s* and c(s*) = 0, then the optimal value function V*(s) is a Lyapunov function for the closed-loop system under the optimal policy.

This is not automatic — it requires careful reward design and assumes the optimal policy is actually found. But it establishes a formal link: **the optimal value function can serve as a stability certificate**.

### 5.3 Using Lyapunov Functions to Constrain RL

The most practical approach: learn a Lyapunov function alongside the policy and enforce the Lyapunov decrease condition as a constraint during training.

**Constrained policy optimization:**
```
max_π  E[Σ γ^t r(s_t, a_t)]
s.t.   V_L(f(x, π(x))) - V_L(x) ≤ -α||x||^2  for all x in safe set
```

where V_L is a learned Lyapunov function (parameterized, e.g., by a neural network).

**Berkenkamp et al. (2017)** used Gaussian process models of the dynamics + Lyapunov verification to safely expand the region of attraction during learning. The key idea: only explore states where stability can be verified, gradually expanding the safe set as the model improves.

### 5.4 The Youla-Kucera Parameterization Approach

An alternative: parameterize the space of all stabilizing controllers using the Youla-Kucera parameterization from robust control, then optimize within this space using RL. This guarantees stability by construction — every policy in the search space is stabilizing. The RL algorithm then optimizes performance within this safe set.

---

## 6. LQR as a Special Case of RL: The Formal Reduction

The Linear Quadratic Regulator is the simplest nontrivial problem that both control theory and RL can address. It serves as the Rosetta Stone between the two fields.

### 6.1 The LQR Problem

**Dynamics:** x_{k+1} = Ax_k + Bu_k (linear)
**Cost:** J = Σ_{k=0}^{∞} (x_k^T Q x_k + u_k^T R u_k) (quadratic, Q ≥ 0, R > 0)
**Objective:** Find u_k = Kx_k (linear state feedback) minimizing J

### 6.2 LQR as an MDP

- **State space S:** ℝ^n (continuous)
- **Action space A:** ℝ^m (continuous)
- **Transition:** P(s'|s,a) = δ(s' - As - Ba) (deterministic, linear)
- **Reward:** r(s,a) = -(s^T Q s + a^T R a) (negative quadratic cost)
- **Discount:** γ = 1 for undiscounted; γ < 1 for discounted variant
- **Optimal policy:** π*(s) = Ks where K = -(R + B^T P B)^{-1} B^T P A and P solves the discrete algebraic Riccati equation (DARE)

### 6.3 What Happens to RL Algorithms on LQR

**Value iteration:** The Bellman backup V_{k+1}(x) = min_u [x^T Q x + u^T R u + V_k(Ax + Bu)] preserves quadratic structure. If V_k(x) = x^T P_k x, then V_{k+1}(x) = x^T P_{k+1} x where P_{k+1} solves a Riccati recursion. Value iteration converges to the solution of the DARE. This is a well-known result in control theory.

**Policy iteration:** Starting from any stabilizing K_0, alternating policy evaluation (solving a Lyapunov equation for P) and policy improvement (computing K from P) converges to the optimal K* in finitely many steps. This is Hewer's algorithm (1971), predating RL by decades.

**Q-learning (model-free):** The Q-function Q(x,u) = [x; u]^T H [x; u] is also quadratic. H can be estimated from data without knowing A or B. This is the Bradtke-Ydstie (1994) result — the first model-free LQR solution.

**Policy gradient:** The cost J(K) = E[x_0^T P_K x_0] as a function of K is non-convex but satisfies a gradient domination / Polyak-Lojasiewicz condition, ensuring gradient descent converges to the global optimum despite non-convexity (Fazel et al., 2018). This is a remarkable result that explains why policy gradient works well in practice.

### 6.4 Sample Complexity of LQR (Recht, 2019)

Recht's key contribution was analyzing LQR from an RL perspective: how many samples do you need to learn a near-optimal controller? Results show:
- Model-based approaches (system identification + certainty equivalence) achieve ε-suboptimality with O(1/ε) samples
- Model-free policy gradient requires O(1/ε^2) samples
- The gap quantifies the "cost of not having a model"

This case study demonstrates that for LQR at least, model-based methods dominate — a finding that generalizes to more complex settings, challenging the model-free RL paradigm.

### 6.5 Why LQR Matters as a Bridge

LQR is the one problem where:
1. The optimal solution is known in closed form (DARE)
2. RL algorithms provably converge to it
3. Stability is guaranteed (the optimal LQR gain always stabilizes the system if (A,B) is stabilizable)
4. Sample complexity can be precisely characterized
5. The gap between model-based and model-free approaches can be quantified

It is the benchmark against which any claim about RL-for-control must be measured.

---

## 7. What Control Theory Offers RL

### 7.1 Stability Guarantees

Control theory's Lyapunov analysis, small-gain theorems, and passivity theory provide tools to certify that a system will not diverge. RL has nothing comparable. For any RL agent deployed in a physical system, control-theoretic stability analysis should be the minimum standard.

### 7.2 Robustness Analysis

Control theory quantifies how much perturbation a system can tolerate:
- **Gain margin:** How much the loop gain can change before instability
- **Phase margin:** How much delay/phase shift is tolerable
- **H∞ norm:** Worst-case amplification of disturbances
- **Structured singular value (μ):** Robustness to structured uncertainty

RL has no equivalent. An RL policy that works perfectly in simulation may fail catastrophically with a slight change in dynamics. Robust control provides mathematical tools to quantify and guarantee robustness.

### 7.3 Frequency-Domain Analysis

Bode plots, Nyquist plots, and frequency response methods give intuitive visual tools for understanding system behavior. They reveal resonances, bandwidth limitations, and noise sensitivity. These have no RL counterpart. For continuous control systems, frequency-domain analysis remains indispensable.

### 7.4 Systematic Design Procedures

Control theory offers principled design procedures:
- Pole placement (place eigenvalues where desired)
- Loop shaping (shape the frequency response)
- LQR/LQG (optimize a quadratic cost)
- H∞ synthesis (optimize worst-case performance)
- Model predictive control (solve finite-horizon optimization online)

These are computationally efficient, well-understood, and provide guarantees. RL's design procedure is: define reward, train agent, hope it works.

### 7.5 Separation Principles and Certainty Equivalence

For linear-Gaussian systems, control theory's separation principle says: estimate the state optimally (Kalman filter), then control as if the estimate were the true state (certainty equivalence). The estimation and control problems decouple.

RL has no general separation principle. Partially observed environments (POMDPs) are fundamentally harder than fully observed ones, and there is no general decomposition.

---

## 8. What RL Offers Control Theory

### 8.1 Learning from Data with Unknown Dynamics

RL's core strength: it can find good policies without knowing the system dynamics. This addresses the fundamental limitation of model-based control — you need an accurate model. For complex systems (biological, social, high-dimensional physical), accurate models may be unavailable. RL can learn directly from interaction.

### 8.2 Handling High-Dimensional, Nonlinear Systems

Control theory's analytical tools (Riccati equations, root locus, Bode plots) work best for low-dimensional linear systems. For high-dimensional nonlinear systems (robotic manipulation with vision, autonomous driving), control theory must resort to linearization, gain scheduling, or model predictive control — all of which have limitations.

Deep RL can handle these systems end-to-end, learning directly from high-dimensional sensory input. The representation power of neural networks allows RL to scale where classical control cannot.

### 8.3 Discrete Decision-Making

Control theory was designed for continuous systems — flows, temperatures, velocities. RL naturally handles discrete decisions — which route to take, which action to select from a finite set, how to allocate resources.

MDPs with discrete state and action spaces have no natural control-theoretic formulation. This is RL's native domain.

### 8.4 Multi-Agent and Game-Theoretic Settings

Multi-agent RL (MARL) addresses problems with multiple interacting agents — competitive, cooperative, or mixed. While control theory has results for decentralized control and differential games, RL's framework is more flexible and scales to larger numbers of agents.

### 8.5 Reward Specification Rather Than Model Specification

In RL, you specify *what* you want (the reward function) rather than *how* to achieve it (the control law). This is a more natural interface for complex tasks where the desired behavior is easier to specify than the control strategy.

### 8.6 Exploration and Self-Improvement

RL agents actively explore their environment and improve over time. Classical controllers are designed once and deployed. Adaptive control exists but is more limited in scope. RL's ability to continuously learn and improve is a fundamental advantage in non-stationary environments.

---

## 9. Implications for Agent Design

### 9.1 The Case for Control-Theoretic Stability in Modern Agents

Modern AI agents (LLM-based, RL-based, or hybrid) are increasingly deployed in feedback loops with real-world consequences. The control theory perspective suggests these agents should be analyzed as feedback systems, with stability and robustness as primary design criteria.

**Argument:** An agent that maximizes expected reward but can become unstable (oscillating, diverging, or exhibiting erratic behavior) under perturbation is fundamentally unreliable. Control theory offers mathematical tools to analyze and prevent such behavior.

### 9.2 Specific Recommendations

1. **Lyapunov analysis of agent behavior.** Define a Lyapunov-like function over the agent's state space. Verify that the agent's policy satisfies decrease conditions. This provides a stability certificate.

2. **Robustness margins for learned policies.** After training an RL policy, analyze its robustness to model uncertainty using H∞ or μ-analysis. Quantify how much the environment can change before the policy fails.

3. **Youla parameterization for safe exploration.** Constrain the RL search space to stabilizing controllers using Youla-Kucera parameterization. This guarantees stability by construction.

4. **Model predictive control + RL.** Use MPC's finite-horizon optimization (with stability constraints) as the planning backbone, and RL to learn the terminal cost or improve the model. This combines MPC's guarantees with RL's adaptability.

5. **Constrained MDPs for safety.** Formulate safety requirements as constraints in a CMDP, using Lyapunov or barrier functions to enforce them during training and deployment.

### 9.3 The Convergence Thesis

The fields are converging. Recent work shows this clearly:

- **Data-driven control** (Willems' fundamental lemma, behavioral systems theory) uses data directly for control design, overlapping with model-free RL
- **Safe RL** incorporates control-theoretic constraints (Lyapunov, barrier functions)
- **Model-based RL** is essentially system identification + optimal control
- **ADP** is explicitly the bridge, using RL algorithms to solve control problems

The question is no longer "control theory or RL?" but "how do we combine their strengths?" Control theory provides the safety and stability backbone; RL provides the learning and adaptability.

### 9.4 Open Questions

1. **Can we get the best of both worlds?** Stability guarantees of control theory + learning capability of RL, without sacrificing either?
2. **Scalability of stability analysis.** Lyapunov analysis for high-dimensional neural network policies is computationally intractable. Can we find scalable alternatives?
3. **Non-stationary environments.** Control theory's robust stability assumes bounded uncertainty. What if the environment changes fundamentally? Neither field handles this well.
4. **Multi-agent stability.** Guaranteeing stability of interacting RL agents is largely unsolved.
5. **Formal verification of learned controllers.** Can we formally verify that a neural network policy satisfies stability and safety specifications? Active research area, currently limited to small networks.

---

## 10. Key References

### Foundational Bridge Papers
- Lewis, Vrabie & Vamvoudakis (2012). "Reinforcement Learning and Feedback Control." *IEEE Control Systems*, 32(6), 76-105.
- Recht (2019). "A Tour of Reinforcement Learning: The View from Continuous Control." *Annual Review of Control, Robotics, and Autonomous Systems*, 2, 253-279.
- Bertsekas (2019). *Reinforcement Learning and Optimal Control.* Athena Scientific.
- Sutton & Barto (2018). *Reinforcement Learning: An Introduction.* 2nd ed. MIT Press. (Ch. 1: historical connections to optimal control.)

### Stability and Safety
- Berkenkamp, Turchetta, Schoellig & Krause (2017). "Safe Model-based Reinforcement Learning with Stability Guarantees." *NeurIPS*.
- Chow, Nachum, Duenez-Guzman & Ghavamzadeh (2018). "A Lyapunov-based Approach to Safe Reinforcement Learning." *NeurIPS*.
- Chang, Roohi & Gao (2019). "Stability-Certified Reinforcement Learning: A Control-Theoretic Perspective." arXiv:1810.11505.
- Wang (2024). "Control Lyapunov-Barrier Function-Based Safe RL for Nonlinear Optimal Control." *AIChE Journal*.
- Kushwaha & Biron (2025). "A Review on Safe RL Using Lyapunov and Barrier Functions." *IEEE Access*.

### LQR and RL
- Bradtke & Ydstie (1994). "Adaptive linear quadratic control using policy iteration." *CDC*.
- Fazel, Ge, Kakade & Mesbahi (2018). "Global Convergence of Policy Gradient Methods for the Linear Quadratic Regulator." *ICML*.
- Dean, Mania, Matni, Recht & Tu (2020). "On the Sample Complexity of the Linear Quadratic Regulator." *Foundations of Computational Mathematics*.

### ADP Surveys
- Wang, Gao, Liu, Li & Lewis (2024). "Recent Progress in RL and ADP for Advanced Control Applications." *IEEE/CAA J. Automatica Sinica*.
- Wang et al. (2026). "Control Oriented Reinforcement Learning: A Survey." *Int. J. Robust and Nonlinear Control*.

### Textbooks
- Bertsekas & Tsitsiklis (1996). *Neuro-Dynamic Programming.* Athena Scientific.
- Lewis, Vrabie & Syrmos (2012). *Optimal Control.* 3rd ed. Wiley.
- Bertsekas (2012). *Dynamic Programming and Optimal Control.* Vols. I & II. Athena Scientific.

---

## Summary Table: The Bridge at a Glance

| Aspect | Control Theory | RL | Bridge/Unification |
|---|---|---|---|
| Core equation | HJB PDE | Bellman equation | HJB is continuous-time limit of Bellman |
| Framework | State-space, transfer functions | MDP | MDP generalizes state-space to stochastic case |
| Objective | Minimize cost, ensure stability | Maximize reward | r = -c; stability as constraint in CMDP |
| Model | Assumed known | Learned from data | ADP, data-driven control |
| Guarantees | Stability, robustness (deterministic) | Convergence, regret (statistical) | Lyapunov-constrained RL |
| Benchmark | LQR | Atari, MuJoCo | LQR as RL problem; MuJoCo as control problem |
| Key tool | Lyapunov functions | Value functions | Value function as Lyapunov candidate |
| Design | Analytical (Riccati, pole placement) | Learning (gradient descent, TD) | Actor-critic ADP |
