# babylm2025

Working out which scores from the 2025 (3rd) BabyLM Challenge are actually
meaningful — reliable, discriminative, not saturated or at chance — so we know what
to optimize for a 2026 entry.

## Files
- `analysis.md` — the main write-up: what each 2025 score measures, how the
  aggregate is built, and which numbers carry signal vs. noise. **Start here.**
- `rules-2026.md` — reference summary of the 2026 challenge rules (tracks, budgets,
  evaluation philosophy).
- `PLAN.md` — plan, progress, and caveats.

## One-line takeaway
Track **BLiMP** (then GLUE); discount **EWoK** and the whole **human-likeness**
half — the flagship `Macro Average` gives that noisy half a full 50% weight. See
`analysis.md`.

## Open next step
A first-hand reanalysis over the raw per-model leaderboard
(`BabyLM-community/leaderboard-all-results` on HF) — cross-model variance per task
and the inter-task correlation matrix — would turn the argument into a measurement.
It is currently blocked only by the Hugging Face MCP tool needing interactive
approval.
