"""Re-check coupler 06:31 (T2 scenes A and B) through my code path:
their scene lists (collider seeds, from coupler/verify_scenes.py, imported
read-only with bytecode writing off) are rebuilt with MY builder via
xlate (asserting cell equality with collider's build_row), run with the
engine and typed with MY typer.  Their trains 'v2/3s6w18' (I_L) and
'v2/3s8w16' (Z_L) are aliased to my registered IL / ZL; the alias is
validated by xlate.mapping (my row must equal theirs for seed (0,0))."""
import sys, os
sys.dont_write_bytecode = True
import numpy as np
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import xlate
L.register_IL()
vlib.LIB["v2/3s6w18"] = vlib.LIB["IL"]
vlib.LIB["v2/3s8w16"] = vlib.LIB["ZL"]

CP = os.path.abspath(os.path.join(v3.HERE, "..", "coupler"))
cwd = os.getcwd()
sys.path.insert(0, CP)
os.chdir(CP)
import verify_scenes as VS      # noqa: E402  (read-only)
os.chdir(cwd)
L.register_IL()                 # their imports may reload my library
vlib.LIB.setdefault("v2/3s6w18", vlib.LIB["IL"])
vlib.LIB.setdefault("v2/3s8w16", vlib.LIB["ZL"])


def counters(names):
    val = lambda b: 0 if b == "E" else int(b[2:]) - 1
    return tuple(val(b) for b in names if b == "E" or b.startswith("E^"))


def mine(scene, T):
    scene = xlate.expand(scene)
    items, c0, same = xlate.check(scene)
    assert same, "my row differs from collider's build_row"
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return [v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T)]


if __name__ == "__main__":
    bad = 0
    for v1 in (0, 1, 2):
        for v2 in range(0, 6):
            sc, T = VS.scene_A(v1, v2)
            got = mine(sc, T)
            exp = VS.expect_A(v1, v2)
            ok = got == [("E" if exp[0] == 0 else f"E^{exp[0] + 1}"), ("E" if exp[1] == 0 else f"E^{exp[1] + 1}")]
            note = "" if ok else ("  (expected exception)" if v1 == 0 and v2 in (0, 1) else "  MISMATCH")
            bad += (not ok) and not (v1 == 0 and v2 in (0, 1))
            print(f"A v1={v1} v2={v2}: mine {got} expect (R2,R1)={exp}{note}", flush=True)
    for v1 in range(1, 6):
        for v2 in range(0, 3):
            sc, T = VS.scene_B(v1, v2)
            got = mine(sc, T)
            exp = VS.expect_B(v1, v2)
            ok = got == [("E" if exp[0] == 0 else f"E^{exp[0] + 1}"), ("E" if exp[1] == 0 else f"E^{exp[1] + 1}")]
            bad += not ok
            print(f"B v1={v1} v2={v2}: mine {got} expect (R2,R1)={exp}{'' if ok else '  MISMATCH'}", flush=True)
    # controls: R2 in the other classes
    for t in (VS.R2T0 + 1, VS.R2T0 + 2):
        sc, T = VS.scene_A(0, 3, r2t0=t)
        print(f"control A r2t0={t}: {mine(sc, T)}")
    print("unexpected mismatches:", bad)
