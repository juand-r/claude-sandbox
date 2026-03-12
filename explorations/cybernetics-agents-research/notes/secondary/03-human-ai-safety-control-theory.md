# Human-AI Safety: A Descendant of Generative AI and Control Systems Safety

## Citation
Bajcsy, A. & Fisac, J.F. (2024). "Human-AI Safety: A Descendant of Generative AI and Control Systems Safety." arXiv:2405.09794.

## Summary

A position paper that explicitly bridges control theory safety frameworks with generative AI. Proposes modeling human-AI interaction as a closed-loop dynamical system and introduces a safety filter formalism operating on latent state spaces. The core thesis: safety means "continued satisfaction of the human's critical needs at all times" — a constraint-satisfaction problem, not a value-alignment optimization problem.

## Key Arguments

1. **Values vs. Needs distinction.** Safety is not about optimizing for human values (alignment) but about never violating hard constraints (needs). This is a fundamentally different framing — one from control theory (constraint satisfaction) vs. ML (loss minimization).

2. **Closed-loop analysis required.** Analyzing model outputs in isolation is insufficient. Safety requires analyzing feedback loops between AI outputs and human responses over time — a dynamic systems perspective.

3. **Safety filter architecture.** Three components:
   - **Fallback policy** (π_shield): Conservative policy prioritizing failure avoidance
   - **Safety monitor** (Δ): Evaluates whether candidate actions preserve safety
   - **Intervention scheme** (φ): Permits safe actions; replaces unsafe ones with safe alternatives

4. **Formal safety game.** Models human-AI interaction as a zero-sum dynamic game with safety value function: V(z₀) := max_πAI min_πH (min_t≥0 ℓ(z_t)). The AI must find a strategy guaranteeing safety against worst-case human behavior.

## Relevant Formalisms

- **State representation**: Three interacting dynamics — world state (s), human internal state (z^H), AI internal state (z^AI)
- **Safe information state set Ω**: States from which there exists an AI policy maintaining safety against all allowable human behaviors
- **Universal Safety Filter Theorem (6.1)**: If the AI starts in a state deemed safe under fallback policy, the filtered system maintains safety for all time, for any task policy, against all allowable human behaviors
- **Failure specification**: Three approaches — explicit rules (Constitutional AI), common sense (extractable via prompting), personal feedback (learned from interaction)

## Connection to Our Research

This paper is the most direct bridge between classical control theory and modern AI agent safety:

- **Ashby's variety ↔ Operational Design Domain**: The paper's "allowable human behaviors" (action bound Â^H) is essentially a variety constraint. The AI must have requisite variety to handle all behaviors within the ODD.
- **Good Regulator ↔ Internal Model**: The AI's latent state z^AI must model the human's internal state z^H — a direct instantiation of Conant-Ashby's theorem.
- **Ultrastability ↔ Safety Filter**: The safety filter that intervenes when the system approaches failure boundaries is structurally similar to Ashby's ultrastable system switching parameters when essential variables approach limits.
- **PCT connection**: The safety value function ℓ measures "distance from failure" — analogous to PCT's error signal (discrepancy between current and reference perception). The system acts to keep this positive.
- **Cybernetic hierarchy**: The fallback-monitor-intervention architecture mirrors a cybernetic control hierarchy — operational controller (task policy) overseen by a meta-controller (safety filter).

## Key References to Chase

1. **Fisac, J.F. et al. (2019).** "A general safety framework for learning-based control in uncertain robotic systems." — The original safety filter formalism for robotics.
2. **Mitchell, I.M. et al. (2005).** Reachability analysis — foundational method for computing safe sets.
3. **Leveson, N. (2011).** *Engineering a Safer World.* — Systems-theoretic accident model (STAMP), a cybernetic approach to safety engineering.
