"""Check queue 23:30 item 4: a tape C crossing an Ebar is displaced by +7
cells (the Ebar's slip) - here for single C1, C2, C3 vs Ebar, all 4 classes
(det((7,0),(30,-8))/14 = 4), my builder/typer. A 'crossing' = products are
the same C type and one Ebar; report the C's displacement vs a C-alone run."""
import pairscan

T = 1500
for C in ("C1", "C2", "C3"):
    alone, _ = pairscan.run_items([(C, 0, 0)], T)
    (n0, x0, _), = alone
    res = pairscan.classes(C, "Ebar", 60, T, n_expected=4)
    for k, (names, objs, placed) in sorted(res.items()):
        cs = [(n, x) for n, x in objs if n.split("@")[0] == C]
        if sorted(names) == sorted([C, "Ebar"]) and len(cs) == 1 and cs[0][0] == n0:
            print(f"{C} x Ebar class {k}: crosses, {C} displaced {cs[0][1] - x0:+d} cells")
        else:
            print(f"{C} x Ebar class {k}: {list(names)}")
