# Anthropic MCP Specification: Cybernetic Analysis

## Source
- Model Context Protocol Specification (2025-11-25 revision)
- https://modelcontextprotocol.io/specification/2025-11-25
- Originally released by Anthropic, November 2024
- Donated to Agentic AI Foundation (Linux Foundation), December 2025

## What MCP Is

MCP is an open protocol standardizing how LLM applications integrate with external data sources and tools. It uses JSON-RPC 2.0 for communication between three roles:

- **Hosts**: LLM applications that initiate connections (the container process)
- **Clients**: Connectors within the host, each maintaining a 1:1 session with a server
- **Servers**: Services providing context and capabilities

Inspired by Language Server Protocol (LSP) for IDE tooling. The analogy is deliberate: LSP standardized programming language support across editors; MCP standardizes tool/context integration across AI applications.

## Architecture: Client-Host-Server

The host process creates and manages multiple client instances. Each client has one stateful session with one server. This is a strict isolation model:

- Servers cannot see the full conversation
- Servers cannot see into other servers
- Cross-server interactions are mediated by the host
- The host enforces all security boundaries

This maps directly to **Ashby's Law of Requisite Variety** in an interesting way: the host is the regulator, and the client-server isolation creates controlled channels of variety.

## Three Server Primitives

| Primitive | Control | Description |
|-----------|---------|-------------|
| **Prompts** | User-controlled | Templates invoked by user choice (slash commands, menus) |
| **Resources** | Application-controlled | Contextual data attached by the client (files, git history) |
| **Tools** | Model-controlled | Functions the LLM can invoke to take actions |

This is a hierarchy of control: user > application > model. The cybernetic significance is that it's a **layered variety management system**. Each layer has different requisite variety:
- Users have highest variety (can choose any prompt)
- Applications filter/curate (resource selection)
- Models have constrained variety (can only call defined tools)

## Tools as Variety Amplification

Tools are the most cybernetically interesting primitive. The tool specification defines:

```json
{
  "name": "tool_name",
  "description": "Human-readable description",
  "inputSchema": { /* JSON Schema for parameters */ },
  "outputSchema": { /* Optional: expected output structure */ },
  "annotations": { /* Metadata about behavior */ }
}
```

### Discovery and Invocation Flow
1. Client sends `tools/list` -> Server returns available tools
2. LLM selects tool based on contextual understanding
3. Client sends `tools/call` with arguments -> Server executes -> returns result
4. Server can notify `tools/list_changed` when available tools change

### Cybernetic Analysis: Tool Use as Variety Amplification

From Ashby's perspective, an LLM without tools is a **variety-limited regulator**. It can only produce text. Adding tools amplifies the model's variety of possible actions:

- Without tools: variety = {text outputs}
- With tools: variety = {text outputs} x {tool_1 actions} x {tool_2 actions} x ... x {tool_n actions}

Each tool is a **channel of requisite variety** that the model can activate. The JSON Schema input constraints on each tool bound the variety per channel -- you can't call `get_weather` with arbitrary parameters, only those matching the schema. This is **variety attenuation** applied to each amplification channel.

The `listChanged` notification mechanism is a **feedback loop**: the environment (server) signals that available variety has changed, and the system adapts.

### Error Handling as Negative Feedback

Two types of errors:
1. **Protocol errors** (malformed requests) -- structural failures, the channel itself is broken
2. **Tool execution errors** (`isError: true`) -- actionable feedback the LLM can use to self-correct

Tool execution errors are explicitly designed as negative feedback for the model: "Clients SHOULD provide tool execution errors to language models to enable self-correction." This is a textbook **error-controlled regulator** -- the system detects deviation from desired output and corrects.

## Sampling: Recursive Variety

The sampling feature allows servers to request LLM completions from the client. This is the inverse flow: instead of the model calling tools on the server, the server calls the model through the client.

Key design:
- Server sends `sampling/createMessage` with messages, model preferences, optional tools
- Client mediates: presents to user for approval, forwards to LLM, returns result
- **Human-in-the-loop is required**: user must approve prompts and review results
- Server can specify model preferences (cost/speed/intelligence priorities) and hints

### Agentic Loops via Sampling + Tools

The November 2025 update added tools-in-sampling: servers can request LLM completions that include tool definitions. This enables:
1. Server requests LLM sampling with tools
2. LLM returns tool_use (stopReason: "toolUse")
3. Server executes tools, sends results back in new sampling request
4. LLM processes results, may request more tools or produce final answer

This creates **recursive agentic loops** where MCP servers can run their own agent cycles using the client's LLM access. From a cybernetics perspective, this is **recursion in the variety management hierarchy** -- the server becomes a second-order regulator, using the model as its own variety amplifier.

## Capability Negotiation as Structural Coupling

During initialization, clients and servers exchange capability declarations:
- Server declares: tools, resources, prompts, subscriptions
- Client declares: sampling, roots, elicitation

This is **structural coupling** in the Maturana/Varela sense: two systems establishing the parameters of their interaction domain. Neither system dictates to the other; they negotiate a shared interface. The protocol is explicitly designed for progressive feature addition -- you start minimal and add capabilities as needed.

## Security Model: Variety Attenuation

The security principles are fundamentally about **constraining variety**:
1. Users must consent to data access (attenuating information flow)
2. Servers cannot see full conversations (attenuating context variety)
3. Tool invocations require human approval (attenuating action variety)
4. Roots define filesystem boundaries (attenuating spatial variety)
5. Servers are isolated from each other (preventing variety leakage between channels)

The human-in-the-loop requirement for both tool calls and sampling is a **metacontrol mechanism** -- the human operates at a higher logical level, approving or denying the system's proposed actions.

## Cybernetic Significance

MCP is, perhaps unintentionally, a practical implementation of several cybernetic principles:

1. **Requisite Variety (Ashby)**: Tools amplify model variety to match environmental complexity; schemas attenuate each channel
2. **Error-controlled regulation**: Tool errors as negative feedback for self-correction
3. **Recursive structure**: Sampling-with-tools creates nested regulatory loops
4. **Structural coupling**: Capability negotiation establishes interaction domains
5. **Variety attenuation for safety**: Security model is systematic variety reduction

What MCP does NOT address from a cybernetic perspective:
- No homeostatic goals or setpoints -- tools are invoked for arbitrary purposes
- No viability criteria -- there's no notion of system health or survival
- No autonomy -- servers are entirely reactive, they don't self-organize
- No model of the environment -- servers expose capabilities but don't model what the host needs

MCP is a **channel architecture**, not an **autonomous system architecture**. It's infrastructure for variety management, not a viable system itself. To build a viable agent system on MCP, you'd need to add Beer's Systems 2-5 on top of the MCP plumbing.
