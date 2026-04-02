# Escape Room Benchmark — Implementation Plan

## Architecture Principle

The benchmark has two clearly separate concerns:

1. **The game environment** — rooms, engine, communication channel, eval harness. This is the product.
2. **The agents** — contestants that plug into the environment via a defined interface. These are what we're evaluating.

The agent interface is a thin contract. Any agent framework (smolagents, Pi, OpenAI Agents SDK, raw LLM calls, etc.) can be wrapped to conform to it. We start with the simplest possible agent (raw OpenAI chat completions) to test the environment. Then we add real agent frameworks as contestants.

## Approach

Bottom-up: build and test each layer before the next. Each step has a clear deliverable and a way to verify it works before moving on.

---

## Step 1: Room Data Model

**Goal**: Define the data structures for rooms, puzzles, agent state, and actions.

**Deliverables**:
- `room.py` — Room class: holds puzzle graph, global state, win condition.
- `puzzle.py` — Puzzle class: holds puzzle type, required info, solution, dependencies.
- `state.py` — AgentState class: what each agent can see (private info, observations so far).

**Test**: Instantiate a simple room (one cipher puzzle) from a dict/JSON definition. Assert that agent states are correctly partitioned — Agent A sees key but not message, Agent B sees message but not key.

**Done when**: Can load a room definition and confirm info partitioning is correct.

---

## Step 2: Room Oracle / Game Engine

**Goal**: The engine that accepts actions, checks solutions, updates state, returns observations.

**Deliverables**:
- `engine.py` — RoomEngine class.
  - `submit_action(agent_id, action_str) -> Observation`
  - Parses actions (e.g., "enter code 4-7-2 on keypad")
  - Checks against puzzle solutions
  - Unlocks dependent puzzles on success
  - Tracks solved/unsolved state
  - Detects win condition

**Test**: Script a sequence of correct actions against the simple room from Step 1. Verify state transitions: puzzle solved -> dependent puzzle unlocked -> room escaped. Also test wrong answers (should not unlock anything).

**Done when**: Can run a scripted playthrough with correct and incorrect actions, all state transitions verified.

---

## Step 3: Communication Channel

**Goal**: A logged, turn-based channel for agent-to-agent messages, separate from actions.

**Deliverables**:
- `channel.py` — Channel class.
  - `send_message(from_agent, message_str)` — adds to log
  - `get_messages(agent_id) -> list` — returns messages visible to this agent
  - Full transcript logging
  - Turn tracking and turn budget enforcement

**Test**: Simulate a back-and-forth between two dummy agents. Verify message ordering, that each agent sees the other's messages, that the turn budget is enforced, and that the full transcript is recoverable.

**Done when**: Channel logs a clean transcript and enforces turn limits.

---

## Step 4: Agent Interface + First Real Agent

**Goal**: Define the agent contract and build a real agent (OpenAI Agents SDK) to test the environment. See AGENTS.md for full options analysis.

**Deliverables**:
- `agent.py` — Agent base class (the contract).
  - `observe(observation) -> None` — receives new info from the engine or channel
  - `act() -> Action` — returns either a room action or a message to teammate
  - Any agent framework can be wrapped to implement this interface.
- `scripted_agent.py` — Deterministic agent for testing. Follows a hardcoded action sequence. Used to verify the engine is correct.
- `openai_sdk_agent.py` — OpenAI Agents SDK wrapper.
  - Uses `@function_tool` for `send_message` and `submit_action` tools.
  - `StopAtTools` / `max_turns=1` for step-by-step control.
  - History via `result.to_input_list()` across turns.
  - System prompt explaining the escape room, available actions, communication protocol.
  - Uses `OPENAI_API_KEY` from environment, gpt-4o-mini for dev, gpt-4o for real runs.

**Test**:
1. Scripted agent plays through simple room. Confirms harness loop works.
2. OpenAI SDK agent plays through same room. Confirms a real agent can interact with the environment.

**Done when**: Both agents can play through a room end-to-end.

---

## Step 5: Hand-Craft the 5 Rooms

**Goal**: Create the puzzle content.

