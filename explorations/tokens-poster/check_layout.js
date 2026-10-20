// Render poster-a0.html, save a preview PNG, and report each column's bottom against its box.
// Run: node check_layout.js  -> poster-a0-preview.png
const path = require('path');
const PW = process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright';
const { chromium } = require(PW);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 3179, height: 4494 } });
  await page.goto('file://' + path.join(__dirname, 'poster-a0.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  const report = await page.evaluate(() => {
    const boxes = [...document.querySelectorAll('[data-kit-shape]')].map((b) => ({ name: b.dataset.kitShape, r: b.getBoundingClientRect() }));
    const inside = (r, b) => r.left >= b.left - 1 && r.right <= b.right + 1 && r.top >= b.top - 1;
    const out = [];
    for (const el of document.querySelectorAll('.col, [data-kit]')) {
      const r = el.getBoundingClientRect();
      const owner = boxes.filter((b) => b.name.endsWith('box') && inside(r, b.r)).pop();
      if (owner) out.push({ el: el.dataset.kit || 'col', bottom: Math.round(r.bottom), boxBottom: Math.round(owner.r.bottom), slack: Math.round(owner.r.bottom - r.bottom) });
    }
    const p = document.getElementById('poster');
    return { cols: out.filter((o) => o.el === 'col'), tight: out.filter((o) => o.slack < 30), scroll: [p.scrollWidth, p.scrollHeight] };
  });
  console.log(JSON.stringify(report, null, 1));
  await page.screenshot({ path: path.join(__dirname, 'poster-a0-preview.png') });
  await browser.close();
})();
