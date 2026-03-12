# VSM Mapped onto Multi-Agent Frameworks: CrewAI, LangGraph, AutoGen

**Stream G, Item 29**
**Date:** 2026-03-12

---

## 1. Beer's Viable System Model: Quick Recap

The VSM posits that any system capable of independent existence must contain five subsystems, seven communication channels, and a recursive structure. This is not an org chart but a set of **necessary and sufficient conditions for viability**.

### The Five Systems

| System | Function | Orientation |
|--------|----------|-------------|
| **S1 (Operations)** | Primary activities that produce the system. Multiple autonomous units, each itself a viable system at lower recursion. | Doing the work |
| **S2 (Coordination)** | Dampens oscillation between S1 units. Anti-conflict, not command. A service organ. | Preventing interference |
| **S3 (Control)** | Manages "inside and now." Resource allocation, performance monitoring, synoptic judgment of internal state. | Internal optimization |
| **S3\* (Audit)** | Sporadic, direct monitoring of S1 that bypasses routine reporting. Independent verification. | Trust but verify |
| **S4 (Intelligence)** | Scans "outside and then." Environmental monitoring, future modeling, strategic adaptation. | External adaptation |
| **S5 (Policy/Identity)** | Provides closure. Defines identity, values, purpose. Balances S3-S4 homeostat. Absorbs residual variety. | Who are we? |

### The Key Axioms

1. **First Axiom:** Horizontal variety (across S1 units) must equal vertical variety (through coordination/control channels). If horizontal exceeds vertical, the system fragments. If vertical exceeds horizontal, it is over-controlled.
2. **Second Axiom:** V(System 3) = V(System 4). Internal management and external intelligence must balance. This is the exploitation-exploration tradeoff.
3. **Third Axiom:** V(System 5) = residual variety from the S3-S4 imbalance. If the 3-4 homeostat works well, S5 has little to do; if it fails, S5 is overwhelmed.

### Recursion

> "In a recursive organizational structure, any viable system contains, and is contained in, a viable system."

The same five-system structure applies at every level. Each S1 unit is itself a viable system with its own S1-S5. This is cybernetic isomorphism — the structure at every recursion level is identical, differing only in domain.

### Variety Engineering

Ashby's Law: only variety absorbs variety. The VSM operationalizes this through **attenuators** (filters reducing incoming variety) and **amplifiers** (mechanisms increasing outgoing variety). The four organizational principles require that communication channels have higher capacity than the variety they carry, that transducers at boundaries match channel variety, and that these balances are maintained cyclically without delay.

### The Seven Channels

1. Resource bargaining (S3 ↔ S1, two-way)
2. Command (S3 → S1, downward)
3. S2 coordination/damping (among S1 units and to S3)
4. S3\* audit (direct into S1 operations)
5. Lateral S1-to-S1 channels
6. Environment-to-S1 channels
7. Algedonic (pain/pleasure) emergency escalation

---

## 2. Framework-by-Framework VSM Analysis

### 2.1 CrewAI

**Architecture summary:** CrewAI organizes agents as a "crew" of role-based specialists coordinated through sequential, hierarchical, or custom processes. Core primitives are Agents, Tasks, Tools, and Crew. Communication follows a strict hub-and-spoke model — agents communicate only with the orchestrator, never directly with each other. A "Flows" layer provides event-driven, deterministic workflow control. Memory includes short-term, long-term, entity, and contextual tiers.

#### S1 (Operations): PRESENT

Individual agents with defined roles, goals, and backstories serve as S1 operational units. Each agent has its own tools and area of expertise, and can execute tasks autonomously within its scope. This is a clean S1 implementation.

**However:** CrewAI agents are not themselves viable systems. They have no internal S2-S5 structure. They are workers, not autonomous viable units. Beer's S1 requires that each operational element "is itself a viable system" — capable of self-regulation. CrewAI agents can execute tasks but cannot self-diagnose, self-audit, or adapt their own strategy. They depend entirely on the orchestrator for coordination. This is a **partial** S1: the units exist but lack internal viability.

#### S2 (Coordination): PARTIAL — WEAK