**Deliverables**:
- `rooms/` directory with 5 room definitions (JSON or Python dicts).
  - Room 1 (Easy): Single cipher/key split.
  - Room 2 (Easy): Single multi-part code.
  - Room 3 (Medium): Cipher + multi-part code, sequentially dependent.
  - Room 4 (Medium): Two puzzles with info split across both, requires 2-3 exchanges.
  - Room 5 (Hard): Full dependency chain (Type 3). Cipher -> unlock -> map + coordinates.
- Each room definition includes:
  - Puzzle graph (nodes + edges for dependencies)
  - Info partition (what A sees, what B sees)
  - Optimal solution path (for computing efficiency metrics)
  - Load-bearing info tokens (for information utilization metric)

**Test**: Load each room into the engine. Run a scripted optimal playthrough for each. All 5 must complete successfully.

**Done when**: All 5 rooms have verified solutions and metadata for metrics.

---

## Step 6: Eval Harness

**Goal**: Run a trial end-to-end and compute metrics from logs.

**Deliverables**:
- `harness.py` — Trial runner.
  - Instantiates room, engine, channel, two agents.
  - Runs the turn loop until escape or budget exhausted.
  - Saves full logs (actions, messages, state transitions).
- `metrics.py` — Metric computation from logs.
  - Success rate (binary)
  - Step efficiency ratio (actual / optimal)
  - Message efficiency (messages sent / minimum needed)
  - Redundancy score (from action logs: did both agents attempt same puzzle?)
- `run_benchmark.py` — CLI entry point.
  - `--agent <agent_type>` (scripted, baseline_llm, smolagents, etc.)
  - `--model <model_name>` (for LLM-backed agents)
  - `--rooms all` or `--rooms 1,3,5`
  - `--trials N` for statistical significance

**Test**: Run scripted agent through all 5 rooms. Verify metrics against known-optimal values. Then run baseline LLM agent through all 5 rooms, verify logs and metrics are clean.

**Done when**: `python run_benchmark.py --agent baseline_llm --model gpt-4o --rooms all` produces a metric profile.

---

## Step 7: Add Second Agent Contestant (smolagents)

**Goal**: Add smolagents as a second framework to compare against OpenAI Agents SDK. Same LLM (gpt-4o), different agent architecture — isolates framework quality.

**Deliverables**:
- `agents/smolagents_agent.py` — smolagents `ToolCallingAgent` wrapper.
  - Uses `LiteLLMModel(model_id="gpt-4o")` for apples-to-apples comparison.
  - Custom `Tool` subclasses for `send_message` and `submit_action`.
- Results comparison table: OpenAI SDK vs. smolagents across all 5 rooms.

**Test**: Run smolagents through all 5 rooms. Compare metric profiles against OpenAI SDK results.

**Done when**: Two agent frameworks benchmarked side-by-side with results table.

---

## Step 8 (Stretch): Adversarial Variant

**Goal**: Test error recovery / calibrated trust.

- Inject wrong information from one agent (either via a "faulty agent" mode or by tampering with channel messages).
- Measure whether the other agent detects the inconsistency.

Not required for MVP but the architecture from Steps 1-7 should make this straightforward to add.

---

## File Structure (expected)

```
explorations/escape-room-benchmark/
  DESIGN.md
  PLAN.md
  src/
    room.py
    puzzle.py
    state.py
    engine.py
    channel.py
    agent.py              # base interface
    scripted_agent.py     # deterministic, for testing
    openai_sdk_agent.py   # OpenAI Agents SDK wrapper
    harness.py
    metrics.py
    run_benchmark.py
  agents/                 # real agent framework wrappers
    smolagents_agent.py
    openai_sdk_agent.py
    ...
  rooms/
    room_01_cipher.json
    room_02_code.json
    room_03_cipher_code.json
    room_04_double_split.json
    room_05_dependency_chain.json
  tests/
    test_room.py
    test_engine.py
    test_channel.py
    test_harness.py
    test_metrics.py
```

## Status

- [x] Step 1: Room Data Model
- [x] Step 2: Room Oracle / Game Engine
- [x] Step 3: Communication Channel
- [x] Step 4: Agent Interface + First Real Agent (OpenAI SDK)
- [x] Step 5: Hand-Craft the 5 Rooms
- [x] Step 6: Eval Harness
- [x] Step 7: Add Second Agent Contestant (smolagents)
- [ ] Step 8: Adversarial Variant (stretch)
