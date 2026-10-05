import torch

import canaries as C
import follow_test as F
import model as M
import train as T


def test_position_0_is_the_embedding_row_and_ignores_position_1():
    torch.manual_seed(0)
    m = M.SelfReporter()
    t = torch.tensor([3, 3, 7])
    i = torch.tensor([0, 5, 5])
    states = m.states(m.E[t], i)
    assert torch.equal(states[0][:, 0], m.E[t])          # the input really is the embedding row
    assert torch.equal(states[0][:, 1], m.E_idx[i])
    # causal attention: position 0's state never depends on the index token
    for h in states[1:]:
        torch.testing.assert_close(h[0, 0], h[1, 0])


def test_answer_depends_on_index_token():
    torch.manual_seed(0)
    m = M.SelfReporter()
    a = m(torch.tensor([3, 3]), torch.tensor([0, 5]))
    assert a[0] != a[1]


def test_perfect_reader_is_exact_for_rows_and_new_vectors():
    torch.manual_seed(1)
    E = torch.randn(M.N_TOKENS, M.DIM)
    m = C.perfect_reader(E)
    t, i = M.all_pairs(torch.arange(M.N_TOKENS))
    torch.testing.assert_close(m(t, i), E[t, i], atol=1e-5, rtol=0)
    x = 3 * torch.randn(300, M.DIM)             # the construction is exact while every |x_j| < 15
    assert x.abs().max() < 15
    j = torch.randint(0, M.DIM, (300,))
    torch.testing.assert_close(m.answer(x, j), x[torch.arange(300), j], atol=1e-5, rtol=0)


def test_canaries_reproduce_known_results():
    F.check_canaries(seed=0)
    F.check_canaries(seed=1)


def test_loss_is_one_minus_r2_of_the_batch():
    a, y = torch.randn(64), torch.randn(64)
    assert abs(T.loss_fn(a, y).item() - (1 - M.r2(a, y))) < 1e-5


def test_split_is_disjoint_and_complete():
    tr, ho = M.split_tokens(3)
    assert len(ho) == M.N_HELD_OUT
    assert sorted(tr.tolist() + ho.tolist()) == list(range(M.N_TOKENS))


def test_fixed_condition_leaves_E_untouched_and_trained_moves_only_training_rows():
    torch.manual_seed(5)
    E0 = M.SelfReporter().E.detach().clone()          # same seed -> same initial E as in train()
    m, _, _ = T.train("fixed", 5, epochs=2, verbose=False)
    assert torch.equal(m.E.detach(), E0)
    m, _, _ = T.train("trained", 5, epochs=2, verbose=False)
    tr, ho = M.split_tokens(5)
    assert torch.equal(m.E.detach()[ho], E0[ho])
    assert not torch.equal(m.E.detach()[tr], E0[tr])


def test_follow_measures_a_hand_made_partial_follower():
    """A model whose answer is 0.5 · x_i must give follow ratio 0.5 and no other movement."""
    class Half(torch.nn.Module):
        def __init__(self, E):
            super().__init__()
            self.E = torch.nn.Parameter(E.clone())

        def answer(self, x, i):
            return 0.5 * x[torch.arange(len(x)), i]

        def forward(self, t, i):
            return self.answer(self.E[t], i)

    torch.manual_seed(2)
    m = Half(torch.randn(M.N_TOKENS, M.DIM))
    out = F.follow(m, torch.arange(10), 0.3, torch.Generator().manual_seed(0))
    assert abs(out["follow_ratio_mean"] - 0.5) < 1e-5
    assert out["other_movement_mean"] < 1e-5
    local = F.local_follow(m, torch.arange(10))
    assert abs(local["local_follow_mean"] - 0.5) < 1e-6
    assert local["local_other_mean"] < 1e-6


def test_local_follow_sees_off_diagonal_movement():
    """Answers a(x) = P x with P a permutation (no fixed points): trace 0, and
    |P − 0·I|_F / √d = 1."""
    class Shift(torch.nn.Module):
        def __init__(self, E):
            super().__init__()
            self.E = torch.nn.Parameter(E.clone())

        def answer(self, x, i):
            return x[torch.arange(len(x)), (i + 1) % x.shape[1]]

        def forward(self, t, i):
            return self.answer(self.E[t], i)

    m = Shift(torch.randn(M.N_TOKENS, M.DIM))
    local = F.local_follow(m, torch.arange(5))
    assert local["local_follow_mean"] == 0.0
    assert abs(local["local_other_mean"] - 1.0) < 1e-6


def test_no_gradient_flows_through_the_target():
    """The gradient into E must equal the gradient with the target replaced by a constant."""
    torch.manual_seed(0)
    m = M.SelfReporter()
    t, i = torch.tensor([1, 2, 3, 4]), torch.tensor([0, 1, 2, 3])
    T.batch_loss(m, t, i).backward()
    g_train = m.E.grad.clone()
    m.E.grad = None
    const = m.E[t, i].detach().clone()
    T.loss_fn(m(t, i), const).backward()
    torch.testing.assert_close(g_train, m.E.grad)
    # and the target path, had it been allowed, would change the gradient
    m.E.grad = None
    T.loss_fn(m(t, i), m.E[t, i]).backward()
    assert not torch.allclose(g_train, m.E.grad)


def test_training_learns_the_training_tokens():
    for condition in T.CONDITIONS:
        _, _, log = T.train(condition, 0, epochs=40, log_every=40, verbose=False)
        assert log[-1]["r2_train"] > 0.9, (condition, log[-1])


def test_save_and_load_round_trip(tmp_path):
    m, s, _ = T.train("trained", 0, epochs=1, verbose=False)
    torch.save({"state_dict": m.state_dict(), "settings": s}, tmp_path / "x.pt")
    m2, s2 = T.load(tmp_path / "x.pt")
    t, i = M.all_pairs(torch.arange(M.N_TOKENS))
    with torch.no_grad():
        assert torch.equal(m(t, i), m2(t, i))
    assert s2 == s


def test_vocabulary_size_setting():
    assert T.epochs_for(64) == T.EPOCHS                       # the original runs are unchanged
    for V in (256, 1024, 4096):
        steps = T.epochs_for(V) * -(-(V - V // 4) * M.DIM // T.BATCH)
        assert abs(steps - T.TOTAL_STEPS) / T.TOTAL_STEPS < 0.01, (V, steps)
    assert T.run_name("fixed", 0, 64, T.EPOCHS) == "fixed_seed0"
    assert T.run_name("trained", 2, 1024, T.epochs_for(1024)) == "trained_V1024_seed2"
    assert F.RUN_NAME.match("trained_V1024_seed2") and F.RUN_NAME.match("fixed_seed0")
    assert not F.RUN_NAME.match("fixed_V256_seed0_3ep")


def test_larger_vocabulary_split_and_training():
    torch.manual_seed(7)
    E0 = M.SelfReporter(n_tokens=256).E.detach().clone()
    m, s, log = T.train("trained", 7, epochs=1, verbose=False, n_tokens=256)
    tr, ho = M.split_tokens(7, 256, 64)
    assert s["n_tokens"] == 256 and s["n_held_out"] == 64 and m.E.shape == (256, M.DIM)
    assert len(set(tr.tolist()) & set(ho.tolist())) == 0 and len(tr) + len(ho) == 256
    assert torch.equal(m.E.detach()[ho], E0[ho])              # held-out embedding vectors untouched
    assert not torch.equal(m.E.detach()[tr], E0[tr])
