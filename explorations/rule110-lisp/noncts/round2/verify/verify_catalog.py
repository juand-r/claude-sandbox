"""Re-simulate collider catalog reactions through my pipeline: X at (0,0),
Y at r['Y_event'] (collider convention), translated, exact engine, my typer."""
import os, sys, json
import vlib, xlate
COLL = xlate.COLL
R = {r["id"]: r for r in json.load(open(os.path.join(COLL, "reactions.json")))}

def resim(rid, T=None):
    r = R[rid]
    T = T or max(3 * r["T"], 1500)
    sc = [(r["X"], 0, 0), (r["Y"], int(r["Y_event"][0]), int(r["Y_event"][1]))]
    ex = xlate.expand(sc)
    items, c0, same = xlate.check(ex)
    assert same
    row, org, placed = vlib.build(items, c0=c0, T=T)
    rr = vlib.evolve(row, T)
    mine = sorted(n.split("@")[0] for n, x, w, k in vlib.identify(rr, org, T=T))
    return mine, sorted(p[0] for p in r["products_base"])

if __name__ == "__main__":
    for rid in sys.argv[1:]:
        mine, theirs = resim(rid)
        print(rid, "| mine", mine, "| catalog", theirs, "|", "SAME" if mine == theirs else "DIFFERENT")
