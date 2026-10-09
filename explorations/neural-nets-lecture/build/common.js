/* ================= Neural networks lectures: shared helpers ================= */
const $=id=>document.getElementById(id);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function txt(parent,x,y,s,a={}){const t=el('text',{x,y,...a},parent);t.textContent=s;return t;}
/* ---------- math labels in SVG, in the KaTeX fonts (embedded by build/tex.js) ---------- */
// Write labels as plain text: single letters become italic variables, words and digits stay upright,
// ℒ is the script L, and subscripts are written with Unicode (x₁, wⱼᵢ) or as _N (x_N).
// Each run of characters gets its own <tspan>; subscripts are smaller and lowered.
const MATH_SCALE=1.15;   // KaTeX's glyphs are smaller than the mono font's at the same size
const SUB={'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','ᵢ':'i','ⱼ':'j','ₖ':'k','ₚ':'p'},SUP={'ᵀ':'T'};
const KATEX_CHAR={'·':'⋅','‖':'∥'};   // the characters KaTeX's fonts have for these
const isLatin=c=>/[A-Za-z]/.test(c||''),GREEK_IT='αβγδεζηθικλμνξπρστυφχψω';
function mathRuns(s){
  const runs=[],push=(t,fam,it,shift)=>{const r=runs[runs.length-1];
    if(r&&r.fam===fam&&r.it===it&&r.shift===shift)r.t+=t;else runs.push({t,fam,it,shift});};
  for(let i=0;i<s.length;i++){let c=s[i],shift=0;
    if(c==='_'&&i+1<s.length){c=s[++i];shift=1;}
    else if(SUB[c]){c=SUB[c];shift=1;}
    else if(SUP[c]){c=SUP[c];shift=-1;}
    const word=shift===0&&isLatin(c)&&(isLatin(s[i-1])||isLatin(s[i+1]));
    if(c==='ℒ')push('L','KaTeX_Caligraphic',false,shift);
    else if(isLatin(c)&&!word)push(c,'KaTeX_Math',true,shift);
    else if(GREEK_IT.includes(c))push(c,'KaTeX_Math',true,shift);
    else if(c==='-'&&/[\d.]/.test(s[i+1]||''))push('−','KaTeX_Main',false,shift);   // a minus sign, not a hyphen
    else push(KATEX_CHAR[c]||c,'KaTeX_Main',false,shift);}
  return runs;}
function mtxt(parent,x,y,s,a={}){
  const fs=(+a['font-size']||16)*MATH_SCALE,t=el('text',{x,y,...a,'font-size':fs.toFixed(1)},parent);
  let cur=0;   // the current baseline offset in px
  for(const r of mathRuns(String(s))){const off=r.shift===1?.28*fs:r.shift===-1?-.4*fs:0;
    const sp=el('tspan',{'font-family':r.fam,'font-style':r.it?'italic':'normal',dy:(off-cur).toFixed(1)},t);
    if(r.shift)sp.setAttribute('font-size',(.72*fs).toFixed(1));
    sp.textContent=r.t;cur=off;}
  t.setAttribute('aria-label',s);return t;}
const stepG=(parent,k)=>el('g',{'data-step':k},parent);
const sig=z=>1/(1+Math.exp(-z));
// the engine's chart() draws tick numbers and axis names in its own fonts; redraw them as math labels
const engineChart=chart;
chart=function(host,o){const api=engineChart(host,o);
  for(const t of [...api.svg.querySelectorAll('text')]){const a={};
    for(const at of t.attributes)if(at.name!=='font-family')a[at.name]=at.value;
    t.replaceWith(mtxt(t.parentNode,a.x,a.y,t.textContent,a));}
  return api;};
const label=(L,x,y,s,a={})=>mtxt(L,x,y,s,{'font-size':16,'font-weight':700,'paint-order':'stroke',stroke:'var(--surface)','stroke-width':5,...a});
const D=JSON.parse($('nn-data').textContent);   // made by experiments.py
const fmt=(v,d=2)=>v.toFixed(d).replace('-','−');