CrewAI's hub-and-spoke architecture means there is **no direct lateral coordination between agents**. All coordination flows through the manager/orchestrator. In sequential mode, the output of one task feeds into the next, which is pipeline coordination, not dampening. In hierarchical mode, the manager agent coordinates, but this is S3 (control), not S2 (coordination).

The task dependency mechanism (one task's output feeds another's input) provides some implicit coordination — agents don't duplicate work because the workflow is predefined. But there is no mechanism for agents to signal conflicts, detect oscillation, or mutually adjust. If two agents' outputs contradict, there is no S2 dampening — only S3 intervention from the manager.

**VSM diagnosis:** The absence of genuine S2 means CrewAI relies entirely on vertical control (S3) for what should be lateral coordination. Beer predicted this: "Without System 2, the only coordination mechanism is command from above — which lacks requisite variety." This is precisely CrewAI's architecture.

#### S3 (Control): PRESENT

The manager agent in hierarchical mode, or the Flow orchestrator, serves the S3 function: it allocates tasks, monitors progress, decides what happens next. The resource bargaining channel is partially implemented through task delegation (the manager decides which agent handles what). Performance monitoring exists through task output validation and guardrails.

**Limitation:** S3 in the VSM receives consolidated performance information and makes synoptic judgments. CrewAI's manager receives task outputs but has limited ability to assess overall system health or make cross-cutting optimization decisions. There is no equivalent of Beer's triple vector (Actuality/Capability/Potentiality) for quantifying agent performance.

#### S3\* (Audit): ABSENT

There is no independent audit mechanism in CrewAI. The manager agent evaluates task outputs, but this is S3 (control), not S3\* (audit). Beer's S3\* is specifically about bypassing normal reporting channels to verify that S1 units are not distorting information. In CrewAI, the manager relies entirely on agent outputs — it has no mechanism for independent spot-checking, no way to verify that an agent's claimed results match reality.

Guardrails (output length checks, keyword filters) are the closest analog, but these are static validation rules, not the sporadic, targeted probes that S3\* requires.

**VSM prediction:** Without S3\*, the system is vulnerable to agents reporting false success, hallucinating completed work, or producing outputs that look correct but are factually wrong. This is exactly what the multi-agent failure literature documents (Cemri et al., 2025: "incomplete verification," "incorrect verification").

#### S4 (Intelligence): ABSENT

There is no environmental scanning function in CrewAI. No agent monitors the external environment for threats, opportunities, or changing requirements. No agent maintains a model of the future. No mechanism adapts the crew's strategy based on environmental change.

A planning agent can create step-by-step plans, but this is task decomposition (S3 activity), not strategic intelligence (S4 activity). S4 should be asking: "Is our approach still appropriate? Has the environment changed? Should we reconfigure?"

**VSM prediction:** Without S4, the system becomes a rigid pipeline. Beer: "Without System 4, there is no mechanism for the organisation to learn about its future." CrewAI workflows are brittle — they execute predefined task sequences and cannot adapt when assumptions change mid-execution.

#### S5 (Policy/Identity): PARTIAL

The crew definition (the overall goal, the roles, the process type) serves a partial S5 function — it defines what the system is and what it's for. The system prompt and crew configuration provide identity and constraints.

**However:** S5's critical function is monitoring the S3-S4 homeostat and intervening when it fails. Since there is no S4, the homeostat doesn't exist. S5 also handles algedonic alerts — emergency signals from any level. CrewAI has no algedonic channel. If an agent encounters a catastrophic failure, there is no bypass mechanism to escalate directly to the top.

#### Failure Modes VSM Predicts for CrewAI

1. **Oscillation from missing S2:** When agents produce contradictory outputs with no lateral coordination, the system either ignores the contradiction (if sequential) or the manager thrashes trying to resolve it (variety overload on S3).
2. **Silent failure from missing S3\*:** Agents hallucinate work or produce subtly wrong outputs that pass guardrails. Errors compound silently.
3. **Brittleness from missing S4:** Any change in requirements, tool availability, or environmental conditions causes total failure because no component is scanning for change.
4. **S3 overload:** Because S2 is absent, S3 (the manager) handles all coordination. This violates variety balance — the manager becomes a bottleneck, especially as crew size grows.

