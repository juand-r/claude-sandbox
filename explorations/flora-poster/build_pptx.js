// Build an editable PowerPoint/Keynote version of the A0 poster.
//
// Every text block becomes a real text box (Archivo / STIX Two Text) at its position and size;
// the ablation table becomes a native table; charts, diagrams, Figure 5 and the QR codes are images.
//
// How: open poster-a0.html in Chromium with fonts restricted to what Keynote can select
// reliably (normal width; Regular or Bold), read every element's box, text runs and styles
// from that render, and write them out with pptxgenjs. Positions therefore match a layout
// that Archivo Regular/Bold actually produces.
//
// Run (from this folder):  npm install && node build_pptx.js   ->  poster-a0.pptx
// Needs Playwright with Chromium (global install at PW below).

const path = require('path');
const pptxgen = require('pptxgenjs');
const PW = process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright';
const { chromium } = require(PW);

const POSTER = path.join(__dirname, 'poster-a0.html');
const OUT = path.join(__dirname, 'poster-a0.pptx');
const PAGE_W_PX = 3179, PAGE_H_PX = 4494;          // artboard size (A0 at 96 px/in)
const SLIDE_W_IN = 841 / 25.4, SLIDE_H_IN = 1189 / 25.4;
const IN_PER_PX = SLIDE_W_IN / PAGE_W_PX;
const PT_PER_PX = IN_PER_PX * 72;
const IMAGE_SCALE = 2;                              // images at 192 px per printed inch
const WIDTH_SLACK_PX = 16;                          // room for small text-metric differences

// Elements exported as pictures rather than text. Everything else with data-kit is text,
// except the table below.
const IMAGE_ELEMENTS = new Set([
  's1-noble-gas-diagram', 's2-equation', 's3-flora-diagram', 'figure-scatter',
  'results-legend', 'results-chart', 'validator-chart',
]);
const TABLE_ELEMENTS = new Set(['ablation-table']);
const QR_ELEMENTS = new Set(['qr-paper', 'qr-code']);   // QR image + text labels

