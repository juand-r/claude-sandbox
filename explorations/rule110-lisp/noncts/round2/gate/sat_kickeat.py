"""SAT (synth's r110sat/react/scene, read-only import): is there an
Ebar-speed packet Y (free (30,-8) train, width <= W, slip 0) that is
  scene C: C1 + Y -> C1 alone   (eaten by the messenger), and
  scene F: F  + Y -> F alone    (absorbed by a register marker = a kick)?
The same unknown Y is shared by both scenes. Modes: C (only scene C), F
(only scene F), CF (both). Positive controls: mode C must find an eater
(catalog: (-4,23) etc.), mode F a kick ((-9,29), (-26,27)).
Every SAT answer is re-simulated with the exact engine (check_sat_vs_sim).
Usage: python sat_kickeat.py W MODE [--kC list] [--kF list] [--TC 300] [--TF 500]"""
import argparse
import json
import os
import sys
import time

SYN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "synth")
sys.path.insert(0, SYN)
from lib import load_gliders  # noqa: E402
from r110sat import CNF, make_window  # noqa: E402
from react import TrainVar, fixed_from_glider  # noqa: E402
from scene import Scene  # noqa: E402
from classes import placements_by_class  # noqa: E402

G = load_gliders()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sat_kickeat.jsonl")


def scene_for(cnf, Y, marker, width, k, T, vL):
    M = fixed_from_glider(cnf, G[marker], width)
    tau, x = placements_by_class(M, (0, 0), Y, M.W + 4)[k]
    win = make_window(T, 0, x + Y.W + tau, vL, 2 / 3, margin=24)
    S = Scene(cnf, T, [(M, 0, 0), (Y, tau, x)], window=win, name=marker)
    S.is_item(T, S.lo - T, S.hi + T, M, far_left=S.p_left)
    return S


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("W", type=int)
    ap.add_argument("mode")
    ap.add_argument("--kC", default="0")
    ap.add_argument("--kF", default="0")
    ap.add_argument("--TC", type=int, default=300)
    ap.add_argument("--TF", type=int, default=520)
    a = ap.parse_args()
    for kC in map(int, a.kC.split(",")):
        for kF in map(int, a.kF.split(",")):
            t = time.time()
            cnf = CNF()
            Y = TrainVar(cnf, a.W, 30, -8, 0, name="Y")
            scenes = []
            if "C" in a.mode:
                scenes.append(scene_for(cnf, Y, "C1", 12, kC, a.TC, -0.3))
            if "F" in a.mode:
                scenes.append(scene_for(cnf, Y, "F", 24, kF, a.TF, -0.3))
            sol = cnf.solve()
            rec = {"W": a.W, "mode": a.mode, "kC": kC, "kF": kF, "sat": sol is not None,
                   "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["Y"] = "".join(map(str, Y.decode(sol)))
                rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
            print(json.dumps(rec), flush=True)
            with open(OUT, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