---

### 2.2 LangGraph

**Architecture summary:** LangGraph models agents as nodes in a directed graph, connected by edges that represent control flow and data handoff. State is centralized and persistent (reducer-driven schemas). Supports checkpointing, human-in-the-loop, subgraph composition, and multiple coordination patterns (sequential, supervisor, scatter-gather, pipeline parallel). Explicitly designed as a state machine for agent workflows.

#### S1 (Operations): PRESENT

Agent nodes in the graph serve as S1 operational units. Each node can be a complete agent with its own tools and logic, or a simpler function. Subgraph composition allows grouping related agents — a subgraph can be treated as a single node at a higher level.

**Closer to VSM than CrewAI:** Subgraph composition is structurally close to VSM recursion. A subgraph is itself a graph (potentially with its own supervisor, state, and coordination patterns), embedded as a node within a larger graph. This is the beginning of "each S1 unit is itself a viable system."

**Still partial:** Individual agent nodes are typically not structured as complete viable systems internally. They are functions or tool-calling agents, not self-regulating entities with their own coordination and audit.

#### S2 (Coordination): PARTIAL

LangGraph's centralized state provides an implicit coordination mechanism — all nodes read and write to shared state, which prevents some forms of conflict (at least at the data level). The reducer pattern ensures that concurrent state updates are merged deterministically rather than overwritten.

This is closer to **stigmergic coordination** than to Beer's S2. Agents coordinate through the shared medium (state) rather than through direct lateral channels. The state serves as an external trace that subsequent agents respond to.

**What's missing:** There is no explicit dampening mechanism. If two agents in a scatter-gather pattern produce conflicting results, the state reducer merges them according to predefined rules — but there is no mechanism to detect the conflict, signal it, and dampen the oscillation. The reducer is a mechanical merge, not an intelligent dampener. Beer's S2 also requires "both formal reporting and informal networks" — LangGraph provides the formal state but not the informal channels.

#### S3 (Control): PRESENT

The supervisor pattern is a direct implementation of S3. A supervisor node routes tasks to worker nodes, monitors their outputs, and can redirect work based on results. Resource allocation is implicit in routing decisions (which agent handles which task).

LangGraph's checkpointing and execution history provide the consolidated performance information that S3 needs. The state system maintains a record of which nodes were visited and what changes were made — this is S3's information base.

**Stronger than CrewAI's S3:** The explicit state schema means S3 (the supervisor or graph logic) has structured, typed information about system state, not just agent output text. The evaluator-optimizer pattern (one agent produces, another evaluates, loop until acceptable) implements the S3 performance monitoring function.

#### S3\* (Audit): PARTIAL

LangGraph's checkpointing system provides a foundation for audit — you can inspect any point in the workflow's execution, replay from checkpoints, and examine state changes. LangSmith (the observability platform) adds tracing and evaluation capabilities.

This is closer to S3\* than anything in CrewAI or AutoGen, but it is **passive** audit infrastructure, not **active** audit behavior. Beer's S3\* actively probes S1 operations — it doesn't just log what happened, it independently verifies that what was reported matches reality. LangGraph provides the pipes for audit but not the auditor.

**A developer could implement S3\* by adding:** A dedicated audit node that periodically samples the outputs of other nodes and independently verifies them (e.g., re-executing a subset of work, checking facts against external sources). But this would be a custom addition, not a framework feature.

#### S4 (Intelligence): ABSENT

Like CrewAI, LangGraph has no built-in environmental scanning or strategic adaptation function. The graph structure is defined at design time. While conditional edges allow runtime routing decisions, these are reactive (responding to current state) rather than strategic (anticipating future needs).

A developer could add an S4-like node that monitors external conditions and modifies the graph's routing — LangGraph's dynamic edge capability supports this. But the framework provides no primitives for it.

#### S5 (Policy/Identity): PARTIAL

The graph definition itself — what nodes exist, how they're connected, what state they share, what termination conditions apply — serves as S5. It defines the system's identity and constraints. Human-in-the-loop integration allows policy-level intervention (a human can inspect state and redirect the workflow).

