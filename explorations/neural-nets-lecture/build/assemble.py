"""One-time scaffold: build a neural networks deck from the SVM deck's engine (styles, slide engine,
presenter view, chart helper) plus this folder's slides_<k>.html, common.js, code_<k>.js, extra.css,
the precomputed runs in data.json, and the images in ../assets (embedded as base64).

    python3 build/assemble.py 1 neural_nets_1.html
    python3 build/assemble.py 2 neural_nets_2.html
    python3 build/assemble.py 2 neural_nets_2_annotate.html build/annotate_2.json

With a third argument (a JSON file of slide id -> step), it builds an annotation copy: every slide shows
one fixed step and has no presses; slides not in the file show their last step.

Formulas written as \( … \) (inline) or \[ … \] (display) are typeset with KaTeX at build time; run
`npm install` in build/ once first.

It cuts the SVM deck at marker lines, so it reproduces the deck only against the SVM deck as of the
commit that added this folder.
"""
import base64
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

here = Path(__file__).parent   # this build/ folder
k, target = sys.argv[1], sys.argv[2]
fixed = json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv) > 3 else None   # annotation copy
DECKS = {
    '1': ('Neural Networks, Part 1', 'Lecture slides: softmax and cross-entropy, gradient descent, the perceptron and XOR, hidden layers and forward propagation.'),
    '2': ('Neural Networks, Part 2', 'Lecture slides: backpropagation, learning rates, momentum, stochastic and mini-batch gradient descent, early stopping.'),
}
title, desc = DECKS[k]
svm = (here / '../../svm-lecture/svm_lecture.html').read_text().split('\n')
L = lambda a, b: '\n'.join(svm[a - 1:b])   # 1-based inclusive line range


def find(pat, start=1):
    for i in range(start - 1, len(svm)):
        if pat in svm[i]:
            return i + 1
    raise KeyError(pat)


def sub(s, a, b):
    assert s.count(a) == 1, a
    return s.replace(a, b)


MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg'}


def embed(m):
    f = here / '../assets' / m.group(1)
    return f'data:{MIME[f.suffix]};base64,' + base64.b64encode(f.read_bytes()).decode()


head = L(1, find('</style>') - 1)
head = sub(head, '<meta name="description" content="Lecture slides: hyperplanes, margins, hard- and soft-margin support vector classifiers, kernels.">',
           f'<meta name="description" content="{desc}">')
head = sub(head, '<title>Support Vector Machines</title>', f'<title>{title}</title>')
# phones: narrower sliders so a toolbar never overflows (rule kept after the deck's last phone rule)
head += '\n@media (max-width:620px){input[type=range]{width:6.5em}}'
body_open = L(find('</style>'), find('<main id="deck">'))
footer = L(find('</main>'), find('<script>') - 1)
engine = L(find('<script>'), find('window.__HINTS = {') - 1)
engine = sub(engine, "new BroadcastChannel('deck-svm')", f"new BroadcastChannel('deck-nn{k}')")
engine = sub(engine, "const W=o.W||640,H=o.H||420,m={l:o.ml||58,r:18,t:16,b:46};", "const W=o.W||640,H=o.H||420,m={l:o.ml||58,r:o.mr||18,t:16,b:46};")
engine = sub(engine, "const api={svg,sx,sy,layer,clear,W,H,", "const api={svg,sx,sy,layer,clear,W,H,xmin,xmax,ymin,ymax,")
engine = sub(engine, "!e.closest('.tree-svg')", "!e.closest('.tree-svg,.noanim')")
if k == '2':   # class 2: the next slide appears at once, without the smooth scroll (asked by the user)
    engine = sub(engine, "slides[i].scrollIntoView({behavior:'smooth',block:'start'})", "slides[i].scrollIntoView({behavior:'instant',block:'start'})")
    head += '\nhtml,#deck{scroll-behavior:auto!important}'
    head += '\n@media (max-width:620px){#s-recap .eq .katex{font-size:.64em!important}}'   # a⁽¹⁾ is wider than h
if fixed is not None:   # annotation copy: each slide is drawn at its data-fixed step, and no press moves within a slide
    engine = sub(engine, "slides.forEach((sl,i)=>applySteps(i,i===cur?step:(i<cur?maxStep(i):0)));", "slides.forEach((sl,i)=>applySteps(i,+sl.dataset.fixed));")
    engine = sub(engine, "const h=hooks[slides[cur].id];if(h&&h.step)h.step(step);", "const h=hooks[slides[cur].id];if(h&&h.step)h.step(+slides[cur].dataset.fixed);")
    engine = sub(engine, f"new BroadcastChannel('deck-nn{k}')", f"new BroadcastChannel('deck-nn{k}-annotate')")
    head = sub(head, f'<title>{title}</title>', f'<title>{title} (annotation copy)</title>')
rest = L(find('/* ---------- hover helper cards ---------- */'), find('/* ================= SVM lecture ================= */') - 1)
fitboot = L(find('/* ---------- fit every slide to the screen'), len(svm))
slides = re.sub(r'\{\{IMG:([^}]+)\}\}', embed, (here / f'slides_{k}.html').read_text())
if fixed is not None:
    ids = set(re.findall(r'<section class="slide[^"]*" id="([^"]+)"', slides))
    unknown = [i for i in fixed if not i.startswith('_') and i not in ids]
    assert not unknown, f'annotation file names slides that do not exist: {unknown}'
    def fix(m):
        sid, n = m.group(2), int(m.group(3))
        f = fixed.get(sid, n)
        assert 0 <= f <= n, f'{sid}: step {f} is not between 0 and {n}'
        return f'{m.group(1)}data-steps="0" data-fixed="{f}">'
    slides = re.sub(r'(<section class="slide[^"]*" id="([^"]+)" )data-steps="(\d+)">', fix, slides)
# formulas written as \( … \) or \[ … \] are typeset by KaTeX now (build/tex.js), with its fonts embedded
katex_css = ''
if '\\(' in slides or '\\[' in slides:
    tex = lambda *a: subprocess.run(['node', str(here / 'tex.js'), *a], check=True, capture_output=True, text=True).stdout
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(slides)
    slides, katex_css = tex(f.name), tex('--css')
    Path(f.name).unlink()
data = '<script type="application/json" id="nn-data">' + (here / 'data.json').read_text() + '</script>'
code = (here / 'common.js').read_text() + '\n' + (here / f'code_{k}.js').read_text()
out = '\n'.join([head, katex_css, (here / 'extra.css').read_text(), body_open, '', slides, footer, data,
                 engine, 'window.__HINTS = {};', '', rest, code, fitboot])
Path(target).write_text(out)
print('wrote', target, len(out))
