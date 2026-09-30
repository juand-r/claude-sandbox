# architect: running log

## Plan
- [x] Read project docs (README, REPORT, NOTES, DIRECTIONS) and board.
- [x] Physical intuition: pairwise collisions via collider's enumerator
      (`cat_pairs.py`), placement helper `rx.py`.
- [x] ARCHITECTURE.md: candidates, primitives, choice; board post.
- [x] F-memory register: crossing counter INC/DEC/NOP, fixed stream (zero TEST open).
- [x] Bidirectional transport: F lane (order-independent, one messenger in flight).
- [ ] Stream control (skip): not started (scholar/collider: soft/hard gates).
- [ ] A controlled branch on gliders: blocked by the zero test.
- [x] Final board post (FINDINGS.md refused by harness; results in NOTES/ARCHITECTURE).

## Log

03:00 Wrote a quick glider zoo (random seeds). Superseded by collider's
library (Martinez strings, verified); moved my scratch to trash/.
My first harness also had a wrap-seam bug (phase mismatch at the cyclic
seam spraying debris); collider's build_row makes the wrap clean. Lesson:
use the shared library for row building.

03:20 Pairwise collisions with C gliders (collider's enumerator):
A/B vs C1-3 have one class each; they form a "ladder":
A: C3 -> C2 -> C1 -> F(out); B: C1 -> C2 -> D1(out), C3 -> E(out).
A + B -> nothing; A + D1 -> C2. Mailbox: C2 stores an A as C1.

03:35 Obstruction observed: no right-mover crosses any C (A, A2-A4, D1,
D2 x C1-C3: 18 pairs, 0 crossings); no fast left-mover crosses E or Ebar
(B, Bbar, Bhat, G: 0 crossings). Checked against collider's full catalog
(collisions.json, 718 collisions). All crossings in the catalog: A-Ebar
4/6, A-G 1/9, C1-Ebar 2/4, C1-F 1/2, C2-Ebar 1/4, C2-F 1/2, F-B 1/4,
F-Ebar 7/12.

03:50 KEY OBSERVATION: F (velocity -1/9) is crossed from both sides:
by C1/C2 (which, in F's rest frame, move right at +1/9) and by Ebar and B
(which move left). So data stored in F gliders is bidirectionally
transparent. The geometry that makes it work is three speeds:
stream (Ebar, -4/15) faster than memory (F, -1/9) faster than messengers
(C, 0). Commands overtake the memory from the right; messengers are left
behind by the memory, i.e. they "move right" relative to it and are later
met by the stream (the way Cook's leaders meet tape data).

Verified: a train of 3 F's (seed gaps g) drifting over a stationary C:
C1 passes cleanly iff g = 15 mod 28 (43, 71, 99, 127 tested), C2 iff
g = 1 mod 28 (29 tested). Predicted from the single-crossing displacement
vectors (C2 + F#1: C2 moves (4,13); C1 + F#1: C1 moves (0,15)) before the
runs. On a train of the "wrong" gap, C1 destroys one F and turns into C2
(C1 + F#0 -> Ebar + C2): the train is a C1/C2 filter.
- Lesson: never pkill -f from a shell whose command line contains the pattern (killed my own shell twice, lost a heredoc file); kill by PID.

(Note: the harness refused to let me create FINDINGS.md ("subagents
return findings as text"); verified results are logged here and on the
board, and will be in my final report. The lead may want to create
FINDINGS.md from them.)

~07:00 Crossing algebra predicts train transparency: for each F x Ebar
clean class k, train vector G = -e_k mod <P_F,P_Ebar> is crossed cleanly
(all 7 classes, several G). Joint C2+Ebar design (C2xF#1, FxEbar#8,
C2xEbar#2) was pairwise-consistent but FAILED 12/12 timings
(m1_robust.py): three-body order dependence.

~08:30 yb3.py: two event orders for M < F < S; require same classes in
both. Unique solution: C1xF#1, FxEbar#3, C1xEbar#1 (+ correct sub-lattice
offset between C1 and Ebar; found the offset b=1 experimentally, it is
G mod L_CE for a 4-F train). First version failed because my "incoming"
C1-Ebar class ignored the F's between them (ether slip) - fixed.

~09:15 m1_yb.py: 20/20 clean over messenger timings a = 0..38.
m1_predict.py: final seeds = initial + sum of displacements EXACTLY
(a = 0, 20, 38); census: 16 E + 1 C + 4 defects invariant under (36,-4)
(census.py has no F family). Bug found on the way: my seed normalisation
had the wrong sign (x - q*d is right).

~10:15 palg.py, winding.py, winding2.py: crossings alone cannot pump a
two-marker register (no winding; table in board post). Scholar's +-6
C1-pair register is a 2-residue (1-bit) system.

Current design questions: addressing (single-glider commands cannot pick
one lane object among others), answer latency from deep stores.

~12:00 multibody.py: 8 of 181 F x (Ebar pair) collisions are genuinely
multi-body (F displacement != sequential prediction). winding3.py (uses
collider predict.py): with pairs, 181 winding transitions. Shortest
cycles (3 packets) = INC (gap +9.33) and DEC (-9.33).
xcounter.py long: INC^1..6, DEC^1..6: 12/12 exact. Earlier failure with
packets 6 F-periods apart was mover interference; 20 periods is clean.
DEC at n = 0 is also clean (goes to n = -1, gap 33.67).

~13:00 Balanced drift: T-drift mod L_FE: INC (4,10)/12, DEC (9,6)/12,
lane Ebar f3 (5,8)/12, identity mover c = pair(-1,25)@(-17,67) (10,10)/12.
INC + lane = DEC; NOP = c + 7 lanes = DEC. Equal drift mod L suffices:
a lattice difference in T's true position only translates collisions
by periods (predict.py's translation rule).
xstream.py: FIXED stream (slot j at j*delta, placement independent of
history), 6 random 8-instruction programs of INC'/DEC/NOP: 6/6 exact.

~13:30 Below zero: DEC from n=-1 leaves the F's as a close compound
(F_19_F, gap 19) with only Ebar debris; DEC^3 from 0 explodes. Plan:
value 0 := n = -1; DEC at 0 -> abnormal compound; a PROBE packet should
restore gap 33.67 and emit a messenger (probe_search.py running, the
only heavy job, per the lead's CPU request).

~15:00 Zero state found by accident: DEC from gap 33.67 gives the close
compound F_19_F, and it behaves like a legitimate value:
  DEC,DEC,INC -> gap 33.67 again (exact D (-12,35)); DEC,DEC,INC,INC ->
  gap 43 (D (0,43)); DEC,DEC,NOP -> compound unchanged; all 17 identity
  movers pass the compound unchanged. Only DEC on the compound explodes.
So: value 0 := compound F_19_F, value k >= 1 := gap 33.67 + 9.33(k-1).
The register now has a distinguishable zero state; what is missing is a
TEST packet: identity on separated pairs, messenger on the compound.
probe_search.py (2 F's + messenger from the compound) found only E-based
movers (which also react with normal F's); aborted the pure-Ebar run
(many 'unsettled' because a stationary messenger with Ebar debris to
its right never 'settles' - classifier bug, fixed in zc_search.py by
recording products regardless). zc_search.py running (only heavy job).

~16:00 zc_fast.py (fast: bare compound + one mover, same process builds
the compound so auto-registered names agree; lesson: auto names like
F_19_F#3 are process-dependent). 660 pure-Ebar movers vs compound: no
clean TEST; outcomes listed on the board. Spec Z2 posted for synth with
zero_state.json.
~16:45 cpump.py: stationary C PAIRS crossing an F pair from the left DO
wind (19 winding transitions over 95 pair movers, residues mod L_FE), so
the upstream register can in principle be pumped from the control side.
Caveat: stage() simulates T and P crossings separately (valid only for
large gaps); used C's end up as stationary debris in the stream's path.

~18:00 Zero test, stages 5-6 (ztest3.py, ztest4.py): 1285 two-packet
sequences are exactly the identity on separated pairs (catalog
prediction). On the compound, 705 leave it unchanged, 559 split it into
two separate F's: 545 at gap 24.33 in the STANDARD residue (i.e. the
separated n = -2 state: a second representation of zero), 14 at gap
33.67 in a different residue ("marked"); no sequence emits a messenger
without right-movers. Single-packet splits to residue (19,23) exist, and
on that residue the identity packet pair(-1,25)@(-14,55) makes P emit
C1 + C2 (P survives, B^2 leaves to the left): the messenger reaction we
want, but the split packets are not identities on normal pairs.
Status: clean zero test NOT found; handed to synth as spec Z2.
xcensus.py: census of a fixed-stream run (INC,INC,DEC,INC,NOP,INC):
42 E-type defects (packet debris), 2 '?' defects that are exactly
(36,-4)-invariant (the F's), gap 71 = n 3. PASS.

~19:30 More zero-test data:
- Separated pair at gap 24.33 (standard residue, "n = -2"): INC works
  exactly from it (two INCs -> gap 43). DEC destroys it: one A to the
  right, B^3, B^3, E, E^2 to the left (a destructive zero answer).
- xstream2.py (DEC' = DEC + S1 split packets, balanced padding): in the
  fixed stream the zero state comes out as another compound, F_12_F, and
  INC from it is exact; DEC at F_12_F scatters (A, D1, C1, F, F, ...).
- ztest5.py: all 17 single and 1285 two-packet identities applied to the
  separated zero: 1107 collapse it cleanly into compound F_18_F, 14 move
  it cleanly, the rest scatter with right-movers. No messenger without
  right-movers.
Conclusion: the zero STATE is a family of close compounds (F_12_F,
F_17_F, F_18_F, F_19_F, ...) connected by clean single-packet moves, INC
leaves it cleanly, but no packet or 2-packet sequence found reads it
cleanly. Synth's SAT (spec Z2, zc.py) had 7 UNSAT instances (slips 0-6,
class 0, width 24) at 19:20.

~20:00 m1_multi.py: lane with THREE C1 messengers (spacing chosen so
each F and each Ebar meets the next messenger in the lane class after
crossing the previous one): 0/5 clean (F's destroyed, E/E^2 debris). So
the lane is verified for ONE messenger in flight at a time; several
messengers need a correct incoming-class analysis (probably the same
sub-lattice subtlety as the b=1 offset). Open; the architecture only
needs one messenger in flight per register.
