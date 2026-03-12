# Busoniu, Babuska & De Schutter (2008) — A Comprehensive Survey of Multiagent Reinforcement Learning

## Citation
Busoniu, L., Babuska, R., and De Schutter, B. (2008). "A Comprehensive Survey of Multiagent Reinforcement Learning." IEEE Transactions on Systems, Man, and Cybernetics, Part C: Applications and Reviews, 38(2), 156-172. DOI: 10.1109/TSMCC.2007.913919

## Source
- IEEE Xplore: https://dl.acm.org/doi/10.1109/TSMCC.2007.913919
- Author PDF: https://busoniu.net/files/papers/smcc08.pdf (accessed, downloaded)

## Full Text Access
PDF downloaded from author's website. Full text available.

## Key Ideas

### Scope
Comprehensive survey of multiagent reinforcement learning (MARL) — the problem of multiple autonomous agents learning to behave optimally through trial-and-error interaction in shared environments.

### Core Challenges
- **Non-stationarity**: each agent's environment includes other learning agents, so the environment changes as agents learn
- **Partial observability**: agents may not observe the full state or other agents' actions
- **Curse of dimensionality**: joint state-action spaces grow exponentially with the number of agents
- **Credit assignment**: determining each agent's contribution to collective outcomes

### Taxonomy
The paper organizes MARL approaches along several dimensions:
- **Cooperative vs. Competitive vs. Mixed** settings
- **Independent learners** (each agent runs single-agent RL, ignoring others) vs. **Joint action learners** (agents model other agents' behaviors)
- **Centralized vs. Decentralized** learning and execution
- **With vs. without communication** between agents

### Two Focal Goals
1. **Stability** — convergence of the learning dynamics despite non-stationarity
2. **Adaptation** — ability to adjust to changing behavior of other agents

### Key Algorithm Families
- Independent learners (simple, scalable, but no convergence guarantees)
- Joint action learners (model opponents, but don't scale)
- Policy gradient and actor-critic methods adapted for multiagent settings
- Team-based and cooperative methods (shared reward, communication)

## Relevance to Agent Design
This is directly relevant to multi-agent LLM systems:
- The cooperative vs. competitive taxonomy applies to multi-agent LLM architectures
- The tradeoff between independent learning (scalable but unstable) and joint learning (principled but expensive) mirrors the tradeoff between independent LLM agents and tightly coordinated multi-agent systems
- The stability-adaptation tension is central: in multi-agent LLM systems, if one agent changes behavior (e.g., a prompt change), all others must adapt
- The credit assignment problem appears when multiple agents contribute to an outcome and we need to determine which agent's contribution was valuable

The paper identifies that for cooperative settings with full observability, convergence is relatively tractable, but partial observability and competitive/mixed settings remain hard — this maps to the challenges in real-world multi-agent LLM deployments.

## Citations
Highly cited survey paper, foundational reference for MARL research.
