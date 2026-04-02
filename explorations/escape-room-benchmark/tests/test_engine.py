"""Tests for the game engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import (
    Puzzle, PuzzleType, Room, RoomMetadata, InfoPartition,
    Action, ActionType,
)
from src.engine import RoomEngine


def make_simple_cipher_room():
    """Single cipher puzzle."""
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
        description="One cipher puzzle. Agents must share info to decode.",
        puzzles=[cipher],
        metadata=RoomMetadata(optimal_steps=1, optimal_messages=2, difficulty="easy"),
    )


def make_dependency_room():
    """Two puzzles: cipher_1 -> code_1."""
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


class TestEngineStart:
    def test_start_returns_observations(self):
        engine = RoomEngine(make_simple_cipher_room())
        obs_a, obs_b = engine.start()
        assert "Agent A" in obs_a.text
        assert "Agent B" in obs_b.text

    def test_start_partitions_info(self):
        engine = RoomEngine(make_simple_cipher_room())
        obs_a, obs_b = engine.start()
        # A gets the key
        assert "Substitution key" in obs_a.text
        assert "Encoded message" not in obs_a.text
        # B gets the encoded message
        assert "Encoded message" in obs_b.text
        assert "Substitution key" not in obs_b.text

    def test_start_shows_shared_info(self):
        engine = RoomEngine(make_simple_cipher_room())
        obs_a, obs_b = engine.start()
        assert "terminal" in obs_a.text.lower()
        assert "terminal" in obs_b.text.lower()

    def test_dependency_room_only_shows_initial_puzzles(self):
        engine = RoomEngine(make_dependency_room())
        obs_a, obs_b = engine.start()
        assert "cipher_1" in obs_a.text
        assert "code_1" not in obs_a.text  # not available yet


class TestEngineSubmit:
    def test_correct_answer_solves_puzzle(self):
        engine = RoomEngine(make_simple_cipher_room())
        engine.start()
        action = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="abcde")
        obs = engine.submit_action(action)
        assert obs.puzzle_solved == "cipher_1"
        assert obs.room_escaped is True
        assert engine.is_escaped

    def test_wrong_answer_does_not_solve(self):
        engine = RoomEngine(make_simple_cipher_room())
        engine.start()
        action = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="wrong")
        obs = engine.submit_action(action)
        assert obs.puzzle_solved is None
        assert "incorrect" in obs.text.lower() or "wrong" in obs.text.lower()
        assert not engine.is_escaped

    def test_case_insensitive_solution(self):
        engine = RoomEngine(make_simple_cipher_room())
        engine.start()
        action = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="ABCDE")
        obs = engine.submit_action(action)
        assert obs.puzzle_solved == "cipher_1"

    def test_cannot_solve_locked_puzzle(self):
        engine = RoomEngine(make_dependency_room())
        engine.start()
        action = Action("agent_a", ActionType.SUBMIT, target="code_1", content="73")
        obs = engine.submit_action(action)
        assert obs.puzzle_solved is None
        assert "not yet available" in obs.text.lower()

    def test_cannot_solve_already_solved(self):
        engine = RoomEngine(make_simple_cipher_room())
        engine.start()
        action = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="abcde")
        engine.submit_action(action)
        obs = engine.submit_action(action)
        assert "already solved" in obs.text.lower()

    def test_nonexistent_puzzle(self):
        engine = RoomEngine(make_simple_cipher_room())
        engine.start()
        action = Action("agent_a", ActionType.SUBMIT, target="fake_puzzle", content="x")
        obs = engine.submit_action(action)
        assert "no puzzle" in obs.text.lower()


class TestEngineDependencyChain:
    def test_solving_p1_unlocks_p2(self):
        engine = RoomEngine(make_dependency_room())
        engine.start()

        # Solve cipher_1
        action = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="a")
        obs = engine.submit_action(action)
        assert obs.puzzle_solved == "cipher_1"
        assert not obs.room_escaped
        assert "code_1" in obs.text  # new puzzle revealed

        # Now code_1 should be available
        available = engine.get_available_puzzles()
        assert any(p.id == "code_1" for p in available)

    def test_full_playthrough(self):
        engine = RoomEngine(make_dependency_room())
        engine.start()

        # Solve cipher_1
        action1 = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="a")
        obs1 = engine.submit_action(action1)
        assert obs1.puzzle_solved == "cipher_1"
        assert "drawer" in obs1.text.lower()  # on_solve_reveals

        # Solve code_1
        action2 = Action("agent_b", ActionType.SUBMIT, target="code_1", content="73")
        obs2 = engine.submit_action(action2)
        assert obs2.puzzle_solved == "code_1"
        assert obs2.room_escaped is True
        assert engine.is_escaped

    def test_on_solve_reveals_private_info(self):
        engine = RoomEngine(make_dependency_room())
        engine.start()

        action = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="a")
        obs = engine.submit_action(action)

        # Agent A (the solver) should see both "both" and "agent_a" reveals
        assert "7" in obs.text  # from "both"
        assert "3" in obs.text  # from "agent_a"

    def test_other_agent_reveals(self):
        engine = RoomEngine(make_dependency_room())
        engine.start()

        action = Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="a")
        engine.submit_action(action)

        puzzle = engine.room.get_puzzle("cipher_1")
        other_reveals = engine.get_other_agent_reveals(puzzle, "agent_a")
        # Agent B should get the "both" reveals but NOT agent_a's private reveals
        assert any("7" in r for r in other_reveals)
        assert not any("3" in r for r in other_reveals)


class TestEngineLook:
    def test_look_shows_available_puzzles(self):
        engine = RoomEngine(make_dependency_room())
        engine.start()
        action = Action("agent_a", ActionType.LOOK)
        obs = engine.submit_action(action)
        assert "cipher_1" in obs.text

    def test_look_shows_solved_puzzles(self):
        engine = RoomEngine(make_dependency_room())
        engine.start()
        engine.submit_action(Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="a"))
        obs = engine.submit_action(Action("agent_a", ActionType.LOOK))
        assert "cipher_1" in obs.text  # in solved list
        assert "code_1" in obs.text    # available


class TestEngineActionLog:
    def test_actions_are_logged(self):
        engine = RoomEngine(make_simple_cipher_room())
        engine.start()
        engine.submit_action(Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="wrong"))
        engine.submit_action(Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="abcde"))
        log = engine.get_action_log()
        assert len(log) == 2
        assert log[0]["turn"] == 1
        assert log[1]["turn"] == 2
        assert log[0]["puzzle_solved"] is None
        assert log[1]["puzzle_solved"] == "cipher_1"

    def test_message_action_raises(self):
        engine = RoomEngine(make_simple_cipher_room())
        engine.start()
        try:
            engine.submit_action(Action("agent_a", ActionType.MESSAGE, content="hello"))
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "channel" in str(e).lower()
