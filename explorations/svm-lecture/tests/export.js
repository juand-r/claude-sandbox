// Run the deck's own SVM solver on every dataset used in the slides and save the results
// to tests/solver_outputs.json, so check_numbers.py can compare them with scikit-learn.
// Run from this folder: NODE_PATH=$(npm root -g) node export.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(__dirname, '../svm_lecture.html'));
  await p.waitForTimeout(500);
  const out = await p.evaluate(() => {
    const S = window.__svm, lin = S.KERNEL.linear();
    const pack = (m, X) => ({ alpha: m.alpha, b: m.b, sv: m.sv, w: m.w || null, iters: m.iters });
    const grid = []; for (let i = 0; i <= 10; i++) for (let j = 0; j <= 10; j++) grid.push([i, j]);
    const res = { data: { SEP: S.SEP, SOFT: S.SOFT, RINGS: S.RINGS, XOR: S.XOR }, HARD_C: S.HARD_C, cases: [] };
    res.cases.push({ name: 'SEP hard', data: 'SEP', kernel: 'linear', C: S.HARD_C, ...pack(S.svmSolve(S.SEP.X, S.SEP.y, { C: S.HARD_C })) });
    for (const C of [0.01, 0.1, 1, 10, 100])
      res.cases.push({ name: `SOFT C=${C}`, data: 'SOFT', kernel: 'linear', C, ...pack(S.svmSolve(S.SOFT.X, S.SOFT.y, { C })) });
    const Z = S.RINGS.X.map(S.lift);
    res.cases.push({ name: 'RINGS lifted hard', data: 'RINGS_LIFTED', X: Z, kernel: 'linear', C: S.HARD_C, ...pack(S.svmSolve(Z, S.RINGS.y, { C: S.HARD_C })) });
    for (const d of ['RINGS', 'XOR']) {
      for (const [kern, g] of [['linear', null], ['rbf', 0.5], ['rbf', 10]]) {
        const K = kern === 'linear' ? lin : S.KERNEL.rbf(g), m = S.svmSolve(S[d].X, S[d].y, { C: 10, K });
        res.cases.push({ name: `${d} ${kern}${g ? ' g=' + g : ''}`, data: d, kernel: kern, gamma: g, C: 10, ...pack(m),
          grid, fgrid: grid.map(x => m.f(x)), ftrain: S[d].X.map(x => m.f(x)) });
      }
    }
    return res;
  });
  fs.writeFileSync(path.resolve(__dirname, 'solver_outputs.json'), JSON.stringify(out));
  console.log('cases', out.cases.length, 'errors', JSON.stringify(errs));
  await b.close();
})();
