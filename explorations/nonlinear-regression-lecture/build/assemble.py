"""One-time scaffold: build the deck from the SVM deck's engine (styles, slide engine, presenter view,
chart helper, supervised-learning map) plus this folder's slides.html, code.js, extra.css and data.json.

    python3 build/assemble.py nonlinear_regression_lecture.html

It cuts the SVM deck at marker lines, so it reproduces the deck only against the SVM deck as of the
commit that added this folder. After that the HTML file is the source; edit it directly.
"""
import re, json, sys
from pathlib import Path
here=Path(__file__).parent   # this build/ folder
svm=(here/'../../svm-lecture/svm_lecture.html').read_text().split('\n')
L=lambda a,b:'\n'.join(svm[a-1:b])          # 1-based inclusive line range
def find(pat,start=1):
    for i in range(start-1,len(svm)):
        if pat in svm[i]:return i+1
    raise KeyError(pat)
head=L(1,find('</style>')-1)
head=head.replace('<meta name="description" content="Lecture slides: hyperplanes, margins, hard- and soft-margin support vector classifiers, kernels.">',
                  '<meta name="description" content="Lecture slides: nonlinear regression with regression trees, kNN regression and support vector regression.">')
head=head.replace('<title>Support Vector Machines</title>','<title>Nonlinear Regression</title>')
assert 'Nonlinear Regression' in head and 'nonlinear regression with' in head
body_open=L(find('</style>'),find('<main id="deck">'))
footer=L(find('</main>'),find('<script>')-1)
engine=L(find('<script>'),find('window.__HINTS = {')-1)
engine=engine.replace("new BroadcastChannel('deck-svm')","new BroadcastChannel('deck-nlr')")
engine=engine.replace("const W=o.W||640,H=o.H||420,m={l:o.ml||58,r:18,t:16,b:46};","const W=o.W||640,H=o.H||420,m={l:o.ml||58,r:o.mr||18,t:16,b:46};")
engine=engine.replace("const api={svg,sx,sy,layer,clear,W,H,","const api={svg,sx,sy,layer,clear,W,H,xmin,xmax,ymin,ymax,")
engine=engine.replace("!e.closest('.tree-svg')","!e.closest('.tree-svg,.noanim')")
for k in ["deck-nlr","r:o.mr||18","xmin,xmax,ymin,ymax,","'.tree-svg,.noanim'"]:assert k in engine,k
hints="window.__HINTS = {};"
rest=L(find('/* ---------- hover helper cards ---------- */'),find('/* ================= SVM lecture ================= */')-1)
tree=L(find('/* ---------- supervised-learning map'),find('/* ---------- fit every slide to the screen')-1)
tree_rep=[
 ("  svm :{cx:605 ,cy:395,w:150,h:104,t:'SVMs'             ,sub:'today'    ,k:'today',s:3,v:'svm'},",
  "  svm :{cx:605 ,cy:395,w:150,h:104,t:'SVMs'             ,sub:'covered'  ,k:'done' ,s:2,v:'svm'},"),
 ("const ONPATH=new Set(['sup','cls','svm']),ONEDGE=new Set(['sup>cls','cls>svm']);",
  "const ONPATH=new Set(['sup','reg']),ONEDGE=new Set(['sup>reg']);"),
 ("3 SVMs (today) and neural networks (next week), 4 the path to today's topic.","3 neural networks (next week), 4 the path to today's topic, regression."),
]
for a,b in tree_rep:
    assert tree.count(a)==1,a; tree=tree.replace(a,b)
tree=re.sub(r"'aria-label':'[^']*'","'aria-label':'Supervised learning splits into classification and regression. Decision trees, nearest neighbor, naive Bayes and support vector machines (covered) sit under classification; linear and polynomial regression (covered) under regression; neural networks (next week) under both.'",tree,count=1)
fitboot=L(find('/* ---------- fit every slide to the screen'),len(svm))
data=json.loads((here/'data.json').read_text())
datablock='<script type="application/json" id="nlr-data">'+json.dumps(data,separators=(',',':'))+'</script>'
out='\n'.join([head,(here/'extra.css').read_text(),body_open,'',(here/'slides.html').read_text(),footer,datablock,engine,hints,'',rest,(here/'code.js').read_text(),tree,fitboot])
dest=Path(sys.argv[1]);dest.write_text(out);print('wrote',dest,len(out))
