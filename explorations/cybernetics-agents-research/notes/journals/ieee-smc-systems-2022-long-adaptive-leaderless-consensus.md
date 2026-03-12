# Adaptive Leaderless Consensus for Uncertain High-Order Nonlinear Multiagent Systems With Event-Triggered Communication

**Authors:** J. Long, W. Wang, J. Huang, J. Lu, K. Liu
**Journal:** IEEE Transactions on Systems, Man, and Cybernetics: Systems, vol. 52, no. 11, pp. 7101-7111, 2022
**DOI:** 10.1109/TSMC.2021.3089435

## Summary

Addresses the leaderless consensus problem for uncertain high-order nonlinear MAS with event-triggered communication.

### Key contributions
- **Leaderless** (vs. leader-following): no designated reference agent; all agents must converge to a common state through purely local interactions
- **High-order nonlinear**: agents have complex dynamics, not just simple integrators
- **Uncertain**: system parameters are not precisely known -- requires adaptive control
- **Event-triggered**: agents communicate only when a triggering condition is met, reducing communication burden

### Technical approach
- Adaptive backstepping control design
- Neural networks or function approximation for handling unknown nonlinearities
- Event-triggered mechanism to reduce communication frequency
- Exclusion of Zeno behavior (infinite triggers in finite time)

## Relevance to Our Research

The "leaderless" aspect is particularly interesting from a cybernetics perspective. It connects to:
- **Self-organization**: order emerges from local interactions without central coordination (Beer's VSM principle of autonomy)
- **Autopoiesis**: the collective behavior is self-generating through agent interactions
- **Stigmergy-like coordination**: agents influence each other indirectly through their states

The combination of uncertainty + event-triggering + leaderless consensus represents a highly distributed, resource-efficient coordination paradigm -- very relevant to designing autonomous agent systems.

## Access

Full text NOT freely available. Behind IEEE paywall.
