"""
Structured coupling stabilises the cascade (the F3+F4 synthesis).

Run:  python experiments_structured.py   -> structured_results.png + summary

  A. Decode-error trace over time: unlocked drifts/jumps, locked stays flat.
  B. 90th-pct error vs coupling K: stabilises at modest K, plateaus (local coupling
     does NOT collapse the code even at large K, unlike global coupling in Stage 2).
  C. Robustness vs drift: locked tolerates far more frequency drift than unlocked.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import structured as st

M, N, F0, DUR = 4, 4, 1.0, 60.0
SEEDS = 12


def err_stat(drift, K, pct=90):
    """Second-half decode-error percentile, averaged over seeds."""
    vals = []
    for s in range(SEEDS):
        t, ph = st.simulate(N, M, F0, drift, K, DUR, seed=s)
        e = st.decode_error(t, ph, M, F0)
        vals.append(np.percentile(e[len(t) // 2:], pct))
    return np.mean(vals)


def main():
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))

    # --- A. error trace -----------------------------------------------------
    for K, lab in [(0.0, "unlocked"), (2.0, "adjacent locking K=2")]:
        t, ph = st.simulate(N, M, F0, drift=0.03, K=K, duration=DUR, seed=3)
        ax[0].plot(t, st.decode_error(t, ph, M, F0), lw=1, label=lab)
    ax[0].set(xlabel="time (s)", ylabel="decode error (s)",
              title="A. Locking holds the ladder together")
    ax[0].legend(fontsize=8)

    # --- B. error vs K ------------------------------------------------------
    Ks = [0, 0.25, 0.5, 1, 2, 4, 8, 16, 32]
    for drift in [0.02, 0.04]:
        e = [err_stat(drift, K) for K in Ks]
        ax[1].plot(Ks, e, "o-", label=f"drift={drift}")
    ax[1].set(xlabel="adjacent coupling K", ylabel="90th-pct decode error (s)",
              title="B. Stabilises at modest K, no collapse at large K",
              xscale="symlog")
    ax[1].legend(fontsize=8)

    # --- C. robustness vs drift ---------------------------------------------
    drifts = [0.0, 0.01, 0.02, 0.04, 0.06, 0.08, 0.12]
    for K, lab in [(0.0, "unlocked"), (4.0, "locked K=4")]:
        e = [err_stat(d, K) for d in drifts]
        ax[2].plot(drifts, e, "o-", label=lab)
    ax[2].set(xlabel="per-stage frequency drift (std)", ylabel="90th-pct decode error (s)",
              title="C. Locking buys drift tolerance")
    ax[2].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig("structured_results.png", dpi=120)

    print("=== structured coupling ===")
    print(f"  unlocked (drift .03) 90pct err: {err_stat(0.03, 0.0):.2f}s")
    print(f"  locked K=2 (drift .03) 90pct err: {err_stat(0.03, 2.0):.2f}s")
    print(f"  locked K=32 (drift .03) 90pct err: {err_stat(0.03, 32.0):.2f}s  (no collapse)")
    print("\nsaved structured_results.png")


if __name__ == "__main__":
    main()
