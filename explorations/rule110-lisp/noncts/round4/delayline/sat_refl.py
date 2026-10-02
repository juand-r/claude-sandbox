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
from react import TrainVar                    # noqa: E402
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
    mid = int(-4 * T / 15) - 6
    S.is_item(T, S.lo - T, mid, Z, far_left=S.p_left)
    S.is_item(T, mid, S.hi + T, en_item(cnf, 2 if target == "refl" else 1), far_right=S.p_right)
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
    a = ap.parse_args()
    t0 = time.time()
    cnf = CNF()
    Y = TrainVar(cnf, a.W, 42, -14, 0, name="Y")
    Z = None
    if a.target in ("refl", "shoot7"):
        Z = TrainVar(cnf, a.WZ, 4, -2, 8 if a.target == "refl" else 0, name="Z")
    scenes = [scene_a(cnf, Y, a.ca, a.T, a.gap, a.moved), scene_b(cnf, Y, Z, a.cb, a.T, a.gap, a.target)]
    sol = cnf.solve()
    rec = dict(vars(a), sat=sol is not None, secs=round(time.time() - t0, 1))
    if sol is not None:
        rec["Y"] = "".join(map(str, Y.decode(sol)))
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
