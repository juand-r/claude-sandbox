"""Measure the glider-level transition table of the E^n stream machine in my
convention: for packet P with seed phase p (mod 3) hitting counter E^(m+1)
with seed phase t (mod 3), record (outcome value m' or None, output seed
phase t' mod 3). Output seed phase is computed from the output phase s at
time T: t' = (T - s) mod 3 (a glider of period (15,-4) at time T is in
phase s = T - t0 mod 15, and 15 = 0 mod 3).
Writes calib.json: key "P,m,t,p" -> [m', t'] or null."""
import json
import vlib, libgen
import adaptive_ca as A
libgen.load()
T = 4000

def one(m, t, P, p, X=60):
    nm = "E" if m == 0 else f"E^{m+1}"
    items = [(nm, t, 0)] + A.parts(P, p, X)
    row, org, placed = vlib.build(items, T=T)
    deltas = {q[2] - it[2] for q, it in zip(placed[1:], items[1:])}
    assert len(deltas) == 1, "packet geometry broken by snapping"
    r = vlib.evolve(row, T)
    ids = [n for n, x, w, k in vlib.identify(r, org, T=T)]
    es = [n for n in ids if n.split("@")[0] == "E" or n.startswith("E^")]
    other = [n.split("@")[0] for n in ids if n not in es]
    if len(es) != 1 or any(o != "Bbar" for o in other):
        return None
    nm2, s = es[0].split("@")
    m2 = 0 if nm2 == "E" else int(nm2[2:]) - 1
    return [m2, (T - int(s)) % 3]

if __name__ == "__main__":
    tab = {}
    for P in "IZJNXWD":
        for m in range(0, 8):
            for t in range(3):
                for p in range(3):
                    tab[f"{P},{m},{t},{p}"] = one(m, t, P, p)
        print(P, "done", flush=True)
    json.dump(tab, open("calib.json", "w"), indent=0)
