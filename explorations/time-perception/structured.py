"""
Structured (adjacent-scale) coupling: stabilising the cascade.

Motivation (from F3 + F4):
  - Global all-to-all coupling DESTROYS the multi-scale code (synchronization).
  - The uncoupled cascade is exact but BRITTLE: a drifting slow stage flips a digit.
Hypothesis: couple ONLY adjacent stages with an M:1 phase-lock, so each slow stage
is slaved to a sub-harmonic of its faster, more accurate neighbour. This should
correct drift (robustness) WITHOUT collapsing the frequency ladder (no global lock).

Ladder: stage k has natural frequency f_k = f0 / M^k, so ideally theta_{k-1} = M*theta_k.
Adjacent n:m locking drives the mismatch phi_k = theta_{k-1} - M*theta_k -> 0.

Setup for the test: stage 0 (fastest) is the accurate reference; slower stages
carry a static frequency error (drift). We decode elapsed time from the phases and
compare locked vs unlocked.
"""

from __future__ import annotations

import numpy as np

import cascade as cas


def simulate(n_stages, M, f0, drift, K, duration, dt=0.002, seed=0):
    """
    Integrate the cascade with optional adjacent M:1 locking.
    `drift` = std of per-stage static multiplicative frequency error (stage 0 exempt).
    Returns (times, phases_in_cycles) where phases are in [0,1) (theta/2pi).
    """
    rng = np.random.default_rng(seed)
    base = f0 / (M ** np.arange(n_stages))
    err = np.ones(n_stages)
    err[1:] += drift * rng.standard_normal(n_stages - 1)   # stage 0 stays accurate
    omega = 2 * np.pi * base * err

    theta = np.zeros(n_stages)
    steps = int(round(duration / dt))
    out = np.empty((steps, n_stages))
    for s in range(steps):
        dtheta = omega.copy()
        if K > 0:
            # Adjacent M:1 phase locking (mutual between neighbours).
            for k in range(1, n_stages):
                phi = theta[k - 1] - M * theta[k]          # want 0
                dtheta[k] += K * np.sin(phi)               # pull slow stage up to ladder
                dtheta[k - 1] -= (K / M) * np.sin(phi)     # gentle back-reaction
        theta = theta + dt * dtheta
        out[s] = np.mod(theta / (2 * np.pi), 1.0)
    return np.arange(steps) * dt, out


def decode_error(times, phases, M, f0):
    """Decode each phase row to time and compare to the true (reference) time."""
    decoded = cas.decode(phases, M) / f0
    return np.abs(decoded - times)


def ladder_consistency(phases, M):
    """Mean |wrap(theta_{k-1} - M theta_k)| over adjacent pairs (0 = perfect ladder)."""
    x = phases * 2 * np.pi
    err = 0.0
    for k in range(1, x.shape[1]):
        d = np.mod(x[:, k - 1] - M * x[:, k] + np.pi, 2 * np.pi) - np.pi
        err = err + np.abs(d)
    return err / (x.shape[1] - 1)
