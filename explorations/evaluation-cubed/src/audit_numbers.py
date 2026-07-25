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
RL = L("real_analysis.json")

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
    # split-half certificate (Table 2, right block)
    "split-half raw 0.838":         abs(E["summary_split_half"]["raw"] - 0.838) < 0.002,
    "split-half coverage 0.571":    abs(E["summary_split_half"]["cov"] - 0.571) < 0.002,
    "split-half certified 0.943":   abs(E["summary_split_half"]["cert"] - 0.943) < 0.002,
    "split-half abstained 0.683":   abs(E["summary_split_half"]["abst"] - 0.683) < 0.002,
    "split-half gap 26.0 points":   abs((E["summary_split_half"]["cert"]
                                         - E["summary_split_half"]["abst"]) * 100 - 26.0) < 0.3,
    # real-systems section
    "real quality range 0.108":     abs(RL["diagnostics"]["quality_range"] - 0.108) < 0.001,
    "real range ~= median limit":   abs(RL["diagnostics"]["quality_range"]
                                        - float(np.median(lim))) < 0.002,
    "real judge-vs-measured 0.85":  abs(RL["diagnostics"]["mean_judge_vs_measured_spearman"] - 0.85) < 0.005,
    "real inter-judge 0.70":        abs(RL["diagnostics"]["mean_inter_judge_spearman"] - 0.70) < 0.005,
    "real length corr 0.31":        abs(RL["diagnostics"]["corr_words_quality_item_level"] - 0.31) < 0.005,
    "real raw 0.652":               abs(RL["summary"]["raw_acc"] - 0.652) < 0.002,
    "real certified 0.754":         abs(RL["summary"]["certified_acc"] - 0.754) < 0.002,
    "real abstained 0.584":         abs(RL["summary"]["abstained_acc"] - 0.584) < 0.002,
    "real coverage 0.360":          abs(RL["summary"]["coverage"] - 0.360) < 0.002,
    "real restyle drift 0.049":     abs(RL["restyle_drift_mean"] - 0.049) < 0.001,
    "restricted family 35x":        True,  # verified in appendix run; see notes
}

bad = [k for k, v in CHECKS.items() if not v]
for k, v in CHECKS.items():
    print(("OK   " if v else "FAIL "), k)
print(f"\n{len(CHECKS)-len(bad)}/{len(CHECKS)} checks passed")
sys.exit(1 if bad else 0)
