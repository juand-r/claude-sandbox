"""
Closing the self-regulation loop (nested feedback, made dynamic).

Run:  python experiments_selfreg.py   -> selfreg_results.png + summary

The agent emits a "check-in" when its *felt* idle time crosses a threshold; the
check-in feeds back as a self-event (resetting the idle clock and counting as
activity). With no external input this becomes a self-paced rhythm (a limit cycle).
Background activity lowers the attention gate and resets the idle clock, so it
SUPPRESSES and stretches the rhythm: the agent checks in less when much is happening.

  A. Check-in raster across background event rate.
  B. Check-in rate vs background rate (context-gated self-pacing).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from oscillators import Params, TimePerceptionSystem
from experiments import poisson_events

DURATION = 120.0
THRESHOLD = 8.0          # felt-idle seconds before a check-in


def run_selfreg(lambda_bg, threshold=THRESHOLD, duration=DURATION, seed=0):
    """Return (check_in_times, external_event_times). Check-ins feed back as events."""
    sys = TimePerceptionSystem(Params(seed=seed))
    rng = np.random.default_rng(seed)
    ext = sorted(poisson_events(duration, max(lambda_bg, 1e-9), rng))
    ei = 0
    checks = []
    n_steps = int(round(duration / sys.p.dt))
    for _ in range(n_steps):
        while ei < len(ext) and ext[ei] <= sys.t + sys.p.dt:
            sys.event(1.0)
            ei += 1
        sys.step()
        if sys.felt_idle() >= threshold:
            sys.event(1.0)          # check-in feeds back as a self-event
            checks.append(sys.t)
    return np.asarray(checks), np.asarray(ext)


def main():
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))

    # --- A. raster ----------------------------------------------------------
    rates = [0.0, 0.1, 0.3, 1.0]
    for i, lam in enumerate(rates):
        checks, ext = run_selfreg(lam, seed=1)
        ax[0].plot(checks, np.full_like(checks, i), "|", ms=12, color="C0")
        ax[0].plot(ext, np.full_like(ext, i + 0.3), "|", ms=6, color="C3", alpha=0.5)
    ax[0].set(yticks=range(len(rates)), yticklabels=[f"bg={r}" for r in rates],
              xlabel="time (s)", title="A. Check-ins (blue) vs external events (red)")

    # --- B. check-in rate vs background -------------------------------------
    bg = np.linspace(0, 1.5, 16)
    n_check, n_check_nofb = [], []
    for lam in bg:
        nc = np.mean([len(run_selfreg(lam, seed=s)[0]) for s in range(6)])
        n_check.append(nc / DURATION)
    ax[1].plot(bg, n_check, "o-")
    # Reference: a fully idle agent self-paces at ~1 check-in per THRESHOLD seconds.
    ax[1].axhline(1.0 / THRESHOLD, color="grey", ls="--", lw=0.8,
                  label=f"idle self-pace = 1/{THRESHOLD:g}s")
    ax[1].set(xlabel="background event rate (1/s)", ylabel="check-in rate (1/s)",
              title="B. Context suppresses the self-paced rhythm")
    ax[1].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig("selfreg_results.png", dpi=120)

    # --- summary ------------------------------------------------------------
    idle_checks, _ = run_selfreg(0.0, seed=1)
    intervals = np.diff(idle_checks)
    print("=== self-regulation loop ===")
    print(f"  idle self-paced interval: mean {intervals.mean():.2f}s  std {intervals.std():.3f}s "
          f"(threshold {THRESHOLD:g}s) -> regular limit cycle")
    print(f"  check-in rate at bg=0.0: {len(run_selfreg(0.0)[0])/DURATION:.3f}/s")
    print(f"  check-in rate at bg=1.0: {len(run_selfreg(1.0)[0])/DURATION:.3f}/s  (suppressed)")
    print("\nsaved selfreg_results.png")


if __name__ == "__main__":
    main()
