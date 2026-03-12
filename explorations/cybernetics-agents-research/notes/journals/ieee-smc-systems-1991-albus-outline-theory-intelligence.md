# Albus (1991) — Outline for a Theory of Intelligence

## Citation
Albus, J.S. (1991). "Outline for a Theory of Intelligence." IEEE Transactions on Systems, Man, and Cybernetics, 21(3), 473-509. DOI: 10.1109/21.97471

## Source
- IEEE Xplore: https://ieeexplore.ieee.org/document/97471/
- NIST: https://www.nist.gov/publications/outline-theory-intelligence
- NASA NTRS: https://ntrs.nasa.gov/citations/19920029704

## Full Text Access
Not accessed. Behind IEEE paywall. NIST and NASA NTRS provide metadata only.

## Key Ideas

### Definition of Intelligence
Intelligence is defined as "that which produces successful behavior." It is assumed to result from natural selection. The paper integrates knowledge from research on both natural (biological) and artificial systems.

### Hierarchical Architecture
The model is a multi-level hierarchical system with four scaling principles at each ascending level:

1. **Control bandwidth** decreases by roughly one order of magnitude per level
2. **Perceptual resolution** of spatial and temporal patterns contracts by about an order of magnitude per level
3. **Goals and planning horizons** expand in scope (space and time) by about an order of magnitude per level
4. **World models and event memories** expand their range by about an order of magnitude per level

### Functional Modules (at every level)
Each node in the hierarchy contains four functional modules:
- **Behavior Generation** — task decomposition, planning, and execution
- **World Modeling** — maintaining a model of the environment at the appropriate abstraction level
- **Sensory Processing** — receiving and processing sensory data into higher-level abstractions
- **Value Judgment** — evaluating situations and alternative plans

Sensory feedback control loops close at every level.

### Connection to NIST RCS
This paper is the theoretical foundation for the NIST Real-time Control System (RCS) architecture, later developed into the 4D/RCS reference model architecture used in autonomous vehicles and robots (DARPA programs, etc.).

## Relevance to Agent Design
This is one of the most directly relevant papers for agent architecture design. The four-module-per-level structure maps naturally onto LLM agent components:
- **Behavior Generation** → task planning and tool use
- **World Modeling** → context/memory management
- **Sensory Processing** → input parsing and perception
- **Value Judgment** → evaluation/reward functions

The order-of-magnitude scaling principle across levels is a powerful design constraint for hierarchical agents: higher levels plan over longer time horizons with coarser abstractions, lower levels execute with finer resolution and faster feedback loops.

The principle of "increasing precision with decreasing intelligence" (from Saridis, which Albus builds on) suggests that higher cognitive functions should set goals and constraints, while lower levels handle precise execution — directly applicable to how an LLM agent might delegate to specialized tools.

## Citations
~786 on Semantic Scholar, ~469 on IEEE Xplore.
