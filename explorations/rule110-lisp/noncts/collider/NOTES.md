# collider notes (running log)

## 2026-09-30

### Setup and conventions
- r110lib.py: ether phase bookkeeping (absolute phase c: cell y reads
  ETHER[(c+y)%14]; one generation adds 4), bit-sliced batch evolution
  (64 experiments per uint64 word), segmentation into objects (defects
  closer than 20 cells merged), glider isolation/verification, collision
  classes (relative seed-event vector mod <P_X,P_Y>; count |det|/14).
- Checked: ether phase advances by 4 per generation; batch engine equals
  scalar engine on random rows.

### Glider discovery
- Random soups (discover.py, 1024 runs, W=2800, T=1600): 119 distinct
  periodic objects, most are same-velocity compounds. Velocities found:
  2/3, 1/5, 0, -1/9, -4/15, -1/3, -1/2. H and gun not found in soups.
- Martinez et al. f1_1 strings (arXiv:0706.3348 App. A) give all 14
  named gliders; my isolation reproduces every period vector. The gun
  string emits gliders (expected; not in library).
- Slip (right ether phase - left, mod 14) is conserved by every
  collision (trivial: far ether untouched). Scholar/synth use it too.

### Bugs found and fixed (keep for the record)
1. Segmentation artifact: two same-velocity gliders ~20 cells apart
   flicker between one and two objects -> never "settled". Fix: standalone
   tests use the union of all defects.
2. isolate_glider found a FALSE period once: a glider left the window
   through the row end (objects touching the ends are ignored), the
   remaining union repeated. Caught by the independent fresh-row
   verification (verify_glider), which raised. Fix: pad beyond light speed
   on both sides; objects near the row edge raise.
3. Compound parsing (naming only): cut-based parse at one time step is
   ambiguous (A4 parsed with wrong spacings). Now a parse must explain
   the compound at every phase; otherwise the compound is named by
   invariants. A^n do NOT parse as independent A's at every phase (they
   are bound: adjacent A's overlap in some phases).

### Catalog v1
- 718 collisions (14 base + A2..A4 as X). All settle; 718/718 verified
  by verify.py (independent scalar engine, full light cone), negative
  control 198/198 detected.

### Open questions / ideas
- What is "v2/3s4w0" (narrow A-speed object, slip 4, width <= 3)? It is
  common in soups (count 26 of 1024) and produced catalytically by
  G hitting Ebar/E/H. Similar: v2/3s2w0 (slip 2), v2/3s10w0 (slip 10):
  row pictures show they are *deletions* of 2/4/.. cells from the ether
  (A is an insertion of 6), i.e. "negative" A-type slips. Check literature
  (scholar) - Cook's list has A^n only?
- v-4/15s1w6: p=15 object at E speed, slip 1, width 6-12. From A+Ebar
  (2 classes) and E+B.

### Later on 2026-09-30
- Renamed A-packets (rename.py): Martinez (111110)^n -> Aw<n>; tight
  packets A^2..A^5 (Cook's A^4 = old v2/3s4w0, found in assembled Cook
  row); B^2, B^3. B strips one A at a time (single class).
- Packets (packets.py): stable 2-glider packets registered as compound
  gliders; ran vs C1-C3 and F. Catalog 3945 collisions, all verified.
- MISTAKE (posted and corrected on the board): outcomes for a non-canonical
  relative event r must be translated by a*P_X where r - rep = aP_X + bP_Y.
  I forgot this in relay.py; the C outputs were right (stationary, invisible
  to time translation) but moving outputs were wrong. Now predict.py does
  it, tested against direct simulation. Lesson: any time I reuse a catalog
  row for a different placement, go through predict().
- F read-and-reset gadget verified directly (check_fread.py).
- Switch analysis (switches.py): like-for-like comparison only possible for
  slip-0 shifters (Ebar pairs); single-glider crossings change the ether
  on the partner's side. Useful fact: a 14-cell shift of C2 advances the
  C2-Ebar class by one step in a 4-cycle.
- regions.py: interaction regions per catalog entry, for glidersim.py.
  Edge case found: some "fusions" are juxtapositions: A adjacent to D2 IS
  a D1 (and A adjacent to C1 is an F) - the free-inputs and free-products
  descriptions overlap in time. Region = [min, max] of the two switch
  times.
- FINDINGS.md: the harness refuses to let me (a subagent) write report
  files; the verified findings go into my final report and the board.
- glidersim.py validated: 188/188 cell-exact agreements on random scenes,
  0 disagreements, 112 refused as possible 3-body (of those, naive
  pairwise application would be wrong/inconsistent in 39) -> guard needed.
- E^n counter: INC = B (single class). DEC from the left = A in one class
  (A-train with fixed spacing class, history-independent: checked all
  histories <= 10); DEC from the right = G, class-free, answer A^3; zero:
  G#0 -> E + A^4. scholar's "G passes E_n" was a too-short run (retracted).
- G + B^k -> GBk (single object, class-independent). E^n + GBk ->
  E^(n+k-4) (+A^(3-k)), class-free for n >= 2; GB3 DEC / GB4 NOP / GB5 INC;
  zero classes GB3#0 -> E + A, GB4#1 -> E, GB5#0 -> E^2. Rigid G-speed
  program streams verified end-to-end in the CA (ecounter.run_gb).
  Observation: without answers the counter value is a static function of
  the stream prefix (slip bookkeeping), so all data dependence enters via
  the zero answer.
- Soft gate: A + GB4 #4 -> A. Absorbers: A + GB1 #3 -> G; A + G-G packet
  -> GB2 (31 combos). No clean hard gate yet (would need A + H -> GB4).
- Mistake avoided/lesson: the one-sided B/G stream needs geometric spacing
  (B faster than G overtakes it); all-G-speed packets avoid that.
- Tooling lesson (new variant of the pkill lesson): waiter loops of the
  form `until ! pgrep -f "python X.py"` match OTHER waiter shells whose
  command lines contain the same string, so they block each other and a
  queue script forever. Use a PID file / `pgrep -x python` + argument
  check, or wait on the PID directly.
- Hard-gate search (gpackets.py): A vs 2234 two-object G-speed packets
  (G, GB1..GB5 pairs, gap <= 30), 9 classes each. Clean-to-clean hits:
  A + (GB3, GB5 packet) -> GB3 in 5 packet/class combos (net NOP packet
  becomes a DEC). Also A + (G, GB2) -> GB4 in several classes (the
  packet G+GB2 is not answer-free itself).
