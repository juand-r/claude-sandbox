#!/usr/bin/env python3
"""
Presidential Actions Dashboard — Pipeline Runner

Usage:
    python run_pipeline.py           # Run all phases
    python run_pipeline.py --phase 1 # Scrape only
    python run_pipeline.py --phase 2 # Enrich only
    python run_pipeline.py --phase 3 # Verify only
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Presidential Actions Data Pipeline")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4],
                        help="Run a specific phase (default: all)")
    args = parser.parse_args()

    phases = [args.phase] if args.phase else [1, 2, 3, 4]

    for phase in phases:
        print(f"\n{'='*60}")
        print(f"  PHASE {phase}")
        print(f"{'='*60}\n")

        if phase == 1:
            from scrape_miller_center import run_phase1
            run_phase1()
        elif phase == 2:
            from enrich import run_phase2
            run_phase2()
        elif phase == 3:
            from verify import run_verification
            run_verification()
        elif phase == 4:
            from score import run_phase4
            run_phase4()

    if not args.phase:
        print(f"\n{'='*60}")
        print(f"  PIPELINE COMPLETE")
        print(f"{'='*60}")
        print(f"\nFinal dataset: data/scored/events_scored.csv")


if __name__ == "__main__":
    main()
