# Karl Friston's Free Energy Principle and Active Inference

## Scholarly Research Notes

**Date:** 2026-03-12
**Focus:** Mathematical formulation, cybernetic connections, agent design implications

---

## 1. Mathematical Formulation of the Free Energy Principle

### 1.1 Core Definition

The Free Energy Principle (FEP) states that any self-organizing system that is at
equilibrium with its environment must minimize its variational free energy.

Variational free energy is defined as:

```
F = E_q[ln q(s) - ln p(o, s)]
```

Where:
- `q(s)` is the **recognition density** (approximate posterior) over hidden states `s`
- `p(o, s)` is the **generative model** — the joint probability of observations `o` and hidden states `s`
- `E_q[.]` denotes expectation under the recognition density `q`

### 1.2 Decomposition: Energy Minus Entropy

This decomposes into two terms:

```
F = E_q[-ln p(o, s)] - H[q(s)]
     ^^^^^^^^^^^^^^^^   ^^^^^^^^^
     Expected energy     Entropy of q
```

This mirrors the Helmholtz free energy from thermodynamics: `F = U - TS`.

- **Expected energy** = how surprised the agent is about joint occurrences of
  sensations and their inferred causes
- **Entropy** = uncertainty in the agent's own beliefs

### 1.3 Decomposition: Surprise + KL Divergence

Equivalently:

```
F = -ln p(o) + D_KL[q(s) || p(s|o)]
    ^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^
    Surprise   KL divergence (approx error)
```

Since `D_KL >= 0`, free energy is always an **upper bound on surprise**:

```
F >= -ln p(o)
```

This is the critical insight: minimizing `F` with respect to `q` (internal states)
makes `q(s)` approximate the true posterior `p(s|o)` — i.e., it performs approximate
Bayesian inference. Since `D_KL` can never be negative, `F` is a tractable bound on
the intractable surprise `-ln p(o)`.

### 1.4 What This Means

An agent that minimizes variational free energy is doing two things simultaneously:

1. **Making its beliefs accurate** (minimizing the KL divergence between approximate
   and true posterior) — this is perception/inference
2. **Minimizing surprise** (maximizing model evidence `p(o)`) — this is self-evidencing

