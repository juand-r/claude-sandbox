"""
Stage 2 (cont.): hierarchical cascade = nested loops at different scales.

A ladder of oscillators, each M times slower than the one below:
    f_k = f0 / M^k,   phase x_k(t) = frac(f0 * t / M^k)  in [0, 1).
This is an odometer / mixed-radix (residue) code: the fast stage gives the fine
fraction, each slower stage supplies the next base-M digit. N stages encode time
over a range ~M^(N-1) * P0 with resolution set by the fast stage -> exponential
dynamic range from a linear number of oscillators. That is the "long durations
from nested fast loops" idea, via a cascade instead of incommensurate frequencies.

Decoding (no noise): digit_{k-1} = floor(M * x_k); reconstruct
    X = x_0 + sum_{k=1}^{N-1} floor(M * x_k) * M^(k-1)     (units of P0 = 1/f0)
valid for X in [0, M^(N-1)).

Trade-off vs the incommensurate bank (see experiments): the cascade is compact and
exact, but BRITTLE — noise at a coarse stage flips a digit and causes a catastrophic
(off-by-M^k) error. The incommensurate bank degrades gracefully.
"""

from __future__ import annotations

import numpy as np


def phases(t, n_stages, M, f0=1.0):
    """Stage phases x_k in [0,1) at time(s) t. t scalar or array -> (len(t), n)."""
    t = np.atleast_1d(t).astype(float)[:, None]
    k = np.arange(n_stages)[None, :]
    return np.mod(f0 * t / (M ** k), 1.0)


def decode(x, M):
    """Reconstruct X (units of P0) from stage phases x (..., n_stages)."""
    x = np.atleast_2d(x)
    n = x.shape[1]
    X = x[:, 0].copy()
    for k in range(1, n):
        # +1e-9 guards against floor undershoot exactly at digit boundaries (fp).
        X += np.floor(M * x[:, k] + 1e-9) * (M ** (k - 1))
    return X


def reconstruct(t, n_stages, M, f0=1.0, phase_noise=0.0, seed=0):
    """Encode times t into phases, optionally add wrapped phase noise, decode back."""
    rng = np.random.default_rng(seed)
    x = phases(t, n_stages, M, f0)
    if phase_noise:
        x = np.mod(x + phase_noise * rng.standard_normal(x.shape), 1.0)
    return decode(x, M) / f0  # back to time units


def range_of(n_stages, M, f0=1.0):
    """Unambiguous coding range in seconds."""
    return (M ** (n_stages - 1)) / f0
