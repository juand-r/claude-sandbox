// Render a standalone figure page (an element #figure with a fixed px size) to a vector PDF
// cut to that size and a transparent PNG at 2x (192 px per printed inch).
//
// Run:  node render_figure.js figures/agent-model.html  -> figures/agent-model.pdf, .png
const path = require('path');
const PW = process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright';
const { chromium } = require(PW);

(async () => {
  const src = path.resolve(process.argv[2]);
  const base = src.replace(/\.html$/, '');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 2 });
  await page.goto('file://' + src);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const fig = await page.$('#figure');
  const box = await fig.boundingBox();
  // Fail loudly if any element spills outside the figure box.
  const spill = await page.evaluate(() => {
    const f = document.getElementById('figure').getBoundingClientRect();
    return [...document.querySelectorAll('#figure *')].filter((e) => {
      const r = e.getBoundingClientRect();
      return r.width && (r.left < f.left - 0.5 || r.right > f.right + 0.5 || r.top < f.top - 0.5 || r.bottom > f.bottom + 0.5);
    }).map((e) => e.textContent.trim().slice(0, 30) || e.tagName);
  });
  if (spill.length) throw new Error('elements outside the figure: ' + spill.join(' | '));
  await fig.screenshot({ path: base + '.png', omitBackground: true });
  await page.pdf({ path: base + '.pdf', width: `${box.width}px`, height: `${box.height}px`, printBackground: true, pageRanges: '1' });
  await browser.close();
  console.log(`wrote ${base}.pdf and ${base}.png (${box.width} x ${box.height} px)`);
})().catch((e) => { console.error(e); process.exit(1); });
