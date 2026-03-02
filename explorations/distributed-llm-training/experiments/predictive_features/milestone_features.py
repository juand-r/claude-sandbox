"""
Compute features at PPL milestones for predicting future trainability.

Each function takes model/optimizer/data state and returns a dict of features.
Features are grouped by compute cost: cheap (no extra passes), medium (extra
forward passes), expensive (extra backward passes).
"""

import math
import copy
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Optional, Iterator


def compute_cheap_features(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    initial_weights: Dict[str, torch.Tensor],
    history: Dict[str, List[float]],
    config: Dict,
    stage: int,
    steps: int,
    wall_time: float,
) -> Dict[str, float]:
    """Features that require no extra forward/backward passes.

    Args:
        model: Current model (should have gradients from most recent backward).
        optimizer: Current optimizer (Adam — we read its state).
        initial_weights: Snapshot of model weights at initialization.
        history: Dict with keys 'loss', 'ppl', 'timestamps' — lists of recent values.
        config: Current hyperparameter config dict (must have 'lr', 'batch_size').
        stage: Current milestone stage number.
        steps: Total training steps so far.
        wall_time: Wall-clock seconds since training started.
    """
    features = {}

    # --- Gradient statistics ---
    grad_norms = []
    layer_grad_norms = {}
    for name, p in model.named_parameters():
        if p.grad is not None:
            gn = p.grad.data.norm(2).item()
            grad_norms.append(gn)
            # Group by layer (take first dotted component, e.g. "layers.0")
            parts = name.split(".")
            layer_key = ".".join(parts[:2]) if len(parts) > 1 else parts[0]
            if layer_key not in layer_grad_norms:
                layer_grad_norms[layer_key] = 0.0
            layer_grad_norms[layer_key] += gn ** 2

    features["grad_norm"] = math.sqrt(sum(g**2 for g in grad_norms)) if grad_norms else 0.0
    features["grad_var"] = float(np.var(grad_norms)) if len(grad_norms) > 1 else 0.0
    # Per-layer gradient norms (sqrt of summed squares within layer)
    for k, v in layer_grad_norms.items():
        features[f"grad_layer_norm_{k}"] = math.sqrt(v)

    # --- Optimizer state (Adam) ---
    m_magnitudes = []
    v_magnitudes = []
    effective_steps = []
    v_max = 0.0
    eps = 1e-8  # Adam default

    for group in optimizer.param_groups:
        eps = group.get("eps", 1e-8)
        for p in group["params"]:
            state = optimizer.state.get(p, {})
            if "exp_avg" in state and "exp_avg_sq" in state:
                m = state["exp_avg"]
                v = state["exp_avg_sq"]
                m_mag = m.abs().mean().item()
                v_mag = v.abs().mean().item()
                m_magnitudes.append(m_mag)
                v_magnitudes.append(v_mag)
                # Effective step size: |m| / sqrt(v + eps)
                eff = (m.abs() / (v.sqrt() + eps)).mean().item()
                effective_steps.append(eff)
                v_max = max(v_max, v.max().item())

    features["adam_m_mean"] = float(np.mean(m_magnitudes)) if m_magnitudes else 0.0
    features["adam_v_mean"] = float(np.mean(v_magnitudes)) if v_magnitudes else 0.0
    features["adam_effective_step"] = float(np.mean(effective_steps)) if effective_steps else 0.0
    features["adam_v_max"] = v_max

    # --- Loss / training dynamics ---
    recent_losses = history.get("loss", [])
    window = min(50, len(recent_losses))
    if window > 1:
        recent = recent_losses[-window:]
        features["loss_variance"] = float(np.var(recent))
        # Linear fit slope
        x = np.arange(window, dtype=np.float64)
        y = np.array(recent, dtype=np.float64)
        slope = np.polyfit(x, y, 1)[0]
        features["loss_slope"] = float(slope)
    else:
        features["loss_variance"] = 0.0
        features["loss_slope"] = 0.0

    features["steps"] = steps
    features["wall_time"] = wall_time

    # --- Weight statistics ---
    weight_norm_sq = 0.0
    dist_from_init_sq = 0.0
    layer_weight_norms = {}

    for name, p in model.named_parameters():
        w_sq = p.data.norm(2).item() ** 2
        weight_norm_sq += w_sq

        parts = name.split(".")
        layer_key = ".".join(parts[:2]) if len(parts) > 1 else parts[0]
        if layer_key not in layer_weight_norms:
            layer_weight_norms[layer_key] = 0.0
        layer_weight_norms[layer_key] += w_sq

        if name in initial_weights:
            diff = (p.data - initial_weights[name]).norm(2).item()
            dist_from_init_sq += diff ** 2

    features["weight_norm"] = math.sqrt(weight_norm_sq)
    features["weight_dist_from_init"] = math.sqrt(dist_from_init_sq)
    for k, v in layer_weight_norms.items():
        features[f"weight_layer_norm_{k}"] = math.sqrt(v)

    # --- Config / meta ---
    features["lr"] = config.get("lr", 0.0)
    features["batch_size"] = config.get("batch_size", 0)
    features["stage"] = stage

    # --- PPL and its derivative ---
    recent_ppls = history.get("ppl", [])
    features["ppl"] = recent_ppls[-1] if recent_ppls else 0.0

    ppl_window = min(50, len(recent_ppls))
    if ppl_window > 1:
        recent_p = recent_ppls[-ppl_window:]
        x = np.arange(ppl_window, dtype=np.float64)
        y = np.array(recent_p, dtype=np.float64)
        ppl_slope = np.polyfit(x, y, 1)[0]
        features["ppl_derivative"] = float(ppl_slope)
    else:
        features["ppl_derivative"] = 0.0

    return features


