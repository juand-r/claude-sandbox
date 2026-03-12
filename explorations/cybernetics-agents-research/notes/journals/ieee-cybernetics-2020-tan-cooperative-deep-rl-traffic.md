# Cooperative Deep Reinforcement Learning for Large-Scale Traffic Grid Signal Control

## Citation
Tan, T., Bao, F., Deng, Y., Jin, A., Dai, Q., & Wang, J. (2020). Cooperative Deep Reinforcement Learning for Large-Scale Traffic Grid Signal Control. *IEEE Transactions on Cybernetics*, 50(6), 2687-2700. DOI: 10.1109/TCYB.2019.2904742

## Access
- IEEE Xplore: https://ieeexplore.ieee.org/document/8695577
- No arXiv preprint found.

## Summary

Proposes the Coder (Cooperative Deep Reinforcement learning) framework for traffic signal control in large-scale grid networks. Reports reducing congestion by approximately 30% in terms of waiting vehicles during high-density traffic flows.

## Key Technical Ideas

1. **Cooperative framework**: Agents share information through a cooperative mechanism, where each agent considers not only its own reward but the collective impact on the traffic network.

2. **Scalable architecture**: Designed specifically for grid-structured traffic networks, exploiting the regular topology for efficient information sharing.

3. **Deep RL with cooperation**: Combines deep Q-networks with a cooperative reward structure that encourages system-wide optimization rather than greedy local optimization.

## Relevance to Cybernetics-Agents Research

**MEDIUM RELEVANCE.** Complements the Wang et al. (2021) paper with a different approach to the same problem:

1. **Cooperative reward = global homeostasis objective**: The cooperative reward structure aligns individual agents with the system-level goal (minimize total congestion). In cybernetic terms, this is designing the "essential variables" of the system: each agent's reward function encodes what the system needs to keep within bounds.

2. **Grid topology as communication structure**: The grid network provides a natural communication topology. This is the physical instantiation of Beer's System 2 -- the coordination channels are determined by the physical adjacency of intersections.

3. **30% congestion reduction**: Demonstrates that cybernetic principles (distributed autonomous units with cooperative coordination) can produce substantial real-world improvements.

## Gaps

- Specific to grid networks -- doesn't generalize easily to irregular topologies.
- No formal stability analysis.
- Limited to the traffic domain.

## Status: INACCESSIBLE
Key information from search results and metadata. Full paper requires IEEE subscription.
