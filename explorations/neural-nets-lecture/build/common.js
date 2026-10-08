/* ================= Neural networks lectures: shared helpers ================= */
const $=id=>document.getElementById(id);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const MONO='JetBrains Mono,monospace';
function txt(parent,x,y,s,a={}){const t=el('text',{x,y,...a},parent);t.textContent=s;return t;}
const stepG=(parent,k)=>el('g',{'data-step':k},parent);
const sig=z=>1/(1+Math.exp(-z));
const label=(L,x,y,s,a={})=>txt(L,x,y,s,{'font-size':16,'font-weight':700,'font-family':MONO,'paint-order':'stroke',stroke:'var(--surface)','stroke-width':5,...a});
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

/* ---------- decision map of an MLP on the XOR box (inputs scaled u = (x − 5) / 2.5) ---------- */
function xorPlot(host,label,{H=430,fs=1.3}={}){
  const api=chart(host,{W:H*1.0,H,ml:58,fs,xmin:0,xmax:10,ymin:0,ymax:10,xticks:[0,5,10],yticks:[0,5,10],xlabel:'x₁',ylabel:'x₂',label});
  api.svg.classList.add('sq');return api;}
function drawMap(api,L,pfn,{N=40}={}){L.textContent='';L.classList.add('noanim');const h=10/N,cw=api.sx(h)-api.sx(0),ch=api.sy(0)-api.sy(h);
  for(let i=0;i<N;i++)for(let j=0;j<N;j++){const p=pfn([(i+.5)*h,(j+.5)*h]);
    el('rect',{x:api.sx(i*h),y:api.sy((j+1)*h),width:cw,height:ch,'shape-rendering':'crispEdges',fill:p>=.5?'var(--pos)':'var(--mean)',opacity:(.04+.32*Math.abs(p-.5)*2).toFixed(3)},L);}}
function drawPts(api,L,X,y,{r=7}={}){X.forEach((p,i)=>el('circle',{cx:api.sx(p[0]),cy:api.sy(p[1]),r,fill:y[i]>0?'var(--pos)':'var(--mean)',stroke:'var(--surface)','stroke-width':2},L));}
const xorP=P=>x=>mlpForward(P,[(x[0]-5)/2.5,(x[1]-5)/2.5]).p[0];

/* ---------- network diagrams ---------- */
function node(L,x,y,r,s,a={},ta={}){el('circle',{cx:x,cy:y,r,fill:'var(--surface)',stroke:'var(--ink)','stroke-width':1.8,...a},L);
  if(s)txt(L,x,y+6,s,{'text-anchor':'middle','font-size':17,'font-family':MONO,fill:'var(--ink)',...ta});}
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
  txt(L,SG[0],SG[1]+7,'σ',{'text-anchor':'middle','font-size':24,'font-family':MONO,fill:'var(--model)'});
  arrow(L,SG[0]+30,SG[1],560,SG[1]);txt(L,575,SG[1]+6,'p',{'font-size':20,'font-family':MONO,fill:'var(--ink)','font-weight':700});
  return svg;}
// a fully connected layer picture: columns of nodes and all edges between neighbouring columns
function layerPos(n,x,top,bot){return Array.from({length:n},(_,i)=>[x,n===1?(top+bot)/2:top+i*(bot-top)/(n-1)]);}
function edges(L,A,B,{r=18,stroke='var(--line)',width=1.5}={}){
  const out=[];for(const a of A)for(const b of B)out.push(el('line',{x1:a[0]+r,y1:a[1],x2:b[0]-r,y2:b[1],stroke,'stroke-width':width},L));return out;}
// a softmax box to the right of output scores at heights ys, with arrows in and labels p₁, p₂, … out
function softmaxBox(L,x0,ys,{x=x0+36,w=80,names}={}){const top=Math.min(...ys)-40,bot=Math.max(...ys)+40;
  el('rect',{x,y:top,width:w,height:bot-top,rx:12,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},L);
  txt(L,x+w/2,(top+bot)/2+5,'softmax',{'text-anchor':'middle','font-size':14,'font-family':MONO,fill:'var(--model)'});
  ys.forEach((y,k)=>{arrow(L,x0,y,x-2,y);txt(L,x+w+12,y+6,names?names[k]:`p${'₁₂₃₄₅₆₇₈₉'[k]}`,{'font-size':18,'font-family':MONO,fill:'var(--ink)','font-weight':700});});}
