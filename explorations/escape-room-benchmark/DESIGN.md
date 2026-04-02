# Escape Room Agent Benchmark — Design Document

## Overview

A benchmark for evaluating multi-agent collaboration through escape room puzzles. The core mechanic is **information asymmetry under communication constraints**: each agent holds private state that is necessary but not sufficient to solve the room. This forces collaboration and tests capabilities no single-agent benchmark can.

## Target Capabilities

### Primary

- **Epistemic self-awareness** — Does the agent know what it knows vs. doesn't know? Can it identify missing information?
- **Targeted information request** — Can it ask good questions, not just dump its entire context?
- **Information integration** — When told something by a teammate, can it incorporate it correctly and act on it?
- **Task decomposition & delegation** — Can agents divide a problem and coordinate who does what?
- **Redundancy avoidance** — Do they duplicate work, step on each other, or work efficiently?

### Secondary (harder to test, worth capturing)

- **Calibrated trust** — If given wrong info by a faulty teammate, does it catch it or blindly follow?
- **Communication compression** — Can agents be concise, or do they flood the channel with noise?
- **Adaptive re-planning** — If a subtask fails or a teammate goes silent, can they recover?

The capability gradient matters: the benchmark should distinguish "agents that can pass basic info along" from "agents that collaborate elegantly."

---

## Structural Requirements

### 1. Information Partitioning (core mechanic)

Every puzzle room has a global state — the "ground truth" — split across agents at the start. The partition is designed so no single agent can solve the room alone.

Example: Agent A sees a cipher alphabet. Agent B sees the encoded message. Neither can decode without the other.

### 2. Puzzle Dependency Graph

Rooms have multiple puzzles with dependencies: solving puzzle A unlocks puzzle B. This creates sequencing decisions and tests whether agents can coordinate who works on what next, not just exchange information once.

### 3. Room Oracle / Game Engine

A thin middleware layer that:
- Holds the true room state
- Accepts agent actions ("I enter code 4-7-2 into the keypad")
- Returns observations ("The keypad beeps. A drawer opens, revealing a note.")
- Tracks what has been unlocked/solved
- Knows the terminal success condition

This keeps evaluation clean and removes ambiguity.

### 4. Communication Channel

Agents communicate through a logged channel, separate from the action interface. Talking to your teammate is distinct from acting on the room.

For MVP: **turn-based** (simpler, more reproducible). Fixed turn budget.

### 5. Hand-Crafted Puzzle Library

No procedural generation at MVP. Hand-crafted rooms let you control exactly what capabilities each room tests and verify clean solutions. Rooms vary along two axes:
- **Depth**: number of dependency steps
- **Breadth**: degree of info fragmentation (coordination needed)

### 6. Difficulty Tiers

- **Easy**: One exchange required, one puzzle.
- **Medium**: Two-three exchanges, dependent puzzles.
- **Hard**: Agents must coordinate task division, multi-step, possibly conflicting info to reconcile.

---

## Evaluation Metrics

### Primary

| Metric | Description |
|--------|-------------|
| **Success rate** | Did they escape? Binary. |
| **Step efficiency** | `actual_turns / optimal_turns` ratio. More useful than raw count. |
| **Message efficiency** | Messages sent vs. minimum messages theoretically needed. |

### Secondary

| Metric | Description |
|--------|-------------|
| **Information utilization rate** | Of all relevant private info an agent possessed, how much was correctly transmitted? Requires labeling "load-bearing" info tokens per puzzle. |
| **Redundancy score** | Did both agents attempt to solve the same puzzle independently? Did they repeat already-shared info? |
| **Error recovery** | (Adversarial variant) If one agent sends wrong info, does the other catch it? |

### Not needed at MVP

- Human baselines
- Latency/cost metrics
- Multi-model combinations

All metrics must be computable automatically from logs. No human judgment for core metrics.

---

## MVP Scope

### Constraints

- 2 agents (A and B, symmetric roles)
- Text-only, no visuals
- 5 hand-crafted rooms across 3 difficulty tiers (2 easy, 2 medium, 1 hard)
- 3 puzzle types maximum
- Turn-based communication, fixed turn budget (20 turns max)
- Automated eval on success, turn count, message count

### Three Puzzle Types

**Type 1 — Cipher/Key Split** (Easy)
Agent A has a substitution key, Agent B has encoded text. Pure info exchange, one-shot solvable.

**Type 2 — Multi-Part Code** (Easy/Medium)
Agent A has digits 1 and 3 of a 4-digit code, Agent B has digits 2 and 4. They must assemble the code together. Tests synthesis.

**Type 3 — Dependency Chain** (Medium/Hard)
Puzzle 1 is a cipher (Type 1). Its solution is a word that unlocks a box. The box contains a map that only makes sense when combined with coordinates Agent B was given at the start. Tests sequential coordination.
