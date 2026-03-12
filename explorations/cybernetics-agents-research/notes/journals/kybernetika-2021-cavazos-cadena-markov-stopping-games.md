# Markov Stopping Games with an Absorbing State and Total Reward Criterion

- **Authors:** Rolando Cavazos-Cadena, Luis Rodríguez-Gutiérrez, Dulce María Sánchez-Guillermo
- **Journal:** Kybernetika, Vol. 57, No. 3, pp. 474-492
- **Year:** 2021
- **DOI:** 10.14736/kyb-2021-3-0474
- **URL:** https://www.kybernetika.cz/content/2021/3/474
- **Access:** Open access (diamond OA)

## Abstract

Examines discrete-time zero-sum games where Player II decides whether to halt the
system (paying terminal rewards to Player I) or allow continued evolution. When the
system is active, Player I selects actions affecting state transitions and earning
running rewards. The value function is characterized by an equilibrium equation, and
Nash equilibrium existence is established under conditions where an absorbing state
remains accessible from any position.

## Key Concepts

### Stopping Games (Dynkin Games)
- Two-player games where one key decision is *when to stop*.
- Originated with Dynkin (1969); extended by Shapley to Markov settings.
- At each step: Player II can stop (pay terminal reward) or continue.
- If continuing, Player I chooses an action affecting transitions.
- Game ends when absorbing state is reached or Player II stops.

### Value Function and Equilibrium Equation
- The value function V(x) satisfies a fixed-point equation combining:
  - Terminal reward (if stopping)
  - Running reward + discounted future value (if continuing)
- Existence proved via non-expansive operator properties and monotonicity.

### Total Reward Criterion
- Performance measured by total expected reward (undiscounted sum).
- The absorbing state assumption ensures the sum is well-defined (game terminates
  with probability 1).

## Mathematical Framework

- Denumerable state space S with absorbing state s*.
- Action set A(x) for Player I at state x.
- Transition kernel q(·|x, a).
- Terminal reward g(x), running reward r(x, a).
- Non-expansive operator T on bounded functions.
- Fixed-point theorem yields value function; saddle point yields equilibrium.

## Relevance to Cybernetics-Agents Research

1. **Optimal stopping = when to act:** A fundamental agent design problem is deciding
   *when* to take an action vs. *when* to wait for more information. Stopping games
   formalize this tradeoff.

2. **Two-agent adversarial interaction:** The zero-sum structure models an agent operating
   in an adversarial environment -- one player tries to maximize reward while the
   environment (or adversary) can terminate the interaction.

3. **Absorbing states as goal states:** The absorbing state concept maps naturally to
   task completion in agent design -- once the goal is reached, the agent's episode ends.

4. **Total reward = cumulative performance:** Agents in realistic settings accumulate
   rewards/costs over time. The total reward criterion (rather than discounted) is
   more natural for finite-horizon or terminating tasks.

5. **Equilibrium as robust strategy:** Nash equilibrium strategies are robust to worst-case
   opponent behavior -- relevant for agents that must perform well under uncertainty
   about environmental responses.

## Keywords

hitting time, non-expansive operator, monotonicity property, fixed point, equilibrium
equation, bounded rewards

## Classification

91A10, 91A15
