"""
Stage 1 demos for the oscillator time-perception engine.

Run:  python experiments.py
Produces stage1_results.png and prints summary statistics.

Three probes of one engine:
  A. Holiday paradox  - prospective vs retrospective disagree (the headline).
  B. Idle detection   - felt-idle threshold drives a self-regulation signal.
  C. Scalar property  - validation; CV of estimates is ~flat across durations.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt

from oscillators import Params, TimePerceptionSystem


def poisson_events(duration, rate, rng):
    """Event times in [0, duration) from a homogeneous Poisson process."""
    times, t = [], 0.0
    while True:
        t += rng.exponential(1.0 / rate)
        if t >= duration:
            return times
        times.append(t)


# --- Demo A: holiday paradox -----------------------------------------------

def demo_holiday(ax):
    """Same wall-clock window; busy vs idle. Prospective should invert retrospective."""
    duration = 60.0
    rng = np.random.default_rng(0)
    busy_events = poisson_events(duration, rate=4.0, rng=rng)   # much happening
    idle_events = poisson_events(duration, rate=0.1, rng=rng)   # almost nothing

    busy = TimePerceptionSystem(Params(seed=1)).run(duration, busy_events)
    idle = TimePerceptionSystem(Params(seed=1)).run(duration, idle_events)

    ax.plot(busy["t"], busy["tau"], label=f"busy (felt {busy['tau'][-1]:.0f}s)")
    ax.plot(idle["t"], idle["tau"], label=f"idle (felt {idle['tau'][-1]:.0f}s)")
    ax.plot([0, duration], [0, duration], "k--", lw=0.8, label="real time")
    ax.set(xlabel="real time (s)", ylabel="prospective felt time tau (s)",
           title="A. Prospective: idle drags, busy flies")
    ax.legend(fontsize=8)

    return {
        "busy_felt": busy["tau"][-1], "idle_felt": idle["tau"][-1],
        "busy_load": busy["load"][-1], "idle_load": idle["load"][-1],
        "n_busy": len(busy_events), "n_idle": len(idle_events),
    }


# --- Demo B: idle detection / self-regulation ------------------------------

def demo_idle_detection(ax, felt_threshold=8.0):
    """Activity, then a gap. Fire a check-in when *felt* idle time crosses a bound."""
    sys = TimePerceptionSystem(Params(seed=2))
    duration = 40.0
    rng = np.random.default_rng(3)
    # Busy for first 10s, then silence.
    events = poisson_events(10.0, rate=3.0, rng=rng)

    ts, felt_idles, fired = [], [], []
    ei = 0
    events = sorted(events)
    n_steps = int(round(duration / sys.p.dt))
    armed = True
    for _ in range(n_steps):
        while ei < len(events) and events[ei] <= sys.t + sys.p.dt:
            sys.event(1.0)
            ei += 1
            armed = True  # re-arm after real input
        sys.step()
        ts.append(sys.t)
        felt_idles.append(sys.felt_idle())
        if armed and sys.felt_idle() >= felt_threshold:
            fired.append(sys.t)
            armed = False  # one check-in per idle stretch

    ts = np.asarray(ts)
    ax.plot(ts, felt_idles, label="felt idle since last event")
    ax.axhline(felt_threshold, color="r", ls="--", lw=0.8, label="check-in threshold")
    for f in fired:
        ax.axvline(f, color="g", ls=":", lw=0.8)
    ax.set(xlabel="real time (s)", ylabel="felt idle tau (s)",
           title="B. Idle detection (check-in at green)")
    ax.legend(fontsize=8)
    return {"check_in_times": fired}


# --- Demo C: scalar property -----------------------------------------------

def demo_scalar(ax, n_trials=400):
    """Estimate elapsed time (idle, gate~1) across durations, with rate jitter.
    Scalar property: SD grows linearly with duration -> CV is ~constant."""
    durations = np.array([2.0, 4.0, 8.0, 16.0, 32.0])
    jitter = 0.15
    means, sds = [], []
    for D in durations:
        ests = []
        for trial in range(n_trials):
            sys = TimePerceptionSystem(Params(rate_jitter=jitter, seed=1000 + trial))
            r = sys.run(D, event_times=[])  # no events: pure clock
            ests.append(r["tau"][-1])
        ests = np.asarray(ests)
        means.append(ests.mean())
        sds.append(ests.std())
    means, sds = np.asarray(means), np.asarray(sds)
    cv = sds / means

    ax.plot(durations, sds, "o-", label="SD of estimate")
    # Reference line through origin: the scalar-property prediction SD = cv_mean * D.
    ax.plot(durations, cv.mean() * durations, "k--", lw=0.8,
            label=f"linear (CV={cv.mean():.3f})")
    ax.set(xlabel="duration (s)", ylabel="SD of felt estimate (s)",
           title="C. Scalar property (SD linear in duration)")
    ax.legend(fontsize=8)
    return {"durations": durations, "cv": cv}


def main():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    a = demo_holiday(axes[0])
    b = demo_idle_detection(axes[1])
    c = demo_scalar(axes[2])
    fig.tight_layout()
    fig.savefig("stage1_results.png", dpi=120)

    print("=== Demo A: holiday paradox ===")
    print(f"  events:      busy={a['n_busy']}  idle={a['n_idle']}")
    print(f"  prospective: busy felt {a['busy_felt']:.1f}s  idle felt {a['idle_felt']:.1f}s"
          f"   -> idle drags? {a['idle_felt'] > a['busy_felt']}")
    print(f"  retrospect.: busy load {a['busy_load']:.1f}   idle load {a['idle_load']:.1f}"
          f"   -> busy longer? {a['busy_load'] > a['idle_load']}")
    dissociation = (a["idle_felt"] > a["busy_felt"]) and (a["busy_load"] > a["idle_load"])
    print(f"  DISSOCIATION reproduced: {dissociation}")

    print("=== Demo B: idle detection ===")
    print(f"  check-in fired at (real s): {[round(x, 1) for x in b['check_in_times']]}")

    print("=== Demo C: scalar property ===")
    print(f"  CV per duration: {np.round(c['cv'], 3)}")
    print(f"  CV spread (max-min): {c['cv'].max() - c['cv'].min():.3f}  (flat => scalar)")

    print("\nsaved stage1_results.png")


if __name__ == "__main__":
    main()
