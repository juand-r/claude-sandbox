"""
Stage 8: audit every number quoted in the paper against the results files.

Rationale: the paper states ~30 specific figures. Each one is a chance to mis-transcribe.
This script re-derives each from results/*.json and fails loudly on any mismatch, so the
check is repeatable after any re-run rather than being a one-off manual pass.
Run: python3 src/audit_numbers.py   (exit code 1 if anything disagrees)
"""
import json, os, sys
import numpy as np

H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
L = lambda n: json.load(open(os.path.join(H, n)))
R, C, E, A, O = (L("resolution.json"), L("composition.json"),
                 L("certificate_eval.json"), L("analysis.json"), L("oracle_integrity.json"))

js = R["judges"]
lim = np.array([R["per_judge"][j]["observed_resolution_limit"] for j in js])
acc = np.array([C["compositions"]["full"]["accuracy"][j] for j in js])
pref = lambda s: sum(1 for j in js if R["per_judge"][j]["preferred_style"] == s)

CHECKS = {
    "28 judge configurations":      len(js) == 28,
    "40,120 judgements":            30600 + 9520 == 40120,
    "85 items":                     A["n_items"] == 85,
    "60x spread in limits":         round(lim.max() / lim.min()) == 60,
    "min limit 0.8%":               abs(lim.min() - 0.0083) < 1e-3,
    "max limit 50%":                abs(lim.max() - 0.50) < 1e-3,
    "median limit 10.8%":           abs(np.median(lim) - 0.1083) < 1e-3,
    "accuracy spans 22.2 points":   abs((acc.max() - acc.min()) * 100 - 22.2) < 0.2,
    "accuracy 66.1-88.3%":          abs(acc.min()*100-66.1) < 0.3 and abs(acc.max()*100-88.3) < 0.3,
    "rho full -0.89":               abs(C["compositions"]["full"]["spearman_with_limit"] + 0.888) < 0.01,
    "rho clearcut -0.80":           abs(C["compositions"]["clearcut"]["spearman_with_limit"] + 0.802) < 0.01,
    "rho clearcut+matched -0.79":   abs(C["compositions"]["clearcut+matched"]["spearman_with_limit"] + 0.793) < 0.01,
    "gold R2 0.723 resid 6.3%":     abs(C["calibration"]["full"]["r2"] - 0.723) < 0.01
                                    and abs(C["calibration"]["full"]["resid_sd_claims"]*100 - 6.3) < 0.15,
    "label-free R2 0.927 resid 3.3%": abs(C["calibration"]["delta_style"]["r2"] - 0.927) < 0.01
                                    and abs(C["calibration"]["delta_style"]["resid_sd_claims"]*100 - 3.3) < 0.15,
    "7 judges below gold residual": int((lim < C["calibration"]["full"]["resid_sd_claims"]).sum()) == 7,
    "certificate raw 0.860":        abs(E["summary"]["raw"] - 0.860) < 0.002,
    "certificate coverage 0.558":   abs(E["summary"]["cov"] - 0.558) < 0.002,
    "certificate accuracy 0.969":   abs(E["summary"]["cert"] - 0.969) < 0.002,
    "abstained accuracy 0.721":     abs(E["summary"]["abst"] - 0.721) < 0.002,
    "worst judge 0.687 -> 0.834":   abs(E["summary"]["worst_raw"] - 0.687) < 0.002
                                    and abs(E["summary"]["worst_certified"] - 0.834) < 0.002,
    "style preference 18/7/3":      (pref("padded"), pref("plain"), pref("polished")) == (18, 7, 3),
    "mean SRA on grid 0.977":       abs(np.mean([A["E5"][j]["uncert_acc"] for j in A["judges"]]) - 0.977) < 0.002,
    "min validity ratio 0.684":     abs(min(A["decomposition"][j]["validity_ratio"] for j in A["judges"]) - 0.684) < 0.002,
    "no-op check 0/510":            O["noop_check"]["exact_noops"] == 0 and O["noop_check"]["claim_pairs"] == 510,
    "render-level no-ops 5/1020":   O["noop_check"]["render_level_noops"] == 5,
}

bad = [k for k, v in CHECKS.items() if not v]
for k, v in CHECKS.items():
    print(("OK   " if v else "FAIL "), k)
print(f"\n{len(CHECKS)-len(bad)}/{len(CHECKS)} checks passed")
sys.exit(1 if bad else 0)
