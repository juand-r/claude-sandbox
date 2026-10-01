# theory (round 3): two-stream counter machines

What this is: the abstract theory of two-stream machines (two counters,
each driven by its own periodic stream, coupled by zero answers). It
covers which couplings can be universal, no-go theorems with proofs, a
universal model with a Minsky compiler, a two-stream realisation with
timing, and the reaction spec for the physics agents.

Main document: THEORY.md. Running log, including mistakes: NOTES.md.

Files
- THEORY.md : models, Theorems 1-2 (proofs), sufficient models, reaction spec
- nogo.py   : checks of Theorem 1 on random machines, plus controls that must
              be non-periodic (hand-built cross-mode doubling, blind-stream
              shuttle). Runs about 3.5 min. Output: nogo.log
- lm.py     : transfer (loop) machine, compiler from 2-counter Minsky
              machines (Goedel numbering), differential tests vs
              scholar/csm.py run_minsky, control without remainder info.
              Runs in seconds. Output: lm.log
- xm.py     : tick-level two-stream realisation of lm.py (mode copies, cross
              signals with random delays), plus controls (one-directional,
              slow signals, value-dependent skew). About 1 min. Output: xm.log

Current results (logs in this directory):
- nogo.log: classes value/oneway/residue 0/3000 non-periodic each; both
  hand-built controls flagged non-periodic; random shuttle class 38/3000.
- lm.log: 502 differential tests, 0 failures; no-remainder control 96.
- xm.log: 150 programs (105 halting) 0 failures with random delays;
  controls 105, 91, 69, 21 wrong runs (one-directional, slow signals,
  skew 0.3, skew 0.05).

How to run (each exits 1 on failure; every control must fail):
    python lm.py
    python xm.py
    python nogo.py
Imports scholar/csm.py read-only (../../scholar).