**Closer to S5 than CrewAI:** The checkpointing and pause/resume capability means a human (or higher-level system) can inspect the S3-S4 state and intervene — which is part of S5's function. But this requires active human monitoring; there is no automatic S5 alerting mechanism.

**No algedonic channel:** There is no built-in emergency escalation that bypasses normal processing. If a node fails catastrophically, the error propagates through the graph's normal edge logic, not through a dedicated bypass channel.

#### Failure Modes VSM Predicts for LangGraph

1. **Graph rigidity from missing S4:** The graph is defined at design time. If the task environment changes (new tools needed, changed requirements, unexpected failure patterns), the graph cannot adapt. This is the "optimizes until obsolete" pathology.
2. **Conflict accumulation from weak S2:** The state reducer handles data conflicts mechanically but cannot detect semantic conflicts between agent outputs. Two agents may produce individually valid but jointly inconsistent results, and the reducer will merge them without recognizing the problem.
3. **Supervisor bottleneck:** The supervisor pattern concentrates all routing decisions in one node, creating a variety bottleneck identical to CrewAI's S3 overload.
4. **Silent failure from passive audit:** Checkpointing records what happened but doesn't verify it was correct. Post-hoc audit (reviewing logs) catches problems too late.

---

### 2.3 AutoGen

**Architecture summary:** AutoGen (v0.4, now merging into Microsoft Agent Framework) uses asynchronous messaging between agents. Core patterns: two-agent chat, sequential chat, group chat (orchestrated by GroupChatManager with speaker selection strategies), nested chat, and swarm. Three-layer architecture: Core (messaging, lifecycle), AgentChat (group chat, pre-built agents), Extensions (integrations). Key innovation: conversational multi-agent patterns where agents "talk" to solve problems.

#### S1 (Operations): PRESENT

Individual agents (AssistantAgent, UserProxyAgent, custom agents) are S1 units. Each has defined capabilities, tools, and roles. The swarm pattern allows agents to hand off tasks to each other based on capability, which is closer to S1 autonomous action than CrewAI's strict delegation.

**AutoGen's key difference:** Agents can communicate more freely than in CrewAI. In group chat, all agents share context and can respond based on the conversation. This gives S1 units more autonomy — they can volunteer responses, challenge other agents, and contribute without being explicitly delegated to.

**Still not recursively viable:** Like the other frameworks, individual agents are not structured as viable systems internally.

#### S2 (Coordination): PARTIAL — BEST OF THE THREE

AutoGen's group chat pattern provides the closest analog to S2 in any current framework. In group chat, all agents share a single conversation thread. They can see each other's outputs and respond accordingly. The GroupChatManager selects speakers, but agents can observe and react to each other's contributions.

This is **partial lateral coordination**. The shared conversation thread allows agents to detect potential conflicts ("I disagree with Agent A's analysis because..."), adjust their behavior based on what others have done, and build on each other's work. This is significantly closer to Beer's "informal networks" and "mutual adjustment protocols" than CrewAI's hub-and-spoke or LangGraph's shared state.

**What's still missing:** The GroupChatManager's speaker selection is still centralized — an agent cannot interrupt or take the floor autonomously. The coordination is **conversational** (agents talk about conflicts) rather than **structural** (a dedicated dampening mechanism). There is no component whose explicit purpose is oscillation dampening.

The nested chat pattern adds another dimension: side conversations can occur for specialized coordination without polluting the main thread. This is structurally interesting — it resembles S2's "regulatory centres for each S1 element."

#### S3 (Control): PRESENT

The GroupChatManager serves the S3 function: it selects speakers, manages the conversation flow, and determines when the group chat terminates. Speaker selection strategies (auto, manual, round-robin, random) are S3 control policies.

In the SelectorGroupChat pattern (v0.4), an LLM-based selector dynamically chooses the next agent based on conversation context. This is more sophisticated than static routing — the S3 function is itself intelligent and context-aware.

**Limitation:** S3's resource bargaining channel (negotiating resources with S1 units) has no equivalent. There is no mechanism for an agent to request more compute, a larger context window, or access to additional tools at runtime.

