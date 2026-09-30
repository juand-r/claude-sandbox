# architect: running log

## Plan
- [x] Read project docs (README, REPORT, NOTES, DIRECTIONS) and board.
- [x] Physical intuition: pairwise collisions via collider's enumerator
      (`cat_pairs.py`), placement helper `rx.py`.
- [x] ARCHITECTURE.md: candidates, primitives, choice; board post.
- [ ] Register gadget (front register) or F-memory register.
- [ ] Relay / bidirectional transport.
- [ ] Stream control (skip).
- [ ] A controlled branch on gliders.
- [ ] FINDINGS.md + final board post.

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
