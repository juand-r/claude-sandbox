# Virgo et al. (2025) — A Good Regulator Theorem for Embodied Agents

**Full Citation:** Virgo, N., Biehl, M., Baltieri, M., & Capucci, M. (2025). "A Good Regulator Theorem for Embodied Agents." *Proceedings of ALIFE 2025*, Kyoto, Japan. arXiv:2508.06326.

**Cited in our notes:** good-regulator-theorem.md (Section 3)

**Source:** Full text accessed via [ar5iv](https://ar5iv.labs.arxiv.org/html/2508.06326).

---

## 1. Motivation

Artificial Life has produced many counterexamples to the naive reading of the Good Regulator Theorem — Braitenberg vehicles, Brooks's subsumption architecture, passive dynamic walkers all regulate effectively without any apparent internal model. This paper reformulates the theorem to handle these cases.

## 2. Key Formal Framework

### Agent as Moore Machine
- Internal state space X
- Readout function r: X → A (produces actions)
- Update function u: X × S → X (processes sensory input)

### Environment as Mealy Machine
- State space Y
- Evolution function e: Y × A → Y × S (maps actions to next state + sensor values)

### Good Set and Regulating Set
- **Good set** G ⊆ X × Y: desirable coupled agent-environment states
- **Regulating set** R: a non-empty, forward-closed subset of G — trajectories starting in R remain in G indefinitely
- **Good regulator** (Definition 2.5): an agent for which such a regulating set exists

## 3. The Central Construction: Interpretation Maps

The key move: instead of requiring the agent to structurally BE a model, the theorem shows it can always be INTERPRETED as having beliefs.

The **interpretation map** ψ: X → P(Z) assigns to each agent internal state x a set of environment states that the agent "believes" are possible. This is NOT something the agent computes — it is something an external observer attributes.

### Consistent Belief Map
Function ψ satisfies consistency when beliefs update coherently:

update(ψ(x), r(x), s) ⊆ ψ(u(x, s))

Posterior beliefs (given action and sensor input) stay within what the agent's next state attributes.

## 4. Main Theorem (Theorem 3.4)

An agent performs objective regulation (classical sense) **if and only if** it admits interpretation as a "subjective good regulator" with consistent beliefs, where:

1. Beliefs update consistently (possibilistic Bayesian update)
2. Beliefs entail goals in all reachable states
3. Some initial agent state has nonempty attributed beliefs

## 5. The Doorstop Problem (Resolved)

Classic objection: a doorstop "regulates" the door (keeps it open). Does it "model" the door?

Resolution: Yes, you CAN attribute beliefs to the doorstop — but they are trivial. The doorstop's "beliefs" don't depend on its state (it has essentially no variable state) and don't update in response to input. The theorem holds, but the resulting "model" is degenerate.

This resolves the counterexample by making explicit that the theorem applies universally, but trivially for simple systems.

## 6. Key Differences from Conant & Ashby (1970)

| Aspect | Conant & Ashby (1970) | Virgo et al. (2025) |
|--------|----------------------|---------------------|
| Applies to | Simplest optimal regulators only | ALL good regulators |
| Temporal scope | Single step | Multi-step (sequential) |
| State spaces | Finite | Any (Moore/Mealy machines) |
| Framework | Probabilistic (entropy) | Possibilistic (set-valued) |
| "Model" is | Intrinsic structural property | Observer-attributed interpretation |
| Observer role | Implicit | Explicit (intentional stance) |

## 7. Philosophical Significance

The paper makes the observer's role explicit — following Dennett's **intentional stance**. Models are not intrinsic properties of systems but are attributed by observers based on:
1. System boundaries chosen
2. Goal definitions imposed
3. Achievement mechanisms identified

This aligns with von Foerster's second-order cybernetics: the observer is part of the description. The "model" is in the eye of the beholder.

## 8. Limitations

- The theorem tells you an interpretation EXISTS; not that the agent actually USES it
- The possibilistic framework avoids probability but is weaker than probabilistic accounts
- Trivial interpretations (doorstop) satisfy the theorem but provide no explanatory value
- The theorem is about WHAT can be attributed, not about mechanism

## 9. Relation to Our Cybernetics-Agents Research

### Connection to second-order cybernetics
This paper is essentially a formalization of von Foerster's insight: "objects are tokens for eigenbehaviors." The "model" attributed to the agent is an eigenform — a stable interpretation that the observer constructs from the agent-environment interaction. The agent doesn't "have" beliefs; the observer attributes beliefs to make the agent's behavior intelligible.

### Connection to Pask
Pask's M-individual/P-individual distinction maps here: the agent (M-individual) admits interpretation as a P-individual (with beliefs/perspectives). The interpretation is observer-dependent — different observers may attribute different belief structures.

### For agent design
- Useful for post-hoc analysis: given a working agent, what beliefs would make its behavior rational?
- Less useful for design: doesn't tell you how to build an agent that regulates
- Compatible with both model-based and model-free approaches

## 10. Key References from This Paper

- **Dennett, D. (1987). *The Intentional Stance*.** — Philosophical framework for attributing beliefs to systems.
- **Brooks, R. (1991). "Intelligence Without Representation."** — Subsumption architecture as counterexample to naive Good Regulator reading.
- **Braitenberg, V. (1984). *Vehicles*.** — Simple agents that appear purposeful without models.

---

*Notes compiled 2026-03-12 from ar5iv full text.*
