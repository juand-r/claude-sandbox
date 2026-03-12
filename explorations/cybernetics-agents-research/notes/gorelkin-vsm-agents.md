# Gorelkin (2025) - VSM for Enterprise Agentic Systems

## Source
- Mikhail Gorelkin, "Stafford Beer's Viable System Model for Building Cost-Effective Enterprise Agentic Systems," Medium, November 1, 2025
- URL: https://medium.com/@magorelkin/stafford-beers-viable-system-model-for-building-enterprise-agentic-systems-81982d6f59c0
- Context: Responds to IBM Research's Feb 2025 paper "Agentic AI Needs a Systems Theory"

## Core Argument

The enterprise AI agent space lacks a coherent systems theory. Current approaches rely on automation-based orchestration (frameworks, prompt chaining, workflow tools) without a structural blueprint for how agents should coordinate, adapt, and maintain viability at scale. Gorelkin argues Beer's Viable System Model provides exactly this blueprint.

The key gap: **When you have multiple AI agents, how do they coordinate without creating bottlenecks?** The standard approach -- centralized orchestrators -- doesn't scale. VSM offers a decentralized, recursive alternative.

## VSM-to-Agent-Architecture Mapping

### System 1: Operational Units
The agents that actually do things. Specialized AI agents handling specific business functions -- customer service, data analysis, document processing, etc. Each is semi-autonomous with its own domain expertise.

In VSM terms, each System 1 unit is itself a viable system (recursion). So a "customer service agent" might internally contain sub-agents for triage, response generation, escalation, etc. -- each with its own S1-S5 structure.

### System 2: Coordination Mechanisms
Prevents conflicts between System 1 agents. Handles scheduling, resource allocation, communication protocols between agents. **This is where anti-oscillation and dampening happens.**

Key insight for agent systems: System 2 provides *lateral* coordination -- agents coordinating with peers, not through a central authority. This maps to protocols, shared state, message queues, or stigmergic mechanisms.

Gorelkin's cost recommendation: System 2 tasks are routine coordination. They don't need frontier models. **Local open-source LLMs (Llama, Mistral, Qwen) suffice for S2.**

### System 3: Operational Management
Optimizes current operations. Ensures resource allocation across System 1 units. Monitors performance. Handles *vertical* integration -- the management function that ensures operational units collectively serve organizational goals.

In agent terms: the system that decides which agents get compute resources, API tokens, priority in queues. Performance monitoring, load balancing, quality assurance.

### System 4: Strategic Intelligence
Scans the environment for threats and opportunities. Models possible futures. The forward-looking, exploratory function.

In agent terms: agents or systems that monitor market changes, user behavior trends, new API capabilities, competitor actions. Identifies when the operational setup needs to change.

Gorelkin's cost recommendation: **This is where frontier models matter.** Strategic reasoning, novel situation analysis, long-horizon planning -- these need the most capable models.

### System 5: Policy and Identity
Sets ultimate direction. Resolves conflicts between System 3 (optimize present) and System 4 (prepare for future). Maintains organizational identity and values.

In agent terms: the policy layer that ensures agents remain aligned with organizational goals even as they learn and adapt. Constitutional constraints. Value alignment.

Gorelkin's cost recommendation: Also benefits from frontier models for sophisticated reasoning about values, trade-offs, and identity.

## The Exploitation-Exploration Tension (S3 vs S4)

This is one of the most cybernetically rich aspects. Beer's VSM structurally separates:
- **System 3**: Exploit current capabilities. Optimize what works now.
- **System 4**: Explore new possibilities. Sense the future.

These are in perpetual tension. System 5 exists precisely to arbitrate between them. In agent systems, this maps directly to the explore-exploit tradeoff in reinforcement learning, but at an architectural/organizational level rather than an individual decision level.

Without this structural separation, agent systems tend toward either:
- Pure exploitation (doing the same thing better, missing disruptive changes)
- Pure exploration (constantly changing, never stabilizing)

## Tiered Intelligence: A Practical Consequence

Not every VSM subsystem needs the same level of AI capability:

| VSM System | Function | Model Tier |
|---|---|---|
| System 1 | Operations | Mixed (task-dependent) |
| System 2 | Coordination | Local/cheap models |
| System 3 | Operational mgmt | Mid-tier models |
| System 4 | Strategic intelligence | Frontier models |
| System 5 | Policy/identity | Frontier models |

This has significant cost implications. Most enterprise agent frameworks use the same (expensive) model for everything. VSM says that's wasteful -- most coordination and routine management doesn't need GPT-4 class reasoning.

## Two Paradigms of Enterprise Agentic AI

Gorelkin identifies a split:

1. **Cognitive approach**: Human + digital twin (ensemble of agentic experts). Synergistic collaboration. The human is part of the system.
2. **Automation approach**: Orchestrated specialized agents performing tasks through predefined workflows. Human is external/supervisory.

VSM applies to both but the cognitive approach more naturally maps to VSM because it already treats the human-agent ensemble as a system with identity, adaptation, and recursive structure.

## Recursive/Fractal Architecture

The "genius" of VSM for agent systems: recursive structure. Each System 1 operational unit is itself a viable system. This means:
- An enterprise agent system has its S1-S5
- Each domain agent within it has its own S1-S5
- Each sub-agent within those has its own S1-S5
- All the way down to individual tool calls

This is how VSM handles scale naturally. You don't need a different architecture for 5 agents vs 500. The same pattern repeats at every level.

## Historical Context: Cybersyn

Gorelkin references Beer's Cybersyn project (Chile, early 1970s) as a real-world attempt at VSM-based management at national scale. The project connected factories across Chile in a real-time information network for economic management. While politically terminated, it demonstrated the viability of cybernetic management principles at scale.

## Cybernetic Analysis

### What Gorelkin Gets Right
1. **The need for a systems theory of agents is real.** Current agent frameworks are engineering without architecture. Orchestration frameworks solve plumbing problems, not structural ones.
2. **VSM's recursive structure maps naturally to hierarchical agent systems.** The fractal property means you get scale-invariant design.
3. **The S3/S4 tension is a genuine design problem.** Agent systems that can't balance exploitation and exploration will either stagnate or thrash.
4. **Tiered intelligence is economically important.** Using frontier models for coordination tasks is wasteful.

### What Could Be Stronger
1. **The mapping is mostly analogical.** Gorelkin describes what each VSM system *would* do in an agent context, but doesn't provide formal specifications or reference implementations. How exactly does S2 lateral coordination work between LLM agents? What protocol?
2. **MCP as a potential S2/S3 mechanism is not discussed.** There's a natural connection: MCP provides the communication protocol for tool coordination (S2) and resource management (S3).
3. **The variety management problem is implicit but not explicitly stated.** Ashby's Law is the foundation of VSM, and the key question for agent viability is whether the system has requisite variety to handle its environment. This should be front and center.
4. **No discussion of pathologies.** Beer's VSM also identifies organizational pathologies (structural coupling failures, missing systems, atrophied functions). An analysis of common agent system failures through this lens would be valuable.

### Connection to Other Work
- IBM Research's "Agentic AI Needs a Systems Theory" (Feb 2025) -- the paper Gorelkin responds to
- Beer's original VSM work (see notes/beer-vsm.md)
- MDPI paper on VSM and organizational pathologies in the AI age (Perez Rios's taxonomy)
- The tiered intelligence concept connects to MCP's model preference system (cost/speed/intelligence priorities)
