"""Recompute every numeric answer in the four exam versions A-D that a colleague made from final_midterm2
(question order shuffled, numbers changed; values transcribed by hand from Exam2_Version_{A,B,C,D}.pdf,
2026-10-19) and flag ties, rounding traps and inconsistencies. Run: .venv/bin/python check_versions.py"""
import math
sg = lambda z: 1 / (1 + math.exp(-z))
V = {
 'A': dict(cm=(400, 60, 50, 45), roc=([.95,.85,.70,.60,.50,.40,.30,.10], 'yynynynn'), auc=0.3,
           svm=((6, 8), -20, {'C': ((1.5, 1.5), 1), 'D': ((1.25, 1.5), -1), 'E': ((3, .5), -1)}),
           knn=([1,2,4,5,7,8], [3,6,4,8,10,12], 4.4), ens=(25, .6), steps=(1000, 5, 50),
           nn1=([[.5,-.5],[-.3,.4]], [.5,-.2], [[.6,.8],[-.2,-.9]], [-.4,.6], [4,2]),
           nn2=([[.5,-1],[1.5,.5]], [.5,-1], [1,-2], .5, [2,1], 1, (.62,.92,.33), (0,0), (0,0))),
 'B': dict(cm=(500, 80, 50, 40), roc=([.90,.80,.75,.65,.55,.45,.30,.20], 'ynyynynn'), auc=0.2,
           svm=((8, 6), -24, {'C': ((2.5, 1), -1), 'D': ((2, 1.5), 1), 'E': ((1.25, 2.25), -1)}),
           knn=([1,3,4,6,7,9], [2,5,3,9,6,11], 5.4), ens=(21, .65), steps=(2000, 4, 100),
           nn1=([[.1,-.7],[.1,.3]], [-.2,-.4], [[-.8,-.5],[-.4,-.8]], [-.2,.3], [2,4]),
           nn2=([[-2,2],[1,-.5]], [-.5,.5], [.5,-.5], -1, [2,2], 1, (.38,.82,.23), (0,1), (1,0))),
 'C': dict(cm=(600, 120, 80, 72), roc=([.97,.88,.72,.66,.52,.41,.33,.12], 'nynyyynn'), auc=0.4,
           svm=((3, 4), -10, {'C': ((1.5, 1.25), -1), 'D': ((2, 1.5), -1), 'E': ((1, 2), 1)}),
           knn=([0,2,3,5,6,8], [1,3,2,7,5,9], 3.6), ens=(31, .55), steps=(1200, 3, 40),
           nn1=([[-.4,.6],[-.8,-.6]], [-.4,.2], [[-.8,-.9],[-.3,.9]], [-.3,.5], [1,3]),
           nn2=([[-1,1],[-.5,1.5]], [1.5,-.5], [-1,1], 1, [3,3], 0, (.82,.92,.75), (0,0), (0,1))),
 'D': dict(cm=(250, 50, 40, 30), roc=([.93,.82,.74,.62,.58,.44,.27,.08], 'nyynyynn'), auc=0.25,
           svm=((8, -6), -10, {'C': ((2.25, 1), -1), 'D': ((1.75, .75), -1), 'E': ((1.75, .5), 1)}),
           knn=([2,3,5,6,8,9], [4,7,4,9,11,13], 6.7), ens=(15, .7), steps=(800, 6, 20),
           nn1=([[-.4,-.2],[.7,-.7]], [.6,-.2], [[.1,.5],[-.6,.5]], [.1,-.1], [4,3]),
           nn2=([[.5,-1.5],[-.5,.5]], [.5,1.5], [2,-1.5], -1.5, [3,1], 1, (.62,.62,.23), (0,1), (1,1))),
}
lin = lambda W, b, x: [sum(w*u for w, u in zip(r, x)) + c for r, c in zip(W, b)]
for v, d in V.items():
    print(f"================= version {v}")
    n, ai, fl, fla = d['cm']; tp, fp = fla, fl - fla; fn, tn = ai - tp, n - ai - fp
    assert min(tp, fp, fn, tn) >= 0
    print(f"Q1 confusion: TP={tp} FP={fp} FN={fn} TN={tn}; precision={tp/(tp+fp):.4f} recall={tp/ai:.4f}")
    sc, lab = d['roc']; assert len(set(sc)) == 8 and sorted(sc, reverse=True) == sc and lab.count('y') == 4
    pts, t, f = [], 0, 0
    for l in lab[:3]:
        t += l == 'y'; f += l == 'n'; pts.append((f/4, t/4))
    auc = sum((sum(1 for j in range(8) if lab[j]=='n' and j>i)) for i in range(8) if lab[i]=='y')/16
    print(f"   ROC next three points: {pts}; this table's own AUC {auc}; flipped detector AUC {1-d['auc']:.2f}")
    (w, b, P) = d['svm']; nw = math.hypot(*w)
    out = {k: (w[0]*x[0] + w[1]*x[1] + b, y) for k, (x, y) in P.items()}
    cats = {k: ('on margin' if math.isclose(y*f, 1) else 'inside' if 0 < y*f < 1 else 'misclassified' if y*f < 0 else 'outside')
            for k, (f, y) in out.items()}
    print(f"Q2 SVM: |w|={nw} margin={2/nw}; f={ {k:round(f,4) for k,(f,y) in out.items()} }; {cats}")
    xs, ys, x0 = d['knn']; dist = sorted((abs(x - x0), y, x) for x, y in zip(xs, ys))
    assert dist[0][0] != dist[1][0] and dist[2][0] != dist[3][0], "kNN tie"
    print(f"Q3 kNN at {x0}: k=1 -> {dist[0][1]} (x={dist[0][2]}); k=3 -> {sum(t[1] for t in dist[:3])/3:.4f} (x={[t[2] for t in dist[:3]]}); 4th neighbour at distance {dist[3][0]:.1f}")
    m, e = d['ens']; pm = sum(math.comb(m, k) * e**k * (1-e)**(m-k) for k in range(m//2 + 1, m + 1))
    print(f"Q5 ensemble: {m} classifiers, error {e}: majority-vote error {pm:.4f} (> {e})" if m % 2 else "even number!")
    N, ep, bs = d['steps']; assert N % bs == 0
    print(f"Q4.3 steps: batch {ep}, SGD {N*ep}, mini-batch {ep*N//bs}")
    W1, b1, W2, b2, x = d['nn1']; zB = lin(W1, b1, x); B = [max(0, z) for z in zB]; C = lin(W2, b2, B); Cn = lin(W2, b2, zB)
    assert all(abs(z) > 1e-9 for z in zB)
    print(f"Q4.1: zB={[round(z,4) for z in zB]} B={[round(z,4) for z in B]} out={[round(c,4) for c in C]} -> Class {'A' if C[0]>C[1] else 'B'}; "
          f"without ReLU {[round(c,4) for c in Cn]} -> Class {'A' if Cn[0]>Cn[1] else 'B'}")
    W1, b1, W2, b2, A, y, given, (k, j), (wj, wi) = d['nn2']
    zB = lin(W1, b1, A); B = [sg(z) for z in zB]; p = sg(sum(w*u for w, u in zip(W2, B)) + b2)
    gB1, gB2, gp = given
    print(f"Q4.2: exact B=({B[0]:.4f},{B[1]:.4f}) p={p:.4f}; given ({gB1},{gB2},{gp}) -> match: {round(B[0],2)==gB1 and round(B[1],2)==gB2 and round(p,2)==gp}")
    Bg = [gB1, gB2]; err = gp - y
    # (a) output weight from hidden unit j (index j) ; (b) first-layer weight into hidden unit wj from input wi
    ga = err * Bg[j]; old_a = W2[j]
    gb = err * W2[wj] * Bg[wj] * (1 - Bg[wj]) * A[wi]; old_b = W1[wj][wi]
    ga_x = (p - y) * B[j]; gb_x = (p - y) * W2[wj] * B[wj] * (1 - B[wj]) * A[wi]
    print(f"   (a) W2 from B{j+1}: grad {ga:.4f} -> {old_a - ga:.4f} (exact {old_a - ga_x:.4f}); "
          f"(b) W1 from A{wi+1} to B{wj+1}: grad {gb:.4f} -> {old_b - gb:.4f} (exact {old_b - gb_x:.4f})")
