"""
K-fold cross-validation: do gradient/optimizer features predict time_to_next
WITHIN a given (lr, bs, stage) cell, where only the seed varies?

Approach:
  1. Remove confound features (wall_time, steps, batch_size, lr, stage)
  2. Demean X and y within each (lr, bs, stage) cell — removes between-cell
     variation entirely. All remaining signal is seed-to-seed variation.
  3. K-fold CV on the demeaned data.
  4. Compare: ppl_only vs all_features vs gradient_only.
  5. Also report within-cell Spearman correlations as a simpler diagnostic.

Outputs:
  results/cv_results.json   — machine-readable for plotting
  results/cv_output.txt     — human-readable summary

Usage:
    python cv_analysis.py [--results path/to/milestone_features.jsonl] [--folds 10]
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy import stats as sp_stats

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

from analyze_features import load_records, extract_feature_matrix


# Features to drop: confounds and config params
CONFOUND_FEATURES = {"wall_time", "steps", "batch_size", "lr", "stage"}


def filter_features(X, feature_names, drop_set):
    """Remove features in drop_set. Returns (X_filtered, filtered_names)."""
    keep = [i for i, name in enumerate(feature_names) if name not in drop_set]
    return X[:, keep], [feature_names[i] for i in keep]


def remove_constant(X, feature_names):
    """Remove features with zero variance."""
    valid = np.std(X, axis=0) > 1e-12
    return X[:, valid], [n for n, v in zip(feature_names, valid) if v]


def demean_within_cells(X, y, cell_ids):
    """Subtract cell means from X and y. Returns demeaned copies.

    After this, all between-cell variation is gone. Only within-cell
    (seed-to-seed) variation remains.
    """
    X_dm = X.copy()
    y_dm = y.copy()

    unique_cells = np.unique(cell_ids)
    for cell in unique_cells:
        mask = cell_ids == cell
        X_dm[mask] -= X_dm[mask].mean(axis=0)
        y_dm[mask] -= y_dm[mask].mean()

    return X_dm, y_dm


def cell_id_array(records):
    """Build cell ID string for each record: 'lr{}_bs{}_stage{}'."""
    return np.array([
        f"lr{r['config']['lr']}_bs{r['config']['batch_size']}_stage{r['stage']}"
        for r in records
    ])


def config_cell_array(records):
    """Build config cell ID (no stage): 'lr{}_bs{}'."""
    return np.array([
        f"lr{r['config']['lr']}_bs{r['config']['batch_size']}"
        for r in records
    ])


def cv_evaluate(X, y, model_class, model_kwargs, n_folds):
    """Run k-fold CV. Returns metrics dict."""
    if X.shape[1] == 0 or np.std(y) < 1e-12:
        y_pred = np.full_like(y, 0.0)
        return {
            "r2_per_fold": [0.0] * n_folds,
            "mae_per_fold": [0.0] * n_folds,
            "r2_overall": 0.0,
            "mae_overall": float(np.mean(np.abs(y))),
        }

    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    y_pred = np.zeros_like(y)
    r2_per_fold = []
    mae_per_fold = []

    scaler = StandardScaler()

    for train_idx, test_idx in kf.split(X, y):
        X_train = scaler.fit_transform(X[train_idx])
        X_test = scaler.transform(X[test_idx])
        y_train, y_test = y[train_idx], y[test_idx]

        model = model_class(**model_kwargs)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        y_pred[test_idx] = preds

        if len(y_test) > 1 and np.std(y_test) > 1e-12:
            r2_per_fold.append(float(r2_score(y_test, preds)))
        else:
            r2_per_fold.append(float("nan"))
        mae_per_fold.append(float(mean_absolute_error(y_test, preds)))

    return {
        "r2_per_fold": r2_per_fold,
        "mae_per_fold": mae_per_fold,
        "r2_overall": float(r2_score(y, y_pred)),
        "mae_overall": float(mean_absolute_error(y, y_pred)),
        "y_true": y.tolist(),
        "y_pred": y_pred.tolist(),
    }


def within_cell_spearman(X, y, feature_names, cell_ids):
    """Compute average within-cell Spearman correlation for each feature.

    For each cell (10 seeds), compute Spearman(feature, time_to_next).
    Average across cells (Fisher z-transform for proper averaging).
    """
    unique_cells = np.unique(cell_ids)
    results = []

    for j, name in enumerate(feature_names):
        z_values = []
        raw_corrs = []
        for cell in unique_cells:
            mask = cell_ids == cell
            if mask.sum() < 4:
                continue
            x_cell = X[mask, j]
            y_cell = y[mask]
            if np.std(x_cell) < 1e-12 or np.std(y_cell) < 1e-12:
                continue
            sr, _ = sp_stats.spearmanr(x_cell, y_cell)
            if not np.isnan(sr):
                raw_corrs.append(sr)
                # Fisher z-transform for averaging
                z = np.arctanh(np.clip(sr, -0.999, 0.999))
                z_values.append(z)

        if z_values:
            mean_z = np.mean(z_values)
            mean_r = np.tanh(mean_z)  # back-transform
            std_r = np.std(raw_corrs)
            n_cells = len(z_values)
        else:
            mean_r = 0.0
            std_r = 0.0
            n_cells = 0

        results.append({
            "feature": name,
            "mean_spearman": mean_r,
            "std_spearman": std_r,
            "n_cells": n_cells,
        })

    results.sort(key=lambda x: abs(x["mean_spearman"]), reverse=True)
    return results


def run_comparison(X_dm, y_dm, feature_names, n_folds, label):
    """Compare ppl_only vs all_features vs gradient_only on demeaned data."""
    results = {}

    ppl_only_drop = set(feature_names) - {"ppl"}
    gradient_drop = CONFOUND_FEATURES | {"ppl"}

    feature_sets = {
        "ppl_only": filter_features(X_dm, feature_names, ppl_only_drop),
        "all_features": filter_features(X_dm, feature_names, CONFOUND_FEATURES),
        "gradient_only": filter_features(X_dm, feature_names, gradient_drop),
    }

    # Clean each
    for key in feature_sets:
        X_v, names_v = feature_sets[key]
        feature_sets[key] = remove_constant(X_v, names_v)

    models = [
        ("ridge", Ridge, {"alpha": 1.0}),
        ("rf", RandomForestRegressor, {"n_estimators": 100, "random_state": 42,
                                       "n_jobs": -1, "max_depth": 5}),
    ]

    for model_name, model_class, model_kwargs in models:
        for variant_name, (X_v, names_v) in feature_sets.items():
            key = f"{model_name}_{variant_name}"
            n = min(n_folds, len(y_dm) // 2)
            if n < 2 or len(y_dm) < 10:
                results[key] = {
                    "r2_overall": float("nan"),
                    "mae_overall": float("nan"),
                    "n_features": len(names_v),
                    "n_samples": len(y_dm),
                    "features": names_v,
                }
                continue

            res = cv_evaluate(X_v, y_dm, model_class, model_kwargs, n)
            res["features"] = names_v
            res["n_features"] = len(names_v)
            res["n_samples"] = len(y_dm)
            results[key] = res

    return results


def print_table(results, label, out):
    """Print comparison table."""
    def p(s=""):
        print(s)
        out.write(s + "\n")

    p(f"\n{'=' * 75}")
    p(f"  {label}")
    p(f"{'=' * 75}")
    p(f"  {'Model':<30} {'R²(CV)':>10} {'MAE(CV)':>10} {'n_feat':>8} {'n':>6}")
    p(f"  {'-' * 68}")

    order = ["ridge_ppl_only", "ridge_gradient_only", "ridge_all_features",
             "rf_ppl_only", "rf_gradient_only", "rf_all_features"]
    for key in order:
        if key not in results:
            continue
        r = results[key]
        r2 = r.get("r2_overall", float("nan"))
        mae = r.get("mae_overall", float("nan"))
        nf = r["n_features"]
        n = r["n_samples"]
        r2_s = f"{r2:>10.4f}" if not np.isnan(r2) else f"{'n/a':>10}"
        mae_s = f"{mae:>10.2f}" if not np.isnan(mae) else f"{'n/a':>10}"
        p(f"  {key:<30} {r2_s} {mae_s} {nf:>8} {n:>6}")

    # Per-fold detail for key models
    p()
    for key in ["ridge_ppl_only", "ridge_all_features", "rf_all_features"]:
        if key not in results or "r2_per_fold" not in results[key]:
            continue
        folds = results[key]["r2_per_fold"]
        valid = [f for f in folds if not np.isnan(f)]
        if valid:
            p(f"  {key:<30} fold R²: {np.mean(valid):.4f} +/- {np.std(valid):.4f}")
    p()


def main():
    parser = argparse.ArgumentParser(description="K-fold CV analysis (within-cell)")
    parser.add_argument(
        "--results",
        default=str(Path(__file__).parent / "results" / "milestone_features.jsonl"),
    )
    parser.add_argument("--folds", type=int, default=10)
    args = parser.parse_args()

    warnings.filterwarnings("ignore")

    records = load_records(args.results)
    if not records:
        print(f"No records found in {args.results}")
        sys.exit(1)

    X, y, feature_names = extract_feature_matrix(records)
    cell_ids = cell_id_array(records)
    config_cells = config_cell_array(records)
    stages = np.array([r["stage"] for r in records])

    print(f"Loaded {len(records)} records, {X.shape[1]} raw features")
    print(f"Confounds removed: {sorted(CONFOUND_FEATURES)}")
    print(f"Cells (lr x bs x stage): {len(np.unique(cell_ids))}")
    print(f"Seeds per cell: ~{len(records) // len(np.unique(cell_ids))}")
    print()

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "cv_output.txt"
    json_path = results_dir / "cv_results.json"

    all_json = {}

    with open(out_path, "w") as out:
        def p(s=""):
            print(s)
            out.write(s + "\n")

        p(f"Within-Cell K-Fold Cross-Validation (k={args.folds})")
        p(f"Confounds removed: {sorted(CONFOUND_FEATURES)}")
        p(f"Demeaning within each (lr, bs, stage) cell")
        p(f"Total: {len(records)} records, {len(np.unique(cell_ids))} cells")
        p()

        # ---------------------------------------------------------------
        # 1. Within-cell Spearman correlations (simple diagnostic)
        # ---------------------------------------------------------------
        p("=" * 75)
        p("  WITHIN-CELL SPEARMAN CORRELATIONS (averaged across cells)")
        p("=" * 75)
        p(f"  {'Feature':<35} {'Mean r_s':>10} {'Std':>10} {'n_cells':>8}")
        p(f"  {'-' * 63}")

        # Filter to non-confound features for this table
        X_clean, names_clean = filter_features(X, feature_names, CONFOUND_FEATURES)
        spearman_results = within_cell_spearman(X_clean, y, names_clean, cell_ids)
        for sr in spearman_results:
            p(f"  {sr['feature']:<35} {sr['mean_spearman']:>10.4f} "
              f"{sr['std_spearman']:>10.4f} {sr['n_cells']:>8}")
        p()

        all_json["within_cell_spearman"] = spearman_results

        # ---------------------------------------------------------------
        # 2. Overall CV on demeaned data (all stages pooled)
        # ---------------------------------------------------------------
        X_dm, y_dm = demean_within_cells(X, y, cell_ids)

        res = run_comparison(X_dm, y_dm, feature_names, args.folds,
                             "Overall (demeaned within lr,bs,stage cells)")
        all_json["overall_demeaned"] = {
            k: {kk: vv for kk, vv in v.items() if kk != "y_true" and kk != "y_pred"}
            for k, v in res.items()
        }
        print_table(res, f"OVERALL DEMEANED (n={len(y_dm)}, {args.folds}-fold CV)", out)

        # ---------------------------------------------------------------
        # 3. Per-stage CV on demeaned data
        # ---------------------------------------------------------------
        unique_stages = sorted(set(stages))
        for s in unique_stages:
            mask = stages == s
            config_cells_s = config_cells[mask]

            # Demean within (lr, bs) cells for this stage
            X_s, y_s = demean_within_cells(X[mask], y[mask], config_cells_s)

            n_folds_s = min(args.folds, len(y_s) // 2)
            if n_folds_s < 2:
                continue

            res_s = run_comparison(X_s, y_s, feature_names, n_folds_s, f"Stage {s}")
            stage_key = f"stage_{s}"
            all_json[stage_key] = {
                k: {kk: vv for kk, vv in v.items() if kk != "y_true" and kk != "y_pred"}
                for k, v in res_s.items()
            }
            print_table(res_s,
                        f"STAGE {s} DEMEANED within (lr,bs) (n={mask.sum()}, {n_folds_s}-fold)",
                        out)

            # Per-stage within-cell Spearman
            sp_s = within_cell_spearman(X_clean[mask], y[mask], names_clean,
                                        config_cells_s)
            all_json[f"spearman_stage_{s}"] = sp_s

        # ---------------------------------------------------------------
        # 4. Summary table
        # ---------------------------------------------------------------
        p("=" * 75)
        p("  SUMMARY: gradient features vs ppl-only (R² from CV)")
        p("=" * 75)
        p(f"  {'Section':<18} {'Model':<8} {'ppl':>8} {'all':>8} "
          f"{'grad':>8} {'delta':>8}")
        p(f"  {'-' * 60}")

        for section_key in ["overall_demeaned"] + [f"stage_{s}" for s in unique_stages]:
            if section_key not in all_json:
                continue
            sec = all_json[section_key]
            label_s = section_key.replace("_demeaned", "").upper()

            for mt in ["ridge", "rf"]:
                ppl_r2 = sec.get(f"{mt}_ppl_only", {}).get("r2_overall", float("nan"))
                all_r2 = sec.get(f"{mt}_all_features", {}).get("r2_overall", float("nan"))
                grad_r2 = sec.get(f"{mt}_gradient_only", {}).get("r2_overall", float("nan"))

                if np.isnan(ppl_r2) or np.isnan(all_r2):
                    continue

                delta = all_r2 - ppl_r2
                marker = " ***" if delta > 0.05 else " *" if delta > 0.01 else ""
                p(f"  {label_s:<18} {mt:<8} {ppl_r2:>8.4f} {all_r2:>8.4f} "
                  f"{grad_r2:>8.4f} {delta:>+8.4f}{marker}")
        p()
        p("  delta = all_features R² - ppl_only R²")
        p("  * = delta > 0.01,  *** = delta > 0.05")
        p()

    # Save JSON
    with open(json_path, "w") as f:
        json.dump(all_json, f, indent=2, default=str)

    print(f"Results saved to {out_path} and {json_path}")


if __name__ == "__main__":
    main()
