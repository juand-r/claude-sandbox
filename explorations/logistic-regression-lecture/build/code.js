/* ================= Logistic regression lecture ================= */
const $=id=>document.getElementById(id);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function txt(parent,x,y,s,a={}){const t=el('text',{x,y,...a},parent);t.textContent=s;return t;}
/* ---------- math labels in SVG, in the KaTeX fonts (embedded by build/tex.js) ---------- */
// Write labels as plain text: single letters become italic variables, words and digits stay upright,
// ℒ is the script L (upright:true keeps every letter upright, for units), and subscripts are written with Unicode (x₁, wⱼᵢ) or as _N (x_N).
// Each run of characters gets its own <tspan>; subscripts are smaller and lowered.
const MATH_SCALE=1.15;   // KaTeX's glyphs are smaller than the mono font's at the same size
const SUB={'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','ᵢ':'i','ⱼ':'j','ₖ':'k'},SUP={'ᵀ':'T'};
const isLatin=c=>/[A-Za-z]/.test(c||''),GREEK_IT='αβγδεηθλμπσφω';
function mathRuns(s,upright=false){
  const runs=[],push=(t,fam,it,shift)=>{const r=runs[runs.length-1];
    if(r&&r.fam===fam&&r.it===it&&r.shift===shift)r.t+=t;else runs.push({t,fam,it,shift});};
  for(let i=0;i<s.length;i++){let c=s[i],shift=0;
    if(c==='_'&&i+1<s.length){c=s[++i];shift=1;}
    else if(SUB[c]){c=SUB[c];shift=1;}
    else if(SUP[c]){c=SUP[c];shift=-1;}
    const word=shift===0&&isLatin(c)&&(isLatin(s[i-1])||isLatin(s[i+1]));
    if(c==='ℒ')push('L','KaTeX_Caligraphic',false,shift);
    else if(isLatin(c)&&!word&&!upright)push(c,'KaTeX_Math',true,shift);
    else if(GREEK_IT.includes(c))push(c,'KaTeX_Math',true,shift);
    else push(c==='·'?'⋅':c,'KaTeX_Main',false,shift);}
  return runs;}
function mtxt(parent,x,y,s,a={}){
  const {upright,...rest}=a,fs=(+a['font-size']||16)*MATH_SCALE,t=el('text',{x,y,...rest,'font-size':fs.toFixed(1)},parent);
  let cur=0;   // the current baseline offset in px
  for(const r of mathRuns(String(s),a.upright)){const off=r.shift===1?.28*fs:r.shift===-1?-.4*fs:0;
    const sp=el('tspan',{'font-family':r.fam,'font-style':r.it?'italic':'normal',dy:(off-cur).toFixed(1)},t);
    if(r.shift)sp.setAttribute('font-size',(.72*fs).toFixed(1));
    sp.textContent=r.t;cur=off;}
  t.setAttribute('aria-label',s);return t;}
const dot=(a,b)=>{let s=0;for(let k=0;k<a.length;k++)s+=a[k]*b[k];return s;};
const stepG=(parent,k)=>el('g',{'data-step':k},parent);
const sigmoid=z=>1/(1+Math.exp(-z));
const label=(L,x,y,s,a={})=>mtxt(L,x,y,s,{'font-size':16,'font-weight':700,'paint-order':'stroke',stroke:'var(--surface)','stroke-width':5,...a});

// the engine's chart() draws tick numbers and axis names in its own fonts; redraw them as math labels
const engineChart=chart;
chart=function(host,o){const api=engineChart(host,o);
  for(const t of [...api.svg.querySelectorAll('text')]){const a={};
    for(const at of t.attributes)if(at.name!=='font-family')a[at.name]=at.value;
    t.replaceWith(mtxt(t.parentNode,a.x,a.y,t.textContent,a));}
  return api;};

/* ---------- datasets ----------
   HOURS: hours of study → pass (+1) or fail (−1), 10 each, overlapping between 3.3 and 7.4 hours (simulated).
   SOFT: the soft-margin dataset of the SVM deck (its separable set plus two points on the wrong side). */
