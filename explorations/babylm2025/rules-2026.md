# BabyLM 2026 rules (reference)

Source: 2026 Call for Papers, "BabyLM Turns 4 and Goes Multilingual" (arXiv
2602.20092); babylm.github.io. Summarised for our own use — check the CFP before
relying on any detail.

## Tracks
- **Strict** — ≤ 100M words (or up to 1B words if you respect the epoch/exposure cap).
- **Strict-Small** — ≤ 10M words (or up to 100M with the exposure cap).
- **Multilingual** (new) — English, Dutch, Chinese, from BabyBabelLM; 100M tokens
  total, adjusted by each language's Byte Premium (Dutch ×1.0516, Chinese ×0.9894
  relative to English).
- The separate **Interaction** and **Multimodal** tracks from 2025 have been folded
  back into Strict / Strict-Small (teacher feedback and multimodal data are allowed
  within the word budget rather than being their own competitions).
- Plus a non-competition **workshop** paper track.

## Constraints
- Training exposure capped at **≤ 10 epochs** over the data.
- **Intermediate checkpoints** required on HF Hub: every 1M words to 10M, every 10M
  to 100M, every 100M thereafter.
- A detoxified training corpus is provided this year.

## Evaluation
- "Much of the evaluation will continue to be based on **zero-shot probability
  comparisons of two text sequences**" — i.e. BLiMP-style minimal-pair scoring stays
  central. Finetuned (Super)GLUE was kept in 2025 because in-context learning does
  not emerge at this data scale; expect similar in 2026.
- An open-source evaluation pipeline + HF leaderboard is provided. Full task list
  and any **hidden tasks** are released closer to the deadline.
- Baselines: GPT-BERT (prior winner), a SimPO preference-optimization model, and
  GPT-2 Small.

## Why this matters for the 2025 score analysis
The 2026 pipeline inherits the 2025 evaluation philosophy (zero-shot minimal pairs
at the core, finetuned GLUE retained). So the 2025 reliable-vs-noisy split of scores
— see `analysis.md` — is expected to carry over, which is what makes last year's
scores worth dissecting before committing effort this year.
