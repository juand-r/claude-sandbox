"""
Game harness: runs a single escape room trial with two agents.

Orchestrates the turn loop:
1. Agents receive initial observations
2. On each turn, one agent acts (submit, message, or look)
3. Engine processes actions, channel handles messages
4. Game ends when room is escaped or turn budget is exhausted

The harness logs everything for metric computation.
"""

import logging
import json
from dataclasses import dataclass, field
from datetime import datetime

from .models import Room, Action, ActionType, Observation
from .engine import RoomEngine
from .channel import Channel
from .agent import BaseAgent, AgentAction, AgentActionType

logger = logging.getLogger(__name__)


@dataclass
class TrialResult:
    """Complete result of a single trial, for metric computation."""
    room_id: str
    escaped: bool
    total_turns: int
    action_log: list[dict] = field(default_factory=list)
    transcript: list[dict] = field(default_factory=list)
    agent_a_actions: int = 0
    agent_b_actions: int = 0
    messages_sent: int = 0
    timestamp: str = ""

    def to_dict(self) -> dict:
        return {
            "room_id": self.room_id,
            "escaped": self.escaped,
            "total_turns": self.total_turns,
            "action_log": self.action_log,
            "transcript": self.transcript,
            "agent_a_actions": self.agent_a_actions,
            "agent_b_actions": self.agent_b_actions,
            "messages_sent": self.messages_sent,
            "timestamp": self.timestamp,
        }


class GameHarness:
    """
    Runs a single escape room game with two agents.

    Turn structure:
    - Agents alternate turns (A, B, A, B, ...)
    - On each turn, the agent chooses: SUBMIT, MESSAGE, or LOOK
    - SUBMIT and LOOK go to the engine
    - MESSAGE goes through the channel
    - After each action, the acting agent receives feedback
    - After a MESSAGE, the receiving agent is notified on their next turn
    - After a SUBMIT that solves a puzzle, both agents may get new info

    Turn budget: total turns across both agents + messages combined.
    """

    def __init__(self, room: Room, agent_a: BaseAgent, agent_b: BaseAgent,
                 max_turns: int = 20):
        self.room = room
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.max_turns = max_turns
        self.engine = RoomEngine(room)
        self.channel = Channel(max_turns=max_turns)
        self._turn_count = 0

    def run(self) -> TrialResult:
        """Run the full game and return results."""
        logger.info(f"=== Starting game: room='{self.room.id}' ===")

        # Initialize
        obs_a, obs_b = self.engine.start()
        self.agent_a.set_role(RoomEngine.AGENT_A, obs_a.text)
        self.agent_b.set_role(RoomEngine.AGENT_B, obs_b.text)

        # Alternate turns: A, B, A, B, ...
        agents = [
            (self.agent_a, RoomEngine.AGENT_A),
            (self.agent_b, RoomEngine.AGENT_B),
        ]
        turn_idx = 0

        while self._turn_count < self.max_turns and not self.engine.is_escaped:
            agent, agent_id = agents[turn_idx % 2]
            self._play_turn(agent, agent_id)
            turn_idx += 1

        # Build result
        result = TrialResult(
            room_id=self.room.id,
            escaped=self.engine.is_escaped,
            total_turns=self._turn_count,
            action_log=self.engine.get_action_log(),
            transcript=self.channel.get_transcript(),
            agent_a_actions=len([
                a for a in self.engine.get_action_log()
                if a["agent"] == RoomEngine.AGENT_A
            ]),
            agent_b_actions=len([
                a for a in self.engine.get_action_log()
                if a["agent"] == RoomEngine.AGENT_B
            ]),
            messages_sent=self.channel.total_messages,
            timestamp=datetime.now().isoformat(),
        )

        status = "ESCAPED" if result.escaped else "FAILED"
        logger.info(f"=== Game over: {status} in {result.total_turns} turns ===")
        return result

    def _play_turn(self, agent: BaseAgent, agent_id: str):
        """Execute one agent's turn."""
        self._turn_count += 1
        logger.info(f"--- Turn {self._turn_count}: {agent_id} ---")

        # Deliver any pending messages from the channel
        new_msgs = self.channel.get_new_messages(agent_id)
        for msg in new_msgs:
            notify_text = f"[Message from {msg.from_agent}]: {msg.text}"
            agent.observe(notify_text)
            logger.info(f"  Delivered message to {agent_id}: {msg.text[:60]}...")

        # Agent decides what to do
        agent_action = agent.act()
        logger.info(f"  Action: {agent_action.action_type.value} "
                     f"target='{agent_action.puzzle_id}' content='{agent_action.content[:60]}'")

        if agent_action.action_type == AgentActionType.MESSAGE:
            self._handle_message(agent, agent_id, agent_action)
        elif agent_action.action_type == AgentActionType.SUBMIT:
            self._handle_submit(agent, agent_id, agent_action)
        elif agent_action.action_type == AgentActionType.LOOK:
            self._handle_look(agent, agent_id, agent_action)

    def _handle_message(self, agent: BaseAgent, agent_id: str, agent_action: AgentAction):
        """Handle a MESSAGE action."""
        sent = self.channel.send(agent_id, agent_action.content)
        if sent:
            agent.observe(f"[Message sent to teammate]: {agent_action.content}")
        else:
            agent.observe("[Message not sent: turn budget exhausted]")

    def _handle_submit(self, agent: BaseAgent, agent_id: str, agent_action: AgentAction):
        """Handle a SUBMIT action."""
        engine_action = Action(
            agent_id=agent_id,
            action_type=ActionType.SUBMIT,
            target=agent_action.puzzle_id,
            content=agent_action.content,
        )
        obs = self.engine.submit_action(engine_action)
        agent.observe(obs.text)

        # If a puzzle was solved, notify the other agent about reveals
        if obs.puzzle_solved:
            self._deliver_solve_reveals(agent_id, obs.puzzle_solved)

    def _handle_look(self, agent: BaseAgent, agent_id: str, agent_action: AgentAction):
        """Handle a LOOK action."""
        engine_action = Action(
            agent_id=agent_id,
            action_type=ActionType.LOOK,
        )
        obs = self.engine.submit_action(engine_action)
        agent.observe(obs.text)

    def _deliver_solve_reveals(self, solver_id: str, puzzle_id: str):
        """After a puzzle is solved, deliver new info to the other agent."""
        other_agent, other_id = (
            (self.agent_b, RoomEngine.AGENT_B) if solver_id == RoomEngine.AGENT_A
            else (self.agent_a, RoomEngine.AGENT_A)
        )

        puzzle = self.room.get_puzzle(puzzle_id)
        reveals = self.engine.get_other_agent_reveals(puzzle, solver_id)
        if reveals:
            reveal_text = f"[Puzzle '{puzzle_id}' was solved! New information:]\n" + "\n".join(reveals)
            other_agent.observe(reveal_text)
            logger.info(f"  Revealed to {other_id}: {len(reveals)} pieces of info")

        # Also deliver private info for newly available puzzles
        for aid, ag in [(RoomEngine.AGENT_A, self.agent_a), (RoomEngine.AGENT_B, self.agent_b)]:
            private_info = self.engine.get_newly_available_private_info(aid)
            if private_info:
                info_text = "[New private information:]\n" + "\n".join(private_info)
                ag.observe(info_text)
                logger.info(f"  New private info for {aid}: {len(private_info)} pieces")
