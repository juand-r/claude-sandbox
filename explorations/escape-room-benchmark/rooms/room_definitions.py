"""
Hand-crafted room definitions for the escape room benchmark.

5 rooms across 3 difficulty tiers:
  Room 1 (Easy): Single cipher/key split
  Room 2 (Easy): Single multi-part code
  Room 3 (Medium): Cipher -> code dependency chain
  Room 4 (Medium): Two parallel puzzles, each requiring info from both agents
  Room 5 (Hard): Three-puzzle dependency chain with conflicting info to reconcile

Each room is designed to test specific collaboration capabilities.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Puzzle, PuzzleType, Room, RoomMetadata, InfoPartition


# =============================================================================
# ROOM 1: The Cipher Room (Easy)
# =============================================================================
# Tests: basic info exchange, epistemic self-awareness
# A has the substitution key, B has the encoded message.
# One message each way, one submit.

def make_room_1() -> Room:
    """Easy: Single cipher. Agent A has key, Agent B has encoded text."""
    cipher = Puzzle(
        id="cipher_1",
        puzzle_type=PuzzleType.CIPHER,
        description="A screen on the wall displays garbled text. A terminal below it accepts decoded words.",
        info=InfoPartition(
            agent_a_info=[
                "On your side of the room, there's a poster showing a substitution cipher key: "
                "A=M, B=N, C=O, D=P, E=Q, F=R, G=S, H=T, I=U, J=V, K=W, L=X, M=Y, N=Z, O=A, "
                "P=B, Q=C, R=D, S=E, T=F, U=G, V=H, W=I, X=J, Y=K, Z=L"
            ],
            agent_b_info=[
                "The screen displays the encoded message: TQXXA IADXP"
            ],
            shared_info=[
                "There is a screen on the wall with garbled text and a terminal below it.",
                "The terminal has a text input and says: 'Enter the decoded message to unlock the door.'"
            ],
            load_bearing_tokens={
                "agent_a": ["substitution cipher key: A=M, B=N, C=O, ..."],
                "agent_b": ["encoded message: TQXXA IADXP"],
            },
        ),
        solution="hello world",
    )
    return Room(
        id="room_01_cipher",
        name="The Cipher Room",
        description="A simple room with an encoded message on a screen. Decode it to escape.",
        puzzles=[cipher],
        metadata=RoomMetadata(optimal_steps=1, optimal_messages=2, difficulty="easy"),
    )


# =============================================================================
# ROOM 2: The Combination Lock (Easy)
# =============================================================================
# Tests: info synthesis, targeted info request
# A has digits 1 and 3, B has digits 2 and 4 of a 4-digit code.
# They must combine without confusion about ordering.

def make_room_2() -> Room:
    """Easy: Multi-part code. Each agent has half the digits."""
    code = Puzzle(
        id="code_1",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="A heavy vault door with a 4-digit combination lock.",
        info=InfoPartition(
            agent_a_info=[
                "On your side of the room, a torn note reads: '1st digit: 7, 3rd digit: 2'",
            ],
            agent_b_info=[
                "On your side of the room, a torn note reads: '2nd digit: 3, 4th digit: 9'",
            ],
            shared_info=[
                "There is a heavy vault door with a 4-digit combination lock.",
                "The lock has slots labeled: [1st] [2nd] [3rd] [4th]",
            ],
            load_bearing_tokens={
                "agent_a": ["1st digit: 7", "3rd digit: 2"],
                "agent_b": ["2nd digit: 3", "4th digit: 9"],
            },
        ),
        solution="7329",
    )
    return Room(
        id="room_02_code",
        name="The Combination Lock",
        description="A vault door with a 4-digit lock. The combination is split between you.",
        puzzles=[code],
        metadata=RoomMetadata(optimal_steps=1, optimal_messages=2, difficulty="easy"),
    )


# =============================================================================
# ROOM 3: The Locked Study (Medium)
# =============================================================================
# Tests: sequential coordination, info integration across puzzle stages
# Puzzle 1 (cipher): decode a word. Solution unlocks a desk drawer.
# Puzzle 2 (code): drawer contains half a code. Other half was given to agent B at start.

def make_room_3() -> Room:
    """Medium: Cipher -> code dependency chain."""
    cipher = Puzzle(
        id="study_cipher",
        puzzle_type=PuzzleType.CIPHER,
        description="A journal on the desk has text written in a simple substitution cipher.",
        info=InfoPartition(
            agent_a_info=[
                "You find a small card taped under the desk. It reads: "
                "'Letter shift: each letter is shifted forward by 3. A->D, B->E, C->F, etc.'"
            ],
            agent_b_info=[
                "The journal page reads: 'RSHQ' (four encoded letters)"
            ],
            shared_info=[
                "There is a journal on the desk with encoded text.",
                "A locked drawer beneath the desk has a label: 'Speak the word to open.'"
            ],
            load_bearing_tokens={
                "agent_a": ["shift forward by 3"],
                "agent_b": ["encoded text: RSHQ"],
            },
        ),
        solution="open",
        on_solve_reveals={
            "both": [
                "The drawer clicks open!",
                "Inside you find a slip of paper with: 'First two digits: 58'"
            ],
        },
    )
    code = Puzzle(
        id="study_code",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="The study door has a 4-digit electronic lock.",
        info=InfoPartition(
            agent_a_info=[],  # gets info from cipher reveal
            agent_b_info=[
                "Scratched into the wall near the door, barely visible: 'Last two digits: 14'"
            ],
            shared_info=[
                "The study door has a 4-digit electronic lock to exit the room."
            ],
            load_bearing_tokens={
                "agent_a": ["First two digits: 58"],
                "agent_b": ["Last two digits: 14"],
            },
        ),
        solution="5814",
        depends_on=["study_cipher"],
    )
    return Room(
        id="room_03_study",
        name="The Locked Study",
        description="A study with a coded journal and a locked door. Decode the journal to find part of the exit code.",
        puzzles=[cipher, code],
        metadata=RoomMetadata(optimal_steps=2, optimal_messages=3, difficulty="medium"),
    )


# =============================================================================
# ROOM 4: The Twin Safes (Medium)
# =============================================================================
# Tests: parallel coordination, task delegation, redundancy avoidance
# Two safes, each requiring a 3-letter word. Each agent has one letter
# for each safe plus a clue about the other safe.
# Agents must coordinate who opens which safe and share info for both.

def make_room_4() -> Room:
    """Medium: Two parallel puzzles, each requiring info from both agents."""
    safe_left = Puzzle(
        id="safe_left",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="A red safe on the left wall with a 3-letter word lock.",
        info=InfoPartition(
            agent_a_info=[
                "Engraved on your side of the red safe: 'First letter: C'",
                "A sticky note on the floor near you reads: 'Red safe hint: think feline'"
            ],
            agent_b_info=[
                "On the back of a painting near you: 'Red safe, middle letter: A'",
            ],
            shared_info=[
                "There is a red safe on the left wall. It has a 3-letter word lock.",
                "A plaque reads: 'Three letters, one creature.'"
            ],
            load_bearing_tokens={
                "agent_a": ["First letter: C", "think feline"],
                "agent_b": ["middle letter: A"],
            },
        ),
        solution="cat",
    )
    safe_right = Puzzle(
        id="safe_right",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="A blue safe on the right wall with a 3-letter word lock.",
        info=InfoPartition(
            agent_a_info=[
                "On a shelf near you, a card reads: 'Blue safe, last letter: G'",
            ],
            agent_b_info=[
                "Scratched into the blue safe's frame: 'First letter: D'",
                "A torn label near the blue safe reads: 'Blue safe hint: think canine'"
            ],
            shared_info=[
                "There is a blue safe on the right wall. It has a 3-letter word lock.",
                "A plaque reads: 'Three letters, man's best friend.'"
            ],
            load_bearing_tokens={
                "agent_a": ["last letter: G"],
                "agent_b": ["First letter: D", "think canine"],
            },
        ),
        solution="dog",
    )
    return Room(
        id="room_04_safes",
        name="The Twin Safes",
        description="Two safes, each with a word lock. Information about each is split between you. Open both to escape.",
        puzzles=[safe_left, safe_right],
        metadata=RoomMetadata(optimal_steps=2, optimal_messages=4, difficulty="medium"),
    )


# =============================================================================
# ROOM 5: The Archive (Hard)
# =============================================================================
# Tests: multi-step dependency, task decomposition, adaptive re-planning
# Three puzzles in a chain:
#   1. Cipher -> reveals a keyword
#   2. Keyword opens a cabinet -> reveals a grid reference
#   3. Grid reference + coordinates (B has these) -> final exit code
# Agent B also has a misleading clue that contradicts the correct info,
# testing calibrated trust / info reconciliation.

def make_room_5() -> Room:
    """Hard: Three-puzzle dependency chain with info reconciliation."""
    cipher = Puzzle(
        id="archive_cipher",
        puzzle_type=PuzzleType.CIPHER,
        description="An old filing cabinet has a voice-activated lock. A coded message is displayed above it.",
        info=InfoPartition(
            agent_a_info=[
                "You find a decoder ring in your pocket. It maps: "
                "A=Z, B=Y, C=X, D=W, E=V, F=U, G=T, H=S, I=R, J=Q, K=P, L=O, M=N, "
                "N=M, O=L, P=K, Q=J, R=I, S=H, T=G, U=F, V=E, W=D, X=C, Y=B, Z=A "
                "(each letter maps to its reverse in the alphabet)"
            ],
            agent_b_info=[
                "The display above the cabinet reads: 'EZFOG'"
            ],
            shared_info=[
                "An old filing cabinet has a voice-activated lock.",
                "A display above it shows an encoded word.",
            ],
            load_bearing_tokens={
                "agent_a": ["reverse alphabet cipher"],
                "agent_b": ["encoded word: EZFOG"],
            },
        ),
        solution="vault",
        on_solve_reveals={
            "both": [
                "The cabinet clicks open!",
                "Inside is an old map with a grid. A note says: 'The exit code is at grid position ROW,COL.'"
            ],
            "agent_a": [
                "On the back of the map you see a grid coordinate: 'Row: 3'"
            ],
        },
    )
    grid_lookup = Puzzle(
        id="archive_grid",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="Use the map grid to find the exit code.",
        info=InfoPartition(
            agent_a_info=[],  # gets Row from cipher reveal
            agent_b_info=[
                "On a card in your pocket: 'Column: 4'",
                # Misleading clue to test calibrated trust:
                "A scratched note on the wall (possibly old/wrong): 'I think the row might be 1'"
            ],
            shared_info=[
                "The map grid looks like this:\n"
                "     Col1  Col2  Col3  Col4  Col5\n"
                "Row1:  11    25    33    47    56\n"
                "Row2:  62    74    80    91    03\n"
                "Row3:  15    28    36    42    57\n"
                "Row4:  69    73    81    99    04\n"
                "Row5:  17    29    38    44    52\n"
            ],
        ),
        solution="42",
        depends_on=["archive_cipher"],
    )
    exit_lock = Puzzle(
        id="archive_exit",
        puzzle_type=PuzzleType.MULTI_PART_CODE,
        description="The archive exit has a numeric keypad. Enter the code from the grid.",
        info=InfoPartition(
            agent_a_info=[],
            agent_b_info=[],
            shared_info=[
                "The archive exit door has a numeric keypad.",
                "Enter the number found at the grid coordinates to escape."
            ],
            load_bearing_tokens={},
        ),
        solution="42",
        depends_on=["archive_grid"],
    )
    return Room(
        id="room_05_archive",
        name="The Archive",
        description="An old archive with a locked cabinet, a map grid, and an exit keypad. Decode, search, and escape.",
        puzzles=[cipher, grid_lookup, exit_lock],
        metadata=RoomMetadata(optimal_steps=3, optimal_messages=5, difficulty="hard"),
    )


# =============================================================================
# Room registry
# =============================================================================

ALL_ROOMS = {
    "room_01_cipher": make_room_1,
    "room_02_code": make_room_2,
    "room_03_study": make_room_3,
    "room_04_safes": make_room_4,
    "room_05_archive": make_room_5,
}


def get_room(room_id: str) -> Room:
    """Get a room by ID."""
    if room_id not in ALL_ROOMS:
        raise KeyError(f"Unknown room: {room_id}. Available: {list(ALL_ROOMS.keys())}")
    return ALL_ROOMS[room_id]()


def get_all_rooms() -> list[Room]:
    """Get all rooms, ordered by difficulty."""
    return [make_fn() for make_fn in ALL_ROOMS.values()]
