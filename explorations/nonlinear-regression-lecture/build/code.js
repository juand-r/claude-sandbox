/* ================= Nonlinear regression lecture ================= */
const $=id=>document.getElementById(id);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const MONO='JetBrains Mono,monospace';
function txt(parent,x,y,s,a={}){const t=el('text',{x,y,...a},parent);t.textContent=s;return t;}
const dot=(a,b)=>{let s=0;for(let k=0;k<a.length;k++)s+=a[k]*b[k];return s;};
const mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
const sse=a=>{if(!a.length)return 0;const m=mean(a);return a.reduce((s,v)=>s+(v-m)**2,0);};
const neg=s=>s.replace(/-/g,'−');
const fx=(v,d=1)=>neg(v.toFixed(d));
const big=v=>Math.round(v).toLocaleString('en-US');
const stepG=(parent,k)=>el('g',{'data-step':k},parent);

/* ---------- datasets (the JSON block above the script; made by make_data.py) ----------
   DOSE: drug dosage (mg) → effectiveness (%), shaped like the lecture's example.
   LIN: a roughly linear cloud for linear SVR.  BMD: simulated bone density against age.
   TWO: simulated data with two features, for kNN in 2D. */
const DATA=JSON.parse($('nlr-data').textContent);
const {DOSE,LIN,BMD,TWO}=DATA;

/* ---------- regression tree, one feature (CART: squared error, midpoint thresholds) ---------- */
// every candidate threshold of x, with the SSE of splitting there and the two side means
function scanSplits(x,y){
  const o=x.map((_,i)=>i).sort((a,b)=>x[a]-x[b]||a-b),xs=o.map(i=>x[i]),ys=o.map(i=>y[i]),out=[];
  for(let k=1;k<xs.length;k++){if(xs[k]===xs[k-1])continue;
    const L=ys.slice(0,k),R=ys.slice(k);out.push({t:(xs[k-1]+xs[k])/2,sse:sse(L)+sse(R),mL:mean(L),mR:mean(R),nL:k,nR:xs.length-k});}
  return out;}
const argmin=c=>c.reduce((b,v,i)=>v.sse<c[b].sse-1e-9?i:b,0);
// grow until a node has fewer than minSplit points (or depth maxDepth, or zero error)
function growTree(x,y,{minSplit=2,maxDepth=Infinity}={},depth=0){
  const node={n:x.length,value:mean(y)};
  if(x.length<minSplit||depth>=maxDepth||sse(y)<1e-12)return node;
  const c=scanSplits(x,y);if(!c.length)return node;
  const t=c[argmin(c)].t,L=x.map((v,i)=>i).filter(i=>x[i]<t),R=x.map((v,i)=>i).filter(i=>x[i]>t);
  node.t=t;
  node.left=growTree(L.map(i=>x[i]),L.map(i=>y[i]),{minSplit,maxDepth},depth+1);
  node.right=growTree(R.map(i=>x[i]),R.map(i=>y[i]),{minSplit,maxDepth},depth+1);
  return node;}
const predictTree=(T,v)=>T.left?predictTree(v<T.t?T.left:T.right,v):T.value;
// the leaves as intervals [lo, hi) of x, left to right
function leafIntervals(T,lo,hi){return T.left?[...leafIntervals(T.left,lo,T.t),...leafIntervals(T.right,T.t,hi)]:[{lo,hi,value:T.value,n:T.n}];}

