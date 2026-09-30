import sys, pickle
from collide import *
z = pickle.load(open('zoo.pkl','rb'))
by = {}
for g in z:
    by.setdefault(NAMES.get((g.dt,g.dx)), []).append(g)
# choose the narrowest representative of each type as the "single" glider
single = {k: min(v, key=lambda g: g.span()[1]-g.span()[0]) for k, v in by.items()}

def survey(xn, yn, gap=70, T=500, xi=None, yi=None):
    X = single[xn] if xi is None else by[xn][xi]
    Y = single[yn] if yi is None else by[yn][yi]
    res = {}
    for kx in range(X.dt):
        for ky in range(Y.dt):
            try:
                row = collide(X, Y, kx, ky, gap)
            except ValueError as e:
                continue
            out = tuple(k for a, b, k in outcome(row, T))
            res.setdefault(out, []).append((kx, ky))
    return res

if __name__ == "__main__":
    xn, yn = sys.argv[1], sys.argv[2]
    for out, ks in survey(xn, yn).items():
        print(len(ks), out)
