"""Neural network quine (Chang & Lipson, arXiv:1803.05859), reimplemented.

All learnable weights live in one flat vector `theta`. Coordinate c is the
index c into theta, and the matrices W1, W2, w_out (and W_cls for the
auxiliary quine) are views into it. Layout, in order:

    W1     (H, H)   hidden layer 1 -> hidden layer 2
    W2     (H, H)   hidden layer 2 -> hidden layer 3
    w_out  (1, H)   hidden layer 3 -> weight prediction
    W_cls  (K, H)   hidden layer 3 -> class logits   (auxiliary quine only)

Network (no biases; see PLAN.md item 1):

    h0 = selu(P_coord[c])                      vanilla
    h0 = selu([P_coord[c], x @ P_img])         auxiliary (50 + 50 units)
    h1 = selu(W1 h0);  h2 = selu(W2 h1)
    weight prediction = w_out h2   (optionally followed by selu)
    class logits      = W_cls h2

P_coord[c] is the one-hot vector e_c times the fixed projection, i.e. row c.
"""

import gzip
import math
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HIDDEN = 100
N_CLASSES = 10
IMG_DIM = 28 * 28
BATCH_SIZE = 10          # paper: "we used a minibatch of size 10"
LAMBDA = 0.01            # paper: lambda in L_Aux
TEMPERATURE = 0.01       # paper: softmax temperature of the auxiliary output
EVAL_CHUNK = 4096        # coordinates per chunk when evaluating all of them

INIT_SCHEMES = ("he_normal", "he_uniform", "lecun_normal", "torch_default")

# Defaults chosen to reproduce the paper's initial losses (NOTES.md, E0).
# The paper says "He init", but He init cannot give its initial L_SR of 90.16.
DEFAULT_INIT = "torch_default"                    # U(-1/sqrt(100), 1/sqrt(100)), std 0.0577
DEFAULT_PROJ_STD = 1.0 / math.sqrt(3 * HIDDEN)    # coordinate projection, same std as the weights
IMG_PROJ_STD = 1.0 / math.sqrt(3 * IMG_DIM)       # std of a default nn.Linear(784, 50)


def init_weights_(w, scheme, gen):
    """Fill a (fan_out, fan_in) matrix in place according to `scheme`."""
    fan_in = w.shape[1]
    if scheme == "he_normal":
        w.normal_(0.0, math.sqrt(2.0 / fan_in), generator=gen)
    elif scheme == "he_uniform":
        b = math.sqrt(6.0 / fan_in)
        w.uniform_(-b, b, generator=gen)
    elif scheme == "lecun_normal":
        w.normal_(0.0, math.sqrt(1.0 / fan_in), generator=gen)
    elif scheme == "torch_default":  # nn.Linear default: U(-1/sqrt(fan_in), 1/sqrt(fan_in))
        b = 1.0 / math.sqrt(fan_in)
        w.uniform_(-b, b, generator=gen)
    else:
        raise ValueError(f"unknown init scheme {scheme!r}")


