# Route map: universal non-CTS computers in Rule 110 (round 4)

Author: theory (round 4). Living table; status labels:
- **closed [thm]**: ruled out by a theorem, inside that theorem's stated model;
- **blocked [sim]**: the needed reaction was searched for and not found, in a stated scope;
- **open**: nothing known for or against;
- **promising**: needed pieces partly exist, and no theorem stands in the way.

Theorem numbers: R2-* = round2/verify/THEORY.md, R3-T1/T2 = round3/theory/THEORY.md,
R4-* = this round's THEORY.md. "Needs" lists what the PHYSICS must supply.

## 1. The table

| # | route | needs from the physics | theorem that applies | status | owner |
|---|---|---|---|---|---|
| 0 | Cook's CTS (reference) | queue tape read at one end, written at the other | - | excluded by the goal | - |
| 1 | one stream-driven counter (any encoding, incl. 2^a 3^b "two counters in one") | INC/DEC/test from one periodic stream | R2-s5 one-counter ceiling: decides only ultimately periodic sets | **closed [thm]** | - |
| 2 | several counters along one stream, each operated at its own place | answers that cross upstream stores | R2-s3 feed-forward; R2-s3.1 drifting lane | **closed [thm]** unless near-end (row 7) | - |
| 3 | clean (monotone) answers, any layout | - | R2-s2 chain machines decidable | **closed [thm]** | - |
| 4 | two E^n rods, two streams, coupled through zero answers (values) | kicks, wraps, deletions near zero | R3-T1 (owned mode), R3-T2 (rods) | **closed [thm]** in the rod model | - |
| 5 | (4) + shuttle between the inner faces | reflections X+R1 -> R1-a + Y, Y+R2 -> R2+a + X, class-consistent over round trips; start/stop at zero | escapes R3-T1 (shared mode) | **blocked [sim]** (joint SAT W <= 30, library scans); open beyond | shuttle |
| 6 | (4) + crossing of a rod, BOTH directions | right-movers and left-movers through E^n with state-dependent outcome | R3-s3.5: one direction is not enough | **blocked [sim]** (W <= 24-30); verify 23:02: cone bound cannot exclude it | objects |
| 6b | (4) + wall-driven pump at R2's back | converter: wall + B -> B + X (one unit) | gives y -> x exactly; x -> y still rate-matched | **blocked [sim]** (parked E, Ebar, E^2-4) | objects |
| 6c | (4) with drift set by CLASS (packets whose effect depends on the rod's class; walls change class) | class-dependent clean packets; walls that rotate the back class | R3-T2 still owns R2's front: only R1's mode becomes coupled | **closed [thm]** alone; useful only with 5/6/6b | - |
| 7 | **near-end lane**: one stream crosses stores; all operations and zero tests at one control point; answers stationary at that point | stores crossable by the stream (F lane: Ebar x F; lab frame: Ebar x C1/C2); kicks of markers; zero test with answer at the control point; abort OR a mode flag (R4-s4) | escapes R2-s3 and R3-T1 (shared control point) | **open**, partly built (address: 2 F registers); blocked on abort-eats-kicks (gate, SAT W <= 30) | queue? / objects |
| 8 | gap as an unbounded register (window rod; one signal in flight) | a window rod that survives echoes; echo timing as zero test; blocking emission while an echo is pending | violates R3 premise (B) | **open** | delayline |
| 9 | gap as a delay line (many signals in flight) with genuine finite control | write/read of a signal train; control that persists across reads | queue machine: not CTS iff control is genuine | **open** | delayline / queue |
| 10 | queue automaton (Post machine) on Cook's tape | state-dependent leader (accept vs reject leaves different prepared leaders) | R2 queue: leader SAT UNSAT W <= 36 | **blocked [sim]** in scope | queue |
| 11 | direct 2-tag (symbol selects the appendant) | same as 10 (the read must outlive one appendant) | - | = row 10 | queue |
| 12 | **phase-free particle TM** (Lindgren-Nordahl / Durand-Lose TM signal machine): stationary cells = tape symbols, head = rigid packet on the A or D lattice (moving right) or B lattice (moving left); NO streams; periodic blank tape | one clean reaction h_q + c_s -> c_s' + h_q' per used (state, symbol, arrival side); cell positions restored up to a potential (R4-L2) | R4-L1: every head-cell collision is single-class, so NO timing bookkeeping; none of R2/R3's theorems applies (no stream, no counters) | **promising** [sim census: clean head steps exist, incl. reflections both ways and pass-throughs] | theory (census, model) -> objects (SAT) |
| 13 | finite seed version of 12 (no periodic background) | 12 + a border object that extends the tape | Durand-Lose 2013: rational 3-speed signal machines are cyclic; Rule 110 heads use 3 speeds (A or D, 0, B) but the TEMPLATE needs the border, i.e. a 4th signal, or a gun | **open**, strictly harder than 12 | - |
| 14 | signal-machine 2-counter (Durand-Lose 2005): counters = distances, a zig-zag head | marker-preserving reflections (same as 12) + marker moves | needs >= 4 speeds from a finite seed (have 8) | **open**, dominated by 12 | - |
| 15 | one register with multiplication (Minsky; FRACTRAN): a length scaled by speed ratios, residues read by collision class | marker-preserving reflections; exact scalings x2, x3 (or any 2 coprime); residue tests mod 2 and 3 | none closes it; residues are only those of the lattice | **open**, dominated by 12 | - |
| 16 | intrinsic universality / simulating a universal CA | blocks exchanging state both ways every step | Ollinger: open problem | **open**, hardest | - |
| 17 | collision logic (billiard-ball style) with streams as clocks | reusable gates, fan-out, crossing both ways in 1-D | inherits the transport asymmetry (scholar s.3) | **open**, no reusable 1-D gate known | - |
| 18 | switchable gun in the gap as a shared mode | a gun that zero events turn on/off; its emissions INC/DEC both inner faces | escapes R3-T1 (shared persistent process) | **open**; the known gun moves at -20/77, not with E^n (-4/15): it drifts 1 cell per ~140 steps relative to the rods | - |
| 19 | k >= 3 rods in a line | middle rods have no stream | R4-s3 [arg]: middle rods have zero bulk drift; leftmost front owned | **closed [arg]** for the rod model | - |

## 2. Ranking (theory's view, 23:10)

1. **Row 12, the phase-free particle TM.** It needs a finite, program-independent
   table of exact local reactions and no timing arithmetic at all (Lemma R4-L1).
   It sidesteps every no-go we have, because there is no stream and no counter.
   The census already shows that the needed KINDS of steps exist (reflections in both
   directions, pass-throughs, rewrites). The open question is purely combinatorial:
   is there a closed table that is universal? Milestones: a binary counter (5 reactions),
   then a universal TM (about 2|Q||Sigma| <= 72 reactions for the small UTMs).
2. **Row 7 with mode flags** instead of aborts (R4-s4): it changes the missing piece from
   "an eater that eats register kicks" (UNSAT W <= 30) to "a crossable flag that shifts the
   class of later packets".
3. Rows 5, 8, 9, 10 (teammates' avenues) as they stand.

## 3. Literature actually read for this map

See THEORY.md s.7 (what I read, and what each source says that matters here).
