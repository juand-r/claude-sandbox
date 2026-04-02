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

### Step 5: Room Definitions — DONE
- 5 rooms across 3 difficulty tiers, all with verified scripted solutions
- **Bug caught**: Room 5 cipher text was wrong (YVOLT should have been EZFOG for VAULT
  with reverse alphabet). Fixed before committing.
- 15 room-specific tests passing

### Step 6: Metrics + CLI Runner — DONE
- `src/metrics.py`: Computes success, step_efficiency, message_efficiency, redundancy
- `run_benchmark.py`: Full CLI with --agent, --model, --rooms, --trials, --max-turns
- 4 metrics tests passing (total: 64 tests)

### First Full Benchmark Run — gpt-4o-mini

```
Room                   Diff     Result Turns  Msgs   StepEff  MsgEff   Redund
room_01_cipher         easy     FAIL   turns=16  msgs=9   7.00   4.50   1.00
room_02_code           easy     PASS   turns=3   msgs=2   1.00   1.00   0.00
room_03_study          medium   PASS   turns=6   msgs=2   2.00   0.67   0.50
room_04_safes          medium   PASS   turns=6   msgs=3   1.50   0.75   0.50
room_05_archive        hard     FAIL   turns=16  msgs=8   2.67   1.60   0.00

Success rate: 3/5 (60%)
Avg step efficiency (successful): 1.50
Avg message efficiency (successful): 0.81
```

**Observations:**
- Room 1 (cipher) FAILED: The full 26-letter substitution cipher was too complex for
  gpt-4o-mini. The agents kept trying wrong decodings and ran out of turns. The redundancy
  of 1.0 means both agents were submitting wrong answers to the same puzzle.
- Room 2 (code) PERFECT: The simple digit-sharing task was trivially solved.
- Rooms 3-4 (medium) PASSED but with some inefficiency and redundancy.
- Room 5 (archive) FAILED: Reverse alphabet cipher also too hard for gpt-4o-mini.
  The agents couldn't decode EZFOG -> VAULT.

**Analysis:** The cipher puzzles are too hard for gpt-4o-mini, which is known to be
weak at character-level manipulation. This is actually fine for the benchmark — it
distinguishes model capability. But I should consider whether Room 1 (labeled "easy")
should use a simpler cipher. A Caesar shift might be more appropriate for "easy" tier.

**Decision**: I'll simplify Room 1's cipher to a Caesar shift (like Room 3 uses) and
keep the reverse alphabet for Room 5 (hard). This gives a better difficulty gradient.
Then re-run and see if gpt-4o-mini can handle the easy rooms.

### Step 7: smolagents Integration — DONE

**Setup issues:**
1. `system_prompt` param doesn't exist — it's `instructions` in smolagents.
2. `max_steps` and `verbosity_level` go to parent `MultiStepAgent`, not `ToolCallingAgent`.
3. Tool call interception: smolagents' `run()` returns a final text summary, not tool outputs.
   Used `step_callbacks` to capture `ActionStep` objects with `tool_calls` attribute.
4. **Critical issue: memory persistence.** By default, `run(reset=True)` wipes agent memory
   each call. For multi-turn games, must use `reset=False` on subsequent calls. Without this,
   smolagents scored 1/5 (20%). With it: 4/5 (80%).

### Comparison: OpenAI SDK vs smolagents (gpt-4o-mini, single trial)

```
Framework        Room 1   Room 2   Room 3   Room 4   Room 5   Success
                 (easy)   (easy)   (med)    (med)    (hard)   Rate
OpenAI SDK       PASS/4t  PASS/3t  PASS/12t PASS/4t  PASS/16t 5/5 (100%)
smolagents       PASS/2t  PASS/7t  PASS/14t PASS/5t  FAIL/16t 4/5 (80%)
```

**Observations:**
- OpenAI SDK has better multi-turn coordination (100% vs 80%)
- smolagents was more efficient on some rooms (Room 1: 2 turns vs 4, Room 4: 5 vs 6)
  but less reliable overall
- smolagents failed Room 5 (hard): the 3-puzzle chain was too complex, agents got
  stuck on the reverse alphabet cipher
- Both frameworks struggle with cipher decoding — this is an LLM limitation, not framework
- smolagents has higher redundancy (both agents trying same puzzle more often)

**Key architectural difference:** OpenAI SDK manages conversation history explicitly
(`to_input_list()`). smolagents has internal memory but needs `reset=False` to persist
it across calls. The OpenAI SDK's approach gives more control.

### Multi-Trial Benchmark (3 trials each, gpt-4o-mini, max 16 turns)

```
Framework      Success   Avg StepEff   Avg MsgEff   Notes
OpenAI SDK     13/15     1.53          0.76         Failed: Room 3 (1x), Room 5 (1x)
smolagents     13/15     2.68          0.88         Failed: Room 5 (2x)
```

**Per-room breakdown (pass rate out of 3 trials):**
```
Room           OpenAI SDK   smolagents
Room 1 (easy)  3/3          3/3
Room 2 (easy)  3/3          3/3
Room 3 (med)   2/3          3/3
Room 4 (med)   3/3          3/3
Room 5 (hard)  2/3          1/3
```

**Key findings:**
1. Both frameworks achieve 87% overall success with gpt-4o-mini.
2. OpenAI SDK is more efficient (avg step_eff 1.53 vs 2.68) — fewer wasted turns.
3. smolagents is slightly more reliable on Room 3 (3/3 vs 2/3) but worse on Room 5 (1/3 vs 2/3).
4. Room 5 (hard) is the true differentiator — both frameworks struggle with the 3-puzzle chain.
5. The difficulty gradient works: easy rooms = ~100%, medium = ~90%, hard = ~50%.

**Conclusion:** The benchmark successfully distinguishes framework quality on multi-agent
collaboration. The difficulty curve is reasonable. The benchmark is ready for broader testing
with different models and additional agent frameworks.

---