class Quine(nn.Module):
    def __init__(self, aux=False, hidden=HIDDEN, init=DEFAULT_INIT,
                 proj_std=DEFAULT_PROJ_STD, out_selu=False, embed_selu=True, seed=0):
        super().__init__()
        self.aux, self.hidden, self.out_selu = aux, hidden, out_selu
        self.embed_selu = embed_selu   # selu on the looked-up projection row (paper: "every layer")
        shapes = {"W1": (hidden, hidden), "W2": (hidden, hidden), "w_out": (1, hidden)}
        if aux:
            shapes["W_cls"] = (N_CLASSES, hidden)
        self.shapes = shapes
        self.n_params = sum(a * b for a, b in shapes.values())

        gen = torch.Generator().manual_seed(seed)
        self.theta = nn.Parameter(torch.empty(self.n_params))
        with torch.no_grad():
            for name in shapes:
                init_weights_(self.view(name), init, gen)

        n_coord_units = hidden // 2 if aux else hidden
        self.register_buffer("P_coord", torch.randn(self.n_params, n_coord_units, generator=gen) * proj_std)
        if aux:
            P_img = torch.randn(IMG_DIM, hidden - n_coord_units, generator=gen) * IMG_PROJ_STD
            self.register_buffer("P_img", P_img)

    # -- parameter layout -------------------------------------------------
    def offsets(self):
        """Return {name: (start, end)} slices of theta."""
        out, start = {}, 0
        for name, (a, b) in self.shapes.items():
            out[name] = (start, start + a * b)
            start += a * b
        return out

    def view(self, name, theta=None):
        theta = self.theta if theta is None else theta
        s, e = self.offsets()[name]
        return theta[s:e].view(self.shapes[name])

    # -- forward ------------------------------------------------------------
    def first_layer(self, coords, images=None):
        pre = self.P_coord[coords]
        if self.aux:
            if images is None:
                raise ValueError("the auxiliary quine needs an image for every coordinate")
            pre = torch.cat([pre, images @ self.P_img], dim=1)
        return F.selu(pre) if self.embed_selu else pre

    def forward(self, coords, images=None, theta=None):
        """Return (weight predictions [B], class logits [B, K] or None).

        `theta` lets hill-climbing evaluate a perturbed vector without
        touching the model's own parameters.
        """
        h = self.first_layer(coords, images)
        h = F.selu(h @ self.view("W1", theta).T)
        h = F.selu(h @ self.view("W2", theta).T)
        w = (h @ self.view("w_out", theta).T).squeeze(1)
        if self.out_selu:
            w = F.selu(w)
        logits = h @ self.view("W_cls", theta).T if self.aux else None
        return w, logits


# -- losses ---------------------------------------------------------------
def sr_loss(pred, target):
    """Self-replicating loss, Eq. 2: sum of squared errors."""
    return ((pred - target) ** 2).sum()


def task_loss(logits, labels):
    """Summed cross-entropy of softmax(logits / T)."""
    return F.cross_entropy(logits / TEMPERATURE, labels, reduction="sum")


@torch.no_grad()
def predict_all(model, images=None):
    """f_theta(c) for every coordinate c. `images[c]` pairs with coordinate c."""
    preds = []
    for s in range(0, model.n_params, EVAL_CHUNK):
        coords = torch.arange(s, min(s + EVAL_CHUNK, model.n_params))
        imgs = None if images is None else images[coords]
        preds.append(model(coords, imgs)[0])
    return torch.cat(preds)


@torch.no_grad()
def full_sr_loss(model, images=None):
    """The 'test loss' of the paper: L_SR over all coordinates, current targets."""
    return sr_loss(predict_all(model, images), model.theta).item()


@torch.no_grad()
def replication_stats(model, images=None):
    """L_SR plus the derived quantities discussed in NOTES.md."""
    pred = predict_all(model, images)
    theta = model.theta
    L = sr_loss(pred, theta).item()
    n = model.n_params
    return {
        "L_SR": L,
        "rms_error": math.sqrt(L / n),              # paper's "average weight prediction margin"
        "mean_abs_error": (pred - theta).abs().mean().item(),
        "srq_paper": math.log(n) - math.log(L) if L > 0 else float("inf"),  # paper's "self-replicating quotient"
        "theta_rms": theta.pow(2).mean().sqrt().item(),
        "pred_rms": pred.pow(2).mean().sqrt().item(),
        "rel_error": L / theta.pow(2).sum().item(),   # L_SR / ||theta||^2
        "r2": 1.0 - L / (theta - theta.mean()).pow(2).sum().item(),  # coefficient of determination
    }


# -- training methods ---------------------------------------------------------
def make_optimizer(name, params):
    """Optimizers of Fig. 4. 'Default hyperparameter settings' = torch defaults,
    except the two learning rates the paper states."""
    if name == "sgd":
        return torch.optim.SGD(params, lr=0.01)
    if name == "sgd_momentum":
        return torch.optim.SGD(params, lr=0.01, momentum=0.9)
    if name == "adam":
        return torch.optim.Adam(params)
    if name == "adagrad":
        return torch.optim.Adagrad(params)
    if name == "adamax":
        return torch.optim.Adamax(params)
    if name == "rmsprop":
        return torch.optim.RMSprop(params)
    raise ValueError(f"unknown optimizer {name!r}")


