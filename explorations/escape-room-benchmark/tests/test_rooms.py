"""
Tests for room definitions: verify each room has a valid solution
via scripted optimal playthroughs.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Action, ActionType
from src.engine import RoomEngine
from src.agent import AgentAction, AgentActionType
from src.scripted_agent import ScriptedAgent
from src.harness import GameHarness
from rooms.room_definitions import get_room, get_all_rooms


class TestRoom1Cipher:
    def test_engine_direct(self):
        room = get_room("room_01_cipher")
        engine = RoomEngine(room)
        obs_a, obs_b = engine.start()

        # A has the Caesar shift info, B has the encoded message
        assert "caesar" in obs_a.text.lower() or "shift" in obs_a.text.lower()
        assert "KHOOR ZRUOG" in obs_b.text

        # KHOOR ZRUOG with Caesar shift -3: K->H, H->E, O->L, O->L, R->O = HELLO
        # Z->W, R->O, U->R, O->L, G->D = WORLD
        result = engine.submit_action(
            Action("agent_a", ActionType.SUBMIT, target="cipher_1", content="hello world")
        )
        assert result.puzzle_solved == "cipher_1"
        assert result.room_escaped is True

    def test_scripted_playthrough(self):
        room = get_room("room_01_cipher")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE, content="Caesar cipher, shifted forward by 3. Shift back to decode."),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="cipher_1", content="hello world"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE, content="Encoded message is KHOOR ZRUOG"),
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        assert result.escaped is True
        assert result.total_turns == 3


class TestRoom2Code:
    def test_engine_direct(self):
        room = get_room("room_02_code")
        engine = RoomEngine(room)
        obs_a, obs_b = engine.start()

        assert "1st digit: 7" in obs_a.text
        assert "2nd digit: 3" in obs_b.text

        result = engine.submit_action(
            Action("agent_a", ActionType.SUBMIT, target="code_1", content="7329")
        )
        assert result.puzzle_solved == "code_1"
        assert result.room_escaped is True

    def test_scripted_playthrough(self):
        room = get_room("room_02_code")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE, content="I have 1st: 7, 3rd: 2"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="code_1", content="7329"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE, content="I have 2nd: 3, 4th: 9"),
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        assert result.escaped is True


class TestRoom3Study:
    def test_cipher_solution(self):
        # RSHQ with shift-3 backward: R->O, S->P, H->E, Q->N = OPEN
        room = get_room("room_03_study")
        engine = RoomEngine(room)
        engine.start()

        result = engine.submit_action(
            Action("agent_a", ActionType.SUBMIT, target="study_cipher", content="open")
        )
        assert result.puzzle_solved == "study_cipher"
        assert "drawer" in result.text.lower()
        assert "58" in result.text

    def test_full_playthrough(self):
        room = get_room("room_03_study")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE, content="Cipher is shift-3. Each letter shifted forward by 3."),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="study_cipher", content="open"),
            AgentAction(AgentActionType.MESSAGE, content="Drawer says first two digits: 58"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE, content="Encoded text is RSHQ"),
            AgentAction(AgentActionType.MESSAGE, content="Last two digits: 14"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="study_code", content="5814"),
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        assert result.escaped is True


class TestRoom4Safes:
    def test_both_safes(self):
        room = get_room("room_04_safes")
        engine = RoomEngine(room)
        engine.start()

        # Red safe: C_T with "feline" hint -> CAT
        result1 = engine.submit_action(
            Action("agent_a", ActionType.SUBMIT, target="safe_left", content="cat")
        )
        assert result1.puzzle_solved == "safe_left"

        # Blue safe: D_G with "canine" hint -> DOG
        result2 = engine.submit_action(
            Action("agent_b", ActionType.SUBMIT, target="safe_right", content="dog")
        )
        assert result2.puzzle_solved == "safe_right"
        assert result2.room_escaped is True

    def test_scripted_playthrough(self):
        room = get_room("room_04_safes")
        # Both agents share info about both safes, then each opens one
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE,
                        content="Red safe: first letter C, hint 'feline'. Blue safe: last letter G."),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="safe_left", content="cat"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE,
                        content="Red safe: middle letter A. Blue safe: first letter D, hint 'canine'."),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="safe_right", content="dog"),
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        assert result.escaped is True
        assert result.messages_sent == 2


class TestRoom5Archive:
    def test_cipher_solution(self):
        # Reverse alphabet: A=Z, B=Y, ..., it's symmetric.
        # VAULT: V->E, A->Z, U->F, L->O, T->G = EZFOG
        # So decoding EZFOG: E->V, Z->A, F->U, O->L, G->T = VAULT
        room = get_room("room_05_archive")
        engine = RoomEngine(room)
        obs_a, obs_b = engine.start()

        assert "EZFOG" in obs_b.text

        result = engine.submit_action(
            Action("agent_a", ActionType.SUBMIT, target="archive_cipher", content="vault")
        )
        assert result.puzzle_solved == "archive_cipher"
        assert "cabinet" in result.text.lower()

    def test_grid_lookup(self):
        room = get_room("room_05_archive")
        engine = RoomEngine(room)
        engine.start()

        # Solve cipher first
        engine.submit_action(
            Action("agent_a", ActionType.SUBMIT, target="archive_cipher", content="vault")
        )

        # Grid: Row 3, Col 4 = 42
        result = engine.submit_action(
            Action("agent_a", ActionType.SUBMIT, target="archive_grid", content="42")
        )
        assert result.puzzle_solved == "archive_grid"

    def test_full_playthrough(self):
        room = get_room("room_05_archive")
        agent_a = ScriptedAgent("A", [
            AgentAction(AgentActionType.MESSAGE, content="I have a reverse-alphabet decoder ring."),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="archive_cipher", content="vault"),
            AgentAction(AgentActionType.MESSAGE, content="Cabinet open! Map says find code at ROW,COL. I see Row: 3"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="archive_grid", content="42"),
            AgentAction(AgentActionType.SUBMIT, puzzle_id="archive_exit", content="42"),
        ])
        agent_b = ScriptedAgent("B", [
            AgentAction(AgentActionType.MESSAGE, content="Encoded word: EZFOG"),
            AgentAction(AgentActionType.MESSAGE, content="I have Column: 4. Ignoring scratched note about row 1, your info is more reliable."),
            AgentAction(AgentActionType.LOOK),  # filler while A submits grid
            AgentAction(AgentActionType.LOOK),  # filler while A submits exit
        ])
        result = GameHarness(room, agent_a, agent_b, max_turns=20).run()
        assert result.escaped is True

    def test_structure(self):
        room = get_room("room_05_archive")
        engine = RoomEngine(room)
        obs_a, obs_b = engine.start()

        assert "archive_cipher" in obs_a.text
        assert "archive_grid" not in obs_a.text
        assert "archive_exit" not in obs_a.text


class TestAllRooms:
    def test_all_rooms_load(self):
        rooms = get_all_rooms()
        assert len(rooms) == 5

    def test_room_ids_unique(self):
        rooms = get_all_rooms()
        ids = [r.id for r in rooms]
        assert len(ids) == len(set(ids))

    def test_all_rooms_have_metadata(self):
        for room in get_all_rooms():
            assert room.metadata.difficulty in ("easy", "medium", "hard")
            assert room.metadata.optimal_steps > 0
            assert room.metadata.optimal_messages >= 0
