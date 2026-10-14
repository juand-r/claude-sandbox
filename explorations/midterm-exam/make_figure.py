"""Fits for the exam's question 3.3: one data set, three models, written as data files for pgfplots.

Usage: .venv/bin/python make_figure.py   (writes latex/fig_data/*.dat)

Panel A: SVR with an RBF kernel (smooth). Panel B: regression tree with max depth 2 and at least 3 points per leaf (a few wide
steps). Panel C: kNN with k = 1 (a narrow step for every training point, through every point).
"""
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

SEED, N_POINTS, X_MAX, N_GRID = 3, 14, 10.0, 2001
out = Path(__file__).parent / "latex" / "fig_data"
out.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(SEED)
x = np.sort(rng.uniform(0.3, X_MAX - 0.3, N_POINTS))
y = 3 + 2 * np.sin(0.6 * x) + 0.3 * x + rng.normal(0, 0.5, N_POINTS)
X = x[:, None]
grid = np.linspace(0, X_MAX, N_GRID)[:, None]

models = {
    "svr": SVR(kernel="rbf", C=10, gamma=0.3, epsilon=0.2),
    "tree": DecisionTreeRegressor(max_depth=2, min_samples_leaf=3, random_state=0),
    "knn": KNeighborsRegressor(n_neighbors=1),
}
np.savetxt(out / "points.dat", np.c_[x, y], header="x y", comments="", fmt="%.4f")
for name, m in models.items():
    m.fit(X, y)
    np.savetxt(out / f"{name}.dat", np.c_[grid[:, 0], m.predict(grid)], header="x y", comments="", fmt="%.4f")
    print(f"{name}: {len(np.unique(np.round(m.predict(grid), 6)))} distinct predicted values on the grid")
tree = models["tree"]
print("tree leaves:", tree.get_n_leaves(), " thresholds:", np.round(np.sort(tree.tree_.threshold[tree.tree_.threshold > -2]), 2))
print("kNN k=1 reproduces every training point:", np.allclose(models["knn"].predict(X), y))
print("y range:", round(y.min(), 2), round(y.max(), 2))