/* ---------- kNN regression: average y of the k nearest points (ties broken by data order) ---------- */
function knnPredict(X,y,q,k){
  const d=X.map((p,i)=>[Array.isArray(p)?(p[0]-q[0])**2+(p[1]-q[1])**2:Math.abs(p-q),i]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  const nb=d.slice(0,k).map(v=>v[1]);return {value:mean(nb.map(i=>y[i])),nb};}

/* ---------- SVR solver ----------
   ε-SVR dual in LIBSVM form: 2n variables β = (α, α*), signs z = (+1…, −1…), linear term
   p = (ε − y, ε + y); minimize ½ βᵀQβ + pᵀβ with Q_st = z_s z_t K(x_s, x_t), 0 ≤ β ≤ C, zᵀβ = 0.
   Solved by SMO with the maximal-violating-pair rule (Fan, Chen & Lin 2005), as in the SVM deck.
   Prediction f(x) = Σ (αᵢ − αᵢ*) K(xᵢ, x) + b; for the linear kernel also the slope w. */
const KERNEL={linear:()=>dot,rbf:g=>(a,b)=>{let s=0;for(let k=0;k<a.length;k++)s+=(a[k]-b[k])**2;return Math.exp(-g*s);}};
function svrSolve(X,y,{C=1,eps=1,K=dot,tol=1e-6,maxIter=500000}={}){
  const n=X.length,N=2*n,Kx=X.map(a=>X.map(b=>K(a,b)));
  const z=t=>t<n?1:-1,kk=(s,t)=>Kx[s%n][t%n],Q=(s,t)=>z(s)*z(t)*kk(s,t);
  const a=new Array(N).fill(0),G=Array.from({length:N},(_,t)=>t<n?eps-y[t]:eps+y[t-n]);
  let it=0;
  for(;it<maxIter;it++){
    let i=-1,j=-1,gmax=-Infinity,gmin=Infinity;
    for(let t=0;t<N;t++){const yt=z(t),v=-yt*G[t];
      if(((yt>0&&a[t]<C)||(yt<0&&a[t]>0))&&v>gmax){gmax=v;i=t;}
      if(((yt<0&&a[t]<C)||(yt>0&&a[t]>0))&&v<gmin){gmin=v;j=t;}}
    if(gmax-gmin<tol)break;
    const ai=a[i],aj=a[j];
    if(z(i)!==z(j)){
      const quad=Math.max(kk(i,i)+kk(j,j)+2*Q(i,j),1e-12),delta=(-G[i]-G[j])/quad,diff=a[i]-a[j];
      a[i]+=delta;a[j]+=delta;
      if(diff>0){if(a[j]<0){a[j]=0;a[i]=diff;}}else{if(a[i]<0){a[i]=0;a[j]=-diff;}}
      if(diff>0){if(a[i]>C){a[i]=C;a[j]=C-diff;}}else{if(a[j]>C){a[j]=C;a[i]=C+diff;}}
    }else{
      const quad=Math.max(kk(i,i)+kk(j,j)-2*Q(i,j),1e-12),delta=(G[i]-G[j])/quad,sum=a[i]+a[j];
      a[i]-=delta;a[j]+=delta;
      if(sum>C){if(a[i]>C){a[i]=C;a[j]=sum-C;}}else{if(a[j]<0){a[j]=0;a[i]=sum;}}
      if(sum>C){if(a[j]>C){a[j]=C;a[i]=sum-C;}}else{if(a[i]<0){a[i]=0;a[j]=sum;}}
    }
    const di=a[i]-ai,dj=a[j]-aj;
    for(let t=0;t<N;t++)G[t]+=Q(t,i)*di+Q(t,j)*dj;
  }
  if(it>=maxIter)throw new Error('svrSolve did not converge');
  // offset as LIBSVM computes it: average over free variables, else midpoint of the feasible interval
  let ub=Infinity,lb=-Infinity,nf=0,sf=0;const tb=1e-12*Math.max(1,C);
  for(let t=0;t<N;t++){const yg=z(t)*G[t];
    if(a[t]>=C-tb){if(z(t)<0)ub=Math.min(ub,yg);else lb=Math.max(lb,yg);}
    else if(a[t]<=tb){if(z(t)>0)ub=Math.min(ub,yg);else lb=Math.max(lb,yg);}
    else{nf++;sf+=yg;}}
  const b=-(nf>0?sf/nf:(ub+lb)/2);
  const coef=X.map((_,i)=>a[i]-a[i+n]),sv=[];coef.forEach((c,i)=>{if(Math.abs(c)>1e-8*Math.max(1,C))sv.push(i);});
  const f=q=>{let s=b;for(const i of sv)s+=coef[i]*K(X[i],q);return s;};
  const out={coef,b,sv,f,iters:it};
  if(K===dot)out.w=X[0].map((_,k)=>sv.reduce((s,i)=>s+coef[i]*X[i][k],0));
  return out;}
// points outside the tube and their total slack; a point within EDGE of the tube's edge counts as on it
// (points on the edge are where the solver puts free support vectors, exact only to its tolerance)
const EDGE=1e-3;
function tubeStats(m,x,y,eps){let out=0,slack=0,s2=0;
  x.forEach((v,i)=>{const r=Math.abs(y[i]-m.f([v]));s2+=(y[i]-m.f([v]))**2;if(r>eps+EDGE){out++;slack+=r-eps;}});
  return {out,slack,sse:s2};}
function olsFit(x,y){const mx=mean(x),my=mean(y);let sxy=0,sxx=0;x.forEach((v,i)=>{sxy+=(v-mx)*(y[i]-my);sxx+=(v-mx)**2;});const b1=sxy/sxx;return {b0:my-b1*mx,b1};}
window.__nlr={DATA,scanSplits,growTree,leafIntervals,predictTree,knnPredict,svrSolve,KERNEL,olsFit,tubeStats};   // used by tests/export.js

/* ---------- drawing ---------- */
const PT='var(--ink)';
function dots(api,L,x,y,{r=7,fill=PT}={}){return x.map((v,i)=>el('circle',{cx:api.sx(v),cy:api.sy(y[i]),r,fill,stroke:'var(--surface)','stroke-width':2},L));}
const DOSE_AX={xmin:0,xmax:40,ymin:-10,ymax:110,xticks:[0,10,20,30,40],yticks:[0,25,50,75,100],xlabel:'drug dosage (mg)',ylabel:'effectiveness (%)'};
const dosePlot=(host,o={})=>chart(host,{W:640,H:420,ml:74,fs:1.35,...DOSE_AX,...o});
// path through the points (x, f(x)) for x on a fine grid of [x0, x1]
function fnPath(api,f,x0,x1,n=240){let d='';for(let i=0;i<=n;i++){const x=x0+(x1-x0)*i/n;d+=(i?'L':'M')+api.sx(x).toFixed(1)+' '+api.sy(f(x)).toFixed(1);}return d;}
// a tree's prediction: flat over each leaf interval, vertical jumps at the thresholds
function stepPath(api,I){return I.map((s,k)=>(k?'L':'M')+api.sx(s.lo).toFixed(1)+' '+api.sy(s.value).toFixed(1)+'H'+api.sx(s.hi).toFixed(1)).join('');}
const vline=(api,L,x,a={})=>el('line',{x1:api.sx(x),x2:api.sx(x),y1:api.sy(api.ymin??0),y2:api.sy(api.ymax??1),stroke:'var(--hi)','stroke-width':2,'stroke-dasharray':'6 5',...a},L);
function ring(api,L,x,y,{color='var(--hi)',r=12,w=3}={}){return el('circle',{cx:api.sx(x),cy:api.sy(y),r,fill:'none',stroke:color,'stroke-width':w},L);}
const label=(L,x,y,s,a={})=>txt(L,x,y,s,{'font-size':16,'font-weight':700,'font-family':MONO,'paint-order':'stroke',stroke:'var(--surface)','stroke-width':5,...a});
const DOSE_TREE=growTree(DOSE.x,DOSE.y,{minSplit:7});

/* ---------- not every pattern is a line ---------- */
{
  const api=dosePlot($('fig-why'),{label:'dosage against effectiveness, with a least-squares line and a regression tree'});
  const {x,y}=DOSE,ols=olsFit(x,y);
  el('path',{d:fnPath(api,v=>ols.b0+ols.b1*v,0,40,2),fill:'none',stroke:'var(--mean)','stroke-width':3.5,'stroke-linecap':'round'},stepG(api.layer('fit'),1));
  el('path',{d:stepPath(api,leafIntervals(DOSE_TREE,0,40)),fill:'none',stroke:'var(--model)','stroke-width':3.5,'stroke-linejoin':'round'},stepG(api.layer('fit'),2));
  dots(api,api.layer('pts'),x,y);
}

/* ---------- a regression tree: the fit and the tree ---------- */
{
  const api=dosePlot($('fig-rt'),{H:440,label:'the regression tree\'s prediction over the dosage data'});
  const {x,y}=DOSE,I=leafIntervals(DOSE_TREE,0,40),pick=I.findIndex(s=>s.lo<26&&s.hi>26),P=I[pick];
  const g2=stepG(api.layer('fit'),2),g3=stepG(api.layer('heat'),3),g3a=stepG(api.layer('anno'),3);
  I.forEach(s=>{if(s.lo>0)vline(api,g2,s.lo,{stroke:'var(--muted)','stroke-width':1.5,opacity:.7});});
  el('path',{d:stepPath(api,I),fill:'none',stroke:'var(--model)','stroke-width':3.5,'stroke-linejoin':'round'},g2);
  el('rect',{x:api.sx(P.lo),y:api.sy(110),width:api.sx(P.hi)-api.sx(P.lo),height:api.sy(-10)-api.sy(110),fill:'var(--hi-soft)'},g3);
  el('line',{x1:api.sx(P.lo),x2:api.sx(P.hi),y1:api.sy(P.value),y2:api.sy(P.value),stroke:'var(--hi)','stroke-width':5,'stroke-linecap':'round'},g3a);
  x.forEach((v,i)=>{if(v>P.lo&&v<P.hi)ring(api,g3a,v,y[i]);});
  label(g3a,api.sx(P.hi)+8,api.sy(P.value)-10,fx(P.value),{fill:'var(--hi)'});
  dots(api,api.layer('pts'),x,y);

  // the tree diagram: leaves spread left to right in order, parents centred over their children
  const W=520,H=440,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'regression tree: dosage below 14.5 gives 4.2; otherwise dosage of 29 or more gives 3.0; otherwise below 23.5 gives 100.0 and from 23.5 to 29 gives 55.3'},$('fig-rt-tree'));
  const gE=el('g',{},svg),gN=el('g',{},svg);
  let leafNo=0;const nLeaves=I.length,depthOf=T=>T.left?1+Math.max(depthOf(T.left),depthOf(T.right)):0,D=depthOf(DOSE_TREE);
  const place=(T,d)=>{T.d=d;if(!T.left){T.px=56+leafNo++*(W-112)/(nLeaves-1);}else{place(T.left,d+1);place(T.right,d+1);T.px=(T.left.px+T.right.px)/2;}T.py=40+d*(H-80)/D;};
  place(DOSE_TREE,0);
  const draw=T=>{
    const leaf=!T.left,s=leaf?fx(T.value)+'%':`dosage < ${T.t}`,w=leaf?92:176,h=40,isPick=leaf&&Math.abs(T.value-P.value)<1e-9;
    if(!leaf)for(const [c,yes] of [[T.left,true],[T.right,false]]){
      el('path',{d:`M${T.px} ${T.py+h/2}L${c.px} ${c.py-h/2}`,stroke:'var(--muted)','stroke-width':1.8,fill:'none'},gE);
      txt(gE,(T.px+c.px)/2+(yes?-10:10),(T.py+c.py)/2+4,yes?'yes':'no',{'text-anchor':yes?'end':'start','font-size':14,fill:'var(--muted)','font-family':MONO});}
    const g=el('g',{},gN);
    el('rect',{x:T.px-w/2,y:T.py-h/2,width:w,height:h,rx:leaf?20:8,fill:leaf?'var(--model-soft)':'var(--surface)',stroke:leaf?'var(--model)':'var(--ink)','stroke-width':1.6},g);
    txt(g,T.px,T.py+6,s,{'text-anchor':'middle','font-size':16,'font-weight':600,'font-family':MONO,fill:leaf?'var(--model)':'var(--ink)'});
    if(isPick){const gp=stepG(g,3);el('rect',{x:T.px-w/2-4,y:T.py-h/2-4,width:w+8,height:h+8,rx:24,fill:'none',stroke:'var(--hi)','stroke-width':3.5},gp);}
    if(!leaf){draw(T.left);draw(T.right);}};
  draw(DOSE_TREE);
}

