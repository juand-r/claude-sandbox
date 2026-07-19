# Plan: Which BabyLM 2025 scores are meaningful?

Goal: for a last-minute BabyLM 2026 entry, figure out which of the many scores
reported in the 2025 (3rd) BabyLM Challenge are actually meaningful — i.e.
reliable, discriminative between models, and not saturated or stuck at chance —
so we know what to optimize and what to ignore.

Note on location: repo convention (CLAUDE.md) puts explorations under
`/explorations/`, so this lives in `explorations/babylm2025/`. The user asked for
a `babylm2025/` subdirectory; this satisfies both.

## Steps
- [x] Look up the 2026 rules (tracks, budgets, evaluation philosophy).
- [x] Recover the 2025 evaluation design: full task list, per-task metric,
      exact aggregation formula.
- [x] Recover the 2025 results (Table 3 of the Findings paper) and the
      organizers' own observations on score variance / discriminability.
- [x] Download and read ALL 41 proceedings papers (2025.babylm-main) from the ACL
      Anthology — not just the Findings summary. Extracted text under `papers/`;
      per-paper reliability receipts in `evidence.md` (five parallel readers).
- [x] Assess each task's meaningfulness (reliable / noisy / at-chance / broken),
      grounded in the primary papers. Rewrote `analysis.md` around this evidence.
- [ ] (Next step, blocked on approval) Pull the raw per-model per-subtask leaderboard
      from the HF dataset `BabyLM-community/leaderboard-all-results` to compute
      cross-model variance per task and the inter-task correlation matrix directly.
      Blocked: the authenticated Hugging Face tool returns "requires approval" and
      isn't being granted in this environment; the dataset is gated (401 via HTTP).
- [x] Write up `analysis.md` (deliverable), `evidence.md` (receipts),
      `rules-2026.md` (reference).
- [x] Commit and push to `claude/babylm-2026-scores-cyhbhz`.

## What the primary-source read changed vs. the first draft
The Findings-only draft said "human-likeness half is low SNR." The papers show it is
worse than that, and pin down mechanisms: EWoK is at chance because 13% of its items'
concepts never appear in training (main.15); AoA is literally miscomputed on 1-5 data
points (main.29); WUG had an eval bug (main.14) and hits exactly 100.00 under morpheme
tokenizers (main.21); BLiMP has a tie-counting inflation artifact (main.16); and a
BROKEN training run beat every real model on the macro aggregate (main.31). The
aggregate ranking itself is not safe — a stronger claim than the draft made.

## Sources
- Findings of the Third BabyLM Challenge (2025), ACL Anthology 2025.babylm-main.28.
- 2026 CFP: arXiv 2602.20092 ("BabyLM Turns 4 and Goes Multilingual").
- Evaluation pipeline: github.com/babylm/evaluation-pipeline-2025.
- Leaderboard: HF space BabyLM-community/babylm-leaderboard-2025-all-tasks.

## Notes / caveats
- The meaningfulness assessment rests on the organizers' Figure 5 (training-dynamics
  variance), Figure 4 (per-task ranges), and Table 3 (real scores) — NOT on a
  first-hand variance computation over the raw leaderboard. That reanalysis is the
  natural next step once the HF connection is back.
- The 50/30/20 (BLiMP/GLUE/MSGS) weighting seen in some web summaries is from the
  2023 challenge and does NOT apply to 2025. MSGS was not used in 2025.
