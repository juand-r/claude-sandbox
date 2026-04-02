"""Tests for the data model layer."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import (
    Puzzle, PuzzleType, Room, RoomMetadata, InfoPartition,
    AgentState, Action, ActionType, Observation,
)


def make_simple_cipher_room():
    """Helper: single cipher puzzle room for testing."""
    cipher = Puzzle(
        id="cipher_1",
        puzzle_type=PuzzleType.CIPHER,
        description="A substitution cipher. Agent A has the key, Agent B has the encoded text.",
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
    """Helper: two puzzles where puzzle_2 depends on puzzle_1."""
    p1 = Puzzle(
        id="cipher_1",
        puzzle_type=PuzzleType.CIPHER,
        description="First cipher",
        info=InfoPartition(
            agent_a_info=["Key: A=X"],
            agent_b_info=["Encoded: X"],
            shared_info=["Solve this first."],
            load_bearing_tokens={"agent_a": ["Key: A=X"], "agent_b": ["Encoded: X"]},
        ),
        solution="a",
        on_solve_reveals={
            "both": ["A drawer opens. Inside is a note with the number 7."],
            "agent_a": ["You notice the note has a faint 3 written on the back."],
        },
    )
    p2 = Puzzle(
        id="code_1",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="Enter a 2-digit code",
        info=InfoPartition(
            agent_a_info=[],   # gets info from p1's on_solve_reveals
            agent_b_info=["You recall the code ends with a digit you'll learn later."],
            shared_info=["There is a keypad on the door."],
            load_bearing_tokens={"agent_a": ["digit 3"]},
        ),
        solution="73",
        depends_on=["cipher_1"],
    )
    return Room(
        id="room_02",
        name="Dependency Room",
        description="Cipher unlocks info for a code puzzle.",
        puzzles=[p1, p2],
        metadata=RoomMetadata(optimal_steps=2, optimal_messages=3, difficulty="medium"),
    )


class TestInfoPartition:
    def test_cipher_room_partition(self):
        room = make_simple_cipher_room()
        cipher = room.get_puzzle("cipher_1")

        # Agent A should see the key but NOT the encoded message
        assert any("key" in info.lower() for info in cipher.info.agent_a_info)
        assert not any("encoded" in info.lower() for info in cipher.info.agent_a_info)

        # Agent B should see the encoded message but NOT the key
        assert any("encoded" in info.lower() for info in cipher.info.agent_b_info)
        assert not any("key" in info.lower() for info in cipher.info.agent_b_info)

        # Both should see shared info
        assert len(cipher.info.shared_info) > 0

    def test_load_bearing_tokens_exist(self):
        room = make_simple_cipher_room()
        cipher = room.get_puzzle("cipher_1")
        assert "agent_a" in cipher.info.load_bearing_tokens
        assert "agent_b" in cipher.info.load_bearing_tokens
        assert len(cipher.info.load_bearing_tokens["agent_a"]) > 0
        assert len(cipher.info.load_bearing_tokens["agent_b"]) > 0


class TestRoom:
    def test_get_puzzle(self):
        room = make_simple_cipher_room()
        p = room.get_puzzle("cipher_1")
        assert p.id == "cipher_1"

    def test_get_puzzle_not_found(self):
        room = make_simple_cipher_room()
        try:
            room.get_puzzle("nonexistent")
            assert False, "Should have raised KeyError"
        except KeyError:
            pass

    def test_initial_puzzles(self):
        room = make_dependency_room()
        initial = room.get_initial_puzzles()
        assert len(initial) == 1
        assert initial[0].id == "cipher_1"

    def test_unlocked_puzzles(self):
        room = make_dependency_room()
        # Nothing solved: only cipher_1 available
        unlocked = room.get_unlocked_puzzles(set())
        assert [p.id for p in unlocked] == ["cipher_1"]

        # cipher_1 solved: code_1 becomes available
        unlocked = room.get_unlocked_puzzles({"cipher_1"})
        assert [p.id for p in unlocked] == ["code_1"]

        # Both solved: nothing left
        unlocked = room.get_unlocked_puzzles({"cipher_1", "code_1"})
        assert unlocked == []

    def test_is_escaped(self):
        room = make_dependency_room()
        assert not room.is_escaped(set())
        assert not room.is_escaped({"cipher_1"})
        assert room.is_escaped({"cipher_1", "code_1"})


class TestAgentState:
    def test_accumulates_info(self):
        state = AgentState(agent_id="agent_a", private_info=["Key: A=X"])
        assert len(state.private_info) == 1

        obs = Observation(text="A drawer opens.", revealed_info=["Note says: 7"])
        state.add_observation(obs)
        assert len(state.observations) == 1
        assert "Note says: 7" in state.private_info

    def test_message_tracking(self):
        state = AgentState(agent_id="agent_a")
        state.add_received_message("agent_b", "The encoded text is MNOPQ", turn=1)
        assert len(state.messages_received) == 1
        assert state.messages_received[0]["from"] == "agent_b"
        assert state.messages_received[0]["turn"] == 1

    def test_action_recording(self):
        state = AgentState(agent_id="agent_a")
        action = Action(agent_id="agent_a", action_type=ActionType.SUBMIT,
                        target="cipher_1", content="abcde")
        state.record_action(action)
        assert len(state.actions_taken) == 1
        assert state.actions_taken[0].target == "cipher_1"
