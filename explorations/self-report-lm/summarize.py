"""Tables for REPORT.md from the training logs and results/measure_<name>.json.

Usage: python summarize.py <name> [<name> ...]   prints Markdown tables
"""
import json
import sys
from pathlib import Path

RESULTS = Path(__file__).parent / "results"


def log_of(name):
    return {r["step"]: r for r in json.loads((RESULTS / f"{name}.json").read_text())["log"]}


def main():
    names = sys.argv[1:]
    logs = {n: log_of(n) for n in names}
    steps = sorted(set.intersection(*(set(L) for L in logs.values())))
    shown = [s for s in steps if s % 1500 == 0 or s == steps[-1]]
    print("| step | " + " | ".join(f"valid loss, {n}" for n in names) + " |")
    print("|---|" + "---|" * len(names))
    for s in shown:
        print(f"| {s:,} | " + " | ".join(f"{logs[n][s]['valid_loss']:.3f}" for n in names) + " |")
    print()
    keys = [("valid_loss", "validation loss (nats/token)"), ("r2_train", "R², training tokens"),
            ("r2_centred_train", "centred R², training tokens"), ("r2_coord_mean_train", "R² of coordinate means, training tokens"),
            ("r2_held_out", "R², held-out tokens"), ("r2_centred_held_out", "centred R², held-out tokens"),
            ("r2_coord_mean_held_out", "R² of coordinate means, held-out tokens"), ("r2_random", "R², random vectors"),
            ("sum_w", "Σw (number-head weights)")]
    M = {n: json.loads((RESULTS / f"measure_{n}.json").read_text()) for n in names if (RESULTS / f"measure_{n}.json").exists()}
    print("| measure | " + " | ".join(M) + " |")
    print("|---|" + "---|" * len(M))
    for k, label in keys:
        print(f"| {label} | " + " | ".join(f"{M[n][k]:.4f}" for n in M) + " |")
    for part in ("train", "held_out"):
        for k in ("follow", "other", "follow_length", "follow_direction", "ones_mean", "ones_sd"):
            print(f"| {k}, {part} | " + " | ".join(f"{M[n][f'jacobian_{part}'][k]:.4f}" for n in M) + " |")
        print(f"| finite follow median / mean, {part} | " + " | ".join(
            f"{M[n][f'finite_follow_median_{part}']:.4f} / {M[n][f'finite_follow_mean_{part}']:.4f}" for n in M) + " |")
    for n in M:
        rows = M[n]["edit_test"]
        print(f"\nEdit test, {n}: mean report follow {sum(r['report_follow'] for r in rows) / len(rows):.4f}; "
              f"mean KL at t {sum(r['kl_at_t'] for r in rows) / len(rows):.2e}, later in window "
              f"{sum(r['kl_after_t_later'] for r in rows) / len(rows):.2e}, no t {sum(r['kl_no_t'] for r in rows) / len(rows):.2e}")
        for st in M[n]["stories"]:
            print("\n> " + st.replace("\n", " "))


if __name__ == "__main__":
    main()
