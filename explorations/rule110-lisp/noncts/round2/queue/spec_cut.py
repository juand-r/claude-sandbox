"""Cut out the synthesis specification for option (c), a leader that reads
differently after an acceptor than after a rejector.

For tape YYNN (first read Y: acceptor) and NYYN (first read N: rejector)
we save the exact Rule 110 row, in a lab window that follows the Ebar frame
around the first raw leader K, at a time shortly before the answer reaches
K. We also save the same window AFTER the reaction, for the plain K
(target P, normal reader) and for the E9 variant (forced-N reader). All
rows are exact simulations (casim.Run). File: spec_c.npz, with keys
<case>_row, <case>_t, <case>_x0 (global column of the window's first cell)."""
import numpy as np
from splice import *

def window_at(m, row, t, lo, hi):
    r = Run(row, m.origin)
    r.step(t)
    sh = r.ebar_frame(t)
    return r.window(lo + sh, hi + sh), lo + sh - m.origin

out = {}
for tape, t_before in (("YYNN", 13000), ("NYYN", 8300)):
    m = Machine(tape, ["YNNNNN"], 30000, left_periods=3, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    w, x0 = window_at(m, m.row, t_before, K - 700, K + 500)
    out[f"{tape}_before_row"], out[f"{tape}_before_t"], out[f"{tape}_before_x0"] = w, t_before, x0
    for label, row in (("plainK", m.row),
                       ("E9", replace_exact(m.row, m.origin + K + 41, m.origin + K + 72,
                                            [(en_tiles(9), 14, 9)], 0, 0))):
        w, x0 = window_at(m, row, t_before + 4000, K - 700, K + 500)
        out[f"{tape}_{label}_after_row"] = w
        out[f"{tape}_{label}_after_t"] = t_before + 4000
        out[f"{tape}_{label}_after_x0"] = x0
np.savez_compressed("spec_c.npz", **out)
print(sorted(out))
