"""Does each self-report depend on the weight it reports? (IDEAS.md section 10)

For a saved network, compute the Jacobian J[c, k] = ∂f(c)/∂θ_k and report:
  - the self-sensitivity ∂f(c)/∂θ_c (1 for a network that reads its weights off),
  - the share of each report's sensitivity that goes to its own weight,
    |J_cc| / |J_c,:|,
  - both per block of weights.

Usage: python diag_grounding.py results/weights/<name>.pt
"""
import sys

import torch

import newton
import quine as q


def main(path):
    torch.set_num_threads(1)
    m, _ = q.load_weights(path, dtype=torch.float64)
    theta = m.theta.detach().clone()
    J = newton.jacobian(m, theta)
    d = J.diagonal()
    row = J.norm(dim=1)
    print(f"{path}: R² {q.replication_stats(m)['r2']:.4f}, N = {m.n_params}")
    print(f"  self-sensitivity ∂f(c)/∂θ_c: mean {d.mean():.4f}, median {d.median():.4f}")
    print(f"  own-weight share |J_cc| / |J_c,:|: median {(d.abs() / row).median():.5f}")
    print(f"  sensitivity of one report to all weights |J_c,:|: median {row.median():.3f}")
    for name, (s, e) in m.offsets().items():
        print(f"  block {name:5s} ({e - s:5d} weights): mean ∂f(c)/∂θ_c {d[s:e].mean():.4f}, "
              f"median own-weight share {(d[s:e].abs() / row[s:e]).median():.5f}")


if __name__ == "__main__":
    main(sys.argv[1])
