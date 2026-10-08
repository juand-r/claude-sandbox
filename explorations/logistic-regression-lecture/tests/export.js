// Run from this folder: NODE_PATH=$(npm root -g) node export.js
// Runs the deck's own logistic regression and SVM code and writes tests/deck_outputs.json for ../check_numbers.py.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(), p = await b.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(__dirname, '../logistic_regression_lecture.html')); await p.waitForTimeout(500);
  const out = await p.evaluate(() => {
    const L = window.__lr, pick = m => ({ w: m.w, b: m.b });
    const thr = [5, 10, 30, 50, 70, 90, 95].map(v => { const t = v / 100, m = L.HOURS_FIT, { x, y } = L.HOURS;
      return { t, xs: -(m.b + Math.log(1 / t - 1)) / m.w[0], tp: x.filter((v, i) => y[i] > 0 && m.p([v]) >= t).length, fp: x.filter((v, i) => y[i] < 0 && m.p([v]) >= t).length }; });
    return { HOURS: L.HOURS, SOFT: L.SOFT, hours: pick(L.HOURS_FIT), softLR: pick(L.SOFT_LR), softSVM: { ...pick(L.SOFT_SVM), sv: L.SOFT_SVM.sv }, thr };
  });
  fs.writeFileSync(path.join(__dirname, 'deck_outputs.json'), JSON.stringify(out));
  console.log('wrote deck_outputs.json; errors', JSON.stringify(errs));
  await b.close();
})();
