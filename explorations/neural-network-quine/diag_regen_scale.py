"""E6 diagnostic: pure regeneration (T=0) from initial weights scaled by alpha.
Prints weight RMS after each of 15 generations."""
import sys
import torch
import quine as q

G = 15
for seed in (0, 1, 2):
    for alpha in (0.25, 0.5, 0.75, 1.0, 1.5):
        m = q.Quine(seed=seed)
        with torch.no_grad():
            m.theta.mul_(alpha)
        rms = []
        for g in range(G):
            q.regenerate(m)
            r = m.theta.pow(2).mean().sqrt().item()
            rms.append(r)
            if not (r < 1e6):
                break
        fate = "zero" if rms[-1] < 1e-8 else ("diverged" if not rms[-1] < 1e6 else "other")
        print(f"seed {seed} alpha {alpha:4.2f}: " + " ".join(f"{r:.1e}" for r in rms[:8]) + f" ... -> {fate}")
