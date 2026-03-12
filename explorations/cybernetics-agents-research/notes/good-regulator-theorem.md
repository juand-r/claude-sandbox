# The Good Regulator Theorem: Scholarly Notes

**Date:** 2026-03-12
**Primary source:** Conant, R.C. & Ashby, W.R. (1970). "Every Good Regulator of a System Must Be a Model of That System." *International Journal of Systems Science*, 1(2), 89-97 (also cited as pp. 511-519 depending on pagination).

---

## 1. The Original Theorem (Conant & Ashby, 1970)

### 1.1 Setup and Notation

The theorem operates on a simple regulation scenario with five sets and three mappings:

**Sets:**
- **S** — system states (the "reguland," i.e., the thing being regulated)
- **R** — regulator states (actions/outputs of the regulator)
- **Z** — outcome states (what actually happens)
- **D** — disturbances (inputs from the environment)
- **G ⊆ Z** — "good" outcomes (the goal set)

**Mappings:**
- **φ: D → S** — disturbance determines system state
- **ρ: D → R** — disturbance determines regulator state (possibly via the system)
- **ψ: S × R → Z** — system state and regulator state jointly determine the outcome

The regulator is modeled as a conditional probability distribution **P(R|S)** — a stochastic mapping from system states to regulator states.

### 1.2 What "Good" Means

A regulator is "good" in a very specific, dual sense:
1. **Optimal:** It minimizes H(Z), the Shannon entropy of the outcome distribution. The regulator achieves the lowest possible uncertainty in outcomes.
2. **Maximally simple:** Among all optimal regulators, it contains no unnecessary stochasticity or complexity.

This dual criterion is crucial. The theorem does NOT say all optimal regulators are models. It says the *simplest* optimal regulators are.

### 1.3 The Formal Theorem

**Theorem (informal):** Any regulator that is maximally both successful and simple must be isomorphic with the system being regulated.

More precisely, the theorem establishes two things:

**Lemma (optimality step):** If a regulator achieves minimal H(Z), then the outcome Z must be a deterministic function of S. That is, H(Z|S) = 0 — given the system state, the outcome is fully determined.

*Proof sketch:* If Z were not deterministic given S, then for some system state s, multiple outcomes z would occur with nonzero probability. But then the regulator could do better by always picking the action that leads to the most common outcome for that s. Contradiction with optimality.

**Theorem (simplicity step):** Given the lemma, any remaining nondeterminism in P(R|S) is unnecessary complexity. If two different regulator states r₁ and r₂ both have nonzero probability given some state s, and both lead to the same z (which they must, by the lemma), then there is no reason to use more than one. The simplest optimal regulator makes R a deterministic function of S:

> R = h(S) for some function h: S → R

This h is the "model" — a homomorphic mapping from system states to regulator states.

### 1.4 What "Model" Means Here (CRITICAL)

The word "model" in this theorem has a very specific, narrow meaning that is **fundamentally different** from what ML/AI people typically mean by "model":

- **In the theorem:** A "model" is a deterministic mapping h: S → R from system states to regulator actions. It is a homomorphism — the regulator's behavior mirrors the structure of the system in the sense that distinct system states that require distinct actions get mapped to distinct regulator states.
- **NOT what it means:** It does NOT mean a predictive model of the system's dynamics. It does NOT mean an internal representation of how the system evolves over time. It does NOT mean a forward model, a generative model, or a world model in any modern sense.

The "model" here is what reinforcement learning calls a **policy** — a state-to-action mapping. That is all.

As Conant and Ashby put it: the regulator's actions are "the system's actions as seen through a mapping h." The regulator is a model in the sense that its state faithfully tracks relevant distinctions in the system state. Two system states that need different treatment get different regulator states; two that need the same treatment may (but need not) get the same regulator state.

### 1.5 Information-Theoretic Framing

The theorem is fundamentally information-theoretic:

- The objective is to minimize **H(Z)**, the entropy of outcomes.
- Optimality requires **H(Z|S) = 0** — the outcome must be fully determined by the system state.
- Simplicity requires **H(R|S) = 0** — the regulator state must be fully determined by the system state.
- Together: R is a deterministic function of S, and Z is a deterministic function of S.

