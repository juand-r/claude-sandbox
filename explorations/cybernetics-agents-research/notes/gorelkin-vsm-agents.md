# Gorelkin (2025) - VSM for Enterprise Agentic Systems

## Source
- Mikhail Gorelkin, "Stafford Beer's Viable System Model for Building Cost-Effective Enterprise Agentic Systems"
- Medium, November 1, 2025
- https://medium.com/@magorelkin/stafford-beers-viable-system-model-for-building-enterprise-agentic-systems-81982d6f59c0

## Context

Gorelkin argues that enterprise agentic AI systems lack a coherent systems theory. The automation-based approach to building agent architectures has no blueprint for how agents should coordinate, adapt, and maintain viability as they scale. His proposal: use Beer's Viable System Model as that blueprint.

He references a February 2025 IBM Research paper "Agentic AI Needs a Systems Theory" as identifying the gap, and positions management cybernetics as the solution. He participated in the American Society for Cybernetics in the early 2000s, so this is informed by genuine cybernetics background.

## The Core Mapping: VSM -> Agentic Systems

Beer's VSM has five subsystems. Gorelkin maps each to components of an enterprise agent architecture:

### System 1: Operational Units
The individual AI agents that perform specific tasks. In an enterprise context, these are the agents handling customer service, data processing, code generation, etc. Each System 1 unit is itself a viable system (VSM's recursive/fractal property), meaning each agent can have its own internal regulation.

### System 2: Coordination Mechanisms
Prevents conflicts between System 1 operational units. In agent terms: how do multiple agents avoid stepping on each other, duplicating work, or creating contradictory outputs? System 2 provides **lateral coordination** -- agents coordinate with each other without going through a central controller.

This is the key architectural challenge Gorelkin identifies: "When you have multiple AI agents, how do they coordinate without creating bottlenecks?" His answer is that VSM's System 2 provides the mechanism for lateral coordination, while System 3 handles vertical integration.

### System 3: Operational Management
Optimizes current operations and ensures resource allocation. In agent terms: which agents get how much compute, API budget, context window? System 3 monitors operational performance and reallocates resources. It handles the **vertical integration** -- making sure the whole is more than the sum of parts.

### System 4: Strategic Intelligence
Scans the environment for threats and opportunities, models possible futures. In agent terms: monitoring for new capabilities, emerging user needs, competitive threats. System 4 is forward-looking where System 3 is present-focused.

### System 5: Policy and Identity
Sets ultimate direction and resolves conflicts between System 3 (present optimization) and System 4 (future adaptation). In agent terms: what is the organization's AI policy? What values govern agent behavior? How do you maintain alignment as agents learn and evolve?

## The System 3-4 Homeostat

Gorelkin highlights the critical tension between System 3 and System 4 as the **exploitation-exploration tradeoff**:

- System 3 wants to optimize what's working now (exploitation)
- System 4 wants to explore new possibilities and adapt (exploration)
- System 5 balances these two, preventing either from dominating

This maps directly onto a fundamental problem in AI agent systems: do you keep using the current approach that works, or do you invest in trying new tools, models, and strategies? VSM provides a structural answer rather than leaving it to ad hoc heuristics.

## Tiered Intelligence: A Pragmatic Application

Gorelkin's most concrete architectural recommendation: not every decision needs a frontier model.

- **System 2 coordination**: Local open-source LLMs (Llama, Mistral, Qwen) -- these are routine arbitration tasks
- **System 3 operations**: Mix of local and frontier models depending on complexity
- **System 4 strategic intelligence**: Frontier models (GPT-4, Claude) -- needs sophisticated reasoning
- **System 5 policy decisions**: Frontier models plus human oversight

This is a **variety-appropriate resource allocation**: match the sophistication of the regulator to the complexity of what's being regulated. Using GPT-4 for simple coordination is wasteful (over-specified variety); using a small model for strategic analysis is dangerous (under-specified variety).

## Two Paradigms of Agentic AI

Gorelkin distinguishes:

1. **Cognitive approach**: Human + digital twin (ensemble of agentic experts). Synergistic collaboration. The human is part of the system.
2. **Automation approach**: Orchestrated specialized agents performing tasks through predefined protocols and workflows. The human is outside the system.

He favors the cognitive approach as more aligned with cybernetic principles -- the human is structurally coupled with the agent system, not just supervising it.

## Recursive/Fractal Architecture

Beer's core insight that Gorelkin emphasizes: VSM is recursive. Each System 1 operational unit is itself a viable system with its own Systems 1-5. This creates a fractal architecture that scales naturally.

For agent systems, this means:
- A customer service agent team is a viable system
- Each individual agent within it is also a viable system
- The entire enterprise agent infrastructure is a viable system
- At every level, the same structural principles apply

This avoids the common problem of agent architectures that work at one scale but break at another.

## Cybersyn as Precedent

Gorelkin references Beer's Cybersyn project in Chile (1971-1973) as a precedent for using cybernetic principles to manage complex real-time systems. Cybersyn attempted to manage the national economy using VSM principles, with a network of telex machines connecting factories across the country to a central operations room.

The analogy to enterprise agent systems: you're managing a distributed network of autonomous units (agents/factories) that need coordination without centralization.

## Critical Assessment

### Strengths
- Provides a principled architecture rather than ad hoc orchestration
- The recursive property solves the scaling problem elegantly
- The System 3-4 homeostat directly addresses exploitation/exploration
- Tiered intelligence is a practical cost-optimization insight
- Grounded in decades of management cybernetics theory and practice

### Weaknesses / Open Questions
- This is a Medium article, not a peer-reviewed paper -- the mapping is suggestive rather than formal
- No concrete implementation or benchmarks
- Doesn't address how to actually implement System 2 coordination in practice (shared state? message passing? stigmergy?)
- The mapping from VSM to agents is plausible but not validated
- Doesn't address the temporal dynamics -- how fast do Systems 3-5 need to operate relative to System 1?
- No discussion of failure modes specific to agent-based System 1 units (hallucination, drift, etc.)

### Connection to Other Work
- Beer's VSM itself (see beer-vsm.md)
- IBM Research "Agentic AI Needs a Systems Theory" (February 2025) -- identifies the gap
- MDPI paper on VSM and organizational pathologies in the age of AI (2025) -- uses VSM to analyze AI risks
- MCP specification (see mcp-specification.md) -- provides the plumbing but not the architecture; MCP is infrastructure that could support VSM-organized agents
