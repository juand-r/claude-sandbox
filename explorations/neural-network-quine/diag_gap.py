"""Where is the remaining error of a trained quine: fit or drift?

From a saved network, take the usual frozen snapshot of the weights and train
one epoch. Then compare
  R² against the snapshot (how well it fits the targets it trained on), and
  R² against its current weights (the quine measure),
and measure how far the weights moved during the epoch (drift). Repeated for
several learning rates, each from the same starting network.
"""
import copy
import sys

import torch

import quine as q

torch.set_num_threads(2)


def r2(pred, target):
    return 1 - ((pred - target) ** 2).sum().item() / ((target - target.mean()) ** 2).sum().item()


def main(path, n_layers):
    base = q.Quine(n_layers=n_layers, init="he_normal", proj_std=1.0)
    base.load_state_dict(torch.load(path))
    print(f"{path}: R² now {r2(q.predict_all(base), base.theta.detach()):.4f}")
    for lr in (2e-3, 2e-4, 2e-5):
        m = copy.deepcopy(base)
        snap = m.theta.detach().clone()
        opt = torch.optim.Adamax(m.parameters(), lr=lr)
        q.grad_epoch(m, opt, torch.Generator().manual_seed(0))
        f, th = q.predict_all(m), m.theta.detach()
        drift = ((th - snap) ** 2).sum().item() / ((snap - snap.mean()) ** 2).sum().item()
        print(f"  lr {lr:.0e}, one epoch: R² vs snapshot {r2(f, snap):.4f}   R² vs current weights {r2(f, th):.4f}"
              f"   drift |Δθ|²/var-sum {drift:.4f}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
