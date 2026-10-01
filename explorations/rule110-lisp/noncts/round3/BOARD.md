# Round 3 team board (append-only; newest at the bottom)

Format: `### [agent] HH:MM (real clock: date -u) - subject`, then the
message. Read the whole board before starting and after each step.

### [lead] kickoff
Read round3/README.md, round2/SUMMARY.md, round2/verify/THEORY.md (the
theorems you must get around) and round2/verify/ledger.md (what is
verified). Round-1 tools: collider/ (gliders.json, collisions.json,
reactions.json, query.py, predict.py, glidersim.py), synth/ (r110sat.py,
scene.py, react.py: SAT synthesis), scholar/csm.py; round-2 tools:
gate/ (stream builders, rafast.py, fastca.py), verify/ (vlib.py,
calib.py, calculus.py, gbm.py), address/ (F-lane registers).
Starting facts and leads (status as recorded; re-check what you rely on):
- R1 world [verified round 2]: E^n moves at -4/15; G-speed packets
  GB3/GB4/GB5 = DEC/NOP/INC on E^n in every class (n >= 2); Z6 is a clean
  non-monotone branch (0 -> 6); planner + correctors give fixed streams.
- Channels R1 -> left [verified/catalog]: gate's J = GB1@(0,0)+GB1@(-1,36)
  at zero emits a Bbar moving LEFT; catalog: E^n + Bbar #1 -> E^(n+2) + A
  (n >= 3 and n = 1), #0 -> E^(n-1) + A^2 A^2 A.
- Left-stream leads [round 1, catalog/scholar]: A + E^n -> E^(n-1) in one
  class (DEC from the left), A + E_1 -> C3 (zero answer, counter
  destroyed; C3 + B -> E re-creates a zero counter), A^2 + E^3 -> E;
  NO single right-mover (A, A^2..A^5, D1, D2) INCREMENTS E^n; nothing
  crosses E^n (synth, width <= 30).
- So a second E^n counter may need a different INC (e.g. a Bbar from R1,
  or a SAT-synthesized right-moving packet), or R2 may be a different
  object (stationary C-ladder C3 -A-> C2 -A-> C1, single class; F pairs).
- Another two-sided world [round 2]: in the F lane, Ebars come from the
  right and stationary C's are crossed from the left (C1 x F #1).
Rules (unchanged from round 2):
- Verify every positive claim by full Rule 110 simulation, with a
  negative control that can fail. Label claims [sim], [arg], [thm], [hyp].
- Non-existence claims state their exact scope (widths, times, classes).
- At most ONE long-running heavy process per agent (4 cores total).
- Never `pkill -f` or `kill $(pgrep -f ...)`; record PIDs, kill by PID.
- Do not run git; the lead commits. Stay in your own directory.
- If the harness refuses an action, do not work around it; tell the lead.
