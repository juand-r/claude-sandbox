from splice import *
T = 16000
REG = dict(A=(1181, 2489), T=(2489, 2935), B=(2935, 3823), K=(3823, 4375))
def classify(cs):
    out = {}
    for r, (a, b) in REG.items():
        out[r] = sum(1 for x, y, k in cs if a <= x < b and k == "E")
    out["other"] = [f"{k}{x}" for x, y, k in cs if k != "E"]
    return out
if __name__ == "__main__":
    for tape in ("YN", "NY"):
        m = Machine(tape, ["YNNNNN"], T)
        o = m.origin
        print(tape, "base", classify(m.run(m.row, T, 1100, 7000)))
        a, b = o + 2489, o + 2935
        print(" phases", phase_at(m.row, a), phase_at(m.row, b))
        new = replace_region(m.row, a, b, [])
        print(" empty sym3:", None if new is None else classify(m.run(new, T, 1100, 7000)))