const HOURS={x:[0.6,1.4,2.2,3.0,3.6,4.3,4.9,5.6,6.3,7.4, 3.3,4.6,5.3,6.0,6.8,7.1,7.7,8.4,9.0,9.6],
             y:[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1,1,1,1,1,1,1,1,1,1]};
const SOFT={X:[[5.5,6.5],[7,5],[8,7.5],[6.5,8.5],[8.5,5.5],[9,8],[5,8.5],
              [4.5,3.5],[3,4],[2,2],[1.5,4.5],[5,2.5],[2,5.5],[3.5,1.5],[6,1],[6.5,6.2],[4.2,5]],
            y:[1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1]};

/* ---------- logistic regression by Newton's method ----------
   Minimizes ½‖w‖² + C Σ log(1 + exp(−yᵢ(w·xᵢ + b))) (b not penalized), the objective of scikit-learn's
   LogisticRegression; C = Infinity drops the ½‖w‖² term. The objective is convex and smooth, so Newton's
   method converges in a few steps. (The deck does not teach how the fit is found: that is next lecture.) */
function solveLinear(A,g){const n=g.length,M=A.map((r,i)=>[...r,g[i]]);
  for(let c=0;c<n;c++){let p=c;for(let r=c+1;r<n;r++)if(Math.abs(M[r][c])>Math.abs(M[p][c]))p=r;[M[c],M[p]]=[M[p],M[c]];
    for(let r=0;r<n;r++){if(r===c)continue;const f=M[r][c]/M[c][c];for(let k=c;k<=n;k++)M[r][k]-=f*M[c][k];}}
  return M.map((r,i)=>r[n]/r[i]);}
function logisticFit(X,y,{C=1,iters=100,tol=1e-12}={}){
  const d=X[0].length,lam=isFinite(C)?1:0,c=isFinite(C)?C:1,A=X.map(x=>[...x,1]);let th=new Array(d+1).fill(0);
  for(let it=0;it<iters;it++){
    const g=th.map((t,k)=>k<d?lam*t:0),H=th.map((_,i)=>th.map((_,j)=>i===j&&i<d?lam:0));
    A.forEach((a,i)=>{const f=dot(a,th),s=sigmoid(-y[i]*f),w=sigmoid(f)*(1-sigmoid(f));
      a.forEach((ak,k)=>{g[k]-=c*y[i]*s*ak;a.forEach((al,l)=>{H[k][l]+=c*w*ak*al;});});});
    const step=solveLinear(H,g);th=th.map((t,k)=>t-step[k]);
    if(Math.sqrt(dot(step,step))<tol)break;}
  const w=th.slice(0,d),b=th[d];
  return {w,b,f:x=>dot(w,x)+b,p:x=>sigmoid(dot(w,x)+b)};}

