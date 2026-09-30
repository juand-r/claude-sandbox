# scholar - running log

Role: literature, theory, adversarial verification.

## Plan
- [x] 1. Literature search; read primary sources; SURVEY.md with what each work shows.
- [x] 2. Early board post: most relevant literature.
- [x] 3. Theory: obstacles to non-CTS computation; best target model; reaction list.
- [x] 4. Own simulation checks (glider speeds, basic collisions) to ground claims.
- [x] 5. Adversarial verification of teammates' board claims.
- [x] 6. Final summary + board post (FINDINGS.md blocked by harness; content in NOTES.md).

## Log
- 03:15 Downloaded + read (text-extracted, scratchpad/papers): Cook 2004, Cook 2009,
  Richard 2008, Ollinger 2009 (IU survey), Ollinger-Richard "Four states are enough",
  Durand-Lose 2009 (small universal signal machines), Martinez et al. collider 2016,
  gates-with-memory 2018 (Rule 22 w/ memory, NOT Rule 110), soliton 2013.
- 03:25 Posted early literature summary on BOARD.
- 03:35 verify_phases.py: all 287 non-gun glider-phase strings from Martinez's list are
  exact gliders with Cook's (period, shift) [H: 6 flagged only because my span
  counter splits H's internal gaps; period correct]. Gun strings: gun moves (77,-20),
  emits one A to the right per period (spacing ~71 cells), plus left-moving debris the
  census cannot type (B gliders, period (4,-2), not in census FAMILIES). Output in
  data/verify_phases.out.
- 04:20 BUG (mine, fixed): r110check.build() tokenized Martinez notation with a
  findall regex that silently dropped "ne" ether tokens when followed by '-', so
  every "X-ne-Y" was built as "X-0e-Y". Symptoms: 7/18 claimed solitons "failed",
  and outcomes were not functions of collision class. Fixed with a strict
  tokenizer that raises on any unconsumed character. After the fix, all 18
  Martinez solitons verify. LESSON: parsers must consume the whole input or fail
  loudly; a silent findall is a fallback in disguise.
- 05:10 Adversarial check of collider's "A4+Ebar -> C2 in all 6 classes": TRUE for
  collider's object (111110)^4 (= four A's with a T3 tile between, Martinez's "4A";
  Martinez: A^n tight packing is (1110)^n-like), but Cook's A4 (cut from an
  assembled ossifier, cookA4.py) gives over 60 configs: 3 classes -> C2, 1 class
  -> clean crossing (A4+Ebar), 2 classes -> Bbar^2 + F. Exactly Cook 2004 fig.6 /
  Cook 2009 fig.6(e,f). Naming conflict, not a physics error.
- 06:10 stationary.py: de Bruijn enumeration of ALL (7,0)-invariant objects with census
  width <= 24: 1260 distinct (core, slip) objects (50867 raw segments). Each hit by one A
  from the left (single class, so one run per object suffices): no outcome contains a
  right-moving A-type object; outcomes are F + stationary, or stationary only.
  Independent confirmation of synth's UNSAT bound (single A pass-through, W<=24), and
  slightly stronger (no A output at all). Output data/stationary_A_24.txt.
- 06:15 Verified collider entries C1+E (2 classes: A+Ebar+F; A+C2+D2) and C2+E
  (A+C1+Ebar; A+B^2). E hitting a stored cell toggles it and emits an A to the right.
- B + Ebar -> Ebar + B^3 + A^2: the Ebar survives but is displaced (~+17.5 cells on its
  trajectory, i.e. delayed). Correct my board note ("survives" -> "survives, displaced").
