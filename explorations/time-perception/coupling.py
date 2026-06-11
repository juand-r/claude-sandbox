"""
Stage 2: interacting oscillators (Kuramoto mean-field coupling).

Two questions:
  1. Does coherence give a usable RECENCY signal? After an event resets the bank
     to a common phase, the order parameter r decays as oscillators dephase. How
     long that decay stays legible is the recency horizon. Does coupling help?
  2. Does coupling destroy the multi-scale CODE? Strong coupling locks oscillators
     to a common frequency, collapsing the unique long-horizon phase pattern that
     is the whole point of a multi-scale clock. We quantify the coding horizon vs K.

Mean-field Kuramoto: dtheta_i = omega_i + K * r * sin(psi - theta_i),
where r*exp(i*psi) = mean_j exp(i*theta_j).
"""

from __future__ import annotations

import numpy as np


def coupling_freqs(n=24, f_min=0.5, f_max=4.0):
    """Moderately spread bank so the sync transition is reachable at finite K."""
    return np.geomspace(f_min, f_max, n)


def simulate(freqs, K, duration, dt=0.005, reset=True, seed=0):
    """
    Integrate the coupled bank. Returns (times, phases) with phases shape (T, n).
    If reset, all phases start at 0 (an event/onset reset); else random.
    """
    rng = np.random.default_rng(seed)
    omega = 2.0 * np.pi * freqs
    n = freqs.size
    theta = np.zeros(n) if reset else rng.uniform(0, 2 * np.pi, n)
    steps = int(round(duration / dt))
    out = np.empty((steps, n))
    for s in range(steps):
        z = np.mean(np.exp(1j * theta))
        r, psi = np.abs(z), np.angle(z)
        theta = theta + dt * (omega + K * r * np.sin(psi - theta))
        out[s] = theta
    times = np.arange(steps) * dt
    return times, out


def order_parameter(phases):
    """r(t) = |mean exp(i theta)| over oscillators, per time row."""
    return np.abs(np.mean(np.exp(1j * phases), axis=1))


def _unit(x):
    n = np.linalg.norm(x)
    return x / (n if n else 1.0)


def similarity_to_start(phases):
    """Cosine similarity of cos-pattern at each t to the pattern at t=0."""
    pat = np.cos(phases)                       # (T, n)
    ref = _unit(pat[0])
    return (pat / np.linalg.norm(pat, axis=1, keepdims=True)) @ ref


def coding_horizon(freqs, K, duration=30.0, dt=0.005, thresh=0.8):
    """
    First recurrence time: the earliest t>0 at which the phase pattern returns to
    high similarity with the start (the code aliases / repeats). Longer = the
    multi-scale code stays unique longer. Censored at `duration` if no recurrence.
    """
    times, phases = simulate(freqs, K, duration, dt, reset=True)
    sim = similarity_to_start(phases)
    # Skip the initial decay from 1.0; find the first later up-crossing of thresh.
    below = np.where(sim < thresh * 0.6)[0]
    if below.size == 0:
        return duration  # never even left the start neighbourhood (fully locked, fast)
    start = below[0]
    rec = np.where(sim[start:] >= thresh)[0]
    return duration if rec.size == 0 else times[start + rec[0]]


def steady_state_r(freqs, K, duration=20.0, dt=0.005, tail=0.3):
    """Time-averaged order parameter over the last `tail` fraction (sync curve)."""
    _, phases = simulate(freqs, K, duration, dt, reset=False)
    r = order_parameter(phases)
    return r[int((1 - tail) * r.size):].mean()
