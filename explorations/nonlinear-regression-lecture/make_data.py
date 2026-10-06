"""Make the deck's datasets and write them to build/data.json (build/assemble.py embeds them in the deck).

    .venv/bin/python make_data.py

DOSE is hand-made to look like the lecture's drug-dosage example (after Josh Starmer / StatQuest): low
effect at low doses, about 100% near 20 mg, falling again above 25 mg. Its values were chosen so that a
regression tree that does not split nodes of 6 or fewer points has the lecture's shape: split at 14.5,
then 29, then 23.5 (check_numbers.py confirms this with scikit-learn).
LIN, BMD and TWO are simulated with a fixed seed:
  LIN  16 points, y = 2x + 3 + noise (sd 2): linear support vector regression.
  BMD  56 people, bone density = 0.80 + 0.30 exp(-((age - 30)/22)^2) + noise (sd 0.035): kNN regression.
  TWO  45 points in [0, 10]^2, y = 10 + 3 sin(x1/1.6) + 0.8 x2 + noise (sd 0.6): kNN with two features.
"""
import json
from pathlib import Path

import numpy as np

r = np.random.default_rng(14)
xl = np.round(np.linspace(.8, 9.6, 16) + r.uniform(-.2, .2, 16), 1)
yl = np.round(2 * xl + 3 + r.normal(0, 2, 16), 1)
age = np.round(np.sort(r.uniform(12, 82, 56)), 0)
bmd = np.round(.80 + .30 * np.exp(-((age - 30) / 22) ** 2) + r.normal(0, .035, 56), 3)
X2 = np.round(r.uniform(0, 10, (45, 2)), 1)
y2 = np.round(10 + 3 * np.sin(X2[:, 0] / 1.6) + .8 * X2[:, 1] + r.normal(0, .6, 45), 1)
D = dict(DOSE=dict(x=[2, 4, 6, 8, 10, 13, 16, 18, 20, 22, 25, 26, 27, 28, 30, 32, 35, 37],
                   y=[0, 0, 0, 0, 5, 20, 98, 100, 102, 100, 66, 60, 50, 45, 10, 2, 0, 0]),
         LIN=dict(x=xl.tolist(), y=yl.tolist()), BMD=dict(x=[int(a) for a in age], y=bmd.tolist()),
         TWO=dict(X=X2.tolist(), y=y2.tolist()))
out = Path(__file__).parent / "build" / "data.json"
out.write_text(json.dumps(D, separators=(",", ":")))
print("wrote", out)
