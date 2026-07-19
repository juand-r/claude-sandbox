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
- [x] Audit the REAL 2026 eval pipeline (github.com/babylm-org/babylm-eval — note
      the new `babylm-org` org, found via babylm.github.io) against each reported bug.
      Verdicts in `report/` Table 1. Both pipelines cloned to scratch and diffed.
- [x] Build the BLiMP vs (Super)GLUE spread figure (`figure/`) from primary-paper
      data; write the LaTeX report (`report/`) and compile to PDF.
- [x] Write up `analysis.md` (deliverable), `evidence.md` (receipts),
      `rules-2026.md` (reference).
- [x] Commit and push to `claude/babylm-2026-scores-cyhbhz`.
- [~] Pull the raw per-model leaderboard (`BabyLM-community/leaderboard-all-results`,
      the 2025 results) to replace the paper-compiled figure points with exact numbers
      and compute cross-model variance + inter-task correlations. DEFERRED TO USER:
      the authenticated HF MCP tool needs an approval dialog that does not resolve in
      this remote/headless session (errors alternate between "requires approval" and
      "Tool permission stream closed"); the dataset is gated (401 via unauthenticated
      HTTP). User will handle the 2026 leaderboard separately. Would sharpen point
      positions, not change conclusions.

## What the primary-source read changed vs. the first draft
The Findings-only draft said "human-likeness half is low SNR." The papers show it is
worse than that, and pin down mechanisms: EWoK is at chance because 13% of its items'
concepts never appear in training (main.15); AoA is literally miscomputed on 1-5 data
points (main.29); WUG had an eval bug (main.14) and hits exactly 100.00 under morpheme
tokenizers (main.21); BLiMP has a tie-counting inflation artifact (main.16); and a
BROKEN training run beat every real model on the macro aggregate (main.31). The
aggregate ranking itself is not safe — a stronger claim than the draft made.

## Deliverables (all under explorations/babylm2025/)
- `analysis.md` — which 2025 scores are meaningful vs noise/broken (primary-source grounded).
- `evidence.md` — per-paper receipts (quotes + numbers) for all 41 papers.
- `report/babylm_scores_report.{tex,pdf}` — 2026 bug-fix audit + BLiMP/GLUE spread + reference bands.
- `figure/` — the spread figure, its data CSV, and the plotting script.
- `rules-2026.md` — 2026 rules reference.
- `papers/*.txt` — extracted text of all 41 proceedings papers (PDFs gitignored).

## Sources
- Findings of the Third BabyLM Challenge (2025), ACL Anthology 2025.babylm-main.28.
- All 41 papers of Proceedings of the First BabyLM Workshop (2025.babylm-main.1–41).
- 2026 CFP: arXiv 2602.20092 ("BabyLM Turns 4 and Goes Multilingual").
- 2025 eval pipeline: github.com/babylm/evaluation-pipeline-2025.
- 2026 eval pipeline: github.com/babylm-org/babylm-eval (linked from babylm.github.io).
- 2025 leaderboard: HF space BabyLM-community/babylm-leaderboard-2025-all-tasks
  (results dataset: BabyLM-community/leaderboard-all-results, gated).
- 2026 leaderboard: HF space BabyLM-community/BabyLM-Leaderboard-2026.

## Notes / caveats
- The meaningfulness assessment (`analysis.md`) rests on the primary papers plus the
  organizers' figures/tables — NOT on a first-hand variance computation over the raw
  leaderboard (deferred to user; see Steps).
- The figure (`figure/`) uses paper-reported BLiMP/GLUE numbers, each point internally
  consistent from one source, incl. author reproductions; GLUE vs SuperGLUE averaging
  conventions vary slightly. Not the official leaderboard.
- Bug-fix audit outcome (2025 → 2026): BLiMP tie/NaN inflation FIXED; AoA mis-fit FIXED;
  WUG tasks REMOVED; EWoK concept-absence NOT FIXED; reading-time unchanged. Aggregation
  is server-side and could not be confirmed from repo code.
- The 50/30/20 (BLiMP/GLUE/MSGS) weighting seen in some web summaries is from the
  2023 challenge and does NOT apply to 2025. MSGS was not used in 2025.
