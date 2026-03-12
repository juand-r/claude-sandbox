# Durfee & Lesser (1991) - Partial Global Planning

## Citation
Durfee, E.H. and Lesser, V.R. (1991). "Partial Global Planning: A Coordination Framework for Distributed Hypothesis Formation." *IEEE Transactions on Systems, Man, and Cybernetics*, Vol. 21, No. 5, pp. 1167-1183.

## Journal Details
- **Journal:** IEEE Transactions on Systems, Man, and Cybernetics
- **Volume/Issue:** 21(5), 1991
- **Pages:** 1167-1183

## Access
- IEEE Xplore: https://ieeexplore.ieee.org/document/120067/
- Semantic Scholar: https://www.semanticscholar.org/paper/9d36f224aa606c292841e70f2c6d62d3d630f700
- Full text accessed via Academia.edu

## Abstract (paraphrased)
Partial global planning provides a framework for coordinating multiple AI systems cooperating in a distributed sensor network. By combining a variety of coordination techniques into a single, unifying framework, it enables separate AI systems to reason about their roles and responsibilities as part of group problem solving, and to modify their planned processing and communication actions to act as a more coherent team. The framework is uniquely suited for systems working in continuous, dynamic, and unpredictable domains because it interleaves coordination with action and allows systems to make effective decisions despite incomplete and possibly obsolete information about network activity.

## Key Arguments

### The Coordination Problem
Multiple distributed AI systems need to form, exchange, and integrate individual hypotheses to create consistent interpretations of their shared environment. The challenge: no single system has complete global knowledge, yet they must act coherently as a team.

### Partial Global Plans (PGPs)
The key innovation is that agents don't need complete global plans. Instead, they build **partial** global views of the planning problem. Each agent maintains:
- Its own local plan
- Partial knowledge of other agents' plans
- A coordination strategy based on this incomplete picture

### Interleaving Coordination with Action
Rather than planning everything before acting (which is impractical in dynamic environments), PGP interleaves:
- **Action:** Agents execute tasks based on current best knowledge
- **Coordination:** Agents exchange plan information and adjust
- **Re-planning:** Plans are modified as new information arrives

This makes the framework robust to incomplete and outdated information.

### Key Design Principles
1. Agents reason about their roles and responsibilities within the group
2. Communication is selective -- agents share what's relevant, not everything
3. Plans are modifiable -- agents can adjust based on coordination information
4. No central coordinator -- coordination emerges from distributed interactions

## Relevance to Agent Design

### Multi-Agent LLM Systems
PGP directly addresses the coordination problem in modern multi-agent LLM architectures:
- Multiple LLM agents working on a shared task need exactly this kind of partial coordination
- No single agent can have complete knowledge of what all others are doing
- The interleaving of action and coordination matches the iterative nature of agent execution

### Operating with Incomplete Information
PGP's key insight -- that agents can coordinate effectively with **partial** knowledge of each other's plans -- is critical for modern multi-agent systems where:
- Communication bandwidth is limited
- Agent states change rapidly
- Complete synchronization is impractical

### Role Reasoning
Agents reasoning about "their roles and responsibilities as part of group problem solving" anticipates modern approaches to agent role assignment in multi-agent frameworks (e.g., AutoGen, CrewAI).

### Extension to GPGP
The later Generalized PGP (GPGP) framework separated coordination from local scheduling, making it domain-independent. This separation of concerns is a key architectural principle for modern agent frameworks.

## Connections to Other Work
- Extends earlier work on Functionally Accurate, Cooperative (FA/C) distributed systems (Lesser & Corkill)
- Influenced GPGP and TAEMS frameworks for multi-agent coordination
- Related to Beer's VSM: System 2 (coordination) function operates with partial information about subsystem activities
- Connects to stigmergy: indirect coordination through shared environment
- Relevant to modern multi-agent frameworks: AutoGen, CrewAI, LangGraph

## Key Insight for Our Research
The concept of "partial" global planning -- that effective coordination doesn't require omniscience -- is a cybernetic insight applicable to modern agent architectures. Current multi-agent LLM systems often try to achieve full coordination (through a central orchestrator), but PGP suggests that distributed, partial coordination may be more robust and scalable. This connects to Ashby's insight that a regulator doesn't need to model everything, only the relevant variety.
