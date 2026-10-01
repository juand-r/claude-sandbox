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

### [verify] 05:31 (real clock: Thu Oct 1 05:31 UTC) - tools up, independent survey, how to hand me claims
1. Independent survey [sim, my builder/typer = round2/verify vlib, exact
   engine; all t0 < P_L x 14 offsets, T=1500; verify/survey_left.log]:
   - A + E^n -> E^(n-1) in 1 of 3 classes (n=2..6); A + E^2 -> E in all 3.
   - A^k + E^(k+1) -> E in ALL classes for k=1..4 (a class-free "set to
     zero if v=k"); A + E -> C3 (1 class) or D1 (2 classes).
   - C3 + B -> E in all classes.
   - E^n + Bbar (Bbar from the right), 3 classes: E^(n+2)+A (n=1,3..6),
     E^(n-1)+A^2+A^2+A (n>=3), E^(n-3)+?+A (n>=4); E^2 + Bbar is garbage
     in every class. Agrees with coupler's catalog reading.
   - Single C1/C2/C3/D1/D2 never give E^(n+-1) cleanly (n=1..6).
2. Instrument: verify/streamwin.py = exact two-stream moving window.
   Left stream (one period vector, e.g. A-family (3,2)) and right stream
   (e.g. G-family (42,-14)) are replaced by their free evolutions (checked
   periodic), the window around the core is stepped exactly, and cell
   equality with the free streams at both window edges is checked every
   step (rigorous; extends/shrinks automatically). test_streamwin.py: equal
   to full engine runs cell for cell at t=500..8000; two controls fail as
   they must. For reference, the plain packed engine does ~7e10
   cell-steps/s, so runs up to ~1e6 steps x 1e6 cells are fine without it.
3. When you post a positive claim, please give: the exact scene (glider,
   t, x) in collider convention (or your builder + script path), T, the
   expected product list, and the control you ran. I rebuild it with my
   own builder, assert my row equals yours cell for cell, and type with my
   own typer.

### [leftstream] 05:40 (real clock: Thu Oct 1 05:40 UTC) - INC FROM THE LEFT EXISTS: one (3,2) train of slip 6, all n = 1..12, single class
1. Why round 1 found none [arg]: slip is conserved mod 14; E^n -> E^(n+1)
   needs +6. A has slip 8, so k A's have 8k; k = 1..5 (A, A^2..A^5) can
   never INC cleanly, D1 (3), D2 (9) neither. Charge-allowed: 6 A's
   (48 = 6), D1+D1, A+D1+D2. That space was never searched.
2. SAT (synth/ r110sat, free (3,2) train, slip 6, joint n = 1..4, T2 = 220,
   width 24): SAT in all 3 classes in ~5 s each
   (leftstream/sat_inc.py, sat_inc_results.jsonl). Positive control first:
   same code with slip 8, delta -1 finds single-A DECs.
3. Claim [sim, my builder lsl.py on collider's library + exact engine,
   typed by collider's products_of]: train
       I_L = cells 111110111110111110001110 at x = 0..23, t = 0,
       ether phase 0 on its left (ETHER[(x+4t+c)%14] convention),
   E at collider seed (7,44), E^n = E + (n-1) B's from the right (absorbed
   before I_L arrives; I_L moved left by m*(15,-4), same class):
       I_L + E^n -> E^(n+1) exactly, nothing else, n = 1..12.
   Displacement of the result vs E^(n+1) built from the same E by B's:
   (7,-8) for every n. Controls (I_L shifted (1,-4), (2,-8) = the other
   two classes): debris for every n (one exception: shift 2 at n = 1 also
   gives E^2). Script: leftstream/claim_inc.py; exact rows in
   leftstream/inc_scenes.json (x0, cL, cR, bits, T, expected, result).
4. DEC from the left re-measured (leftstream/ops.py): A in 1 class:
   E^n -> E^(n-1), n = 2..8, displacement (5,2) for every n; A + E -> C3.
   Bookkeeping: key f(dt,dx) = 2dt - 3dx mod 42 (vanishes on P_A, 42 on
   P_E); DEC moves later packets' keys by -4, INC by -38 = +4. So with a
   nonzero counter every op's class depends only on the program prefix:
   a rigid A-speed stream can be laid out by bookkeeping alone.
Next: zero test from the left that keeps/rebuilds E (SAT: DEC for n >= 2
and at n = 1 either E + escaping A, or E^7 = wrap), then a stream program.
@verify: rows for re-check are in inc_scenes.json. @theory @coupler: R2 =
E^n with INC and DEC both from the left is now available; tell me what
zero behaviour you want (answer right toward R1? wrap?).

### [verify] 05:55 (real clock: date -u ~05:55) - leftstream's INC from the left VERIFIED; a fixed left INC/DEC stream runs in the CA
1. VERIFIED leftstream 05:40 (INC from the left, I_L, n = 1..12, one class)
   [sim; verify/verify_inc.py]. (A) Your 36 exported rows, run by the
   engine and typed by MY typer: 12/12 INC rows give E^(n+1) alone; the
   controls agree with yours, including the n = 1 shift-2 exception.
   (B) My own construction (my E^n from my own E + B harvests, I_L pasted
   at 3 time phases x 4 offsets): for every n = 1..12 exactly one class
   gives E^(n+1) (n = 1: two), the same over all 4 offsets; the others
   give debris. DEC from the left (A, one class) matches my survey.
2. Integration [sim, mine; verify/t1_nonzero.py, t1_validate.py]: a FIXED
   left stream of 38 packets (I_L = INC, A = DEC), word
   DIIDIDDIIIDDDIIDIDIIIDDIDDIIDIDDDIIIID, built greedily with the CA in
   the loop on inputs v = 1..4 (input = E + v B's from the right), matches
   the model on v = 1..11 (v = 1 passes through value 0 and back). Program
   cells identical for every input; control (one slot moved to another
   class) fails 11/11. This confirms leftstream's bookkeeping claim (class
   progression independent of n) in practice. T1 still needs the zero test.

### [leftstream] 05:45 (real clock: Thu Oct 1 05:45 UTC) - T1 milestone: zero test Z from the left + rigid stream programs (INC/DEC/zero), verified
Thanks verify. The zero test:
1. SAT (leftstream/sat_zero.py; free (3,2) train, slip 8, W 24, T2 250;
   n = 2,3 -> E^(n-1) exactly AND n = 1 -> E | A): SAT in all 3 classes.
   Mode "wrap" (n = 1 -> E^7, gate's Z6 mirrored): UNSAT at W 24, T2 300,
   all 3 classes; W 36 running.
2. Z = sat_zero_results.jsonl #1 (train cells
   111110111110111000111011 is #1's Y? no - see file; typed seed
   ('v2/3s8w16', 0, 6) vs E at (6,46)) [sim, check_rec.py, n = 1..9]:
       Z + E^n -> E^(n-1)           (n >= 2)
       Z + E   -> E + A (A leaves to the RIGHT; counter kept at 0)
   Counter displacement (9,0) in BOTH branches, so the classes of all
   later packets are the same whether or not the counter was zero. It is
   R1's GB3 mirrored: a saturating DEC whose zero answer is one A.
3. Rigid left stream [sim] (lstream.py; lpk.py packets I = I_L, D = A,
   Z): packet i = its reference scene translated to the counter's virtual
   front (sum of earlier displacements) + m_i * P_E; no search. One stream
   text for all inputs (t0 fixed from max v); input = E + v B's.
   rand_test.py: 30 random programs of length 16 over {I,D,Z}, v = 0..8:
   270/270 runs match the model (value AND number of A answers to the
   right, nothing else left over). Exported exact rows:
   leftstream/stream_ZIZZIDIIDIIZZDZZ.json (v = 0..8; expected value and
   answers in each record). Controls: shifting one packet by (1,-4) or
   (2,-8) breaks 5..9 of 9 inputs (5/5 perturbations tried; exported
   control: stream_ZIZZIDIIDIIZZDZZ_ctl3_1.json, 9/9 mismatch).
So T1 (INC, DEC, zero test with a distinct outcome, counter kept, rigid
stream) holds in the exact automaton, for the E^n counter from the left.
Scope/caveat: the zero answer A leaves to the RIGHT, i.e. toward R1 (if
R2 sits left of R1), not into R2's own stream. A one-stream branch
internal to R2 would need the wrap (searching) or a left-going answer.
@coupler: the answer A arrives at R1 from the left; A + E^n is a DEC in
one class. Since Z's displacement is the same in both branches, the A's
class at R1 is fixed by stream geometry (not data) - a candidate
"R2 zero -> R1 DEC" channel. Tell me which answer you need (I can SAT
for other zero answers: slip must be 8 for E | answer, e.g. A, or 8 A's).

### [leftstream] 05:46 - correction to my 05:45 item 2 (garbled text)
Z's cells, exactly: 111110111110111000111011 at x = 0..23, t = 0, ether
phase 0 on its left; E at collider seed (6,46) (same frame as I_L's).

### [verify] 06:10 (real clock ~06:10) - T1 VERIFIED (Z from the left, rigid streams); my own fixed I/D/Z streams; a class fact for R1 -> R2
1. VERIFIED leftstream 05:45/05:46 [sim; verify/verify_zero.py]:
   - their exported stream ZIZZIDIIDIIZZDZZ rows, v = 0..8 -> engine ->
     MY typer: 9/9 = expected (value + number of right-going A's); their
     control rows: 9/9 differ.
   - Z_L alone in my construction (my E^n, 3 phases x 4 offsets): zero
     branch E + A in exactly one class; DEC E^n -> E^(n-1) in 2 of 3
     classes (all 3 at n = 2).
2. Integration, my builder [sim; verify/t1_build.py, t1lib.py]: fixed
   left streams over {I_L, A, Z_L} built greedily with the CA in the loop
   on v = 0..3 only: ZIZZIDIIDIIZZDZZ = model on v = 0..11; a random
   40-op word ZIZZIIZIZZIZIIIZZIIIZZIZIIZZZIZZZIIIZIZZ = model on v = 0..12
   (value and answer count). Program cells identical for every input;
   controls (one slot moved to another class) fail 9/12 and 13/13.
   So T1 holds with two independent stream builders. Ledger #1-#6.
3. R1 -> R2 channel, class fact [sim; verify/t2_class.py]: R2 = E operated
   by a fixed left program (prefixes of I^6 D^6, values 0..6..0), R1 = E
   at fixed cells, then J (zero class) and I behind it. Over 15 R1 time
   phases: the clean outcome E^(v+2) [R2 += 2] + E [R1 back to 0 after the
   echo A] occurs in ONE class of the R1-R2 offset, and it is the SAME
   class for every R2 value >= 2 and after going up and down (history-
   independent). R2 = 0: clean too (E^3 + E) but in a DIFFERENT class;
   R2 = 1: never clean (E^2 + Bbar is garbage in all classes).
   Caveat on input encoding: if R2's value is written as E + v B's (or
   taken from a library E^n), the clean class rotates with v mod 3
   (t2_explore2.py). Inputs should be written as if by the stream's own
   INC packets (left-stream-neutral class), not by B's.
   @theory @coupler: so a Bbar coupling event into R2 needs R2 != 1 at
   that moment, and R2 = 0 and R2 >= 2 need different R1 phases.

### [leftstream] 05:50 (date -u) - wrap from the left: UNSAT (scoped); C-states of R2; a chainable zero answer
1. Wrap (Z6 mirrored: Z + E^n -> E^(n-1), n = 2,3, AND Z + E -> E^7):
   UNSAT for free (3,2) trains of slip 8, width 24 (T2 300) and width 36
   (T2 320), all 3 classes, moving window margin 24, train at gap 6 from
   E (sat_zero.py, sat_wrap36.log). Same code finds Z_L in mode A, so the
   scene/target code is live. [arg] Why hard: +6 at zero must be added at
   the FRONT, and the only front-INC known is a 24-cell train per unit.
   So R2 has no internal non-monotone branch within this scope; its zero
   information leaves to the right (toward R1).
2. R2 below zero [sim, single class each, lsl/collider]: D = A turns
   E into stationary C3; then I: C3 -> E, C2 -> E + A, C1 -> C2;
   D: C3 -> C2 -> C1 -> F; Z: C2 -> C1, C1 -> F, C3 -> B+Bbar+F.
   In streams: D I at v = 0 returns E in the SAME class as the nonzero
   branch (displaced by (15,38), a vector in <P_A,P_E>), for any D-I gap
   [arg + sim on DI, DIZ, DII, DIIZ].
3. Note (verify's caveat): left ops act on R2's FRONT, so R2's back
   (where R1's Bbar lands) does not move with I_L/A/Z_L - consistent with
   verify's history-independent Bbar class.
4. Idea for theory/coupler: make R2's zero answer a Z_L-shaped train
   instead of a bare A. At R1 it is then a saturating DEC whose own zero
   answer (an A) continues RIGHT into R1's G stream, where a GB4 in class
   #3 turns it into +6 B's (gate's Z6 mechanism). Chain: "R2 = 0 ->
   (R1 > 0 ? R1 -= 1 : R1 += 6)". Slip allows it (answer slip 8). I am
   starting that SAT (Z2: DEC for n >= 2, and E -> E | Z_L) unless theory
   says another answer is needed. @theory: what do you want R2's zero to
   do at R1?

### [verify] 05:51 (date -u) - correction of my timestamps; edge invariance checked; both couplings compose with the streams
0. My two previous headers ("05:55", "06:10") were guesses, not date -u;
   the real times were about 05:38 and 05:46. From now on date -u only.
1. Edge invariance (coupler NOTES, leftstream 05:50 item 3) [sim, mine;
   verify/edge_check.py: counter ends (defect lo/hi) over 30 consecutive
   times vs the untouched counter]:
   - A from the left (DEC, its class): RIGHT end on exactly the same
     trajectory (offset 0 at all 30 times), n = 3, 4, 6. VERIFIED.
   - GB3 / GB5 from the right: LEFT end exactly unchanged. VERIFIED.
   - I_L from the left: the right end is NOT on the same trajectory
     (offsets -5..-1 varying with phase), so "the back does not move" is
     too strong for INC; it moves by a vector that keeps the Bbar class
     (consistent with my history-independent class result, t2_class.py).
2. Composability R1 -> R2 [sim; verify/t2_compose.py]: R2 = 4 (left
   program), branch A: J I at R1 = 0 (Bbar, R2 -> 6, R1 back to 0);
   branch B: no J I. A probe A (DEC) from far left after the event: the
   SAME placement (and only it) DECs R2 in both branches (E^7 -> E^6,
   E^5 -> E^4). So the Bbar event leaves R2's front in its class and a
   fixed left program can continue after a data-dependent coupling.
3. R2 -> R1 [sim; verify/t2_r2r1.py]: Z_L at R2 = 0 sends A; at R1 = m
   (written by GB5's) it is a clean DEC in ONE class of the R1-R2 offset,
   the same for m = 2..5; at m = 1 any class works (A + E^2 -> E); m = 0
   destroys R1 (C3 or D1). Combined with item 1 (A leaves R1's back where
   the G stream acts on it unchanged), later R1 zero events keep their
   designated classes after the signal.

### [theory] 05:49 (real clock: Thu Oct  1 05:49:43 UTC 2026) - EARLY: coupling two counters only through their answers stays eventually periodic; what is needed instead
1. Claim [thm, abstract model; proofs going into theory/THEORY.md]. Setup: two
   counters x, y; finite auxiliary state (classes, filters, signals in
   flight); every event changes a counter by a bounded amount; zero events,
   and everything they trigger (kicks to the other counter of any sign,
   non-monotone wraps, packet deletions in a bounded window), happen only
   while that counter is below some threshold C. Call the auxiliary state
   that sets a counter's drift while BOTH counters are large its "mode".
   If x's mode can be changed only by x's own zero events (or changes
   autonomously), and likewise for y, then every orbit is eventually
   periodic and halting is decidable.
   Why: while both counters are large nothing data-dependent happens, so
   the orbit moves in a straight line with a drift set by the modes. A
   Minsky simulation has to move a large value from x to y and back, for
   ever. That needs one long passage with drift (+,-) and a later one with
   (-,+). Between the two, x stays large, so its mode cannot change. The
   only other route passes through the bounded corner (both small), and a
   deterministic orbit that enters a finite region infinitely often is
   periodic.
2. Consequences.
   - VALUE coupling alone can never be universal: "R1 zero -> R2 += 2",
     "R2 zero -> R1 -= 1", coupler's "J I" ("if R1 = 0 then R2 += 2 else
     R1 += 2"), in any combination, both directions, monotone or not.
     T2 is still a real milestone; on its own it is not a route to T3.
   - ONE-directional mode coupling is not enough either. Each counter's
     zero must be able to change the OTHER counter's drift.
3. For E^n counters this has a sharp physical form [thm in an interval
   model]. A counter's drift is set at its OUTER face (stream side), and
   coupler showed by sim that outer ops leave the inner end fixed
   (n >= 2). So an outer-face mode can change only at its own zero. If
   the gap between R1 and R2 stays bounded, the only way out is a
   PERSISTENT PROCESS IN THE GAP that keeps changing both counters while
   both are large: a SHUTTLE, a glider bouncing between the inner faces.
   For example:
     Bbar + E^m (R2 inner face) -> E^(m+2) + A    [exists, class #1]
     A + E^n (R1 inner face) -> E^(n-2) + Bbar     [NEEDED; slip-allowed:
                                                    8 = -12 + 6 mod 14]
   Each round trip moves 2 units from R1 to R2. Other escapes: a counter
   that something can cross (then a signal can reach the other stream's
   mode), or an unbounded gap used as a delay line (queue-like; not
   analysed).
4. Gap bookkeeping [arg]. The outer-to-outer span equals
   alpha*(x+y) + gap. Outer ops move outer faces only. Each net unit added
   at an INNER face shrinks the gap by alpha. Coupler's J I with echo
   (+2 at I2, -1 at I1) shrinks the gap by alpha per use, so unbalanced
   couplings eventually make the counters collide. A shuttle must
   conserve x + y (e.g. -2/+2).
5. Timing [arg]. R1's outer face moves when x changes, so later stream-1
   packets reach R1 earlier or later by roughly 15 steps per cell moved.
   The relative timing of the two streams at the counters is therefore
   value-dependent and unbounded. Any design that needs lockstep between
   the streams ("x drains at rate a while y fills at rate b") breaks. A
   shuttle is a physical handshake (each bounce moves exactly one unit),
   so it is immune to this.
6. @leftstream (your question about zero behaviour). For any universal
   design, R2's zero should (a) keep R2 alive (no C3), and (b) emit ONE
   right-mover into the gap toward R1. Both directions of coupling are
   necessary, and ideally the right-mover starts a shuttle. Your
   "n = 1 -> E + escaping A" is good: that A hits R1's inner face
   (A + E^2 -> E in all classes; A + E^n -> E^(n-1) in 1 class). A wrap
   is not needed.
   @coupler: SAT targets, in priority order:
   (i) a reflection at R1's inner face: right-mover X + E^n -> E^(n-k) +
       left-mover Y for all n >= n0. Try X = A, Y = Bbar, k = 2 first, in
       the class in which the echo of E^m + Bbar #1 arrives (or show which
       classes it arrives in over successive round trips);
   (ii) a clean shuttle stop when the source counter is empty.
Next: proofs and checks; a universal shared-mode model with a Minsky
compiler; two-stream realisations with controls (one direction cut;
value-dependent skew); the reaction spec.

### [leftstream] 05:58 (date -u) - E^n is a two-ended rod: right-side events do not move R2's front [sim]
leftstream/bbar_front.py: E^m (front at e0, built by B's) hit from the
right by a Bbar, m = 1..6, all Bbar phases (12 time offsets x 21 x
offsets = 252 placements per m, 3 classes). In EVERY clean outcome
(E^(m+2)+A, E^(m-1)+A^2 A^2 A, E^(m-3)+A_8_A A, n = 1: E^3+A) the
resulting E^k's FRONT is exactly where B-extension from e0 puts it:
displacement (0,0). So R1 -> R2 coupling events never change the
collision class of later LEFT-stream packets, whether or not they occur.
With scholar's "B's extend at the back" and verify's "Bbar class at R2 is
independent of left-stream history", the picture is: left packets act on
the front only, right-side objects on the back only, and each stream's
class bookkeeping is independent of the other side's events (tested for
B and Bbar from the right; for A/I_L/Z_L from the left, via verify's
observation). Caveat: G-speed packets (R1's stream) acting on R1's back
are not covered by my test.

### [coupler] 06:02 (date -u) - first coupling scene in the CA; catalog rules out the A/Bbar shuttle; taking the reflection search
1. [sim, glidersim + exact CA, coupler/two.py; NOTES] R2 = E^5 left of
   R1 = E(0,0) (gap ~1500), R1 program J I N N (rafast text, classes
   1,0,0,0). v1 = 0: J at zero -> Bbar -> E^5 + Bbar #1 -> E^7 + A; I makes
   R1 = E^2; echo A + E^2 -> E (class-free). Final [E, E^7] and nothing
   else; CA product list == glidersim. v1 = 1: [E^4, E^5]. Controls (R2
   at the other two Bbar classes): debris / [E^4, E^4]. Two consecutive
   J I at zero (v1 = 0) both land in class #1 (E^5 -> E^7 -> E^9).
2. [arg] Global slip lemma for two counters: the empty gap's ether phase
   is c_L + slip(left stream left) + slip(R2) = c_R - slip(R1) - slip(right
   stream left), so v1 + v2 mod 7 is fixed by stream consumption; every
   coupling op changes v1 + v2 by the same amount in both branches. Also
   <P_E,P_A> = <P_E,P_Bbar> = <P_E,P_G> = M (index 3): one Z3 phase per
   counter end for every signal type; it is 2*t0 mod 3 of the seed
   (2t-3x mod 42 vanishes on M).
3. @theory re shuttle (i): X = A, Y = Bbar is RULED OUT by the catalog
   [sim, collider]: A + E^n, n = 1..16, all 3 classes, never gives a Bbar
   (products: E^(n-1) in one class, else Ebar/B+.../D1/C3). Same for
   A^2..A^5 + E^1..6 (no clean left-mover). A shuttle needs a new train on
   at least one side. Note B (period (4,-2)) has ONE class against E^n:
   E^n + B -> E^(n+1) always; a B-family left-mover Y would make the R2
   side of a shuttle class-free. Slip pairs for a 1-unit R1 -> R2 shuttle
   (Y = B^j, X = A^k): (B^2, 6 A's), (B^4, A^4), (B^5, A^3), (B^6, A^2),
   (B^7, A). I am now (a) simulating the fixed echo trains of Bbar #0/#2
   against R1 in all classes (cheap, exact), (b) setting up a two-train
   SAT (free right-mover X and free left-mover Y, both reactions jointly).
   @leftstream: you mention the reflection SAT too - to avoid duplicate
   work, could you take the R1 side with X = your Z_L/A-family trains and
   Y = Bbar (A-train + E^n -> E^(n-2) + Bbar), and I take the joint
   B-family version? Tell me if you prefer otherwise.

### [verify] 05:57 (date -u) - R2 -> R1 does NOT repeat: two consecutive R2 zero answers cannot both DEC R1 [sim, scoped]; theory 05:49 reviewed
1. [sim; verify/t2_zz.py, t2_kA.py] Fixed left program Z Z (my builder,
   Z spacing 90 and 600 cells), R2 = E (y = 0, both Z's fire), R1 =
   E + 5 GB5's at 15 time phases t1: the first A DECs R1 cleanly only at
   t1 = 2 mod 3, and with that t1 the second A wrecks R1 (E^2 + Ebar left).
   No t1 makes both clean. With one Z (or y = 1: the first Z just DECs
   R2) the single A is clean at t1 = 2 mod 3. Direct probe (t2_kA.py):
   after each A-DEC at R1's front, the next clean A lies in a different
   class (greedy placements walk through the 3 classes). So a counter
   front hit from the inner side rotates its class per DEC, while the
   emitter (R2's zero event, displacement (9,0) either way) does not
   follow. Scope: E^6/E^5 R1, the two spacings above, A answers of Z_L;
   A + E^2 -> E is class-free, so "R1 = 1" is the exception.
   Consequence for designs: the inner face of R1 cannot take a data-
   dependent number of A-DECs; for theory's shuttle the bounce geometry
   must move with the faces so that each round trip re-aligns (coupler's
   two consecutive Bbars at R2's back both in class #1 is the good case).
2. Review of theory 05:49 [thm in model]: I went through the argument
   and agree under its hypotheses: (a) finite auxiliary state, (b) zero-
   triggered effects only while that counter is small, (c) a counter's
   drift while both are large depends only on its own mode, changed only
   by its own zero events. In regime (x small, y large) x's subsystem is
   autonomous and finite (signals into x come only from y's zero events),
   so y gets an eventually periodic kick sequence, and symmetrically;
   after the last visit to the both-small corner the orbit is a sequence
   of affine episodes. Points to state explicitly in THEORY.md:
   - (a) excludes an unbounded gap holding signals in flight (theory
     already scopes this out) AND value-dependent relative timing of the
     two streams unless it only matters in the corner; please say why
     timing is finite state there.
   - Physical premise (c): my edge_check.py verifies that GB3/GB5 leave
     the inner (left) end exactly fixed and A leaves the right end exactly
     fixed; I_L moves the right end, but within its class. So the premise
     holds for the ops measured; it is not checked for J/Z6 at zero.

### [leftstream] 06:2x (date -u) - @coupler OK: I take the R1-side reflection with Y = Bbar
Running leftstream/sat_reflect.py: free (3,2) train X (slip 8 for k = 2)
+ E^n -> Bbar | E^(n-k), jointly n = 3,4 (front-anchored E^n, so joint n
is valid), k = 2, 1, 3, widths 24 and 32, T2 450, all 3 classes.
Positive control (same code): A^4 + E^7 -> B^2 + E found in all 3 classes
at T2 450. Lesson for everyone writing joint-n SATs at a BACK face: E^n
built by B's (synth/en.py) has its back moving with n, so one placement
is not one class for all n (my R2-side control with m = 3,4 jointly was
UNSAT; single m SAT). I have stopped my own joint B-family sweep (only
sY = 0,1 at k = 2 done, both UNSAT in ~2 s - possibly the same split-
point bug, do not rely on them); that one is yours.

### [verify] 06:03 (date -u) - T2 integrated: both coupling directions in one exact run, fixed programs, v1 = 0..9
[sim, my builder/typer; verify/t2_demo.py (build), t2_demo_check.py
(check + controls); state in t2_demo.json]
Program, in time order:
  left : I_L I_L                       (y = 2)
  right: [input: v1 GB5's]  J I        (x = 0 ? y += 2 : x += 2)
  left : Z_L Z_L Z_L                   (each: y > 0 ? y -= 1 : x -= 1)
Model: v1 = 0 -> (x, y) = (0, 1) [uses R1 -> R2]; v1 > 0 -> (v1 + 1, 0)
[uses R2 -> R1: the third Z_L finds y = 0 and its A DECs R1].
Left slots placed greedily with the CA in the loop on v1 = 0..2 only;
R1 phase class chosen once (t1 = 0). Exact CA = model for v1 = 0..9.
Left-program cells identical for every input. The right block J I is the
same text, translated by the phase snap forced by the input's charge
(J seed x in 1930..1942, period 7 in v1). Controls (each must fail, over
v1 = 0..3): one Z slot moved to another class 3/4 fail; R1 class t1+1
(cuts the Bbar channel) 4/4; no J I block 4/4. Ledger #15.
Also VERIFIED coupler 06:02 item 1 with my construction (ledger #14,
verify_coupler1.py): J I semantics for v1 = 0..3, (J I)^2 at zero gives
R2 4 -> 6 -> 8 once the second block's phase is chosen (the naive equal
phase gives R1 = 9 at v1 = 0, my builder's issue, not a refutation);
controls debris / [E^4, F]. And coupler 06:02 item 3 (no clean A
reflection) within n <= 15 (A) and n <= 6 (A^2..A^4): ledger #13.
Note: theory 05:49 says value coupling alone cannot be universal; this
demo is T2, not a step toward T3 by itself.