/* ---------- SVM solver (copied from the SVM deck, where check_numbers.py tests it against scikit-learn) ---------- */
const HARD_C=1e4;
function svmSolve(X,y,{C=1,K=dot,eps=1e-7,maxIter=200000,strict=true}={}){
  const n=X.length,Kx=X.map(a=>X.map(b=>K(a,b))),Q=(i,j)=>y[i]*y[j]*Kx[i][j];
  const a=new Array(n).fill(0),G=new Array(n).fill(-1);
  let it=0;
  for(;it<maxIter;it++){
    let i=-1,j=-1,gmax=-Infinity,gmin=Infinity;
    for(let t=0;t<n;t++){const v=-y[t]*G[t];
      if(((y[t]>0&&a[t]<C)||(y[t]<0&&a[t]>0))&&v>gmax){gmax=v;i=t;}
      if(((y[t]<0&&a[t]<C)||(y[t]>0&&a[t]>0))&&v<gmin){gmin=v;j=t;}}
    if(gmax-gmin<eps)break;
    const ai=a[i],aj=a[j];
    if(y[i]!==y[j]){
      const quad=Math.max(Kx[i][i]+Kx[j][j]+2*Q(i,j),1e-12),delta=(-G[i]-G[j])/quad,diff=a[i]-a[j];
      a[i]+=delta;a[j]+=delta;
      if(diff>0){if(a[j]<0){a[j]=0;a[i]=diff;}}else{if(a[i]<0){a[i]=0;a[j]=-diff;}}
      if(diff>0){if(a[i]>C){a[i]=C;a[j]=C-diff;}}else{if(a[j]>C){a[j]=C;a[i]=C+diff;}}
    }else{
      const quad=Math.max(Kx[i][i]+Kx[j][j]-2*Q(i,j),1e-12),delta=(G[i]-G[j])/quad,sum=a[i]+a[j];
      a[i]-=delta;a[j]+=delta;
      if(sum>C){if(a[i]>C){a[i]=C;a[j]=sum-C;}}else{if(a[j]<0){a[j]=0;a[i]=sum;}}
      if(sum>C){if(a[j]>C){a[j]=C;a[i]=sum-C;}}else{if(a[i]<0){a[i]=0;a[j]=sum;}}
    }
    const di=a[i]-ai,dj=a[j]-aj;
    for(let t=0;t<n;t++)G[t]+=Q(t,i)*di+Q(t,j)*dj;
  }
  const converged=it<maxIter;
  if(!converged&&strict)throw new Error('svmSolve did not converge');
  let ub=Infinity,lb=-Infinity,nf=0,sf=0;const tol=1e-12*Math.max(1,C);
  for(let t=0;t<n;t++){const yg=y[t]*G[t];
    if(a[t]>=C-tol){if(y[t]<0)ub=Math.min(ub,yg);else lb=Math.max(lb,yg);}
    else if(a[t]<=tol){if(y[t]>0)ub=Math.min(ub,yg);else lb=Math.max(lb,yg);}
    else{nf++;sf+=yg;}}
  const b=-(nf>0?sf/nf:(ub+lb)/2);
  const sv=[];for(let t=0;t<n;t++)if(a[t]>1e-8*Math.max(1,C))sv.push(t);
  const f=x=>{let s=b;for(const t of sv)s+=a[t]*y[t]*K(X[t],x);return s;};
  const out={alpha:a,b,sv,f,iters:it,converged};
  if(K===dot){out.w=X[0].map((_,k)=>sv.reduce((s,t)=>s+a[t]*y[t]*X[t][k],0));}
  return out;
}

const HOURS_FIT=logisticFit(HOURS.x.map(v=>[v]),HOURS.y,{C:Infinity});
const SOFT_LR=logisticFit(SOFT.X,SOFT.y,{C:1});
const SOFT_SVM=svmSolve(SOFT.X,SOFT.y,{C:1});
window.__lr={HOURS,SOFT,logisticFit,svmSolve,HOURS_FIT,SOFT_LR,SOFT_SVM};   // used by tests/export.js

/* ---------- loss curves against y·f(x) ---------- */
const LOSSES={zero:z=>z<=0?1:0,hinge:z=>Math.max(0,1-z),log:z=>Math.log(1+Math.exp(-z))};
function lossPlot(host,label){
  const api=chart(host,{W:640,H:420,ml:62,fs:1.35,xmin:-3,xmax:3,ymin:0,ymax:4,xticks:[-3,-2,-1,0,1,2,3],yticks:[0,1,2,3,4],
    xfmt:v=>String(v).replace('-','−'),xlabel:'y · f(x)',ylabel:'loss',label});
  const path=f=>{let d='';for(let i=0;i<=300;i++){const z=-3+6*i/300;d+=(i?'L':'M')+api.sx(z).toFixed(1)+' '+api.sy(f(z)).toFixed(1);}return d;};
  const zero=`M${api.sx(-3)} ${api.sy(1)}H${api.sx(0)}V${api.sy(0)}H${api.sx(3)}`;
  return {api,path,zero};}
{
  const {api,path,zero}=lossPlot($('fig-hinge'),'0–1 loss and hinge loss against y times f(x)');
  el('path',{d:zero,fill:'none',stroke:'var(--err)','stroke-width':3},api.layer('fit'));
  el('path',{d:path(LOSSES.hinge),fill:'none',stroke:'var(--model)','stroke-width':3.5},stepG(api.layer('fit'),1));
  // the margin: points with y f(x) ≥ 1 pay nothing
  const g3=stepG(api.layer('heat'),3);
  el('rect',{x:api.sx(1),y:api.sy(4),width:api.sx(3)-api.sx(1),height:api.sy(0)-api.sy(4),fill:'var(--model-soft)'},g3);
  label(stepG(api.layer('anno'),3),api.sx(2),api.sy(3.4),'no loss',{fill:'var(--model)','text-anchor':'middle'});
}
{
  const {api,path,zero}=lossPlot($('fig-loss'),'0–1, hinge and log loss against y times f(x)');
  el('path',{d:zero,fill:'none',stroke:'var(--err)','stroke-width':3},api.layer('fit'));
  el('path',{d:path(LOSSES.hinge),fill:'none',stroke:'var(--model)','stroke-width':3.5},api.layer('fit'));
  el('path',{d:path(LOSSES.log),fill:'none',stroke:'var(--hi)','stroke-width':3.5},api.layer('fit'));
}

