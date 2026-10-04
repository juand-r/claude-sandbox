import math
import sys
from pathlib import Path

import pytest
import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import quine as q  # noqa: E402

SMALL = 8  # hidden size for brute-force checks


def test_param_counts_match_paper():
    assert q.Quine().n_params == 20_100
    assert q.Quine(aux=True).n_params == 21_100


def test_views_share_storage_row_major():
    m = q.Quine(hidden=SMALL, aux=True)
    off = m.offsets()
    with torch.no_grad():
        m.theta.zero_()
        m.theta[off["W2"][0] + 3 * SMALL + 5] = 7.0
    assert m.view("W2")[3, 5] == 7.0
    assert m.view("W2").sum() == 7.0 and m.view("W1").sum() == 0.0
    assert off["W_cls"][1] == m.n_params


def explicit_forward(m, c, image=None):
    """Forward pass written out with an actual one-hot vector."""
    onehot = torch.zeros(m.n_params)
    onehot[c] = 1.0
    pre = onehot @ m.P_coord
    if m.aux:
        pre = torch.cat([pre, image @ m.P_img])
    h = F.selu(pre) if m.embed_selu else pre
    h = F.selu(m.view("W1") @ h)
    h = F.selu(m.view("W2") @ h)
    w = m.view("w_out") @ h
    if m.out_selu:
        w = F.selu(w)
    return w.squeeze(), (m.view("W_cls") @ h if m.aux else None)


@pytest.mark.parametrize("aux,out_selu,embed_selu",
                         [(False, False, True), (False, True, True), (True, False, True), (False, False, False)])
def test_forward_matches_one_hot_computation(aux, out_selu, embed_selu):
    m = q.Quine(hidden=SMALL, aux=aux, out_selu=out_selu, embed_selu=embed_selu, seed=1)
    coords = torch.tensor([0, 5, m.n_params - 1])
    images = torch.randn(3, q.IMG_DIM) if aux else None
    with torch.no_grad():
        w, logits = m(coords, images)
        for i, c in enumerate(coords):
            w_ref, l_ref = explicit_forward(m, c, images[i] if aux else None)
            assert torch.allclose(w[i], w_ref, atol=1e-6)
            if aux:
                assert torch.allclose(logits[i], l_ref, atol=1e-5)


def test_full_sr_loss_matches_brute_force_loop():
    m = q.Quine(hidden=SMALL, seed=2)
    with torch.no_grad():
        brute = sum((explicit_forward(m, c)[0] - m.theta[c]).item() ** 2 for c in range(m.n_params))
    assert math.isclose(q.full_sr_loss(m), brute, rel_tol=1e-5)


def test_regeneration_is_simultaneous():
    m = q.Quine(hidden=SMALL, seed=3)
    before = q.predict_all(m).clone()
    q.regenerate(m)
    assert torch.equal(m.theta.detach(), before)


def test_hill_climb_with_zero_noise_accepts_nothing():
    m = q.Quine(hidden=SMALL, seed=4)
    theta0 = m.theta.detach().clone()
    frac = q.hill_climb_epoch(m, sigma=0.0, gen=torch.Generator().manual_seed(0))
    assert frac == 0.0 and torch.equal(m.theta.detach(), theta0)


def test_hill_climb_never_increases_minibatch_loss():
    """Each accepted step lowers the loss of its own minibatch; check this on
    a single-minibatch network, where minibatch loss == full L_SR."""
    m = q.Quine(hidden=2, seed=5)   # 2*2*2 + 2 = 10 params = one minibatch
    assert m.n_params == q.BATCH_SIZE
    gen = torch.Generator().manual_seed(0)
    for _ in range(50):
        target = m.theta.detach().clone()
        before = q.sr_loss(q.predict_all(m), target).item()
        q.hill_climb_epoch(m, sigma=0.05, gen=gen)
        after = q.sr_loss(q.predict_all(m), target).item()
        assert after <= before


def test_grad_epoch_uses_snapshot_targets():
    """With one minibatch and plain SGD, one epoch is one step on
    sum (f(c) - theta_snapshot_c)^2, with no gradient through the target."""
    m = q.Quine(hidden=2, seed=6)
    ref = q.Quine(hidden=2, seed=6)
    opt = torch.optim.SGD(m.parameters(), lr=0.1)
    q.grad_epoch(m, opt, torch.Generator().manual_seed(0))
    target = ref.theta.detach().clone()
    q.sr_loss(ref(torch.arange(ref.n_params))[0], target).backward()
    with torch.no_grad():
        expected = ref.theta - 0.1 * ref.theta.grad
    assert torch.allclose(m.theta.detach(), expected, atol=1e-6)


def test_mnist_loader():
    tx, ty, vx, vy = q.load_mnist()
    assert tx.shape == (60_000, 784) and vx.shape == (10_000, 784)
    assert set(ty.unique().tolist()) == set(range(10))
    assert tx.min() == 0.0 and tx.max() == 1.0
    assert abs(tx.mean().item() - 0.1307) < 0.001   # the well-known MNIST pixel mean
