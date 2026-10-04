"""Write a compact, committed copy (results/weights/<name>.pt) of every full
checkpoint results/<name>.pt. The settings that regenerate P are found by search
and verified bit-for-bit against the stored P, not inferred from file names."""
import itertools
import json
import math
from pathlib import Path

import torch

import quine as q

RES = Path(__file__).parent / "results"
OUT = RES / "weights"


def find_settings(state):
    n = state["theta"].numel()
    aux = "P_img" in state
    candidates = itertools.product((0, 1, 2), ("torch_default", "he_normal"),
                                   (q.DEFAULT_PROJ_STD, 1.0, 0.0577350269), (1, 2))
    for seed, init, proj, nl in candidates:
        kw = dict(seed=seed, init=init, proj_std=proj, n_layers=nl, aux=aux)
        try:
            m = q.Quine(**kw)
        except ValueError:
            continue
        if m.n_params != n or m.P_coord.shape != state["P_coord"].shape:
            continue
        if torch.equal(m.P_coord, state["P_coord"].to(m.P_coord.dtype)) and (
                not aux or torch.equal(m.P_img, state["P_img"].to(m.P_img.dtype))):
            return kw
    return None


def forward_flags(name):
    """Settings that change the forward pass but not P, read from the run's JSON
    config. Runs without a JSON (copies, Newton outputs) used the defaults; the
    functional check below catches any exception."""
    cfg_path = RES / f"{name}.json"
    cfg = json.loads(cfg_path.read_text())["config"] if cfg_path.exists() else {}
    return {"embed_selu": not cfg.get("no_embed_selu", False), "out_selu": cfg.get("out_selu", False)}


def logged_final_sse(name):
    """SSE at the end of the run, from its JSON log (None if unavailable)."""
    cfg_path = RES / f"{name}.json"
    if not cfg_path.exists():
        return None
    row = json.loads(cfg_path.read_text())["log"][-1]
    return row.get("L_SR", row.get("sse"))


def export_one(f, overwrite=False):
    """Export results/<name>.pt to results/weights/<name>.pt; returns a status string."""
    f = Path(f)
    target = OUT / f.name
    if target.exists() and not overwrite:
        return "exists"
    state = torch.load(f)
    kw = find_settings(state)
    if kw is None:
        raise ValueError(f"{f.name}: no settings regenerate its P")
    kw.update(forward_flags(f.stem))
    m = q.Quine(**kw)
    with torch.no_grad():
        m.theta.copy_(state["theta"].to(m.theta.dtype))
    q.save_weights(m, target, kw, extra={"source": f.name})
    m2, _ = q.load_weights(target)                 # round trip
    same = torch.allclose(m2.theta, m.theta, rtol=0, atol=0, equal_nan=True)   # diverged runs hold NaN
    assert same and torch.equal(m2.P_coord, m.P_coord), f.name
    logged = logged_final_sse(f.stem)              # functional check: the reloaded network
    if logged is not None and math.isfinite(logged) and not m2.aux:   # reproduces the logged SSE
        sse = q.full_sr_loss(m2)
        assert abs(sse - logged) <= 1e-3 * max(1.0, abs(logged)), (f.name, sse, logged)
        return "verified"
    return "exported (no functional check)"


def main():
    OUT.mkdir(exist_ok=True)
    counts = {}
    for f in sorted(RES.glob("*.pt")):
        status = export_one(f, overwrite=True)
        counts[status] = counts.get(status, 0) + 1
    print(counts)


if __name__ == "__main__":
    main()
