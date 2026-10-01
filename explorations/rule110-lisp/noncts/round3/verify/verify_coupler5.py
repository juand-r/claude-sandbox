"""Check coupler 08:05 (channel K3 = GB1@(0,0)+GB3@(-18,30)).
A. Their scene_C lists (imported read-only, bytecode off) rebuilt with MY
   builder via xlate (cell equality with collider's build_row asserted),
   engine, MY typer: v1 = 0..3 x v2 = 0..6; R2 at seed times 1, 2;
   controls K3 in rafast class 1, 2 (must not give the model).
B. My own construction: K3 (parts translated by xlate.mapping) against my
   E^n, n = 1..15, all 42 seed phases; outcome table."""
import sys, os
sys.dont_write_bytecode = True
from collections import Counter
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import xlate
import adaptive_ca as AC
L.register_IL()

CP = os.path.abspath(os.path.join(v3.HERE, "..", "coupler"))
cwd = os.getcwd(); sys.path.insert(0, CP); os.chdir(CP)
import verify_scenes as VS      # noqa
os.chdir(cwd)
L.register_IL()
vlib.LIB.setdefault("v2/3s6w18", vlib.LIB["IL"])
vlib.LIB.setdefault("v2/3s8w16", vlib.LIB["ZL"])


def mine(scene, T):
    scene = xlate.expand(scene)
    items, c0, same = xlate.check(scene)
    assert same, "my row differs from collider's build_row"
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return [v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T)]


nm = lambda v: "E" if v == 0 else f"E^{v + 1}"
want = lambda e: [nm(e[0]), nm(e[1])]

if __name__ == "__main__":
    bad = 0
    for v1 in range(4):
        for v2 in range(7):
            sc, T = VS.scene_C(v1, v2)
            got = mine(sc, T)
            ok = got == want(VS.expect_C(v1, v2))
            bad += not ok
            print(f"C v1={v1} v2={v2}: mine {got} expect {VS.expect_C(v1, v2)} {'' if ok else 'MISMATCH'}", flush=True)
    for r2t0 in (1, 2):
        for v2 in (0, 1, 3):
            sc, T = VS.scene_C(0, v2, r2t0=r2t0)
            got = mine(sc, T)
            ok = got == want(VS.expect_C(0, v2))
            bad += not ok
            print(f"C r2t0={r2t0} v2={v2}: mine {got} {'ok' if ok else 'MISMATCH'}", flush=True)
    cfail = 0
    for c in (1, 2):
        for v2 in (0, 3):
            sc, T = VS.scene_C(0, v2, classes=(c, 0, 0))
            got = mine(sc, T)
            cfail += got != want(VS.expect_C(0, v2))
            print(f"control K3 class {c} v2={v2}: {got}", flush=True)
    print(f"mismatches {bad}; controls differing from the model {cfail}/4")
    # B: own construction, K3 vs my E^n
    mdt, mdx = AC.my_offset("GB1", "GB3", -18, 30)
    for n in range(1, 16):
        R = nm(n - 1)
        out = Counter()
        for t0 in range(42):
            items = [(R, 0, 0), ("GB1", t0, 150), ("GB3", t0 + mdt, 150 + mdx)]
            objs, r, org, placed = v3.run(items, 4000)
            assert (placed[2][1] - placed[1][1], placed[2][2] - placed[1][2]) == (mdt, mdx)
            out[" + ".join(v3.names(objs))] += 1
        print(f"K3 + {R}: {dict(out)}", flush=True)