/* ---------- the sigmoid ---------- */
{
  const api=chart($('fig-sig'),{W:640,H:400,ml:62,fs:1.35,xmin:-6,xmax:6,ymin:0,ymax:1,xticks:[-6,-4,-2,0,2,4,6],yticks:[0,.25,.5,.75,1],
    xfmt:v=>String(v).replace('-','−'),xlabel:'score z',ylabel:'σ(z)',label:'the sigmoid function'});
  let d='';for(let i=0;i<=240;i++){const z=-6+12*i/240;d+=(i?'L':'M')+api.sx(z).toFixed(1)+' '+api.sy(sigmoid(z)).toFixed(1);}
  el('path',{d,fill:'none',stroke:'var(--model)','stroke-width':3.5},api.layer('fit'));
  const L=api.layer('anno');
  for(const z of [-2,0,2]){const p=sigmoid(z);
    el('line',{x1:api.sx(z),x2:api.sx(z),y1:api.sy(0),y2:api.sy(p),stroke:'var(--hi)','stroke-width':1.5,'stroke-dasharray':'4 4'},L);
    el('line',{x1:api.sx(-6),x2:api.sx(z),y1:api.sy(p),y2:api.sy(p),stroke:'var(--hi)','stroke-width':1.5,'stroke-dasharray':'4 4'},L);
    el('circle',{cx:api.sx(z),cy:api.sy(p),r:6,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2},L);
    label(L,api.sx(z)+10,api.sy(p)+(z>0?18:-8),p.toFixed(2),{fill:'var(--hi)'});}
}

/* ---------- one feature: fitted probability curve and a threshold ---------- */
{
  const {x,y}=HOURS,m=HOURS_FIT,lift=v=>v>0?1:0;
  const api=chart($('fig-fit'),{W:640,H:400,ml:62,fs:1.35,xmin:0,xmax:10,ymin:-.06,ymax:1.06,xticks:[0,2,4,6,8,10],yticks:[0,.25,.5,.75,1],
    xlabel:'hours of study',ylabel:'p(pass)',label:'hours of study against pass or fail, with the fitted probability'});
  let d='';for(let i=0;i<=200;i++){const v=10*i/200;d+=(i?'L':'M')+api.sx(v).toFixed(1)+' '+api.sy(m.p([v])).toFixed(1);}
  el('path',{d,fill:'none',stroke:'var(--model)','stroke-width':3.5},stepG(api.layer('fit'),1));
  const gT=stepG(api.layer('anno'),2),gR=stepG(api.layer('heat'),2);
  x.forEach((v,i)=>el('circle',{cx:api.sx(v),cy:api.sy(lift(y[i])),r:8,fill:y[i]>0?'var(--pos)':'var(--mean)',stroke:'var(--surface)','stroke-width':2},api.layer('pts')));
  const inp=$('r-ft'),nP=y.filter(v=>v>0).length,nN=y.length-nP;
  const set=act('ft',v=>{inp.value=v;const t=v/100,xs=-(m.b+Math.log(1/t-1))/m.w[0];   // p(x) = t  ⇔  w x + b = log(t/(1−t))
    gT.textContent='';gR.textContent='';
    el('rect',{x:api.sx(xs),y:api.sy(1.06),width:api.sx(10)-api.sx(xs),height:api.sy(-.06)-api.sy(1.06),fill:'var(--pos)',opacity:.08},gR);
    el('line',{x1:api.sx(0),x2:api.sx(10),y1:api.sy(t),y2:api.sy(t),stroke:'var(--hi)','stroke-width':2,'stroke-dasharray':'6 5'},gT);
    el('line',{x1:api.sx(xs),x2:api.sx(xs),y1:api.sy(-.06),y2:api.sy(1.06),stroke:'var(--hi)','stroke-width':2,'stroke-dasharray':'6 5'},gT);
    label(gT,api.sx(xs)+8,api.sy(.5)+(t>.5?40:-14),`${xs.toFixed(1)} h`,{fill:'var(--hi)',upright:true});
    const tp=x.filter((v,i)=>y[i]>0&&m.p([v])>t).length,fp=x.filter((v,i)=>y[i]<0&&m.p([v])>t).length;   // positive when p > t, as on slide 3
    $('v-ft-t').textContent=t.toFixed(2);$('v-ft-tpr').textContent=`${tp}/${nP}`;$('v-ft-fpr').textContent=`${fp}/${nN}`;});
  inp.addEventListener('input',()=>set(+inp.value));
  hooks['s-fit']={step(s){const v={0:50,1:50,2:50,3:30}[s];if(v!==undefined)set(v);}};
  set(50);
}