// Runs in the browser: collect paragraphs of styled runs from an element.
function extractInPage(spec) {
  const { imageSet, tableSet, qrSet } = spec;
  const hex = (c) => {
    const m = c.match(/[\d.]+/g);
    if (!m) throw new Error(`cannot parse colour ${c}`);
    return m.slice(0, 3).map((v) => (+v).toString(16).padStart(2, '0')).join('').toUpperCase();
  };
  const box = (el) => { const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; };
  const isInline = (el) => getComputedStyle(el).display.startsWith('inline');
  const isRowFlex = (el) => { const cs = getComputedStyle(el); return cs.display.includes('flex') && cs.flexDirection.startsWith('row'); };

  // Split an element into paragraph elements.
  function paragraphsOf(el) {
    if (isRowFlex(el)) return [el];
    const blocks = [...el.children].filter((c) => !isInline(c));
    if (blocks.length === 0) return [el];
    return blocks.flatMap(paragraphsOf);
  }

  function runStyle(node, para) {
    const el = node.parentElement;
    const cs = getComputedStyle(el);
    const sub = el.closest('sub'), sup = el.closest('sup');
    // PowerPoint shrinks superscript/subscript runs itself, so give them the surrounding size.
    const shift = (sub && para.contains(sub)) ? sub : (sup && para.contains(sup)) ? sup : null;
    return {
      sizePx: parseFloat(getComputedStyle(shift ? shift.parentElement : el).fontSize),
      bold: +cs.fontWeight >= 600,
      italic: cs.fontStyle === 'italic',
      color: hex(cs.color),
      face: cs.fontFamily.includes('STIX') ? 'STIX Two Text' : 'Archivo',
      sub: !!(sub && para.contains(sub)),
      sup: !!(sup && para.contains(sup)),
      upper: cs.textTransform === 'uppercase',
      letterPx: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing),
    };
  }

  function runsOf(para) {
    const runs = [];
    const add = (text, style) => {
      const prev = runs[runs.length - 1];
      if (prev && JSON.stringify(prev.style) === JSON.stringify(style)) prev.text += text;
      else runs.push({ text, style });
    };
    // Flex rows (a heading's number + words) lose their gap; join the items with a space.
    const parts = isRowFlex(para) ? [...para.children] : [para];
    parts.forEach((part, i) => {
      const walker = document.createTreeWalker(part, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        const t = n.textContent.replace(/[ \t\n\r]+/g, ' ');
        if (!t) continue;
        const style = runStyle(n, para);
        add(style.upper ? t.toUpperCase() : t, style);
      }
      if (i < parts.length - 1 && runs.length) runs[runs.length - 1].text += ' ';
    });
    if (runs.length) {
      runs[0].text = runs[0].text.replace(/^ +/, '');
      runs[runs.length - 1].text = runs[runs.length - 1].text.replace(/ +$/, '');
    }
    return runs.filter((r) => r.text.length);
  }

  function paragraph(para) {
    const cs = getComputedStyle(para);
    const size = parseFloat(cs.fontSize);
    const lh = cs.lineHeight === 'normal' ? 1.2 * size : parseFloat(cs.lineHeight);
    return { ...box(para), lineHeightPx: lh, align: cs.textAlign === 'center' ? 'center' : cs.textAlign === 'right' ? 'right' : 'left', runs: runsOf(para) };
  }

  const items = [];
  for (const el of document.querySelectorAll('[data-kit]')) {
    const name = el.dataset.kit;
    if (imageSet.includes(name)) {
      items.push({ kind: 'image', name, ...box(el) });
    } else if (tableSet.includes(name)) {
      const rows = [...el.querySelectorAll('tr')].map((tr) => {
        const trs = getComputedStyle(tr);
        return {
          h: tr.getBoundingClientRect().height,
          borderBottomPx: parseFloat(trs.borderBottomWidth) || 0,
          borderBottomColor: hex(trs.borderBottomColor),
          cells: [...tr.children].map((td) => ({ w: td.getBoundingClientRect().width, ...paragraph(td) })),
        };
      });
      items.push({ kind: 'table', name, ...box(el), rows });
    } else if (qrSet.includes(name)) {
      const img = el.querySelector('img');
      items.push({ kind: 'image', name: name + '-image', ...box(img) });
      const paras = paragraphsOf(el).filter((p) => p.tagName !== 'IMG').map(paragraph).filter((p) => p.runs.length);
      items.push({ kind: 'text', name: name + '-label', x: box(el).x, w: box(el).w, paras });
    } else {
      const paras = paragraphsOf(el).map(paragraph).filter((p) => p.runs.length);
      if (!paras.length) throw new Error(`no text found in ${name}`);
      items.push({ kind: 'text', name, x: box(el).x, w: box(el).w, paras });
    }
  }
  const band = document.querySelector('[data-kit-shape]');
  const root = document.querySelector('body > div > div');
  return {
    background: hex(getComputedStyle(root).backgroundColor),
    band: { ...box(band), color: hex(getComputedStyle(band).backgroundColor) },
    items,
  };
}

async function render() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: PAGE_W_PX, height: PAGE_H_PX }, deviceScaleFactor: IMAGE_SCALE });
  await page.goto('file://' + POSTER);
  await page.evaluate(() => document.fonts.ready);
  // Keynote-safe type: normal width, weights collapse to Regular (400) or Bold (700).
  await page.evaluate(() => {
    for (const el of document.querySelectorAll('body *')) {
      const w = +getComputedStyle(el).fontWeight;
      el.style.fontStretch = '100%';
      el.style.fontWeight = w >= 600 ? '700' : '400';
    }
  });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  const overflow = await page.evaluate(() => document.querySelector('body > div > div').scrollHeight);
  if (overflow > 4494) throw new Error(`poster overflows with Keynote-safe fonts: ${overflow}px`);

  const layout = await page.evaluate(extractInPage, {
    imageSet: [...IMAGE_ELEMENTS], tableSet: [...TABLE_ELEMENTS], qrSet: [...QR_ELEMENTS],
  });

  // Pictures: transparent backgrounds, then one screenshot per image item.
  await page.addStyleTag({ content: 'html, body, body > div > div, [data-kit-shape] { background: transparent !important; }' });
  for (const it of layout.items.filter((i) => i.kind === 'image')) {
    const buf = await page.screenshot({ clip: { x: it.x, y: it.y, width: it.w, height: it.h }, omitBackground: true });
    it.data = 'image/png;base64,' + buf.toString('base64');
  }
  await browser.close();
  return layout;
}

