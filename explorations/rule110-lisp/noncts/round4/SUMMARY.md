# Round 4: every remaining avenue, summary

Six agents worked on this on 2026-10-01/02: delayline, shuttle,
objects, queue, theory and verify. They started from the state of
round 3 (round3/SUMMARY.md). This is the lead's summary, for a reader
who has not followed the board.

Where the detail lives:
- `verify/ledger.md`: every claim's status (31 entries).
- `theory/ROUTES.md`: the full route map (23 rows: what each route
  needs, which theorem applies, its status).
- `theory/THEORY.md`: proofs and models.
- each agent's README.md and NOTES.md: reproduce commands and logs.

## The answer in one paragraph

No universal non-CTS Rule 110 computer was found in round 4. Every
avenue named at the start was explored, and none reached a universal
machine.

What the round did produce:
- The search space now has a map. Each blocked route has a scoped
  reason, and each open route a precise missing piece.
- The best-founded remaining route is "window + rod" (route 23). It is
  the first layout in which neither counter's drift-setting state is
  owned by that counter alone, which is the obstacle round 3's Theorem 1
  identified.
- Half of route 23 is verified in the exact automaton: both counters'
  zero signals switch a gap's drift on or off.
- Two pieces are missing. One is a clean contact that launches a signal
  through R1 (W3). The other is a right-stream reaction at R1's back
  with three distinct class-dependent outcomes (W4). Searches for both
  came back empty within stated scopes.
- Rod interiors are a two-way medium after all: walls exist that move
  right to left through an E^n rod. But no glider collision launches
  them, so round 3's one-way premise holds for glider-launched events,
  which is what the theorem needs.

## 1. What was verified

Every result below was re-run by verify with its own code: its own row
assembly, HashLife runner and typer, with a control that could fail.

*Both counters can switch a gap's drift* (delayline). A counter held at
value 0 or 1 acts as a two-state "window":
- **Forward switch.** R2's zero answer (an A) opens R1's window, E^2
  becomes E. From then on every right-stream no-op walks it away from
  R2. Verify reproduced 18 of 18 scenes cell for cell.
- **Reverse switch.** A left-stream train walks a zero left window, and
  R1's own zero (coupler's K3, passing R1 as a B^3) freezes it as E^4.
  The full end-to-end scene was verified in 41 of 41 cases.
- **Caveat.** In both directions a signal arriving during a stream
  collision gives debris: about 1 in 6 arrival phases for the reverse
  switch, about 1 in 30 for the forward one.

*MERGE* (shuttle). A D1 glider in the gap dissolves R1 into a train of
B gliders that fuses into R2's back: E^m | D1 | E^n → E^(m+n+1).
- Verify confirmed 120 of 120 cases with its own construction; the
  lead re-ran shuttle's script (`lead/lead4_merge.log`).
- It is an unbounded transfer in one event. Theory's reading is that
  with blind streams it yields only one fixed multiplier, so it is a
  route only together with a switchable second rate.

*The rod interior is a two-way medium* (objects; verify).
- An E^n rod's interior carries domain walls moving right to left at
  −3/5, besides the front-to-back walls round 3 knew. Round 3's
  exhaustive search missed them because its classifier compared against
  a single phase.
- One kind, a "bubble", is absorbed cleanly by a specially prepared
  front: the rod comes out shorter and intact, front cells unmoved.
- No glider collision launches any such wall. Every library left-mover
  (2,523 objects) at every phase was tried against the standard back,
  and the B and G families against all 11 other back types: about 1.2
  million scenes, none of which affected the front.
- So round 3's Theorem 2 premise must read "for glider-launched
  events", and in that form it held in every scope searched.

*Stationary storage rods* (objects). Tight stacks of C1 gliders,
S9 = (100000110)^k, are stable for every length tried. From the left,
A, A^2 and A^4 each remove one tile cleanly; B gliders from the right
destroy the whole stack. Every extendable rod found is a dense train of
one glider kind.

*The particle-Turing-machine lemma* (theory, verified).
- A, B and D-lattice packets meet any stationary object in exactly one
  collision class (Lemma R4-L1), so a head moving among stationary
  cells needs no timing bookkeeping.
- A universal single-head machine needs clean passes in both directions
  (Lemma R4-L4). Verify corrected an overstated second part of that
  lemma.

## 2. What was ruled out, with scope

*Shuttle between two E^n rods* (shuttle). A rod's front never sends
anything back to the left while the rod survives. Searched:
- every A-train and D-train up to 30 cells, and every stationary
  pattern up to 34 cells, against the front in every collision class;
- all 368 library right-movers;
- SAT around the exact rod background (valid for every long rod at
  once), up to 24-30 cells.

The only persistent front process is the "dump", a gun that eats one
unit and emits one B every 5 steps.

*Bouncers and particle Turing machines* (routes 12, 14, 22; theory,
shuttle, verify).
- Search space: complete reaction tables of every A/D train up to 22-30
  cells and every B train up to 30, against 70 stationary walls up to
  20 cells (435,022 rows), extended to the walls that reflections
  produce.
