"""
Stochastic extension of the (f, x) dynamical system.

Instead of a deterministic meta-rule phi: F x X -> F,
we have a stochastic meta-rule phi: F x X -> Distribution(F).

This means at each step, the next function is sampled from a distribution
that depends on the current (f, x).

Key questions:
- Do orbits converge to stationary distributions?
- What's the mixing time?
- How does stochasticity affect "creativity" (escape from attractors)?
"""

import random
import numpy as np
from collections import Counter
from dataclasses import dataclass
from dds import Func, State, enumerate_functions, step, OrbitInfo


@dataclass
class StochasticMetaRule:
    """A stochastic meta-rule: given (f, x), returns a distribution over F.
    transition_probs[(f.table, x)] = {g.table: prob, ...}
    """
    n: int
    transition_probs: dict  # (func_table, x) -> {func_table: prob}

    def sample(self, f: Func, x: int, rng: random.Random = None) -> Func:
        """Sample next function from the distribution."""
        rng = rng or random.Random()
        key = (f.table, x)
        dist = self.transition_probs.get(key, {f.table: 1.0})
        tables = list(dist.keys())
        probs = [dist[t] for t in tables]
        chosen = rng.choices(tables, weights=probs, k=1)[0]
        return Func(chosen)


def make_noisy_meta(deterministic_phi, funcs: list[Func], noise: float = 0.1,
                    rng: random.Random = None) -> StochasticMetaRule:
    """Add uniform noise to a deterministic meta-rule.

    With probability (1-noise), use the deterministic choice.
    With probability noise, pick a random function from F.
    """
    n = funcs[0].n
    transition_probs = {}

    for f in funcs:
        for x in range(n):
            det_result = deterministic_phi(f, x)
            dist = {}
            # Distribute noise uniformly over all functions
            noise_per_func = noise / len(funcs)
            for g in funcs:
                dist[g.table] = noise_per_func
            # Add the deterministic mass
            dist[det_result.table] = dist.get(det_result.table, 0) + (1 - noise)
            transition_probs[(f.table, x)] = dist

    return StochasticMetaRule(n=n, transition_probs=transition_probs)


def make_temperature_meta(funcs: list[Func], energy_fn, temperature: float = 1.0) -> StochasticMetaRule:
    """Boltzmann-style meta-rule: probability of choosing function g is
    proportional to exp(-energy(f, x, g) / temperature).

    energy_fn(f, x, g) -> float: energy of transitioning from (f, x) to g.
    """
    n = funcs[0].n
    transition_probs = {}

    for f in funcs:
        for x in range(n):
            energies = {g.table: energy_fn(f, x, g) for g in funcs}
            # Boltzmann distribution
            min_e = min(energies.values())
            weights = {t: np.exp(-(e - min_e) / max(temperature, 1e-10))
                      for t, e in energies.items()}
            total = sum(weights.values())
            dist = {t: w / total for t, w in weights.items()}
            transition_probs[(f.table, x)] = dist

    return StochasticMetaRule(n=n, transition_probs=transition_probs)


def stochastic_orbit(state: State, meta: StochasticMetaRule,
                     steps: int = 100, seed: int = 42) -> list[State]:
    """Run a stochastic orbit for a fixed number of steps."""
    rng = random.Random(seed)
    trajectory = [state]
    s = state
    for _ in range(steps):
        new_f = meta.sample(s.f, s.x, rng)
        new_x = s.f(s.x)
        s = State(new_f, new_x)
        trajectory.append(s)
    return trajectory


def estimate_stationary_distribution(state: State, meta: StochasticMetaRule,
                                     steps: int = 10000, burn_in: int = 1000,
                                     seed: int = 42) -> dict:
    """Estimate the stationary distribution by running a long trajectory."""
    traj = stochastic_orbit(state, meta, steps=steps, seed=seed)
    # Discard burn-in
    counts = Counter()
    for s in traj[burn_in:]:
        counts[(s.f.table, s.x)] += 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.most_common()}


def measure_escape_rate(meta: StochasticMetaRule, funcs: list[Func],
                        n: int, num_trials: int = 100, steps: int = 200,
                        seed: int = 42) -> dict:
    """For each deterministic fixed point, measure how quickly the stochastic
    system escapes. Returns escape statistics.

    A fixed point of the deterministic system (f, x) satisfies
    f(x) = x and phi_det(f, x) = f.
    In the stochastic version, noise causes escape.
    """
    rng = random.Random(seed)

    # Find states that are fixed points in the zero-noise limit
    # (i.e., states where the most probable transition goes back to itself)
    fixed_points = []
    for f in funcs:
        for x in range(n):
            if f(x) == x:
                key = (f.table, x)
                dist = meta.transition_probs.get(key, {})
                if dist.get(f.table, 0) > 0.5:  # majority stays
                    fixed_points.append(State(f, x))

    results = {}
    for fp in fixed_points:
        escape_times = []
        for trial in range(num_trials):
            traj = stochastic_orbit(fp, meta, steps=steps,
                                   seed=rng.randint(0, 10**9))
            # Find first time the state differs from the fixed point
            for t, s in enumerate(traj[1:], 1):
                if s != fp:
                    escape_times.append(t)
                    break
            else:
                escape_times.append(steps)  # didn't escape

        results[(fp.f.table, fp.x)] = {
            "mean_escape_time": np.mean(escape_times),
            "median_escape_time": np.median(escape_times),
            "fraction_escaped": sum(1 for t in escape_times if t < steps) / num_trials,
        }

    return results


