# queue (round 4): running log

Avenue (e): a queue machine with genuine finite control in Rule 110, not a
cyclic tag system. Builds on round2/queue (Cook's read cycle at glider
level, charge law, option (c) SAT).

## Plan (tick as done)
- [ ] P0 Read board, round2/queue, scholar THEORY, Cook machinery. 
- [ ] P1 Phase as state: does a rejected appendant of length L != 0 mod 6
      leave a DIFFERENT prepared leader (P_r, r = L mod 6)? What does P_r
      read, and what does its answer write? (round2: L=8 reads 1-5 ok,
      read 6 wrong: a Y written after the shifted read was READ AS N.)
- [ ] P2 If P_r is a clean reader with a different function or a clean
      displaced reader: build the state model and verify a state-dependent
      read (same symbol, same block, different appended data).
- [ ] P3 Otherwise: option (c) / skip-with-anti-symbol by SAT with moving
      windows and wider regions.
- [ ] P4 Small demo + non-CTS argument.

## Log
