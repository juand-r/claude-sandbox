#!/usr/bin/env python3
"""AI Jam Session -- 5 LLM agents improvise music together."""

import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import SessionConfig, LLMConfig
from agents import Agent
from midi_utils import format_history_for_prompt, parse_measure, build_midi_file


INSTRUMENTS = ["piano", "bass", "drums", "vibraphone", "strings"]


def run_jam(config: SessionConfig) -> str:
    """Run a full jam session and return the path to the output MIDI file."""

    # Initialize agents
    agents = {inst: Agent(inst, config) for inst in INSTRUMENTS}

    # Shared history: instrument -> list of text measures
    history: dict[str, list[str]] = {inst: [] for inst in INSTRUMENTS}

    bpr = config.beats_per_round
    unit_label = "measures" if bpr == config.beats_per_measure else f"{bpr}-beat segments"
    print(f"Starting jam session: {config.num_rounds} rounds ({unit_label})")
    print(f"  Tempo: {config.tempo} BPM | Key: {config.key} | Style: {config.style}")
    print(f"  Beats per round: {bpr}")
    print(f"  LLM: {config.llm.provider} / {config.llm.model}")
    print(f"  Band: {', '.join(INSTRUMENTS)}")
    print()

    for round_idx in range(config.num_rounds):
        round_start = time.time()
        print(f"Round {round_idx + 1}/{config.num_rounds}...", end=" ", flush=True)

        # Build shared context from history
        history_text = format_history_for_prompt(history, round_idx)

        # Call all agents in parallel
        round_results: dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(agents[inst].generate_measure, history_text, round_idx): inst
                for inst in INSTRUMENTS
            }
            for future in as_completed(futures):
                inst = futures[future]
                try:
                    measure_text = future.result()
                    round_results[inst] = measure_text
                except Exception as e:
                    print(f"\n  ERROR [{inst}]: {e}")
                    # Generate a silent measure as fallback
                    round_results[inst] = f"REST 0.0 {config.beats_per_round}.0"

        # Append to history
        for inst in INSTRUMENTS:
            history[inst].append(round_results[inst])

        elapsed = time.time() - round_start
        # Quick validation: count notes per instrument
        note_counts = []
        for inst in INSTRUMENTS:
            events = parse_measure(round_results[inst], inst, config.beats_per_round)
            note_counts.append(f"{inst}:{len(events)}")
        print(f"done ({elapsed:.1f}s) [{', '.join(note_counts)}]")

    # Build MIDI file
    print(f"\nBuilding MIDI file: {config.output_file}")
    mid = build_midi_file(history, config)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.output_file)
    mid.save(output_path)
    print(f"Saved to {output_path}")

    # Print summary
    total_notes = 0
    for inst in INSTRUMENTS:
        inst_notes = sum(len(parse_measure(m, inst, config.beats_per_round)) for m in history[inst])
        total_notes += inst_notes
        print(f"  {inst}: {inst_notes} notes across {config.num_rounds} rounds")
    print(f"  Total: {total_notes} notes")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="AI Jam Session")
    parser.add_argument("--rounds", type=int, default=8, help="Number of rounds")
    parser.add_argument("--beats-per-round", type=int, default=None,
                        help="Beats per round (default: full measure, e.g. 4 for 4/4). Use 1 or 2 for finer granularity.")
    parser.add_argument("--tempo", type=int, default=120, help="Tempo in BPM")
    parser.add_argument("--key", type=str, default="C minor", help="Key signature")
    parser.add_argument("--style", type=str, default="jazz fusion with a relaxed groove", help="Style description")
    parser.add_argument("--provider", type=str, default="anthropic", choices=["anthropic", "openai"], help="LLM provider")
    parser.add_argument("--model", type=str, default=None, help="LLM model name (default depends on provider)")
    parser.add_argument("--output", type=str, default="jam_output.mid", help="Output MIDI file name")
    args = parser.parse_args()

    # Set model default based on provider
    if args.model is None:
        if args.provider == "anthropic":
            args.model = "claude-sonnet-4-20250514"
        else:
            args.model = "gpt-4o-mini"

    config = SessionConfig(
        tempo=args.tempo,
        key=args.key,
        num_rounds=args.rounds,
        beats_per_round=args.beats_per_round,
        style=args.style,
        llm=LLMConfig(provider=args.provider, model=args.model),
        output_file=args.output,
    )

    run_jam(config)


if __name__ == "__main__":
    main()
