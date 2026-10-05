"""A small transformer asked about its own embedding weights.

Input: two tokens [t, i]. t is a content token (one of N_TOKENS); i is an index
token meaning "coordinate i" (one of DIM). The model outputs one number, which
should equal E[t, i], coordinate i of the embedding row of t.

Design choices (see PLAN.md):
- No positional embeddings: content and index tokens come from separate tables,
  so the model can tell them apart. The internal state at position 0 is then
  exactly E[t].
- No LayerNorm: it divides the internal state by its size, which would prevent
  an answer from following a change in the size of E[t].
- The model width equals the embedding size, DIM.

An exact reader exists in this architecture (`canaries.perfect_reader`), so a
trained model that fails to read cannot blame the architecture.
"""
import math

import torch
import torch.nn.functional as F
from torch import nn

N_TOKENS = 64           # content tokens: the ones asked about
DIM = 32                # embedding size = model width = number of index tokens
N_LAYERS = 2
N_HEADS = 4
MLP_WIDTH = 128
N_HELD_OUT = 16         # content tokens never asked about in training


class Attention(nn.Module):
    """Multi-head causal self-attention with biases."""

    def __init__(self, dim, n_heads):
        super().__init__()
        if dim % n_heads:
            raise ValueError(f"dim {dim} not divisible by n_heads {n_heads}")
        self.n_heads, self.head_dim = n_heads, dim // n_heads
        self.qkv = nn.Linear(dim, 3 * dim)
        self.out = nn.Linear(dim, dim)

    def forward(self, x):
        B, T, D = x.shape
        q, k, v = self.qkv(x).split(D, dim=2)
        q, k, v = (a.view(B, T, self.n_heads, self.head_dim).transpose(1, 2) for a in (q, k, v))
        scores = q @ k.transpose(2, 3) / math.sqrt(self.head_dim)            # (B, heads, T, T)
        causal = torch.ones(T, T, dtype=torch.bool, device=x.device).tril()
        scores = scores.masked_fill(~causal, float("-inf"))
        y = scores.softmax(dim=-1) @ v                                       # (B, heads, T, head_dim)
        return self.out(y.transpose(1, 2).reshape(B, T, D))


class Block(nn.Module):
    def __init__(self, dim, n_heads, mlp_width):
        super().__init__()
        self.attn = Attention(dim, n_heads)
        self.fc1 = nn.Linear(dim, mlp_width)
        self.fc2 = nn.Linear(mlp_width, dim)

    def forward(self, x):
        x = x + self.attn(x)
        return x + self.fc2(F.relu(self.fc1(x)))


class SelfReporter(nn.Module):
    """E: embedding table of the content tokens (the weights asked about).
    E_idx: embedding table of the index tokens."""

    def __init__(self, n_tokens=N_TOKENS, dim=DIM, n_layers=N_LAYERS, n_heads=N_HEADS, mlp_width=MLP_WIDTH):
        super().__init__()
        self.E = nn.Parameter(torch.randn(n_tokens, dim))
        self.E_idx = nn.Parameter(torch.randn(dim, dim))
        self.blocks = nn.ModuleList(Block(dim, n_heads, mlp_width) for _ in range(n_layers))
        self.readout = nn.Linear(dim, 1)

    def states(self, x, i):
        """Internal states after each block, given content vectors x (B, dim)
        and index tokens i (B,). Element 0 is the input."""
        h = torch.stack([x, self.E_idx[i]], dim=1)                           # (B, 2, dim)
        out = [h]
        for block in self.blocks:
            h = block(h)
            out.append(h)
        return out

    def answer(self, x, i):
        """The model's answer for content vector x and coordinate i. Used directly
        for content vectors that are not rows of E (brand-new tokens)."""
        return self.readout(self.states(x, i)[-1][:, 1]).squeeze(1)

    def forward(self, t, i):
        """The model's answer to "coordinate i of your embedding of token t"."""
        return self.answer(self.E[t], i)


def split_tokens(seed, n_tokens=N_TOKENS, n_held_out=N_HELD_OUT):
    """(training tokens, held-out tokens), a random split fixed by the seed."""
    perm = torch.randperm(n_tokens, generator=torch.Generator().manual_seed(seed))
    return perm[n_held_out:].sort().values, perm[:n_held_out].sort().values


def all_pairs(tokens, dim=DIM):
    """Every (t, i) with t in tokens and i in 0..dim-1, as two flat tensors."""
    t = tokens.repeat_interleave(dim)
    i = torch.arange(dim).repeat(len(tokens))
    return t, i


def r2(pred, target):
    """1 − SSE / Σ(target − mean target)²."""
    return 1 - ((pred - target) ** 2).sum().item() / ((target - target.mean()) ** 2).sum().item()
