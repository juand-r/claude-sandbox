// Run from this folder: NODE_PATH=$(npm root -g) node export.js
// Runs the deck's own tree, kNN and SVR code on the deck's datasets and writes tests/deck_outputs.json,
// which ../check_numbers.py compares with scikit-learn.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(), p = await b.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(__dirname, '../nonlinear_regression_lecture.html')); await p.waitForTimeout(500);
  const out = await p.evaluate(() => {
    const N = window.__nlr, { DOSE, LIN, BMD, TWO } = N.DATA;
    const grid = (a, b, n) => Array.from({ length: n + 1 }, (_, i) => a + (b - a) * i / n);
    const gx = grid(0.05, 39.95, 400);          // never exactly on a threshold
    const trees = [];
    for (let m = 2; m <= 19; m++) { const T = N.growTree(DOSE.x, DOSE.y, { minSplit: m });
      trees.push({ minSplit: m, leaves: N.leafIntervals(T, 0, 40), pred: gx.map(v => N.predictTree(T, v)) }); }
    const knnGrid = grid(10, 85, 300);
    const knn = [1, 9, 40].map(k => ({ k, at40: N.knnPredict(BMD.x, BMD.y, 40, k).value, pred: knnGrid.map(v => N.knnPredict(BMD.x, BMD.y, v, k).value),
      train: BMD.x.map(v => N.knnPredict(BMD.x, BMD.y, v, k).value) }));
    const g2 = []; for (let i = 0; i < 20; i++) for (let j = 0; j < 20; j++) g2.push([(i + .5) / 2, (j + .5) / 2]);
    const knn2 = [1, 9].map(k => ({ k, pred: g2.map(q => N.knnPredict(TWO.X, TWO.y, q, k).value) }));
    const svr = [];
    const run = (name, data, o, gridX) => { const X = data.x.map(v => [v]), K = o.kernel === 'rbf' ? N.KERNEL.rbf(o.gamma) : N.KERNEL.linear();
      const m = N.svrSolve(X, data.y, { C: o.C, eps: o.eps, K }), st = N.tubeStats(m, data.x, data.y, o.eps);
      svr.push({ name, data: name.split(' ')[0], ...o, coef: m.coef, b: m.b, w: m.w || null, iters: m.iters, grid: gridX, pred: gridX.map(v => m.f([v])), out: st.out, slack: st.slack, sse: st.sse }); };
    for (const v of [1, 4, 8, 16, 24]) run(`LIN eps=${v / 4}`, LIN, { kernel: 'linear', C: 0.1, eps: v / 4 }, grid(0, 10, 50));
    for (const C of [0.01, 0.1, 10]) run(`LIN C=${C}`, LIN, { kernel: 'linear', C, eps: 2 }, grid(0, 10, 50));
    run('DOSE linear', DOSE, { kernel: 'linear', C: 1000, eps: 5 }, gx);
    for (const g of [0.02, 10 ** -0.7, 0.001, 1]) run(`DOSE rbf g=${g}`, DOSE, { kernel: 'rbf', gamma: g, C: 1000, eps: 5 }, gx);
    const ols = N.olsFit(DOSE.x, DOSE.y);
    return { data: N.DATA, gx, trees, splits: N.scanSplits(DOSE.x, DOSE.y), knnGrid, knn, g2, knn2, svr, ols };
  });
  fs.writeFileSync(path.join(__dirname, 'deck_outputs.json'), JSON.stringify(out));
  console.log('wrote deck_outputs.json; errors', JSON.stringify(errs));
  await b.close();
})();
