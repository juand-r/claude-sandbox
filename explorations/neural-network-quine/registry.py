"""Build the run registry in EXPERIMENTS.md from results/*.json and results/weights/*.pt.

Every run gets the same columns. Architecture and initialization come from the
saved weights (whose settings were recovered by exact match of P); training
settings come from the run's JSON config. Final R² is taken from the log when it
was logged, otherwise recomputed from the saved weights.

Usage: python registry.py      (rewrites the block between the registry markers)
"""
import json
import math
from pathlib import Path

import torch

import quine as q

HERE = Path(__file__).parent
RES = HERE / "results"
DOC = HERE / "EXPERIMENTS.md"
START, END = "<!-- registry start -->", "<!-- registry end -->"

FAMILIES = [  # (key, heading), in display order
    ("paper_opt", "A. Paper reproduction: gradient optimizers (paper E1, E2) and sensitivity runs"),
    ("paper_hill", "B. Paper reproduction: hill-climbing (paper E3, E4)"),
    ("paper_regen", "C. Paper reproduction: regeneration (paper E5, E6)"),
    ("paper_aux", "D. Paper reproduction: MNIST version (paper E7, E8)"),
    ("grid", "E. Long training from random initialization: weight init x P scale, layers, embedding SELU"),
    ("scratch_variants", "F. From random initialization: loss and target variants"),
    ("continuation", "G. Continuation from saved networks: learning rate, full gradient, 1 − R²"),
    ("newton", "H. Damped Newton (Levenberg–Marquardt) and pure Newton"),
]


def family(name, cfg):
    if name.startswith("aux"):
        return "paper_aux"
    if name.startswith("hill"):
        return "paper_hill"
    if name.startswith("regen"):
        return "paper_regen"
    if name.startswith(("lm", "newton")):
        return "newton"
    if cfg.get("start"):
        return "continuation"
    if cfg.get("epochs", 0) >= 1000:
        return "scratch_variants" if (cfg.get("full_grad") or cfg.get("normalized")) else "grid"
    return "paper_opt"


def fmt(x, nd=4):
    if x is None:
        return "—"
    if isinstance(x, float) and not math.isfinite(x):
        return "diverged"
    return f"{x:.{nd}f}"


def describe(name, cfg, settings):
    """Human-readable columns for one run."""
    init = {"torch_default": "default", "he_normal": "He"}.get(settings.get("init"), settings.get("init", "?"))
    proj = settings.get("proj_std")
    p_scale = "—" if proj is None else ("1" if abs(proj - 1) < 1e-6 else "0.058")
    layers = settings.get("n_layers", 2)
    emb = "no" if settings.get("embed_selu") is False else "yes"
    emb += ", output" if settings.get("out_selu") else ""
    if name.startswith(("lm", "newton")):
        method = cfg.get("method", "newton" if name.startswith("newton") else "lm")   # early runs lack the field
        training = {"lm": "damped Newton", "lm_normalized": "damped Newton", "newton": "pure Newton"}[method]
        loss = "1 − R²" if method == "lm_normalized" else "SSE"
        targets, lr = "live", "—"
        n_iter = None
    elif name.startswith("hill"):
        training, loss, targets, lr = f"hill-climbing σ={cfg.get('sigma'):g}", "SSE", "frozen", "—"
    elif name.startswith("regen"):
        training, loss, targets, lr = f"regeneration T={cfg.get('T')}", "SSE", "frozen", "Adamax default" if cfg.get("T") else "—"
    else:
        training = cfg.get("optimizer", "?")
        loss = "1 − R²" if cfg.get("normalized") else ("SSE + 0.01·CE" if name.startswith("aux_quine") else
                                                         "0.01·CE only" if name.startswith("aux_taskonly") else "SSE")
        targets = "live (full gradient)" if cfg.get("full_grad") else "frozen"
        lr = f"{cfg['lr']:g}" if cfg.get("lr") else "default"
    start = Path(cfg["start"]).stem if cfg.get("start") else "random init"
    return init, p_scale, layers, emb, training, loss, targets, lr, start


def final_r2_from_weights(name):
    w = RES / "weights" / f"{name}.pt"
    if not w.exists():
        return None, {}
    model, ckpt = q.load_weights(w)
    if model.aux:
        return None, ckpt["settings"]
    if not torch.isfinite(model.theta).all():
        return float("nan"), ckpt["settings"]
    return q.replication_stats(model)["r2"], ckpt["settings"]


def length(name, cfg, log):
    if name.startswith(("lm", "newton")):
        return f"{log[-1]['step']} it"
    if name.startswith("regen"):
        return f"{cfg.get('generations')} gen"
    return f"{log[-1].get('epoch', '?')} ep"


def build():
    rows = {k: [] for k, _ in FAMILIES}
    torch.set_num_threads(2)
    for f in sorted(RES.glob("*.json")):
        data = json.loads(f.read_text())
        if "config" not in data or "log" not in data:
            continue
        name, cfg, log = f.stem, data["config"], data["log"]
        r2_w, settings = final_r2_from_weights(name)
        last = [r for r in log if "L_SR" in r or "sse" in r]
        final_sse = (last[-1].get("L_SR", last[-1].get("sse")) if last else None)
        logged_r2 = [r["r2"] for r in log if "r2" in r and math.isfinite(r["r2"])]
        final_r2 = logged_r2[-1] if logged_r2 and "r2" in log[-1] else r2_w
        best_r2 = max(logged_r2) if logged_r2 else None
        rms = last[-1].get("theta_rms") if last else None
        diverged = any(r.get("phase") == "diverged" for r in log) or (final_sse is not None and not math.isfinite(final_sse))
        init, p_scale, layers, emb, training, loss, targets, lr, start = describe(name, cfg, settings)
        rows[family(name, cfg)].append(
            f"| {name} | {layers} | {init} | {p_scale} | {emb} | {training} | {loss} | {targets} | {lr} | "
            f"{length(name, cfg, log)} | {start} | {'diverged' if diverged else fmt(final_r2)} | {fmt(best_r2)} | "
            f"{'diverged' if diverged else fmt(final_sse, 2)} | {fmt(rms, 3)} |")
    out = [START, "",
           "Generated by `registry.py`; do not edit by hand. R² is computed with the network's",
           "current weights as targets. \"Best R²\" is the maximum over the logged epochs or",
           "iterations (— when the run predates R² logging). MNIST runs have no R² here because",
           "their predictions depend on the image paired with each coordinate.", ""]
    head = ("| run (results/<run>.json) | layers | weight init | P scale | SELU on embedding (\", output\": also on output) | training | loss | "
            "targets | lr | length | started from | final R² | best R² | final SSE | weight RMS |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for key, title in FAMILIES:
        if rows[key]:
            out += [f"### {title}", "", head, *rows[key], ""]
    out.append(END)
    return "\n".join(out)


def main():
    text = DOC.read_text()
    i, j = text.index(START), text.index(END) + len(END)
    DOC.write_text(text[:i] + build() + text[j:])
    print(f"registry written to {DOC.name}")


if __name__ == "__main__":
    main()
