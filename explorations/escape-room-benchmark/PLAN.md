# Escape Room Benchmark — Implementation Plan

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

## Step 4: Agent Interface

**Goal**: Define the contract between the harness and an LLM agent.

**Deliverables**:
- `agent.py` — Agent base class / interface.
  - `observe(observation) -> None` — receives new info from the engine or channel
  - `act() -> Action` — returns either a room action or a message to teammate
  - An LLM-backed implementation that formats observations into a prompt and parses the LLM response into an action or message.
  - A scripted/dummy agent for testing without LLM calls.

**Test**: Run the dummy agent through the simple room from Steps 1-2 using the channel from Step 3. Confirm the harness loop works: observe -> act -> engine processes -> next turn.

**Done when**: A scripted agent can play through a room end-to-end via the harness loop.

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

**Test**: Run the scripted agent through all 5 rooms. Verify metrics are computed correctly against known-optimal values.

**Done when**: `python run_benchmark.py --agent scripted` produces a metric profile for all 5 rooms.

---

## Step 7: LLM Agent Integration

**Goal**: Plug in actual LLM agents and run the benchmark.

**Deliverables**:
- LLM agent implementation in `agent.py` (or `llm_agent.py`).
  - System prompt explaining the escape room setup, available actions, communication protocol.
  - Response parsing: distinguish "I want to act on the room" from "I want to message my teammate."
  - Error handling for malformed responses.
- `run_benchmark.py` — CLI entry point.
  - `--agent llm --model <model_name>`
  - `--rooms all` or `--rooms 1,3,5`
  - `--trials N` for statistical significance

**Test**: Run a single easy room with an LLM agent pair. Verify the loop completes, logs are clean, metrics are computed.

**Done when**: Can run `python run_benchmark.py --agent llm --model <model> --rooms all --trials 5` and get a results table.

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
    agent.py
    llm_agent.py
    harness.py
    metrics.py
    run_benchmark.py
  rooms/
    room_01_cipher.json (or .py)
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

- [ ] Step 1: Room Data Model
- [ ] Step 2: Room Oracle / Game Engine
- [ ] Step 3: Communication Channel
- [ ] Step 4: Agent Interface
- [ ] Step 5: Hand-Craft the 5 Rooms
- [ ] Step 6: Eval Harness
- [ ] Step 7: LLM Agent Integration
- [ ] Step 8: Adversarial Variant (stretch)
