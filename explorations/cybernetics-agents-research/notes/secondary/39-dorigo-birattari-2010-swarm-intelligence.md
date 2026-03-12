# Dorigo & Birattari (2007/2010) — Swarm Intelligence

## Citation

Dorigo, M., & Birattari, M. (2007). Swarm intelligence. *Scholarpedia*, 2(9), 1462. DOI: 10.4249/scholarpedia.1462

Also relevant:
- Dorigo, M., Birattari, M., & Brambilla, M. (2014). Swarm robotics. *Scholarpedia*, 9(1), 1463.
- Brambilla, M., Ferrante, E., Birattari, M., & Dorigo, M. (2013). Swarm robotics: A review from the swarm engineering perspective. *Swarm Intelligence*, 7(1), 1–41.

Available: http://www.scholarpedia.org/article/Swarm_intelligence

## Definition

"Swarm intelligence is the discipline that deals with natural and artificial systems composed of many individuals that coordinate using decentralized control and self-organization. In particular, the discipline focuses on the collective behaviors that result from the local interactions of the individuals with each other and with their environment."

## Core Concepts

### 1. Decentralized Control

No central controller. No single agent has a global view or directs the others. Collective behavior emerges entirely from local interactions. This is the defining feature that distinguishes swarm intelligence from centralized multi-agent systems.

### 2. Self-Organization

The system organizes itself without external direction. Patterns of collective behavior emerge from simple rules followed by individual agents. Key mechanisms:
- **Positive feedback**: Amplification of successful behaviors (e.g., pheromone trails reinforced by successful ants)
- **Negative feedback**: Damping of unsuccessful behaviors (e.g., pheromone evaporation)
- **Fluctuations**: Random variations that enable exploration of new solutions
- **Multiple interactions**: Agents must interact frequently for collective patterns to emerge

### 3. Stigmergy

Indirect coordination through modification of the environment. Agent A modifies the environment; Agent B responds to the modification without needing to interact with A directly. Pheromone trails are the paradigmatic example. This is a form of variety transmission through the environment rather than through direct communication.

## Key Algorithms

### Ant Colony Optimization (ACO)

Inspired by ant foraging. Software "ants" explore solution spaces, depositing "pheromone" on good solutions. Subsequent ants are probabilistically attracted to pheromone trails. Over time, the colony converges on good solutions. Key properties:
- Stochastic construction: Each ant builds a solution probabilistically
- Pheromone model: Shared memory encoded in the environment
- Evaporation: Old solutions decay, preventing premature convergence
- Applications: Traveling salesman, routing, scheduling

### Particle Swarm Optimization (PSO)

Inspired by bird flocking. Each "particle" has a position (candidate solution) and velocity. Particles are attracted toward their personal best position and the global best position found by the swarm. Over time, the swarm converges.

### Swarm Robotics

Physical embodiment of swarm intelligence principles. Robot swarms are:
- **Fault-tolerant**: No single point of failure
- **Scalable**: Adding robots doesn't require redesigning the system
- **Flexible**: The swarm can adapt to changing environments

Design challenges: Currently "more art than science" — no systematic design methodology exists. Most design is manual (human designer specifies individual behaviors and hopes for useful emergent collective behavior) or evolutionary (optimize individual controllers via evolutionary algorithms).

## Relevance to Agent Design

### 1. Swarm Intelligence as Anti-Centralization

Current LLM agent architectures are typically centralized: a single LLM makes decisions, uses tools, generates responses. Even multi-agent frameworks (CrewAI, AutoGen) often have an "orchestrator" agent that coordinates. Swarm intelligence provides a fundamentally different paradigm:
- No orchestrator
- Local information only
- Collective intelligence emerges from simple interactions

### 2. Stigmergy for Multi-Agent Coordination

Instead of agents passing messages to each other, they could modify a shared environment (database, file system, knowledge graph) and respond to each other's modifications. This is stigmergy. It scales better than direct communication and is more robust to individual agent failures.

This connects to the stigmergy notes already in this project.

### 3. The Variety Argument

From a cybernetic perspective, swarm intelligence achieves requisite variety through **aggregation**: each agent has limited variety (simple rules, local information), but the swarm collectively has enormous variety through the combinatorial space of possible interaction patterns. This is Ashby's principle at work: variety is distributed across the swarm rather than concentrated in a single complex controller.

### 4. Exploration vs. Exploitation

ACO elegantly balances exploration (random search) and exploitation (following pheromone trails) through the evaporation mechanism. This is a concrete, well-studied implementation of the exploration-exploitation tradeoff that all agents face. LLM agents struggle with this — they tend to either explore randomly (trying many tools) or exploit narrow patterns (repeating successful approaches).

### 5. The "More Art Than Science" Problem

Dorigo acknowledges that swarm design is currently ad hoc. This echoes the state of LLM agent design: we assemble architectures (ReAct, Reflexion, etc.) based on intuition and experimentation, without systematic design principles. Cybernetics offers design principles (requisite variety, good regulation, ultrastability) that could systematize both swarm design and agent design.

## Connection to Cybernetics

- **Self-organization**: Core to both cybernetics (Ashby, von Foerster) and swarm intelligence
- **Decentralized control**: Ashby's principle that the controller need not be separate from the controlled system
- **Feedback loops**: Positive feedback (pheromone reinforcement) and negative feedback (evaporation) as regulation mechanisms
- **Variety distribution**: The swarm distributes requisite variety across many simple agents rather than concentrating it in one complex agent
- **Stigmergy as environmental coupling**: Agents coupled through their environment, not through direct communication — this is the cybernetic concept of circular causality applied to multiple agents

## Relation to Other Notes

- Bonabeau et al. (1999): The foundational book on swarm intelligence
- Stigmergy in multi-agent systems: Direct application
- Ashby variety calculus: Variety distribution in swarms
- VSM (Beer): Hierarchical vs. flat organization — swarms are flat, VSM is hierarchical. Tension?
- Heylighen stigmergy: Theoretical framework
