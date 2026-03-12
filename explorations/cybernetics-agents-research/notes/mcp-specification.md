# Anthropic Model Context Protocol (MCP) Specification

## Source
- Specification: https://modelcontextprotocol.io/specification/2025-11-25
- Announced: November 2024 by Anthropic
- Major update: November 2025
- Donated to Linux Foundation's Agentic AI Foundation (AAIF), December 2025
- Schema source: https://github.com/modelcontextprotocol/specification/blob/main/schema/2025-11-25/schema.ts

## What MCP Is

An open protocol for standardizing how LLM applications integrate with external data sources and tools. Uses JSON-RPC 2.0 messages. Inspired by the Language Server Protocol (LSP), which standardized programming language support across IDEs. MCP does the analogous thing for AI application integrations.

## Architecture: Client-Host-Server

Three-tier model:

- **Host**: The LLM application (e.g., Claude Desktop, an IDE). Creates/manages multiple clients. Coordinates AI/LLM integration. Enforces security policies and user consent. Aggregates context across clients.
- **Client**: Created by the host, maintains isolated 1:1 connection with a server. Handles protocol negotiation, capability exchange, message routing, subscriptions.
- **Server**: Provides context and capabilities. Exposes resources, tools, and prompts. Can be local processes or remote services. Operates independently with focused responsibilities.

Key isolation property: **Servers cannot see the full conversation, nor can they see into other servers.** The host mediates all cross-server interactions.

## Protocol Layers

Built on JSON-RPC 2.0 with stateful sessions. Capability negotiation at initialization -- both client and server declare what they support. Features are progressively addable.

## Server Features (What Servers Expose)

### 1. Tools (Model-Controlled)
Functions the LLM can discover and invoke autonomously. The LLM decides when to use them based on context.

Tool definition schema:
- `name`: unique identifier (1-128 chars, case-sensitive)
- `description`: human-readable
- `inputSchema`: JSON Schema for parameters
- `outputSchema`: optional JSON Schema for structured results
- `annotations`: metadata about behavior (untrusted unless from trusted server)

Invocation flow:
1. Client sends `tools/list` to discover tools
2. LLM selects tool to use
3. Client sends `tools/call` with name + arguments
4. Server returns result (text, image, audio, resource links, embedded resources)
5. Server can notify `tools/list_changed` when tool set changes

Two error types:
- Protocol errors (JSON-RPC): malformed requests, unknown tools
- Tool execution errors (`isError: true`): API failures, validation errors. These are fed back to the LLM for self-correction.

### 2. Resources (Application-Controlled)
Contextual data attached and managed by the client. Example: file contents, git history. Not directly invoked by the LLM -- the application decides what to attach.

### 3. Prompts (User-Controlled)
Pre-defined templates invoked by user choice. Example: slash commands, menu options.

## Client Features (What Clients Expose to Servers)

### 1. Sampling
Servers can request LLM completions from the client. This is what enables **nested agentic loops**: a server can run its own agent loop using the client's LLM access, while the user retains control.

Flow:
1. Server sends `sampling/createMessage` with messages + optional tools
2. Client presents request to user for approval (human-in-the-loop)
3. Client forwards to LLM
4. LLM responds (possibly with tool_use)
5. Client presents response to user for review
6. Client returns approved response to server

Model preferences use abstract priorities (cost, speed, intelligence on 0-1 scale) plus optional model hints (substring matching). This decouples servers from specific model names.

Supports multi-turn tool loops: server receives tool_use response, executes tools, sends results back in new sampling request. Can iterate until done.

### 2. Roots
Filesystem boundaries. Servers can ask what directories/files they have access to. Must be `file://` URIs.

### 3. Elicitation
Server-initiated requests for additional information from users.

## Cybernetic Analysis: Tool Use as Variety Amplification

### Ashby's Law of Requisite Variety
The fundamental cybernetic insight: a controller must have at least as much variety as the system it seeks to control. An LLM alone has limited variety -- it can only produce text. Its action space is constrained to language generation.

