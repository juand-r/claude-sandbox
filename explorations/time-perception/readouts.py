"""
Back-end read-outs (Stage 1b).

Two layers, kept distinct on purpose:

1. SBF coincidence (the oscillator *substrate*). Activity cos(2*pi*f_i*t);
   durations read out by matching the current phase pattern to stored templates.
   We test what noise it needs to behave like a clock, and find its limits.

2. Log observer (the behavioural *read-out*). A scalar (Weber) measurement on the
   log-time axis, plus a Bayesian prior. This is the standard, clean way to get the
   three behavioural signatures, and it matches the log-scale recommendation from
   the Stage-1 design discussion.

Key empirical lessons (see NOTES.md):
  - Scalar property needs COMMON-MODE multiplicative noise (a global rate that
    varies trial to trial). Independent per-oscillator noise degrades the code and
    gives a NON-scalar, growing CV.
  - The linear-phase coincidence kernel has constant ABSOLUTE resolution, so its
    bisection point sits near the ARITHMETIC mean. Geometric-mean bisection comes
    from the log read-out, not from the oscillator kernel.
"""

from __future__ import annotations

import numpy as np


# --- frequency banks --------------------------------------------------------

def log_freqs(n=40, f_min=0.2, f_max=8.0):
    return np.geomspace(f_min, f_max, n)


def lin_freqs(n=40, f_min=0.2, f_max=8.0):
    return np.linspace(f_min, f_max, n)


def _unit(x, axis=-1):
    """L2-normalise along an axis (so dot products become cosine similarities)."""
    n = np.linalg.norm(x, axis=axis, keepdims=True)
    return x / np.where(n == 0, 1.0, n)


def pattern(t, freqs):
    """cos(2*pi*f*t); t scalar or array -> (len(t), n) matrix."""
    t = np.atleast_1d(t)[:, None]
    return np.cos(2.0 * np.pi * t * freqs[None, :])


def _observed(true_T, freqs, cm, ind, rng):
    """Phase pattern at true_T with common-mode (cm) and independent (ind) freq jitter."""
    eff = freqs * (1.0 + cm * rng.standard_normal()) * (1.0 + ind * rng.standard_normal(freqs.size))
    return np.cos(2.0 * np.pi * eff * true_T)


# === 1. SBF coincidence substrate ==========================================

def sbf_estimate(true_T, freqs, grid, cm=0.0, ind=0.0, rng=None):
    """Estimate a duration by best template match (cosine similarity, argmax)."""
    rng = rng or np.random.default_rng()
    obs = _unit(_observed(true_T, freqs, cm, ind, rng))
    templates = _unit(pattern(grid, freqs), axis=1)      # (G, n)
    return grid[int(np.argmax(templates @ obs))]


def scalar_property(durations, freqs, cm=0.0, ind=0.0, n_trials=400, seed=0):
    """Per-duration (mean, sd, cv) of the SBF estimate under the given noise mix."""
    rng = np.random.default_rng(seed)
    out = {"durations": np.asarray(durations, float), "mean": [], "sd": [], "cv": []}
    for D in durations:
        grid = np.arange(0.6 * D, 1.4 * D, max(D * 0.002, 0.004))  # symmetric, fine
        ests = np.array([sbf_estimate(D, freqs, grid, cm, ind, rng)
                         for _ in range(n_trials)])
        out["mean"].append(ests.mean())
        out["sd"].append(ests.std())
        out["cv"].append(ests.std() / ests.mean())
    for k in ("mean", "sd", "cv"):
        out[k] = np.asarray(out[k])
    return out


def sbf_bisection_curve(anchor_short, anchor_long, freqs, cm=0.06,
                        n_probes=25, n_trials=400, seed=0):
    """Bisection using the SBF coincidence rule (cosine similarity to anchors)."""
    rng = np.random.default_rng(seed)
    tS = _unit(np.cos(2.0 * np.pi * freqs * anchor_short))
    tL = _unit(np.cos(2.0 * np.pi * freqs * anchor_long))
    probes = np.linspace(anchor_short, anchor_long, n_probes)
    p_long = []
    for p in probes:
        choices = []
        for _ in range(n_trials):
            obs = _unit(_observed(p, freqs, cm, 0.0, rng))
            choices.append(int(obs @ tL > obs @ tS))
        p_long.append(np.mean(choices))
    p_long = np.asarray(p_long)
    return {
        "probes": probes, "p_long": p_long,
        "bisection_point": float(np.interp(0.5, p_long, probes)),
        "geometric_mean": float(np.sqrt(anchor_short * anchor_long)),
        "arithmetic_mean": float(0.5 * (anchor_short + anchor_long)),
    }


# === 2. Log observer (behavioural read-out) ================================

def log_measure(T, w, rng):
    """Scalar (Weber) measurement: constant noise on the log-time axis."""
    return np.log(T) + w * rng.standard_normal(np.shape(T))


def log_scalar_property(durations, w=0.15, n_trials=2000, seed=0):
    """SD should be linear in duration -> CV flat ~ w (the Weber fraction)."""
    rng = np.random.default_rng(seed)
    durations = np.asarray(durations, float)
    cv = []
    for D in durations:
        ests = np.exp(log_measure(np.full(n_trials, D), w, rng))
        cv.append(ests.std() / ests.mean())
    return {"durations": durations, "cv": np.asarray(cv)}


def log_bisection_curve(anchor_short, anchor_long, w=0.15, n_probes=25, n_trials=4000, seed=0):
    """Decide 'long' if the log-measurement is above the log-midpoint -> geom mean."""
    rng = np.random.default_rng(seed)
    midpoint_log = 0.5 * (np.log(anchor_short) + np.log(anchor_long))
    probes = np.linspace(anchor_short, anchor_long, n_probes)
    p_long = []
    for p in probes:
        m = log_measure(np.full(n_trials, p), w, rng)
        p_long.append(np.mean(m > midpoint_log))
    p_long = np.asarray(p_long)
    return {
        "probes": probes, "p_long": p_long,
        "bisection_point": float(np.interp(0.5, p_long, probes)),
        "geometric_mean": float(np.sqrt(anchor_short * anchor_long)),
        "arithmetic_mean": float(0.5 * (anchor_short + anchor_long)),
    }


def log_central_tendency(durations, w=0.18, prior_sd_log=0.35, n_trials=4000, seed=0):
    """Bayesian estimate on the log axis with a prior over the range -> Vierordt."""
    rng = np.random.default_rng(seed)
    durations = np.asarray(durations, float)
    log_d = np.log(durations)
    prior_mu = log_d.mean()                    # geometric mean of the range
    prior_var, meas_var = prior_sd_log ** 2, w ** 2
    weight = (1.0 / meas_var) / (1.0 / meas_var + 1.0 / prior_var)

    est_means = []
    for D in durations:
        m = log_measure(np.full(n_trials, D), w, rng)
        post_log = weight * m + (1.0 - weight) * prior_mu
        est_means.append(np.exp(post_log).mean())
    est_means = np.asarray(est_means)
    slope, intercept = np.polyfit(log_d, np.log(est_means), 1)
    return {
        "durations": durations, "estimates": est_means,
        "slope": float(slope),
        "indifference": float(np.exp(intercept / (1.0 - slope))) if slope != 1 else np.nan,
        "geometric_mean": float(np.exp(prior_mu)),
    }
