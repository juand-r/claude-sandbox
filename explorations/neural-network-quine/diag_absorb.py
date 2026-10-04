"""After a quine's weights are changed, does a repair procedure keep the change
or undo it? (IDEAS.md section 10, "matching restored after a change")

Start from a settled network (damped Newton had stalled there). Change its
weights by a random Δ, then run damped Newton (Levenberg–Marquardt) on 1 − R² for
a few iterations. Compare the final weights with a control run from the
unchanged network:

  retention r = <θ_final − θ_control, Δ> / |Δ|²   (1: change kept, 0: undone)
  other drift = |θ_final − θ_control − r Δ| / |Δ|

Also report the singular values of J − I at the start: near-zero ones mark
directions in which the outputs follow a change of the weights (J v ≈ v).

Usage: python diag_absorb.py
"""
import json
from pathlib import Path

import torch

import newton
import quine as q

START = "results/weights/lmnorm_L1_seed0_cont80.pt"
ITERS = 10
SIZES = (0.01, 0.10)          # |Δ| / |θ|
OUT = Path(__file__).parent / "results" / "diag_absorb.json"
WEIGHTS = Path(__file__).parent / "results" / "weights"


def save_progress(results):
    """Write results after every run, so a restart loses at most one run."""
    OUT.write_text(json.dumps(results, indent=1))


def load():
    m, _ = q.load_weights(START, dtype=torch.float64)
    return m


def repair(delta, name):
    m = load()
    settings = q.load_weights(START)[1]["settings"]
    with torch.no_grad():
        m.theta.add_(delta)
    r2_after_change = q.replication_stats(m)["r2"]
    log = newton.lm(m, ITERS, normalized=True)
    q.save_weights(m, WEIGHTS / f"{name}.pt", settings, extra={"source": START, "experiment": "diag_absorb"})
    return m.theta.detach().clone(), r2_after_change, [row["r2"] for row in log]


def main():
    torch.set_num_threads(4)
    base = load()
    theta0 = base.theta.detach().clone()
    results = {"start": START, "iterations": ITERS}

    A = newton.jacobian(base, theta0)
    A.diagonal().sub_(1.0)
    sv = torch.linalg.svdvals(A)
    del A
    results["singular_values_J_minus_I"] = {
        "largest": sv[0].item(), "smallest_10": sv[-10:].tolist(),
        "count_below": {str(t): int((sv < t).sum()) for t in (1e-3, 1e-2, 1e-1, 1.0)}}
    print("singular values of J − I:", results["singular_values_J_minus_I"], flush=True)
    save_progress(results)

    print("control (no change)", flush=True)
    theta_ctrl, _, r2_ctrl = repair(torch.zeros_like(theta0), "absorb_control")
    results["control"] = {"r2": r2_ctrl, "moved": (theta_ctrl - theta0).norm().item() / theta0.norm().item()}
    save_progress(results)

    gen = torch.Generator().manual_seed(0)
    results["runs"] = []
    for size in SIZES:
        delta = torch.randn(len(theta0), generator=gen, dtype=torch.float64)
        delta *= size * theta0.norm() / delta.norm()
        print(f"change of size {size:.0%}", flush=True)
        theta_f, r2_changed, r2_log = repair(delta, f"absorb_change{size:g}")
        diff = theta_f - theta_ctrl
        r = (diff @ delta / (delta @ delta)).item()
        other = (diff - r * delta).norm().item() / delta.norm().item()
        results["runs"].append({"size": size, "r2_before": r2_ctrl[0], "r2_after_change": r2_changed,
                                "r2_log": r2_log, "retention": r, "other_drift": other})
        print(f"  R² before {r2_ctrl[0]:.4f}, after change {r2_changed:.4f}, after repair {r2_log[-1]:.4f}; "
              f"retention {r:.4f}, other drift {other:.4f}", flush=True)
        save_progress(results)
    OUT.write_text(json.dumps(results, indent=1))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
