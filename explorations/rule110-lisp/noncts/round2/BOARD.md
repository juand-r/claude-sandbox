# Round 2 team board (append-only; newest at the bottom)

Format: `### [agent] HH:MM (real clock, `date -u`) - subject`, then the
message. Read the whole board before starting and after each step.

### [lead] kickoff
Read noncts/SUMMARY.md first, then the round-1 files you need. Frontier:
- E^n counter + rigid G-speed stream: GB3 = DEC, GB4 = NOP, GB5 = INC on
  E^n in every class for n >= 2 (collider, re-checked by scholar). At
  zero, GB3 #0 -> E + A: the answer is one A moving right into the
  oncoming stream. The A already transforms some packets:
  A + (GB3, GB5) -> GB3, A + (G, GB2) -> GB4, A + GB4 #4 -> A (passes),
  A + GB1 #3 -> G. No clean "hard gate" (A + H -> GB4 with H doing
  something else without A) up to 44 cells wide (synth).
- F-memory lane (architect): order-independent crossings C1 x F #1,
  F x Ebar #3, C1 x Ebar #1; F-pair counter with pass-through INC/DEC;
  no non-destructive zero test found (660 + 1,302 packet tests, SAT <= 24).
- Obstruction (argued, checked against the catalog): no right-mover
  crosses a stationary C cleanly; no left-mover faster than Ebar crosses
  an Ebar. Exception: specific 8-9 A packets cross one C cell (fuel).
- Tools: collider/ (gliders.json, collisions.json, reactions.json,
  query.py, predict.py, glidersim.py), synth/ (r110sat.py, react.py,
  scene.py), scholar/ (r110check.py, classes.py, csm.py, stationary.py),
  ../../engine.py (exact Rule 110), ../../census.py (glider census).
Rules:
- Verify every positive claim by full Rule 110 simulation, with a
  negative control that can fail. Label claims [sim], [arg], [hyp].
- Non-existence claims state their exact scope (widths, times, classes).
- At most ONE long-running heavy process per agent (4 cores total).
- Never `pkill -f` or `kill $(pgrep -f ...)`: it kills your own shell.
  Record PIDs at launch and kill by PID.
- Do not run git; the lead commits. Stay in your own directory; do not
  edit round-1 files (import or copy them).
- If the harness refuses an action, do not work around it; note it and
  tell the lead.
