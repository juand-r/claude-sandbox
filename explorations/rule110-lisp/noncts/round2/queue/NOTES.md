# queue: running log (agent "queue", round 2)

Task: a queue automaton with genuine finite control in Rule 110 (not a
cyclic tag system). See ../README.md and ../BOARD.md.

## Plan (revisit and tick)

- [ ] P1 Look inside Cook's machine at glider level: what are the leader,
      prepared leader, acceptor, rejector, components, moving data?
      (typed spacetime pictures of one accept and one reject)
- [ ] P2 Pick a state mechanism. Candidates:
      (a) conditional leader: an object X with acceptor+X -> leader,
          rejector+X -> deleted (rejector continues) => a read N skips the
          next block => position in the program becomes data-dependent;
      (b) state in phase (appendant length not = 0 mod 6 changes the next
          leader's class after reject vs accept);
      (c) state in the preparation of the next leader.
- [ ] P3 One verified state-dependent step (+ negative control).
- [ ] P4 Small clockwise TM end to end.

## Log

### 23:30-00:45 Looking inside Cook's machine (P1)

Tools: view.py (typed spacetime PNG), answer_path.py / answer_type.py
(non-Ebar objects in the Ebar frame, typed with scholar/r110check),
splice.py (edit the t = 0 table; run with casim.Run; census in the Ebar
frame), filt.py.

Findings, all [sim] (runs cited):
1. The ACCEPTOR is a stationary object in the lab frame (C family): typed
   C3 -> C1^2 -> ... -> C3 as the table's Ebar clusters flow into it; it
   emits moving data (Ebars) and drifts right slowly (net ~0.05 c/step).
   `python answer_path.py YN YNNNNN 536 1200 12000 -500 4400 300`.
2. The REJECTOR is a right-mover: D1 -> A^3 -> D1 per Ebar pair
   (catalog: D1+Ebar#3/#9 -> A^3, A^3+Ebar#2/#3/#5 -> D1), 0.47 c/step
   in the Ebar frame. `python answer_type.py NY YNNNNN 536 3300 12300 900 4000 300 | python filt.py`.
   So Cook's answer is a finite-state TRANSDUCER through which the table
   flows; acc/rej are two families (C vs D1/A^3).
3. The raw leader K = [Ebar][E5][E2][E^3][Ebars...] (E_n = Cook's
   extendible E, typed by period (15,-4) and width 5 / 1). Both answers
   turn [Ebar, E5, E2] into [Ebar, E1] (acc also leaves one extra Ebar of
   moving data). Prepared leader identical after acc and rej.
   `python t_k.py YN 11700 12300 50 3700 4000`, `python t_k.py NY 8600 9000 30 3750 4000`.
4. Slips (ether phase jump across a block at t = 0, splice.phase_at):
   II, IJ = 0; K = 12; G (prepared leader) = 8; F (moving Y) = 7, E = 0.
5. Rejected appendants of ODD length break the machine at the next read
   (L = 7, 9, 11: region "!", then a garbage cascade with G, B^2 gliders);
   EVEN lengths 8, 10 gave correct reads for 4 reads (len6.py, len6.log).
   So the rejection constraint seen here is parity, not "multiple of 6"
   (scope: 4 reads, program {N^L, YNNNNN}, tape NYYNYY, v = 2*Cook's).

### Where state could cross a read [arg]

Answer k is absorbed by leader k+1, which then reads. So state can cross
from read k to read k+1 only (a) if some leader is transparent to one
answer type ("soft leader" S: rej deletes it and continues, acc prepares
it), or (b) if the prepared leader differs according to the answer and
both forms read cleanly. With only Cook's K the control is the fixed cycle
(a CTS). A toggle T (acc <-> rej inside an appendant) would give
symbol-dependent appendants but still fixed control flow.

Slip bookkeeping for S (answers at the same table point differ by 7:
C3 = 3 vs A^3 = 10 etc.): if rej + S -> rej + g and acc + S -> P + md
(P the standard prepared leader, md emitted moving data), then
slip(S) = slip(g) = 5 + slip(md) (mod 14). So a garbage-free S (g empty)
is impossible unless the accept path emits moving data of slip 9 [arg].
Garbage of slip 5 could be an E5 or E1+..., which would have to cross the
tape and the ossifiers.

### Negative screens [sim]
- K (and everything after it) translated by 60 lattice shifts (s = 0..29,
  m = 0..1): the rejector is absorbed in every one (scan_leader.log).
- One Ebar inserted just before K (90 placements, scan_S1.log): no clean
  pass of the rejector; a few placements destroy K and the next
  appendant with garbage (e.g. k=27, t_tr3.py NY 27 0 30000).
- Replacing K by G, L, KK, LK, KL, GK, DK, HK, IK, EDK, FDK (t_subst.py):
  G/GK with a rejector give garbage; the rest behave like K.
- A symbol emptied to ether: the acceptor crosses the gap and then dies
  on the next component (class mismatch) (t_trace.py).

### 00:00-00:20 slip law, symmetry lattice, E_n leader variants

- Board post at 00:09 (I wrote "00:20" in its header by mistake; the
  real time was 00:09).
- scan_shift2.py/.log [sim]: of 60 spacetime shifts of (K + everything
  after), only (0,0), (s=6,D=24), (s=18,D=16) keep reads 0/1 correct for
  YYNN/YNYN/NYYN/NNYY. These generate V = <(12,8),(30,-8)>; splice.
  valid_shifts() lists V; insert_exact()/replace_exact() re-attach the
  remainder with a V shift so that an edit is the ONLY change.
- Slip law [arg]: per program period 12p + 9n_Y + 2n_N = 7m_Y + g
  (mod 14) => n = p + 4g (mod 7). Measured slips: K 12, G 8, II/IJ 0,
  moving Y 7 / N 0, ossifier 2 (B block = one A^4 = 4), tape Y 9 / N 2.
- Pair screen (scan_pair.py, 545 of 3600 pairs before I stopped it):
  every "rejector passes" hit (14) left B-type garbage that ran left and
  ate tape data; the acceptor path of the two clean-looking ones is broken.
  Not soft leaders. Consistent with the slip law.
- E9 instead of E2 in the leader (scan_e9.log): placements (2,23),
  (5,34), (14,9) give a leader that ALWAYS REJECTS: it consumes one
  symbol, appends nothing, and the machine continues correctly
  (t_e9.py 2 23 YYNN 110000 5000 first: reads Y,[N],N,N vs reference
  Y,Y,N,N - the forced read consumed the Y). [sim, 4 tapes x 2 reads +
  one longer run]. A slip-neutral "empty appendant" leader; possibly a
  replacement for Cook's broken L block (not yet checked in a periodic
  program).
- Idea being screened (scan_en.py E5/E3): a leader variant whose
  behaviour depends on the INCOMING answer type (acc vs rej). If one
  reads normally after acc and is forced to N after rej (or vice versa),
  that is a 2-state control (live/dead) with one symbol per leader, which
  the slip law allows.
