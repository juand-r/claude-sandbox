"""
Agent base class — the contract between the harness and any agent.

Any agent framework (OpenAI SDK, smolagents, etc.) must be wrapped
to implement this interface.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class AgentActionType(Enum):
    """What the agent decides to do on its turn."""
    SUBMIT = "submit"     # Submit an answer to a puzzle
    MESSAGE = "message"   # Send a message to teammate
    LOOK = "look"         # Look around / examine the room


@dataclass
class AgentAction:
    """
    The action returned by an agent on its turn.

    For SUBMIT: puzzle_id is the target, content is the answer.
    For MESSAGE: content is the message text.
    For LOOK: no additional fields needed.
    """
    action_type: AgentActionType
    puzzle_id: str = ""
    content: str = ""


class BaseAgent(ABC):
    """
    Base class for all agents in the escape room benchmark.

    The harness calls:
    1. set_role(agent_id, initial_observation) — once, at game start
    2. observe(text) — whenever new info arrives (puzzle results, teammate messages)
    3. act() -> AgentAction — when it's the agent's turn to do something
    """

    def __init__(self, name: str = ""):
        self.name = name
        self.agent_id: str = ""

    @abstractmethod
    def set_role(self, agent_id: str, initial_observation: str):
        """Called once at game start with the agent's ID and initial observation."""
        pass

    @abstractmethod
    def observe(self, text: str):
        """Called when the agent receives new information (results, messages, reveals)."""
        pass

    @abstractmethod
    def act(self) -> AgentAction:
        """
        Called when it's the agent's turn. Returns what the agent wants to do.
        The agent should decide between submitting an answer, messaging teammate, or looking around.
        """
        pass

    @abstractmethod
    def reset(self):
        """Reset the agent for a new game."""
        pass
