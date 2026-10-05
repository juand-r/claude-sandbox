"""Two hand-built models whose measurement results are known in advance.

They are run through exactly the same measurement code as the trained models
(`follow_test.measure`). If the code reports anything other than the expected
values for them, the code is wrong.

- perfect_reader: a SelfReporter with hand-set weights that reads its embedding
  exactly. Expected: R² 1 on every token set, follow ratio 1, other movement 0.
- Memorizer: stores its answers for the training tokens and, for any content
  vector, returns the stored answers of the nearest training row. It depends on
  E[t] only through which training row is nearest. Expected: R² 1 on training
  tokens; R² near 0 on held-out and brand-new tokens (measured: −0.09 for one
  split; the nearest row is chosen for being close, so it is weakly correlated
  with the new row, which lifts R² above the −1 of an unrelated row); follow
  ratio 0 for changes too small to change the nearest row.
"""
import torch
from torch import nn

import model as M


@torch.no_grad()
def perfect_reader(E, big=10.0, n_layers=M.N_LAYERS, n_heads=M.N_HEADS, mlp_width=M.MLP_WIDTH):
    """A SelfReporter, with embedding table E, whose answer is exactly x_i
    whenever every |x_j| < 1.5 · big.

    Layer 1, attention. Query weights are zero, so every score is 0 and position
    1 gives weight 1/2 to each position. Value and output maps are the identity.
    With E_idx[i] = big · e_i, position 1 becomes
        z = big·e_i + (x + big·e_i)/2 = x/2 + 1.5·big·e_i.
    Layer 1, MLP (3·dim of the units, the rest unused). For each coordinate j:
        a_j = relu(z_j), b_j = relu(−z_j)     (a_j − b_j = z_j)
        c_j = relu(z_j − 0.75·big)            (active only for j = i)
    The output writes −(a_j − b_j) into coordinate j, which cancels z, and adds
    every c_j into coordinate 0. Afterwards position 1 holds s·e_0 with
        s = c_i = x_i/2 + 0.75·big.
    (For j ≠ i, z_j − 0.75·big = x_j/2 − 0.75·big < 0; for j = i it is
    x_i/2 + 0.75·big > 0.)
    Layer 2 adds nothing (all its weights and biases zero).
    Readout: answer = 2·h_0 − 1.5·big = x_i.
    """
    dim = E.shape[1]
    if mlp_width < 3 * dim:
        raise ValueError(f"needs mlp_width >= {3 * dim}")
    m = M.SelfReporter(n_tokens=E.shape[0], dim=dim, n_layers=n_layers, n_heads=n_heads, mlp_width=mlp_width)
    for p in m.parameters():
        p.zero_()
    m.E.copy_(E)
    m.E_idx.copy_(big * torch.eye(dim))
    eye = torch.eye(dim)

    b1 = m.blocks[0]
    b1.attn.qkv.weight[2 * dim:] = eye          # value = identity; query and key stay zero
    b1.attn.out.weight.copy_(eye)
    W1, bias1, W2 = b1.fc1.weight, b1.fc1.bias, b1.fc2.weight
    W1[:dim] = eye                               # a_j = relu(z_j)
    W1[dim:2 * dim] = -eye                       # b_j = relu(-z_j)
    W1[2 * dim:3 * dim] = eye                    # c_j = relu(z_j - 0.75 big)
    bias1[2 * dim:3 * dim] = -0.75 * big
    W2[:, :dim] = -eye                           # write -a_j into coordinate j
    W2[:, dim:2 * dim] = eye                     # write +b_j into coordinate j
    W2[0, 2 * dim:3 * dim] = 1.0                 # add every c_j into coordinate 0

    m.readout.weight[0, 0] = 2.0
    m.readout.bias[0] = -1.5 * big
    return m


class Memorizer(nn.Module):
    """Answers with the stored values of the nearest stored training row."""

    def __init__(self, E, train_tokens):
        super().__init__()
        self.E = nn.Parameter(E.clone())
        self.register_buffer("stored", E[train_tokens].clone())

    def answer(self, x, i):
        nearest = torch.cdist(x, self.stored).argmin(dim=1)
        return self.stored[nearest, i]

    def forward(self, t, i):
        return self.answer(self.E[t], i)
