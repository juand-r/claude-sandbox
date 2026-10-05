# Lab notes

## 2026-10-05: implementation and code review

Implemented `model.py`, `train.py`, `follow_test.py`, `canaries.py`, tests.

My own mistakes, caught before review:
- First draft of the perfect-reader construction ignored that the residual
  stream already holds x/2 at position 1, so a linear readout would see all of
  x. Fixed: the MLP cancels the residual (2·d units) and adds the selected
  coordinate (d units), 96 units in all.
- I claimed the memorizer canary would score R² ≈ −1 on held-out tokens. It
  scores about −0.09: the nearest stored row is chosen for being close, so it is
  weakly correlated with the new row.

Independent review (a subagent, read-only; scratch scripts in the session
scratchpad). No bug found in the model, training loop or the arithmetic.
Findings and what I did:

1. The mean follow ratio is dominated by rare jumps: the nearest-row memorizer
   scores 0.35-0.6 on held-out tokens at 10% changes, median 0. Done: added the
   exact local measure (Jacobian from autograd: trace/d and the size of the rest),
   the median, the jump fraction, and 1% changes. Canary checks now cover the
   memorizer's held-out results. I also found that at 100% changes the
   memorizer's held-out median is 0.26 (a large change lands near another stored
   row along δ), so 100% changes are not evidence of reading on their own.
2. "R² after change" hardly measured following (memorizer 0.99 at 10%).
   Replaced by R² of the change (Δanswers against δ).
3. The driver would have measured trial runs and rebuilt baselines from module
   defaults. Fixed: main runs only (name pattern), baseline from saved settings,
   once per seed.
4. Test gaps. Added: no gradient through the target (fails if `.detach()` is
   removed), training learns (R² > 0.9 in 40 epochs), local follow on hand-made
   models (half-reader, coordinate shift), position 1's input is E_idx[i].
   12 tests pass.
5. In this architecture held-out rows are just new inputs, so held-out R² and
   brand-new R² measure the same thing in the fixed condition. In the trained
   condition the training rows drift and held-out rows stay at initialization.
   To be stated in the write-up.
6. Pooled R² includes the per-coordinate means. Added a centred R².
7. Comment on gradient flow was misleading: in the trained condition E still
   gets a gradient through its role as the input. Comment fixed; E's RMS logged.
8. PLAN.md out of date with the code. Updated.

Quick numbers seen during development (seed 0, not the experiment): after 40
epochs, R² 0.94 on training tokens, 0.32-0.34 on held-out tokens, both
conditions. The reviewer's 200-epoch runs: training R² 1.0, held-out 0.34-0.39.

## 2026-10-05: first runs

`run_all.sh`: 2 conditions x 3 seeds, 3,000 epochs, about 230 s each, four in
parallel; then `follow_test.py`. No failures. Results in REPORT.md. Held-out R²
levels off by about epoch 500 (seed 0 fixed: 0.49; seed 1 fixed: 0.39-0.41) and
does not decline later.

## 2026-10-05: terminology review of REPORT.md

The user could not follow "row" and asked for a full review of terms. I
rewrote the report with a Terms section, then a separate Claude instance read
it cold. Its findings, all verified and fixed:
- Wrong number of mine: the quine sentence in the introduction mixed two
  measurements. Now cites a saved file
  (`../neural-network-quine/diag_own_influence.py` and its output; median size
  of a hidden weight's derivative of its own output 0.010 on the R² 0.9975
  network).
- Understated claim of mine: "the embedding table changed little". With trained
  embeddings, training tokens' embedding vectors moved by a median of 19-21% of
  their length (cosine to the start ≥ 0.925); held-out ones did not move.
- "Half as much" and "other movement 0.65" held only for held-out tokens; now
  both sets are reported.
- Finite-change follow at 100% on held-out tokens (0.38-0.42) is below follow;
  the claim that finite changes agree is now limited to changes up to 10%.
- One rounding error (0.66 for 0.6548).
- The 30-epoch trial numbers were not saved; now in
  `results/trial_30ep_seed0_follow_test.json`.
- Terms used two ways ("trained", "size", "change") and undefined terms
  (internal state, position, run, pass, length) fixed.

## 2026-10-05: vocabulary sweep (V = 256, 1024, 4096)

Second review (separate Claude instance) of the vocabulary change: no bugs; V = 64
runs reproduce bit for bit. Added its suggested guard: the measurement driver
raises if a stored measurement's settings differ from the saved run's.
Caveats it raised, for the write-up: equal steps means fewer passes per token
at larger V (3000, 750, 188, 47 epochs), so in the trained condition each
embedding vector gets far fewer updates; the centred R² uses a per-coordinate
mean over very different numbers of tokens across V.

Mistake of mine: `pkill -f "[p]ytest -q tests"` inside a command whose own text
contained "pytest -q tests" killed that command (exit 144). Same class of error
as the earlier pgrep self-matches. Rule: never pkill by a pattern that also
appears in the current command line; kill by PID.