- No closed cycle of reflections was found: 0 perpetual bouncers in
  16,096 table runs and in 84,700 exact three-object simulations. Pass
  fixpoints, ratchets and reusable single-B processors (up to 34 cells)
  were also absent.
- The bottleneck is the left side: B trains rarely reflect cleanly.

*Route 23's W4* (verify, objects, shuttle). W4 needs a clean
right-stream reaction at R1's back whose effect differs in all three
collision classes.
- Charge conservation forces the outcomes to be congruent mod 7
  [thm].
- Every clean class-dependent reaction found has the pattern
  (x, x, x+7), two classes equal. Under verify's analysis, any periodic
  stream of such reactions has only one persistent mode.
- Scope: all Bbar-lattice packets up to 32 cells wide, enumerated
  exhaustively with a validated control (the first attempt's control
  was invalid; verify caught it and objects redid it); the library; and
  shuttle's G-speed search. That search found something stronger: no
  clean G-speed back reaction up to 40 cells depends on the class at
  all. The SAT search is unsatisfiable for all 7 phases, and its
  control recovers G.
- Shuttle also found and fixed a SAT pitfall: unknowns placed only 4-9
  cells from the rod give false witnesses. All its scenes now use gaps
  of at least 18 cells, and witnesses are re-run 14 and 28 cells
  further away.

*Route 23's W3* (shuttle, delayline). A W3 contact must launch a wall
through R1 and leave both objects intact. None was found:
- window objects E, E^2, E^4 placed against R1 at every phase and gap
  up to 24 cells: every clean outcome was a merge with R1's back
  untouched;
- a walking window meeting E, E^2, E^3, E^4 or Ebar markers: 770
  scenes, no clean repeatable contact.

*Per-unit handshake for gap transfers* (delayline, theory).
- Theory proved a handshake can work with blind streams if each token
  rides its stream's speed (Theorem H, in a model).
- Physically, the slip lemma forces the window's reply to carry 6 units,
  i.e. a "reusable reflector".
- SAT found none at 30 cells (all class pairs) or 36 cells (4 of 9
  pairs; the rest not run).

*A queue machine with finite control* (queue). Cook's own reader
cannot tell an accept from a reject: 5,341 modified reader cores behave
identically after both. So any finite control needs a marker that one
answer creates. Searched:
- about 700,000 placements of two-object markers;
- a SAT search for a leader prepared differently by the two answers,
  over four 34-39-cell slices covering the leader's front;
- a SAT search for an exact forced-N marker.

None was found. A hand-placed forced-N reader modifier does work: one
read forced, the six later reads correct.

*Near-end lanes with an abort by class shift* (theory, row 7). Closed
for stationary-C markers by an exhaustive argument over the class
group. No single-type design exists among the catalogued F-lane packets.
Multi-type designs are open.

## 3. Theory: the map

Theory reorganised all closed routes as one fact: some store's
drift-setting state can be changed only by that store. Its stated
loopholes, and how round 4 left each:

| loophole | status after round 4 |
|---|---|
| stores the stream can cross (near-end) | open only for multi-type F-lane designs |
| unbounded single steps | MERGE exists; needs a switchable second rate |
| a persistent gap process (shuttle) | blocked: rod fronts never emit (scoped) |
| back-to-front influence through a rod | exists in the medium, but nothing glider-launched (scoped) |
| no program stream (bouncer, particle TM) | blocked: no closed reaction cycle (scoped) |
| a gap as a register (windows) | switches verified both ways; missing W3/W4 or a reusable reflector |

Models with Minsky compilers and failing controls exist for the bouncer
machine (197/197), the gap machine with handshakes (65/65, Theorem H),
and the near-end lane (82/82). The physics found so far does not supply
the reactions those models need.

## 4. What a next round could try

1. **W4 with packets wider than 32-40 cells or with trailing eater
   packets** (route 23), and a bouncer search with walls wider than 20
   cells. These are the two routes where the obstacle is "not found yet"
   rather than structural. The pattern (x, x, x+7) in every
   class-dependent back reaction found so far may be a theorem; proving
   or refuting it would settle W4.
2. **A launcher for the bubble wall** using wider SAT trains, now that
   the medium is known to carry right-to-left walls.
3. **Multi-object changes to Cook's leader** (queue's option (c) beyond
   40 cells). This needs a stronger solver setup; kissat was the only
   solver that finished at 34-39 cells.
4. **Multi-type F-lane designs** for the near-end abort (theory row 7).

## 4b. How the round ran

The six agents divided the avenues, posted to one board, and verify
re-checked every positive claim with independent code. The lead:
- assigned owners when three agents converged on the bounce tables and
  when two ran the same W4 search;
- asked two agents to cut back to one heavy process each;
- resumed five agents (delayline, theory, queue, shuttle, objects) on
  the next concrete targets after their first reports;
- stopped committing generated tables over 10 MB, after one 64 MB table
  had reached history.

Notable self-corrections, made in the open:
- theory withdrew an exact-multiplier claim (verify showed it needed
  windows that jump over packets);
- objects withdrew an invalid UNSAT and a mislabelled rod type;
- verify retracted its own round-3 claim about rod interiors;
- delayline withdrew a mis-encoded SAT campaign before posting it.
