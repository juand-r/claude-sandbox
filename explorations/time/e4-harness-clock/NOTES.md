# E4 working notes

## Design decisions
- 9 scenarios, families: freshness / staleness / expiry / wait. Each binary decision
  with a documented human threshold (in seconds).
- 4 gaps per scenario straddling the threshold (two clearly-fresh/borderline-fresh,
  two borderline-stale/clearly-stale). Gaps are never placed exactly on the threshold,
  so `correct_label` is always well-defined (fresh if gap < threshold else stale).
- 3 conditions on the SAME scenario+gap:
  - none: transcript states the prior action, explicitly "(No timing information)".
  - text: ISO absolute timestamps on transcript lines; model computes gap itself.
  - harness: a `[HARNESS] elapsed since that action: <humanized>` field.
- Forced one-word label, parsed by substring match (last-occurrence tiebreak).
- N=3 trials, temperature 0 (deterministic-ish), models haiku/sonnet/opus/gpt4o/o4-mini.

## Bug log
- opus (claude-opus-4-8) returns 400 "`temperature` is deprecated for this model" when
  temperature is passed at all. common.py only skips temperature for REASONING_MODELS
  (the gpt-5/o4 family), not opus. Fix in run.py: NO_TEMPERATURE = {"opus"} -> pass
  temperature=None for opus. Dropped the failed opus rows and re-ran; resume logic
  (load_done) refills only missing cells.
- First background launch wrote 11-12 opus failures before/around the edit landing;
  cleaned them out by filtering ok==False rows, then relaunched.

## Observations during dry run (stock_price, threshold 5 min)
- haiku & sonnet in `none` default to REFETCH for everything (wrong on fresh gaps) —
  with no time signal they assume a fast-moving quote is stale.
- `harness` flipped both to correct REUSE on the fresh gaps. This is the E4 effect.
- `text` (absolute timestamps): sonnet computed the gap and got fresh cases right;
  haiku still said REFETCH (did not reliably compute the gap). Suggestive that text
  timestamps help the stronger model but not the weaker one, while the harness clock
  helps both — consistent with the hypothesis.