/* ---------- a small MLP: sigmoid hidden layer, softmax output (same as experiments.py) ---------- */
function mlpForward(P,u){
  const [W1,b1,W2,b2]=P,h=W1.map((r,i)=>sig(r[0]*u[0]+r[1]*u[1]+b1[i]));
  const z=W2.map((r,k)=>r.reduce((s,w,j)=>s+w*h[j],b2[k])),mx=Math.max(...z),e=z.map(v=>Math.exp(v-mx)),S=e.reduce((a,b)=>a+b,0);
  return {h,p:e.map(v=>v/S)};}

/* ---------- contour lines of a grid F[i][j] at level c (marching squares) ---------- */
function contourPath(api,xs,ys,F,c){let d='';
  for(let i=0;i+1<xs.length;i++)for(let j=0;j+1<ys.length;j++){
    const v=[F[i][j]-c,F[i+1][j]-c,F[i+1][j+1]-c,F[i][j+1]-c],P=[[xs[i],ys[j]],[xs[i+1],ys[j]],[xs[i+1],ys[j+1]],[xs[i],ys[j+1]]],pts=[];
    for(let k=0;k<4;k++){const a=v[k],b=v[(k+1)%4];if((a>=0)!==(b>=0)){const t=a/(a-b),p=P[k],q=P[(k+1)%4];pts.push([p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])]);}}
    for(let k=0;k+1<pts.length;k+=2)d+=`M${api.sx(pts[k][0]).toFixed(1)} ${api.sy(pts[k][1]).toFixed(1)}L${api.sx(pts[k+1][0]).toFixed(1)} ${api.sy(pts[k+1][1]).toFixed(1)}`;}
  return d;}
// a loss landscape: shaded cells (darker = lower) plus contour lines at the given levels
function landscape(api,L,G,levels){
  const xs=G.w,ys=G.b,F=G.L,lo=Math.min(...F.flat()),hi=Math.max(...F.flat()),g=el('g',{},L);g.classList.add('noanim');
  for(let i=0;i+1<xs.length;i++)for(let j=0;j+1<ys.length;j++){const v=(F[i][j]+F[i+1][j]+F[i][j+1]+F[i+1][j+1])/4,t=Math.pow((v-lo)/(hi-lo),.5);
    el('rect',{x:api.sx(xs[i]),y:api.sy(ys[j+1]),width:api.sx(xs[i+1])-api.sx(xs[i]),height:api.sy(ys[j])-api.sy(ys[j+1]),'shape-rendering':'crispEdges',fill:'var(--model)',opacity:(.42*(1-t)).toFixed(3)},g);}
  for(const c of levels)el('path',{d:contourPath(api,xs,ys,F,c),fill:'none',stroke:'var(--model)','stroke-width':1,opacity:.55},g);
  return g;}
// a path of parameter values, with dots at each step
function drawPath(api,L,path,{color='var(--hi)',upTo=path.length-1,dots=true,width=2.5}={}){
  const P=path.slice(0,upTo+1);
  el('path',{d:P.map((p,k)=>(k?'L':'M')+api.sx(p[0]).toFixed(1)+' '+api.sy(p[1]).toFixed(1)).join(''),fill:'none',stroke:color,'stroke-width':width,'stroke-linejoin':'round'},L);
  if(dots)P.forEach(p=>el('circle',{cx:api.sx(p[0]),cy:api.sy(p[1]),r:3,fill:color},L));
  const e=P[P.length-1];el('circle',{cx:api.sx(e[0]),cy:api.sy(e[1]),r:7.5,fill:color,stroke:'var(--surface)','stroke-width':2},L);}
function star(api,L,p,{color='var(--ink)'}={}){const cx=api.sx(p[0]),cy=api.sy(p[1]),pts=[];
  for(let k=0;k<10;k++){const r=k%2?4.5:10,a=-Math.PI/2+k*Math.PI/5;pts.push([cx+r*Math.cos(a),cy+r*Math.sin(a)].map(v=>v.toFixed(1)).join(','));}
  el('polygon',{points:pts.join(' '),fill:color,stroke:'var(--surface)','stroke-width':1.5},L);}

