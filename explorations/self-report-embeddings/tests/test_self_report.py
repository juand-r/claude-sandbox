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
    assert torch.equal(states[0][:, 0], m.E[t])
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


def test_save_and_load_round_trip(tmp_path):
    m, s, _ = T.train("trained", 0, epochs=1, verbose=False)
    torch.save({"state_dict": m.state_dict(), "settings": s}, tmp_path / "x.pt")
    m2, s2 = T.load(tmp_path / "x.pt")
    t, i = M.all_pairs(torch.arange(M.N_TOKENS))
    with torch.no_grad():
        assert torch.equal(m(t, i), m2(t, i))
    assert s2 == s
