"""E5 diagnostic: what does one Adamax epoch learn between regenerations?

After regeneration the weights are theta_R. One optimization epoch moves them
to theta_R + delta. Measure, for the network after that epoch:
  - error against theta_R (the snapshot targets it was trained on)
  - error against its current weights theta_R + delta (the paper's test loss)
  - how far regeneration lands from theta_R
"""
import torch
import quine as q

torch.set_num_threads(4)
m = q.Quine(seed=0)
opt = q.make_optimizer("adamax", m.parameters())
gen = torch.Generator().manual_seed(0)
q.grad_epoch(m, opt, gen)
q.regenerate(m)
for g in range(2, 6):
    theta_R = m.theta.detach().clone()
    q.grad_epoch(m, opt, gen)
    f = q.predict_all(m)
    theta = m.theta.detach()
    sq = lambda v: v.pow(2).sum().item()
    print(f"gen {g}: |theta_R|^2 {sq(theta_R):.3f}  |delta|^2 {sq(theta - theta_R):.3f}  "
          f"|f - theta_R|^2/|theta_R|^2 {sq(f - theta_R) / sq(theta_R):.3f}  "
          f"|f - theta|^2/|theta|^2 {sq(f - theta) / sq(theta):.3f}  "
          f"corr(f, delta) {torch.corrcoef(torch.stack([f, theta - theta_R]))[0, 1]:.3f}")
    q.regenerate(m)
    print(f"        after regeneration: |theta_new - theta_R|^2/|theta_R|^2 {sq(m.theta.detach() - theta_R) / sq(theta_R):.3f}, "
          f"new network's prediction RMS {q.predict_all(m).pow(2).mean().sqrt():.2e}")
