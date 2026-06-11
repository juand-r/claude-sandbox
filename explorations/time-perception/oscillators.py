"""
Oscillator-based engine for subjective time (Stage 1, uncoupled).

A bank of phase oscillators at geometrically spaced frequencies forms a
multi-scale clock. Events perturb the phases (perception). An attention gate
makes the prospective clock run fast when little is happening. Three read-outs
come off the same state:

  - prospective tau    : gated integral of the self-clock (felt rate, in-the-moment)
  - retrospective load : accumulated perturbation magnitude (remembered duration)
  - coherence          : order parameter, decays as oscillators dephase after a reset

No coupling yet (Stage 1). The oscillators are independent; events are the only
thing that touches them. Coupling is Stage 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np


@dataclass
class Params:
    """All tunables in one place. No magic numbers scattered in the code."""

    n_osc: int = 32              # oscillators in the bank
    f_min: float = 0.05          # Hz, slowest oscillator
    f_max: float = 5.0           # Hz, fastest oscillator
    self_rate: float = 1.0       # subjective seconds per real second, baseline
    dt: float = 0.01             # integration step (s)

    reset_strength: float = 0.6  # fraction a phase is pulled toward 0 per unit salience
    activity_tau: float = 2.0    # s, leak time-constant of the attention/activity estimate
    gate_k: float = 1.5          # sensitivity of the gate to activity

    rate_jitter: float = 0.0     # per-instance multiplicative jitter on self_rate (Weber)
    seed: int | None = None


class TimePerceptionSystem:
    """
    Stateful simulator. Drive it with .step(dt) for the passage of real time and
    .event(salience) when something enters the system. Read tau / load /
    coherence() whenever you want a subjective quantity.
    """

    def __init__(self, params: Params | None = None):
        self.p = params or Params()
        rng = np.random.default_rng(self.p.seed)

        # Geometric (log-spaced) frequencies: scale-free coverage, and the spacing
        # that makes the bisection midpoint land on the geometric mean later.
        self.freqs = np.geomspace(self.p.f_min, self.p.f_max, self.p.n_osc)
        self.omega = 2.0 * np.pi * self.freqs

        # Per-instance multiplicative jitter on the prospective rate. This is the
        # injected multiplicative noise that produces the scalar property; without
        # it the clock is deterministic. Drawn once per system instance (a "trial").
        jitter = 1.0 + self.p.rate_jitter * rng.standard_normal()
        self.eff_self_rate = self.p.self_rate * max(jitter, 1e-6)

        self.reset()

    def reset(self) -> None:
        """Reset to t=0 with all oscillators phase-aligned (an onset reset)."""
        self.t = 0.0
        self.phases = np.zeros(self.p.n_osc)   # coherent start
        self.tau = 0.0                         # prospective (felt) time
        self.load = 0.0                        # retrospective load
        self.activity = 0.0                    # leaky estimate of recent input
        self.last_event_t = 0.0                # real time of last event
        self.tau_at_last_event = 0.0           # felt time at last event

    # --- dynamics -----------------------------------------------------------

    def gate(self) -> float:
        """
        Attention-to-time gate in [0, 1]. High when activity is low (idle), so
        the prospective clock runs fast and idle time *drags*. Low when flooded,
        so busy time *flies*. This is the corrected prospective sign.
        """
        return 1.0 / (1.0 + self.p.gate_k * self.activity)

    def step(self, dt: float | None = None) -> None:
        """Advance real time by dt: oscillators turn, activity leaks, felt time accrues."""
        dt = self.p.dt if dt is None else dt
        self.phases = (self.phases + self.omega * dt) % (2.0 * np.pi)
        # Activity decays toward zero between events (leaky integrator).
        self.activity *= np.exp(-dt / self.p.activity_tau)
        # Prospective time accrues at the gated self-clock rate.
        self.tau += self.gate() * self.eff_self_rate * dt
        self.t += dt

    def event(self, salience: float = 1.0) -> None:
        """
        Something enters the system. Perturb the phases toward 0 (a partial
        reset, scaled by salience), bump activity, and bank the perturbation
        magnitude as retrospective load.
        """
        alpha = np.clip(self.p.reset_strength * salience, 0.0, 1.0)
        # Shortest-path pull of each phase toward 0, by fraction alpha.
        wrapped = (self.phases + np.pi) % (2.0 * np.pi) - np.pi  # to (-pi, pi]
        delta = -alpha * wrapped
        self.phases = (self.phases + delta) % (2.0 * np.pi)

        self.load += float(np.sum(np.abs(delta)))  # phase-space change stored
        self.activity += salience
        self.last_event_t = self.t
        self.tau_at_last_event = self.tau

    # --- read-outs ----------------------------------------------------------

    def coherence(self) -> float:
        """Kuramoto order parameter |mean(e^{i theta})| in [0, 1]. Recency signal:
        ~1 right after a reset, decays as oscillators dephase."""
        return float(np.abs(np.mean(np.exp(1j * self.phases))))

    def felt_idle(self) -> float:
        """Prospective (felt) time elapsed since the last event."""
        return self.tau - self.tau_at_last_event

    def real_idle(self) -> float:
        """Real time elapsed since the last event."""
        return self.t - self.last_event_t

    # --- convenience --------------------------------------------------------

    def run(self, duration: float, event_times=None, salience: float = 1.0):
        """
        Simulate `duration` seconds. `event_times` is an iterable of real times
        at which a unit (or `salience`) event fires. Returns a dict of recorded
        traces sampled every step.
        """
        event_times = sorted(event_times or [])
        ei = 0
        rec = {k: [] for k in ("t", "tau", "load", "coherence", "gate", "activity")}
        n_steps = int(round(duration / self.p.dt))
        for _ in range(n_steps):
            # Fire any events scheduled within this step.
            while ei < len(event_times) and event_times[ei] <= self.t + self.p.dt:
                self.event(salience)
                ei += 1
            self.step()
            rec["t"].append(self.t)
            rec["tau"].append(self.tau)
            rec["load"].append(self.load)
            rec["coherence"].append(self.coherence())
            rec["gate"].append(self.gate())
            rec["activity"].append(self.activity)
        return {k: np.asarray(v) for k, v in rec.items()}