/* ---------- choosing a split: SSE of every threshold ---------- */
{
  const {x,y}=DOSE,C=scanSplits(x,y),best=argmin(C);
  const api=dosePlot($('fig-split'),{H:330,label:'one candidate threshold with the mean on each side'});
  const sapi=chart($('fig-sse'),{W:640,H:210,ml:74,fs:1.35,xmin:0,xmax:40,ymin:0,ymax:30000,xticks:[0,10,20,30,40],yticks:[0,10000,20000,30000],yfmt:v=>v?v/1000+'k':'0',xlabel:'threshold (mg)',ylabel:'SSE',label:'SSE for every candidate threshold'});
  const gT=stepG(api.layer('anno'),1),gR=stepG(api.layer('resid'),1),gM=stepG(api.layer('fit'),1);
  const gAll=stepG(sapi.layer('fit'),2),gBest=stepG(sapi.layer('anno'),3),gCur=stepG(sapi.layer('pts'),1);
  el('path',{d:C.map((c,k)=>(k?'L':'M')+sapi.sx(c.t)+' '+sapi.sy(c.sse)).join(''),fill:'none',stroke:'var(--err)','stroke-width':2,opacity:.6},gAll);
  C.forEach(c=>el('circle',{cx:sapi.sx(c.t),cy:sapi.sy(c.sse),r:4.5,fill:'var(--err)'},gAll));
  ring(sapi,gBest,C[best].t,C[best].sse,{r:10,w:2.5});
  dots(api,api.layer('pts'),x,y,{r:6.5});
  const inp=$('r-split');inp.max=C.length-1;
  const set=act('split',k=>{inp.value=k;const c=C[k];
    gT.textContent='';gR.textContent='';gM.textContent='';gCur.textContent='';
    vline(api,gT,c.t);
    for(const [lo,hi,m] of [[0,c.t,c.mL],[c.t,40,c.mR]])el('line',{x1:api.sx(lo),x2:api.sx(hi),y1:api.sy(m),y2:api.sy(m),stroke:'var(--model)','stroke-width':3.5,'stroke-linecap':'round'},gM);
    x.forEach((v,i)=>{const m=v<c.t?c.mL:c.mR;el('line',{x1:api.sx(v),x2:api.sx(v),y1:api.sy(y[i]),y2:api.sy(m),stroke:'var(--err)','stroke-width':2.5,'stroke-linecap':'round'},gR);});
    el('circle',{cx:sapi.sx(c.t),cy:sapi.sy(c.sse),r:7.5,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2},gCur);
    $('v-sp-t').textContent=c.t;$('v-sp-l').textContent=fx(c.mL);$('v-sp-r').textContent=fx(c.mR);$('v-sp-s').textContent=big(c.sse);});
  inp.addEventListener('input',()=>set(+inp.value));
  hooks['s-split']={step(s){const k={0:0,1:0,3:best}[s];if(k!==undefined)set(k);}};
  set(0);
}

