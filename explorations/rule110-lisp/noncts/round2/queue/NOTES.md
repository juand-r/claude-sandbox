# queue: running log (agent "queue", round 2)

Task: a queue automaton with genuine finite control in Rule 110 (not a
cyclic tag system). See ../README.md and ../BOARD.md.

## Plan (revisit and tick)

- [x] P1 Look inside Cook's machine at glider level: what are the leader,
      prepared leader, acceptor, rejector, components, moving data?
      (typed spacetime pictures of one accept and one reject)
- [x] P2 Pick a state mechanism (explored; see Analysis: the charge law
      rules out clean versions of (a) and limits (b); (c) is the target).
      Candidates:
      (a) conditional leader: an object X with acceptor+X -> leader,
          rejector+X -> deleted (rejector continues) => a read N skips the
          next block => position in the program becomes data-dependent;
      (b) state in phase (appendant length not = 0 mod 6 changes the next
          leader's class after reject vs accept);
      (c) state in the preparation of the next leader.
- [ ] P3 One verified state-dependent step (+ negative control). NOT
      ACHIEVED.
- [ ] P4 Small clockwise TM end to end. NOT ATTEMPTED (needs P3).

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

[SUPERSEDED by the "Charge law" section below: the premise that acc and
rej differ by 7 at the same table point was wrong.]
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

### 00:20-00:40 corrections and more negatives

- MISTAKE corrected: I had inferred tape-symbol slips Y 9 / N 2 from the
  F/E moving-data blocks. Measured directly (slips.py) both are 2 (4 C's).
  The slip law is unchanged (it only needs the values mod 7).
- MISTAKE: scan_en.py E3 produced no rows: the object typed "E^3" inside K
  is not collider's E^3 glider (identity replacement fails), so the E3
  scan was vacuous. Not reported as a negative.
- MISTAKE (process): a first pair screen used insert_items (minimal
  alignment, generally NOT a machine symmetry), so its "hits" were
  confounded by a misaligned K. Replaced by insert_exact + valid_shifts.
- MISTAKE (process): killing a "sh -c" wrapper by PID left its timeout
  child running; killed the children by PID afterwards. Use one process
  per background job.
- forcedN.py (periodic program {YNNNNN, NNNNNN}, appendant-1 leader = E9
  variant "X" built as a custom block with make_block): control with K
  matches the CTS 6/6 (YYNYYN); with X: Y, N(forced), then '!' at read 2.
  So the E9 leader is not clean in a periodic program.
- make_block() check: a block rebuilt from an unedited row equals K row
  for row (35..64); a machine with X at the first leader reproduces the
  replace_exact run ([26,2] both).

## Analysis (for the final report)

### The read cycle at glider level [sim]
read: prepared leader P + tape symbol (4 C's) -> answer
  Y -> acceptor: stationary C-family object (C3 <-> C1^2 ...), the table
       flows into it; each component comes out as moving-data Ebars;
  N -> rejector: right-mover D1 <-> A^3, each component is deleted.
sweep end: answer + raw leader K -> P (identical for acc and rej; acc
  also leaves one extra moving Ebar). K = [Ebar][E5][E2][E^3][Ebars];
  [Ebar, E5, E2] -> [Ebar, E1].
unprepared K at the tape: eats the symbol, leaves an E_n (typed E^7) and
  a B^5, no answer (t_rawk.py).

### Charge (slip mod 7) law [arg; slip conservation is a theorem]
Measured slips mod 14: K 12, P 8, components 0, tape symbol 2, ossifier
2, moving data 0 or 7. Mod 7 a read (K + symbol) is neutral: leaders carry
charge -2, symbols +2. Over one program period with p leaders, a machine
whose only garbage is Ebar trains reads n = p (mod 7) symbols. Hence a
finite control that changes the number of reads per period (soft leaders,
skips, jumps) must either
  (a) change it by multiples of 7 (e.g. a jump over 7 blocks), or
  (b) dump the unpaired charge as non-Ebar garbage: per skipped leader an
      "anti-symbol" of slip 12 (e.g. something that later eats one tape
      symbol, or that an ossifier annihilates), or
  (c) keep one read per leader and put the state into HOW the leader
      reads (P_acc != P_rej, same charge), e.g. normal vs forced-N.
Observed: every rejector "pass" in my screens left B-type garbage that ran
left and ate tape symbols - option (b) realised badly.

### Why (c) is the cheapest target
(c) needs no charge bookkeeping at all: a leader variant whose prepared
form after an acceptor reads normally and after a rejector is forced to N
(or inverted). Forced-N readers exist (E9 variant) but were not clean in a
periodic program, and none of the screened variants depended on the
incoming answer type. Machine semantics if found: a(i) = s(i) AND a(i-1)
on such blocks, a(i) = s(i) on plain blocks; block i appends iff a(i) = Y.
That is a genuine 1-bit control (same symbol, same block, different
appendant depending on earlier reads), with one read per leader.

### 00:40-01:00 inside-leader scans, tight-pair screen

- scan_gap.py [sim]: shifting E2 (and everything after it) by machine
  symmetries V relative to E5 (gap +16..+80 cells, 8 shifts) keeps all
  four tapes normal: V is a symmetry even inside K.
- scan_en.py E2b / E5b [sim]: moving E2 to any of 62 other lattice
  placements, or E5 to any of 60 other placements (V-inequivalent),
  breaks the machine (garbage). Only V-equivalent placements are normal.
- screen_tight.py (tight Ebar-pair compounds from collider/gliders.json,
  slip 0, inserted right before K; acceptor tape YNYN must stay normal):
  ~20 of the first 1361 placements keep the acceptor path normal, mostly
  Ebar_14_Ebar. Stage B (check4b.py, four tapes): acc-in tapes normal,
  rej-in tapes broken. Ebar_14_Ebar (k=0, o=22): YYNN correct for 5 reads
  (t_tight.py ... YYNN 140000 7000); with a rejector the pair + K emit a
  burst of 7 B's (B^2 + B^4 + B: slip 42 = 0, charge-neutral, the analogue
  of gate's 7-jump) that runs left and wrecks the tape (t_tight2.py).
  So: an acceptor-transparent, rejector-sensitive insertion exists; its
  rejector branch is not clean. A garbage collector for B's would be any
  E_n to their left (B + E_n -> E_(n+1), single class), but everything to
  the left of a leader is swept by the answer first, and nothing crosses
  E_n, so I see no place to put one.
- Process note: Monitor returns immediately; I re-armed it several times
  thinking it had waited. It notifies asynchronously.

### Spec for option (c) (spec_cut.py -> spec_c.npz)
Exact windows (Ebar-frame-following lab windows, K-700..K+500 global at
t = 0) of: the acceptor arriving at the first raw leader (tape YYNN,
t = 13000; the acceptor is C1^2 at K-498) and the rejector arriving (NYYN,
t = 8300), and the same windows 4000 steps later with the plain K (target:
standard prepared leader, E1 at K+68) and with the E9 variant (forced-N
reader). A leader K' realising option (c) maps
  acc-before -> plainK-after (normal reader), rej-before -> E9-after
  (forced-N reader), or any other pair of clean, different readers.
Note the forced-N reader itself was not clean in a periodic program
(forcedN.py), so the right-hand target should be re-validated first.

### 01:00-01:15 stage B, rejector garbage, anti-symbol test, charge symmetry

- Stage B (check4b.jsonl, 34 acceptor-transparent survivors of 1906
  tight-pair placements): acceptor tapes normal for most; on rejector
  tapes the next appendant stays RAW or is garbled, always after a burst
  of B's running left from the leader: e.g. Ebar@(0,0)+Ebar@(-13,31)
  (k=8,o=5): B + B^4 (5 B's, slip 2) and the leader remnant
  [E^3, E(w1), E^3]; Ebar_14_Ebar (k=3,o=17): B^2 + B + B^5 (t_tight2.py).
- eat_symbol.py [sim]: a clean Cook tape symbol (4 C's, slip 2) hit by a
  B pair (two B tiles) at 5 placements (phase 2, offsets 65-69) becomes
  exactly two Ebars (typed at T = 1400; other placements give E+F,
  Ebar+F, A+E+F, C2+Ebar+G, ...). So an "anti-symbol" B^2 (slip 12) that
  eats one tape symbol into Ebar-train garbage exists, as the charge law
  allows. (Not checked: whether the two Ebars then cross the remaining
  tape and the ossifiers harmlessly.)
- Charge symmetry [arg]: the acceptor and rejector branches of a block
  start from answers of equal slip, consume the same table material and
  both end in the same prepared leader, so the garbage they leave has
  equal charge mod 7 (standard moving data is neutral). A skip on ONE
  branch (rejector eats the next symbol, charge -2) therefore forces the
  other branch to destroy charge -2 somewhere too, e.g. an "anti-word"
  of moving data that annihilates one ossifier, or forces the branches to
  end in different prepared leaders. This is why simple insertions
  before K cannot give a clean one-branch skip.

### 01:25 tight-pair screen complete
screen_tight.jsonl: all 3960 placements of 66 tight Ebar-pair compounds
(phases x 2 offsets) right before K; 720 have no valid symmetric
re-attachment, 3240 were run on the acceptor tape YNYN (T = 40000), 62
kept it normal. check4b.jsonl (all 62, four tapes, T = 60000): 33 keep
both acceptor tapes normal; NONE has a clean rejector branch. Four looked
like "forced N after a rejector" (NYYN -> NN, NNYY -> NN; e.g.
Ebar@(0,0)+Ebar@(-18,37) k = 9, o = 22), but traces (t_tight.py ... NYYN
130000 5000) show the appendant region being destroyed by garbage, not
swept; later reads are chaos. Scoped negative for option (c) in this
family.

## Continuation (lead's request, 01:35-): option (c) synthesis

### Step 1: is there a clean alternative reader?
- verify_lead.py: decoder-free multi-read check vs a reference with
  forced-N leaders. t_forced_diag.py [sim]: E9 leader at the FIRST K only:
  tape YNYN (forced read of an N) 6/6 = reference; tape YYNN (forced read
  of a Y) Y,N, then '!' at read 2. Control (plain): 6/6 both tapes.
  t_e9read.py: reading a Y, the E9 reader emits the standard rejector PLUS
  one B running left (B@64 at t=32700), which damages the next tape
  symbol. Reading an N it emits only the rejector. So the forced-N reader
  is clean on N and dirty on Y.
- E2 -> E16 (scan_en_E2c.log, 63 placements): no clean variant (the 4
  "forced-N" rows also break read 0).
- Prepared core after a REJECTOR (N-first tapes, Ebar frame, t = 32000):
  [Ebar@39][E@68] (slip 2); after an acceptor there is an extra moving
  Ebar@0 in front. The read of K's leader happens at ~33000.
- reader_screen.py: replace the rejector-prepared core [K-30, K+110) at
  t_in = 32000 by every placement of every slip-2 Ebar-speed library
  object (74 objects); scenes NYYN (reads Y) and NNYY (reads N); compare
  the window [K-700, K+700) at 34000 cell for cell with the plain Y and N
  outcomes. Positive control inside the search space: the original core is
  'Ebar@(0,0)+E@(-5,27)' (k=9, o=55) (identity reproduces the row).
  A first run on acc-first tapes was the wrong setting (it kept the
  acceptor's extra Ebar); moved to trash/.
