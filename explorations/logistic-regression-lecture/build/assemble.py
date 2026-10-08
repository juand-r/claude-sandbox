"""One-time scaffold: build the deck from the SVM deck's engine (styles, slide engine, presenter view,
chart helper) plus this folder's slides.html, code.js and extra.css.

    python3 build/assemble.py logistic_regression_lecture.html

It cuts the SVM deck at marker lines, so it reproduces the deck only against the SVM deck as of the
commit that added this folder. After that the HTML file is the source; edit it directly.
"""
import sys
from pathlib import Path

here = Path(__file__).parent   # this build/ folder
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


head = L(1, find('</style>') - 1)
head = sub(head, '<meta name="description" content="Lecture slides: hyperplanes, margins, hard- and soft-margin support vector classifiers, kernels.">',
           '<meta name="description" content="Lecture slides: logistic regression as the SVM\'s linear score with log loss instead of hinge loss; the sigmoid; one neuron.">')
head = sub(head, '<title>Support Vector Machines</title>', '<title>Logistic Regression</title>')
# phones: narrower sliders so a toolbar never overflows (rule kept after the deck's last phone rule)
head += '\n@media (max-width:620px){input[type=range]{width:6.5em}}'
body_open = L(find('</style>'), find('<main id="deck">'))
footer = L(find('</main>'), find('<script>') - 1)
engine = L(find('<script>'), find('window.__HINTS = {') - 1)
engine = sub(engine, "new BroadcastChannel('deck-svm')", "new BroadcastChannel('deck-logreg')")
engine = sub(engine, "const W=o.W||640,H=o.H||420,m={l:o.ml||58,r:18,t:16,b:46};", "const W=o.W||640,H=o.H||420,m={l:o.ml||58,r:o.mr||18,t:16,b:46};")
engine = sub(engine, "const api={svg,sx,sy,layer,clear,W,H,", "const api={svg,sx,sy,layer,clear,W,H,xmin,xmax,ymin,ymax,")
engine = sub(engine, "!e.closest('.tree-svg')", "!e.closest('.tree-svg,.noanim')")
rest = L(find('/* ---------- hover helper cards ---------- */'), find('/* ================= SVM lecture ================= */') - 1)
fitboot = L(find('/* ---------- fit every slide to the screen'), len(svm))
out = '\n'.join([head, (here / 'extra.css').read_text(), body_open, '', (here / 'slides.html').read_text(), footer,
                 engine, 'window.__HINTS = {};', '', rest, (here / 'code.js').read_text(), fitboot])
Path(sys.argv[1]).write_text(out)
print('wrote', sys.argv[1], len(out))