/* ---------- grow, then stop ---------- */
{
  const {x,y}=DOSE,api=dosePlot($('fig-grow'),{label:'regression tree fit for a chosen stopping rule'});
  const gFit=stepG(api.layer('fit'),1),gThr=stepG(api.layer('extra'),1),inp=$('r-grow');
  dots(api,api.layer('pts'),x,y);
  const set=act('grow',v=>{inp.value=v;const T=growTree(x,y,{minSplit:v}),I=leafIntervals(T,0,40);
    gFit.textContent='';gThr.textContent='';
    I.forEach(s=>{if(s.lo>0)vline(api,gThr,s.lo,{stroke:'var(--muted)','stroke-width':1.3,opacity:.6});});
    el('path',{d:stepPath(api,I),fill:'none',stroke:'var(--model)','stroke-width':3.5,'stroke-linejoin':'round'},gFit);
    $('v-gr-m').textContent=v;$('v-gr-n').textContent=I.length;
    $('v-gr-s').textContent=big(x.reduce((s,v2,i)=>s+(y[i]-predictTree(T,v2))**2,0));});
  inp.addEventListener('input',()=>set(+inp.value));
  hooks['s-grow']={step(s){const v={0:2,1:2,2:7,3:19,4:7}[s];if(v!==undefined)set(v);}};
  set(2);
}

