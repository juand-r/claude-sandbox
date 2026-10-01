from adaptive import build, outcome, e_key
prog = "JJJJJNZ"
base = [1, 0, 2, 1, 0]
for cn in range(3):
    for cz in range(3):
        res = []
        for v in (0, 2, 9):
            st, log = outcome(build(["I"] * v + list(prog), [0] * v + base + [cn, cz]))
            try:
                res.append((v, e_key(st)))
            except Exception:
                res.append((v, "bad", [g[0] for g in st] if st else None))
        print(cn, cz, res)