#### S3\* (Audit): ABSENT

AutoGen has no built-in audit mechanism that bypasses normal conversation channels. The GroupChatManager sees all messages, but it is the same entity that manages the conversation — it has no independent verification channel.

AutoGen's "self-criticism" capability (an agent evaluating its own output) is explicitly **not** S3\*. Beer's entire point with S3\* is that the audit must be independent of the audited system. Self-evaluation fails precisely because the evaluator shares the same biases and blindspots as the producer.

#### S4 (Intelligence): ABSENT

No environmental scanning or strategic adaptation function. The group chat pattern is focused on the current task, not on monitoring external conditions or planning for future adaptation.

#### S5 (Policy/Identity): PARTIAL

The initial prompt, agent definitions, and termination conditions define system identity and constraints. The UserProxyAgent (in human-in-the-loop mode) can serve an S5 function — a human monitoring the conversation and intervening when agents deviate from purpose.

**Interesting structural feature:** AutoGen's termination conditions (text mentions, max messages, timeout, token usage) are a rudimentary form of homeostatic bounds — the system maintains essential variables (cost, length, time) within viable limits. This is not full S5, but it is more than the other frameworks offer as built-in behavior.

#### Failure Modes VSM Predicts for AutoGen

1. **Conversational drift (goal drift):** The shared conversation thread is both a strength (S2 coordination) and a risk. Without strong S5 identity maintenance, agents can drift off-topic through emergent conversational dynamics. This is exactly the "goal drift" failure documented in the literature.
2. **GroupChatManager bottleneck:** Like the other frameworks' supervisors, the manager is a variety bottleneck. As group size grows, speaker selection becomes increasingly difficult.
3. **No adaptation:** Missing S4 means the system cannot adjust its approach mid-task if conditions change.
4. **Echo chambers:** Without S3\* audit, agents in group chat may reinforce each other's errors. If Agent A hallucinates a fact and Agent B builds on it, Agent C may accept it as established truth. The shared context becomes a vehicle for error propagation rather than error correction.

---

## 3. Comparative Table

| VSM System | Function | CrewAI | LangGraph | AutoGen |
|------------|----------|--------|-----------|---------|
| **S1 (Operations)** | Autonomous operational units | **Present** (role-based agents, but not internally viable) | **Present** (agent nodes, subgraph recursion possible) | **Present** (agents with more conversational autonomy) |
| **S2 (Coordination)** | Lateral dampening, anti-oscillation | **Absent** (hub-and-spoke only; no lateral channels) | **Partial** (shared state as stigmergic medium; no active dampening) | **Partial** (shared conversation thread; closest to mutual adjustment) |
| **S3 (Control)** | Internal management, resource allocation | **Present** (manager agent, Flows) | **Present** (supervisor node, evaluator-optimizer) | **Present** (GroupChatManager, speaker selection) |
| **S3\* (Audit)** | Independent verification | **Absent** (guardrails are static, not sporadic probes) | **Partial** (checkpointing/tracing provides audit infrastructure, not auditor) | **Absent** (no independent verification channel) |
| **S4 (Intelligence)** | Environmental scanning, strategic adaptation | **Absent** | **Absent** | **Absent** |
| **S5 (Policy/Identity)** | Identity, closure, S3-S4 balance | **Partial** (crew definition provides identity; no homeostat, no algedonic) | **Partial** (graph definition + HITL; closer to S5 intervention) | **Partial** (termination conditions as homeostatic bounds; HITL) |
| **Algedonic Channel** | Emergency bypass escalation | **Absent** | **Absent** | **Absent** |
| **Recursion** | Self-similar at every level | **Absent** (agents are flat, not nested viable systems) | **Partial** (subgraph composition enables structural nesting) | **Absent** (nested chat is functional nesting, not structural) |
| **Variety Engineering** | Explicit attenuator/amplifier design | **Absent** (implicit through role scoping) | **Absent** (implicit through state schema) | **Absent** (implicit through agent specialization) |

### Summary Verdict