/* ---------- kNN regression ---------- */
{
  const {x,y}=BMD,Q=40,inp=$('r-knn');inp.max=x.length;
  const api=chart($('fig-knn'),{W:640,H:420,ml:80,fs:1.35,xmin:10,xmax:85,ymin:.7,ymax:1.2,xticks:[10,25,40,55,70,85],yticks:[.7,.8,.9,1,1.1,1.2],yfmt:v=>v.toFixed(1),xlabel:'age (years)',ylabel:'bone density',label:'bone density against age with a kNN regression curve'});
  const gQ=stepG(api.layer('anno'),1),gQl=stepG(api.layer('extra'),1),gC=stepG(api.layer('fit'),2);
  dots(api,api.layer('pts'),x,y,{r:6});
  const set=act('knn',k=>{inp.value=k;gQ.textContent='';gQl.textContent='';gC.textContent='';
    const {value,nb}=knnPredict(x,y,Q,k);
    // the curve: kNN prediction on a fine grid of ages
    el('path',{d:fnPath(api,v=>knnPredict(x,y,v,k).value,10,85,600),fill:'none',stroke:'var(--model)','stroke-width':3,'stroke-linejoin':'round'},gC);
    nb.forEach(i=>ring(api,gQ,x[i],y[i],{r:10,w:2.5}));
    vline(api,gQl,Q);
    el('line',{x1:api.sx(10),x2:api.sx(85),y1:api.sy(value),y2:api.sy(value),stroke:'var(--hi)','stroke-width':1.5,'stroke-dasharray':'3 5'},gQl);
    el('circle',{cx:api.sx(Q),cy:api.sy(value),r:9,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2.5},gQ);
    $('v-kn-k').textContent=k;$('v-kn-p').textContent=value.toFixed(3);
    $('v-kn-s').textContent=x.reduce((s,v,i)=>s+(y[i]-knnPredict(x,y,v,k).value)**2,0).toFixed(3);});
  inp.addEventListener('input',()=>set(+inp.value));
  hooks['s-knn']={step(s){const k={0:9,1:9,2:9,3:1,4:40}[s];if(k!==undefined)set(k);}};
  set(9);
}

