"""Mean norm of the token embedding vectors by token frequency (counts in the training text),
for asked-about and never-asked tokens of a given split. Writes results/norms_by_frequency.json.
Usage: python norms_by_frequency.py"""
import json

import numpy as np
import torch

import lm
import measure as Ms

RUNS = (("lmonly_s0", 0), ("joint_s0", 0), ("joint_s1", 1), ("joint_detached_s0", 0))
BINS = ((0, 100), (100, 10_000), (10_000, 10**12))


def main():
    counts = np.bincount(np.fromfile(Ms.T.DATA / "train.bin", dtype=np.uint16), minlength=lm.N_TEXT)
    out = {}
    for name, split_seed in RUNS:
        m, _ = Ms.load(name)
        L = m.E[:lm.N_TEXT].detach().norm(dim=1).numpy()
        tr, ho = lm.split_tokens(split_seed)
        out[name] = {"split_seed": split_seed}
        for set_name, toks in (("asked_about", tr.numpy()), ("never_asked", ho.numpy())):
            c = counts[toks]
            out[name][set_name] = [{"count_from": lo, "count_below": hi, "n_tokens": int(((c >= lo) & (c < hi)).sum()),
                                    "mean_norm": float(L[toks][(c >= lo) & (c < hi)].mean())} for lo, hi in BINS]
    (Ms.HERE / "results" / "norms_by_frequency.json").write_text(json.dumps(out, indent=1))
    for n, d in out.items():
        print(n, {k: [round(b["mean_norm"], 2) for b in v] for k, v in d.items() if k != "split_seed"})


if __name__ == "__main__":
    torch.set_num_threads(2)
    main()
