"""How much does weight c influence the network's output for weight c, compared
with how much the other weights influence that output? (Asked in discussion,
2026-10-05.) For a random sample of hidden-layer weights c, compute the row
∂f(c)/∂θ of the Jacobian and compare |∂f(c)/∂θ_c| with |∂f(c)/∂θ_k| for k ≠ c.

Usage: python diag_own_influence.py <weights.pt> [n_sample]
"""
import sys

import torch
from torch.func import jacrev

import quine as q

path = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
torch.manual_seed(0)
m, _ = q.load_weights(path, dtype=torch.float64)
th = m.theta.detach().clone()
n_hidden = m.offsets()["w_out"][0]                       # W1 and W2 come first in θ
cs = torch.randperm(n_hidden)[:n]
J = jacrev(lambda t: m(cs, theta=t)[0])(th)              # n × N
rows = torch.arange(n)
own = J[rows, cs]
others = J.abs().clone()
others[rows, cs] = float("nan")
print(f"{path}: {n} random hidden-layer weights c, N = {m.n_params}")
print(f"  ∂f(c)/∂θ_c: mean {own.mean():.4f}, median of |·| {own.abs().median():.4f}")
print(f"  |∂f(c)/∂θ_k|, k ≠ c, median over k then over c: {others.nanmedian(dim=1).values.median():.4f}")
print(f"  number of weights k with |∂f(c)/∂θ_k| > |∂f(c)/∂θ_c|: median over c "
      f"{int((J.abs() > own.abs()[:, None]).sum(1).median())} of {m.n_params}")
