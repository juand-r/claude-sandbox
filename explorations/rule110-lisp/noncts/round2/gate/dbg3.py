from adaptive import ref_key, outcome, build, e_key
for n in range(1, 10):
    print(n, ref_key(n))
# J as INC from E^2 vs GB5 as INC:
for prog, cl in (("IJ", [0, 0]), ("IJ", [0, 1]), ("IJ", [0, 2]), ("II", [0, 0])):
    st, _ = outcome(build(list(prog), cl))
    print(prog, cl, e_key(st))
