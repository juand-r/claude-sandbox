# Lab notes

## 2026-10-06: setup

Data: TinyStories from Hugging Face (roneneldan/TinyStories), downloaded with curl:
data/train-00000-of-00004-2d5a1467fff1081b.parquet (529,930 stories) and
data/validation-00000-of-00001-869c898b519ad725.parquet (21,990 stories),
saved as data/train0.parquet and data/valid.parquet (not committed; data/ is ignored).

Design note found while planning: with pre-LayerNorm the blocks see only
normalized inputs, so the question is laid out [QUERY, COORD_i, t] and the
answer is read at t's position (PLAN.md). Earlier I told the user that reading
before the final norm makes exact reading possible; that was too strong.

Timing: about 1.1 s per training step with 2 threads (measured while another
process was running), so two runs in parallel with 2 threads each.

Mistake: prepare.py first encoded all 530k stories in one batch; it reached 14
GB and was killed by the kernel (out of memory). Fixed by encoding in chunks of
10,000 stories; the tokenizer it had already saved is reused.
