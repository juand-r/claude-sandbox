import sys, verify_gate_wrap2 as V
for w in sys.argv[1:]:
    for k in range(1, len(w) + 1):
        got, exp = V.ca(w[:k]), V.model(w[:k])
        print(w[:k], got, exp, "OK" if got == exp else "MISMATCH", flush=True)
