"""Layer 2: Turing machines and the TM -> tag-system compiler (Cook 2009,
following Cocke-Minsky; exponential runtime, used for correctness tests
and small programs).

TM model (as in the paper): m states psi_1..psi_m, t symbols sigma_1..
sigma_t, two-way infinite tape with periodic backgrounds on both sides.
Lookup tables: write W[(i,j)] -> symbol index, move M[(i,j)] -> 'L'|'R'|'H',
next state G[(i,j)] -> state index (1-based indices throughout).

The tag system produced has deletion number s = t+2. Symbols are encoded
as strings like "H_3", "H_3_2", "R_3*" for H_{psi_3}, H_{psi_3 sigma_2},
R_{psi_3 *}. Tape symbols sigma_{t+1}, sigma_{t+2} mark where the explicit
tape portion meets the periodic background.
"""


class TM:
    def __init__(self, m, t, write, move, nxt):
        self.m, self.t = m, t
        self.write, self.move, self.nxt = write, move, nxt

    def run(self, state, left_bg, left, cur, right, right_bg, max_steps):
        """left: explicit symbols adjacent-first (b_1 nearest head);
        right likewise (d_1 nearest). Backgrounds repeat outward:
        left_bg = (a_1, ..., a_w) with a_1 nearest the explicit part.
        Yields (state, symbol_read) per step; stops on halt."""
        left, right = list(left), list(right)
        for _ in range(max_steps):
            yield state, cur
            i, j = state, cur
            mv = self.move[(i, j)]
            if mv == "H":
                return
            w = self.write[(i, j)]
            state = self.nxt[(i, j)]
            if mv == "L":
                right.insert(0, w)
                if not left:
                    left = list(left_bg)
                cur = left.pop(0)
            else:
                left.insert(0, w)
                if not right:
                    right = list(right_bg)
                cur = right.pop(0)


def tm_to_ts(tm, state, left_bg, left, cur, right, right_bg):
    """-> (rules, tape, s): tag system with deletion number s = t+2."""
    t, m = tm.t, tm.m
    s = t + 2
    rules = {}
    for i in range(1, m + 1):
        rules[f"H_{i}"] = [f"H_{i}_{j}" for j in range(1, s + 1)]
        rules[f"L_{i}"] = [f"L_{i}_{j}" for j in range(1, s + 1)]
        rules[f"R_{i}"] = [f"R_{i}_{j}" for j in range(1, s + 1)]
        rules[f"R_{i}*"] = [f"R_{i}"] * s
        for j in range(1, t + 1):
            mv = tm.move.get((i, j))
            if mv is None:
                continue
            if mv == "H":
                rules[f"H_{i}_{j}"] = []
                rules[f"L_{i}_{j}"] = []
                rules[f"R_{i}_{j}"] = []
                continue
            u = tm.write[(i, j)]
            g = tm.nxt[(i, j)]
            if mv == "L":
                rules[f"H_{i}_{j}"] = [f"R_{g}*"] * (s * (s - u)) + [f"H_{g}"] * j
                rules[f"L_{i}_{j}"] = [f"L_{g}"]
                rules[f"R_{i}_{j}"] = [f"R_{g}"] * (s * s)
            else:
                rules[f"H_{i}_{j}"] = [f"H_{g}"] * j + [f"L_{g}"] * (s * (s - u))
                rules[f"L_{i}_{j}"] = [f"L_{g}"] * (s * s)
                rules[f"R_{i}_{j}"] = [f"R_{g}"]
        # markers: sigma_{t+1} extends the left background,
        # sigma_{t+2} extends the right background
        a, e = left_bg, right_bg
        w_, z = len(a), len(e)
        rules[f"H_{i}_{t + 1}"] = (
            [f"H_{i}"] * (t + 1 + s - a[0])
            + [f"L_{i}"] * (s ** w_ + sum((s - a[k]) * s ** k for k in range(1, w_))))
        rules[f"H_{i}_{t + 2}"] = (
            [f"R_{i}*"] * sum((s - e[k]) * s ** k for k in range(1, z))
            + [f"H_{i}"] * (t + 2 + s - e[0]))
        rules[f"L_{i}_{t + 1}"] = [f"L_{i}"] * s
        rules[f"L_{i}_{t + 2}"] = [f"L_{i}"] * s
        rules[f"R_{i}_{t + 1}"] = [f"R_{i}"] * s
        rules[f"R_{i}_{t + 2}"] = [f"R_{i}"] * s

    x, y = len(left), len(right)
    b, d = left, right
    tape = (
        [f"H_{state}"] * (1 + s - cur)
        + [f"L_{state}"] * (s ** (x + 1) + sum((s - b[k]) * s ** (k + 1) for k in range(x)))
        + [f"R_{state}"] * sum((s - d[k]) * s ** (k + 1) for k in range(y)))
    return rules, tape, s


def ts_run_list(rules, tape, s, max_ts_steps):
    """Tag-system runner over list-of-strings tapes.
    Yields (n, tape_list) before each step."""
    tape = list(tape)
    for n in range(max_ts_steps):
        yield n, tape
        if len(tape) < s:
            return
        head = tape[0]
        app = rules[head]
        del tape[:s]
        tape.extend(app)
    yield max_ts_steps, tape
