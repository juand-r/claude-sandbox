"""A faster subset of measure.py, for comparing variants during stage 1 (PLAN.md).

- validation loss on 20 × 32 fixed windows (the training-log windows of train.py);
- centred R² over all asked-about and all never-asked tokens;
- follow, other movement and the gain along E[t] (norm direction) on N_TOKENS random
  asked-about and N_TOKENS random never-asked tokens (the same tokens every time).
"""
import numpy as np
import torch

import lm
import measure as Ms
import train as T

N_TOKENS = 128
_valid = None


def valid_batches():
    global _valid
    if _valid is None:
        data = T.load_tokens("valid")
        vgen = torch.Generator().manual_seed(1234)
        _valid = [T.lm_batch(data, T.LM_BATCH, vgen) for _ in range(T.EVAL_LM_BATCHES)]
    return _valid


@torch.no_grad()
def quick_measure(m, seed):
    tr, ho = lm.split_tokens(seed, m.n_text)
    out = {"valid_loss": float(np.mean([T.lm_loss(m, x, y).item() for x, y in valid_batches()]))}
    gen = torch.Generator().manual_seed(4242)
    for name, toks in (("asked", tr), ("never", ho)):
        _, out[f"r2c_{name}"], _ = Ms.r2_set(m, toks)
        sample = toks[torch.randperm(len(toks), generator=gen)[:N_TOKENS]]
        j = Ms.jacobian_measures(m, sample)
        out[f"follow_{name}"], out[f"other_{name}"], out[f"length_{name}"] = j["follow"], j["other"], j["follow_length"]
    return out


def fmt(r):
    return (f"valid {r['valid_loss']:.3f}  R²c {r['r2c_asked']:.3f}/{r['r2c_never']:.3f}  "
            f"follow {r['follow_asked']:.3f}/{r['follow_never']:.3f}  other {r['other_asked']:.3f}/{r['other_never']:.3f}  "
            f"length {r['length_asked']:.3f}/{r['length_never']:.3f}")