/* ---------- kNN with two features: prediction maps for k = 1 and k = 9 ---------- */
const VIRIDIS=['#440154','#3B528B','#21918C','#5EC962','#FDE725'];
function viridis(t){t=clamp(t,0,1)*(VIRIDIS.length-1);const i=Math.min(VIRIDIS.length-2,Math.floor(t)),u=t-i;
  const c=s=>[1,3,5].map(k=>parseInt(s.slice(k,k+2),16)),a=c(VIRIDIS[i]),b=c(VIRIDIS[i+1]);
  return 'rgb('+a.map((v,k)=>Math.round(v+(b[k]-v)*u)).join(',')+')';}
{
  const {X,y}=TWO,lo=Math.min(...y),hi=Math.max(...y),col=v=>viridis((v-lo)/(hi-lo)),N=50;
  for(const [id,k] of [['fig-k1',1],['fig-k9',9]]){
    const api=chart($(id),{W:430,H:416,ml:58,fs:1.35,xmin:0,xmax:10,ymin:0,ymax:10,xticks:[0,5,10],yticks:[0,5,10],xlabel:'x₁',ylabel:'x₂',label:`kNN prediction map, k = ${k}`});
    const L=api.layer('heat'),h=10/N,cw=api.sx(h)-api.sx(0),ch=api.sy(0)-api.sy(h);L.classList.add('noanim');   // thousands of cells: no draw-in
    for(let i=0;i<N;i++)for(let j=0;j<N;j++)el('rect',{x:api.sx(i*h),y:api.sy((j+1)*h),width:cw+.6,height:ch+.6,fill:col(knnPredict(X,y,[(i+.5)*h,(j+.5)*h],k).value)},L);
    X.forEach((p,i)=>el('circle',{cx:api.sx(p[0]),cy:api.sy(p[1]),r:5.5,fill:col(y[i]),stroke:'#fff','stroke-width':1.6},api.layer('pts')));
  }
}

