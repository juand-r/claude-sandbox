"""Print the markdown tables used in REPORT.md, computed from results/*.json."""

import json
import math
import statistics as st
from pathlib import Path

RESULTS = Path(__file__).parent / "results"
SEEDS = (0, 1, 2)


def load(name):
    return json.loads((RESULTS / f"{name}.json").read_text())["log"]


def ms(xs, fmt="{:.2f}"):
    """mean (sd) over seeds."""
    if len(xs) == 1:
        return fmt.format(xs[0])
    return f"{fmt.format(st.mean(xs))} ({fmt.format(st.stdev(xs))})"


def diverged(log):
    """A run diverged if it says so, or if any logged loss is non-finite."""
    return any(r.get("phase") == "diverged" or not math.isfinite(r.get("L_SR", 0.0)) for r in log)


def sum_sq(r):
    return r["theta_rms"] ** 2 * 20_100


def table_optimizers():
    print("\n### E1/E2: optimizers (vanilla quine), mean (sd) over seeds 0-2\n")
    print("| optimizer | epochs | initial L_SR | best L_SR | epoch of best | Σθ² at best | L_SR/Σθ² at best | final L_SR |")
    print("|---|---|---|---|---|---|---|---|")
    for key, ep in [("sgd", 30), ("sgd_momentum", 30), ("adam", 30), ("adagrad", 30),
                    ("adamax", 30), ("adamax", 100), ("rmsprop", 30)]:
        logs = [load(f"opt_{key}_{100 if key == 'adamax' else ep}ep_seed{s}")[:ep + 1] for s in SEEDS]
        best = [min(l, key=lambda r: r["L_SR"]) for l in logs]
        print(f"| {key} | {ep} | {ms([l[0]['L_SR'] for l in logs])} | {ms([b['L_SR'] for b in best])} "
              f"| {ms([b['epoch'] for b in best], '{:.0f}')} | {ms([sum_sq(b) for b in best])} "
              f"| {ms([b['rel_error'] for b in best], '{:.3f}')} | {ms([l[-1]['L_SR'] for l in logs], '{:.3g}')} |")


def table_regeneration():
    print("\n### E5: regeneration, T=1, G=10, per seed\n")
    print("| seed | best L_SR after regeneration | weight RMS there | L_SR/Σθ² there "
          "| L_SR/Σθ² after Adamax epochs (gen 2-10) |")
    print("|---|---|---|---|---|")
    for s in SEEDS:
        log = load(f"regen_T1_G10_seed{s}")
        rg = [r for r in log if r.get("phase") == "after_regen"]
        ao = [r["rel_error"] for r in log if r.get("phase") == "after_opt" and r["epoch"] >= 2]
        b = min(rg, key=lambda r: r["L_SR"])
        print(f"| {s} | {b['L_SR']:.3f} (gen {b['epoch']}) | {b['theta_rms']:.4f} | {b['rel_error']:.4f} "
              f"| {min(ao):.2f}-{max(ao):.2f} |")
    print("\n### E6: regeneration only (T=0)\n")
    for s in SEEDS:
        log = load(f"regen_T0_G10_seed{s}")
        rg = [r for r in log if r.get("phase") == "after_regen"]
        fate = "diverged (loss became non-finite)" if diverged(log) else "ran 10 generations without diverging"
        print(f"- seed {s}: weight RMS by generation " + ", ".join(f"{r['theta_rms']:.2g}" for r in rg[:6]) + f"; {fate}")


def table_aux():
    print("\n### E7/E8: auxiliary quine, Adamax, 30 epochs, mean (sd) over seeds 0-2\n")
    print("| run | initial L_Aux | initial L_SR | initial λ·L_Task | final accuracy | final L_SR | final λ·L_Task | final L_SR/Σθ² |")
    print("|---|---|---|---|---|---|---|---|")
    for kind in ("quine", "taskonly"):
        logs = [load(f"aux_{kind}_30ep_seed{s}") for s in SEEDS]
        i, f = [l[0] for l in logs], [l[-1] for l in logs]
        print(f"| {kind} | {ms([r['L_aux'] for r in i], '{:.1f}')} | {ms([r['L_SR'] for r in i], '{:.1f}')} "
              f"| {ms([r['lam_L_task'] for r in i], '{:.1f}')} | {ms([100 * r['accuracy'] for r in f])}% "
              f"| {ms([r['L_SR'] for r in f], '{:.1f}')} | {ms([r['lam_L_task'] for r in f], '{:.1f}')} "
              f"| {ms([r['rel_error'] for r in f], '{:.2f}')} |")


def table_hill():
    print("\n### E3/E4: hill-climbing (seed 0)\n")
    print("| run | epochs | start L_SR | best L_SR (epoch) | final L_SR | final Σθ² | final L_SR/Σθ² | acceptance |")
    print("|---|---|---|---|---|---|---|---|")
    for p in sorted(RESULTS.glob("hill_*.json")):
        log = load(p.stem)
        b, f = min(log, key=lambda r: r["L_SR"]), log[-1]
        print(f"| {p.stem} | {f['epoch']} | {log[0]['L_SR']:.2f} | {b['L_SR']:.2f} ({b['epoch']}) | {f['L_SR']:.4g} "
              f"| {sum_sq(f):.4g} | {f['rel_error']:.3f} | {f.get('accept', float('nan')):.2f} |")


def table_sensitivity():
    print("\n### Sensitivity (seed 0)\n")
    print("| variant | Adamax 30 ep: initial L_SR | best L_SR | L_SR/Σθ² at best | regeneration T=1: outcome |")
    print("|---|---|---|---|---|")
    for suffix, label in [("", "defaults"), ("_he", "literal He init, N(0,1) projection"), ("_outselu", "SELU on weight output")]:
        try:
            opt = load(f"opt_adamax_{'100' if not suffix else '30'}ep_seed0{suffix}")[:31]
            regen = load(f"regen_T1_G10_seed0{suffix}")
        except FileNotFoundError:
            print(f"| {label} | (not run yet) | | | |")
            continue
        b = min(opt, key=lambda r: r["L_SR"])
        if diverged(regen):
            g = next(r["epoch"] for r in regen if r.get("phase") == "diverged" or not math.isfinite(r["L_SR"]))
            out = f"diverged (loss non-finite at generation {g})"
        else:
            rg = [r for r in regen if r.get("phase") == "after_regen"]
            rb = min(rg, key=lambda r: r["L_SR"])
            out = f"best L_SR {rb['L_SR']:.3f}, weight RMS {rb['theta_rms']:.4f}, L_SR/Σθ² {rb['rel_error']:.3f}"
        print(f"| {label} | {opt[0]['L_SR']:.4g} | {b['L_SR']:.4g} | {b['rel_error']:.3f} | {out} |")


if __name__ == "__main__":
    table_optimizers()
    table_regeneration()
    table_aux()
    table_hill()
    table_sensitivity()