def stochastic_complexity(trajectory: list[State]) -> dict:
    """Compute complexity measures for a stochastic trajectory."""
    x_seq = [s.x for s in trajectory]
    f_seq = [s.f.table for s in trajectory]

    # Entropy of x values
    x_counts = Counter(x_seq)
    total = len(x_seq)
    x_probs = [c / total for c in x_counts.values()]
    x_entropy = -sum(p * np.log2(p) for p in x_probs if p > 0)

    # Entropy of function values
    f_counts = Counter(f_seq)
    f_probs = [c / total for c in f_counts.values()]
    f_entropy = -sum(p * np.log2(p) for p in f_probs if p > 0)

    # Transition entropy (conditional entropy of next state given current state)
    bigram_counts = Counter()
    unigram_counts = Counter()
    for i in range(len(trajectory) - 1):
        curr = (trajectory[i].f.table, trajectory[i].x)
        nxt = (trajectory[i+1].f.table, trajectory[i+1].x)
        bigram_counts[(curr, nxt)] += 1
        unigram_counts[curr] += 1

    transition_entropy = 0.0
    for (curr, nxt), count in bigram_counts.items():
        p_joint = count / (len(trajectory) - 1)
        p_cond = count / unigram_counts[curr]
        transition_entropy -= p_joint * np.log2(p_cond)

    # Function mutation rate
    f_changes = sum(1 for i in range(1, len(trajectory))
                   if trajectory[i].f != trajectory[i-1].f)
    mutation_rate = f_changes / max(len(trajectory) - 1, 1)

    return {
        "x_entropy": round(x_entropy, 4),
        "f_entropy": round(f_entropy, 4),
        "transition_entropy": round(transition_entropy, 4),
        "mutation_rate": round(mutation_rate, 4),
        "distinct_states": len(set((s.f.table, s.x) for s in trajectory)),
        "distinct_functions": len(set(s.f.table for s in trajectory)),
    }


if __name__ == "__main__":
    from dds import identity_meta, make_xor_output_meta, make_shift_table_meta

    n = 2
    funcs = enumerate_functions(n)
    print(f"=== Stochastic DDS, n={n} ===")
    print(f"|F| = {len(funcs)}, |States| = {len(funcs) * n}")

    # Compare deterministic meta-rules with noisy versions
    for det_name, det_phi in [
        ("identity", identity_meta),
        ("xor_output", make_xor_output_meta(n)),
        ("shift_table", make_shift_table_meta()),
    ]:
        print(f"\n--- {det_name} ---")
        for noise in [0.0, 0.05, 0.1, 0.3, 0.5]:
            meta = make_noisy_meta(det_phi, funcs, noise=noise)

            # Pick a starting state
            start = State(funcs[0], 0)
            traj = stochastic_orbit(start, meta, steps=1000, seed=42)
            cm = stochastic_complexity(traj)

            print(f"  noise={noise:.2f}: x_ent={cm['x_entropy']:.3f}, "
                  f"f_ent={cm['f_entropy']:.3f}, trans_ent={cm['transition_entropy']:.3f}, "
                  f"mut_rate={cm['mutation_rate']:.3f}, "
                  f"distinct_states={cm['distinct_states']}")

    # Escape rate analysis
    print(f"\n--- Escape rates from fixed points ---")
    for det_name, det_phi in [("identity", identity_meta)]:
        for noise in [0.01, 0.05, 0.1, 0.3]:
            meta = make_noisy_meta(det_phi, funcs, noise=noise)
            escapes = measure_escape_rate(meta, funcs, n, num_trials=200, steps=500)
            print(f"  {det_name}, noise={noise:.2f}:")
            for state_key, stats in escapes.items():
                print(f"    state={state_key}: mean_escape={stats['mean_escape_time']:.1f}, "
                      f"frac_escaped={stats['fraction_escaped']:.2f}")

    # Temperature-based meta-rule
    print(f"\n--- Temperature-based meta-rule ---")
    def hamming_energy(f: Func, x: int, g: Func) -> float:
        """Energy = Hamming distance between f and g tables."""
        return sum(1 for a, b in zip(f.table, g.table) if a != b)

    for temp in [0.1, 0.5, 1.0, 2.0, 5.0]:
        meta = make_temperature_meta(funcs, hamming_energy, temperature=temp)
        start = State(funcs[0], 0)
        traj = stochastic_orbit(start, meta, steps=1000, seed=42)
        cm = stochastic_complexity(traj)
        print(f"  temp={temp:.1f}: x_ent={cm['x_entropy']:.3f}, "
              f"f_ent={cm['f_entropy']:.3f}, mut_rate={cm['mutation_rate']:.3f}, "
              f"distinct_f={cm['distinct_functions']}")