/* ---------- SVR: tube, slack ---------- */
// draw an SVR fit: shaded tube, dashed tube edges, the prediction line, and vertical slack segments
function drawSVR(api,G,m,x,y,eps,{x0,x1,labels=false}){
  G.tube.textContent='';G.slack.textContent='';if(G.lab)G.lab.textContent='';
  const up=fnPath(api,v=>m.f([v])+eps,x0,x1),dn=fnPath(api,v=>m.f([v])-eps,x1,x0);
  el('path',{d:up+dn.replace(/^M/,'L')+'Z',fill:'var(--model-soft)',stroke:'none'},G.tube);
  for(const s of [1,-1])el('path',{d:fnPath(api,v=>m.f([v])+s*eps,x0,x1),fill:'none',stroke:'var(--model)','stroke-width':2,'stroke-dasharray':'7 6',opacity:.85},G.tube);
  el('path',{d:fnPath(api,v=>m.f([v]),x0,x1),fill:'none',stroke:'var(--model)','stroke-width':3.5,'stroke-linecap':'round'},G.tube);
  x.forEach((v,i)=>{const f=m.f([v]),r=y[i]-f;if(Math.abs(r)<=eps+EDGE)return;
    el('line',{x1:api.sx(v),x2:api.sx(v),y1:api.sy(y[i]),y2:api.sy(f+Math.sign(r)*eps),stroke:'var(--err)','stroke-width':3,'stroke-linecap':'round'},G.slack);});
  if(labels){const xe=x1-.15,ye=m.f([xe]);
    for(const [s,t] of [[1,'w · x + b + ε'],[0,'w · x + b'],[-1,'w · x + b − ε']])
      label(G.lab,api.sx(xe)+12,api.sy(ye+s*eps)+5,t,{fill:'var(--model)','font-size':15});
    // ε bracket near the left end
    const xb=x0+.45,fb=m.f([xb]),Lb=G.lab;
    el('line',{x1:api.sx(xb),x2:api.sx(xb),y1:api.sy(fb),y2:api.sy(fb+eps),stroke:'var(--hi)','stroke-width':2.5},Lb);
    for(const v of [fb,fb+eps])el('line',{x1:api.sx(xb)-6,x2:api.sx(xb)+6,y1:api.sy(v),y2:api.sy(v),stroke:'var(--hi)','stroke-width':2.5},Lb);
    label(Lb,api.sx(xb)-10,api.sy(fb+eps/2)+6,'ε',{fill:'var(--hi)','text-anchor':'end','font-size':18});}
}
const linPlot=(host,label)=>chart(host,{W:640,H:420,ml:62,mr:150,fs:1.35,xmin:0,xmax:10,ymin:0,ymax:26,xticks:[0,2,4,6,8,10],yticks:[0,5,10,15,20,25],xlabel:'x',ylabel:'y',label});
const LX=LIN.x.map(v=>[v]);
{
  const {x,y}=LIN,C=0.1,api=linPlot($('fig-svr'),'linear SVR with its ε-tube');
  const G={tube:stepG(api.layer('fit'),1),slack:stepG(api.layer('resid'),2),lab:stepG(api.layer('anno'),1)};
  dots(api,api.layer('pts'),x,y);
  const inp=$('r-svr');
  const set=act('svr',v=>{inp.value=v;const eps=v/4,m=svrSolve(LX,y,{C,eps}),st=tubeStats(m,x,y,eps);
    drawSVR(api,G,m,x,y,eps,{x0:0,x1:10,labels:true});
    $('v-sv-e').textContent=eps.toFixed(2);$('v-sv-n').textContent=st.out;$('v-sv-x').textContent=st.slack.toFixed(1);});
  inp.addEventListener('input',()=>set(+inp.value));
  hooks['s-svr']={step(s){set(8);}};
  set(8);
}
{
  const {x,y}=LIN,eps=2,api=linPlot($('fig-svrc'),'linear SVR for a chosen C');
  const G={tube:api.layer('fit'),slack:api.layer('resid'),lab:api.layer('anno')};
  dots(api,api.layer('pts'),x,y);
  const inp=$('r-svrc');
  const set=act('svrc',v=>{inp.value=v;const C=10**(v/100),m=svrSolve(LX,y,{C,eps}),st=tubeStats(m,x,y,eps);
    drawSVR(api,G,m,x,y,eps,{x0:0,x1:10,labels:true});
    $('v-sc-c').textContent=`C = ${C<1?C.toFixed(C<.1?3:2):C.toFixed(C<10?1:0)}`;
    $('v-sc-w').textContent=m.w[0].toFixed(2);$('v-sc-n').textContent=st.out;$('v-sc-x').textContent=st.slack.toFixed(1);});
  inp.addEventListener('input',()=>set(+inp.value));
  hooks['s-svrobj']={step(s){const v={0:-100,1:-100,2:100,3:-200,4:-100}[s];if(v!==undefined)set(v);}};
  set(-100);
}