const inch = (px) => +(px * IN_PER_PX).toFixed(4);
const pt = (px) => +(px * PT_PER_PX).toFixed(2);

function textRuns(paras) {
  const out = [];
  paras.forEach((p, pi) => {
    const prev = paras[pi - 1];
    const spaceBefore = prev ? Math.max(0, p.y - (prev.y + prev.h)) : 0;
    p.runs.forEach((r, ri) => {
      const s = r.style;
      const opts = {
        fontFace: s.face, fontSize: pt(s.sizePx), bold: s.bold, italic: s.italic, color: s.color,
        lineSpacing: pt(p.lineHeightPx), paraSpaceBefore: pt(spaceBefore), align: p.align,
      };
      if (s.sub) opts.subscript = true;
      if (s.sup) opts.superscript = true;
      if (s.letterPx) opts.charSpacing = pt(s.letterPx);
      if (ri === p.runs.length - 1 && pi < paras.length - 1) opts.breakLine = true;
      out.push({ text: r.text, options: opts });
    });
  });
  return out;
}

async function main() {
  const layout = await render();
  const pres = new pptxgen();
  pres.defineLayout({ name: 'A0_PORTRAIT', width: SLIDE_W_IN, height: SLIDE_H_IN });
  pres.layout = 'A0_PORTRAIT';
  pres.title = 'Improving LLMs via Validator-to-Generator Alignment (poster)';
  const slide = pres.addSlide();
  slide.background = { color: layout.background };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: inch(layout.band.x), y: inch(layout.band.y), w: inch(layout.band.w), h: inch(layout.band.h),
    fill: { color: layout.band.color }, line: { type: 'none' }, objectName: 'center-band',
  });

  for (const it of layout.items) {
    if (it.kind === 'image') {
      slide.addImage({ data: it.data, x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h), objectName: it.name });
    } else if (it.kind === 'text') {
      const top = it.paras[0].y;
      const last = it.paras[it.paras.length - 1];
      slide.addText(textRuns(it.paras), {
        x: inch(it.x), y: inch(top), w: inch(it.w + WIDTH_SLACK_PX), h: inch(last.y + last.h - top),
        margin: 0, valign: 'top', isTextBox: true, fit: 'none', wrap: true, objectName: it.name,
      });
    } else if (it.kind === 'table') {
      const rows = it.rows.map((row) => row.cells.map((c) => ({
        text: textRuns([c]),
        options: {
          valign: 'middle', margin: [0, 0, 0, 0],
          border: [{ type: 'none' }, { type: 'none' },
            row.borderBottomPx ? { type: 'solid', pt: pt(row.borderBottomPx), color: row.borderBottomColor } : { type: 'none' },
            { type: 'none' }],
        },
      })));
      slide.addTable(rows, {
        x: inch(it.x), y: inch(it.y), w: inch(it.w),
        colW: it.rows[0].cells.map((c) => inch(c.w)), rowH: it.rows.map((r) => inch(r.h)),
        objectName: it.name,
      });
    }
  }
  await pres.writeFile({ fileName: OUT });
  const n = (k) => layout.items.filter((i) => i.kind === k).length;
  console.log(`wrote ${OUT}: ${n('text')} text boxes, ${n('table')} table, ${n('image')} images`);
}

main().catch((e) => { console.error(e); process.exit(1); });