- **All three frameworks are strongest at S1 and S3.** They all provide worker agents and some form of central control. This makes sense: operations and control are the most obvious requirements.
- **All three frameworks are weakest at S4.** None has any built-in environmental scanning or strategic adaptation. This is the most universal gap.
- **S2 is the most variable.** AutoGen's group chat provides the best approximation; CrewAI's hub-and-spoke provides the worst.
- **S3\* is absent or nearly so everywhere.** This is arguably the most dangerous gap — it means all three frameworks are vulnerable to agents reporting false success.
- **No framework implements algedonic signals, recursion (in the VSM sense), or explicit variety engineering.**

---

## 4. What Would a VSM-Compliant Multi-Agent Framework Look Like?

Drawing on the analysis above, here is an architectural sketch.

### Layer 0: Viable Agent (The Recursive Unit)

Every agent is a viable system internally. Not just a tool-calling wrapper around an LLM, but a unit with:
- **Internal S1:** The agent's execution capability (LLM calls, tool use)
- **Internal S2:** Self-coordination across subtasks (preventing internal oscillation, e.g., not flip-flopping between approaches)
- **Internal S3:** Self-monitoring (tracking its own token budget, error rate, progress toward goal)
- **Internal S3\*:** Ability to spot-check its own outputs against external ground truth (not self-critique, but verification against an independent source — retrieval from a knowledge base, execution of tests, comparison with known-correct examples)
- **Internal S4:** Awareness of its own limitations and context (monitoring whether its tools are working, whether the environment has changed since it started)
- **Internal S5:** Adherence to its role identity and constraints

This is the unit of recursion. The same structure appears at every level.

### Layer 1: The Operational Crew (S1 Assembly)

Multiple viable agents working on a shared task. Each has genuine autonomy within its domain. The crew-level structure:

- **S1:** The individual viable agents
- **S2:** A coordination protocol — not a manager, but a shared medium + dampening rules:
  - Shared state (stigmergic medium) that all agents read/write
  - Conflict detection: a lightweight process that monitors shared state for contradictions (Agent A says X, Agent B says not-X)
  - Dampening: when conflicts are detected, the conflicting agents are notified and given a window to resolve laterally before escalation
  - This could be implemented as a dedicated "coordinator" agent that watches the shared state but has no command authority — only the ability to flag conflicts and facilitate resolution
- **S3:** An oversight process that:
  - Allocates resources (which agent gets how much compute budget)
  - Monitors performance using Beer's triple vector: Actuality (what agents have produced), Capability (what they could produce given resources), Potentiality (what is demanded by the task)
  - Intervenes only when S2 coordination fails (i.e., conflicts persist after the S2 window expires)
- **S3\*:** An independent audit agent that:
  - Is a different LLM (or at minimum, a different prompt/temperature/approach) from the operational agents
  - Sporadically samples agent outputs and verifies them against independent criteria
  - Reports directly to S3, bypassing the agents' own reporting
  - Operates on a schedule or trigger (not continuous — that would destroy autonomy)
- **S4:** An intelligence agent that:
  - Monitors task progress against changing requirements
  - Scans for environmental changes (new data available, tools broken, user feedback indicating changed needs)
  - Proposes strategy adaptations to S3 (not commands — proposals that S3 evaluates against internal capability)
  - Maintains a model of the task environment
- **S5:** The policy layer:
  - Defined by the human user's goals, constraints, and values
  - Monitors the S3-S4 interaction (is the crew both executing effectively AND adapting appropriately?)
  - Has access to an algedonic channel: any agent can fire an emergency signal (e.g., "I've encountered something dangerous/illegal/fundamentally misaligned") that bypasses S3 and goes directly to S5 (which may be a human)
  - Defines termination conditions, success criteria, and identity constraints

### The Seven Channels (Implemented)

| VSM Channel | Implementation |
|-------------|---------------|
| Resource bargaining (S3 ↔ S1) | Agents can request more tokens/tools; S3 evaluates and grants or denies |
| Command (S3 → S1) | Direct task assignment when S2 coordination fails |
| S2 coordination | Shared state + conflict detection + dampening window |
| S3\* audit | Independent verification agent with direct channel to S3 |
| Lateral S1-to-S1 | Agents can read each other's outputs in shared state (stigmergic) and, in some patterns, communicate directly |
| Environment-to-S1 | Each agent has its own tools and environmental connections |
| Algedonic | Emergency signal from any agent → S5 (human), with timeout-based escalation |

