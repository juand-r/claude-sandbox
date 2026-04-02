# Escape Room Agent Benchmark

A benchmark for evaluating multi-agent collaboration through escape room puzzles. The core mechanic is **information asymmetry under communication constraints**: each agent holds private state that is necessary but not sufficient to solve the room.

## What It Tests

- **Epistemic self-awareness** — does the agent know what it knows vs. doesn't know?
- **Targeted information exchange** — can agents share relevant info concisely?
- **Information integration** — can an agent act on info received from a teammate?
- **Task decomposition** — can agents coordinate who does what?
- **Sequential coordination** — can agents chain puzzle solutions across dependency graphs?

## Quick Start

```bash
# Set up
cd explorations/escape-room-benchmark
source venv/bin/activate  # or create: python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here

# Run benchmark
python run_benchmark.py --agent openai_sdk --model gpt-4o-mini --rooms all
python run_benchmark.py --agent smolagents --model gpt-4o-mini --rooms all --trials 3
```

## Rooms

| Room | Difficulty | Puzzles | Description |
|------|-----------|---------|-------------|
| `room_01_cipher` | Easy | 1 (cipher) | Caesar cipher: A has key, B has encoded text |
| `room_02_code` | Easy | 1 (code) | 4-digit code split across agents |
| `room_03_study` | Medium | 2 (cipher→code) | Cipher solution unlocks info for a code puzzle |
| `room_04_safes` | Medium | 2 (parallel) | Two word-lock safes, info for each split across both agents |
| `room_05_archive` | Hard | 3 (chain) | Cipher → grid lookup → exit code, with a misleading clue |

## Agent Frameworks

Two agent frameworks are implemented:

- **OpenAI Agents SDK** (`--agent openai_sdk`): Uses tool-calling with `stop_on_first_tool` for step-by-step control. Manages conversation history explicitly.
- **smolagents** (`--agent smolagents`): HuggingFace's ToolCallingAgent with LiteLLMModel. Uses `step_callbacks` for tool call interception and `reset=False` for memory persistence.

## Metrics

| Metric | Description |
|--------|-------------|
| **Success rate** | Did the agents escape? (binary) |
| **Step efficiency** | `engine_actions / optimal_actions` (1.0 = perfect) |
| **Message efficiency** | `messages_sent / optimal_messages` (1.0 = perfect) |
| **Redundancy score** | Fraction of puzzles attempted by both agents (0.0 = no overlap) |

## Sample Results (gpt-4o-mini, 3 trials)

```
Framework      Success   Avg StepEff   Avg MsgEff
OpenAI SDK     13/15     1.53          0.76
smolagents     13/15     2.68          0.88
```

## CLI Options

```
python run_benchmark.py [options]

--agent TYPE        Agent framework: openai_sdk, smolagents (default: openai_sdk)
--model NAME        LLM model name (default: gpt-4o-mini)
--rooms ROOMS       Comma-separated room IDs or 'all' (default: all)
--trials N          Trials per room (default: 1)
--max-turns N       Max turns per trial (default: 20)
--log-dir DIR       Log output directory (default: logs)
-v, --verbose       Verbose logging
```

## Architecture

```
src/
  models.py       # Data model: Puzzle, Room, AgentState, Action, Observation
  engine.py       # Game engine: accepts actions, checks solutions, manages state
  channel.py      # Agent-to-agent message channel with turn budget
  harness.py      # Game loop orchestrator
  metrics.py      # Metric computation from logs
  agent.py        # BaseAgent interface (the contract for all agents)

agent_wrappers/
  openai_sdk_agent.py   # OpenAI Agents SDK wrapper
  smolagents_agent.py   # smolagents wrapper

rooms/
  room_definitions.py   # 5 hand-crafted room definitions

tests/              # 64 tests covering all modules
```

## Adding a New Agent Framework

1. Create `agent_wrappers/your_agent.py` implementing `BaseAgent`
2. Implement `set_role()`, `observe()`, `act()`, and `reset()`
3. Register it in `run_benchmark.py`'s `create_agent()` factory
4. Run: `python run_benchmark.py --agent your_agent --rooms all`

See AGENTS.md for analysis of framework options and DESIGN.md for the full spec.
