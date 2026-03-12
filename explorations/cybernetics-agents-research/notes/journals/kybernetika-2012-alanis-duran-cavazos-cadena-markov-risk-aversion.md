# An Optimality System for Finite Average Markov Decision Chains Under Risk-Aversion

- **Authors:** Alfredo Alanís-Durán, Rolando Cavazos-Cadena
- **Journal:** Kybernetika, Vol. 48, No. 1, pp. 83-104
- **Year:** 2012
- **DOI:** N/A
- **URL:** https://www.kybernetika.cz/content/2012/1/83
- **PDF:** https://www.kybernetika.cz/content/2012/1/83/paper.pdf
- **Access:** Open access (diamond OA)

## Abstract

Studies controlled Markov chains with finite state space and compact action sets where
decision makers exhibit risk-averse preferences with constant risk-sensitivity. The
optimal (possibly non-constant) value function is characterized by a system of optimality
equations, from which optimal stationary policies can be derived. The paper proves
equivalence between superior and inferior limit average cost functions under standard
continuity-compactness assumptions.

## Key Concepts

### Risk-Sensitive MDPs
- Standard MDPs optimize expected total/average reward.
- Risk-sensitive MDPs incorporate risk preferences via an exponential utility:
  the decision maker's objective involves E[exp(γ · total_cost)] where γ < 0
  represents risk aversion.
- This changes the optimality equation structure: costs in different states become
  coupled through the exponential transformation.

### Optimality System (Not Just One Equation)
- In standard average-cost MDPs with communicating chains: a single optimality equation
  (Bellman equation) suffices.
- Under risk aversion: the optimal average cost may be non-constant across states,
  requiring a *system* of equations -- one for each partition element of the state space.
- The state space partitions into classes where different average costs may apply.

### State Space Partition
- The state space decomposes into groups based on which states communicate under
  optimal policies.
- Each group may have a different optimal average cost.
- This is a richer structure than the standard MDP setting where the optimal average
  cost is a single scalar.

### Stationary Optimal Policies
- Despite the more complex value function structure, optimal policies remain stationary
  (time-invariant, state-dependent).
- The policy depends only on the current state -- consistent with Markov/feedback form.

## Mathematical Framework

- Finite state space S, compact action sets A(x).
- Transition kernel p(·|x, a) with continuity in a.
- Cost function c(x, a) continuous in a.
- Risk sensitivity parameter γ < 0 (risk aversion).
- Perron-Frobenius theory used for existence results.
- Average cost criterion with exponential utility.

## Relevance to Cybernetics-Agents Research

1. **Risk-averse agents:** Real agents should not be risk-neutral. A robot performing
   a dangerous task or a financial agent should exhibit risk aversion. This paper
   provides the mathematical foundation for risk-sensitive decision making in
   Markov environments.

2. **Beyond expected value:** The exponential utility captures the idea that an agent
   should not just optimize expected performance but should also avoid catastrophic
   outcomes -- directly relevant to safe AI and robust agent design.

3. **State-dependent optimal costs:** The insight that optimal performance may differ
   across states (non-constant value function) is relevant for agents operating in
   heterogeneous environments where different "regions" have different difficulty levels.

4. **MDP foundations for agent design:** MDPs are the mathematical backbone of
   reinforcement learning. This paper extends the theory to risk-sensitive settings,
   bridging classical control theory (where robustness is central) with decision theory.

5. **Stationary policies suffice:** Even with risk aversion, memoryless state-feedback
   policies are optimal -- supporting reactive agent architectures.

## Keywords

partition of the state space, nonconstant optimal average cost, equality of superior
and inferior limit risk-averse average criteria

## Classification

93E20, 60J05, 93C55