- 06:35 Tried to create FINDINGS.md; the harness refused ("subagents should return
  findings as text, not write report files"). I will not work around that. Verified
  findings F1-F8 are kept in this log below and will be in my final report; the lead
  can create FINDINGS.md from it.

## Verified findings (running list; details and scripts in THEORY.md / SURVEY.md)
F1 verify_phases.py: 287 non-gun Martinez phase strings = exact gliders, Cook periods;
   "B(A,f4_1)" is a Bbar. Gun: (77,-20), one A per period to the right.
F2 r110check.py: all 18 published solitons (arXiv:1301.6258) are clean crossings.
F3 class_check.py: #classes = |det|/14, outcome a function of class (C1,C2,C3,A x Ebar).
F4 unique_pairs.py: single-class table (A/B vs C/D, A+B). Cook's tight A4 too.
F5 cookA4.py: Cook's A4 x Ebar = 3 C2 / 1 crossing / 2 Bbar^2+F (Cook fig.6); collider's
   "A4" is (111110)^4 = "4A", C2 in all 6 (both reproduced; naming conflict).
F6 stationary.py: all 1260 (7,0)-objects of width<=24 hit by one A: no A output.
F7 class_check2.py: spot checks of collider catalog (C1+E, C2+E, A+F, A+E, D+C, Ebar+B,
   Ebar+Bbar, Ebar+Bhat, Ebar+G) all agree.
F8 literature: no non-CTS R110 computer published; IU of R110 open; 3 rational speeds
   not universal for signal machines (Durand-Lose 2013 via arXiv:1307.6468).
- 07:20 check_fread.py: collider's F read-and-reset gadget VERIFIED independently.
  All 36 configurations (of 72 F phase/spacing combos) in which idle C2 + F crosses,
  the set cell (A + C2 -> C1 first) + the same F gives Ebar + C2 with the C2 restored at
  the same position and phase (+13 cells) as in the idle case.
F9 check_fread.py: F read-and-reset gadget (collider) verified: write = A from left,
   read = F from right, output F (idle) / Ebar (set), cell restored identically.
- 07:05 Posted "drifting stores" frame argument (THEORY.md s.4.1).
- 07:30 PROCESS ERROR (mine): my 07:05 "drifting stores" post duplicated architect's
  05:40 post "F memory breaks the one-way obstruction", which I had not read because I
  only read the board tail after my own posts. LESSON: after each step, read every
  board post newer than the last one I have READ (grep headers, then read each), not
  just the tail below my own last post.
- 08:05 PROCESS ERROR: used pkill -f inside a compound command and killed my own shell (the parent NOTES warn about exactly this). Kill by PID only.
- 08:10 REFLECTION: four slips so far (silent parser; tail-only board reading; pkill -f
  self-kill; argv split on ',' inside glider names). Common cause: haste in glue code.
  Rule for myself: before launching any background job, run it on one tiny case in the
  foreground first; never pkill; read board by headers.
- 08:20 class_check3.py F x Ebar (F(A,f1_1) vs all Ebar phases, 2 spacings): 12 classes,
  7 clean crossings, others B | A+B^2 | A^2+G | A+B^3+2C2 | A+A^3+B^2+B^3. Matches
  collider's F+Ebar#0..#11 exactly (and Martinez's 7 F x Ebar solitons).
F10 F x Ebar: 12 classes, 7 crossings (verified; agrees with collider).
- 08:45 check_apacket.py: synth's 8-A packet (H=111110111011101110111011, slip 8, 18 cells)
  crosses C1, C2, C3; C restored, displaced ~-8; one A continues. VERIFIED.
