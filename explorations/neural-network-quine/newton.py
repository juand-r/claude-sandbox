"""Newton's method on the quine equations f_θ(c) = θ_c for all c (IDEAS.md section 9).

The residual is r(θ) = f_θ(C) − θ, a map from ℝᴺ to ℝᴺ. Each step solves
(J − I) Δ = −r, where J = ∂f_θ(C)/∂θ, then backtracks on the step length until
SSE = |r|² decreases. Everything is in double precision. R² is tracked at every
step because θ = 0 also solves the equations.

Usage: python newton.py <start.pt> <n_layers> <out_name> [max_steps]
"""
import json
import sys
import time
from pathlib import Path

import torch
from torch.func import jacrev

import quine as q

JAC_CHUNK = 512          # coordinates per Jacobian chunk
MAX_HALVINGS = 12        # backtracking: step lengths 1, 1/2, ..., 1/2^12


def jacobian(model, theta, chunk=JAC_CHUNK):
    """J[c, k] = ∂f_θ(c)/∂θ_k for all coordinates c, as an N × N tensor."""
    n = model.n_params
    J = torch.empty(n, n, dtype=theta.dtype)
    f = lambda th, coords: model(coords, theta=th)[0]
    for s in range(0, n, chunk):
        coords = torch.arange(s, min(s + chunk, n))
        J[s:s + len(coords)] = jacrev(f)(theta, coords)
    return J


@torch.no_grad()
def predict(model, theta):
    out = []
    for s in range(0, model.n_params, q.EVAL_CHUNK):
        out.append(model(torch.arange(s, min(s + q.EVAL_CHUNK, model.n_params)), theta=theta)[0])
    return torch.cat(out)


def stats(model, theta):
    r = predict(model, theta) - theta
    sse = r.pow(2).sum().item()
    return r, sse, 1 - sse / (theta - theta.mean()).pow(2).sum().item(), theta.pow(2).mean().sqrt().item()


def newton(model, max_steps):
    theta = model.theta.detach().clone()
    r, sse, r2, rms = stats(model, theta)
    log = [{"step": 0, "sse": sse, "r2": r2, "theta_rms": rms, "t": 1.0, "seconds": 0.0}]
    print(f"step 0: SSE {sse:.6g}  R² {r2:.6f}  weight rms {rms:.4f}", flush=True)
    for k in range(1, max_steps + 1):
        t0 = time.time()
        A = jacobian(model, theta)
        A.diagonal().sub_(1.0)                       # A = J − I
        delta = torch.linalg.solve(A, -r)
        del A
        t = 1.0
        for _ in range(MAX_HALVINGS + 1):
            cand = theta + t * delta
            r_c, sse_c, r2_c, rms_c = stats(model, cand)
            if sse_c < sse:
                break
            t /= 2
        else:
            print(f"step {k}: no decrease along the Newton direction; stopping", flush=True)
            break
        theta, r, sse, r2, rms = cand, r_c, sse_c, r2_c, rms_c
        log.append({"step": k, "sse": sse, "r2": r2, "theta_rms": rms, "t": t,
                    "step_norm_rel": (t * delta).norm().item() / theta.norm().item(),
                    "seconds": time.time() - t0})
        print(f"step {k}: SSE {sse:.6g}  R² {r2:.6f}  weight rms {rms:.4f}  step length {t:g}  "
              f"({time.time() - t0:.0f} s)", flush=True)
    with torch.no_grad():
        model.theta.copy_(theta)
    return log


def main():
    start, n_layers, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    max_steps = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    torch.set_num_threads(4)
    model = q.Quine(n_layers=n_layers, init="he_normal", proj_std=1.0)
    model.load_state_dict(torch.load(start))
    model.double()
    log = newton(model, max_steps)
    res = Path(__file__).parent / "results"
    (res / f"{out}.json").write_text(json.dumps({"config": {"start": start, "n_layers": n_layers}, "log": log}, indent=1))
    torch.save(model.float().state_dict(), res / f"{out}.pt")
    print(f"wrote results/{out}.json")


if __name__ == "__main__":
    main()
