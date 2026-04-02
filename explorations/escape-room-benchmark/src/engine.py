"""
Room Oracle / Game Engine.

Holds the true room state, accepts agent actions, returns observations,
tracks what's been solved, and detects the win condition.

The engine is the source of truth. Agents interact with the room
exclusively through this interface.
"""

import logging
from dataclasses import dataclass, field

from .models import (
    Room, Puzzle, Action, ActionType, Observation, AgentState, InfoPartition,
)

logger = logging.getLogger(__name__)


@dataclass
class EngineState:
    """Internal state of the engine for a single game."""
    room: Room
    solved_puzzles: set[str] = field(default_factory=set)
    agent_states: dict[str, AgentState] = field(default_factory=dict)
    turn_count: int = 0
    action_log: list[dict] = field(default_factory=list)
    escaped: bool = False


class RoomEngine:
    """
    The game engine. One instance per game (room + two agents).

    Usage:
        engine = RoomEngine(room)
        obs_a, obs_b = engine.start()
        # ... game loop: agents take actions, engine returns observations
    """

    AGENT_A = "agent_a"
    AGENT_B = "agent_b"

    def __init__(self, room: Room):
        self.state = EngineState(room=room)

    @property
    def room(self) -> Room:
        return self.state.room

    @property
    def solved_puzzles(self) -> set[str]:
        return self.state.solved_puzzles

    @property
    def is_escaped(self) -> bool:
        return self.state.escaped

    @property
    def turn_count(self) -> int:
        return self.state.turn_count

    def start(self) -> tuple[Observation, Observation]:
        """
        Initialize the game. Returns starting observations for Agent A and Agent B.
        Each agent sees the shared room description, shared puzzle info, and their
        private info for all initially available puzzles.
        """
        # Create agent states
        self.state.agent_states = {
            self.AGENT_A: AgentState(agent_id=self.AGENT_A),
            self.AGENT_B: AgentState(agent_id=self.AGENT_B),
        }

        initial_puzzles = self.room.get_initial_puzzles()

        # Build starting observations
        obs_a = self._build_initial_observation(self.AGENT_A, initial_puzzles)
        obs_b = self._build_initial_observation(self.AGENT_B, initial_puzzles)

        self.state.agent_states[self.AGENT_A].add_observation(obs_a)
        self.state.agent_states[self.AGENT_B].add_observation(obs_b)

        logger.info(f"Game started: room='{self.room.id}', puzzles={[p.id for p in self.room.puzzles]}")
        return obs_a, obs_b

    def submit_action(self, action: Action) -> Observation:
        """
        Process an agent's action and return an observation.

        Only handles SUBMIT and LOOK actions. MESSAGE actions should go
        through the Channel, not the engine.
        """
        if action.action_type == ActionType.MESSAGE:
            raise ValueError("Messages should be sent through the Channel, not the engine.")

        self.state.turn_count += 1
        agent_state = self.state.agent_states[action.agent_id]
        agent_state.record_action(action)

        # Log the action
        log_entry = {
            "turn": self.state.turn_count,
            "agent": action.agent_id,
            "type": action.action_type.value,
            "target": action.target,
            "content": action.content,
        }

        if action.action_type == ActionType.SUBMIT:
            obs = self._handle_submit(action)
        elif action.action_type == ActionType.LOOK:
            obs = self._handle_look(action)
        else:
            obs = Observation(text=f"Unknown action type: {action.action_type}")

        log_entry["result"] = obs.text
        log_entry["puzzle_solved"] = obs.puzzle_solved
        self.state.action_log.append(log_entry)

        agent_state.add_observation(obs)
        return obs

    def get_agent_state(self, agent_id: str) -> AgentState:
        """Get the current state for an agent."""
        return self.state.agent_states[agent_id]

    def get_available_puzzles(self) -> list[Puzzle]:
        """Get puzzles currently available to work on (dependencies met, not yet solved)."""
        return self.room.get_unlocked_puzzles(self.solved_puzzles)

    def get_action_log(self) -> list[dict]:
        """Get the full action log for metric computation."""
        return self.state.action_log

    # --- Private methods ---

    def _build_initial_observation(self, agent_id: str, puzzles: list[Puzzle]) -> Observation:
        """Build the starting observation for an agent."""
        lines = [
            f"You are {agent_id.replace('_', ' ').title()} in escape room '{self.room.name}'.",
            f"Room description: {self.room.description}",
            "",
            "Available puzzles:",
        ]

        revealed_info = []
        for puzzle in puzzles:
            lines.append(f"  - {puzzle.id}: {puzzle.description}")
            # Shared info
            for info in puzzle.info.shared_info:
                lines.append(f"    [shared] {info}")
            # Private info for this agent
            private = self._get_private_info(agent_id, puzzle.info)
            for info in private:
                lines.append(f"    [private] {info}")
                revealed_info.append(info)

        return Observation(text="\n".join(lines), revealed_info=revealed_info)

    def _get_private_info(self, agent_id: str, info: InfoPartition) -> list[str]:
        """Get the private info for a specific agent from a partition."""
        if agent_id == self.AGENT_A:
            return info.agent_a_info
        elif agent_id == self.AGENT_B:
            return info.agent_b_info
        else:
            raise ValueError(f"Unknown agent: {agent_id}")

    def _handle_submit(self, action: Action) -> Observation:
        """Handle a SUBMIT action: check answer against puzzle solution."""
        puzzle_id = action.target
        answer = action.content.strip()

        # Check puzzle exists
        try:
            puzzle = self.room.get_puzzle(puzzle_id)
        except KeyError:
            return Observation(text=f"There is no puzzle called '{puzzle_id}'.")

        # Check puzzle is available
        if puzzle_id in self.solved_puzzles:
            return Observation(text=f"Puzzle '{puzzle_id}' is already solved.")

        available_ids = {p.id for p in self.get_available_puzzles()}
        if puzzle_id not in available_ids:
            unsolved_deps = [d for d in puzzle.depends_on if d not in self.solved_puzzles]
            return Observation(
                text=f"Puzzle '{puzzle_id}' is not yet available. "
                     f"You must first solve: {unsolved_deps}"
            )

        # Check answer
        if answer.lower() == puzzle.solution.lower():
            return self._solve_puzzle(puzzle, action.agent_id)
        else:
            logger.info(f"{action.agent_id} submitted wrong answer '{answer}' for {puzzle_id}")
            return Observation(text=f"Wrong answer for '{puzzle_id}'. The answer '{answer}' is incorrect.")

    def _solve_puzzle(self, puzzle: Puzzle, solver_agent_id: str) -> Observation:
        """Mark a puzzle as solved and reveal any new info."""
        self.solved_puzzles.add(puzzle.id)
        logger.info(f"Puzzle '{puzzle.id}' solved by {solver_agent_id}")

        revealed_info = []
        reveal_lines = []

        # Process on_solve_reveals
        for target, infos in puzzle.on_solve_reveals.items():
            if target == "both":
                # Both agents get this info — but we only return it in this observation.
                # The other agent will need to be notified separately by the harness.
                for info in infos:
                    revealed_info.append(info)
                    reveal_lines.append(info)
            elif target == solver_agent_id:
                for info in infos:
                    revealed_info.append(info)
                    reveal_lines.append(info)
            # Info for the other agent is stored but not returned here.
            # The harness is responsible for delivering it.

        # Check if new puzzles became available
        newly_available = self.room.get_unlocked_puzzles(self.solved_puzzles)
        if newly_available:
            for p in newly_available:
                reveal_lines.append(f"A new puzzle is now available: {p.id} — {p.description}")
                # Reveal shared info for newly available puzzles
                for info in p.info.shared_info:
                    reveal_lines.append(f"  [shared] {info}")

        # Check win condition
        escaped = self.room.is_escaped(self.solved_puzzles)
        self.state.escaped = escaped

        text_parts = [f"Correct! Puzzle '{puzzle.id}' is solved."]
        if reveal_lines:
            text_parts.append("\n".join(reveal_lines))
        if escaped:
            text_parts.append("ALL PUZZLES SOLVED. You have escaped the room!")

        return Observation(
            text="\n".join(text_parts),
            revealed_info=revealed_info,
            puzzle_solved=puzzle.id,
            room_escaped=escaped,
        )

    def _handle_look(self, action: Action) -> Observation:
        """Handle a LOOK action: describe available puzzles and state."""
        available = self.get_available_puzzles()
        solved = self.solved_puzzles

        lines = ["You look around the room."]
        if solved:
            lines.append(f"Solved puzzles: {', '.join(sorted(solved))}")
        if available:
            lines.append("Available puzzles:")
            for p in available:
                lines.append(f"  - {p.id}: {p.description}")
        else:
            lines.append("No unsolved puzzles remaining." if self.is_escaped
                         else "No puzzles currently available. Something needs to be solved first.")
        return Observation(text="\n".join(lines))

    def get_other_agent_reveals(self, puzzle: Puzzle, solver_agent_id: str) -> list[str]:
        """
        Get the info that should be revealed to the OTHER agent when a puzzle is solved.
        The harness should call this and deliver the info.
        """
        other_id = self.AGENT_B if solver_agent_id == self.AGENT_A else self.AGENT_A
        reveals = []
        for target, infos in puzzle.on_solve_reveals.items():
            if target == "both" or target == other_id:
                reveals.extend(infos)

        # Also include shared info from newly available puzzles
        newly_available = self.room.get_unlocked_puzzles(self.solved_puzzles)
        for p in newly_available:
            for info in p.info.shared_info:
                reveals.append(f"[New puzzle available: {p.id}] {info}")

        return reveals

    def get_newly_available_private_info(self, agent_id: str) -> list[str]:
        """
        Get private info for newly available puzzles for a specific agent.
        Called after a puzzle is solved to deliver new private info.
        """
        available = self.get_available_puzzles()
        infos = []
        for p in available:
            private = self._get_private_info(agent_id, p.info)
            infos.extend(private)
        return infos
