"""Self-report accuracy by token frequency (counts in data/train.bin), for training and
held-out tokens. Usage: python analyze_frequency.py <name>   writes results/frequency_<name>.json"""
import json
import sys

import numpy as np
import torch

import lm
import measure as Ms

BINS = ((0, 100), (100, 10_000), (10_000, 10**12))


def main():
    name = sys.argv[1]
    torch.set_num_threads(1)
    m, s = Ms.load(name)
    tr, ho = lm.split_tokens(s["seed"], s["n_text"])
    counts = np.bincount(np.fromfile(Ms.T.DATA / "train.bin", dtype=np.uint16), minlength=s["n_text"])
    out = []
    with torch.no_grad():
        for set_name, toks in (("train", tr), ("held_out", ho)):
            t = toks.repeat_interleave(m.dim)
            i = torch.arange(m.dim).repeat(len(toks))
            a = torch.cat([m.report(t[k:k + 32768], i[k:k + 32768]) for k in range(0, len(t), 32768)])
            a = a.view(len(toks), m.dim)
            y = m.E[toks]
            err = (a - y).pow(2).sum(1)
            var = (y - y.mean(0)).pow(2).sum(1)        # coordinate means over the whole set
            c = counts[toks.numpy()]
            for lo, hi in BINS:
                sel = torch.from_numpy((c >= lo) & (c < hi))
                if sel.sum() == 0:
                    continue
                out.append({"set": set_name, "count_from": lo, "count_below": hi, "n_tokens": int(sel.sum()),
                            "centred_r2": (1 - err[sel].sum() / var[sel].sum()).item(),
                            "mean_length": y[sel].norm(dim=1).mean().item()})
    (Ms.HERE / "results" / f"frequency_{name}.json").write_text(json.dumps(out, indent=1))
    for r in out:
        print(r)


if __name__ == "__main__":
    main()