/* ---------- two features: probability map, boundary, and the SVM's line ---------- */
{
  const {X,y}=SOFT,m=SOFT_LR,s=SOFT_SVM;
  const api=chart($('fig-2d'),{W:520,H:500,ml:62,fs:1.35,xmin:0,xmax:10,ymin:0,ymax:10,xticks:[0,2,4,6,8,10],yticks:[0,2,4,6,8,10],
    xlabel:'x₁',ylabel:'x₂',label:'logistic regression probability map, its boundary, and the SVM line'});
  api.svg.classList.add('sq');
  const N=50,h=10/N,cw=api.sx(h)-api.sx(0),ch=api.sy(0)-api.sy(h),gH=stepG(api.layer('heat'),1);gH.classList.add('noanim');
  for(let i=0;i<N;i++)for(let j=0;j<N;j++){const p=m.p([(i+.5)*h,(j+.5)*h]);
    el('rect',{x:api.sx(i*h),y:api.sy((j+1)*h),width:cw,height:ch,'shape-rendering':'crispEdges',fill:p>=.5?'var(--pos)':'var(--mean)',opacity:(.04+.3*Math.abs(p-.5)*2).toFixed(3)},gH);}   // no overlap: overlapping translucent cells show a grid
  // the line w·x + b = c across the plot (w₂ ≠ 0 for both models here)
  const line=(w,b,c,a,L)=>el('line',{x1:api.sx(0),y1:api.sy((c-b)/w[1]),x2:api.sx(10),y2:api.sy((c-b-10*w[0])/w[1]),...a},L);
  const g1=stepG(api.layer('fit'),1);
  line(m.w,m.b,0,{stroke:'var(--model)','stroke-width':3.5,'stroke-linecap':'round'},g1);
  line(s.w,s.b,0,{stroke:'var(--ink)','stroke-width':2.5,'stroke-dasharray':'8 6'},stepG(api.layer('fit'),2));
  X.forEach((p,i)=>el('circle',{cx:api.sx(p[0]),cy:api.sy(p[1]),r:8,fill:y[i]>0?'var(--pos)':'var(--mean)',stroke:'var(--surface)','stroke-width':2},api.layer('pts')));
}

