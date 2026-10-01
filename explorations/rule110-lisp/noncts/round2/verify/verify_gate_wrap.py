"""Independent check of gate's claim (gate/NOTES.md 00:00, test_wrap.py 3):
program I^v Z^3 (Z = GB3@(0,0)+GB4@(-25,46), "DEC, wrap 0 -> 6") on a fresh
E ends as E^((v-3) mod 7 + 1), v = 0..6.
Scene: gate's own placement rule (stream.build), so the claim is about THEIR
stream; I translate it to my convention (row equality asserted cell for
cell), evolve with the exact engine, and type with MY typer.
Control: same scene with the GB4 of the LAST Z shifted by (7,0) (changes its
class against the answer A): cases where that Z meets zero must change."""
import sys
import vlib, xlate, gate_scene

def run(v, prog_tail="ZZZ", shift_last=None):
    sc = gate_scene.scene(list("I" * v + prog_tail))
    ex = xlate.expand(sc)
    if shift_last:
        i = max(j for j, it in enumerate(ex) if it[0] == "GB4")
        g, t, x = ex[i]
        ex[i] = (g, t + shift_last[0], x + shift_last[1])
    items, c0 = xlate.translate(ex)
    if not shift_last:
        _, _, same = xlate.check(ex)
        assert same, "translation mismatch"
    last_x = items[-1][2]
    T = int(15 * (last_x + 200)) + 2000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    assert [p[2] for p in placed] == [i[2] for i in items]
    r = vlib.evolve(row, T)
    return [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)], T

def name(val):
    return "E" if val == 0 else f"E^{val+1}"

ok = True
for v in range(7):
    ids, T = run(v)
    exp = [name((v - 3) % 7)]
    good = ids == exp
    ok &= good
    print(f"v={v}: {ids} expected {exp} {'OK' if good else 'MISMATCH'} (T={T})", flush=True)
print("control (last Z's GB4 shifted by (7,0)):")
ctrl_changed = 0
for v in range(7):
    ids, T = run(v, shift_last=(7, 0))
    exp = [name((v - 3) % 7)]
    ctrl_changed += ids != exp
    print(f"  v={v}: {ids}", flush=True)
print("claim", "REPRODUCED" if ok else "NOT reproduced", "; control changed", ctrl_changed, "of 7")
sys.exit(0 if ok and ctrl_changed > 0 else 1)
