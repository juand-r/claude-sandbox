"""Zero test, stage 4. Value 0 is the close compound F_19_F (left by DEC
from gap 33.67). Scan every pure-Ebar mover (single Ebar or catalog Ebar
pair, every class relative to T) against the compound and record all
products (settled or not) as JSON lines for later analysis. Wanted: the
compound intact + exactly one stationary messenger + only -4/15 debris."""
import json, re, sys
sys.path.insert(0, "../collider")
from collide import simulate
from winding3 import movers
from probe_search import scenario
from rx import LIB

if __name__ == "__main__":
    MV = [m for m in movers() if not re.search(r"E(?!bar)", m[0])]
    out = open("zc_search.jsonl", "w")
    for i, mv in enumerate(MV):
        res = simulate(LIB, scenario(mv), 36 * 600 + 8000)
        rec = {"i": i, "mover": mv, "settled": res["settled"],
               "products": res["products"]}
        out.write(json.dumps(rec) + "\n")
        out.flush()
        names = [p[0] for p in res["products"]]
        comp = sum(1 for n in names if n.startswith("F_19_F"))
        cs = [n for n in names if n in ("C1", "C2", "C3")]
        if comp == 1 and len(cs) == 1:
            print("CANDIDATE", i, mv, sorted(names), flush=True)
    print("done", len(MV), flush=True)
