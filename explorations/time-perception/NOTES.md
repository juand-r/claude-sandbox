# NOTES — overnight session

Working autonomously while the user sleeps. Discipline: one change at a time,
log hypotheses + findings, commit per milestone, report negative results too.

### F3. Stage 2, coupling — answers the open question with a quantified trade-off.
- Setup: Kuramoto mean-field, 24 oscillators, f in [0.5, 4] Hz.
- Sync transition at K_c ~ 8 (steady-state r jumps 0.2 -> ~0.9 around K=8-10).
- Coding horizon (first recurrence of the start pattern) COLLAPSES at the same K:
  >30s (censored) for K<=7.5, then 25.7 (K=8) -> 3.4 (K=9) -> 0.46 (K>=12).
  Strong coupling locks everything to one frequency -> the multi-scale code dies.
- Recency (order parameter at t=2s after a reset): K=0 -> 0.10 (decays fast);
  rises with K. SWEET SPOT K~6-8: r(2s) ~0.27-0.37 (recency sustained ~3x longer)
  while horizon still intact (>=25s). K>=9: strong recency but code destroyed.
- VERDICT: coupling earns its place, but only in a narrow weak-coupling window
  just below K_c. It buys a longer-lasting recency signal without killing the
  code. Above K_c it is catastrophic. Matches the Stage-1 skeptical prediction.

### F4. Cascade (nested loops) vs incommensurate bank — a capacity/robustness trade-off.
- Cascade = ladder of oscillators each Mx slower = odometer/mixed-radix code.
  4 stages (M=10) -> exact decode over a 1000s range (exponential capacity from a
  linear number of oscillators). Noiseless max error 0.
- BUT catastrophically brittle: per-oscillator phase noise of 0.01 already gives
  off-by-1s errors, 0.02 -> off-by-10s (a flipped digit costs M^k). 90th-pct error
  0 -> 1 -> 10 -> 19s as noise rises.
- Incommensurate bank over the same range degrades GRACEFULLY: 90th-pct error stays
  0.02 -> 0.06s across the same noise range. Robust, but needs more oscillators and
  has a bounded unique range (recurrence horizon).
- Two opposite multi-scale strategies: cascade = compact + exact + brittle (digital);
  bank = redundant + graceful + bounded-range (analog). Note: this is the SAME lesson
  as F3 in another guise -- structure that maximises capacity (tight coupling /
  positional code) is fragile; redundancy buys robustness.

## Tonight's queue
1. Stage 1b: SBF coincidence read-out (analytic cosines).
   - Hyp: scalar property emerges from per-trial FREQUENCY jitter via the readout
     (SD of estimate ~ proportional to T), NOT injected as scalar rate jitter.
   - Hyp: bisection point lands on the GEOMETRIC mean with log-spaced freqs, and
     drifts toward the arithmetic mean with linear-spaced freqs (controlled test).
2. Stage 1b: Bayesian central tendency on top of the SBF estimate.
   - Hyp: prior over tested range -> regression slope < 1, indifference at geomean.
3. Stage 2: Kuramoto coupling.
   - Hyp: coherence gives a recency signal; strong K collapses the multi-scale
     code. Quantify with a "coding horizon" metric vs K. Answer: does coupling
     earn its place?
4. Stage 2: hierarchical cascade (nested loops) = mixed-radix self-generated clock.
5. Robustness sweep of the holiday-paradox dissociation.
6. Write REPORT.md.

## Findings log

### F1. SBF read-out, first run — all three hypotheses FAILED, same root cause.
- Scalar property: CV grew 0.035 -> 0.455 (not flat). Independent per-oscillator
  frequency jitter scrambles the phase pattern (phase error ~ f_i*eta*T exceeds pi
  at long T) instead of rescaling time. => Scalar property needs COMMON-MODE
  (global rate) jitter, one eta per trial scaling all oscillators. This is exactly
  the SET claim (trial-to-trial pacemaker-rate variation). Independent local noise
  is a different, code-degrading process.
- Bisection point landed at 4.70 (nonsense, < anchors midpoint). Cause: raw dot
  product not norm-matched; templates of different duration have different norms
  and bias the comparison. Fix: cosine similarity / distance.
- Central tendency slope 1.10 (>1, wrong way). It was sitting on the broken
  estimate + asymmetric grid. Fix measurement first.

### Deeper point (to verify): does oscillator coincidence give Weber + geom-mean?
- The analytic coincidence kernel Sum cos(2pi f_i (t-a)) has a peak whose absolute
  width is set by f_max -> CONSTANT absolute resolution, i.e. NOT scalar by itself.
- So scalar timing needs multiplicative (common-mode) noise, and geometric-mean
  bisection likely needs a log/ratio read-out, NOT the linear-phase kernel.

### F2. Stage 1b, corrected run — clean and coherent.
- SBF scalar property: common-mode jitter 0.05 -> CV flat ~0.05. Independent jitter
  0.05 -> CV grows 0.03 -> 0.23. CONFIRMS scalar property = common-mode rate noise.
- SBF native resolution (A3) peaks sharply (width ~1/f_max) at the anchor; far from
  it, similarity is ~0. Resolution is ABSOLUTE, not scalar.
- SBF bisection DEGENERATES: point ~4.7 (log) / 4.0 (lin), meaningless. Reason: with
  only two templates (S=4, L=16) a probe in between is >1/f_max from BOTH, so both
  similarities collapse to ~0 and the decision is residual-noise driven. Coincidence
  works as RECOGNITION (dense template bank, as in estimation) but cannot INTERPOLATE
  / compare across a wide gap with sparse anchors. Honest limitation of the substrate.
- Log observer does all three cleanly: CV flat 0.15; bisection point 7.98 ~ geom 8.0;
  central tendency slope 0.79 (<1), indifference 8.5 ~ geom 8.1 (Vierordt).
- Takeaway: the oscillator substrate gives the multi-scale code + scalar variability
  (with common-mode noise); the BEHAVIOURAL signatures (geom-mean bisection,
  Vierordt) live in a log/ratio read-out on top. Oscillations are necessary but not
  sufficient for the psychophysics.
