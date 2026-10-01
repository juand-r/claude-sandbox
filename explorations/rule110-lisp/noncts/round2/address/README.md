# address (round 2): two registers in one Rule 110 lane

Goal: two independently addressable registers (round 1 could only drive
the frontmost/last store).

Main result [sim]: three F gliders T > M > P moving at -1/9 hold two
registers, reg1 = gap(T,M) and reg2 = gap(M,P). A stream of Ebar pairs
from the right changes either register while the other stays exactly
unchanged. The mechanism is absorption: a pair crosses some F's and is
swallowed by one F (F + Ebar pair -> F, displaced), and its collision
class decides which F. Without absorption the same lane admits no
addressing at all (catalog-exhaustive negative result).

Files (run from this directory; they import round-1 code read-only):
- lane.py, gen.py: catalog-level crossing chains (architect/collider predict).
- tworeg.py, graph.py, cycles.py, cgraph.py: residue graphs for 2-4 F's,
  crossings only (negative result). cmsg.py: same for C messengers.
- absorb.py, absorb_walks*.py: graphs with absorption, closed walks.
- tworeg_abs.py: the four instructions DN1/UP1/DN2/UP2, verified by full
  simulation (`python tworeg_abs.py 0 2`); control_abs.py: negative controls.
- fixed_stream.py, run_fixed.py: the same driven by a FIXED stream (slot j
  placed from j and the instruction type only), with drift balancing.
- simcheck.py: simulation checks of the 3-marker negative predictions.
- NOTES.md: running log, including mistakes.