/* ---------- the cartoon loss surface (both decks) ---------- */
// ℒ(a, b) = 1.6 − 1.0 exp(−|θ − m₁|²/1.2) − 0.65 exp(−|θ − m₂|²/0.8) + 0.04|θ|², m₁ = (1.2, 0.9), m₂ = (−1.4, −1.1)
const CART={m1:[1.2,.9],s1:1.2,a1:1.0,m2:[-1.4,-1.1],s2:.8,a2:.65,c:.04};
function cartoon([a,b]){const q1=((a-CART.m1[0])**2+(b-CART.m1[1])**2)/CART.s1,q2=((a-CART.m2[0])**2+(b-CART.m2[1])**2)/CART.s2;
  return 1.6-CART.a1*Math.exp(-q1)-CART.a2*Math.exp(-q2)+CART.c*(a*a+b*b);}
function cartoonGrad([a,b]){const e1=CART.a1*Math.exp(-(((a-CART.m1[0])**2+(b-CART.m1[1])**2)/CART.s1)),e2=CART.a2*Math.exp(-(((a-CART.m2[0])**2+(b-CART.m2[1])**2)/CART.s2));
  return [e1*2*(a-CART.m1[0])/CART.s1+e2*2*(a-CART.m2[0])/CART.s2+2*CART.c*a, e1*2*(b-CART.m1[1])/CART.s1+e2*2*(b-CART.m2[1])/CART.s2+2*CART.c*b];}
// gradient descent on the cartoon; beta > 0 adds momentum (v ← βv + ∇ℒ, θ ← θ − ηv)
function cartoonPath(t0,{eta=.25,steps=120,beta=0}={}){const P=[t0.slice()];let t=t0.slice(),v=[0,0];
  for(let k=0;k<steps;k++){const g=cartoonGrad(t);v=[beta*v[0]+g[0],beta*v[1]+g[1]];t=[t[0]-eta*v[0],t[1]-eta*v[1]];P.push(t);}return P;}
function cartoonGrid(n=60){const w=[],b=[],L=[];for(let i=0;i<=n;i++){w.push(-3+6*i/n);b.push(-3+6*i/n);}
  for(const a of w)L.push(b.map(v=>cartoon([a,v])));return {w,b,L};}
function cartoonPlot(host,{H=440,label='a made-up loss surface with two valleys'}={}){
  const api=chart(host,{W:H,H,ml:58,fs:1.3,xmin:-3,xmax:3,ymin:-3,ymax:3,xticks:[-3,0,3],yticks:[-3,0,3],xfmt:v=>String(v).replace('-','−'),yfmt:v=>String(v).replace('-','−'),xlabel:'θ₁',ylabel:'θ₂',label});
  api.svg.classList.add('sq');landscape(api,api.layer('heat'),cartoonGrid(),[.7,.8,.9,1,1.1,1.2,1.3,1.4,1.5]);return api;}

/* ---------- decision map of an MLP on the XOR box (inputs scaled u = (x − 5) / 2.5) ---------- */
function xorPlot(host,label,{H=430,fs=1.3}={}){
  const api=chart(host,{W:H*1.0,H,ml:58,fs,xmin:0,xmax:10,ymin:0,ymax:10,xticks:[0,5,10],yticks:[0,5,10],xlabel:'x₁',ylabel:'x₂',label});
  api.svg.classList.add('sq');return api;}
// shade the chart's box by p(green) = pfn(x): green where p ≥ 0.5, purple below, stronger when surer
function drawMap(api,L,pfn,{N=40}={}){L.textContent='';L.classList.add('noanim');
  const hx=(api.xmax-api.xmin)/N,hy=(api.ymax-api.ymin)/N,cw=api.sx(api.xmin+hx)-api.sx(api.xmin),ch=api.sy(api.ymin)-api.sy(api.ymin+hy);
  for(let i=0;i<N;i++)for(let j=0;j<N;j++){const x=api.xmin+i*hx,y=api.ymin+j*hy,p=pfn([x+hx/2,y+hy/2]);
    el('rect',{x:api.sx(x),y:api.sy(y+hy),width:cw,height:ch,'shape-rendering':'crispEdges',fill:p>=.5?'var(--pos)':'var(--mean)',opacity:(.04+.32*Math.abs(p-.5)*2).toFixed(3)},L);}}
