"""
OpenAI Agents SDK wrapper for the escape room benchmark.

Wraps the OpenAI Agents SDK into our BaseAgent interface.
The agent uses tool-calling to decide between submitting answers
and messaging its teammate.

The SDK agent has a real reasoning loop — it receives observations,
reasons about what to do, and selects a tool (action) to execute.
We use tool_use_behavior="stop_on_first_tool" so the agent stops
after making one tool call, which we intercept as the agent's action.
"""

import os
import logging
import json

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# "agents" is the openai-agents SDK package
from agents import Agent, Runner, function_tool, RunResult, ModelSettings
from src.agent import BaseAgent, AgentAction, AgentActionType

logger = logging.getLogger(__name__)

# --- System prompt template ---

SYSTEM_PROMPT = """You are an AI agent in a collaborative escape room puzzle.

## Your Situation
- You are {agent_id} working with a teammate to escape a room.
- You each have DIFFERENT private information. Neither of you can solve the room alone.
- You must communicate with your teammate to share information and coordinate.

## Available Actions (pick exactly ONE per turn)

1. **submit_answer(puzzle_id, answer)** — Submit an answer to a puzzle. Only do this when you are confident.
2. **send_message(text)** — Send a message to your teammate. Use this to share info or ask questions.
3. **look_around()** — Examine the room to see available puzzles and current state.

## Rules
- You MUST call exactly one tool on each turn. Do not just respond with text.
- Be concise in messages.
- Share only what's relevant; don't dump everything at once.
- Don't submit an answer unless you have enough information to be confident.
- Pay close attention to what your teammate tells you.
"""


class OpenAISDKAgent(BaseAgent):
    """
    Agent backed by the OpenAI Agents SDK.

    Uses tool-calling to decide between game actions.
    We stop after the first tool call and intercept it as the agent's action.
    """

    def __init__(self, name: str = "openai_sdk", model: str = "gpt-4o-mini"):
        super().__init__(name=name)
        self.model = model
        self._observations: list[str] = []
        self._conversation_history: list[dict] = []
        self._agent: Agent | None = None

    def set_role(self, agent_id: str, initial_observation: str):
        self.agent_id = agent_id
        self._observations = [initial_observation]
        self._conversation_history = []
        self._setup_agent()

    def observe(self, text: str):
        self._observations.append(text)

    def act(self) -> AgentAction:
        """
        Run the SDK agent for one step. Collects all pending observations
        into a user message, calls the agent, and intercepts the tool call.
        """
        # Build the user message from accumulated observations
        if not self._observations:
            user_msg = "It's your turn. What would you like to do? You MUST call one of your tools."
        else:
            parts = self._observations.copy()
            parts.append("\nIt's your turn. Choose an action by calling one of your tools.")
            user_msg = "\n\n".join(parts)
            self._observations = []

        self._conversation_history.append({
            "role": "user",
            "content": user_msg,
        })

        try:
            result = Runner.run_sync(
                self._agent,
                input=self._conversation_history,
                max_turns=1,  # stop after one model call
            )

            action = self._extract_action(result)

            # Update history for next turn
            self._conversation_history = result.to_input_list()

            logger.info(f"  [{self.agent_id}] SDK chose: {action.action_type.value} "
                        f"puzzle='{action.puzzle_id}' content='{action.content[:60]}'")
            return action

        except Exception as e:
            logger.error(f"OpenAI SDK agent error for {self.agent_id}: {e}", exc_info=True)
            return AgentAction(AgentActionType.LOOK)

    def reset(self):
        self._observations = []
        self._conversation_history = []
        self._agent = None

    def _setup_agent(self):
        """Create the SDK Agent with our tools and system prompt."""
        self._agent = Agent(
            name=f"EscapeRoom_{self.agent_id}",
            instructions=SYSTEM_PROMPT.format(agent_id=self.agent_id),
            tools=[submit_answer, send_message, look_around],
            model=self.model,
            model_settings=ModelSettings(temperature=0.2),
            tool_use_behavior="stop_on_first_tool",
        )

    def _extract_action(self, result: RunResult) -> AgentAction:
        """
        Extract the agent's action from the RunResult.

        With stop_on_first_tool, the result contains the tool call info.
        We inspect result.raw_responses to find which tool was called.
        """
        # Check the raw responses for tool calls
        for response in result.raw_responses:
            if hasattr(response, 'output') and response.output:
                for item in response.output:
                    if hasattr(item, 'type') and item.type == 'function_call':
                        return self._parse_tool_call(item.name, item.arguments)

        # If no tool call found, check if the final output encodes an action
        output = result.final_output or ""
        if output.startswith("ACTION:"):
            return self._parse_action_string(output)

        logger.warning(f"[{self.agent_id}] No tool call found in result, defaulting to LOOK. "
                       f"final_output: {output[:200]}")
        return AgentAction(AgentActionType.LOOK)

    def _parse_tool_call(self, tool_name: str, arguments: str) -> AgentAction:
        """Parse a tool call name and arguments into an AgentAction."""
        try:
            args = json.loads(arguments) if isinstance(arguments, str) else arguments
        except json.JSONDecodeError:
            args = {}

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
        else:
            logger.warning(f"Unknown tool: {tool_name}")
            return AgentAction(AgentActionType.LOOK)

    def _parse_action_string(self, output: str) -> AgentAction:
        """Parse an ACTION: encoded string (fallback)."""
        if output.startswith("ACTION:SUBMIT:"):
            parts = output.split(":", 3)
            if len(parts) >= 4:
                return AgentAction(AgentActionType.SUBMIT, puzzle_id=parts[2], content=parts[3])
        elif output.startswith("ACTION:MESSAGE:"):
            return AgentAction(AgentActionType.MESSAGE, content=output[len("ACTION:MESSAGE:"):])
        elif output.startswith("ACTION:LOOK"):
            return AgentAction(AgentActionType.LOOK)
        return AgentAction(AgentActionType.LOOK)


# --- Tool definitions (module-level for the SDK) ---

@function_tool
def submit_answer(puzzle_id: str, answer: str) -> str:
    """Submit an answer to a puzzle. Use this when you are confident in your answer.

    Args:
        puzzle_id: The ID of the puzzle to submit the answer for (e.g., 'cipher_1', 'code_1').
        answer: Your answer to the puzzle.
    """
    return f"ACTION:SUBMIT:{puzzle_id}:{answer}"


@function_tool
def send_message(text: str) -> str:
    """Send a message to your teammate. Use this to share information, ask questions, or coordinate.

    Args:
        text: The message to send to your teammate.
    """
    return f"ACTION:MESSAGE:{text}"


@function_tool
def look_around() -> str:
    """Look around the room to see what puzzles are available and what has been solved."""
    return "ACTION:LOOK"
