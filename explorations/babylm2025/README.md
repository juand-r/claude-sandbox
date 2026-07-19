# babylm2025

Working out which scores from the 2025 (3rd) BabyLM Challenge are actually
meaningful — reliable, discriminative, not saturated or at chance — so we know what
to optimize for a 2026 entry.

## Files
- `report/babylm_scores_report.pdf` — compiled LaTeX report: which 2025 eval bugs
  the **2026** pipeline fixed (audited against `babylm-org/babylm-eval` source), plus
  a figure of the **BLiMP vs (Super)GLUE spread** across systems and reference bands
  for judging a score. Source: `report/babylm_scores_report.tex`; figure:
  `figure/make_figure.py` (+ `blimp_glue_data.csv`).
- `analysis.md` — the main write-up: what each 2025 score measures, how the
  aggregate is built, and which numbers carry signal vs. noise. **Start here.**
- `evidence.md` — per-paper receipts (quotes + numbers) backing every claim in
  `analysis.md`, across all 41 proceedings papers.
- `rules-2026.md` — reference summary of the 2026 challenge rules (tracks, budgets,
  evaluation philosophy).
- `papers/` — extracted text of all 41 `2025.babylm-main` papers (PDFs gitignored).
- `PLAN.md` — plan, progress, and caveats.

## One-line takeaway
Trust **BLiMP** (read coarsely) and **(Super)GLUE**; treat everything else as
compromised — **EWoK is at chance**, the **human-likeness half is at the noise floor
or buggy** (AoA is literally miscomputed), and the flagship `Macro Average` is
unsafe: a *broken training run* beat every real model on it. Grounded in the winners'
own papers. See `analysis.md`.

## Open next step
A first-hand reanalysis over the raw per-model leaderboard
(`BabyLM-community/leaderboard-all-results` on HF) — cross-model variance per task
and the inter-task correlation matrix — would turn the argument into a measurement.
It is currently blocked only by the Hugging Face MCP tool needing interactive
approval.
