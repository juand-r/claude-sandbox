"""Zero test, stage 3b: only movers that are the identity on every normal
register state (predicted: apply(mv, D) == D at the common residue) can
serve as a PROBE. Run each against the abnormal compound left by DEC at
value 0, and report the products even if not settled (settling fails
whenever a stationary messenger has Ebar debris on its right)."""
import sys
from winding3 import movers, apply
from probe_search import scenario
from rx import LIB, history
sys.path.insert(0, "../collider")
from library import Library
from collide import simulate

if __name__ == "__main__":
    ids = [mv for mv in movers() if apply(mv, (0, 43)) == (0, 43)]
    print("identity movers:", len(ids), flush=True)
    for mv in ids:
        res = simulate(LIB, scenario(mv), 36 * 600 + 8000)
        names = sorted(p[0] for p in res["products"])
        print(mv, "settled" if res["settled"] else "UNSETTLED", names, flush=True)
