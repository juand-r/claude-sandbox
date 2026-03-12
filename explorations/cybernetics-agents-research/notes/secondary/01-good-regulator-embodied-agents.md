# A "Good Regulator Theorem" for Embodied Agents

## Citation
Virgo, N., Biehl, M., Baltieri, M., & Capucci, M. (2025). "A 'Good Regulator Theorem' for Embodied Agents." *Proceedings of Artificial Life 2025 (ALIFE)*, MIT Press. arXiv:2508.06326.

## Summary

Revisits and generalizes the classic Conant & Ashby (1970) theorem — "every good regulator of a system must be a model of that system" — for embodied agents operating under partial observability. The original theorem required structural isomorphism between controller and system; this paper shifts to an observer-attributed interpretation where an agent "has a model" rather than "is a model."

## Key Arguments

1. **The original theorem is too narrow.** Artificial Life has produced many counterexamples (Braitenberg vehicles, simple reflexive systems) that regulate effectively without any obvious internal model. The original proof assumes full observability and deterministic systems — conditions rarely met by embodied agents.

2. **Models are observer-dependent.** The paper introduces "consistent belief maps" ψ: X → P(Z) that assign to each agent state a set of possible environmental states. These are *possibilistic* (not probabilistic) — they track which environments remain consistent with observations. A model is not an intrinsic property of the system but is imposed by an external observer (aligns with Dennett's intentional stance).

3. **Main theorem (Thm 3.4):** An agent is a good regulator if and only if it can be interpreted as a "subjective good regulator" — one that maintains consistent beliefs about environmental states, updates them via a Mealy machine model, and keeps beliefs within a goal set.

4. **Trivial models resolve counterexamples.** A doorstop "regulates" a door but has a trivial model (constant belief). The theorem holds universally, but the explanatory value depends on model non-triviality. Complex feedback coupling produces non-trivial models.

## Relevant Formalisms

- **Regulation situation**: Agent-environment pairing with good set G ⊆ X×Y
- **Good regulator**: Agent with nonempty, forward-closed regulating set R ⊆ G
- **Consistent belief maps**: Must satisfy possibilistic update rule — updated beliefs contain all environment states consistent with prior beliefs, observed actions, and sensor values
- **String diagrams**: Used to represent sensorimotor loops as composed morphisms

## Connection to Our Research

This is directly relevant to understanding what it means for an AI agent to have an "internal model" of its task environment:

- **ReAct/Reflexion**: These agents maintain working memory that tracks environmental state. The belief-map formalism could formalize what kind of "model" their scratchpads constitute.
- **Good Regulator ↔ Agent World Models**: The paper explicitly draws parallels to efforts extracting learned environmental models from trained agents — relevant to understanding whether LLM agents implicitly learn world models.
- **Observer-dependence**: The insight that models are observer-attributed rather than intrinsic challenges naive claims about whether LLMs "truly understand" their domains. What matters is whether an observer can consistently attribute beliefs.
- **Connection to Free Energy Principle**: Authors note resemblance to FEP synchronization maps but express uncertainty about precise mathematical relationship.

## Key References to Chase

1. **Conant, R.C. & Ashby, W.R. (1970).** "Every good regulator of a system must be a model of that system." *Int. J. Systems Science*, 1(2), 89-97. — The original theorem.
2. **Baltieri, M., Virgo, N., & Capucci, M. (2025).** Work on possibilistic reasoning and the internal model principle — extends this framework.
3. **McGregor, S. (2016, 2017).** "As-if" agency formalizing Dennett's intentional stance — foundational for the observer-dependent model interpretation.