### Tiered Intelligence (per Gorelkin)

Not every VSM function needs a frontier model:
- **S2 coordination:** Small/fast model or rule-based (conflict detection is pattern matching, not deep reasoning)
- **S3 control:** Medium model (resource allocation, performance assessment)
- **S3\* audit:** Frontier model or specialized verifier (audit requires independent judgment)
- **S4 intelligence:** Frontier model (environmental scanning requires sophisticated reasoning)
- **S5 policy:** Human + frontier model advisory

### Recursion in Practice

The entire crew (Layer 1) can be embedded as a single S1 unit within a larger system. A research project might have:
- **Recursion level 0:** Project coordinator (with its own S1-S5)
- **Recursion level 1:** Research crew, Writing crew, Review crew (each is an S1 unit at level 0, but internally has the full Layer 1 structure)
- **Recursion level 2:** Within the Research crew, individual research agents (each is a viable agent per Layer 0)

The Law of Cohesion governs cross-recursion variety balance: the variety accessible to the project coordinator's S3 from each crew must equal the metasystemic variety within each crew.

---

## 5. Honest Assessment: Where VSM Does Not Fit

The VSM is not a perfect lens for multi-agent frameworks. Here is where it falls short or misleads.

### 5.1 VSM Assumes Long-Lived Systems; Most Agent Runs Are Ephemeral

The VSM was designed for organizations that must survive indefinitely. Most multi-agent executions are ephemeral — they run for seconds to hours, complete a task, and terminate. The viability question ("can this system survive in a changing environment?") barely applies to a crew that exists for 30 seconds to write a report.

**Consequence:** S4 (environmental scanning) and S5 (identity maintenance) are less critical for short-lived agent runs than the VSM suggests. The S4 gap matters most for long-running autonomous agents; for a quick task execution, it may genuinely not matter.

### 5.2 VSM Does Not Account for the LLM Substrate

The VSM was designed for organizations of humans and machines. LLM-based agents have properties no human organization has:
- **Instantaneous cloning:** You can spin up identical agents at will. VSM has no concept of this.
- **Shared weights:** All agents may share the same LLM, meaning S1 units are not truly independent — they share biases, knowledge gaps, and failure modes. Beer's S1 assumes independent operational units with distinct capabilities. When all agents are GPT-4 with different prompts, the independence is superficial.
- **Context window as hard constraint:** The VSM's variety engineering assumes you can always design better attenuators and amplifiers. The context window is a fixed information bottleneck with no organizational analog.
- **Hallucination:** The VSM assumes S1 units may distort information deliberately or accidentally (hence S3\*). But hallucination is qualitatively different — the agent believes false things about its own capabilities and the world. This is not organizational politics; it is a property of the computational substrate that the VSM was never designed to handle.

### 5.3 VSM Assumes Stable Identity; Agents Are Stateless

Beer's S5 defines an enduring identity — "what the organization IS." Agents typically have no persistent identity across runs. Their "identity" is a system prompt that can be changed by anyone at any time. The VSM's concept of identity-as-closure (the system produces and maintains its own identity) does not apply to entities whose identity is externally assigned and reset every session.

### 5.4 VSM Does Not Model the Cost of Communication

In human organizations, communication channels have operational costs (meetings, reports, management overhead) but these are roughly fixed per channel. In LLM-agent systems, every communication is an LLM call with token costs that scale with message length. The O(n^2) cost problem (documented in the AutoGPT failure analysis) has no VSM equivalent. Beer never had to ask "is this coordination channel worth its token cost?"

### 5.5 VSM Does Not Address the Single-Model Bottleneck

When a "manager" agent, a "worker" agent, and an "auditor" agent are all the same LLM with different prompts, you don't actually have independent systems. The audit agent (S3\*) cannot genuinely independently verify the worker agent's output if both share the same reasoning patterns, knowledge, and biases. This is a fundamental problem that the VSM does not address because it assumes structurally distinct components.

