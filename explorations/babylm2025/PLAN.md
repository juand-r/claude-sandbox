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
- [x] Assess each task's meaningfulness (reliable / noisy / at-chance / saturated).
- [ ] (Next step, blocked) Pull the raw per-model per-subtask leaderboard from
      the HF space `BabyLM-community/babylm-leaderboard-2025-all-tasks` to compute
      cross-model variance per task and inter-task correlations directly.
      Blocked because the Hugging Face MCP server disconnected mid-session.
- [x] Write up `analysis.md` (the deliverable) and `rules-2026.md` (reference).
- [x] Commit and push to `claude/babylm-2026-scores-cyhbhz`.

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
