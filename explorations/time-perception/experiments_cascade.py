"""
Cascade vs incommensurate bank: two ways to get multi-scale time, opposite failure
modes.

Run:  python experiments_cascade.py   -> cascade_results.png + summary

  A. Dynamic range: cascade decodes a huge range exactly; a single oscillator aliases.
  B. Robustness: per-oscillator phase noise. Cascade (odometer) fails catastrophically
     (digit flips -> off-by-M^k); the incommensurate bank degrades gracefully.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cascade as cas
import readouts as R


def bank_decode(t, freqs, grid, phase_noise=0.0, rng=None):
    """Decode time by matching a (noisy) phase pattern to templates over a grid."""
    rng = rng or np.random.default_rng()
    t = np.atleast_1d(t)
    templates = R._unit(R.pattern(grid, freqs), axis=1)        # (G, n)
    noise = 2 * np.pi * phase_noise * rng.standard_normal((t.size, freqs.size))
    obs = R._unit(np.cos(2 * np.pi * t[:, None] * freqs[None, :] + noise), axis=1)
    return grid[np.argmax(obs @ templates.T, axis=1)]


def main():
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))

    # --- A. dynamic range ---------------------------------------------------
    M, N, f0 = 10, 4, 1.0           # range = M^(N-1) = 1000 s from 4 stages
    rng_t = np.linspace(0, cas.range_of(N, M, f0), 4000, endpoint=False)
    decoded = cas.reconstruct(rng_t, N, M, f0)
    single = cas.reconstruct(rng_t, 1, M, f0)   # one stage: aliases every 1 s
    ax[0].plot(rng_t, decoded, lw=1, label=f"cascade ({N} stages, range {int(cas.range_of(N,M,f0))}s)")
    ax[0].plot(rng_t, single * 200, lw=0.6, alpha=0.7,
               label="single oscillator (aliases, scaled)")
    ax[0].plot(rng_t, rng_t, "k--", lw=0.6, label="veridical")
    ax[0].set(xlabel="true time (s)", ylabel="decoded time (s)",
              title="A. Cascade: exponential range from few stages")
    ax[0].legend(fontsize=7)

    # --- B. robustness ------------------------------------------------------
    # Fair comparison over [0, 100] s.
    Mc, Nc = 10, 3                  # cascade range = 100 s
    freqs = np.geomspace(0.07, 3.0, 16)
    grid = np.arange(0, 100, 0.05)
    test_t = np.linspace(1, 99, 400)
    noises = [0.0, 0.005, 0.01, 0.02, 0.04, 0.08]

    cas_med, cas_90, bank_med, bank_90 = [], [], [], []
    rng = np.random.default_rng(0)
    for pn in noises:
        ec = np.abs(cas.reconstruct(test_t, Nc, Mc, 1.0, phase_noise=pn, seed=1) - test_t)
        eb = np.abs(bank_decode(test_t, freqs, grid, phase_noise=pn, rng=rng) - test_t)
        cas_med.append(np.median(ec)); cas_90.append(np.percentile(ec, 90))
        bank_med.append(np.median(eb)); bank_90.append(np.percentile(eb, 90))

    ax[1].plot(noises, cas_90, "o-", color="C3", label="cascade 90th pct")
    ax[1].plot(noises, cas_med, "o--", color="C3", alpha=0.6, label="cascade median")
    ax[1].plot(noises, bank_90, "s-", color="C0", label="bank 90th pct")
    ax[1].plot(noises, bank_med, "s--", color="C0", alpha=0.6, label="bank median")
    ax[1].set(xlabel="per-oscillator phase noise", ylabel="decode error (s)",
              title="B. Cascade brittle, bank graceful", yscale="log")
    ax[1].legend(fontsize=7)

    fig.tight_layout()
    fig.savefig("cascade_results.png", dpi=120)

    print("=== A. dynamic range ===")
    print(f"  cascade {N} stages -> range {int(cas.range_of(N,M,f0))}s, noiseless max err "
          f"{np.abs(decoded-rng_t).max():.3g}")
    print("=== B. robustness (error in s) ===")
    print(f"  noise levels: {noises}")
    print(f"  cascade 90th: {np.round(cas_90,2)}")
    print(f"  bank    90th: {np.round(bank_90,2)}")
    print("\nsaved cascade_results.png")


if __name__ == "__main__":
    main()