### MCP as Variety Amplifier
MCP dramatically amplifies the LLM's variety through tool access:

1. **Expanding the action space**: Each tool adds new possible actions (query a database, call an API, write a file, execute code). The LLM's effective variety grows multiplicatively with each tool added.

2. **Dynamic variety through discovery**: Tools are not fixed at design time. The `tools/list` + `tools/list_changed` mechanism means the available variety can change during a session. New tools can appear, old ones disappear. This is adaptive variety -- the system's action repertoire evolves.

3. **Composability as variety multiplication**: Because servers are independent and composable, variety grows combinatorially. N servers with M tools each gives N*M available actions, plus combinations.

4. **Recursive variety through sampling**: The sampling feature creates recursive variety amplification. A server can request LLM completions, which can use tools, which can trigger more sampling. This is a positive feedback loop on variety.

### Variety Attenuation (The Control Side)
MCP also provides variety attenuation -- reducing the space of actions to manageable levels:

1. **Capability negotiation**: Only declared capabilities are available. This constrains variety to what's been explicitly permitted.

2. **Human-in-the-loop**: Sampling requires user approval. Every tool invocation SHOULD require user confirmation. This is a critical variety attenuator -- the human filters the LLM's proposed actions.

3. **Server isolation**: Servers can't see each other or the full conversation. This constrains the information available for action selection -- a form of information-theoretic variety attenuation.

4. **Root boundaries**: Filesystem access is constrained to declared roots. Explicit variety limitation.

5. **Security constraints**: Input validation, access controls, rate limiting, output sanitization. Each is a variety attenuator.

### The Regulator-System Balance
MCP's architecture embodies Ashby's Law structurally:
- Tools amplify variety to match the complexity of the tasks (requisite variety for the environment)
- Capability negotiation, human approval, and isolation attenuate variety to maintain control (requisite variety for safety)

The balance between these is the core design tension. Too much attenuation (too many approvals, too few tools) and the system is ineffective. Too much amplification (unrestricted tool access, no oversight) and the system is unsafe.

### Connection to Good Regulator Theorem
MCP tools effectively extend the LLM's model of the world. The Good Regulator Theorem says every good regulator must contain a model of the system it regulates. Tools provide:
- **Sensing**: Resources and tool outputs give the LLM information about external systems
- **Acting**: Tool invocations let the LLM modify external systems
- **Modeling**: The tool descriptions (inputSchema, outputSchema, annotations) give the LLM a model of what each tool does

This is exactly the sense-model-act loop that cybernetics identifies as fundamental to regulation.

### The Tiered Control Hierarchy
The Host-Client-Server architecture maps onto a hierarchical control structure:
- **Host** = meta-controller (policy, security, coordination) -- analogous to Beer's System 5/4/3
- **Client** = operational controller (message routing, capability management) -- analogous to System 2
- **Server** = operational unit (focused capability) -- analogous to System 1

The host controls what the client can do; the client mediates what servers can access. This is recursive hierarchical control.

### MCP as a Conversation in Pask's Sense
The protocol is fundamentally conversational:
- Capability negotiation = establishing a shared language
- Tool discovery = learning the other's repertoire
- Tool invocation = making a request in that shared language
- Tool results = responding in that language
- Sampling = reversing the direction of conversation (server asks client)

This maps closely onto Pask's Conversation Theory: two participants constructing shared understanding through cyclical exchange.

## Key Design Decision: "Servers Should Be Easy to Build"
The complexity is pushed to the host/client side. Servers are simple, focused, composable. This is a deliberate asymmetry: the controller (host) absorbs complexity so that the operational units (servers) can remain simple. This follows the cybernetic principle that the controller must have requisite variety, not the controlled elements.

## Security Concerns (Noted)
- Prompt injection vulnerabilities
- Tool description spoofing (lookalike tools)
- Data exfiltration through tool permissions
- Most MCP servers found to lack authentication (Knostic scan, July 2025)
- Tool annotations are untrusted by default

These are failures of variety attenuation -- the system allows more variety than it can safely control.
