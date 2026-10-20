// Build an editable PowerPoint/Keynote version of the A0 poster (adapted from flora-poster/build_pptx.js).
//
// Every [data-kit] text block becomes a text box (Archivo) at its rendered position and size;
// [data-kit-shape] elements become filled (rounded) rectangles; figure <img> elements are embedded
// from their PNG files; numbered orange circles (.num) become circles with the number inside.
//
// How: open poster-a0.html in Chromium with weights restricted to Regular/Bold (what Keynote offers
// for Archivo), read boxes, paragraphs and runs from that render, and write them with pptxgenjs.
//
// Run (from this folder):  npm install && node build_pptx.js   ->  poster-a0.pptx
// Needs Playwright with Chromium (global install at PW below).

const fs = require('fs');
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
const WIDTH_SLACK_PX = 16;                          // room for small text-metric differences

// Runs in the browser: collect shapes, images, badges and text paragraphs.
function extractInPage() {
  const hex = (c) => {
    const m = c.match(/[\d.]+/g);
    if (!m) throw new Error(`cannot parse colour ${c}`);
    return m.slice(0, 3).map((v) => (+v).toString(16).padStart(2, '0')).join('').toUpperCase();
  };
  const box = (el) => { const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; };
  const isInline = (el) => getComputedStyle(el).display.startsWith('inline');
  const isRowFlex = (el) => { const cs = getComputedStyle(el); return cs.display.includes('flex') && cs.flexDirection.startsWith('row'); };

  function paragraphsOf(el) {
    if (isRowFlex(el)) return [el];
    const blocks = [...el.children].filter((c) => !isInline(c));
    if (blocks.length === 0) return [el];
    return blocks.flatMap(paragraphsOf);
  }

  function runStyle(node) {
    const cs = getComputedStyle(node.parentElement);
    return {
      sizePx: parseFloat(cs.fontSize),
      bold: +cs.fontWeight >= 600,
      italic: cs.fontStyle === 'italic',
      color: hex(cs.color),
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
    const walker = document.createTreeWalker(para, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) {
      if (n.parentElement.closest('.num')) continue;          // drawn as a badge instead
      const t = n.textContent.replace(/[ \t\n\r]+/g, ' ');
      if (t) add(t, runStyle(n));
    }
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
    // For a heading with a badge, the text starts where the words start.
    const words = para.querySelector('.num') ? para.querySelector('.num').nextElementSibling : null;
    const b = words ? box(words) : box(para);
    return { ...b, lineHeightPx: lh, align: cs.textAlign === 'center' ? 'center' : cs.textAlign === 'right' ? 'right' : 'left', runs: runsOf(para) };
  }

  const shapes = [...document.querySelectorAll('[data-kit-shape]')].map((el) => {
    const cs = getComputedStyle(el);
    return {
      name: el.dataset.kitShape, ...box(el), fill: hex(cs.backgroundColor),
      radiusPx: parseFloat(cs.borderTopLeftRadius) || 0,
      borderPx: parseFloat(cs.borderTopWidth) || 0, borderColor: hex(cs.borderTopColor),
    };
  });

  const items = [];
  for (const el of document.querySelectorAll('[data-kit]')) {
    const name = el.dataset.kit;
    if (el.tagName === 'IMG') {
      items.push({ kind: 'image', name, src: el.getAttribute('src'), ...box(el) });
      continue;
    }
    for (const img of el.querySelectorAll('img')) {
      items.push({ kind: 'image', name: name + '-image', src: img.getAttribute('src'), ...box(img) });
    }
    for (const num of el.querySelectorAll('.num')) {
      const cs = getComputedStyle(num);
      items.push({ kind: 'badge', name: name + '-number', ...box(num), text: num.textContent.trim(),
                   fill: hex(cs.backgroundColor), color: hex(cs.color), sizePx: parseFloat(cs.fontSize) });
    }
    const paras = paragraphsOf(el).filter((p) => p.tagName !== 'IMG').map(paragraph).filter((p) => p.runs.length);
    if (!paras.length) throw new Error(`no text found in ${name}`);
    const x = Math.min(...paras.map((p) => p.x));
    const right = Math.max(...paras.map((p) => p.x + p.w));
    items.push({ kind: 'text', name, x, w: right - x, paras });
  }
  return { background: hex(getComputedStyle(document.getElementById('poster')).backgroundColor), shapes, items };
}

async function render() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: PAGE_W_PX, height: PAGE_H_PX } });
  await page.goto('file://' + POSTER);
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => {
    for (const el of document.querySelectorAll('body *')) {
      el.style.fontWeight = +getComputedStyle(el).fontWeight >= 600 ? '700' : '400';
    }
  });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  const size = await page.evaluate(() => { const p = document.getElementById('poster'); return [p.scrollWidth, p.scrollHeight]; });
  if (size[0] > PAGE_W_PX || size[1] > PAGE_H_PX) throw new Error(`poster overflows: ${size}`);
  const layout = await page.evaluate(extractInPage);
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
        fontFace: 'Archivo', fontSize: pt(s.sizePx), bold: s.bold, italic: s.italic, color: s.color,
        lineSpacing: pt(p.lineHeightPx), paraSpaceBefore: pt(spaceBefore), align: p.align,
      };
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
  pres.title = 'Tokens of Meaning (poster)';
  const slide = pres.addSlide();
  slide.background = { color: layout.background };

  for (const s of layout.shapes) {
    const rounded = s.radiusPx > 0;
    slide.addShape(rounded ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, {
      x: inch(s.x), y: inch(s.y), w: inch(s.w), h: inch(s.h), fill: { color: s.fill },
      line: s.borderPx ? { color: s.borderColor, width: pt(s.borderPx) } : { type: 'none' },
      ...(rounded ? { rectRadius: inch(s.radiusPx) } : {}), objectName: s.name,
    });
  }
  for (const it of layout.items) {
    if (it.kind === 'image') {
      const file = path.join(__dirname, it.src);
      if (!fs.existsSync(file)) throw new Error(`missing image ${file}`);
      slide.addImage({ path: file, x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h), objectName: it.name });
    } else if (it.kind === 'badge') {
      slide.addText(it.text, {
        shape: pres.shapes.OVAL, x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
        fill: { color: it.fill }, line: { type: 'none' }, color: it.color, fontFace: 'Archivo',
        fontSize: pt(it.sizePx), bold: true, align: 'center', valign: 'middle', margin: 0, objectName: it.name,
      });
    } else {
      const top = it.paras[0].y;
      const last = it.paras[it.paras.length - 1];
      slide.addText(textRuns(it.paras), {
        x: inch(it.x), y: inch(top), w: inch(it.w + WIDTH_SLACK_PX), h: inch(last.y + last.h - top),
        margin: 0, valign: 'top', isTextBox: true, fit: 'none', wrap: true, objectName: it.name,
      });
    }
  }
  await pres.writeFile({ fileName: OUT });
  const n = (k) => layout.items.filter((i) => i.kind === k).length;
  console.log(`wrote ${OUT}: ${layout.shapes.length} shapes, ${n('text')} text boxes, ${n('badge')} badges, ${n('image')} images`);
}

main().catch((e) => { console.error(e); process.exit(1); });
