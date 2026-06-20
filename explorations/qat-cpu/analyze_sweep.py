#!/usr/bin/env python3
"""
Analyze batch size sweep results.
Reads sweep_qat_bs{8,16,32,64}.csv and prints:
  1. Throughput comparison (tokens/sec, ms/step)
  2. Time-to-perplexity comparison (wall-clock to reach threshold)
  3. Efficiency analysis (tokens processed vs loss)
"""

import csv
import sys
import os

def read_csv(path):
    """Read CSV, return list of dicts with numeric conversion."""
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = {}
            for k, v in row.items():
                try:
                    d[k] = float(v)
                except (ValueError, TypeError):
                    d[k] = v
            rows.append(d)
    return rows


def analyze():
    batch_sizes = [8, 16, 32, 64]
    results = {}

    for bs in batch_sizes:
        path = f"sweep_qat_bs{bs}.csv"
        if not os.path.exists(path):
            print(f"  [skip] {path} not found")
            continue
        data = read_csv(path)
        if not data:
            print(f"  [skip] {path} is empty")
            continue
        results[bs] = data

    if not results:
        print("No data found!")
        return

    # === 1. Throughput ===
    print("=" * 60)
    print("1. THROUGHPUT")
    print("=" * 60)
    print(f"{'BS':>4}  {'tok/step':>10}  {'ms/step':>10}  {'tok/sec':>10}  {'last BPB':>10}")
    print("-" * 60)

    for bs in sorted(results.keys()):
        data = results[bs]
        tok_per_step = bs * 128  # seq_len=128
        # Use last few steps for steady-state timing (skip first which is warmup)
        if len(data) >= 3:
            steady = data[1:]  # skip first step
        else:
            steady = data
        avg_ms = sum(r['ms_per_step'] for r in steady) / len(steady)
        avg_tps = sum(r['tok_per_sec'] for r in steady) / len(steady)
        last_bpb = data[-1]['bpb']
        print(f"{bs:>4}  {tok_per_step:>10}  {avg_ms:>10.1f}  {avg_tps:>10.0f}  {last_bpb:>10.3f}")

    # === 2. Scaling efficiency ===
    print()
    print("=" * 60)
    print("2. BATCH SIZE SCALING")
    print("=" * 60)

    base_bs = min(results.keys())
    base_data = results[base_bs]
    if len(base_data) >= 3:
        base_ms = sum(r['ms_per_step'] for r in base_data[1:]) / len(base_data[1:])
    else:
        base_ms = base_data[-1]['ms_per_step']
    base_tps = base_bs * 128 / (base_ms / 1000)

    print(f"{'BS':>4}  {'ms/step':>10}  {'tok/sec':>10}  {'speedup':>10}  {'efficiency':>10}")
    print("-" * 60)
    for bs in sorted(results.keys()):
        data = results[bs]
        if len(data) >= 3:
            ms = sum(r['ms_per_step'] for r in data[1:]) / len(data[1:])
        else:
            ms = data[-1]['ms_per_step']
        tps = bs * 128 / (ms / 1000)
        speedup = tps / base_tps
        ideal_speedup = bs / base_bs
        efficiency = speedup / ideal_speedup * 100
        print(f"{bs:>4}  {ms:>10.1f}  {tps:>10.0f}  {speedup:>10.2f}x  {efficiency:>9.1f}%")

    # === 3. Time-to-perplexity ===
    print()
    print("=" * 60)
    print("3. TIME-TO-PERPLEXITY (wall-clock seconds to reach threshold)")
    print("=" * 60)

    thresholds = [80, 60, 40, 30, 20, 15, 10]
    print(f"{'BS':>4}", end="")
    for t in thresholds:
        print(f"  {'ppl<'+str(t):>8}", end="")
    print()
    print("-" * (4 + 10 * len(thresholds)))

    for bs in sorted(results.keys()):
        data = results[bs]
        print(f"{bs:>4}", end="")
        for t in thresholds:
            hit = None
            for row in data:
                if row['val_ppl'] < t:
                    hit = row['elapsed_sec']
                    break
            if hit is not None:
                print(f"  {hit:>8.1f}", end="")
            else:
                print(f"  {'---':>8}", end="")
        print()

    # === 4. Loss vs wall-clock ===
    print()
    print("=" * 60)
    print("4. LOSS TRAJECTORY (BPB at selected time points)")
    print("=" * 60)

    # Find max elapsed time across all runs
    max_time = 0
    for data in results.values():
        if data:
            max_time = max(max_time, data[-1]['elapsed_sec'])

    # Time checkpoints
    checkpoints = [30, 60, 120, 180, 300, 600, 900, 1200]
    checkpoints = [c for c in checkpoints if c <= max_time * 1.5]

    if checkpoints:
        print(f"{'BS':>4}", end="")
        for t in checkpoints:
            label = f"{t}s"
            print(f"  {label:>8}", end="")
        print()
        print("-" * (4 + 10 * len(checkpoints)))

        for bs in sorted(results.keys()):
            data = results[bs]
            print(f"{bs:>4}", end="")
            for t in checkpoints:
                # Find closest eval point at or before time t
                best = None
                for row in data:
                    if row['elapsed_sec'] <= t:
                        best = row['bpb']
                if best is not None:
                    print(f"  {best:>8.3f}", end="")
                else:
                    print(f"  {'---':>8}", end="")
            print()

    # === 5. Tokens-to-perplexity ===
    print()
    print("=" * 60)
    print("5. TOKENS-TO-PERPLEXITY (total tokens to reach threshold)")
    print("=" * 60)
    print(f"{'BS':>4}", end="")
    for t in thresholds:
        print(f"  {'ppl<'+str(t):>8}", end="")
    print()
    print("-" * (4 + 10 * len(thresholds)))

    for bs in sorted(results.keys()):
        data = results[bs]
        print(f"{bs:>4}", end="")
        for t in thresholds:
            hit = None
            for row in data:
                if row['val_ppl'] < t:
                    hit = row['tokens_seen']
                    break
            if hit is not None:
                print(f"  {hit/1e6:>7.2f}M", end="")
            else:
                print(f"  {'---':>8}", end="")
        print()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    analyze()
