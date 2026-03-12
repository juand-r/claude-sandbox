# Weiss (1999) — Multiagent Systems: A Modern Approach to Distributed Artificial Intelligence

**Full Citation:** Weiss, G. (Ed.) (1999). *Multiagent Systems: A Modern Approach to Distributed Artificial Intelligence*. Cambridge, MA: MIT Press. 547 pp.

**Source:** MIT Press, ACM Digital Library, Amazon, Semantic Scholar, JCST book review (Vidal), UMA PDF.

---

## 1. Overview

An edited volume with thirteen chapters by leading researchers, serving as the first comprehensive textbook-level treatment of DAI (Distributed Artificial Intelligence) as a mature field. Where Ferber (1999) is a single author's vision and Wooldridge (2002) is a pedagogical introduction, Weiss provides depth through specialist contributors.

**Definition of DAI:** "The study, construction, and application of multiagent systems, that is, systems in which several interacting, intelligent agents pursue some set of goals or perform some set of tasks."

## 2. Structure and Key Chapters

### Part I: Basic Themes (Chapters 1-8)

**Ch. 1: Intelligent Agents (Wooldridge)**
- Defines agent properties: autonomy, situatedness, reactivity, proactiveness
- Agent-environment coupling as a formal relationship
- Notation for describing agent behavior

**Ch. 2: Multiagent Systems and Societies of Agents (Huhns & Stephens)**
- Moves from individual agents to societies
- Agent communication: speech acts, KQML, KIF, ontologies
- Interaction protocols as the medium of collective intelligence

**Ch. 3: Distributed Problem Solving and Planning (Durfee)**
- Task decomposition and distribution
- Partial global planning
- Coordination of distributed plans

**Ch. 4: Search (various)**
- Bidirectional and real-time multiagent search
- Asynchronous dynamic programming in multi-agent settings
- Distributed optimization

**Ch. 5: Distributed Rational Decision Making (Sandholm)**
- Game-theoretic analysis of agent interaction
- Mechanism design for multi-agent systems
- Strategic behavior and equilibria

**Ch. 6: Learning in Multiagent Systems (Sen & Weiss)**
- Types of multi-agent learning
- Credit assignment in multi-agent settings
- Reinforcement learning with multiple agents
- Building models of other agents
- Relationship between learning and communication

**Ch. 7: Computational Organization Theory (Carley & Gasser)**
- Organizations as computational entities
- Organizational design as a multi-agent problem
- Knowledge sharing, adaptivity, and learning in organizations
- Connecting organizational science to AI

**Ch. 8: Formal Methods in DAI (Singh, Rao & Georgeff)**
- Modal, dynamic, and temporal logics for agents
- BDI logics: formal semantics for beliefs, desires, intentions
- Verification and specification of multi-agent systems

### Part II: Related Themes (Chapters 9-13)

**Ch. 9: Industrial and Practical Applications (Parunak)**
- Bridging research and industry
- Real-world problems suited to agent solutions
- Manufacturing, logistics, information management

**Ch. 10-13:** Groupware/CSCW, distributed decision support, concurrent programming, distributed control.

## 3. Key Contributions Beyond Wooldridge and Ferber

### 3.1 Multi-Agent Learning (Ch. 6)
The most relevant chapter for modern AI agent research. Key issues:
- **Credit assignment**: When multiple agents contribute to an outcome, how do you determine which agent's actions were responsible? This is the multi-agent version of the RL credit assignment problem.
- **Agent modeling**: Agents that build models of other agents' behavior can predict and adapt to them. This is the multi-agent Good Regulator: to interact effectively with another agent, you need a model of that agent.
- **Learning vs. communication**: There is a tradeoff — agents can learn about each other through observation or through explicit communication. Learning is slower but does not require shared protocols.

### 3.2 Computational Organization Theory (Ch. 7)
Connects organizational science to MAS. Key ideas:
- Organizations can be modeled as multi-agent systems with specific structural properties
- Organizational design is equivalent to choosing an agent coordination architecture
- There is a formal relationship between organizational structure, information processing capacity, and task performance

