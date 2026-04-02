# Agent & LLM Contestants — Options and Choices

## The Two Axes

We're evaluating along two independent axes:

1. **Agent framework** — the reasoning loop, memory management, tool selection logic
2. **LLM backend** — the underlying language model powering the agent

These are separable. Most frameworks let you swap LLM backends. This means we can test:
- Same framework, different LLMs (isolates model quality)
- Same LLM, different frameworks (isolates agent architecture)
- Both varying (full matrix)

---

## Agent Frameworks

### 1. OpenAI Agents SDK  ← **Starting here**
- **Install**: `pip install openai-agents`
- **Repo**: github.com/openai/openai-agents-python (~19k stars)
- **Pros**:
  - Clean step-by-step control (`StopAtTools`, `max_turns=1`) — ideal for turn-based games
  - `@function_tool` decorator makes custom tools trivial
  - History management via `result.to_input_list()` for multi-turn
  - We already have `OPENAI_API_KEY` in the environment
  - Good docs, active development
- **Cons**:
  - Tied to OpenAI models (provider lock-in for this framework)
  - Relatively new, API may change
  - Less battle-tested than some alternatives
- **Verdict**: Best starting point. Lowest friction to get a real agent running in our environment.

### 2. smolagents (HuggingFace)
- **Install**: `pip install smolagents[litellm]`
- **Repo**: github.com/huggingface/smolagents (~26k stars)
- **Pros**:
  - Genuinely minimal (~1k LOC core)
  - Proper ReAct loop (think → tool → observe → repeat)
  - Model-agnostic via LiteLLM (OpenAI, Anthropic, local models, etc.)
  - `ToolCallingAgent` variant uses structured tool calls (no code execution)
  - Easy to hack on / inspect internals
- **Cons**:
  - Less clean step-by-step control than OpenAI SDK — `max_steps` controls the loop but injecting observations mid-loop is clunkier
  - `CodeAgent` (default) executes generated Python, which is overkill and risky for our use case
  - Smaller community than LangChain-based options
- **Verdict**: Strong second contestant. Add after OpenAI SDK is working.

### 3. LangGraph
- **Install**: `pip install langgraph`
- **Repo**: github.com/langchain-ai/langgraph
- **Pros**:
  - Graph-based state machine maps well to multi-agent coordination
  - Checkpointing, conditional routing
  - Large ecosystem and community
  - Model-agnostic via LangChain
- **Cons**:
  - Heavy dependency tree (LangChain)
  - Steep learning curve, lots of abstractions
  - Overkill for our needs
- **Verdict**: Maybe later. Complexity tax not worth it for MVP.

### 4. CrewAI
- **Install**: `pip install crewai`
- **Repo**: github.com/crewAIInc/crewAI (~44k stars)
- **Pros**:
  - Role-based agent design (could map to "Agent A" / "Agent B" roles)
  - Built-in delegation between agents
- **Cons**:
  - Designed for workflows (research, writing), not interactive environments
  - No concept of external observations from a game engine
  - Would be fighting the framework
- **Verdict**: Poor fit. Skip unless someone specifically requests it.

### 5. AutoGen (Microsoft)
- **Install**: `pip install autogen`
- **Repo**: github.com/microsoft/autogen (~55k stars)
- **Pros**:
  - Conversation-based multi-agent patterns — closest conceptual fit
  - Large community
- **Cons**:
  - In maintenance mode, migrating to new Microsoft Agent Framework
  - API in flux
  - Enterprise-oriented, heavy
- **Verdict**: Skip. Don't build on a framework in transition.

### 6. Pi (pi-agent-core)
- **Repo**: github.com/badlogic/pi-mono (~30k stars)
- **Pros**:
  - Extremely minimal core agent loop
  - Model-agnostic
- **Cons**:
  - TypeScript — our benchmark is Python
  - Would need subprocess wrapper or port
  - No multi-agent support
- **Verdict**: Interesting but wrong language. Revisit only if we want a TS contestant.

---

## LLM Backends

### Available now (via OPENAI_API_KEY)

| Model | Cost | Speed | Notes |
|-------|------|-------|-------|
| **gpt-4o** | Medium | Fast | Best default. Strong reasoning + tool use. |
| **gpt-4o-mini** | Low | Very fast | Good for cheap iteration during development. |
| **o1** | High | Slow | Reasoning model. Interesting to test but expensive. |
| **o3-mini** | Medium | Medium | Cheaper reasoning model. |

### Available later (need API keys)

| Model | Framework support | Notes |
|-------|-------------------|-------|
| **Claude (Anthropic)** | smolagents via LiteLLM | Would need ANTHROPIC_API_KEY |
| **Gemini (Google)** | smolagents via LiteLLM | Would need GOOGLE_API_KEY |
| **Llama / Mistral (local)** | smolagents via HfApiModel or Ollama | Free but slower. Good for reproducibility. |

---

## Chosen Approach

### Phase 1 (MVP)
- **Framework**: OpenAI Agents SDK
- **Model**: gpt-4o (primary), gpt-4o-mini (for cheap dev iteration)
- **Why**: Lowest friction, best step-by-step control, key already available.

### Phase 2 (comparison)
- **Add**: smolagents with same OpenAI models
- **Why**: Same LLM, different framework → isolates agent architecture quality.

### Phase 3 (broader eval)
- **Add**: smolagents with non-OpenAI models (Claude, Gemini, local)
- **Why**: Full matrix of framework × model combinations.

---

## Test Matrix (eventual)

```
                    gpt-4o    gpt-4o-mini   claude    gemini
OpenAI Agents SDK     ✓          ✓            -         -
smolagents            ✓          ✓            ✓         ✓
```

OpenAI SDK only works with OpenAI models. smolagents covers the rest via LiteLLM.
