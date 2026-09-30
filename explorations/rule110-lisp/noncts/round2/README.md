# Non-CTS computers in Rule 110, round 2 (started 2026-09-30)

Round 1 (noncts/SUMMARY.md, noncts/BOARD.md, noncts/*/) produced a
verified collision catalog, building blocks for a two-counter machine,
and a reasoned explanation of why known Rule 110 computers are queues.
It did not produce a machine. Round 2 attacks what was missing.

Goal, in tiers:
- M1: one verified data-dependent branch in the automaton: a stored value
  (zero vs nonzero) changes what the later program does, cleanly and
  composably.
- M2: a nontrivially programmable non-CTS machine running end to end in
  the automaton (for example a counter loop that branches on zero, or
  parity of a counter).
- M3: a universal non-CTS machine: two counters (or an equivalent) with a
  compiler from Minsky machines, demonstrated on a small program.

Agents, one directory each:
- gate/    - make zero answers act on the program stream (M1, M2)
- address/ - two registers, or universality without addressing
- queue/   - a queue automaton with genuine finite control (not a CTS)
- verify/  - independent verification, the ledger, end-to-end integration

BOARD.md is the shared board (append-only). Each agent keeps NOTES.md
in its directory; its final report goes to the lead.
