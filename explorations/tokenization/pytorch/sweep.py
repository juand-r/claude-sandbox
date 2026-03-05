"""
sweep.py - Sweep factored embedding dimensions.

Equivalent to sweep_factored.sh but in Python.

Usage:
  python sweep.py --phase din --mode binary
  python sweep.py --phase dout --mode bigram
  python sweep.py --phase all
  python sweep.py --phase din --mode binary --device cuda
"""

import argparse
import csv
import os
import sys

from train_tok import TrainConfig, train, MODE_CONFIG


RESULTS_DIR = "factored_results"
SUMMARY_FILE = os.path.join(RESULTS_DIR, "summary.csv")
D_VALUES = [4, 8, 16, 32, 64, 128]
DIM = 128

SUMMARY_HEADER = [
    "phase", "mode", "vocab", "tok_per_char", "seq_len",
    "d_in", "d_out", "n_params", "bpc", "loss", "ppl",
    "time_sec", "random_bpc",
]


def ensure_summary():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    if not os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(SUMMARY_HEADER)


def already_done(phase, mode, d_in, d_out):
    """Check if this config already has a row in the summary."""
    if not os.path.exists(SUMMARY_FILE):
        return False
    with open(SUMMARY_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row["phase"] == phase and row["mode"] == mode
                    and row["d_in"] == str(d_in) and row["d_out"] == str(d_out)):
                return True
    return False


def append_summary(phase, mode, vocab, tpc, seq_len, d_in, d_out,
                   n_params, bpc, loss, ppl, time_sec, random_bpc):
    with open(SUMMARY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            phase, mode, vocab, f"{tpc:.1f}", seq_len,
            d_in, d_out, n_params,
            f"{bpc:.3f}", f"{loss:.4f}", f"{ppl:.2f}",
            f"{time_sec:.1f}", f"{random_bpc:.2f}",
        ])


def run_one(phase, mode, d_in, d_out, device, n_steps):
    mcfg = MODE_CONFIG[mode]
    print(f"\n=== {phase}: mode={mode} d_in={d_in} d_out={d_out} ===")

    if already_done(phase, mode, d_in, d_out):
        print(f"  Already done, skipping.")
        return

    csv_path = os.path.join(
        RESULTS_DIR, f"{mode}_din{d_in}_dout{d_out}.csv"
    )

    cfg = TrainConfig(
        mode=mode,
        d_in=d_in,
        d_out=d_out,
        device=device,
        n_steps=n_steps,
        csv_path=csv_path,
    )

    final_bpc, final_loss, final_ppl, total_time = train(cfg)

    from train_tok import random_baseline_bpc, get_seq_len
    rbpc = random_baseline_bpc(mode)
    seq_len = get_seq_len(mode, cfg.char_context)

    append_summary(
        phase, mode, mcfg["vocab"], mcfg["tpc_f"], seq_len,
        d_in, d_out, 0,  # n_params printed in train output
        final_bpc, final_loss, final_ppl, total_time, rbpc,
    )


def get_modes(mode_filter):
    if mode_filter == "binary":
        return ["binary"]
    elif mode_filter == "bigram":
        return ["bigram"]
    else:
        return ["binary", "bigram"]


def main():
    parser = argparse.ArgumentParser(description="Factored embedding sweep")
    parser.add_argument("--phase", type=str, default="all",
                        choices=["din", "dout", "all"])
    parser.add_argument("--mode", type=str, default="",
                        choices=["binary", "bigram", ""],
                        help="Filter to one mode (default: both)")
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--n_steps", type=int, default=3000)
    parser.add_argument("--d_values", type=str, default="4,8,16,32,64,128",
                        help="Comma-separated d values to sweep")
    args = parser.parse_args()

    d_values = [int(x) for x in args.d_values.split(",")]
    modes = get_modes(args.mode)
    ensure_summary()

    if args.phase in ("din", "all"):
        print("=" * 44)
        print(f"Phase 1: Sweeping d_in (d_out={DIM} fixed)")
        print("=" * 44)
        for mode in modes:
            for d_in in d_values:
                run_one("din_sweep", mode, d_in, DIM, args.device, args.n_steps)

    if args.phase in ("dout", "all"):
        print("=" * 44)
        print(f"Phase 2: Sweeping d_out (d_in={DIM} fixed)")
        print("=" * 44)
        for mode in modes:
            for d_out in d_values:
                run_one("dout_sweep", mode, DIM, d_out, args.device, args.n_steps)

    print("\n" + "=" * 44)
    print("Sweep complete.")
    print(f"Summary: {SUMMARY_FILE}")
    print("=" * 44)

    # Print summary
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE) as f:
            print(f.read())


if __name__ == "__main__":
    main()
