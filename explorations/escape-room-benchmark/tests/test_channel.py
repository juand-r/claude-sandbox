"""Tests for the communication channel."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.channel import Channel


class TestChannelBasic:
    def test_send_and_receive(self):
        ch = Channel(max_turns=20)
        ch.send("agent_a", "Hello B")
        msgs = ch.get_new_messages("agent_b")
        assert len(msgs) == 1
        assert msgs[0].text == "Hello B"
        assert msgs[0].from_agent == "agent_a"
        assert msgs[0].to_agent == "agent_b"

    def test_bidirectional(self):
        ch = Channel(max_turns=20)
        ch.send("agent_a", "msg 1")
        ch.send("agent_b", "msg 2")
        ch.send("agent_a", "msg 3")

        # B should have 2 messages from A
        all_to_b = ch.get_all_messages("agent_b")
        assert len(all_to_b) == 2

        # A should have 1 message from B
        all_to_a = ch.get_all_messages("agent_a")
        assert len(all_to_a) == 1

    def test_new_messages_only(self):
        ch = Channel(max_turns=20)
        ch.send("agent_a", "msg 1")
        msgs1 = ch.get_new_messages("agent_b")
        assert len(msgs1) == 1

        # No new messages yet
        msgs2 = ch.get_new_messages("agent_b")
        assert len(msgs2) == 0

        # Send another
        ch.send("agent_a", "msg 2")
        msgs3 = ch.get_new_messages("agent_b")
        assert len(msgs3) == 1
        assert msgs3[0].text == "msg 2"

    def test_agents_dont_see_own_messages(self):
        ch = Channel(max_turns=20)
        ch.send("agent_a", "hello")
        msgs = ch.get_new_messages("agent_a")
        assert len(msgs) == 0


class TestChannelTurnBudget:
    def test_turn_counting(self):
        ch = Channel(max_turns=3)
        ch.send("agent_a", "1")
        ch.send("agent_b", "2")
        assert ch.turn_count == 2
        assert ch.budget_remaining == 1
        assert not ch.budget_exhausted

    def test_budget_enforced(self):
        ch = Channel(max_turns=2)
        assert ch.send("agent_a", "1") is True
        assert ch.send("agent_b", "2") is True
        assert ch.budget_exhausted
        assert ch.send("agent_a", "3") is False
        assert ch.total_messages == 2  # third message not added

    def test_zero_budget(self):
        ch = Channel(max_turns=0)
        assert ch.budget_exhausted
        assert ch.send("agent_a", "x") is False


class TestChannelTranscript:
    def test_transcript_format(self):
        ch = Channel(max_turns=20)
        ch.send("agent_a", "Hello")
        ch.send("agent_b", "Hi there")
        transcript = ch.get_transcript()
        assert len(transcript) == 2
        assert transcript[0]["from"] == "agent_a"
        assert transcript[0]["to"] == "agent_b"
        assert transcript[0]["turn"] == 1
        assert transcript[1]["from"] == "agent_b"
        assert transcript[1]["turn"] == 2

    def test_empty_transcript(self):
        ch = Channel(max_turns=20)
        assert ch.get_transcript() == []

    def test_messages_by_agent(self):
        ch = Channel(max_turns=20)
        ch.send("agent_a", "msg 1")
        ch.send("agent_b", "msg 2")
        ch.send("agent_a", "msg 3")
        a_msgs = ch.get_messages_by_agent("agent_a")
        assert len(a_msgs) == 2
        b_msgs = ch.get_messages_by_agent("agent_b")
        assert len(b_msgs) == 1