The regulator cannot reduce entropy beyond what is achievable given its information about the system. This connects to Ashby's earlier **Law of Requisite Variety** (1956): a controller must have at least as much variety (number of distinguishable states) as the disturbances it must counteract.

### 1.6 Proof Assumptions and Limitations

Key assumptions (often unstated or buried in the proof):
1. **Finite state spaces** — S, R, Z are all finite.
2. **Single-step interaction** — The theorem considers a single-step regulation problem, not sequential decision-making.
3. **Full observability** — The regulator has access to the system state S (or at least the disturbance D that determines S).
4. **The goal set G disappears** — Despite being defined in the setup, G plays no role in the actual proof. The theorem is about minimizing entropy of Z, not about achieving particular outcomes.
5. **Causal structure is unspecified** — Conant & Ashby deliberately leave ambiguous whether the regulator observes S directly, observes D, or uses feedback. They claim this generality is a feature; critics argue it makes the theorem vacuous in some interpretations.

### 1.7 What the Theorem Actually Proves (Deflationary Reading)

Stripped of the dramatic phrasing, the theorem proves:

1. An optimal regulator maps distinct-action-requiring states to distinct actions (no confusion).
2. An optimal regulator does not randomize when randomization is unnecessary (no noise).

In other words: **the simplest optimal policy is a deterministic function of the state.** This is... not very surprising. As Erdogan (2021) puts it, the result is "almost trivial."

The grandeur of the theorem comes from the rhetorical packaging, not the mathematical content. The phrase "must be a model of that system" suggests something far deeper than what is proven.

---

## 2. Erdogan's Reinterpretation (2021)

**Source:** Erdogan, G. (2021). "On Conant and Ashby's Good Regulator Theorem." Blog post at gokererdogan.github.io.

### 2.1 The Key Insight

Erdogan makes the crucial observation that the Good Regulator Theorem's setup is equivalent to a **single-step MDP**, and the "model" P(R|S) is what RL calls a **policy**, not a world model.

Setup in RL terms:
- S = states
- R = actions
- Z = next states
- P(R|S) = the policy
- Minimizing H(Z) = minimizing uncertainty in the next state

### 2.2 Why This Matters for AI

The theorem is frequently cited as a deep justification for model-based approaches in AI: "See, even the cyberneticists proved you need a model!" But this is a category error:

- **Model-based RL** uses a model of the environment's dynamics: P(S'|S,A) — how the world evolves given states and actions.
- **The theorem's "model"** is P(R|S) = P(A|S) — a policy.

The theorem says nothing about whether you need a predictive model of the environment. It says you need a good policy. Both model-based and model-free RL aim to produce good policies. The theorem is neutral between them.

### 2.3 What the Theorem Does NOT Prove

- It does NOT prove agents need internal world models.
- It does NOT prove model-based methods are superior to model-free methods.
- It does NOT prove anything about the internal structure of the regulator — only about its input-output behavior.
- It does NOT address multi-step, sequential, or partially observable settings.

### 2.4 Assessment

Erdogan concludes the theorem is "much less significant and much less relevant for AI than commonly imagined." The importance attributed to it comes from equivocating between two meanings of "model" — a mapping (policy) and a predictive representation (world model).

---

## 3. Virgo et al. (2025): A Good Regulator Theorem for Embodied Agents

**Source:** Virgo, N., Biehl, M., Baltieri, M., & Capucci, M. (2025). "A Good Regulator Theorem for Embodied Agents." *Proceedings of ALIFE 2025*, Kyoto, Japan. Also: arXiv:2508.06326.

### 3.1 Motivation

