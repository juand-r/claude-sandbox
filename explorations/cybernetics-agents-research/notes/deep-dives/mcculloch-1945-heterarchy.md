# McCulloch — "A Heterarchy of Values Determined by the Topology of Nervous Nets" (1945)

**Author:** Warren S. McCulloch
**Published:** Bulletin of Mathematical Biophysics, Vol. 7, pp. 89-93, 1945
**DOI:** 10.1007/BF02478457
**Full text:** Behind paywall (Springer). Not freely available online.

## The Core Problem

How do you handle **intransitive preferences** in a system?

In a hierarchy, if A > B and B > C, then A > C (transitivity). But McCulloch observed that nervous systems routinely exhibit circular preferences: A preferred to B, B preferred to C, but C preferred to A.

This is not a bug. It is a feature.

## The Concept of Heterarchy

McCulloch coined the term **"heterarchy"** to describe an organizational structure where:
- There is no single supreme governing level
- Multiple competing orderings coexist
- Control flows circularly rather than top-down
- Which element dominates depends on context

### Heterarchy vs. Hierarchy

| Hierarchy | Heterarchy |
|---|---|
| Fixed rank: A > B > C | Circular: A > B > C > A |
| Single ordering principle | Multiple competing orderings |
| Transitivity holds | Transitivity violated |
| Top-down control | Distributed, contextual control |
| Stable, rigid | Adaptive, flexible |

### The Rock-Paper-Scissors Analogy
Rock beats scissors, scissors beats paper, paper beats rock. No single element dominates. This is heterarchical.

## The Neural Basis

McCulloch showed that circular preferences correspond to **circular pathways in neural nets**. The topology of the network determines the value structure.

From the abstract: "Because of the dromic character of purposive activities, the closed circuits sustaining them and their interaction can be treated topologically." The value anomaly (intransitive preference) "corresponds to a circularity in the neural net."

Key insight: **"The apparent inconsistency of preference is shown to indicate consistency of an order too high to permit construction of a scale of values."**

This means: what looks like irrational behavior is actually a higher-order consistency that cannot be captured by a simple linear ranking.

## Why This Is Critical for Multi-Agent Systems

This paper is arguably more relevant to modern AI agent architectures than the 1943 paper. Here's why:

### 1. Multi-Agent Coordination Without Fixed Hierarchy
Most multi-agent systems assume either:
- A fixed hierarchy (orchestrator -> workers)
- Full equality (peer-to-peer)

Heterarchy offers a third option: **contextual authority**. Different agents lead depending on the situation. This maps directly to McCulloch's later concept of "Redundancy of Potential Command."

### 2. Handling Conflicting Objectives
Real-world AI systems must balance competing values (safety vs. helpfulness, speed vs. accuracy, cost vs. quality). A hierarchical value ordering forces you to always prioritize the same thing. A heterarchical value ordering allows the system to prioritize differently in different contexts — which is what intelligent behavior actually requires.

### 3. Robustness Through Circularity
A hierarchy has a single point of failure at the top. A heterarchy, with its circular structure, has no single point of failure. If any node fails, the circular flow continues through the remaining nodes.

### 4. Emergent Behavior
Heterarchical structures produce emergent behavior that cannot be predicted from the individual components. This is exactly what we see in multi-agent systems and swarm intelligence.

## Modern Applications

- **Manufacturing control**: Heterarchical multi-agent systems have been studied extensively for factory control (dispatching, scheduling)
- **Decentralized AI architectures**: Google Research evaluates peer-to-peer mesh architectures where agents communicate directly
- **Hybrid control**: Modern MARL (Multi-Agent Reinforcement Learning) uses CTDE (Centralized Training, Decentralized Execution) — a blend of hierarchy and heterarchy
- **Swarm intelligence**: Emergent self-organization among agents with decentralized control

## Connection to Other McCulloch Work

- Builds on the 1943 paper's neural net formalism
- Directly leads to "Redundancy of Potential Command" (1950s-60s)
- Collected in *Embodiments of Mind* (MIT Press, 1965)

## Key Takeaway

Hierarchy is not the only — or even the best — way to organize a complex system. Heterarchy, where authority is contextual and value orderings are circular, produces more adaptive, robust, and intelligent behavior. McCulloch proved this mathematically for neural nets in 1945. The AI field is still catching up.
