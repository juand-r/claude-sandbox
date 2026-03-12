# Large-Scale Traffic Signal Control Using a Novel Multiagent Reinforcement Learning

## Citation
Wang, X., Ke, L., Qiao, Z., & Chai, X. (2021). Large-Scale Traffic Signal Control Using a Novel Multiagent Reinforcement Learning. *IEEE Transactions on Cybernetics*, 51(1), 174-187. DOI: 10.1109/TCYB.2020.3015811

## Access
- arXiv preprint: https://arxiv.org/abs/1908.03761
- PDF: https://arxiv.org/pdf/1908.03761
- IEEE Xplore: https://ieeexplore.ieee.org/document/9184911

## Summary

Proposes Cooperative Double Q-Learning (Co-DQL) for large-scale traffic signal control. Addresses three critical challenges: scalability to many intersections, modeling inter-agent interactions, and stability of learning. Uses mean field approximation to handle the exponential growth of joint action spaces.

## Key Technical Contributions

1. **Independent Double Q-Learning**: Extends double Q-learning to multi-agent setting to eliminate overestimation bias. Each agent maintains two Q-functions.

2. **Mean Field Approximation**: Models the effect of neighboring agents as an average (mean field), reducing the complexity from exponential in number of agents to linear. Each agent only needs to track the average behavior of its neighbors rather than individual policies.

3. **UCB Exploration Policy**: Uses Upper Confidence Bound to balance exploration vs. exploitation in a principled way.

4. **Enhanced Reward Allocation**: Designs reward functions that align individual agent incentives with global system performance.

5. **Local State Sharing**: Agents share local state information with neighbors to improve coordination without requiring global communication.

## Relevance to Cybernetics-Agents Research

**HIGH RELEVANCE.** This paper is a concrete instance of several cybernetic principles applied (unknowingly) to agent design:

1. **Mean field as variety reduction**: The mean field approximation is a textbook example of Ashby's variety management. The full joint action space has variety that grows exponentially -- no agent can model it. Mean field reduces this to a manageable summary statistic. This is precisely the kind of variety attenuation that Ashby argues any viable regulator must perform.

2. **Requisite variety in practice**: Each traffic signal agent must have enough variety in its policy to handle the variety of traffic patterns it encounters. The paper's reward engineering is an attempt to match the agent's variety to the problem's variety.

3. **Distributed autonomy with coordination**: Each intersection controls itself (System 1 in VSM terms) while local state sharing provides minimal coordination (System 2). There is no global controller -- global coherent behavior emerges from local interactions. This is precisely Beer's recursive viable system structure.

4. **Scalability through decomposition**: The paper's approach to scaling is fundamentally cybernetic: decompose the problem into semi-autonomous units that coordinate locally. This is the VSM principle of recursive viable systems.

5. **Double Q-learning as error-correcting feedback**: The two Q-functions provide a mechanism for detecting and correcting overestimation bias -- a negative feedback loop that maintains accuracy (homeostasis of value estimates).

## Key Numbers

- Tested on SUMO traffic simulator
- Scales to 30+ intersections
- Outperforms independent Q-learning, independent DQN, and several other baselines
- Average waiting time reduced significantly compared to fixed-time signals

## Gaps

- No analysis of what happens when the environment changes fundamentally (e.g., road closures, new construction). The system is adaptive but may not be ultrastable.
- Mean field assumption breaks down when agent interactions are highly heterogeneous -- acknowledges this limitation.
- No formal stability analysis of the learning process itself.