Artificial Life has produced many counterexamples to the naive reading of the Good Regulator Theorem — systems that regulate effectively without any apparent internal model (e.g., Braitenberg vehicles, Brooks's subsumption architecture, passive dynamic walkers). This paper asks: can we reformulate the theorem so it applies to these cases too?

### 3.2 Key Move: From "Being a Model" to "Having Beliefs"

The classical theorem says: a good regulator **is** a model (in the homomorphism sense).
Virgo et al. say: a good regulator **can be interpreted as having beliefs** about its environment.

This is a fundamental shift from an intrinsic structural property to an observer-relative interpretive property.

### 3.3 Formal Framework

They model the agent-environment system as:
- **Agent:** A Moore machine with internal state X, readout function r (producing actions), and update function u (processing sensory input).
- **Environment:** A Mealy machine with state Y and evolution function e.
- **Good set:** G ⊆ X × Y — the set of "acceptable" joint states.
- **Good regulator:** Existence of a nonempty, forward-closed set R ⊆ X × Y ⊆ G such that trajectories starting in R remain in G indefinitely.

### 3.4 The Interpretation Map

The central construction is the **interpretation map** ψ: X → P(Z), which assigns to each agent internal state x a set of environment states that the agent "believes" are possible. This is not something the agent computes — it is something an external observer attributes to the agent.

### 3.5 Main Theorem (Theorem 3.4)

An agent is a good regulator (classical sense) **if and only if** it can be interpreted as a "subjective good regulator" — one where:

1. **Beliefs update consistently:** When the agent receives sensory input and updates its state, the attributed beliefs follow a possibilistic (not probabilistic) version of Bayes' rule.
2. **Beliefs entail goals:** The attributed beliefs ψ(x) satisfy goal constraints in all reachable states.
3. **Starting beliefs are consistent:** Some initial agent state has nonempty attributed beliefs.

### 3.6 The Doorstop Problem

A classic objection: a doorstop is a "good regulator" of the door (it keeps the door open), but it clearly doesn't model anything. Virgo et al. resolve this: you CAN attribute beliefs to the doorstop, but they are trivial — the doorstop's "beliefs" don't depend on its state (it has no state to speak of) and don't update in response to input. The theorem holds, but the resulting "model" is degenerate.

### 3.7 Significance

- The theorem applies to ALL good regulators, not just the "simplest optimal" ones.
- It removes the finite-state and single-step restrictions.
- It uses a possibilistic (set-valued) rather than probabilistic framework.
- It makes the observer's role explicit — models are not intrinsic properties of systems but are attributed by observers taking the "intentional stance" (Dennett).
- **Key limitation:** The theorem tells you that an interpretation EXISTS; it does not tell you whether the agent actually USES that interpretation or whether it is a useful description for prediction.

---

## 4. Richens, Abel, Bellot & Everitt (2025): General Agents Contain World Models

**Source:** Richens, J., Abel, D., Bellot, A., & Everitt, T. (2025). "General Agents Contain World Models." *ICML 2025*. arXiv:2506.01622.

### 4.1 The Question

Do agents capable of flexible, goal-directed behavior necessarily contain world models? Unlike the Good Regulator Theorem (which proves something weaker than it sounds), this paper aims to prove the strong claim directly.

### 4.2 Setup

- **Controlled Markov Process (cMP):** An MDP without reward — tuple (S, A, P) where P_{ss'}(a) = P(S'=s'|A=a, S=s).
- Assumptions: finite, communicating (every state reachable from every other), stationary.
- **Goal-conditioned policy:** An agent that can pursue arbitrary goals (reach arbitrary target states or state distributions).

### 4.3 Main Result (Theorem 1)

Any agent capable of generalizing to multi-step goal-directed tasks **must have learned a predictive model of its environment** — specifically, one that can be extracted from the agent's policy.

Key distinctions from the Good Regulator Theorem:
- This IS about world models (predictive models of dynamics), not just policies.
- It addresses multi-step, sequential decision-making.
- It requires goal generalization — the agent must handle multiple goals, not just one.
- The more goals the agent can handle / the better its performance, the more accurate the extracted world model must be.

### 4.4 Implications

1. Model-free agents that generalize across goals are, in a meaningful sense, model-based — the world model is implicit in the policy.
2. World models can be EXTRACTED from trained policies (algorithmic consequence).
3. Agent capabilities in complex environments can be bounded by the accuracy of extractable world models.

### 4.5 Relationship to Good Regulator Theorem

This paper does what people THOUGHT the Good Regulator Theorem did — it proves that general agents must contain world models (in the predictive sense). The Good Regulator Theorem only proves agents must have good policies. Richens et al. prove the stronger claim, but require stronger assumptions (multi-step, multi-goal, communicating MDP).

### 4.6 Related: Richens & Everitt (2024) — Robust Agents Learn Causal World Models

A companion result: agents that maintain low regret under distributional shifts must have learned **causal** models (not just correlational ones). This extends the world-model-necessity result from goal generalization to domain generalization.

---

## 5. Francis & Wonham (1976): The Internal Model Principle

**Source:** Francis, B.A. & Wonham, W.M. (1976). "The Internal Model Principle of Control Theory." *Automatica*, 12, 457-465.

### 5.1 Context

This is the engineering/control-theory version of the Good Regulator Theorem, formulated rigorously for linear time-invariant (LTI) systems. It is arguably more important than the Good Regulator Theorem itself, with ~1500 citations and deep influence on control engineering.

### 5.2 The Problem

Consider a linear system subject to disturbances and reference signals that are themselves generated by a known dynamical system (the "exosystem"). The controller must:
1. Stabilize the closed loop.
2. Drive the regulation error to zero asymptotically.
3. Maintain these properties under small parameter perturbations ("structural stability").

### 5.3 The Internal Model Principle (Informal)

A structurally stable controller that achieves asymptotic regulation **must contain** a suitably reduplicated copy of the dynamics that generate the disturbance and reference signals.

### 5.4 Formal Content

For a linear system with disturbances generated by an autonomous exosystem with characteristic polynomial p(s), any controller that achieves structurally stable asymptotic regulation must include, in its feedback path, a copy of the dynamics described by p(s). In the frequency domain, the controller's transfer function must include poles that cancel the unstable poles of the disturbance generator.

**Necessity:** If the controller does NOT contain the internal model, then either regulation fails, or it is not robust to parameter perturbations.

**Sufficiency:** If the controller DOES contain the internal model and the closed loop is stable, then asymptotic regulation is achieved.

### 5.5 Key Differences from the Good Regulator Theorem

| Aspect | Good Regulator Theorem | Internal Model Principle |
|--------|----------------------|-------------------------|
| **Domain** | Abstract, finite sets | Linear time-invariant systems |
| **"Model" means** | Deterministic policy (state-to-action map) | Copy of disturbance dynamics |
| **What it proves** | Simplest optimal policy is deterministic | Controller must contain exosystem dynamics |
| **Temporal scope** | Single-step | Continuous-time / infinite horizon |
| **Robustness** | Not addressed | Central requirement (structural stability) |
| **Practical utility** | Limited (too abstract) | High (directly informs controller design) |
| **Proof technique** | Information theory (entropy) | Geometric control theory / frequency domain |

### 5.6 The IMP's "Model" Is Genuinely a Model

Unlike the Good Regulator Theorem, the Internal Model Principle really does require the controller to contain a model — a dynamical subsystem whose behavior reproduces the dynamics of the disturbance. This is a structural requirement on the controller's internal architecture, not merely a statement about its input-output behavior.

If the disturbance is a sinusoid at frequency ω, the controller must contain an oscillator at frequency ω. If the disturbance is a ramp, the controller must contain a double integrator. The controller literally simulates the disturbance-generating process.

### 5.7 Significance

The IMP is a cornerstone of robust control theory. It explains why:
- A proportional controller cannot eliminate steady-state error to a step input (no integrator = no model of step).
- PID control works for step and ramp inputs (the integrator IS the internal model).
- Repetitive control works for periodic disturbances (the internal model contains the period).

---

## 6. Synthesis: How These Results Relate

### 6.1 The Progression of Claims

1. **Good Regulator Theorem (1970):** The simplest optimal regulator's output is a deterministic function of the system state. ("Model" = policy.)
2. **Internal Model Principle (1976):** A robust controller must contain a copy of the disturbance dynamics. ("Model" = dynamical simulator of disturbances.)
3. **Erdogan (2021):** The Good Regulator Theorem doesn't actually say what people think — it proves you need a good policy, not a world model. Deflation.
4. **Richens et al. (2025):** General agents (multi-goal, multi-step) DO necessarily contain world models (extractable from the policy). Re-inflation, but with proper foundations.
5. **Virgo et al. (2025):** Any good regulator can be INTERPRETED as having beliefs, but this is observer-relative. The model is in the eye of the beholder.

### 6.2 The "Model" Ambiguity

The entire history of this literature is haunted by the word "model" meaning different things:

| Usage | What it actually means | Who uses it |
|-------|----------------------|-------------|
| Conant & Ashby | Deterministic mapping S → R (a policy) | Cybernetics |
| Francis & Wonham | Dynamical copy of exosystem | Control theory |
| Model-based RL | Transition model P(S'|S,A) | ML/AI |
| Virgo et al. | Observer-attributed belief structure | ALife/philosophy |
| Richens et al. | Extractable predictive model from policy | Modern AI theory |
| Common parlance | Internal representation of external reality | Everyone else |

Much confusion in the literature stems from failing to distinguish these.

### 6.3 What Is Actually Established

Taking all these results together:

1. **Deterministic policies are optimal** (Conant & Ashby) — not deep.
2. **Robust linear controllers must contain disturbance models** (Francis & Wonham) — deep and practically important.
3. **Multi-goal agents implicitly contain world models** (Richens et al.) — deep and relevant to modern AI.
4. **Any good regulator admits a belief interpretation** (Virgo et al.) — philosophically interesting but observer-relative.
5. **The original Good Regulator Theorem does NOT prove agents need world models** (Erdogan) — important corrective.

### 6.4 Open Questions

- Does the Richens et al. result extend to partially observable settings (POMDPs)?
- Can the Virgo et al. belief-interpretation framework be made quantitative (probabilistic rather than possibilistic)?
- Is there a unified theorem that subsumes both the IMP and the Good Regulator Theorem?
- What is the relationship between Richens et al.'s extractable world models and the actual computational mechanisms used by trained agents?

---

## 7. Key Takeaways for an Agent-Design Perspective

1. **Do not cite the Good Regulator Theorem as proof that agents need world models.** It proves no such thing. The "model" in the theorem is a policy, not a predictive model.

2. **The Internal Model Principle is the real engineering result.** If you want robust rejection of structured disturbances, your controller literally needs to simulate those disturbances internally.

3. **Richens et al. (2025) is the modern result that proves world models are necessary** — but only for agents that generalize across goals in multi-step settings. Model-free agents that handle only a single task need not contain world models.

4. **The Virgo et al. (2025) result is philosophically important** but operationally weak: saying an observer CAN interpret an agent as having beliefs is not the same as saying the agent HAS beliefs or USES a model.

5. **The real lesson may be Ashby's Law of Requisite Variety** (1956), which underlies all of this: a controller must have at least as many distinguishable responses as there are distinguishable disturbances. The Good Regulator Theorem is, in some sense, an information-theoretic restatement of requisite variety.

---

## Sources

- Conant, R.C. & Ashby, W.R. (1970). [Full text PDF](https://pespmc1.vub.ac.be/books/Conant_Ashby.pdf)
- Erdogan, G. (2021). [Blog post](https://gokererdogan.github.io/2021/02/12/good-regulator-theorem/)
- Virgo, N. et al. (2025). [arXiv:2508.06326](https://arxiv.org/abs/2508.06326)
- Richens, J. et al. (2025). [arXiv:2506.01622](https://arxiv.org/abs/2506.01622)
- Francis, B.A. & Wonham, W.M. (1976). "The Internal Model Principle of Control Theory." *Automatica*, 12, 457-465. [Semantic Scholar](https://www.semanticscholar.org/paper/The-internal-model-principle-of-control-theory-Francis-Wonham/da7a60f2db454fda5a5c412f567edd798f506d80)
- Baez, J.C. (2016). [Blog post on the theorem](https://johncarlosbaez.wordpress.com/2016/01/27/the-good-regulator-theorem/)
- Swentworth, J. (2023). ["Fixing the Good Regulator Theorem"](https://www.lesswrong.com/posts/Dx9LoqsEh3gHNJMDk/fixing-the-good-regulator-theorem) (LessWrong)
