"""
Analyze milestone features: which features predict time_to_next_milestone?

Reads the JSONL output from run_experiment.py and runs:
1. Pearson/Spearman correlations
2. Linear regression with standardized coefficients
3. Random forest feature importance
4. Per-stage breakdown (do predictive features change across stages?)

Usage:
    python analyze_features.py [--results path/to/milestone_features.jsonl]
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

# Optional imports — we degrade gracefully if sklearn is missing
try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# Features that are per-layer vectors (variable number of keys).
# We'll detect them by prefix and aggregate (mean) for the regression.
LAYER_PREFIXES = ("grad_layer_norm_", "weight_layer_norm_")


def load_records(path: str) -> list:
    records = []
    with open(path) as f:
        for line in f:
            r = json.loads(line.strip())
            if r["time_to_next"] is not None:
                records.append(r)
    return records


def extract_feature_matrix(records: list):
    """Extract (X, y, feature_names) from records.

    Per-layer features are aggregated to mean + std.
    Returns X (n_samples, n_features), y (n_samples,), feature_names list.
    """
    # First pass: collect all feature keys and identify layer features
    all_keys = set()
    for r in records:
        all_keys.update(r["features"].keys())

    # Separate scalar features from layer features
    scalar_keys = sorted(k for k in all_keys
                         if not any(k.startswith(p) for p in LAYER_PREFIXES))
    layer_groups = {}
    for k in all_keys:
        for prefix in LAYER_PREFIXES:
            if k.startswith(prefix):
                if prefix not in layer_groups:
                    layer_groups[prefix] = []
                layer_groups[prefix].append(k)

    # Build feature names: scalar features + aggregated layer features
    feature_names = list(scalar_keys)
    for prefix in sorted(layer_groups.keys()):
        feature_names.append(f"{prefix}mean")
        feature_names.append(f"{prefix}std")

    # Build matrix
    X = np.zeros((len(records), len(feature_names)))
    y = np.zeros(len(records))

    for i, r in enumerate(records):
        feat = r["features"]
        y[i] = r["time_to_next"]

        for j, name in enumerate(feature_names):
            if name in feat:
                X[i, j] = float(feat[name])
            elif name.endswith("mean"):
                prefix = name[:-4]
                vals = [float(feat[k]) for k in layer_groups.get(prefix, []) if k in feat]
                X[i, j] = np.mean(vals) if vals else 0.0
            elif name.endswith("std"):
                prefix = name[:-3]
                vals = [float(feat[k]) for k in layer_groups.get(prefix, []) if k in feat]
                X[i, j] = np.std(vals) if vals else 0.0

    return X, y, feature_names


def correlations(X, y, feature_names):
    """Compute Pearson and Spearman correlations."""
    from scipy import stats as sp_stats

    print("=" * 70)
    print("CORRELATIONS WITH time_to_next")
    print("=" * 70)
    print(f"{'Feature':<35} {'Pearson':>10} {'Spearman':>10}")
    print("-" * 55)

    results = []
    for j, name in enumerate(feature_names):
        col = X[:, j]
        if np.std(col) < 1e-12:
            continue
        pearson_r, pearson_p = sp_stats.pearsonr(col, y)
        spearman_r, spearman_p = sp_stats.spearmanr(col, y)
        results.append((name, pearson_r, spearman_r, abs(spearman_r)))

    # Sort by absolute Spearman
    results.sort(key=lambda x: x[3], reverse=True)
    for name, pr, sr, _ in results:
        print(f"  {name:<33} {pr:>10.4f} {sr:>10.4f}")
    print()


def linear_regression(X, y, feature_names):
    """Linear regression with standardized coefficients."""
    if not HAS_SKLEARN:
        print("sklearn not installed, skipping linear regression.")
        return

    print("=" * 70)
    print("LINEAR REGRESSION (standardized coefficients)")
    print("=" * 70)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Remove constant features
    valid = np.std(X_scaled, axis=0) > 1e-12
    X_valid = X_scaled[:, valid]
    valid_names = [n for n, v in zip(feature_names, valid) if v]

    reg = LinearRegression()
    reg.fit(X_valid, y)
    r2 = reg.score(X_valid, y)
    print(f"  R² = {r2:.4f}  (n={len(y)})")
    print()

    # Sort by absolute coefficient
    coefs = list(zip(valid_names, reg.coef_))
    coefs.sort(key=lambda x: abs(x[1]), reverse=True)
    print(f"  {'Feature':<35} {'Coefficient':>12}")
    print("  " + "-" * 47)
    for name, coef in coefs[:20]:
        print(f"  {name:<35} {coef:>12.4f}")
    print()


def random_forest(X, y, feature_names):
    """Random forest feature importance."""
    if not HAS_SKLEARN:
        print("sklearn not installed, skipping random forest.")
        return

    print("=" * 70)
    print("RANDOM FOREST FEATURE IMPORTANCE")
    print("=" * 70)

    # Remove constant features
    valid = np.std(X, axis=0) > 1e-12
    X_valid = X[:, valid]
    valid_names = [n for n, v in zip(feature_names, valid) if v]

    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_valid, y)
    r2 = rf.score(X_valid, y)
    print(f"  R² (in-sample) = {r2:.4f}  (n={len(y)})")
    print()

    importances = list(zip(valid_names, rf.feature_importances_))
    importances.sort(key=lambda x: x[1], reverse=True)
    print(f"  {'Feature':<35} {'Importance':>12}")
    print("  " + "-" * 47)
    for name, imp in importances[:20]:
        print(f"  {name:<35} {imp:>12.4f}")
    print()


def per_stage_analysis(records, X, y, feature_names):
    """Check if predictive features change across stages."""
    print("=" * 70)
    print("PER-STAGE CORRELATIONS (Spearman with time_to_next)")
    print("=" * 70)

    from scipy import stats as sp_stats

    stages = sorted(set(r["stage"] for r in records))
    stage_array = np.array([r["stage"] for r in records])

    # Header
    stage_labels = [f"Stage {s}" for s in stages]
    header = f"  {'Feature':<30}" + "".join(f"{s:>10}" for s in stage_labels)
    print(header)
    print("  " + "-" * (30 + 10 * len(stages)))

    # For each feature, compute Spearman within each stage
    top_features = []
    for j, name in enumerate(feature_names):
        col = X[:, j]
        if np.std(col) < 1e-12:
            continue

        row = f"  {name:<30}"
        max_abs = 0
        for s in stages:
            mask = stage_array == s
            if mask.sum() < 3:
                row += f"{'n/a':>10}"
                continue
            sr, _ = sp_stats.spearmanr(col[mask], y[mask])
            row += f"{sr:>10.3f}"
            max_abs = max(max_abs, abs(sr))
        top_features.append((row, max_abs))

    # Sort by max absolute correlation across any stage
    top_features.sort(key=lambda x: x[1], reverse=True)
    for row, _ in top_features[:20]:
        print(row)
    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze predictive features")
    parser.add_argument(
        "--results",
        default=str(Path(__file__).parent / "results" / "milestone_features.jsonl"),
        help="Path to results JSONL file",
    )
    args = parser.parse_args()

    # Check dependencies
    try:
        from scipy import stats as sp_stats
    except ImportError:
        print("ERROR: scipy is required. Install with: pip install scipy")
        sys.exit(1)

    records = load_records(args.results)
    if not records:
        print(f"No records with time_to_next found in {args.results}")
        sys.exit(1)

    print(f"Loaded {len(records)} milestone records with time_to_next targets")
    print()

    X, y, feature_names = extract_feature_matrix(records)
    print(f"Feature matrix: {X.shape[0]} samples x {X.shape[1]} features")
    print()

    correlations(X, y, feature_names)
    linear_regression(X, y, feature_names)
    random_forest(X, y, feature_names)
    per_stage_analysis(records, X, y, feature_names)


if __name__ == "__main__":
    main()
