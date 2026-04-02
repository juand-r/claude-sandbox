"""
smolagents (HuggingFace) wrapper for the escape room benchmark.

Uses ToolCallingAgent with LiteLLMModel for OpenAI model access.
The agent has a ReAct reasoning loop: think -> tool call -> observe -> repeat.

We capture the first tool call via step_callbacks and use that as the
agent's action for the turn. smolagents always runs to completion (or
max_steps), so we set max_steps=1 and intercept the tool call.
"""

import os
import logging

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from smolagents import Tool, ToolCallingAgent, LiteLLMModel
from src.agent import BaseAgent, AgentAction, AgentActionType

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an AI agent in a collaborative escape room puzzle.

## Your Situation
- You are {agent_id} working with a teammate to escape a room.
- You each have DIFFERENT private information. Neither of you can solve the room alone.
- You must communicate with your teammate to share information and coordinate.

## Available Actions (pick exactly ONE per turn)
1. submit_answer(puzzle_id, answer) — Submit an answer to a puzzle. Only when confident.
2. send_message(text) — Send a message to your teammate.
3. look_around() — Examine the room.

## Rules
- Pick ONE tool per turn. Be concise. Share only what's relevant.
- Don't submit unless you have enough information to be confident.
- Pay close attention to what your teammate tells you.
"""


class SubmitAnswerTool(Tool):
    name = "submit_answer"
    description = "Submit an answer to a puzzle. Use when you are confident."
    inputs = {
        "puzzle_id": {"type": "string", "description": "The puzzle ID (e.g., 'cipher_1')"},
        "answer": {"type": "string", "description": "Your answer"},
    }
    output_type = "string"

    def forward(self, puzzle_id: str, answer: str) -> str:
        return f"ACTION:SUBMIT:{puzzle_id}:{answer}"


class SendMessageTool(Tool):
    name = "send_message"
    description = "Send a message to your teammate to share info, ask questions, or coordinate."
    inputs = {
        "text": {"type": "string", "description": "The message to send"},
    }
    output_type = "string"

    def forward(self, text: str) -> str:
        return f"ACTION:MESSAGE:{text}"


class LookAroundTool(Tool):
    name = "look_around"
    description = "Look around the room to see available puzzles and current state."
    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        return "ACTION:LOOK"


class SmolagentsAgent(BaseAgent):
    """
    Agent backed by smolagents ToolCallingAgent.

    Uses step_callbacks to capture the first tool call from each run.
    """

    def __init__(self, name: str = "smolagents", model: str = "gpt-4o-mini"):
        super().__init__(name=name)
        self.model_name = model
        self._observations: list[str] = []
        self._agent: ToolCallingAgent | None = None
        self._captured_tool_calls: list = []

    def set_role(self, agent_id: str, initial_observation: str):
        self.agent_id = agent_id
        self._observations = [initial_observation]
        self._captured_tool_calls = []
        self._setup_agent()

    def observe(self, text: str):
        self._observations.append(text)

    def act(self) -> AgentAction:
        """Run the smolagent for one step and extract the action from tool calls."""
        if not self._observations:
            task = "It's your turn. What would you like to do? Call one of your tools."
        else:
            parts = self._observations.copy()
            parts.append("\nIt's your turn. Choose an action by calling one of your tools.")
            task = "\n\n".join(parts)
            self._observations = []

        self._captured_tool_calls = []

        try:
            # reset=False preserves memory across calls (critical for multi-turn games)
            # First call uses default reset=True, subsequent calls use reset=False
            is_first = not hasattr(self, '_has_run') or not self._has_run
            self._agent.run(task, max_steps=1, reset=is_first)
            self._has_run = True
        except Exception as e:
            # smolagents may raise on max_steps, but we still capture the tool call
            if not self._captured_tool_calls:
                logger.error(f"smolagents error for {self.agent_id}: {e}")

        # Extract action from captured tool calls
        action = self._extract_action()
        logger.info(f"  [{self.agent_id}] smolagents chose: {action.action_type.value} "
                    f"puzzle='{action.puzzle_id}' content='{action.content[:60]}'")
        return action

    def reset(self):
        self._observations = []
        self._captured_tool_calls = []
        self._agent = None
        self._has_run = False

    def _on_step(self, step):
        """Step callback: capture tool calls from each step."""
        if hasattr(step, 'tool_calls') and step.tool_calls:
            self._captured_tool_calls.extend(step.tool_calls)

    def _setup_agent(self):
        """Create the smolagents ToolCallingAgent."""
        model = LiteLLMModel(
            model_id=self.model_name,
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        self._agent = ToolCallingAgent(
            tools=[SubmitAnswerTool(), SendMessageTool(), LookAroundTool()],
            model=model,
            instructions=SYSTEM_PROMPT.format(agent_id=self.agent_id),
            max_steps=1,
            verbosity_level=0,
            step_callbacks=[self._on_step],
        )

    def _extract_action(self) -> AgentAction:
        """Extract an AgentAction from captured tool calls."""
        if not self._captured_tool_calls:
            logger.warning(f"[{self.agent_id}] No tool calls captured, defaulting to LOOK")
            return AgentAction(AgentActionType.LOOK)

        # Use the first tool call
        tc = self._captured_tool_calls[0]
        tool_name = tc.name
        args = tc.arguments if isinstance(tc.arguments, dict) else {}

        if tool_name == "submit_answer":
            return AgentAction(
                AgentActionType.SUBMIT,
                puzzle_id=args.get("puzzle_id", ""),
                content=args.get("answer", ""),
            )
        elif tool_name == "send_message":
            return AgentAction(
                AgentActionType.MESSAGE,
                content=args.get("text", ""),
            )
        elif tool_name == "look_around":
            return AgentAction(AgentActionType.LOOK)
        elif tool_name == "final_answer":
            # smolagents may call final_answer; treat as LOOK
            logger.info(f"[{self.agent_id}] Agent called final_answer, treating as LOOK")
            return AgentAction(AgentActionType.LOOK)
        else:
            logger.warning(f"[{self.agent_id}] Unknown tool: {tool_name}")
            return AgentAction(AgentActionType.LOOK)
