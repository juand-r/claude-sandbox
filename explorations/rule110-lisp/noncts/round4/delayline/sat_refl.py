"""SAT (synth/r110sat.py, read-only): a right-stream packet Y (G lattice,
period (42,-14), width W, slip 0) acting on a value-1 / value-0 window:
  scene a (closed): E^2 + Y (class ca) -> E^2 only, UNMOVED (undisturbed
                    placement) [--moved: any placement]
  scene b (open):   E   + Y (class cb) -> target
targets:
  refl  : Z (free B-lattice train (4,-2), width WZ, slip 8 = 6 units) left
          + E^2 right    -- reusable reflector (lead 00:16 item 3; THEORY_DL s.8.3)
  shoot7: Z (B-lattice, slip 0 = 7 units) left + E right -- 7-unit shooter
  walk  : E only (any placement)   -- POSITIVE CONTROL (GB4, width 29, does it)
  pass2 : Z (B-lattice, slip 12 = 2 units) left + E right, with --only_b:
          POSITIVE CONTROL for the Z branch (library GB3@(0,0)+G@(-16,45),
          width 47, class 2, does it)
  close4: Z (slip 4 = 3 units) left + E^5 right: S43 = GB3@(0,0)+GB5@(-14,54)
          does it (width 84); with --fixY it controls the full two-scene
          encoding including the Z branch
Every SAT answer is re-simulated cell for cell (check_sat_vs_sim).
Results appended to sat_refl.jsonl (this directory).
Usage: python sat_refl.py --target refl --W 30 --ca 0 --cb 0 [--T 360] [--WZ 30]"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
SYNTH = os.path.abspath(os.path.join(HERE, "..", "..", "synth"))
OUT = os.path.join(HERE, "sat_refl.jsonl")
sys.path.insert(0, SYNTH)
_cwd = os.getcwd()
os.chdir(SYNTH)
from r110sat import CNF, make_window          # noqa: E402
from react import TrainVar, Fixed             # noqa: E402
from scene import Scene                       # noqa: E402
from classes import placements_by_class       # noqa: E402
from en import en_item                        # noqa: E402
os.chdir(_cwd)
MARGIN = 20


def scene_a(cnf, Y, c, T, gap, moved):
    E2 = en_item(cnf, 2)
    tau, x = placements_by_class(E2, (0, 0), Y, E2.W + gap)[c]
    win = make_window(T, 0, x + Y.W + tau, -4 / 15, -1 / 3, margin=MARGIN)
    S = Scene(cnf, T, [(E2, 0, 0), (Y, tau, x)], window=win, name="a")
    only = None if moved else Scene.undisturbed(E2, 0, 0, T)
    S.is_item(T, S.lo - T, S.hi + T, en_item(cnf, 2), far_left=S.p_left,
              far_right=S.p_right, only=only)
    return S


def scene_b(cnf, Y, Z, c, T, gap, target):
    E1 = en_item(cnf, 1)
    tau, x = placements_by_class(E1, (0, 0), Y, E1.W + gap)[c]
    vL = -1 / 2 if Z is not None else -4 / 15
    win = make_window(T, 0, x + Y.W + tau, vL, -4 / 15, margin=MARGIN)
    S = Scene(cnf, T, [(E1, 0, 0), (Y, tau, x)], window=win, name="b")
    if target == "walk":
        S.is_item(T, S.lo - T, S.hi + T, en_item(cnf, 1), far_left=S.p_left, far_right=S.p_right)
        return S
    mid = int(-4 * T / 15) - 2   # undisturbed E's left side: Z must be left of it, the rod (walks are rightward) right of it
    S.is_item(T, S.lo - T, mid, Z, far_left=S.p_left)
    S.is_item(T, mid, S.hi + T, en_item(cnf, {"refl": 2, "close4": 5}.get(target, 1)), far_right=S.p_right)
    return S


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="refl")
    ap.add_argument("--W", type=int, default=30)
    ap.add_argument("--WZ", type=int, default=30)
    ap.add_argument("--ca", type=int, default=0)
    ap.add_argument("--cb", type=int, default=0)
    ap.add_argument("--T", type=int, default=360)
    ap.add_argument("--gap", type=int, default=4)
    ap.add_argument("--moved", action="store_true")
    ap.add_argument("--only_b", action="store_true", help="scene b alone (positive control for the Z branch)")
    ap.add_argument("--fixY", default=None, help="library packet name: Y fixed (encoding control)")
    a = ap.parse_args()
    t0 = time.time()
    cnf = CNF()
    if a.fixY:
        # ENCODING CONTROL: Y fixed to a library packet (collider bits,
        # re-framed so that its left ether has relative phase 0)
        sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "collider")))
        os.chdir(os.path.abspath(os.path.join(HERE, "..", "..", "collider")))
        from library import Library
        from r110lib import ETHER
        os.chdir(_cwd)
        b, lph, rph, off = Library.load().gliders[a.fixY].state_at(0, 0, 0)
        bits = "".join(ETHER[(k) % 14] for k in range(lph % 14)) + b
        Y = Fixed(cnf, bits, (rph - lph) % 14, (42, -14), name="Y")
    else:
        Y = TrainVar(cnf, a.W, 42, -14, 0, name="Y")
    Z = None
    if a.target in ("refl", "shoot7", "pass2", "close4"):
        Z = TrainVar(cnf, a.WZ, 4, -2, {"refl": 8, "shoot7": 0, "pass2": 12, "close4": 4}[a.target], name="Z")
    sb = scene_b(cnf, Y, Z, a.cb, a.T, a.gap, a.target)
    scenes = [sb] if a.only_b else [scene_a(cnf, Y, a.ca, a.T, a.gap, a.moved), sb]
    sol = cnf.solve()
    rec = dict(vars(a), sat=sol is not None, secs=round(time.time() - t0, 1))
    if sol is not None:
        rec["Y"] = a.fixY if a.fixY else "".join(map(str, Y.decode(sol)))
        if Z is not None:
            rec["Z"] = "".join(map(str, Z.decode(sol)))
        rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
        rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
        rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
        if not rec["sim_ok"]:
            raise AssertionError("SAT/sim mismatch")
    print(json.dumps({k: v for k, v in rec.items() if k != "rows0"}), flush=True)
    with open(OUT, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
