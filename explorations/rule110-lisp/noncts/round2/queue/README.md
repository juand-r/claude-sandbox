# queue: a queue automaton with finite control in Rule 110 (round 2)

Goal: extend Cook's verified glider queue (the main project's encoder /
casim) so that what a read appends depends on a carried state, not only
on the position in the periodic program (i.e. not a cyclic tag system).

Status: no state-dependent step was built. What exists is a glider-level
picture of Cook's read cycle, a charge (slip) law that says exactly what
any finite-control extension of this queue must pay, tools to edit Cook's
table at t = 0 and run it exactly, and scoped negative screens. Details and
commands are in NOTES.md; the final summary is on ../BOARD.md.

Files:
- splice.py: build Cook rows (or custom block sequences / custom blocks),
  insert or replace table material at exact lattice placements, re-attach
  the rest with a machine symmetry shift, run (casim.Run), census in the
  Ebar frame, decoder-free read check for arbitrary rows.
- view.py, answer_path.py, answer_type.py, filt.py, t_k.py, t_rawk.py:
  look at answers and leaders (typed objects over time).
- slips.py: measured slips of tape symbols.
- scan_*.py / screen_tight.py / check4.py / classify_scan.py: screens
  (logs *.log / *.jsonl next to them).
- len6.py: odd vs even rejected appendant length. forcedN.py: periodic test
  of the E9 leader. t_e9.py, t_pair.py, t_shift.py: traces.

Run any script from this directory with the main project's Python
environment (numba, numpy, PIL); they import ../../.. modules read-only.
