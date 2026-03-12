# A Dynamic Periodic Event-Triggered Approach to Consensus of Heterogeneous Linear Multiagent Systems With Time-Varying Communication Delays

## Citation
Deng, C., Che, W.-W., & Wu, Z.-G. (2021). A Dynamic Periodic Event-Triggered Approach to Consensus of Heterogeneous Linear Multiagent Systems With Time-Varying Communication Delays. *IEEE Transactions on Cybernetics*, 51(4), 1812-1821. DOI: 10.1109/TCYB.2019.2920531

## Access
- IEEE Xplore: https://ieeexplore.ieee.org/document/8753682
- No arXiv preprint found.

## Summary

Proposes a dynamic periodic event-triggered mechanism for achieving consensus in heterogeneous multi-agent systems. Rather than communicating continuously (expensive, often unnecessary) or at fixed intervals (potentially wasteful or too infrequent), agents communicate only when a triggering condition is met -- and this condition itself adapts dynamically based on the system's state.

## Key Technical Ideas

1. **Event-triggered communication**: Agents transmit information only when a local triggering condition detects that their state has changed enough to warrant communication. This reduces communication overhead dramatically.

2. **Dynamic triggering thresholds**: Unlike static event-triggered schemes where the threshold is fixed, this paper uses a dynamic internal variable that adapts the threshold. When the system is far from consensus, communication is more frequent; near consensus, it becomes rare.

3. **Heterogeneous agents**: Agents have different dynamics (different A, B matrices in their state-space models), making consensus harder because they must coordinate despite having fundamentally different behaviors.

4. **Zeno-free guarantee**: Proves that the triggering events don't accumulate infinitely fast (no "Zeno behavior"), which would make the scheme impractical.

## Relevance to Cybernetics-Agents Research

**HIGH RELEVANCE.** Event-triggered communication is a deeply cybernetic idea with direct relevance to agent design:

1. **Event-triggering = attention/salience mechanism**: The triggering condition is a formalized attention mechanism. The agent only communicates (allocates communication resources) when something "interesting" happens -- when its state has changed enough to be worth reporting. This is exactly the variety filtering that cybernetics prescribes: don't transmit everything, transmit only what matters.

2. **Dynamic thresholds = adaptive variety management**: The dynamic internal variable that adjusts the triggering threshold is an adaptive variety attenuator. When the system is "hot" (far from equilibrium), more variety flows through communication channels. When it's "cool" (near consensus), variety is attenuated. This is precisely Beer's variety engineering in action.

3. **Heterogeneous consensus = viable system coordination**: Different agents with different dynamics must reach agreement. In VSM terms: System 1 units with different operational characteristics must be coordinated by System 2/3 mechanisms that account for their heterogeneity.

4. **Directly applicable to LLM multi-agent systems**: LLM-based multi-agent systems (CrewAI, AutoGen, etc.) face the same problem: when should agents communicate? Current systems either communicate after every step (wasteful, context-exhausting) or at fixed intervals (potentially missing critical updates). Event-triggered communication provides a principled alternative.

5. **Zeno behavior avoidance = preventing communication floods**: In LLM agent systems, excessive inter-agent communication can exhaust context windows and API budgets. The Zeno-free guarantee is the formal analogue of preventing "communication storms" in agent systems.

## Key Insight for Our Research

This paper formalizes the answer to a critical question for multi-agent AI systems: **how do agents decide when to communicate?** The cybernetic answer: communicate when the discrepancy between your internal model of the system and the actual system state exceeds a dynamically-adjusted threshold. This is variety filtering applied to communication bandwidth.

## Gaps

- Linear systems only.
- Fixed communication topology -- no adaptation of who communicates with whom.
- The triggering conditions are mathematically elegant but may be hard to implement for LLM agents where "state" is a high-dimensional embedding.

## Status: INACCESSIBLE
Key information from IEEE Xplore metadata and search results. Full paper requires subscription.
