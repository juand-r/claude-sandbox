"""Per-prompt scores for the IFEval test prompts, to pick an example for the cartoon figure.

Reads the untrained Gemma-2-9b-it score files from a rankalign checkout (branch `longform`):
  outputs/scores_basetyp-v6-google_gemma-2-9b-it_ifeval-prompt_N_test_log-odds_tc_*.csv
For the untrained model, `gen_score_typcorr` = log p(y|x) - log p(y), the PMI correction.

Usage: python ifeval_candidates.py /path/to/rankalign [prompt numbers to show pairs for]
"""
import glob
import sys

import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import roc_auc_score

TEST_PROMPTS = range(1, 22)  # prompts 1..21 are test-only in rankalign (prompt_14 has no file)
N_PAIRS = 3


def load(root, n):
    pattern = f"{root}/outputs/scores_basetyp-v6-google_gemma-2-9b-it_ifeval-prompt_{n}_test_log-odds_tc_*.csv"
    files = glob.glob(pattern)
    if not files:
        return None
    d = pd.read_csv(files[0])
    d["y"] = (d.correct == "Yes").astype(int)
    return d


def summary(d):
    auc = lambda col: 100 * roc_auc_score(d.y, d[col])
    rho = lambda col: pearsonr(d[col], d.val_score)[0]
    return (f"raw AUROC {auc('gen_score'):5.1f}  PMI AUROC {auc('gen_score_typcorr'):5.1f}  "
            f"val AUROC {auc('val_score'):5.1f}  rho raw {rho('gen_score'):+.2f}  rho PMI {rho('gen_score_typcorr'):+.2f}")


def pairs(d):
    """Correct answers the raw score ranks low but PMI and validator rank high; wrong answers the reverse."""
    r = {c: d[c].rank(pct=True) for c in ["gen_score", "gen_score_typcorr", "val_score"]}
    story = r["gen_score_typcorr"] + r["val_score"] - r["gen_score"]
    d = d.assign(story=story, raw_pct=r["gen_score"], pmi_pct=r["gen_score_typcorr"], val_pct=r["val_score"])
    best_correct = d[d.y == 1].nlargest(N_PAIRS, "story")
    best_wrong = d[d.y == 0].nsmallest(N_PAIRS, "story")
    return best_correct, best_wrong


def main():
    root = sys.argv[1]
    show = [int(a) for a in sys.argv[2:]]
    for n in TEST_PROMPTS:
        d = load(root, n)
        if d is not None:
            print(f"prompt {n:2d}  {summary(d)}")
    for n in show:
        d = load(root, n)
        print(f"\n=== prompt {n}: {d.prompt[0][:160]!r}")
        for label, rows in zip(["CORRECT", "WRONG"], pairs(d)):
            for _, x in rows.iterrows():
                print(f"  {label} raw pct {x.raw_pct:.2f}  PMI pct {x.pmi_pct:.2f}  val pct {x.val_pct:.2f}")
                print(f"    {x.response[:300]!r}")


if __name__ == "__main__":
    main()
