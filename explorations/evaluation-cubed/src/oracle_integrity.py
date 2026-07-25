"""
Stage 2b: stimulus-integrity checks, following the protocol of arXiv:2607.13707
("The Test Oracle Problem in Synthetic LLM-as-Judge Corpora").

That paper reports a synthetic judge corpus whose generation step failed silently: four
standard robustness checks missed it, and the resulting statistics contained both an
entirely fabricated effect ("disappearance") and a real effect whose magnitude and
sometimes direction were bent ("distortion"). Aggregate statistics cannot tell the two
apart. Their conclusion is that mechanical-perturbation corpora -- like ours -- are
preferable because the corruption step is string-checkable, but that the integrity checks
must be run and reported *before* any aggregate statistic.

So we run them:
  1. mechanical no-op check   -- every corrupted claim must actually differ from the true
                                 one (their positive control caught 30% injected no-ops
                                 this way, at zero cost)
  2. degeneration rates       -- fragments under three words, verbatim copies
  3. word count per condition -- sharp divergence from intent flags trouble
  4. a manual-reading sample  -- 20 items per condition, dumped for a human to actually read

Outputs: results/oracle_integrity.json, results/manual_read_sample.txt
"""

from __future__ import annotations

import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

sys.path.insert(0, HERE)
from build_systems import QUALITY_LEVELS, STYLES, claim_set  # noqa: E402

N_MANUAL = 20
FRAGMENT_WORDS = 3


def norm(s: str) -> str:
    return " ".join(s.lower().split())


def main() -> None:
    items = json.load(open(os.path.join(DATA, "items.json")))
    answers = json.load(open(os.path.join(DATA, "answers.json")))
    out: dict = {}

    # ---- 1. mechanical no-op check on the corruption step --------------------
    n_pairs, n_noop, n_identical_norm = 0, 0, 0
    for it in items:
        for c in it["claims"]:
            n_pairs += 1
            if c["true"] == c["false"]:
                n_noop += 1
            if norm(c["true"]) == norm(c["false"]):
                n_identical_norm += 1
    out["noop_check"] = {"claim_pairs": n_pairs, "exact_noops": n_noop,
                         "normalised_noops": n_identical_norm,
                         "noop_rate": n_noop / n_pairs}
    print(f"1. no-op check: {n_noop}/{n_pairs} corrupted claims identical to the true claim "
          f"({n_noop / n_pairs:.4f}); normalised {n_identical_norm}")

    # A no-op at the *rendering* step would be an answer at k>0 that still conveys only
    # true claims. The claim-level entailment check already measures this; surface it.
    bad_k = [r for r in answers if r["k"] > 0 and r["verified_false"] == 0]
    out["noop_check"]["render_level_noops"] = len(bad_k)
    print(f"   rendering-level no-ops (k>0 but no false claim detected): "
          f"{len(bad_k)}/{sum(1 for r in answers if r['k'] > 0)}")

    # ---- 2. degeneration rates ----------------------------------------------
    print("\n2. degeneration rates and 3. word counts, per condition:")
    per_cond = {}
    print(f"   {'condition':<18} {'n':>4} {'mean_w':>7} {'min_w':>6} {'frag':>6} "
          f"{'copy':>6} {'fidel':>6}")
    for st in STYLES:
        for k in QUALITY_LEVELS:
            sub = [r for r in answers if r["style"] == st and r["k"] == k]
            words = [r["n_words"] for r in sub]
            frag = sum(1 for w in words if w < FRAGMENT_WORDS)
            copies = 0
            for r in sub:
                a = norm(r["answer"])
                if a == norm(r["question"]):
                    copies += 1
                    continue
                # verbatim copy of the statement list would mean the renderer did nothing
                it = next(x for x in items if x["id"] == r["item_id"])
                stmts, _ = claim_set(it, r["k"])
                if a == norm(" ".join(stmts)):
                    copies += 1
            fid = sum(r["render_faithful"] for r in sub) / (6 * len(sub))
            key = f"{st}/k{k}"
            per_cond[key] = {"n": len(sub), "mean_words": sum(words) / len(words),
                             "min_words": min(words), "fragments": frag,
                             "verbatim_copies": copies, "claim_fidelity": fid}
            print(f"   {key:<18} {len(sub):>4} {sum(words)/len(words):>7.1f} {min(words):>6} "
                  f"{frag:>6} {copies:>6} {fid:>6.3f}")
    out["per_condition"] = per_cond

    tot = len(answers)
    out["degeneration"] = {
        "total": tot,
        "fragments": sum(c["fragments"] for c in per_cond.values()),
        "verbatim_copies": sum(c["verbatim_copies"] for c in per_cond.values()),
    }

    # ---- 4. manual reading sample -------------------------------------------
    rng = random.Random(0)
    lines = []
    for st in STYLES:
        for k in QUALITY_LEVELS:
            sub = [r for r in answers if r["style"] == st and r["k"] == k]
            for r in rng.sample(sub, min(N_MANUAL // len(QUALITY_LEVELS) + 2, len(sub))):
                it = next(x for x in items if x["id"] == r["item_id"])
                stmts, bad = claim_set(it, r["k"])
                lines.append(f"===== {st} / k={k} / {r['item_id']} "
                             f"({r['n_words']}w, fidelity {r['render_faithful']}/6) =====")
                lines.append(f"Q: {r['question']}")
                lines.append("INTENDED STATEMENTS:")
                for s, b in zip(stmts, bad):
                    lines.append(f"  [{'FALSE' if b else 'true '}] {s}")
                lines.append("ANSWER:")
                lines.append(r["answer"])
                lines.append("")
    path = os.path.join(RESULTS, "manual_read_sample.txt")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"\n4. wrote manual-reading sample ({len(lines)} lines) -> {path}")

    with open(os.path.join(RESULTS, "oracle_integrity.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
