"""Tests for metric computation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Puzzle, PuzzleType, Room, RoomMetadata, InfoPartition
from src.agent import AgentAction, AgentActionType
from src.scripted_agent import ScriptedAgent
from src.harness import GameHarness
from src.metrics import compute_metrics
from rooms.room_definitions import get_room


class TestMetrics:
    def test_optimal_playthrough_metrics(self):
        """Optimal scripted play should give efficiency ratios near 1.0."""
        room = get_room("room_02_code")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE, content="1st: 7, 3rd: 2"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="7329"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE, content="2nd: 3, 4th: 9"),
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        profile = compute_metrics(result, room)

        assert profile.success is True
        assert profile.step_efficiency == 1.0  # 1 submit / 1 optimal
        assert profile.message_efficiency == 1.0  # 2 messages / 2 optimal
        assert profile.redundancy_score == 0.0

    def test_suboptimal_playthrough_metrics(self):
        """Extra turns should increase efficiency ratios."""
        room = get_room("room_02_code")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.LOOK),  # wasted turn
            AgentAction(AgentActionType.MESSAGE, content="1st: 7, 3rd: 2"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="wrong"),  # wrong
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="7329"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.LOOK),  # wasted
            AgentAction(AgentActionType.MESSAGE, content="2nd: 3, 4th: 9"),
            AgentAction(AgentActionType.LOOK),  # wasted
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        profile = compute_metrics(result, room)

        assert profile.success is True
        assert profile.step_efficiency > 1.0  # more actions than optimal
        assert profile.message_efficiency == 1.0  # still 2 messages

    def test_failed_playthrough_metrics(self):
        """Failed attempt should show success=False."""
        room = get_room("room_02_code")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.LOOK),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.LOOK),
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=2).run()
        profile = compute_metrics(result, room)

        assert profile.success is False
        assert profile.total_turns == 2

    def test_redundancy_detection(self):
        """Both agents attempting the same puzzle should be flagged."""
        room = get_room("room_02_code")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="1234"),  # wrong
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="7329"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="5678"),  # also wrong
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        profile = compute_metrics(result, room)

        assert profile.redundancy_score == 1.0  # both agents tried code_1
