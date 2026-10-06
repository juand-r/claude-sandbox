import torch

import lm
import measure as Ms
import train as T


def small_model(seed=0):
    torch.manual_seed(seed)
    return lm.SelfReportLM(n_text=64, dim=16, n_layers=2, n_heads=2, ctx=8)


def test_question_layout_and_report():
    m = small_model()
    t, i = torch.tensor([3, 5]), torch.tensor([0, 7])
    emb = torch.stack([m.E[m.query_id].expand(2, -1), m.E[m.coord_id(i)], m.E[t]], dim=1)
    assert torch.equal(emb[:, 2], m.E[t])                       # t is last, its input is E[t]
    assert m.coord_id(15) == m.E.shape[0] - 1                    # COORD_15 is the last row
    torch.testing.assert_close(m.report(t, i), m.answer(m.E[t], i))
    # the answer depends on which coordinate is asked
    a = m.report(torch.tensor([3, 3]), torch.tensor([0, 1]))
    assert a[0] != a[1]


def test_lm_is_causal_and_tied():
    m = small_model()
    ids = torch.randint(0, 64, (1, 8))
    ids2 = ids.clone()
    ids2[0, 5] = (ids[0, 5] + 1) % 64
    with torch.no_grad():
        a, b = m.lm_logits(ids), m.lm_logits(ids2)
    torch.testing.assert_close(a[0, :5], b[0, :5])               # earlier positions unaffected
    assert not torch.allclose(a[0, 5:], b[0, 5:])
    assert a.shape[-1] == 64                                     # special symbols are never predicted
    with torch.no_grad():
        m.E[10] += 1.0                                           # tied: the output side changes too
        c = m.lm_logits(ids)
    assert not torch.allclose(a[..., 10], c[..., 10])


def test_report_loss_is_one_minus_r2_and_target_is_detached():
    m = small_model()
    t, i = torch.tensor([1, 2, 3, 4, 5]), torch.tensor([0, 3, 6, 9, 12])
    with torch.no_grad():
        expected = 1 - lm.r2(m.report(t, i), m.E[t, i])
    assert abs(T.report_loss(m, t, i).item() - expected) < 1e-5
    T.report_loss(m, t, i).backward()
    g = m.E.grad.clone()
    m.E.grad = None
    const = m.E[t, i].detach().clone()
    a = m.report(t, i)
    (((a - const) ** 2).mean() / const.var(unbiased=False)).backward()
    torch.testing.assert_close(g, m.E.grad)


def test_split():
    tr, ho = lm.split_tokens(0)
    assert len(ho) == lm.N_TEXT // 4 and len(tr) + len(ho) == lm.N_TEXT
    assert not set(tr.tolist()) & set(ho.tolist())


def test_lr_schedule():
    assert abs(T.lr_at(0, 1000) - T.LR / T.WARMUP) < 1e-12
    assert abs(T.lr_at(T.WARMUP, 1000) - T.LR) < 1e-12
    assert abs(T.lr_at(1000, 1000) - T.LR_MIN) < 1e-12


class Fake(torch.nn.Module):
    """A stand-in model whose answers are a known function of x."""
    def __init__(self, fn, n=20, d=8):
        super().__init__()
        self.E = torch.nn.Parameter(torch.randn(n, d) + 2.0)
        self.dim, self.fn = d, fn

    def answer(self, x, i):
        return self.fn(x)[torch.arange(len(x)), i]


def test_jacobian_measures_on_known_functions():
    toks = torch.arange(10)
    half = Ms.jacobian_measures(Fake(lambda x: 0.5 * x), toks)
    assert abs(half["follow"] - 0.5) < 1e-6 and half["other"] < 1e-6
    assert abs(half["follow_length"] - 0.5) < 1e-6 and abs(half["follow_direction"] - 0.5) < 1e-6
    # direction-only reader a(x) = c x/|x|: J = (c/|x|)(I − x̂x̂ᵀ), so length 0, direction c/|x|
    m = Fake(lambda x: 3.0 * x / x.norm(dim=1, keepdim=True))
    out = Ms.jacobian_measures(m, toks)
    expected = (3.0 / m.E[toks].norm(dim=1)).mean().item()
    assert abs(out["follow_length"]) < 1e-5
    assert abs(out["follow_direction"] - expected) < 1e-5
    shift = Ms.jacobian_measures(Fake(lambda x: x.roll(1, dims=1)), toks)
    assert shift["follow"] == 0.0 and abs(shift["other"] - 1.0) < 1e-6


def test_finite_follow_restores_E():
    m = Fake(lambda x: 0.5 * x)
    E0 = m.E.detach().clone()
    med, ratios = Ms.finite_follow(m, torch.arange(10), 0.1, torch.Generator().manual_seed(0))
    assert abs(med - 0.5) < 1e-5
    assert torch.equal(m.E.detach(), E0)