function drawPts(api,L,X,y,{r=7}={}){X.forEach((p,i)=>el('circle',{cx:api.sx(p[0]),cy:api.sy(p[1]),r,fill:y[i]>0?'var(--pos)':'var(--mean)',stroke:'var(--surface)','stroke-width':2},L));}
const xorP=P=>x=>mlpForward(P,[(x[0]-5)/2.5,(x[1]-5)/2.5]).p[0];

/* ---------- network diagrams ---------- */
function node(L,x,y,r,s,a={},ta={}){el('circle',{cx:x,cy:y,r,fill:'var(--surface)',stroke:'var(--ink)','stroke-width':1.8,...a},L);
  if(s)mtxt(L,x,y+6,s,{'text-anchor':'middle','font-size':17,fill:'var(--ink)',...ta});}
function arrow(L,x1,y1,x2,y2,a={}){const t=Math.atan2(y2-y1,x2-x1),hd=9,c=a.stroke||'var(--muted)';
  el('line',{x1,y1,x2:x2-Math.cos(t)*hd*.6,y2:y2-Math.sin(t)*hd*.6,stroke:c,'stroke-width':1.8,...a},L);
  el('polygon',{points:[[x2,y2],[x2-hd*Math.cos(t-.4),y2-hd*Math.sin(t-.4)],[x2-hd*Math.cos(t+.4),y2-hd*Math.sin(t+.4)]].map(v=>v.join(',')).join(' '),fill:c},L);}
// one neuron: inputs → weights → Σ + b → σ → p (as on the last slide of the logistic regression deck)
function neuronDiagram(host,{W=640,H=260,aria='one neuron'}={}){
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':aria},host),L=el('g',{},svg);
  const ins=[[70,50],[70,130],[70,210]],S=[300,130],SG=[440,130];
  ins.forEach(([x,y],k)=>{node(L,x,y,24,`x${'₁₂₃'[k]}`);arrow(L,x+24,y,S[0]-34,S[1]+(y-130)*.25);
    label(L,(x+S[0])/2-4,(y+S[1])/2-8+(k-1)*6,`w${'₁₂₃'[k]}`,{fill:'var(--model)','text-anchor':'middle','font-size':15});});
  node(L,S[0],S[1],34,'Σ + b');arrow(L,S[0]+34,S[1],SG[0]-30,SG[1]);
  el('rect',{x:SG[0]-30,y:SG[1]-30,width:60,height:60,rx:10,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},L);
  mtxt(L,SG[0],SG[1]+7,'σ',{'text-anchor':'middle','font-size':24,fill:'var(--model)'});
  arrow(L,SG[0]+30,SG[1],560,SG[1]);mtxt(L,575,SG[1]+6,'p',{'font-size':20,fill:'var(--ink)','font-weight':700});
  return svg;}
// a fully connected layer picture: columns of nodes and all edges between neighbouring columns
function layerPos(n,x,top,bot){return Array.from({length:n},(_,i)=>[x,n===1?(top+bot)/2:top+i*(bot-top)/(n-1)]);}
function edges(L,A,B,{r=18,stroke='var(--line)',width=1.5}={}){
  const out=[];for(const a of A)for(const b of B)out.push(el('line',{x1:a[0]+r,y1:a[1],x2:b[0]-r,y2:b[1],stroke,'stroke-width':width},L));return out;}
// a softmax box to the right of output scores at heights ys, with arrows in and labels p₁, p₂, … out
function softmaxBox(L,x0,ys,{x=x0+36,w=80,names}={}){const top=Math.min(...ys)-40,bot=Math.max(...ys)+40;
  el('rect',{x,y:top,width:w,height:bot-top,rx:12,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},L);
  mtxt(L,x+w/2,(top+bot)/2+5,'softmax',{'text-anchor':'middle','font-size':14,fill:'var(--model)'});
  ys.forEach((y,k)=>{arrow(L,x0,y,x-2,y);mtxt(L,x+w+12,y+6,names?names[k]:`p${'₁₂₃₄₅₆₇₈₉'[k]}`,{'font-size':18,fill:'var(--ink)','font-weight':700});});}
