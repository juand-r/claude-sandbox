"""
Stage 2 experiments: does coupling earn its place?

Run:  python experiments_stage2.py   -> stage2_results.png + summary

  A. Recency: order parameter r(t) after a reset, for several K.
  B. Sync curve: steady-state r vs K (locate the transition K_c).
  C. Coding horizon vs K (does strong coupling destroy the multi-scale code?).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import coupling as C


def main():
    freqs = C.coupling_freqs()
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))

    # --- A. recency: r(t) after reset, several K ----------------------------
    Ks_recency = [0.0, 3.0, 10.0, 30.0]
    for K in Ks_recency:
        t, ph = C.simulate(freqs, K, duration=8.0)
        ax[0].plot(t, C.order_parameter(ph), label=f"K={K:g}")
    ax[0].set(xlabel="time since reset (s)", ylabel="order parameter r",
              title="A. Recency signal (coherence decay)")
    ax[0].legend(fontsize=8)

    # --- B. sync curve ------------------------------------------------------
    Ks = np.linspace(0, 40, 25)
    r_ss = np.array([C.steady_state_r(freqs, K) for K in Ks])
    ax[1].plot(Ks, r_ss, "o-")
    ax[1].set(xlabel="coupling K", ylabel="steady-state r",
              title="B. Synchronization transition")

    # --- C. coding horizon vs K --------------------------------------------
    Ks_h = np.linspace(0, 40, 21)
    horizon = np.array([C.coding_horizon(freqs, K) for K in Ks_h])
    ax[2].plot(Ks_h, horizon, "o-")
    ax[2].set(xlabel="coupling K", ylabel="coding horizon (s, censored at 30)",
              title="C. Strong coupling collapses the code")

    fig.tight_layout()
    fig.savefig("stage2_results.png", dpi=120)

    print("=== A. recency (r at t=2s after reset) ===")
    for K in Ks_recency:
        t, ph = C.simulate(freqs, K, duration=8.0)
        r = C.order_parameter(ph)
        i2 = np.argmin(np.abs(t - 2.0))
        print(f"  K={K:>4g}: r(2s)={r[i2]:.3f}")
    print("=== B. sync curve ===")
    print(f"  r(K=0)={r_ss[0]:.3f}  r(K=40)={r_ss[-1]:.3f}")
    kc_idx = np.argmax(r_ss > 0.5)
    print(f"  K where r first >0.5: {Ks[kc_idx]:.1f}")
    print("=== C. coding horizon ===")
    print(f"  horizon(K=0)={horizon[0]:.2f}s  horizon(K=40)={horizon[-1]:.2f}s")
    print(f"  horizon vs K: {np.round(horizon, 2)}")
    print("\nsaved stage2_results.png")


if __name__ == "__main__":
    main()