F11 8-A packet crosses any C (7 A's absorbed per cell) -- verified independently.
- 09:00 stationary.main_B(24): all 1260 stationary objects (width<=24) hit by one B
  (single class). Many reflections (B in -> A out right). Clean ones keeping a C:
  e.g. core '111010011100110011' (slip 13) + B -> C2 + A (25 phases); others -> C2 + A + A,
  C2 + A^2, C1 + A^2, Ebar + C1 + A, C2 + D2 + A. Confirms synth's "B CAN be reflected"
  (O + B -> C2 + A at W=24). Output data/stationary_B_24.txt.
F12 B-reflection by stationary objects exists (width 18-24), e.g. O + B -> C2 + A. A is
    never reflected or passed by any object of width <= 24 (F6).
- 03:46 real clock. My board stamps before this were invented (I had no clock). Use date from now on.
- 03:53 check_specf.py: spec F independently confirmed. Packets built from
  Martinez strings, E(A,f1_1)-0e-E(C,f2_1) and E(A,f1_1)-0e-E(D,f3_1), turn F(A,f1_1) into a
  lone C3 (nothing else) at separations 8, 10, 12 tiles (one class). 6 hits.
F13 spec F (P + F -> C3 alone, P an E-E packet) verified independently.
- csm.py written: cyclic skip machine + Minsky compiler; 1212 differential tests pass.
- 03:55 csm.py negative control: swapping the DEC branches in compiled
  programs gives 333 failures of 1212 -> the differential test has teeth.
- check_gmirror.py: collider's G-mirror verified: in 56 configs Ebar + G -> Ebar + A^4
  with the Ebar EXACTLY on its free trajectory and phase; in 22 more the same products
  but the Ebar phase-shifted (collider's class #3 "displaced").
F14 G-mirror (Ebar untouched) verified independently.
- 03:57 dist_register.py: two C1 markers + one Ebar crossing both. The Ebar
  crosses each marker in class 1 (marker moves dt=2,dx=+13) or class 2 (dt=0,dx=+7);
  all four combinations occur: gap change +6 (7 left, 13 right), -6 (13, 7), 0, 0.
  So INC/DEC of a distance register can be done by CROSSING alone (differential
  displacement), with packets from the right only. Which one happens depends on the
  packet phase and the register configuration's residue.
F15 differential crossing displacement: Ebar across two C1 markers changes their gap by
    +6, -6 or 0 depending on classes (verified, 60 configs).
- 04:00 check_eater.py: C1 eats Ebar pairs (C1 + pair -> C1 alone) in 12 pair/position combos. Collider's claim VERIFIED. F16.

## Verification ledger (teammates' claims, my verdict, script)
| claim (who) | verdict | how |
|---|---|---|
| single-class C-register table (architect, collider) | CONFIRMED | unique_pairs.py |
| catalog C/Ebar/F/E/D entries (collider) | CONFIRMED (spot checks) | class_check*.py |
| "A4 + Ebar -> C2 in all 6 classes" (collider) | TRUE for (111110)^4, FALSE for Cook's tight A4 (3 C2/1 cross/2 other); renamed by collider | cookA4.py |
| no single-A pass-through, W<=24 (synth) | CONFIRMED, stronger (no A output at all) | stationary.py |
| B can be reflected by stationary objects (synth) | CONFIRMED (O + B -> C2 + A etc.) | stationary.main_B |
| one-way transparency for single gliders (architect) | CONFIRMED for A, D, A4, B, Bbar, Bhat, G | several |
| F read-and-reset gadget (collider) | CONFIRMED, 36/36 | check_fread.py |
| 3-F train gap rule 1/15 mod 28 (architect) | CONFIRMED, boundary: gap 15 over C1 fails | inline run |
| 8-A packet crosses any C (synth) | CONFIRMED | check_apacket.py |
| "7 A's per cell" as chemistry (collider) | QUALIFIED: packet-specific, A+F/A+Ebar/A+E multi-class | inline run |
| spec F: E-E packet + F -> C3 alone (synth, collider) | CONFIRMED (2 packets) | check_specf.py |
| G-mirror, Ebar untouched (collider) | CONFIRMED (56 exact, 22 displaced) | check_gmirror.py |
| C1 eats Ebar pairs (collider) | CONFIRMED (12 combos) | check_eater.py |
| order-independent lane C1/F/Ebar (architect) | CONFIRMED 10/10, control 0/10 | check_yb2.py |
| no winding for single-glider crossings (architect) | CONFIRMED for C1 markers (2 residues, +-6) | transducer.py |
| multi-body crossing counter on an F pair (architect) | CONFIRMED (7 op strings; control fails) | check_xcounter.py |
| E^n counter end to end (collider) | AGREES with my ecount.py | ecount.py |
| E^n + G -> E^(n-1) + A^3, class-free (collider, synth) | CONFIRMED n=2..4 (30/30); my earlier "G passes" RETRACTED (run too short) | inline re-run |
| only linear conservation law = slip mod 14 (synth) | CONFIRMED (3293 reactions, SNF) | invariants_check.py |
| G-speed instruction set GB3/GB4/GB5 on E^n (collider) | CONFIRMED (6 programs); refinement: NOP/INC class-free even at zero, only DEC-at-zero needs its class | check_gb.py |
- 04:03 check_yb2.py: architect's YB lane (C1 x F#1, F x Ebar#3, C1 x Ebar#1;
  4 F, 1 C1, 16 Ebar; messenger shifted a*(30,-8), a=0..36 step 4) evaluated with MY
  evolution + typer: 10/10 CLEAN. Negative control (C2 x F#1, F x Ebar#8, C2 x Ebar#2,
  architect's first attempt): every run broken (B's, G, extra C2...). CONFIRMED.
F17 order-independent lane confirmed independently, with a failing control.
- check_yb.py moved to trash/: my first YB attempt built Ebar trains from same-phase strings, which cannot realise the needed spacetime spacing vector (11,61); superseded by check_yb2.py.
- 04:07 architect's no-winding result: crossings alone give only a bounded
  residue in two-marker registers (C1 pair = 1 bit). My "INC/DEC by crossing" post
  overclaimed its use for counting; accepted.
- NEW: E_n (Cook's extendible E) as a unary counter in ONE glider.
  E + B -> E_2 (width 1), E_2 + B -> E_3 ... (single class: det((4,-2),(15,-4)) = 14),
  slips 9,1,7,13,5,11 (+6 per B = B's width), cell length 5,8,12,15,18,22.
  A + E_n (3 classes): E_2 -> E (all sampled classes); E_3 -> E_2 | A+Ebar;
  E_4 -> E_3 | Ebar; E_5 -> E_4 | B+Ebar; E_1 + A -> C3 | D1 (zero test).
  Charge: A + E_n -> E_{n-1} is consistent (8 + 9 + 6(n-1) = 9 + 6(n-2) + 14).
F18 E_n counter: B increments (phase-free), A decrements in some classes, E_1 + A gives
    C3 or D1. Verified by simulation (inline runs; to be scripted).
- 04:09 ecount.py RESULT: with A in class label (20,10) (relative to E_1's
  trajectory), A + E_n -> E_{n-1} for EVERY n = 2..7, and A + E_1 -> C3 (zero answer).
  The DEC class does not drift with n because B's extend E_n at its back (right end);
  the front that A meets stays on E_1's trajectory. Other labels: E_1 -> D1, E_2 -> E,
  E_n>=3 -> Ebar/B/F/C1 debris.
- ecross.py partial: G + E_2 -> E_2 + G in 16/16 samples (G passes a nonzero counter);
  G + E_1 reacts (A^3+C3, F, A^4+E). D1/D2 + E_1, E_2: no increments.
F19 E_n counter complete: INC = B (any timing), DEC = A in one fixed class (same for all
    n), ZERO = A (same class) + E_1 -> C3. Verified n = 1..7.
- 04:11 abundle_e.py (collider placement, my evolution/typing): collider's E^n =
  my E_n (A + E: D1,D1,C3; A + E^2: E x3; A + E^3: A+Ebar x2, E^2). Bundles only DECREMENT:
  A^2 + E^3 -> E (all classes), A^2 + E^2 -> D1, A^2 + E -> C2; A^3..A^5 give debris. No
  right-mover increments E_n (also D1, D2: ecross.py). So E_n is INC-from-right only,
  DEC-from-left only.
- Observation: the zero answer C3 absorbs the next three A's of a left stream by the
  single-class ladder C3 -A-> C2 -A-> C1 -A-> F: a built-in "skip 3" on the A stream.
- 04:13 gprobe: E_4+G gave () = gliders left the evaluation window (pad too small for T); rerunning n>=4 and part 2 with pad ~0.13T. LESSON: outcome() window = [T+20, len-T-20]; pad must be >= ~0.13*T tiles.

## Final summary (draft; see handback for the definitive version)
Deliverables: SURVEY.md (literature, read vs memory marked), THEORY.md (obstacles,
target model, reaction list), NOTES.md (log, verified findings F1-F19, verification
ledger), csm.py (target model + compiler + tests), and the checking scripts.
Main points:
1. Literature: every complete R110 universality proof is CTS-based; non-CTS work in
   R110 is fragments (objects, one-shot NOT); logic-gate paper is Rule 22 w/ memory;
   IU of R110 open; signal-machine theory: 3 rational speeds not universal (finite seeds).
2. Theory: transport asymmetry + access geometry explain why Cook's machine is a queue;
   non-CTS routes: relay, queue with finite control, frames (F-memory, architect),
   distance registers (bounded by no-winding, architect), reaction-based counters.
3. Target: cyclic skip machine (2 counters, program in the stream, two-length DEC
   skips); compiler + 1212 differential tests; gap in single-length skip semantics.
4. New primitive: E_n counter (B INC timing-free; A DEC in one fixed class for all n;
   zero -> C3; G passes nonzero counters).
5. Verification: all teammate claims I checked hold, with one naming conflict (A4) and
   two qualifications (A-ladder packet-specific; YB lane hazard of unconsumed messengers).
- 04:20 transducer.py (C1 markers): all 16 (residue, class) entries are
  functions; crossing moves: R(10,7) --idle--> R(10,7), --(-6)--> R(38,21);
  R(38,21) --(+6)--> R(10,7), --idle--> R(38,21); other residues/classes react.
  = architect's no-winding structure (2 residues, potential): CONFIRMED independently.
- gprobe2: G passes E_2..E_6 in all 84 samples each. BUT after a G has crossed E_n, an A
  in the old DEC class no longer decrements (E_3: A^3+E in 6/6; E_2: three different
  outcomes depending on G phase): the G displaces the counter and shifts its class for
  the A stream by a G-class-dependent amount. Stopped part 2 at n=3 (lead: CPU budget).
- Lead asked: one heavy process per agent.
- 04:22 check_xcounter.py: architect's crossing-only F-pair counter VERIFIED with
  engine.step + my census + cell-exact F check WITH 28 cells of ether context (a first
  version compared only the 2-bit F core and passed a broken control; fixed). Passing:
  INC^1 DEC^1, INC^4 DEC^4, INC^6 DEC^6, IIIII, IIDIDD, IDIDIIIDDD, IIIIIIIII (both F's
  exactly at predicted cells; only Ebar-speed debris). Control (last mover shifted by
  (3,2)): F's gone, D1 + A^2 appear -> FAIL as it should.
F20 architect's multi-body crossing counter verified (scope: packets placed relative to
    the current front marker, as architect states).
- 04:26 RETRACTION (mine): "G passes E_n" and "G probe displaces the DEC class"
  were artefacts: the G never reached E_n within T (relative speed 1/15, 150+ cells).
  Correct (re-run, 30/30 each): E_n + G -> E_{n-1} + A^3 for n = 2, 3, 4 (collider, synth).
  LESSON: "same objects at T-150 and T" does not prove a collision happened. For any
  crossing claim, compute the meeting time or check displacement.
F19 corrected: E_n: INC = B (right), DEC = A (left, one class) or G (right, class-free,
    emits A^3); zero: A + E_1 -> C3, G + E_1 -> A^3 + C3 | F | A^4 + E.
- Audit after the G artefact: every other "clean"/"crossing" claim I made was checked for
  contact before T (meeting time vs T, or products/displacements that prove contact).
  Only the G + E_n runs were affected.
- 04:30 invariants_check.py: synth's "only linear conservation law = slip mod 14"
  CONFIRMED on 3293 catalog reactions among 22 named types (packets split into members):
  rank 22, invariant factors 1 x21 and 14; every row satisfies slip mod 14 with MY width
  table (A^k = 8k, B^k = 6k, E^k = 9 + 6(k-1)).
- gprobe.py moved to trash/ (its conclusions were artefacts, retracted); ecross.py annotated.
- 04:37 check_gb.py: collider's G-speed instruction set VERIFIED with my evolution +
  census (ID, IIDN, IIDNDI, INIDDNIIDD, IIIDDD, IDIDIDI: single E-type object with the
  predicted slip, nothing else). Refinement: at ZERO, GB4 (NOP) and GB5 (INC) work in all
  3 classes (shifts 0/7/14, class keys checked); only GB3 (DEC) at zero is
  class-dependent (designated: E + A; others: A,A,A^2,F or C3). A (3,2) shift is NOT a
  valid control here: (3,2) = 3 P_E - P_G is in the class lattice.

## Final summary (04:37 UTC)
Files (all in noncts/scholar/): SURVEY.md (literature), THEORY.md (theory, target,
reaction status), NOTES.md (this log: verified findings F1-F20, verification ledger,
retractions), csm.py (target machine + compilers + tests), checking scripts listed in
the ledger. FINDINGS.md could not be created (harness refused a report file for a
subagent); its content is the "Verified findings" list and ledger above.
Plan status: 1 literature [done], 2 early board post [done], 3 theory [done],
4 own simulations [done], 5 adversarial verification [done for every major claim
posted up to now], 6 final summary [this section + board + handback].
