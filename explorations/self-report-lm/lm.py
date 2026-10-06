"""A small GPT-style language model that can also report its own embedding coordinates.

Embedding table E: rows 0 .. N_TEXT-1 are the text tokens (BPE), then QUERY,
then COORD_0 .. COORD_{DIM-1}. Embeddings are tied: language-model logits are
ln_f(h) @ E[:N_TEXT]ᵀ, so the extra symbols are never predicted.

Self-report question (t, i): the sequence [QUERY, COORD_i, t]. The answer is
number_head(h_last), where h_last is the internal state at t's position (the
last) before the final LayerNorm. t is last on purpose: with pre-LayerNorm the
blocks only see normalized inputs, but the internal state at t's own position
still contains E[t] itself, unnormalized (PLAN.md, design note).
"""
import math

import torch
import torch.nn.functional as F
from torch import nn

N_TEXT = 4096       # text tokens (BPE vocabulary, incl. end-of-story)
DIM = 128
N_LAYERS = 4
N_HEADS = 4
CTX = 128
INIT_STD = 0.02     # GPT-2 initialization


class Block(nn.Module):
    def __init__(self, dim, n_heads):
        super().__init__()
        self.n_heads = n_heads
        self.ln1 = nn.LayerNorm(dim)
        self.qkv = nn.Linear(dim, 3 * dim)
        self.proj = nn.Linear(dim, dim)
        self.ln2 = nn.LayerNorm(dim)
        self.fc1 = nn.Linear(dim, 4 * dim)
        self.fc2 = nn.Linear(4 * dim, dim)

    def forward(self, x):
        B, T, D = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(D, dim=2)
        q, k, v = (a.view(B, T, self.n_heads, D // self.n_heads).transpose(1, 2) for a in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.proj(y.transpose(1, 2).reshape(B, T, D))
        return x + self.fc2(F.gelu(self.fc1(self.ln2(x))))


class SelfReportLM(nn.Module):
    def __init__(self, n_text=N_TEXT, dim=DIM, n_layers=N_LAYERS, n_heads=N_HEADS, ctx=CTX):
        super().__init__()
        self.n_text, self.dim, self.ctx = n_text, dim, ctx
        self.query_id = n_text
        self.E = nn.Parameter(torch.randn(n_text + 1 + dim, dim) * INIT_STD)
        self.P = nn.Parameter(torch.randn(ctx, dim) * INIT_STD)
        self.blocks = nn.ModuleList(Block(dim, n_heads) for _ in range(n_layers))
        self.ln_f = nn.LayerNorm(dim)
        self.number_head = nn.Linear(dim, 1)
        for name, p in self.named_parameters():
            if name.endswith(".weight") and p.dim() == 2:
                std = INIT_STD / math.sqrt(2 * n_layers) if name.endswith(("proj.weight", "fc2.weight")) else INIT_STD
                nn.init.normal_(p, std=std)
            elif name.endswith(".bias") and "ln" not in name:
                nn.init.zeros_(p)

    def coord_id(self, i):
        return self.n_text + 1 + i

    def residual(self, emb):
        """Internal states after the last block, before ln_f. emb: (B, T, dim)."""
        h = emb + self.P[:emb.shape[1]]
        for block in self.blocks:
            h = block(h)
        return h

    def lm_logits(self, ids):
        h = self.residual(self.E[ids])
        return self.ln_f(h) @ self.E[:self.n_text].T

    def answer(self, x, i):
        """Answers to "coordinate i" when the vector at t's position is x (B, dim).
        Used directly for vectors that are not rows of E."""
        B = x.shape[0]
        emb = torch.stack([self.E[self.query_id].expand(B, -1), self.E[self.coord_id(i)], x], dim=1)
        return self.number_head(self.residual(emb)[:, -1]).squeeze(-1)

    def report(self, t, i):
        """The model's answer to "coordinate i of the embedding vector of token t"."""
        return self.answer(self.E[t], i)


def r2(pred, target):
    """1 − SSE / Σ(target − mean target)², one pooled mean."""
    return 1 - ((pred - target) ** 2).sum().item() / ((target - target.mean()) ** 2).sum().item()


def split_tokens(seed, n_text=N_TEXT):
    """(training tokens, held-out tokens): a quarter of the text tokens held out, fixed by the seed."""
    perm = torch.randperm(n_text, generator=torch.Generator().manual_seed(seed))
    n_held_out = n_text // 4
    return perm[n_held_out:].sort().values, perm[:n_held_out].sort().values
