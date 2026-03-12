# Deep Reinforcement Learning for Multiagent Systems: A Review of Challenges, Solutions, and Applications

## Citation
Nguyen, T.T., Nguyen, N.D., & Nahavandi, S. (2020). Deep Reinforcement Learning for Multiagent Systems: A Review of Challenges, Solutions, and Applications. *IEEE Transactions on Cybernetics*, 50(9), 3826-3839. DOI: 10.1109/TCYB.2020.2977374

## Access
- arXiv preprint: https://arxiv.org/abs/1812.11794
- PDF: https://arxiv.org/pdf/1812.11794
- IEEE Xplore: https://ieeexplore.ieee.org/document/9043893

## Summary

Highly cited survey (~895 citations) covering deep reinforcement learning approaches for multi-agent systems. Reviews the fundamental challenges that arise when multiple agents must learn simultaneously in shared environments.

## Key Challenges Identified

1. **Non-stationarity**: When multiple agents learn concurrently, each agent's environment becomes non-stationary from its own perspective because other agents' policies are changing. This breaks the Markov assumption that single-agent RL depends on.

2. **Partial observability**: In realistic multi-agent settings, agents cannot observe the full state of the environment or other agents' internal states.

3. **Continuous state and action spaces**: High-dimensional environments require function approximation (deep learning).

4. **Multi-agent training schemes**: Centralized training with decentralized execution (CTDE) vs. fully decentralized vs. fully centralized approaches.

5. **Multi-agent transfer learning**: Transferring knowledge between agents or between tasks.

## Key Approaches Reviewed

- Independent learners (each agent treats others as part of environment)
- Centralized training with decentralized execution (CTDE)
- Communication learning (agents learn what/when to communicate)
- Mean field approaches (approximate many-agent interactions via average)

## Relevance to Cybernetics-Agents Research

**HIGH RELEVANCE.** This paper maps directly onto several cybernetic themes:

1. **Non-stationarity = Ashby's ultrastability problem**: When the environment is non-stationary because other agents are adapting, each agent faces the same challenge Ashby described: the need for a system that can adapt to an environment that is itself adapting. Ashby's homeostat was designed precisely for this.

2. **Partial observability = The Good Regulator Theorem constraint**: Conant-Ashby says a good regulator must be a model of the system. Partial observability means agents cannot build complete models -- they must build *sufficient* models. This is exactly the question of requisite variety: how much variety in the model is needed?

3. **CTDE = Centralized vs. distributed control**: Beer's VSM explicitly addresses this: System 3 (centralized coordination) vs. System 1 (autonomous operations). CTDE is a pragmatic engineering answer to the same tension Beer formalized.

4. **Communication learning**: Agents learning what to communicate maps to Beer's variety engineering -- communication channels as variety attenuators/amplifiers between subsystems.

5. **Scalability**: The survey's concern with scaling to many agents echoes Ashby's variety explosion problem. Mean field approximation is essentially a variety reduction technique.

## Key Quotes / Observations

- The paper frames multi-agent RL as fundamentally about coordination through communication -- a cybernetic framing even if the authors don't use that language.
- The CTDE paradigm is essentially a pragmatic compromise between centralized regulation (high variety capacity but poor scalability) and decentralized autonomy (scalable but coordination-limited).

## Gaps / Limitations

- No connection made to classical cybernetics literature, despite the problems being deeply cybernetic.
- Limited discussion of stability guarantees -- cybernetic stability analysis (Lyapunov, Ashby's essential variables) could provide formal grounding.
- No discussion of homeostasis or bounded goals for agents.
