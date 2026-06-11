"""
Stage 1b: substrate vs behavioural read-out.

Run:  python experiments_stage1b.py   -> stage1b_results.png + summary

Top row  = SBF oscillator substrate (what the oscillators natively do).
Bottom   = log observer (the clean behavioural read-out).

  A1. Scalar property: common-mode jitter (flat CV) vs independent jitter (grows).
  A2. SBF bisection point (predict ~arithmetic, since kernel res. is absolute).
  B1. Log scalar property (flat CV = Weber fraction).
  B2. Log bisection (geometric mean).
  B3. Log central tendency (Vierordt, slope < 1).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import readouts as R


def main():
    fig, ax = plt.subplots(2, 3, figsize=(15, 8.4))
    summary = {}

    # --- A1: SBF scalar property, common vs independent noise ---------------
    durations = [2, 4, 8, 16, 32]
    cm = R.scalar_property(durations, R.log_freqs(), cm=0.05, ind=0.0)
    ind = R.scalar_property(durations, R.log_freqs(), cm=0.0, ind=0.05)
    ax[0, 0].plot(cm["durations"], cm["cv"], "o-", label="common-mode 0.05")
    ax[0, 0].plot(ind["durations"], ind["cv"], "s-", label="independent 0.05")
    ax[0, 0].set(xlabel="duration (s)", ylabel="CV of estimate",
                 title="A1. SBF scalar property")
    ax[0, 0].legend(fontsize=8)
    summary["sbf_cv_common"] = cm["cv"]
    summary["sbf_cv_independent"] = ind["cv"]

    # --- A2: SBF bisection point --------------------------------------------
    S, L = 4.0, 16.0
    sbf_log = R.sbf_bisection_curve(S, L, R.log_freqs(), cm=0.06)
    sbf_lin = R.sbf_bisection_curve(S, L, R.lin_freqs(), cm=0.06)
    ax[0, 1].plot(sbf_log["probes"], sbf_log["p_long"], "o-", ms=3, label="log freqs")
    ax[0, 1].plot(sbf_lin["probes"], sbf_lin["p_long"], "s-", ms=3, label="lin freqs")
    ax[0, 1].axhline(0.5, color="grey", lw=0.6)
    ax[0, 1].axvline(sbf_log["geometric_mean"], color="g", ls="--", lw=0.8,
                     label=f"geom={sbf_log['geometric_mean']:.1f}")
    ax[0, 1].axvline(sbf_log["arithmetic_mean"], color="r", ls=":", lw=0.8,
                     label=f"arith={sbf_log['arithmetic_mean']:.1f}")
    ax[0, 1].set(xlabel="probe (s)", ylabel="P(long)", title="A2. SBF bisection")
    ax[0, 1].legend(fontsize=7)
    summary["sbf_bisection_log"] = sbf_log["bisection_point"]
    summary["sbf_bisection_lin"] = sbf_lin["bisection_point"]

    # --- A3: native absolute resolution (why it isn't scalar) ---------------
    # Similarity of pattern(t) to pattern(t0) — width is set by f_max, constant.
    freqs = R.log_freqs()
    t = np.linspace(0, 6, 2000)
    for t0 in (1.0, 4.0):
        sim = R._unit(R.pattern(t, freqs), axis=1) @ R._unit(np.cos(2 * np.pi * freqs * t0))
        ax[0, 2].plot(t, sim, label=f"anchor {t0:.0f}s")
    ax[0, 2].set(xlabel="t (s)", ylabel="cosine similarity",
                 title="A3. Native resolution is absolute, not scalar")
    ax[0, 2].legend(fontsize=8)

    # --- B1: log scalar property --------------------------------------------
    lsp = R.log_scalar_property([2, 4, 8, 16, 32], w=0.15)
    ax[1, 0].plot(lsp["durations"], lsp["cv"], "o-")
    ax[1, 0].set(xlabel="duration (s)", ylabel="CV",
                 title="B1. Log observer scalar property", ylim=(0, 0.3))
    summary["log_cv"] = lsp["cv"]

    # --- B2: log bisection ---------------------------------------------------
    lb = R.log_bisection_curve(S, L, w=0.15)
    ax[1, 1].plot(lb["probes"], lb["p_long"], "o-", ms=3)
    ax[1, 1].axhline(0.5, color="grey", lw=0.6)
    ax[1, 1].axvline(lb["geometric_mean"], color="g", ls="--", lw=0.8,
                     label=f"geom={lb['geometric_mean']:.1f}")
    ax[1, 1].axvline(lb["arithmetic_mean"], color="r", ls=":", lw=0.8,
                     label=f"arith={lb['arithmetic_mean']:.1f}")
    ax[1, 1].axvline(lb["bisection_point"], color="b", lw=0.8,
                     label=f"point={lb['bisection_point']:.1f}")
    ax[1, 1].set(xlabel="probe (s)", ylabel="P(long)", title="B2. Log bisection")
    ax[1, 1].legend(fontsize=7)
    summary["log_bisection"] = lb["bisection_point"]
    summary["geom_mean"] = lb["geometric_mean"]

    # --- B3: log central tendency -------------------------------------------
    ct = R.log_central_tendency([2, 3, 5, 8, 13, 21, 34], w=0.18)
    ax[1, 2].plot(ct["durations"], ct["estimates"], "o-", label="estimate")
    ax[1, 2].plot(ct["durations"], ct["durations"], "k--", lw=0.8, label="veridical")
    ax[1, 2].axvline(ct["indifference"], color="b", lw=0.8,
                     label=f"indiff={ct['indifference']:.1f}")
    ax[1, 2].set(xlabel="true (s)", ylabel="estimate (s)",
                 title=f"B3. Central tendency (slope={ct['slope']:.2f})")
    ax[1, 2].legend(fontsize=7)
    summary["ct_slope"] = ct["slope"]
    summary["ct_indiff"] = ct["indifference"]

    fig.tight_layout()
    fig.savefig("stage1b_results.png", dpi=120)

    print("=== A. SBF substrate ===")
    print(f"  scalar CV common-mode: {np.round(summary['sbf_cv_common'], 3)}  (flat => scalar)")
    print(f"  scalar CV independent: {np.round(summary['sbf_cv_independent'], 3)}  (grows => not scalar)")
    print(f"  bisection log-freqs:  {summary['sbf_bisection_log']:.2f}")
    print(f"  bisection lin-freqs:  {summary['sbf_bisection_lin']:.2f}")
    print(f"  (geom={sbf_log['geometric_mean']:.1f}, arith={sbf_log['arithmetic_mean']:.1f})")
    print("=== B. Log observer ===")
    print(f"  scalar CV: {np.round(summary['log_cv'], 3)}  (flat => scalar)")
    print(f"  bisection point: {summary['log_bisection']:.2f}  geom mean: {summary['geom_mean']:.2f}")
    print(f"  central tendency slope: {summary['ct_slope']:.3f}  indiff: {summary['ct_indiff']:.2f}")
    print("\nsaved stage1b_results.png")


if __name__ == "__main__":
    main()