The key claim: biological systems that persist must have low average surprise
(otherwise they'd visit states incompatible with survival). Therefore they must,
on average, minimize free energy.

### 1.5 Key Papers

- Friston, K. (2010). "The free-energy principle: a unified brain theory?"
  *Nature Reviews Neuroscience*, 11, 127-138.
  - The landmark review establishing FEP as a unifying framework.
  - Available: https://www.nature.com/articles/nrn2787

- Friston, K. et al. (2023). "The free energy principle made simpler but not too
  simple." *Physics Reports*, 1024, 1-29.
  - Starts from Langevin equation, derives Bayesian mechanics as "physics of sentience."
  - Three key steps: (i) partition states via conditional independencies from sparse
    coupling, (ii) unpack implications as Bayesian inference, (iii) describe paths via
    variational principle of least action.
  - Available: https://arxiv.org/abs/2201.06387

---

## 2. Connection to Cybernetics: FEP as Formalization of Homeostasis

### 2.1 Ashby's Homeostasis

W. Ross Ashby established that living systems preserve themselves by keeping
**essential variables** within a narrow range. Walter Cannon coined "homeostasis"
for the constancy of physiological variables. Ashby formalized this: a system is
**ultrastable** if it can reconfigure itself to maintain essential variables within
viability bounds despite environmental perturbation.

### 2.2 FEP as Mathematical Homeostasis

FEP formalizes homeostasis as follows: if a system persists, it must occupy a
limited set of states (its characteristic states). This means it has low entropy
over its state space. Low entropy = low average surprise. Therefore, the system
must (on average) minimize surprise — and the tractable way to do this is to
minimize variational free energy.

The connection:
- **Essential variables** (Ashby) = **characteristic states** (Friston)
- **Homeostasis** = **minimizing surprise** = staying in expected states
- **Ultrastability** = **active inference** = acting to maintain expected states

### 2.3 The Good Regulator Theorem

Conant and Ashby (1970): "Every good regulator of a system must be a model of
that system."

FEP makes this precise: minimizing surprise = maximizing model evidence `p(o)`.
An agent that maximizes its model evidence literally *becomes a model of its
environment*. The agent's internal states come to mirror (in a statistical sense)
the structure of external states that it must regulate.

Friston's formulation: "The agent becomes a model of the environment in which it
is immersed. This is exactly consistent with the Good Regulator theorem."

This is the deep link: FEP says agents must embody generative models of their
environment, and the Good Regulator Theorem says optimal regulators must be models
of what they regulate. These are formally the same claim.

### 2.4 Requisite Variety

Ashby's Law of Requisite Variety: a controller must have at least as much variety
(state repertoire) as the system it controls. Under FEP, this maps to the
expressiveness of the generative model — it must be rich enough to account for the
relevant structure of the environment. A model that is too simple will have
persistently high free energy (high surprise), leading to dissolution.

---

## 3. Active Inference: Unifying Action and Perception

### 3.1 The Core Idea

Active inference says that both action and perception serve the same objective:
minimizing variational free energy.

Two routes to minimize free energy:
1. **Change internal states** (perception): update `q(s)` to better approximate
   `p(s|o)` — i.e., revise beliefs to match sensory evidence.
2. **Change sensory input** (action): act on the world to make observations
   conform to predictions — i.e., make the world match your model.

This is the radical claim: action is not about maximizing reward. Action is about
making the world conform to the agent's generative model. Goals and preferences
are encoded as **prior beliefs** about expected observations.

### 3.2 Formal Statement

Under active inference, the agent selects actions `a` to minimize free energy:

```
a* = argmin_a F(o, q) = argmin_a E_q[ln q(s) - ln p(o(a), s)]
```

Where `o(a)` denotes observations that depend on action. The agent acts to
sample observations that it expects — those with high probability under its
generative model.

### 3.3 Perception-Action Loop

The perception-action loop under active inference:

1. **Observe** sensory data `o`
2. **Infer** hidden states: update `q(s)` to minimize `F` w.r.t. internal states
   (this is perception / state estimation)
3. **Act**: select actions to minimize expected free energy going forward
   (this is planning / decision-making)
4. **Learn**: update model parameters to reduce long-term free energy
   (this is learning / model updating)

All four processes are different aspects of the same objective.

### 3.4 Key Paper

- Da Costa, L. et al. (2020). "Active inference on discrete state-spaces: A
  synthesis." *Journal of Mathematical Psychology*, 99, 102447.
  - Complete mathematical synthesis of active inference on discrete state-space
    (POMDP) models.
  - Derives neuronal dynamics from first principles.
  - Available: https://arxiv.org/abs/2001.07203

---

## 4. Epistemic Value and Curiosity

### 4.1 The Exploration Problem

A central problem in agent design: how to balance exploitation (pursuing known
rewards) with exploration (gathering information about uncertain aspects of the
environment). In standard RL, exploration is typically bolted on (epsilon-greedy,
UCB, intrinsic motivation as separate reward signal). Active inference claims
exploration arises *naturally* from the objective function.

### 4.2 Information Gain as Epistemic Value

When an agent evaluates a policy, the expected free energy decomposes into terms
that include **epistemic value** — the expected information gain about hidden
states. An action with high epistemic value is one where the agent expects to
learn a lot (reduce uncertainty about hidden states by observing outcomes).

Formally, epistemic value = mutual information between expected observations and
hidden states under a given policy:

```
Epistemic value = I(o_τ; s_τ | π) = E_q[D_KL[q(s_τ|o_τ, π) || q(s_τ|π)]]
```

This is the expected Bayesian update — how much the agent expects its beliefs to
change after making an observation. High epistemic value = large expected belief
update = informative action.

### 4.3 Curiosity Without Add-Ons

The crucial difference from RL: epistemic value is not an ad-hoc intrinsic reward
signal. It falls out of the mathematics of expected free energy minimization
directly. Active inference agents are *inherently* curious — they seek out
observations that resolve uncertainty about hidden states, because doing so
reduces expected free energy.

### 4.4 Caveat

Millidge et al. showed that in linear Gaussian systems, the epistemic terms become
constant and do not drive purposeful exploration. The exploration bonus is
meaningful mainly in discrete/nonlinear settings where observations can
disambiguate between qualitatively different hypotheses.

---

## 5. Expected Free Energy for Planning

### 5.1 Definition

The Expected Free Energy (EFE) for a policy `π` at future time `τ` is:

```
G(π, τ) = E_q(o_τ, s_τ | π)[ln q(s_τ | π) - ln p(o_τ, s_τ)]
```

This is structurally similar to variational free energy, but evaluated for
*future* (expected) observations rather than current observations.

### 5.2 Decomposition: Risk + Ambiguity

```
G(π, τ) = D_KL[q(o_τ|π) || p(o_τ)]  +  E_q(s_τ|π)[H[p(o_τ|s_τ)]]
           ^^^^^^^^^^^^^^^^^^^^^^^       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
           Risk                          Ambiguity
```

- **Risk**: divergence between predicted outcomes and preferred outcomes. Policies
  that lead to outcomes far from preferences have high risk.
- **Ambiguity**: expected uncertainty in the observation mapping. Policies that lead
  to states where observations are unreliable have high ambiguity.

### 5.3 Decomposition: Pragmatic + Epistemic Value

Alternatively:

```
G(π, τ) = -E_q(o_τ|π)[ln p(o_τ)]  -  I(o_τ; s_τ | π)
           ^^^^^^^^^^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^^^^^^
           Pragmatic value (neg)      Epistemic value (neg)
```

- **Pragmatic value** (negated): expected log-probability of preferred outcomes.
  Drives exploitation — pursuing outcomes the agent prefers.
- **Epistemic value** (negated): mutual information between future observations and
  hidden states. Drives exploration — seeking informative observations.

Minimizing `G` therefore simultaneously maximizes pragmatic value (exploitation)
and epistemic value (exploration).

### 5.4 Policy Selection

Beliefs about policies are computed via softmax over negative EFE:

```
Q(π) = σ(-G(π)) = exp(-G(π)) / Σ_π' exp(-G(π'))
```

Policies expected to lead to preferred outcomes AND reduce uncertainty are
assigned higher probability.

### 5.5 Generalised Free Energy

Parr & Friston (2019) introduced a unified quantity combining variational and
expected free energy:

```
F_generalised = Σ_{τ≤t} F^π_τ  +  Σ_{τ>t} G^π_τ
                ^^^^^^^^^^^^^^     ^^^^^^^^^^^^^^
                Past/present:      Future:
                variational FE     expected FE
```

This elegantly unifies inference about the past (perception) with inference about
the future (planning) under a single objective.

**Key paper:** Parr, T. & Friston, K. (2019). "Generalised free energy and active
inference." *Biological Cybernetics*, 113, 495-513.
https://link.springer.com/article/10.1007/s00422-019-00805-w

---

## 6. Comparison to Reinforcement Learning

### 6.1 Core Differences

| Dimension | Reinforcement Learning | Active Inference |
|-----------|----------------------|-----------------|
| **Objective** | Maximize cumulative reward | Minimize (expected) free energy |
| **Reward** | External signal from environment | Prior preferences over observations (no separate reward) |
| **Policy** | Mapping from states to actions | Sequence of actions (sequential policy) |
| **Exploration** | Bolted on (epsilon-greedy, UCB, etc.) | Emerges from epistemic value in EFE |
| **Observability** | Typically MDP (fully observable) | Naturally POMDP (partially observable) |
| **Perception** | Separate from decision-making | Unified with action under same objective |
| **Model** | Optional (model-free vs model-based) | Always model-based (generative model required) |

### 6.2 Formal Relationship

Friston et al. (2009) showed that reward can be recast as the log-probability of
preferred observations: `r(o) = ln p(o)`. Under this mapping, maximizing expected
reward becomes equivalent to minimizing expected surprise about preferred outcomes.

Beren Millidge's retrospective (2024) concludes that active inference and RL are
"essentially isomorphic" — both are consequences of mapping decision problems onto
Bayesian inference. The difference is "slightly different assumptions about how
reward is encoded" into probabilistic graphical models. This has "little practical
importance for designing action selection algorithms."

### 6.3 What Active Inference Adds

Despite the formal equivalence, active inference offers:

1. **Principled exploration**: epistemic value arises from the objective, not as
   an add-on. (Though see caveats in Section 4.4.)
2. **Natural POMDP handling**: formulated in belief space from the start.
3. **Unified perception-action**: same objective for state estimation and planning.
4. **Preference vs reward**: encoding goals as priors rather than rewards may be
   more natural for some problems (e.g., homeostatic agents).

### 6.4 What Active Inference Lacks

1. **Scalability**: has not been scaled to high-dimensional problems to the same
   degree as deep RL.
2. **Model-free option**: always requires a generative model, which may be
   impractical in complex environments.
3. **Proven practical advantage**: "relatively little special sauce" over standard
   RL for practical algorithm design (Millidge 2024).

### 6.5 Key Papers

- Friston, K. et al. (2009). "Reinforcement learning or active inference?"
  *PLOS ONE*. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0006421
- Sajid, N. et al. (2019). "Active inference: demystified and compared."
  https://arxiv.org/abs/1909.10863
- Tschantz, A. et al. (2020). "Reinforcement Learning through Active Inference."
  https://arxiv.org/abs/2002.12636
- Millidge, B. (2024). "A Retrospective on Active Inference."
  https://www.beren.io/2024-07-27-A-Retrospective-on-Active-Inference/

---

## 7. The Markov Blanket Formalism

### 7.1 Definition

A Markov blanket defines the boundary of a system in a **statistical** sense. It
partitions the states of a system into four sets:

```
All states = {Internal, Sensory, Active, External}

         External
            |
         [Sensory]      <-- Markov Blanket
            |
         Internal
            |
         [Active]        <-- Markov Blanket
            |
         External
```

- **Internal states** (`μ`): the agent's "brain" / model
- **External states** (`η`): the environment
- **Sensory states** (`s`): inputs from environment to agent (parents of internal)
- **Active states** (`a`): outputs from agent to environment (children of internal)
- **Markov blanket** = {Sensory, Active} states

### 7.2 Conditional Independence

The blanket enforces **conditional independence**: internal states are conditionally
independent of external states given the blanket states (and vice versa). Internal
and external states can only influence each other via sensory and active states.

```
p(μ | η, s, a) = p(μ | s, a)    (internal independent of external given blanket)
p(η | μ, s, a) = p(η | s, a)    (external independent of internal given blanket)
```

### 7.3 Significance for Agents

This provides a principled, formal definition of what constitutes an "agent":
anything with a Markov blanket that minimizes free energy with respect to its
internal and active states. The blanket *defines* the agent-environment boundary
without requiring a physical boundary (like a cell membrane).

The FEP then says: if such a partition exists, the internal states must (on
average) encode a probabilistic model of external states, and the active states
must (on average) minimize expected surprise.

### 7.4 Nested / Hierarchical Blankets

Markov blankets compose hierarchically: cells have blankets, organs have blankets
(composed of cellular blankets), organisms have blankets, social groups have
blankets. This gives a natural account of multi-scale organization.

### 7.5 Critical Issues

**Pearl blankets vs Friston blankets** (Bruineberg et al.):
- **Pearl blankets**: epistemic tool for Bayesian inference (standard in graphical
  models). These are properties of the *model*.
- **Friston blankets**: metaphysical claim about the physical boundary between an
  agent and its environment. These are claimed to be properties of the *territory*.

The critique: Friston's use conflates a statistical tool with an ontological claim
about what constitutes an agent. Just because you can identify conditional
independencies in a dynamical system does not mean those independencies correspond
to meaningful agent-environment boundaries.

**Sparse coupling assumption** (Friston et al. 2023): Markov blankets arise from
sparsely coupled dynamics — most degrees of freedom do not interact directly. A
2025 paper proved that "weak" Markov blankets (conditional independence up to
vanishing interactions) emerge almost surely in the infinite-dimensional limit,
grounding this conjecture.

### 7.6 Key Papers

- Kirchhoff, M. et al. (2018). "The Markov blankets of life." *J. Royal Society
  Interface*. https://royalsocietypublishing.org/doi/10.1098/rsif.2017.0792
- Bruineberg, J. et al. "The Emperor's New Markov Blankets."
  https://philsci-archive.pitt.edu/18467/

---

## 8. Critiques of the Free Energy Principle

### 8.1 The Tautology Critique

**Core claim**: FEP is an unfalsifiable tautology. This is acknowledged by both
critics and proponents (including Friston himself, who calls it "a piece of
mathematical reasoning... no more subject to empirical falsification than calculus").

Steven Byrnes (LessWrong): "Anything you can derive from FEP, you can derive
directly from the same underlying premises without ever mentioning FEP." Since it
applies to everything (including rocks), it has little specific explanatory power
for how brains actually work.

The counter-argument: the FEP is a *principle* (like Hamilton's principle in
physics), not a theory. It constrains what theories are possible. Process theories
(like predictive coding, active inference) are falsifiable — the principle itself
is not.

### 8.2 Too General

Since FEP applies to any system with a Markov blanket (which is effectively
everything), critics argue it says nothing specific. A rock "minimizes free
energy" by reaching thermal equilibrium. This universality may be a feature (it
shows brains are not special) or a bug (it doesn't explain what makes brains
different from rocks).

### 8.3 Ergodicity Assumption

FEP assumes the system is at nonequilibrium steady state (ergodic within its
characteristic states). Critics point out this is at odds with biological
reality — organisms undergo phase transitions (development, metamorphosis, death)
that violate ergodicity. Proponents reply by restricting the formalism to
"well-defined, steady phases," but this risks circularity: FEP works for phases
where FEP works.

### 8.4 The Markov Blanket Problem

Aguilera, Millidge, Tschantz & Buckley (2021) argue:
- No necessary connection between a *statistical* Markov blanket and a *functional*
  boundary (a cell membrane does not imply statistical conditional independence).
- FEP only describes internal states *on average over counterfactual realizations*,
  not individual trajectories.

### 8.5 Practical Criticism (Millidge 2024)

Beren Millidge, after years of working on active inference, concluded:
- Active inference and RL are "essentially isomorphic."
- Scaling requires flexible parametrization (neural networks), at which point
  you're doing standard deep RL with a Bayesian interpretation.
- "Relatively little special sauce" for practical agent design.
- Neuroscientific evidence for the specific mechanisms is "relatively weak."

### 8.6 The Notation Problem

Andrews (2021): "The math is not the territory." FEP's mathematical notation
creates an illusion of precision that may not map onto biological or physical
reality. The formal framework may be internally consistent but disconnected from
empirical phenomena.

### 8.7 Assessment

The critiques broadly fall into two categories:
1. **As a principle**: it is unfalsifiable and too general (tautology critique).
   This is a philosophical rather than scientific objection — many useful
   principles in physics are similarly unfalsifiable.
2. **As a practical framework**: it offers limited advantages over existing methods
   (RL critique). This is an engineering objection — it may be true now but could
   change as the framework develops.

The strongest defense: FEP provides a *language* and *constraint* for thinking
about self-organizing systems, much as the principle of least action provides a
language for physics. Whether this language adds value over alternatives is the
real question.

---

## 9. Active Inference Agents in Practice

### 9.1 Software Implementations

**pymdp** (Python): First open-source library for active inference on discrete
POMDPs. Provides Agent class abstracting state estimation, policy inference, and
action selection. NumPy-based, validated against MATLAB SPM implementation.
- GitHub: https://github.com/infer-actively/pymdp
- Paper: https://arxiv.org/abs/2201.03904

**ActiveInference.jl** (Julia): Inspired by pymdp, similar syntax.

**SPM/DEM** (MATLAB): The gold-standard, Friston's own toolbox in SPM.

### 9.2 VERSES AI / Genius Platform

VERSES AI (Chief Scientist: Karl Friston since 2022) has commercialized active
inference through the **Genius** platform (launched April 2025).

Key developments:
- **Renormalization Generative Models (RGMs)**: "From pixels to planning: scale-free
  active inference" (2024). Hierarchical architecture borrowing renormalization from
  physics. Achieved 99.8% on MNIST subset with 90% less training data.
- Claims to be 5,000x more cost-effective than OpenAI o1 on certain tasks (AXIOM
  model, per researcher Devansh).
- Multi-agent robotics outperforming Meta's Habitat Benchmark without pre-training.
- Named in Gartner's 2025 Hype Cycle for AI (spatial computing, active inference).
- 25+ papers published in Q3 2024 alone. Presented at ICLR 2025, NeurIPS, IWAI.

### 9.3 Robotics Applications

Active inference has been deployed in:
- **Robot navigation**: hierarchical generative model for warehouse navigation using
  camera-only input (Oliver et al., 2021).
- **Bio-inspired navigation (2025)**: ROS2 system building topological maps
  incrementally, no prior training, competitive with SOTA exploration methods.
- **Humanoid control**: iCub robot with adaptive body perception, robust reaching
  and head tracking under high sensor noise.
- **Hierarchical planning**: discrete symbolic planning ("go to kitchen") + continuous
  sensorimotor control (joint velocities).

### 9.4 Performance Assessment

General finding: active inference performs comparably to RL in simple environments,
and *better* in environments with:
- **Volatility** (changing dynamics)
- **Ambiguity** (uncertain observations)
- **Context sensitivity** (changing task demands)
- **Partial observability** (POMDP settings)

But: "AIF has yet to be scaled to tackle high-dimensional problems to the same
extent as established approaches such as deep reinforcement learning."

### 9.5 Key Challenges

1. **Scaling to high dimensions**: generative models become intractable.
2. **Learning generative models from data**: bootstrapping problem.
3. **Long-horizon planning**: EFE computation scales poorly with planning depth.
4. **Delayed rewards/consequences**: performance degrades when action effects are
   not immediately observable.

### 9.6 Key Papers

- Da Costa et al. (2022). "How Active Inference Could Help Revolutionise Robotics."
  *Entropy*. https://www.mdpi.com/1099-4300/24/3/361
- Lanillos et al. (2021). "Active Inference in Robotics and Artificial Agents:
  Survey and Challenges." https://arxiv.org/abs/2112.01871

---

## 10. FEP, Good Regulator Theorem, and Ashby's Homeostasis

### 10.1 The Lineage

```
Cannon (1932): Homeostasis
    |
Ashby (1952): Ultrastability, Requisite Variety
    |
Conant & Ashby (1970): Good Regulator Theorem
    |
Internal Model Principle (1970s-80s): Control Theory formalization
    |
Friston (2005-2010): Free Energy Principle
    |
Active Inference (2010s-present): Process theory for agents
```

### 10.2 The Formal Chain

1. **Homeostasis** (Cannon/Ashby): living systems keep essential variables within
   bounds.

2. **Ultrastability** (Ashby): systems that persist must reconfigure themselves to
   maintain essential variables despite perturbation. This is adaptation.

3. **Good Regulator Theorem** (Conant & Ashby): to regulate effectively, the
   regulator must be a model of the system it regulates. This establishes the
   necessity of internal models.

4. **Requisite Variety** (Ashby): the controller's variety must match the system's
   variety. This establishes the complexity requirements for internal models.

5. **Free Energy Principle** (Friston): formalizes all of the above in a single
   variational objective. Minimizing free energy simultaneously:
   - Maintains the system in expected states (homeostasis)
   - Updates internal states to model external states (Good Regulator)
   - Adjusts the complexity of the model to match environmental demands
     (Requisite Variety)
   - Acts on the environment to maintain expected observations (ultrastability)

### 10.3 What FEP Adds Beyond Classical Cybernetics

1. **Mathematical precision**: cybernetic concepts were largely qualitative or
   limited to linear systems. FEP provides a variational calculus that applies
   to arbitrary nonlinear stochastic systems.

2. **Unification of perception and action**: classical cybernetics treated
   sensing and acting as separate channels in a feedback loop. FEP shows they
   minimize the same objective.

3. **Information-theoretic grounding**: surprise, entropy, and mutual information
   provide rigorous measures of what cybernetics discussed qualitatively.

4. **Hierarchical generative models**: FEP naturally accommodates multi-scale
   models (hierarchical predictive coding), which classical cybernetics could
   not formalize.

5. **Epistemic action**: classical cybernetics had no formal account of
   exploration or information-seeking behavior. FEP derives it from the
   expected free energy.

### 10.4 What FEP Does NOT Add

1. **Practical control algorithms**: classical control theory (PID, LQR, MPC)
   remains more practically useful for engineering.
2. **Falsifiable predictions**: cybernetics at least made specific claims about
   specific systems. FEP is more general and correspondingly less specific.
3. **Simplicity**: Ashby's ideas are immediately intuitive. FEP's mathematical
   apparatus can obscure rather than illuminate.

---

## Summary Assessment for Agent Design

### What FEP/Active Inference Offers for Agent Builders

1. **A principled framework** for agents that must perceive, act, learn, and plan
   under uncertainty — all derived from a single objective.
2. **Natural exploration-exploitation balance** via the epistemic/pragmatic
   decomposition of expected free energy.
3. **POMDP-native**: designed for partial observability from the ground up.
4. **Goal specification as priors**: preferences over observations rather than
   external reward signals. This may be more natural for autonomous agents that
   must define their own objectives.
5. **Hierarchical composition**: Markov blanket nesting gives a formal account
   of multi-agent and multi-scale organization.

### What Remains Problematic

1. **Scaling**: the hard problem. Generative models for complex environments are
   expensive to learn and use for inference.
2. **Formal equivalence to RL**: if the two are isomorphic, why not use the
   better-engineered, better-understood RL framework?
3. **Tautology risk**: the principle itself is unfalsifiable. Its value depends
   entirely on the process theories derived from it.
4. **Practical advantage unclear**: no convincing demonstration that active
   inference *must* be used rather than standard methods.

### The Honest Take

FEP is best understood as a *language* and *constraint* for thinking about agents,
not as an algorithm. It tells you what an optimal agent *must* do (minimize free
energy) but not how to do it efficiently. The practical algorithms (predictive
coding, active inference on POMDPs, deep active inference) are where the value
lies, and these can often be derived without invoking FEP at all.

The most valuable insight for agent design may be the simplest one: an agent that
persists must be a model of its environment (Good Regulator), and it must balance
information-seeking with goal-pursuing (exploration-exploitation). FEP provides a
beautiful mathematical frame for this, but the frame is not the picture.

---

## References

### Primary Sources

1. Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*, 11, 127-138. https://www.nature.com/articles/nrn2787
2. Friston, K. et al. (2023). "The free energy principle made simpler but not too simple." *Physics Reports*, 1024, 1-29. https://arxiv.org/abs/2201.06387
3. Da Costa, L. et al. (2020). "Active inference on discrete state-spaces: A synthesis." *J. Mathematical Psychology*, 99, 102447. https://arxiv.org/abs/2001.07203
4. Parr, T. & Friston, K. (2019). "Generalised free energy and active inference." *Biological Cybernetics*, 113, 495-513. https://link.springer.com/article/10.1007/s00422-019-00805-w
5. Friston, K. et al. (2009). "Reinforcement learning or active inference?" *PLOS ONE*. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0006421
6. Parr, T., Pezzulo, G., & Friston, K.J. (2022). *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior*. MIT Press.

### Critical and Comparative Sources

7. Millidge, B. (2024). "A Retrospective on Active Inference." https://www.beren.io/2024-07-27-A-Retrospective-on-Active-Inference/
8. Byrnes, S. "Why I'm not into the Free Energy Principle." LessWrong. https://www.lesswrong.com/posts/MArdnet7pwgALaeKs/why-i-m-not-into-the-free-energy-principle
9. Andrews, M. (2021). "The math is not the territory." *Biology & Philosophy*. https://link.springer.com/article/10.1007/s10539-021-09807-0
10. Bruineberg, J. et al. "The Emperor's New Markov Blankets." https://philsci-archive.pitt.edu/18467/
11. Sajid, N. et al. (2019). "Active inference: demystified and compared." https://arxiv.org/abs/1909.10863
12. Millidge, B. et al. (2021). "Whence the Expected Free Energy?" *Neural Computation*. https://direct.mit.edu/neco/article/33/2/447/95645/

### Cybernetic Foundations

13. Conant, R.C. & Ashby, W.R. (1970). "Every good regulator of a system must be a model of that system." *Int. J. Systems Science*, 1(2), 89-97.
14. Ashby, W.R. (1952). *Design for a Brain*. Chapman & Hall.
15. Ashby, W.R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.

### Implementation and Applications

16. Heins, C. et al. (2022). "pymdp: A Python library for active inference in discrete state spaces." https://arxiv.org/abs/2201.03904
17. Lanillos, P. et al. (2021). "Active Inference in Robotics and Artificial Agents." https://arxiv.org/abs/2112.01871
18. VERSES AI Research. https://www.verses.ai/active-inference-research
19. Kirchhoff, M. et al. (2018). "The Markov blankets of life." *J. Royal Society Interface*. https://royalsocietypublishing.org/doi/10.1098/rsif.2017.0792
