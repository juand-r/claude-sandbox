# Richens et al. (2025) — General Agents Contain World Models

**Full Citation:** Richens, J., Abel, D., Bellot, A., & Everitt, T. (2025). "General Agents Contain World Models." *ICML 2025*. arXiv:2506.01622.

**Cited in our notes:** good-regulator-theorem.md (Section 4)

**Source:** Full text accessed via [ar5iv](https://ar5iv.labs.arxiv.org/html/2506.01622).

---

## 1. The Question

Do agents capable of flexible, goal-directed behavior necessarily contain world models? This paper proves the affirmative — and does so in a way that is meaningfully stronger than the Good Regulator Theorem.

## 2. Setup

### Environment
A **controlled Markov process (cMP)**: tuple (S, A, P) where P_{ss'}(a) = P(S'=s' | A=a, S=s). Finite state space, finite action space, irreducible (every state reachable from every other), stationary.

### Goals
Expressed via **Linear Temporal Logic (LTL)**:
- Eventually (◇): reach a target state
- Next (○): take a specific action
- Now (⊤): trivial/current constraint
- Goals compose sequentially or in parallel
- "Depth" measures number of sub-goals

### Agents
Goal-conditioned deterministic policies π mapping histories and goals to actions. A **bounded goal-conditioned agent** satisfies regret bound δ for goals up to depth n:

P(τ ⊨ ψ | π, s₀) ≥ max_π P(τ ⊨ ψ | π, s₀)(1 − δ) for ψ ∈ Ψ_n

## 3. Main Theorem (Theorem 1)

**Claim:** Any bounded agent achieving goals of depth n > 1 must encode an accurate world model in its policy.

**Formal result:** Given a bounded agent with failure rate δ for depth-n goals, one can extract world model P̂_{ss'}(a) with error:

|P̂_{ss'}(a) − P_{ss'}(a)| ≤ √[2P_{ss'}(a)(1 − P_{ss'}(a)) / ((n−1)(1−δ))]

For δ ≪ 1 and n ≫ 1, error ~ O(δ/√n) + O(1/n).

## 4. Proof Strategy

The extraction algorithm (Algorithm 1) works by querying the agent with "either-or" composite goals:
1. Agent must choose between: (a) succeed r times at transitioning s → s' via action a, or (b) succeed r+1 times
2. Agent's action choice reveals which outcome has higher success probability
3. By varying r and observing decision boundaries, the algorithm estimates P_{ss'}(a)
4. The regret bound ensures decision points concentrate near the true median

**Key lemmas:**
- Lemmas 3 & 4 factorize sequential goals, isolating single-step transitions
- Lemma 6 shows optimal agents achieve composite goals with binomial success probabilities parameterized by P_{ss'}(a)

## 5. Theorem 2: Myopic Agents Need No World Model

Agents optimizing only immediate outcomes (n=1) need NOT learn transition probabilities. The paper constructs a myopic-optimal policy consistent with *any* transition function.

**Implication:** World models become necessary ONLY for multi-step horizons. Single-step regulation (the domain of the Good Regulator Theorem) does not require world models.

## 6. Relationship to Good Regulator Theorem

The paper explicitly critiques Conant & Ashby:
- The Good Regulator Theorem proves only that optimal policies are deterministic functions of state — it says nothing about predictive world models.
- This paper proves the stronger claim: multi-goal agents necessarily contain extractable world models.
- But it requires stronger assumptions: multi-step, multi-goal, communicating MDP, full observability.

## 7. Implications for Agent Design

1. **No model-free shortcut:** Any agent generalizing to long-horizon tasks implicitly learns environmental dynamics. Model-free and model-based approaches are informationally equivalent for general agents.

2. **Emergent capabilities:** Simple goal sequences may trigger world model learning, potentially explaining emergent generalization in LLMs.

3. **Safety applications:** World models can be extracted from capable agents without internal access — supporting interpretability and safety verification.

4. **Capability bounds:** Agent capabilities are bounded by learnability of accurate world models.

## 8. Limitations

- Assumes **full observability** — extension to POMDPs unclear
- Proves **existence** but not specific **use** of the recovered model
- Requires communicating MDP (all states reachable)
- Does not address computational cost of model extraction

## 9. Relation to Our Cybernetics-Agents Research

This is the modern completion of the research program begun by Conant & Ashby:

| Paper | What it proves | Assumptions |
|-------|---------------|-------------|
| Conant & Ashby (1970) | Optimal policy is deterministic | Single-step, finite |
| Francis & Wonham (1976) | Controller must contain exosystem dynamics | LTI systems, continuous |
| Richens et al. (2025) | Multi-goal agents contain world models | Multi-step, communicating MDP |

The progression shows increasing strength of the "model necessity" claim as assumptions are refined.

### Bridge to cybernetic principles
- **Ashby's Law of Requisite Variety** sets the floor: enough distinct responses for distinct disturbances
- **Conant-Ashby** says those responses should be deterministic functions of state
- **Richens et al.** says for multi-step goals, those functions encode predictive dynamics
- This vindicates Beer's System 4 (the "outside and then" function that maintains a model of the environment)

## 10. Key References from This Paper

- **Richens, J. & Everitt, T. (2024). "Robust Agents Learn Causal World Models."** — Companion result: agents maintaining low regret under distributional shifts must learn CAUSAL models.
- **Ha, D. & Schmidhuber, J. (2018). "World Models."** — Showed explicit world model learning improves agent performance.
- **Hutter, M. (2004). *Universal Artificial Intelligence*.** — AIXI framework for universal agents.

---

*Notes compiled 2026-03-12 from ar5iv full text.*
