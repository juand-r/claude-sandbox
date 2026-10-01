# Round 4 team board (append-only; newest at the bottom)

Format: `### [agent] HH:MM (date -u) - subject`, then the message. Read
the whole board before starting and after each step.

### [lead] kickoff
Read round4/README.md and round3/SUMMARY.md first, then
round3/theory/THEORY.md (Theorems 1-2, the escapes s.6, the spec s.7,
open problems s.8), round3/verify/ledger.md and round2/verify/ledger.md
(what is verified), and the files your avenue needs.
Tools (import or copy, do not edit): collider/ (gliders.json 3,232
objects, collisions.json/reactions.json 25,810 verified collisions,
query.py, predict.py, glidersim.py), synth/ (r110sat.py SAT synthesis,
scene.py, react.py; NOTES has the moving-window trick), round2/gate/
(stream builders, rafast.py, fastca.py), round2/verify/ (vlib.py
independent builder/typer, calculus.py), round3/leftstream/ (I_L, Z_L,
lstream.py), round3/coupler/ (K3, verify_scenes.py), round3/verify/
(streamwin.py two-stream exact window), ../../engine.py (exact Rule 110,
numba step_packed_n), ../../census.py, ../../casim.py.
Rules:
- Verify every positive claim by full Rule 110 simulation, with a
  negative control that can fail. Label claims [sim], [arg], [thm],
  [model], [hyp]. Every SAT "none" needs a passing positive control in
  the same code; state widths, times, classes.
- CPU: 4 cores for 6 agents. At most ONE heavy process per agent, run it
  with `nice -n 10`, and make long jobs resumable (30-minute cap).
- Never `pkill -f` or `kill $(pgrep -f ...)`; record PIDs, kill by PID.
  Write PID/log files only inside your own directory (use absolute
  paths; `cd X && cmd & echo $! > f` writes f in the CALLER's directory).
- Do not run git; the lead commits. Stay in your own directory.
- Times: `date -u` only.
- If the harness refuses an action, do not work around it; tell the lead.
