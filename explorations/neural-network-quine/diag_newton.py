"""Why did the first Newton step fail? Diagnostics on one network."""
import sys
import time

import torch

import newton
import quine as q

torch.set_num_threads(4)
m = q.Quine(n_layers=1, init="he_normal", proj_std=1.0)
m.load_state_dict(torch.load(sys.argv[1]))
m.double()
theta = m.theta.detach().clone()
r, sse, r2, _ = newton.stats(m, theta)
t0 = time.time()
J = newton.jacobian(m, theta)
print(f"Jacobian {tuple(J.shape)} in {time.time() - t0:.0f} s; SSE {sse:.4f}, R² {r2:.6f}")
A = J - torch.eye(len(theta), dtype=theta.dtype)
d = torch.linalg.solve(A, -r)
print(f"|d| / |θ| = {d.norm() / theta.norm():.3e};  solve residual |A d + r| / |r| = {(A @ d + r).norm() / r.norm():.3e}")
for eps in (1e-2, 1e-4, 1e-6, 1e-8):
    r_new = newton.predict(m, theta + eps * d) - (theta + eps * d)
    lin = r + eps * (A @ d)                    # = (1 - eps) r if the linearization holds
    print(f"  step {eps:.0e}: SSE {r_new.pow(2).sum():.6f} (now {sse:.6f}); "
          f"linearization error |r_new - (r + eps A d)| / |eps A d| = {(r_new - lin).norm() / (eps * (A @ d)).norm():.3e}")
sv = torch.linalg.svdvals(A)
print(f"singular values of J - I: largest {sv[0]:.3e}, smallest {sv[-1]:.3e}, condition number {sv[0] / sv[-1]:.3e}")
print("smallest 10:", [f"{x:.2e}" for x in sv[-10:].tolist()])
