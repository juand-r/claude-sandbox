# Deterministic Markov Nash Equilibria for Potential Discrete-Time Stochastic Games

- **Author:** Alejandra Fonseca-Morales
- **Journal:** Kybernetika, Vol. 58, No. 2, pp. 163-179
- **Year:** 2022
- **DOI:** 10.14736/kyb-2022-2-0163
- **URL:** https://www.kybernetika.cz/content/2022/2/163
- **PDF:** https://www.kybernetika.cz/content/2022/2/163/paper.pdf
- **Access:** Open access (diamond OA)

## Abstract

Addresses finding deterministic (feedback/closed-loop) Markov Nash equilibria for a
class of discrete-time stochastic games. Applies a "potential game" framework using
dynamic programming on games with Borel state and action spaces and potentially
non-smooth, unbounded cost functions. Encompasses team coordination games and
stochastic games with action-independent transition laws.

## Key Concepts

### Potential Games
- A multi-player game is a "potential game" if there exists a single function (the
  potential) whose change when any one player deviates equals the change in that
  player's payoff.
- This reduces the multi-player optimization to a single-agent optimal control problem.
- Monderer & Shapley (1996) introduced the concept for static games; this paper
  extends it to stochastic dynamic games.

### Dynamic Programming for Game Equilibria
- The paper shows that standard dynamic programming (Bellman equation) techniques
  from optimal control theory carry over to computing Nash equilibria in potential games.
- Key result: Nash equilibria can be found by solving an optimal control problem rather
  than a fixed-point problem -- computationally much simpler.

### Deterministic/Feedback Strategies
- Focus on deterministic (pure strategy) Markov equilibria -- strategies that depend
  only on the current state, not the full history.
- This is the "feedback" or "closed-loop" form, directly analogous to state-feedback
  controllers in control theory.

## Mathematical Framework

- State space X and action spaces Ai are Borel spaces.
- Transition kernel Q(·|x, a1, ..., an) governs dynamics.
- Cost functions may be non-smooth and unbounded.
- Potential function P aggregates individual costs.
- Bellman optimality equation applied to P yields equilibrium strategies.

## Relevance to Cybernetics-Agents Research

1. **Multi-agent coordination:** Potential games model situations where agents' interests
   are partially aligned -- common in cooperative multi-agent systems. The potential
   function acts as a coordination mechanism.

2. **Control theory ↔ game theory bridge:** The core contribution is showing that game
   equilibria can be computed using control-theoretic tools (dynamic programming).
   This is a concrete realization of the cybernetic vision of unifying control and
   decision-making.

3. **Feedback strategies = reactive agents:** The focus on Markov/feedback strategies
   aligns with reactive agent architectures where decisions depend on current
   observations, not full history.

4. **Scalability insight:** Reducing N-player game to single-agent optimization is
   a powerful simplification for agent design -- suggests that if agent interactions
   have a potential structure, coordination can be achieved without explicit negotiation.

5. **Stochastic environments:** The framework handles stochastic transitions and
   unbounded costs, making it applicable to realistic agent environments.

## Keywords

optimal control, dynamic programming, stochastic games, potential approach

## Classification

91A50, 91A25, 93E20, 91A14, 91A10
