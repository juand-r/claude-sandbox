# Moed & Saridis (1990) - A Boltzmann Machine for the Organization of Intelligent Machines

## Citation
Moed, M.C. and Saridis, G.N. (1990). "A Boltzmann Machine for the Organization of Intelligent Machines." *IEEE Transactions on Systems, Man and Cybernetics*, Vol. 20, No. 5, pp. 1104-1115.

## Journal Details
- **Journal:** IEEE Transactions on Systems, Man and Cybernetics
- **Volume/Issue:** 20(5), September/October 1990
- **Authors:** Michael C. Moed and George N. Saridis, Rensselaer Polytechnic Institute (CIRSSE)

## Access
- IEEE Xplore: https://ieeexplore.ieee.org/document/59972/
- Full PDF via NASA: https://ntrs.nasa.gov/api/citations/19900019724/downloads/19900019724.pdf

## Core Framework: Hierarchical Intelligent Control

### The Three-Tier Architecture
Saridis's approach (developed since 1977) structures intelligent machines using three levels, governed by the **Principle of Increasing Precision with Decreasing Intelligence (IPDI)**:

1. **Organization Level:** Highest level. Responsible for planning the sequence of tasks/actions. Deals with maximum uncertainty, requires most "intelligence" (in the AI sense). Formulated here as a Boltzmann machine.
2. **Coordination Level:** Middle level. Coordinates the execution of tasks planned by the organization level. Manages interactions between subsystems.
3. **Execution Level:** Lowest level. Carries out actual control actions with maximum precision. Standard control theory applies.

### Entropy as Unifying Measure
The entire system is formulated as a probabilistic model where uncertainty and imprecision are expressed in terms of **entropies**. The optimal strategy for decision planning and task execution is found by **minimizing total entropy** in the system.

This is a remarkable insight: entropy serves as a bridge between information theory and control theory, providing a single cost function that spans from high-level symbolic planning to low-level continuous control.

### The Boltzmann Machine for Organization
The paper's main contribution is designing the Organization level as a **Boltzmann machine** (a type of neural network). Since this level must plan action sequences, the problem is formulated as finding the right sequence of tasks/events that minimizes entropy.

Three search techniques are presented for finding optimal action sequences:
1. **Simulated annealing**
2. **Expanding subinterval random search**
3. **Modified Genetic Algorithm** (proven to converge to the minimum)

### Machine Intelligence and Knowledge
The paper defines key quantities:
- **Machine Intelligence:** Measured by the reduction in entropy achieved by the system's decision-making.
- **Machine Knowledge:** The information stored that enables intelligent decisions.
- **Precision:** The accuracy of execution at the lowest level.

## Relevance to Agent Design

### IPDI Principle and Modern Agents
The Principle of Increasing Precision with Decreasing Intelligence is highly relevant to modern LLM agents:
- **High level (Organization):** LLM does broad strategic planning -- lots of "intelligence" but imprecise outcomes.
- **Middle level (Coordination):** Agent orchestration, tool selection, subtask management.
- **Low level (Execution):** Specific tool calls, API interactions -- precise and deterministic.

This maps directly to how we think about agent architectures: the LLM provides high-level reasoning while tools provide precise execution.

### Entropy Minimization as Agent Objective
The idea that an intelligent system should minimize total entropy (uncertainty) across all levels is a powerful framing for agent design. An agent that successfully reduces uncertainty about its environment and the outcomes of its actions is, by this measure, more intelligent.

This connects to:
- **Active inference** (Friston's free energy principle)
- **Information-gathering actions** in exploration/exploitation tradeoffs
- **Uncertainty-aware planning** in modern AI agents

### Neural Network for Planning
Using a Boltzmann machine (an energy-based model) for task sequencing was prescient. Modern approaches use transformers (also attention-based) for similar planning tasks. The underlying principle -- search for optimal sequences by minimizing a cost function -- remains the same.

### Self-Organization Through Search
The use of simulated annealing and genetic algorithms for finding optimal plans is an early example of what we now call "search" in AI planning. Modern agents use various search strategies (beam search, MCTS in Tree-of-Thoughts) for similar purposes.

## Connections to Other Work
- Extends Saridis's hierarchical intelligent control framework (1977, 1979)
- Related to Albus's RCS architecture (different approach to similar problem)
- The entropy formulation connects to information-theoretic approaches to control
- IPDI principle echoes Beer's VSM recursion levels
- Connects to Ashby's law of requisite variety (managing variety through hierarchical decomposition)

## Key Insight for Our Research
The IPDI principle provides a formal basis for something we observe empirically in LLM agent architectures: higher levels of the system trade precision for flexibility and generality. The entropy-based formulation gives us a quantitative language for discussing this tradeoff, which is missing from most current agent architecture discussions.