/* ---------- the same model in 3D: height = p(green); drag to turn ---------- */
{
  const {X,y}=SOFT,m=SOFT_LR,W=520,H=500,S=34,ZS=6;   // ZS: height of p = 1 in x-units
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'the probability surface over the two features, between 0 and 1; green points at height 1, purple at 0'},$('fig-3d'));
  svg.classList.add('noanim');
  const gAx=el('g',{},svg),gLow=el('g',{},svg),gSurf=el('g',{},svg),gTop=el('g',{},svg);
  let yaw=-.8,pitch=.3;   // looking roughly along the boundary, so the sigmoid profile shows
  const proj=([px,py,pz])=>{const a=px-5,b2=py-5,c=pz*ZS,cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
    const Xr=a*cy-b2*sy,Yr=a*sy+b2*cy;return [W/2+30+Xr*S,H*.7-(c*cp-Yr*sp)*S,c*sp+Yr*cp];};   // +30: room for the p ticks
  const N=24,h=10/N;
  const seg=(L,p,q,a)=>{const A=proj(p),B=proj(q);return el('line',{x1:A[0],y1:A[1],x2:B[0],y2:B[1],...a},L);};
  function draw3(){
    for(const g of [gAx,gLow,gSurf,gTop])g.textContent='';
    // floor grid, box edges and axes
    for(let v=0;v<=10;v+=2.5){seg(gAx,[v,0,0],[v,10,0],{stroke:'var(--grid)','stroke-width':1.2});seg(gAx,[0,v,0],[10,v,0],{stroke:'var(--grid)','stroke-width':1.2});}
    const ax=(p,q,s,dx=6,dy=4)=>{seg(gAx,p,q,{stroke:'var(--line)','stroke-width':1.5});const B=proj(q);mtxt(gAx,B[0]+dx,B[1]+dy,s,{fill:'var(--muted)','font-size':16,'font-weight':700});};
    ax([0,0,0],[10.8,0,0],'x₁');ax([0,0,0],[0,10.8,0],'x₂');ax([0,0,0],[0,0,1.12],'p',-4,-8);
    for(const v of [0,.5,1]){const A=proj([0,0,v]);seg(gAx,[0,0,v],[-.25,0,v],{stroke:'var(--line)','stroke-width':1.5});
      mtxt(gAx,A[0]-12,A[1]+5,String(v),{fill:'var(--muted)','font-size':14,'text-anchor':'end'});}
    seg(gAx,[0,0,1],[10,0,1],{stroke:'var(--line)','stroke-width':1,'stroke-dasharray':'3 5',opacity:.7});
    seg(gAx,[0,0,1],[0,10,1],{stroke:'var(--line)','stroke-width':1,'stroke-dasharray':'3 5',opacity:.7});
    // purple points at p = 0 go under the surface, green points at p = 1 above it
    const dotAt=(L,p,yi)=>{const P=proj([p[0],p[1],yi>0?1:0]);el('circle',{cx:P[0],cy:P[1],r:7,fill:yi>0?'var(--pos)':'var(--mean)',stroke:'var(--surface)','stroke-width':1.5},L);};
    X.forEach((p,i)=>{if(y[i]<0)dotAt(gLow,p,y[i]);});
    // the surface as small quads, far ones first
    const quads=[];
    for(let i=0;i<N;i++)for(let j=0;j<N;j++){const cs=[[i,j],[i+1,j],[i+1,j+1],[i,j+1]].map(([a,b2])=>{const u=a*h,v=b2*h;return proj([u,v,m.p([u,v])]);});
      const pc=m.p([(i+.5)*h,(j+.5)*h]);quads.push({cs,pc,d:cs.reduce((s2,q)=>s2+q[2],0)/4});}
    quads.sort((A,B)=>B.d-A.d);
    for(const q of quads)el('polygon',{points:q.cs.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join(' '),fill:q.pc>=.5?'var(--pos)':'var(--mean)','fill-opacity':(.22+.5*Math.abs(q.pc-.5)*2).toFixed(3),stroke:'var(--surface)','stroke-width':.5,'stroke-opacity':.6},gSurf);
    // the p = 0.5 line: w·x + b = 0 inside the square, lifted to height 0.5
    const x2=x1=>-(m.b+m.w[0]*x1)/m.w[1],ends=[];
    for(const x1 of [0,10]){const v=x2(x1);if(v>=0&&v<=10)ends.push([x1,v]);}
    for(const v of [0,10]){const x1=-(m.b+m.w[1]*v)/m.w[0];if(x1>0&&x1<10)ends.push([x1,v]);}
    if(ends.length>=2)seg(gTop,[...ends[0],.5],[...ends[1],.5],{stroke:'var(--model)','stroke-width':3.5,'stroke-linecap':'round'});
    X.forEach((p,i)=>{if(y[i]>0)dotAt(gTop,p,y[i]);});
  }
  let drag=null;
  svg.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY,yaw,pitch];try{svg.setPointerCapture(e.pointerId);}catch(_){}});
  svg.addEventListener('pointermove',e=>{if(!drag)return;yaw=drag[2]+(e.clientX-drag[0])/150;pitch=clamp(drag[3]+(e.clientY-drag[1])/220,.05,1.3);draw3();});
  svg.addEventListener('pointerup',()=>{drag=null;});svg.addEventListener('pointercancel',()=>{drag=null;});
  draw3();
  // step 4 swaps the 2D figure for the 3D one; the text stays
  hooks['s-2d']={step(s){const on3=s>=4;$('fig-2d').classList.toggle('off',on3);$('fig-3d').classList.toggle('off',!on3);$('lg-svm').classList.toggle('off',on3);}};
}

