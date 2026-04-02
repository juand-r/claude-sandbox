"""
Scripted agent for deterministic testing of the harness.

Takes a list of pre-defined actions and executes them in order.
Used to verify the engine, channel, and harness work correctly
without any LLM calls.
"""

from .agent import BaseAgent, AgentAction


class ScriptedAgent(BaseAgent):
    """
    Agent that follows a hardcoded action script.

    Usage:
        script = [
            AgentAction(AgentActionType.MESSAGE, content="The key is A=X"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="a"),
        ]
        agent = ScriptedAgent("test_agent", script)
    """

    def __init__(self, name: str, script: list[AgentAction]):
        super().__init__(name=name)
        self.script = script
        self._step = 0
        self.observations: list[str] = []

    def set_role(self, agent_id: str, initial_observation: str):
        self.agent_id = agent_id
        self.observations.append(initial_observation)

    def observe(self, text: str):
        self.observations.append(text)

    def act(self) -> AgentAction:
        if self._step >= len(self.script):
            raise RuntimeError(
                f"ScriptedAgent '{self.name}' ran out of scripted actions "
                f"at step {self._step}. Script has {len(self.script)} actions."
            )
        action = self.script[self._step]
        self._step += 1
        return action

    def reset(self):
        self._step = 0
        self.observations = []
