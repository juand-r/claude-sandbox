// Run from this folder: NODE_PATH=$(npm root -g) node mathwrap.js [deck.html]
// Checks every formula on every slide, at several screen sizes:
//  - an inline formula (.math) must not break across lines (except on phones, where the decks let
//    formulas wrap rather than overflow);
//  - no formula (.math, .dm, .eq) may stick out of the text block that holds it.
// Prints each problem with its slide; exits with code 1 if there are any.
const { chromium } = require('playwright');
const path = require('path');
const deck = path.resolve(__dirname, process.argv[2] || '../svm_lecture.html');
const SIZES = [[1440, 810], [1280, 720], [1920, 1080], [1024, 768], [390, 844]];
(async () => {
  const b = await chromium.launch();
  let problems = 0;
  for (const [W, H] of SIZES) {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    await p.goto('file://' + deck); await p.waitForTimeout(700);
    const found = await p.evaluate(() => {
      const out = [];
      document.querySelectorAll('.slide').forEach(sl => {
        sl.querySelectorAll('.math, .eq').forEach(el => {
          const t = el.textContent.replace(/\s+/g, ' ').trim();
          const block = el.closest('li, p, td, .card, .tile, .prose, .eq:not(:scope)') || sl;
          if (innerWidth > 620 && el.classList.contains('math') && !el.classList.contains('dm') && el.getClientRects().length > 1)
            out.push(`${sl.id}: breaks across lines: "${t}"`);
          const r = el.getBoundingClientRect(), rb = block.getBoundingClientRect();
          if (r.width && r.right > rb.right + 1) out.push(`${sl.id}: sticks out by ${Math.round(r.right - rb.right)}px: "${t}"`);
          if (el.classList.contains('eq') && el.scrollWidth > el.clientWidth + 1) out.push(`${sl.id}: equation box scrolls: "${t}"`);
        });
      });
      return out;
    });
    console.log(`${W}×${H}: ${found.length ? found.length + ' problem(s)' : 'ok'}`);
    found.forEach(f => console.log('   ' + f));
    problems += found.length;
    await p.close();
  }
  await b.close();
  process.exit(problems ? 1 : 0);
})();
