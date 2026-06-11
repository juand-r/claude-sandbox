"""
Robustness of the holiday-paradox dissociation (Stage 1 engine).

Run:  python robustness.py   -> robustness_results.png + summary

Is the dissociation a knife-edge or a robust regime? We sweep how much happens
(event rate) over a fixed 60 s window and check that:
  - prospective felt time DECREASES with event rate (busy flies), and
  - retrospective load INCREASES with event rate (busy remembered longer),
monotonically and across a range of gate parameters.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from oscillators import Params, TimePerceptionSystem
from experiments import poisson_events

WINDOW = 60.0
N_SEED = 8


def sweep_rate(rates, params_kw=None, seeds=N_SEED):
    """Mean felt-time and load over the window vs event rate, averaged over seeds."""
    params_kw = params_kw or {}
    felt, load = [], []
    for lam in rates:
        fs, ls = [], []
        for s in range(seeds):
            rng = np.random.default_rng(s)
            ev = poisson_events(WINDOW, max(lam, 1e-6), rng)
            rec = TimePerceptionSystem(Params(seed=s, **params_kw)).run(WINDOW, ev)
            fs.append(rec["tau"][-1]); ls.append(rec["load"][-1])
        felt.append(np.mean(fs)); load.append(np.mean(ls))
    return np.asarray(felt), np.asarray(load)


def main():
    rates = np.linspace(0.05, 8.0, 16)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))

    # --- A. dissociation across rate ----------------------------------------
    felt, load = sweep_rate(rates)
    ax0 = ax[0]; ax0b = ax0.twinx()
    l1, = ax0.plot(rates, felt, "o-", color="C0", label="prospective felt (s)")
    l2, = ax0b.plot(rates, load, "s-", color="C3", label="retrospective load")
    ax0.axhline(WINDOW, color="grey", ls="--", lw=0.6)
    ax0.set(xlabel="event rate (1/s)", ylabel="felt time (s)",
            title="A. Dissociation is monotonic, not a knife-edge")
    ax0b.set_ylabel("retrospective load")
    ax0.legend(handles=[l1, l2], fontsize=8, loc="center right")

    # --- B. prospective robustness to gate_k --------------------------------
    for gk in [0.5, 1.0, 1.5, 3.0]:
        f, _ = sweep_rate(rates, {"gate_k": gk})
        ax[1].plot(rates, f, "o-", ms=3, label=f"gate_k={gk}")
    ax[1].set(xlabel="event rate (1/s)", ylabel="felt time (s)",
              title="B. 'Busy flies' holds across gate_k")
    ax[1].legend(fontsize=8)

    # --- C. prospective robustness to activity_tau --------------------------
    for at in [0.5, 1.0, 2.0, 4.0]:
        f, _ = sweep_rate(rates, {"activity_tau": at})
        ax[2].plot(rates, f, "o-", ms=3, label=f"activity_tau={at}")
    ax[2].set(xlabel="event rate (1/s)", ylabel="felt time (s)",
              title="C. 'Busy flies' holds across activity_tau")
    ax[2].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig("robustness_results.png", dpi=120)

    print("=== A. dissociation across event rate ===")
    print(f"  felt monotonic decreasing: {bool(np.all(np.diff(felt) <= 1e-6))}")
    print(f"  load monotonic increasing: {bool(np.all(np.diff(load) >= -1e-6))}")
    print(f"  felt: {np.round(felt,1)}")
    print(f"  load: {np.round(load,0)}")
    print("\nsaved robustness_results.png")


if __name__ == "__main__":
    main()
