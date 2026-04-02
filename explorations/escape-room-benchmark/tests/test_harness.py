"""Tests for the game harness using scripted agents."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import (
    Puzzle, PuzzleType, Room, RoomMetadata, InfoPartition,
)
from src.agent import AgentAction, AgentActionType
from src.scripted_agent import ScriptedAgent
from src.harness import GameHarness


def make_simple_cipher_room():
    cipher = Puzzle(
        id="cipher_1",
        puzzle_type=PuzzleType.CIPHER,
        description="Decode the message using the substitution key.",
        info=InfoPartition(
            agent_a_info=["Substitution key: A=M, B=N, C=O, D=P, E=Q"],
            agent_b_info=["Encoded message: MNOPQ"],
            shared_info=["There is a terminal on the wall expecting a decoded word."],
            load_bearing_tokens={
                "agent_a": ["Substitution key: A=M, B=N, C=O, D=P, E=Q"],
                "agent_b": ["Encoded message: MNOPQ"],
            },
        ),
        solution="abcde",
    )
    return Room(
        id="room_01",
        name="Simple Cipher Room",
        description="One cipher puzzle. Share info to decode.",
        puzzles=[cipher],
        metadata=RoomMetadata(optimal_steps=1, optimal_messages=2, difficulty="easy"),
    )


def make_dependency_room():
    p1 = Puzzle(
        id="cipher_1",
        puzzle_type=PuzzleType.CIPHER,
        description="Decode the letter.",
        info=InfoPartition(
            agent_a_info=["Key: A=X"],
            agent_b_info=["Encoded: X"],
            shared_info=["There is a locked terminal."],
            load_bearing_tokens={"agent_a": ["Key: A=X"], "agent_b": ["Encoded: X"]},
        ),
        solution="a",
        on_solve_reveals={
            "both": ["A drawer opens revealing a note that says: 7"],
            "agent_a": ["On the back of the note you see: 3"],
        },
    )
    p2 = Puzzle(
        id="code_1",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="Enter the 2-digit code on the door keypad.",
        info=InfoPartition(
            agent_a_info=[],
            agent_b_info=[],
            shared_info=["There is a keypad on the door requiring a 2-digit code."],
            load_bearing_tokens={"agent_a": ["digit 3"]},
        ),
        solution="73",
        depends_on=["cipher_1"],
    )
    return Room(
        id="room_02",
        name="Dependency Room",
        description="Solve the cipher to unlock the code puzzle.",
        puzzles=[p1, p2],
        metadata=RoomMetadata(optimal_steps=2, optimal_messages=3, difficulty="medium"),
    )


class TestHarnessSimpleRoom:
    def test_optimal_playthrough(self):
        """Agents share info and solve in minimal turns."""
        room = make_simple_cipher_room()

        # A sends key to B, B sends encoded text to A, then A submits
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE, content="The substitution key is A=M, B=N, C=O, D=P, E=Q"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="abcde"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE, content="The encoded message is MNOPQ"),
        ])

        harness = GameHarness(room, agent_a, agent_b, max_turns=20)
        result = harness.run()

        assert result.escaped is True
        assert result.messages_sent == 2
        assert result.total_turns == 3  # A msg, B msg, A submit

    def test_wrong_then_correct(self):
        """Agent submits wrong answer first, then correct."""
        room = make_simple_cipher_room()

        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="wrong"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="abcde"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.LOOK),  # just wastes a turn
        ])

        harness = GameHarness(room, agent_a, agent_b, max_turns=20)
        result = harness.run()

        assert result.escaped is True
        assert result.total_turns == 3  # A wrong, B look, A correct

    def test_budget_exhaustion(self):
        """Agents run out of turns without solving."""
        room = make_simple_cipher_room()

        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.LOOK),
            AgentAction(AgentActionType.LOOK),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.LOOK),
            AgentAction(AgentActionType.LOOK),
        ])

        harness = GameHarness(room, agent_a, agent_b, max_turns=3)
        result = harness.run()

        assert result.escaped is False
        assert result.total_turns == 3


class TestHarnessDependencyRoom:
    def test_full_playthrough(self):
        """Agents solve cipher, get reveals, then solve code."""
        room = make_dependency_room()

        # A: share key, solve cipher, share "3" from reveal, do nothing
        # B: share encoded text, do nothing, submit 73
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE, content="Key: A=X"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="a"),
            AgentAction(AgentActionType.MESSAGE, content="I see the number 3 on the back of the note"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE, content="Encoded: X"),
            AgentAction(AgentActionType.MESSAGE, content="I see the note says 7"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="73"),
        ])

        harness = GameHarness(room, agent_a, agent_b, max_turns=20)
        result = harness.run()

        assert result.escaped is True
        assert result.messages_sent == 4

    def test_reveals_delivered_to_other_agent(self):
        """When A solves cipher, B gets the 'both' reveals."""
        room = make_dependency_room()

        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="a"),
            AgentAction(AgentActionType.LOOK),  # filler
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.LOOK),  # will have received reveal
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="73"),
        ])

        harness = GameHarness(room, agent_a, agent_b, max_turns=20)
        result = harness.run()

        assert result.escaped is True
        # Check that agent B received the reveal
        assert any("7" in obs for obs in agent_b.observations)


class TestHarnessResult:
    def test_result_has_all_fields(self):
        room = make_simple_cipher_room()
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="abcde"),
        ])
        agent_b = ScriptedAgent("B", [])

        harness = GameHarness(room, agent_a, agent_b, max_turns=20)
        result = harness.run()

        assert result.room_id == "room_01"
        assert result.escaped is True
        assert result.timestamp != ""
        d = result.to_dict()
        assert "action_log" in d
        assert "transcript" in d

    def test_action_log_populated(self):
        room = make_simple_cipher_room()
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="wrong"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="abcde"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.LOOK),
        ])

        harness = GameHarness(room, agent_a, agent_b, max_turns=20)
        result = harness.run()

        assert len(result.action_log) == 3  # wrong submit, look, correct submit
