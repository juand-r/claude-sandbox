# Escape Room Benchmark — Development Journal

## 2026-04-02

### Session Start

Setting up the project. User is away on a work trip; I have full autonomy.

**Environment setup:**
- Python 3.11 virtual env created at `venv/`
- Installed: `openai-agents==0.13.4`, `pytest==9.0.2` + dependencies
- `requirements.txt` generated from `pip freeze`
- Directory structure: `src/`, `rooms/`, `tests/`, `agents/`

**Plan:** Work through Steps 1-7 of PLAN.md. Test each layer before the next. Commit frequently.

### Step 1: Room Data Model — DONE
- `src/models.py`: Puzzle, Room, AgentState, Action, Observation types
- 10 tests passing

### Step 2: Game Engine — DONE
- `src/engine.py`: RoomEngine with action processing, dependency tracking, win detection
- 18 tests passing

### Step 3: Communication Channel — DONE
- `src/channel.py`: Turn-based messaging with budget enforcement
- 10 tests passing

### Step 4a: Agent Interface + Scripted Agent + Harness — DONE
- `src/agent.py`: BaseAgent interface
- `src/scripted_agent.py`: Deterministic agent for testing
- `src/harness.py`: Full game loop orchestrator
- 7 harness tests passing

### Step 4b: OpenAI Agents SDK Integration — DONE
- `agent_wrappers/openai_sdk_agent.py`: Real agent using OpenAI SDK
- **Key issue encountered**: Originally tried to parse `final_output` string, but SDK runs
  the agent to completion after tool calls, so `final_output` is natural language, not the
  tool return value. Fix: use `tool_use_behavior="stop_on_first_tool"` and `max_turns=1`,
  then inspect `raw_responses` for the actual tool call with arguments.
- **Also**: Renamed `agents/` directory to `agent_wrappers/` because it collided with the
  `agents` package from the OpenAI SDK (`from agents import Agent` was importing our dir).
- **First successful LLM run**: Two gpt-4o-mini agents escaped the simple cipher room in
  3 turns (2 messages + 1 submit). They correctly exchanged key and encoded text, decoded
  the message, and submitted the answer.

---
