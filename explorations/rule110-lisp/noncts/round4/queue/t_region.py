from zscreen import *
S = setup()
for tape in S:
    K0, sc, _ = S[tape]
    seg = sc.seg
    cl_ = clusters(seg)
    rel = [(x + 0 - sc.ebar_to_seg(K0), y + 0 - sc.ebar_to_seg(K0)) for x, y in cl_]
    print(tape, [r for r in rel if -700 < r[0] < 200])