def grad_epoch(model, opt, gen, train_images=None, train_labels=None, task_only=False):
    """One epoch of the paper's pseudo-code: snapshot targets, then a pass over
    all coordinates in random minibatches of 10.

    Auxiliary quine: each coordinate is paired with a random training image,
    and the loss is L_SR + lambda * L_Task on the minibatch. With task_only
    the L_SR term is dropped (classification-only baseline).
    """
    target = model.theta.detach().clone()
    perm = torch.randperm(model.n_params, generator=gen)
    if model.aux:
        img_idx = torch.randint(len(train_images), (model.n_params,), generator=gen)
    for s in range(0, model.n_params, BATCH_SIZE):
        coords = perm[s:s + BATCH_SIZE]
        if model.aux:
            idx = img_idx[s:s + BATCH_SIZE]
            pred, logits = model(coords, train_images[idx])
            loss = LAMBDA * task_loss(logits, train_labels[idx])
            if not task_only:
                loss = loss + sr_loss(pred, target[coords])
        else:
            pred, _ = model(coords)
            loss = sr_loss(pred, target[coords])
        opt.zero_grad()
        loss.backward()
        opt.step()


@torch.no_grad()
def hill_climb_epoch(model, sigma, gen):
    """One epoch of hill-climbing (vanilla quine): for each minibatch, perturb
    every parameter with N(0, sigma^2) noise and keep the perturbation if the
    minibatch loss against the epoch's snapshot targets decreases.
    Returns the fraction of accepted perturbations."""
    target = model.theta.detach().clone()
    theta = model.theta.data
    perm = torch.randperm(model.n_params, generator=gen)
    accepted = 0
    for s in range(0, model.n_params, BATCH_SIZE):
        coords = perm[s:s + BATCH_SIZE]
        candidate = theta + sigma * torch.randn(model.n_params, generator=gen)
        old = sr_loss(model(coords, theta=theta)[0], target[coords])
        new = sr_loss(model(coords, theta=candidate)[0], target[coords])
        if new < old:
            theta.copy_(candidate)
            accepted += 1
    return accepted / math.ceil(model.n_params / BATCH_SIZE)


@torch.no_grad()
def regenerate(model, images=None):
    """Replace every weight by the network's prediction of it, all at once."""
    model.theta.copy_(predict_all(model, images))


# -- MNIST ------------------------------------------------------------------
def _read_idx(path):
    with gzip.open(path, "rb") as f:
        data = f.read()
    ndim = data[3]
    dims = [int.from_bytes(data[4 + 4 * i: 8 + 4 * i], "big") for i in range(ndim)]
    return np.frombuffer(data, dtype=np.uint8, offset=4 + 4 * ndim).reshape(dims)


def load_mnist(root=Path(__file__).parent / "data" / "mnist"):
    """Return (train_x, train_y, test_x, test_y); x in [0, 1], flattened to 784."""
    def images(name):
        x = torch.from_numpy(_read_idx(root / name).astype(np.float32) / 255.0)
        return x.reshape(len(x), -1)

    def labels(name):
        return torch.from_numpy(_read_idx(root / name).astype(np.int64))

    return (images("train-images-idx3-ubyte.gz"), labels("train-labels-idx1-ubyte.gz"),
            images("t10k-images-idx3-ubyte.gz"), labels("t10k-labels-idx1-ubyte.gz"))


def test_pairing_images(model, test_x):
    """Fixed pairing for evaluating L_SR of the auxiliary quine:
    coordinate c gets test image c mod len(test_x)."""
    return test_x[torch.arange(model.n_params) % len(test_x)]


@torch.no_grad()
def classification_eval(model, test_x, test_y):
    """Test-set task loss and accuracy. Test image i is paired with coordinate i mod N."""
    total_loss, correct = 0.0, 0
    for s in range(0, len(test_x), EVAL_CHUNK):
        idx = torch.arange(s, min(s + EVAL_CHUNK, len(test_x)))
        _, logits = model(idx % model.n_params, test_x[idx])
        total_loss += task_loss(logits, test_y[idx]).item()
        correct += (logits.argmax(1) == test_y[idx]).sum().item()
    return total_loss, correct / len(test_x)