### 5.6 VSM Under-Specifies the Coordination Mechanism

Beer says S2 should "dampen oscillation" and provides examples (schedules, shared information systems, mutual adjustment). But he does not specify *how* — what data structures, what protocols, what algorithms. For human organizations, this is fine (humans figure out how to coordinate). For software systems, this gap means the VSM tells you *that* you need S2 but not *how to build it*. The stigmergy literature, the distributed systems literature, and the MARL literature provide the "how" that the VSM lacks.

### 5.7 Aspects of Frameworks the VSM Does Not Account For

- **Prompt engineering and in-context learning:** The VSM has no concept of how agents are programmed or learn within a session.
- **Tool composition:** How agents combine tools to solve novel problems is not covered by the VSM's variety framework in a useful way.
- **Benchmarking and evaluation:** The VSM provides viability criteria but not task-performance metrics. The framework comparison question "which one gets better benchmark scores?" is outside the VSM's scope.
- **Developer experience:** The VSM says nothing about API design, debugging tools, or ease of use — factors that dominate practical framework choice.
- **Token economics and latency:** The real-world constraints of cost and speed are not part of the VSM's variety calculus.

### 5.8 The Teleological Gap

The VSM assumes the system has a purpose (POSIWID). But who defines the purpose for a multi-agent system? In a corporation, purpose emerges from stakeholders, history, and environment. In an agent framework, purpose is specified by the developer for each run. The VSM's treatment of purpose-as-emergent doesn't map onto purpose-as-specified.

---

## Summary of Findings

1. **All three frameworks are S1/S3 heavy.** They provide operational agents and centralized control but neglect coordination (S2), audit (S3\*), intelligence (S4), and full policy/identity (S5). This is not accidental — S1 and S3 are the most obvious needs when building multi-agent systems.

2. **S4 (Intelligence) is universally absent.** No framework has built-in environmental scanning or strategic adaptation. This is the biggest structural gap from a VSM perspective, and it predicts the brittleness that the multi-agent failure literature documents.

3. **S3\* (Audit) is the most dangerous gap.** Without independent verification, all three frameworks are vulnerable to the compounding hallucination problem: agents report false success, errors accumulate silently, and the system produces elaborate fictions that pass surface-level validation.

4. **The algedonic channel is missing everywhere.** No framework has a dedicated emergency bypass escalation mechanism. Error handling goes through normal channels, which means critical failures can be delayed or attenuated by intermediate layers.

5. **VSM recursion maps best onto LangGraph's subgraph composition.** Only LangGraph provides a structural mechanism (subgraphs) that approximates the recursive nesting the VSM requires.

6. **The VSM is genuinely useful as an architectural diagnostic** — it identifies specific, named gaps (S2, S3\*, S4, algedonic) with corresponding failure mode predictions. But it must be used with awareness of its limitations (Section 5), particularly the ephemeral nature of agent runs, the shared-model problem, and the cost of communication.

---

## Sources

### VSM and Cybernetics
- Beer, S. (1972/1981). *Brain of the Firm*. Wiley.
- Beer, S. (1979). *The Heart of Enterprise*. Wiley.
- Beer, S. (1984). "The Viable System Model: Its Provenance, Development, Methodology and Pathology." *JORS*, 35(1), 7-25.
- Gorelkin, M. (2025). "Stafford Beer's Viable System Model for Building Cost-Effective Enterprise Agentic Systems." Medium.
- Herring & Kaplan (2000). "The Viable System Model for Software." SCI'2000.

### Multi-Agent Failure Literature
- Cemri, M. et al. (2025). "Why Do Multi-Agent LLM Systems Fail?" arXiv:2503.13657.

### Framework Documentation
- CrewAI: https://docs.crewai.com/
- LangGraph: https://www.langchain.com/langgraph
- AutoGen: https://microsoft.github.io/autogen/ (now Microsoft Agent Framework)

### Stigmergy
- Heylighen, F. (2016). "Stigmergy as a Universal Coordination Mechanism." *Cognitive Systems Research*, 38.
