"""
Data models for the escape room benchmark.

Core types:
- Puzzle: a single puzzle with a solution, info partition, and dependencies
- Room: a collection of puzzles forming an escape room
- AgentState: what a single agent can see at any point in time
- Action: what an agent can do on a given turn
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PuzzleType(Enum):
    """The three puzzle types in our benchmark."""
    CIPHER = "cipher"           # Type 1: A has key, B has encoded text
    MULTI_PART_CODE = "code"    # Type 2: A has some digits, B has others
    DEPENDENCY_CHAIN = "chain"  # Type 3: solution of one puzzle feeds into next


class ActionType(Enum):
    """What an agent can do on a turn."""
    SUBMIT = "submit"       # Submit an answer to a puzzle
    MESSAGE = "message"     # Send a message to teammate
    LOOK = "look"           # Look around / examine something (costs a turn)


@dataclass
class InfoPartition:
    """
    How information is split between agents for a puzzle.

    agent_a_info: what Agent A sees at the start (or when the puzzle becomes available)
    agent_b_info: what Agent B sees at the start (or when the puzzle becomes available)
    shared_info: what both agents see (e.g., "there is a locked keypad on the wall")
    load_bearing_tokens: the specific pieces of info that MUST be communicated to solve
                         the puzzle. Used for the information utilization metric.
    """
    agent_a_info: list[str]
    agent_b_info: list[str]
    shared_info: list[str] = field(default_factory=list)
    load_bearing_tokens: dict[str, list[str]] = field(default_factory=dict)
    # load_bearing_tokens maps agent_id -> list of info strings that agent
    # must transmit to the other for the puzzle to be solvable.
    # e.g. {"agent_a": ["substitution key: A=X, B=Y, ..."], "agent_b": ["encoded message: XYZZY"]}


@dataclass
class Puzzle:
    """
    A single puzzle in the escape room.

    id: unique identifier within the room (e.g., "cipher_1")
    puzzle_type: one of the three types
    description: human-readable description of the puzzle (for logging/debugging)
    info: how information is split between agents
    solution: the correct answer (string, compared case-insensitively)
    depends_on: list of puzzle IDs that must be solved before this one is available
    on_solve_reveals: additional info revealed to agents when this puzzle is solved.
                      Maps agent_id -> list of new info strings. Use "both" for shared.
    """
    id: str
    puzzle_type: PuzzleType
    description: str
    info: InfoPartition
    solution: str
    depends_on: list[str] = field(default_factory=list)
    on_solve_reveals: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class RoomMetadata:
    """
    Metadata for computing eval metrics.

    optimal_steps: minimum number of submit actions needed to solve the room
    optimal_messages: minimum number of messages needed between agents
    difficulty: easy / medium / hard
    """
    optimal_steps: int
    optimal_messages: int
    difficulty: str  # "easy", "medium", "hard"


@dataclass
class Room:
    """
    An escape room: a set of puzzles with dependencies.

    The room is "escaped" when all puzzles are solved.
    """
    id: str
    name: str
    description: str
    puzzles: list[Puzzle]
    metadata: RoomMetadata

    def get_puzzle(self, puzzle_id: str) -> Puzzle:
        """Get a puzzle by ID. Raises KeyError if not found."""
        for p in self.puzzles:
            if p.id == puzzle_id:
                return p
        raise KeyError(f"Puzzle '{puzzle_id}' not found in room '{self.id}'")

    def get_initial_puzzles(self) -> list[Puzzle]:
        """Get puzzles with no dependencies (available from the start)."""
        return [p for p in self.puzzles if not p.depends_on]

    def get_unlocked_puzzles(self, solved_ids: set[str]) -> list[Puzzle]:
        """Get puzzles whose dependencies are all satisfied."""
        return [
            p for p in self.puzzles
            if p.id not in solved_ids
            and all(dep in solved_ids for dep in p.depends_on)
        ]

    def is_escaped(self, solved_ids: set[str]) -> bool:
        """Room is escaped when all puzzles are solved."""
        return solved_ids == {p.id for p in self.puzzles}


@dataclass
class Action:
    """An action taken by an agent."""
    agent_id: str
    action_type: ActionType
    target: str = ""       # puzzle_id for SUBMIT, empty for MESSAGE/LOOK
    content: str = ""      # answer for SUBMIT, message text for MESSAGE, target for LOOK


@dataclass
class Observation:
    """What an agent sees in response to an action or at the start of the game."""
    text: str
    revealed_info: list[str] = field(default_factory=list)
    puzzle_solved: str | None = None     # puzzle_id if a puzzle was just solved
    room_escaped: bool = False


@dataclass
class AgentState:
    """
    What a single agent knows at any point in time.

    Accumulates info over the course of the game.
    """
    agent_id: str
    private_info: list[str] = field(default_factory=list)      # info from puzzle partitions
    observations: list[Observation] = field(default_factory=list)  # all observations received
    messages_received: list[dict] = field(default_factory=list)    # messages from teammate
    messages_sent: list[str] = field(default_factory=list)         # messages sent to teammate
    actions_taken: list[Action] = field(default_factory=list)      # all actions taken

    def add_observation(self, obs: Observation):
        self.observations.append(obs)
        self.private_info.extend(obs.revealed_info)

    def add_received_message(self, from_agent: str, text: str, turn: int):
        self.messages_received.append({
            "from": from_agent,
            "text": text,
            "turn": turn,
        })

    def add_sent_message(self, text: str):
        self.messages_sent.append(text)

    def record_action(self, action: Action):
        self.actions_taken.append(action)
