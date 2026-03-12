# Herring & Kaplan — Viable System Model for Software Architecture

## Key Papers

### 1. Herring & Kaplan (2000) — "The Viable System Model for Software"
- **Venue:** 4th World Multiconference on Systemics, Cybernetics and Informatics (SCI'2000)
- Uses Beer's VSM as basis for a component system architecture
- Proposes the **Viable System Architecture** (VSA)
- Key construct: the **"viable component"** — a software component structured with VSM-inspired interfaces

### 2. Herring — "Viable Software: The Intelligent Control Paradigm for Adaptable and Adaptive Architecture"
- Develops the **Intelligent Control Paradigm** as an instance of the Viable Software Approach
- VSM as basis for software system architecture
- Model-based architecture for developing software by *piecemeal adaptation*
- Goal: software that becomes *adaptive at runtime*
- Software built this way is called **Viable Software** — a unifying class of self-controlling software that is an intelligent control system

### 3. Herring & Kaplan — "Groove: A Case Study in Adaptive Architecture"
- **VSA as a high-level reference architecture**
- Applied to the Groove collaboration system
- Demonstrates how the VSM-based architectural methodology can extend existing systems with adaptive features

## The Viable System Architecture (VSA)

The VSA translates Beer's five systems into software architecture:

- **System 1 → Operational components** — the actual functional units doing work
- **System 2 → Coordination interfaces** — protocols for dampening oscillation between components
- **System 3 → Management/oversight layer** — monitors operational component performance, allocates resources
- **System 3* → Audit/verification** — independent checks on component behaviour
- **System 4 → Adaptation layer** — environmental monitoring, strategic adaptation
- **System 5 → Policy/identity** — configuration of system purpose and constraints

Each component is a "viable component" — self-contained, with its own internal five-system structure (recursion).

## Key Insights

1. **Piecemeal adaptation** — VSM-based software evolves incrementally rather than requiring complete redesign. Each component can adapt independently while maintaining whole-system viability.

2. **Self-controlling software** — "Viable Software" is software that regulates itself using cybernetic feedback loops. This predates (and is more theoretically grounded than) later "self-healing" and "self-adaptive" software concepts.

3. **Runtime adaptivity** — The goal is not just modular software but software that adapts its own behaviour at runtime, guided by VSM principles.

## Other VSM-IT Papers

### Peppard (2005) — "The Application of the Viable Systems Model to IT Governance"
- **Venue:** ICIS 2005
- VSM as theoretical lens for IT governance
- Single descriptive case study
- VSM used to describe and diagnose IT governance from a practical perspective

### VSM in Software Development Organisation
- Case study of "Violet Computing" — using VSM to diagnose and restructure a software development team
- VSM identified structural dysfunctions resulting from environmental shifts
- Key finding: VSM facilitates modularisation of teams and improved communication across units

## Gaps

- The Herring & Kaplan work is from 2000 and has not been widely continued
- No substantial body of work applying VSM to modern software patterns (microservices, event-driven, serverless)
- The search for "VSM + microservices" returned no relevant results
- There is an open opportunity to connect VSM to modern cloud-native architecture patterns

## Relevance to Agent Architectures

This is the most directly relevant body of work for our project. Key takeaways:

1. VSM *can* be translated into software architecture — Herring & Kaplan proved this
2. The "viable component" concept maps to "viable agent" — an agent with its own internal five-system structure
3. Runtime adaptivity is a key goal: agents that adapt their own behaviour using cybernetic feedback
4. The gap in modern applications (microservices, cloud-native) represents an opportunity
5. The Groove case study shows the approach works for extending existing systems — important for practical adoption