def compute_grad_snr(
    model: nn.Module,
    loss_fn,
    data_iter: Iterator,
    n_batches: int = 5,
) -> Dict[str, float]:
    """Gradient signal-to-noise ratio: mean(grad)^2 / var(grad) across mini-batches.

    Requires n_batches extra backward passes.
    """
    grad_accum = {}  # name -> list of gradient tensors
    model.train()

    computed = 0
    for batch in data_iter:
        if computed >= n_batches:
            break
        model.zero_grad()
        loss = loss_fn(model, batch)
        loss.backward()

        for name, p in model.named_parameters():
            if p.grad is not None:
                if name not in grad_accum:
                    grad_accum[name] = []
                grad_accum[name].append(p.grad.data.clone())
        computed += 1

    if computed < 2:
        return {"grad_snr": 0.0}

    # Compute SNR per parameter, then average
    snrs = []
    for name, grads in grad_accum.items():
        stacked = torch.stack(grads)  # (n_batches, *param_shape)
        mean_grad = stacked.mean(dim=0)
        var_grad = stacked.var(dim=0)
        # SNR = mean^2 / var, averaged over parameter elements
        # Avoid division by zero
        snr = (mean_grad ** 2 / (var_grad + 1e-10)).mean().item()
        snrs.append(snr)

    return {"grad_snr": float(np.mean(snrs))}


def compute_sharpness(
    model: nn.Module,
    loss_fn,
    data_batch,
    n_perturbations: int = 5,
    sigma_scale: float = 0.01,
) -> Dict[str, float]:
    """SAM-style sharpness: perturb weights, measure loss change.

    Args:
        sigma_scale: Perturbation magnitude relative to weight norm.
    """
    model.eval()

    # Compute base loss
    with torch.no_grad():
        base_loss = loss_fn(model, data_batch).item()

    # Compute weight norm for scaling perturbation
    weight_norm = 0.0
    for p in model.parameters():
        weight_norm += p.data.norm(2).item() ** 2
    weight_norm = math.sqrt(weight_norm)
    sigma = sigma_scale * weight_norm

    # Save original weights
    original_state = {name: p.data.clone() for name, p in model.named_parameters()}

    deltas = []
    for _ in range(n_perturbations):
        # Add random perturbation
        for p in model.parameters():
            noise = torch.randn_like(p.data) * sigma / math.sqrt(p.data.numel())
            p.data.add_(noise)

        with torch.no_grad():
            perturbed_loss = loss_fn(model, data_batch).item()

        deltas.append(perturbed_loss - base_loss)

        # Restore original weights
        for name, p in model.named_parameters():
            p.data.copy_(original_state[name])

    model.train()
    return {"sharpness": float(np.mean(deltas))}


def compute_hessian_trace(
    model: nn.Module,
    loss_fn,
    data_batch,
    n_vectors: int = 5,
) -> Dict[str, float]:
    """Hutchinson stochastic trace estimate: E[v^T H v] where v ~ Rademacher.

    Requires n_vectors backward passes (via Hv product).
    """
    model.train()
    model.zero_grad()

    # Forward + backward to get gradients
    loss = loss_fn(model, data_batch)
    grads = torch.autograd.grad(loss, model.parameters(), create_graph=True)

    trace_estimates = []
    for _ in range(n_vectors):
        # Rademacher random vector
        v = [torch.randint_like(p, 0, 2) * 2.0 - 1.0 for p in model.parameters()]

        # Compute Hv via grad(g^T v)
        gv = sum((g * vi).sum() for g, vi in zip(grads, v))
        hv = torch.autograd.grad(gv, model.parameters(), retain_graph=True)

        # Trace estimate = v^T Hv
        trace_est = sum((vi * hvi).sum().item() for vi, hvi in zip(v, hv))
        trace_estimates.append(trace_est)

    model.zero_grad()
    return {"hessian_trace": float(np.mean(trace_estimates))}


def compute_all_features(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    loss_fn,
    initial_weights: Dict[str, torch.Tensor],
    history: Dict[str, List[float]],
    config: Dict,
    stage: int,
    steps: int,
    wall_time: float,
    data_iter: Optional[Iterator] = None,
    data_batch=None,
    expensive: bool = True,
) -> Dict[str, float]:
    """Compute all features. Set expensive=False to skip costly features."""
    features = compute_cheap_features(
        model, optimizer, initial_weights, history, config, stage, steps, wall_time
    )

    if data_iter is not None:
        features.update(compute_grad_snr(model, loss_fn, data_iter))

    if expensive and data_batch is not None:
        features.update(compute_sharpness(model, loss_fn, data_batch))
        features.update(compute_hessian_trace(model, loss_fn, data_batch))

    return features