/* ---------- nonlinear SVR on the dosage data ---------- */
{
  const {x,y}=DOSE,DX=x.map(v=>[v]),C=1000,eps=5,api=dosePlot($('fig-svrk'),{label:'SVR on the dosage data'});
  const G={tube:stepG(api.layer('fit'),1),slack:stepG(api.layer('resid'),1)};
  dots(api,api.layer('pts'),x,y);
  let kern='linear',lg=-1.7;
  const set=act('svrk',([k,l])=>{kern=k;lg=l;$('r-sk-g').value=Math.round(l*100);
    const g=10**lg,m=svrSolve(DX,y,{C,eps,K:kern==='linear'?KERNEL.linear():KERNEL.rbf(g)}),st=tubeStats(m,x,y,eps);
    drawSVR(api,G,m,x,y,eps,{x0:0,x1:40});
    $('v-sk-k').textContent=kern==='linear'?'linear':'RBF';$('v-sk-n').textContent=st.out;$('v-sk-s').textContent=big(st.sse);
    $('v-sk-g').textContent=kern==='rbf'?`γ = ${g<.01?g.toFixed(4):g<.1?g.toFixed(3):g.toFixed(2)}`:'';
    $('r-sk-g').disabled=kern!=='rbf';
    $('b-sk-linear').classList.toggle('sel',kern==='linear');$('b-sk-rbf').classList.toggle('sel',kern==='rbf');});
  $('b-sk-linear').onclick=()=>set(['linear',lg]);$('b-sk-rbf').onclick=()=>set(['rbf',lg]);
  $('r-sk-g').addEventListener('input',e=>set(['rbf',e.target.value/100]));
  const PRESET={0:['linear',-1.7],1:['linear',-1.7],2:['rbf',-1.7],3:['rbf',-.7]};
  hooks['s-svrk']={step(s){if(PRESET[s])set(PRESET[s]);}};
  set(PRESET[0]);
}
