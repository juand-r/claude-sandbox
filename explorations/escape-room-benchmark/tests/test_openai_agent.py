"""
Integration test: OpenAI Agents SDK agent playing through escape rooms.

These tests make real API calls. Run with:
    OPENAI_API_KEY=... python -m pytest tests/test_openai_agent.py -v -s

The -s flag shows print output so you can see the agent's reasoning.
"""

import sys
import os
import json
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import (
    Puzzle, PuzzleType, Room, RoomMetadata, InfoPartition,
)
from src.harness import GameHarness
from agent_wrappers.openai_sdk_agent import OpenAISDKAgent

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(name)s - %(message)s')


def make_simple_cipher_room():
    cipher = Puzzle(
        id="cipher_1",
        puzzle_type=PuzzleType.CIPHER,
        description="Decode the message using the substitution key.",
        info=InfoPartition(
            agent_a_info=["Substitution key: A=M, B=N, C=O, D=P, E=Q"],
            agent_b_info=["Encoded message: MNOPQ"],
            shared_info=["There is a terminal on the wall. Enter the decoded word to solve this puzzle."],
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
        description="One cipher puzzle. You and your teammate must share information to decode a message and escape.",
        puzzles=[cipher],
        metadata=RoomMetadata(optimal_steps=1, optimal_messages=2, difficulty="easy"),
    )


def test_openai_agent_simple_cipher():
    """Two OpenAI agents collaborate to solve a simple cipher room."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set, skipping")
        return

    room = make_simple_cipher_room()
    agent_a = OpenAISDKAgent(name="agent_a", model="gpt-4o-mini")
    agent_b = OpenAISDKAgent(name="agent_b", model="gpt-4o-mini")

    harness = GameHarness(room, agent_a, agent_b, max_turns=12)
    result = harness.run()

    print("\n=== TRIAL RESULT ===")
    print(f"Escaped: {result.escaped}")
    print(f"Total turns: {result.total_turns}")
    print(f"Messages sent: {result.messages_sent}")
    print(f"\nAction log:")
    for entry in result.action_log:
        print(f"  Turn {entry['turn']}: {entry['agent']} {entry['type']} "
              f"target='{entry['target']}' -> {entry['result'][:80]}")
    print(f"\nTranscript:")
    for msg in result.transcript:
        print(f"  [{msg['turn']}] {msg['from']} -> {msg['to']}: {msg['text']}")

    # We expect the agents to escape, but LLMs are non-deterministic
    # so we just check the result is well-formed
    assert result.room_id == "room_01"
    assert isinstance(result.escaped, bool)
    assert result.total_turns > 0
    print(f"\n{'SUCCESS' if result.escaped else 'FAILED'} in {result.total_turns} turns")


if __name__ == "__main__":
    test_openai_agent_simple_cipher()
