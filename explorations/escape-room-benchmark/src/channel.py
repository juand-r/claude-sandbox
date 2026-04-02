"""
Communication channel for agent-to-agent messaging.

Turn-based, logged, separate from the game engine.
The channel tracks messages, enforces turn budget, and provides
a full transcript for metric computation.
"""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """A single message between agents."""
    from_agent: str
    to_agent: str
    text: str
    turn: int


class Channel:
    """
    Turn-based communication channel between two agents.

    Usage:
        channel = Channel(max_turns=20)
        channel.send("agent_a", "The key is A=M, B=N")
        msgs = channel.get_new_messages("agent_b")  # returns messages not yet seen by B
    """

    AGENT_A = "agent_a"
    AGENT_B = "agent_b"

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.messages: list[Message] = []
        self.turn_count: int = 0
        # Track how many messages each agent has seen (index into self.messages)
        self._seen_index: dict[str, int] = {self.AGENT_A: 0, self.AGENT_B: 0}

    @property
    def total_messages(self) -> int:
        return len(self.messages)

    @property
    def budget_remaining(self) -> int:
        return max(0, self.max_turns - self.turn_count)

    @property
    def budget_exhausted(self) -> bool:
        return self.turn_count >= self.max_turns

    def send(self, from_agent: str, text: str) -> bool:
        """
        Send a message from one agent to the other.

        Returns True if the message was sent, False if the budget is exhausted.
        Each message counts as one turn.
        """
        if self.budget_exhausted:
            logger.warning(f"Turn budget exhausted ({self.max_turns}). Message not sent.")
            return False

        to_agent = self.AGENT_B if from_agent == self.AGENT_A else self.AGENT_A
        self.turn_count += 1

        msg = Message(
            from_agent=from_agent,
            to_agent=to_agent,
            text=text,
            turn=self.turn_count,
        )
        self.messages.append(msg)
        logger.info(f"[Turn {self.turn_count}] {from_agent} -> {to_agent}: {text[:80]}...")
        return True

    def get_new_messages(self, agent_id: str) -> list[Message]:
        """
        Get messages that this agent hasn't seen yet.
        Advances the seen index.
        """
        new_msgs = [
            m for m in self.messages[self._seen_index[agent_id]:]
            if m.to_agent == agent_id
        ]
        self._seen_index[agent_id] = len(self.messages)
        return new_msgs

    def get_all_messages(self, agent_id: str) -> list[Message]:
        """Get all messages sent TO this agent (for building full context)."""
        return [m for m in self.messages if m.to_agent == agent_id]

    def get_transcript(self) -> list[dict]:
        """
        Get the full transcript as a list of dicts, for logging and metrics.
        """
        return [
            {
                "turn": m.turn,
                "from": m.from_agent,
                "to": m.to_agent,
                "text": m.text,
            }
            for m in self.messages
        ]

    def get_messages_by_agent(self, agent_id: str) -> list[Message]:
        """Get all messages sent BY this agent."""
        return [m for m in self.messages if m.from_agent == agent_id]
