#!/usr/bin/env python3
"""
Escape Room Benchmark — CLI runner.

Usage:
    python run_benchmark.py --agent openai_sdk --model gpt-4o-mini --rooms all
    python run_benchmark.py --agent openai_sdk --model gpt-4o --rooms room_01_cipher,room_03_study
    python run_benchmark.py --agent openai_sdk --rooms all --trials 3
    python run_benchmark.py --agent openai_sdk --rooms all --max-turns 15
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime

from src.harness import GameHarness, TrialResult
from src.metrics import compute_metrics, print_results_table, MetricProfile
from rooms.room_definitions import get_room, get_all_rooms, ALL_ROOMS


def create_agent(agent_type: str, model: str, name: str):
    """Factory: create an agent by type."""
    if agent_type == "openai_sdk":
        from agent_wrappers.openai_sdk_agent import OpenAISDKAgent
        return OpenAISDKAgent(name=name, model=model)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}. Available: openai_sdk")


def run_trial(room_id: str, agent_type: str, model: str, max_turns: int) -> tuple[TrialResult, MetricProfile]:
    """Run a single trial and compute metrics."""
    room = get_room(room_id)
    agent_a = create_agent(agent_type, model, name="agent_a")
    agent_b = create_agent(agent_type, model, name="agent_b")

    harness = GameHarness(room, agent_a, agent_b, max_turns=max_turns)
    result = harness.run()
    profile = compute_metrics(result, room)
    return result, profile


def main():
    parser = argparse.ArgumentParser(description="Escape Room Agent Benchmark")
    parser.add_argument("--agent", type=str, default="openai_sdk",
                        help="Agent type (default: openai_sdk)")
    parser.add_argument("--model", type=str, default="gpt-4o-mini",
                        help="LLM model name (default: gpt-4o-mini)")
    parser.add_argument("--rooms", type=str, default="all",
                        help="Comma-separated room IDs, or 'all' (default: all)")
    parser.add_argument("--trials", type=int, default=1,
                        help="Number of trials per room (default: 1)")
    parser.add_argument("--max-turns", type=int, default=20,
                        help="Max turns per trial (default: 20)")
    parser.add_argument("--log-dir", type=str, default="logs",
                        help="Directory for trial logs (default: logs)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose logging")

    args = parser.parse_args()

    # Set up logging
    log_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
    )

    # Parse room list
    if args.rooms == "all":
        room_ids = list(ALL_ROOMS.keys())
    else:
        room_ids = [r.strip() for r in args.rooms.split(",")]

    # Create log directory
    os.makedirs(args.log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"Escape Room Benchmark")
    print(f"Agent: {args.agent} | Model: {args.model} | Rooms: {len(room_ids)} | "
          f"Trials: {args.trials} | Max turns: {args.max_turns}")
    print()

    all_profiles: list[MetricProfile] = []
    all_results: list[dict] = []

    for room_id in room_ids:
        for trial_num in range(1, args.trials + 1):
            trial_label = f"{room_id} (trial {trial_num}/{args.trials})"
            print(f"Running {trial_label}...", end=" ", flush=True)

            try:
                result, profile = run_trial(room_id, args.agent, args.model, args.max_turns)
                all_profiles.append(profile)

                status = "ESCAPED" if result.escaped else "FAILED"
                print(f"{status} in {result.total_turns} turns, {result.messages_sent} messages")

                # Save detailed log
                log_entry = {
                    "room_id": room_id,
                    "trial": trial_num,
                    "agent": args.agent,
                    "model": args.model,
                    "max_turns": args.max_turns,
                    "result": result.to_dict(),
                    "metrics": profile.to_dict(),
                }
                all_results.append(log_entry)

            except Exception as e:
                print(f"ERROR: {e}")
                logging.exception(f"Trial failed: {trial_label}")

    # Print results table
    print()
    print_results_table(all_profiles)

    # Save all results to JSON
    log_file = os.path.join(args.log_dir, f"benchmark_{timestamp}_{args.agent}_{args.model}.json")
    with open(log_file, "w") as f:
        json.dump({
            "config": {
                "agent": args.agent,
                "model": args.model,
                "rooms": room_ids,
                "trials": args.trials,
                "max_turns": args.max_turns,
            },
            "results": all_results,
        }, f, indent=2)
    print(f"\nDetailed logs saved to: {log_file}")


if __name__ == "__main__":
    main()