This is directly relevant to Beer's VSM — Carley and Gasser's organizational theory addresses the same problem (how to structure an organization for effective performance) but from a computational rather than cybernetic perspective.

### 3.3 Formal Methods (Ch. 8)
Provides logical frameworks for specifying and verifying agent behavior:
- **BDI logic**: Formal semantics for what it means for an agent to believe, desire, and intend
- **CTL (Computation Tree Logic)**: For reasoning about possible futures of multi-agent systems
- **Social commitments**: Formal treatment of obligations and agreements between agents

## 4. Cybernetic Analysis

### 4.1 What's Implicitly Cybernetic
- **Distributed problem solving**: Multiple control loops operating in parallel on different aspects of a shared problem
- **Organizational adaptation**: Organizations that modify their own structure in response to performance feedback — Beer's variety engineering from a computational perspective
- **Agent modeling**: The Good Regulator Theorem applied to inter-agent interaction
- **Learning as model improvement**: Increasing the requisite variety of the agent's world model through experience

### 4.2 What Cybernetics Would Add
- **Requisite variety analysis**: No chapter explicitly analyzes whether a multi-agent system has sufficient collective variety for its task environment
- **Stability analysis**: No treatment of whether multi-agent coordination converges or oscillates — cybernetic stability analysis would fill this gap
- **Hierarchical control**: The book treats organization as a design choice but does not provide a principled hierarchical architecture like Beer's VSM
- **Self-organization**: Largely absent — the book focuses on designed organizations, not emergent ones

### 4.3 What MAS Adds to Cybernetics
- **Game theory**: Formal treatment of strategic interaction that cybernetics lacks
- **Formal verification**: Logical tools for proving properties of multi-agent systems
- **Communication protocols**: Structured inter-agent communication that goes beyond Pask's conversation theory
- **Mechanism design**: Designing the rules of interaction to achieve desired collective outcomes

## 5. Relevance to Modern Agent Design

### 5.1 The Credit Assignment Problem Resurfaces
Modern multi-agent LLM systems (CrewAI, AutoGen) face exactly the credit assignment problem described in Ch. 6:
- When a multi-agent pipeline produces a wrong answer, which agent is responsible?
- When it produces a right answer, which agent's contribution was essential?
- Current multi-agent frameworks have no systematic approach to this problem.

### 5.2 Agent Modeling in LLM Multi-Agent Systems
Sen and Weiss's treatment of agent modeling suggests that LLM agents in multi-agent systems should build models of each other:
- What does agent X know?
- What is agent X likely to do in this situation?
- How should I adjust my communication to be useful to agent X?

Current multi-agent LLM architectures typically treat other agents as black boxes — they send messages and hope for useful responses.

### 5.3 Organizational Theory as Architecture Selection
Carley and Gasser's computational organization theory provides a principled basis for choosing multi-agent architectures:
- Different organizational structures (hierarchical, flat, market-based) have different information processing capacities
- The right structure depends on the task characteristics (decomposability, uncertainty, interdependence)
- Current multi-agent LLM frameworks default to hierarchical structures without considering whether other forms might be more appropriate

## 6. Connections to Other Sources

- **Wooldridge (2002)**: Wooldridge contributes Ch. 1 to Weiss. The textbook develops many of the same ideas in more pedagogical form.
- **Ferber (1999)**: Ferber's treatment of reactive agents and emergent coordination complements Weiss's more formal, cognitive agent focus.
- **Beer (VSM)**: Carley & Gasser's organizational theory is the MAS counterpart to Beer's organizational cybernetics. A synthesis of the two perspectives would be valuable.
- **Ashby (requisite variety)**: The multi-agent learning chapter implicitly engages with requisite variety through the concept of agent modeling capacity.
- **Conant & Ashby (1970)**: Agent modeling is the multi-agent application of the Good Regulator Theorem.

---

*Notes compiled 2026-03-12 from MIT Press, ACM Digital Library, JCST review, and UMA PDF.*