/* ---------- one neuron, then a small network ---------- */
{
  const W=640,H=470,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'inputs x1, x2, x3 with weights w1, w2, w3 feed a sum plus b, then a sigmoid, giving p; below, a small network with a hidden layer'},$('fig-neuron'));
  const circ=(L,x,y,r,s,a={})=>{el('circle',{cx:x,cy:y,r,fill:'var(--surface)',stroke:'var(--ink)','stroke-width':1.8,...a},L);mtxt(L,x,y+6,s,{'text-anchor':'middle','font-size':17,fill:'var(--ink)'});};
  const arrow=(L,x1,y1,x2,y2,a={})=>{const t=Math.atan2(y2-y1,x2-x1),hd=9;
    el('line',{x1,y1,x2:x2-Math.cos(t)*hd*.6,y2:y2-Math.sin(t)*hd*.6,stroke:'var(--muted)','stroke-width':1.8,...a},L);
    el('polygon',{points:[[x2,y2],[x2-hd*Math.cos(t-.4),y2-hd*Math.sin(t-.4)],[x2-hd*Math.cos(t+.4),y2-hd*Math.sin(t+.4)]].map(v=>v.join(',')).join(' '),fill:a.stroke||'var(--muted)'},L);};
  // the neuron
  const L0=el('g',{},svg),ins=[[70,50],[70,120],[70,190]],S=[300,120],SG=[440,120];
  ins.forEach(([x,y],k)=>{circ(L0,x,y,24,`x${'₁₂₃'[k]}`);arrow(L0,x+24,y,S[0]-34,S[1]+(y-120)*.25);
    label(L0,(x+S[0])/2-4,(y+S[1])/2-8+(k-1)*6,`w${'₁₂₃'[k]}`,{fill:'var(--model)','text-anchor':'middle','font-size':15});});
  circ(L0,S[0],S[1],34,'Σ + b');
  arrow(L0,S[0]+34,S[1],SG[0]-30,SG[1]);
  el('rect',{x:SG[0]-30,y:SG[1]-30,width:60,height:60,rx:10,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},L0);
  mtxt(L0,SG[0],SG[1]+7,'σ',{'text-anchor':'middle','font-size':24,fill:'var(--model)'});
  arrow(L0,SG[0]+30,SG[1],560,SG[1]);
  mtxt(L0,575,SG[1]+6,'p',{'font-size':20,fill:'var(--ink)','font-weight':700});
  // a small network: 3 inputs → 4 hidden neurons → 1 output
  const L1=stepG(svg,1),xi=120,xh=320,xo=500,yi=[290,345,400],yh=[270,323,377,430].map(v=>v-15),yo=345;
  for(const a of yi)for(const b of yh)el('line',{x1:xi,y1:a,x2:xh,y2:b,stroke:'var(--line)','stroke-width':1.4},L1);
  for(const b of yh)el('line',{x1:xh,y1:b,x2:xo,y2:yo,stroke:'var(--line)','stroke-width':1.4},L1);
  yi.forEach((y,k)=>circ(L1,xi,y,16,'',{}));yh.forEach(y=>circ(L1,xh,y,16,'',{fill:'var(--model-soft)',stroke:'var(--model)'}));
  circ(L1,xo,yo,16,'',{fill:'var(--model-soft)',stroke:'var(--model)'});
  mtxt(L1,xi,yi[2]+38,'inputs',{'text-anchor':'middle','font-size':14,fill:'var(--muted)'});
  mtxt(L1,xh,yh[3]+38,'hidden neurons',{'text-anchor':'middle','font-size':14,fill:'var(--muted)'});
  mtxt(L1,xo,yo+40,'output',{'text-anchor':'middle','font-size':14,fill:'var(--muted)'});
}
