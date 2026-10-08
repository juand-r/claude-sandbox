/* ================= Class 1 figures ================= */

/* ---------- recap: one neuron ---------- */
neuronDiagram($('fig-recap'),{aria:'one neuron: inputs, weights, a sum plus b, a sigmoid, a probability'});

/* ---------- two classes with one-hot labels: a 3-input, 2-output picture, the second score fixed at 0 ---------- */
{
  const W=520,H=330,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'three inputs feed two output scores, f and 0, followed by a softmax giving p1 and p2'},$('fig-onehot'));
  const L=el('g',{},svg),I=layerPos(3,70,60,270),O=layerPos(2,300,110,220);
  edges(L,I,[O[0]],{r:22});
  I.forEach((p,k)=>node(L,p[0],p[1],22,`x${'₁₂₃'[k]}`));
  node(L,O[0][0],O[0][1],26,'f',{stroke:'var(--model)'},{fill:'var(--model)'});
  node(L,O[1][0],O[1][1],26,'0',{stroke:'var(--muted)','stroke-dasharray':'4 4'},{fill:'var(--muted)'});
  const g1=stepG(L,1);
  el('rect',{x:360,y:95,width:80,height:140,rx:12,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},g1);
  txt(g1,400,172,'softmax',{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:'var(--model)'});
  for(const o of O)arrow(g1,o[0]+26,o[1],358,o[1]);
  txt(g1,452,O[0][1]+6,'p₁',{'font-size':18,'font-family':MONO,fill:'var(--ink)','font-weight':700});
  txt(g1,452,O[1][1]+6,'p₂',{'font-size':18,'font-family':MONO,fill:'var(--ink)','font-weight':700});
  txt(L,O[0][0],O[0][1]-38,'score of class 1',{'text-anchor':'middle','font-size':13,fill:'var(--muted)','font-family':MONO});
  txt(L,O[1][0],O[1][1]+48,'score of class 2',{'text-anchor':'middle','font-size':13,fill:'var(--muted)','font-family':MONO});
}

/* ---------- C classes: N inputs, C outputs, softmax ---------- */
{
  const W=520,H=380,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'N inputs fully connected to C output scores, then a softmax'},$('fig-softmax'));
  const L=el('g',{},svg),I=layerPos(4,70,50,330),O=layerPos(3,290,90,290);
  edges(L,I,O,{r:22});
  ['x₁','x₂','⋮','x_N'].forEach((s,k)=>k===2?txt(L,I[k][0],I[k][1]+8,'⋮',{'text-anchor':'middle','font-size':26,fill:'var(--muted)'}):node(L,I[k][0],I[k][1],22,s==='x_N'?'xN':s));
  ['z₁','z₂','zC'].forEach((s,k)=>node(L,O[k][0],O[k][1],24,s,{stroke:'var(--model)'},{fill:'var(--model)'}));
  const g=stepG(L,1);
  el('rect',{x:350,y:70,width:80,height:240,rx:12,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},g);
  txt(g,390,196,'softmax',{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:'var(--model)'});
  O.forEach((o,k)=>{arrow(g,o[0]+24,o[1],348,o[1]);txt(g,442,o[1]+6,['p₁','p₂','pC'][k],{'font-size':18,'font-family':MONO,fill:'var(--ink)','font-weight':700});});
  txt(L,70,370,'N features',{'text-anchor':'middle','font-size':13,fill:'var(--muted)','font-family':MONO});
  txt(L,290,370,'C classes',{'text-anchor':'middle','font-size':13,fill:'var(--muted)','font-family':MONO});
}

/* ---------- the loss landscape: a cartoon with two valleys; gradient descent from a draggable start ---------- */
// ℒ(a, b) = 1.6 − 1.0 exp(−|θ − m₁|²/1.2) − 0.65 exp(−|θ − m₂|²/0.8) + 0.04|θ|², m₁ = (1.2, 0.9), m₂ = (−1.4, −1.1)
const CART={m1:[1.2,.9],s1:1.2,a1:1.0,m2:[-1.4,-1.1],s2:.8,a2:.65,c:.04};
function cartoon([a,b]){const q1=((a-CART.m1[0])**2+(b-CART.m1[1])**2)/CART.s1,q2=((a-CART.m2[0])**2+(b-CART.m2[1])**2)/CART.s2;
  return 1.6-CART.a1*Math.exp(-q1)-CART.a2*Math.exp(-q2)+CART.c*(a*a+b*b);}
function cartoonGrad([a,b]){const e1=CART.a1*Math.exp(-(((a-CART.m1[0])**2+(b-CART.m1[1])**2)/CART.s1)),e2=CART.a2*Math.exp(-(((a-CART.m2[0])**2+(b-CART.m2[1])**2)/CART.s2));
  return [e1*2*(a-CART.m1[0])/CART.s1+e2*2*(a-CART.m2[0])/CART.s2+2*CART.c*a, e1*2*(b-CART.m1[1])/CART.s1+e2*2*(b-CART.m2[1])/CART.s2+2*CART.c*b];}
function cartoonPath(t0,{eta=.25,steps=120}={}){const P=[t0.slice()];let t=t0.slice();
  for(let k=0;k<steps;k++){const g=cartoonGrad(t);t=[t[0]-eta*g[0],t[1]-eta*g[1]];P.push(t);}return P;}
window.__nn={cartoon,cartoonGrad,cartoonPath,CART};   // used by tests/export.js
function cartoonGrid(n=60){const w=[],b=[],L=[];for(let i=0;i<=n;i++){w.push(-3+6*i/n);b.push(-3+6*i/n);}
  for(const a of w)L.push(b.map(v=>cartoon([a,v])));return {w,b,L};}
function cartoonPlot(host,{H=440,label='a made-up loss surface with two valleys'}={}){
  const api=chart(host,{W:H,H,ml:58,fs:1.3,xmin:-3,xmax:3,ymin:-3,ymax:3,xticks:[-3,0,3],yticks:[-3,0,3],xfmt:v=>String(v).replace('-','−'),yfmt:v=>String(v).replace('-','−'),xlabel:'θ₁',ylabel:'θ₂',label});
  api.svg.classList.add('sq');landscape(api,api.layer('heat'),cartoonGrid(),[.7,.8,.9,1,1.1,1.2,1.3,1.4,1.5]);return api;}
{
  const api=cartoonPlot($('fig-land')),gA=api.layer('anno'),g1=stepG(gA,1),g2=stepG(gA,2),g3=stepG(gA,3);
  const A=[1.9,-1.7],B=[-2.6,.6];   // these two starts end in different valleys (check_numbers.py)
  const bottom=p=>cartoonPath(p,{steps:3000}).pop();
  star(api,api.layer('pts'),bottom(CART.m1));star(api,api.layer('pts'),bottom(CART.m2));
  const handle=el('circle',{r:9,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2.5},api.layer('hover'));handle.style.cursor='grab';
  let start=A.slice();
  function draw(){
    g1.textContent='';g2.textContent='';g3.textContent='';
    handle.setAttribute('cx',api.sx(start[0]));handle.setAttribute('cy',api.sy(start[1]));
    // the gradient points uphill; drawn with a fixed length so it stays visible on flat ground
    const g=cartoonGrad(start),sc=.9/Math.max(Math.hypot(g[0],g[1]),1e-9),q=[start[0]+g[0]*sc,start[1]+g[1]*sc];
    arrow(g1,api.sx(start[0]),api.sy(start[1]),api.sx(q[0]),api.sy(q[1]),{stroke:'var(--ink)','stroke-width':2.5});
    label(g1,api.sx(q[0])-10,api.sy(q[1])+(q[1]<start[1]?22:-10),'∇ℒ',{fill:'var(--ink)','font-size':15,'text-anchor':'end'});
    drawPath(api,g2,cartoonPath(start),{dots:false});
    el('circle',{cx:api.sx(B[0]),cy:api.sy(B[1]),r:7,fill:'var(--err)',stroke:'var(--surface)','stroke-width':2},g3);
    drawPath(api,g3,cartoonPath(B),{dots:false,color:'var(--err)'});}
  const toData=ev=>{const r=api.svg.getBoundingClientRect(),px=(ev.clientX-r.left)/r.width*api.W,py=(ev.clientY-r.top)/r.height*api.H;
    const x=api.xmin+(px-api.sx(api.xmin))/(api.sx(api.xmax)-api.sx(api.xmin))*(api.xmax-api.xmin),y=api.ymin+(py-api.sy(api.ymin))/(api.sy(api.ymax)-api.sy(api.ymin))*(api.ymax-api.ymin);
    return [clamp(x,-2.9,2.9),clamp(y,-2.9,2.9)];};
  const setStart=act('land',p=>{start=p.slice();draw();});
  handle.addEventListener('pointerdown',e=>{e.preventDefault();handle.setPointerCapture(e.pointerId);handle.style.cursor='grabbing';});
  handle.addEventListener('pointermove',e=>{if(handle.hasPointerCapture(e.pointerId))setStart(toData(e));});
  handle.addEventListener('pointerup',()=>{handle.style.cursor='grab';});
  hooks['s-land']={step(){},enter(){start=A.slice();draw();}};
  draw();
}

/* ---------- gradient descent on logistic regression (hours standardized): three learning rates ---------- */
{
  const S=D.lr_std,api=chart($('fig-gd'),{W:440,H:440,ml:70,fs:1.6,xmin:-2.5,xmax:8.5,ymin:-5,ymax:4.5,xticks:[-2,0,2,4,6,8],yticks:[-4,-2,0,2,4],
    xfmt:v=>String(v).replace('-','−'),yfmt:v=>String(v).replace('-','−'),xlabel:'w',ylabel:'b',label:'logistic regression loss over w and b, with a gradient descent path'});
  landscape(api,api.layer('heat'),S.grid,[.5,.55,.65,.8,1,1.3,1.7,2.2,2.8,3.5]);
  star(api,api.layer('pts'),S.opt);
  const lapi=chart($('fig-gdloss'),{W:440,H:440,ml:70,fs:1.6,xmin:0,xmax:40,ymin:0,ymax:2,xticks:[0,10,20,30,40],yticks:[0,.5,1,1.5,2],yfmt:v=>String(v),xlabel:'step',ylabel:'loss',label:'loss at each step'});
  el('line',{x1:lapi.sx(0),x2:lapi.sx(40),y1:lapi.sy(.495),y2:lapi.sy(.495),stroke:'var(--ink)','stroke-width':1.2,'stroke-dasharray':'4 5'},lapi.layer('extra'));
  let run='small',k=0,timer=null;
  function draw(){const R=S.runs[run],L=api.clear('anno'),LL=lapi.clear('fit');
    drawPath(api,L,R.path,{upTo:k});
    const ls=R.loss.slice(0,k+1);el('path',{d:ls.map((v,i)=>(i?'L':'M')+lapi.sx(i).toFixed(1)+' '+lapi.sy(Math.min(v,2)).toFixed(1)).join(''),fill:'none',stroke:'var(--hi)','stroke-width':2.5},LL);
    el('circle',{cx:lapi.sx(k),cy:lapi.sy(Math.min(R.loss[k],2)),r:6,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2},LL);
    $('v-gd-eta').textContent=R.eta;$('v-gd-k').textContent=k;$('v-gd-l').textContent=R.loss[k].toFixed(3);
    for(const n of ['small','good','large'])$('b-gd-'+n).classList.toggle('sel',n===run);}
  const stop=()=>{clearInterval(timer);timer=null;};
  const play=()=>{stop();k=0;draw();timer=setInterval(()=>{if(k>=40){stop();return;}k++;draw();},110);};
  const set=act('gd',([r,kk,go])=>{stop();run=r;k=kk;draw();if(go)play();});
  for(const n of ['small','good','large'])$('b-gd-'+n).onclick=()=>set([n,0,true]);
  $('b-gd-play').onclick=()=>set([run,0,true]);
  hooks['s-gd']={step(s){const r={0:'small',1:'small',2:'good',3:'large'}[s];set([r,s===0?0:40,false]);if(s>0)play();},enter(){stop();}};
  draw();
}

/* ---------- XOR: logistic regression's best fit ---------- */
{
  const X=D.xor.X,y=D.xor.y,api=xorPlot($('fig-xor'),'XOR data with the logistic regression fit');
  const g1=stepG(api.layer('heat'),1),lr=D.xor.lr;
  drawMap(api,g1,x=>sig(lr.w[0]*(x[0]-5)/2.5+lr.w[1]*(x[1]-5)/2.5+lr.b));
  drawPts(api,api.layer('pts'),X,y);
}

/* ---------- add a hidden layer: copy the neuron, then connect the outputs ---------- */
{
  const W=640,H=400,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'two inputs; one neuron copied into three hidden neurons; two outputs with a softmax'},$('fig-hidden'));
  svg.classList.add('noanim');
  const I=layerPos(2,70,130,270),Hn=layerPos(3,270,70,330),O=layerPos(2,450,140,260);
  const gE=el('g',{},svg),gN=el('g',{},svg),center=[270,200];
  // each hidden neuron (with its two input edges) lives in a group that slides from the centre to its place
  const hid=Hn.map((p,j)=>{const g=el('g',{class:'hcopy'},gE),e=I.map(a=>el('line',{x1:a[0]+22,y1:a[1],x2:p[0]-24,y2:p[1],stroke:'var(--line)','stroke-width':1.6},g));
    const gn=el('g',{class:'hcopy'},gN);node(gn,p[0],p[1],24,`h${'₁₂₃'[j]}`,{stroke:'var(--model)'},{fill:'var(--model)'});return {g,gn,e,p};});
  I.forEach((p,k)=>node(gN,p[0],p[1],22,`x${'₁₂'[k]}`));
  const gO=el('g',{class:'fadein'},svg);edges(gO,Hn,O,{r:24});
  O.forEach((p,k)=>node(gO,p[0],p[1],22,`z${'₁₂'[k]}`));
  softmaxBox(gO,472,O.map(p=>p[1]));
  const gL=el('g',{class:'fadein'},svg);
  [['inputs',70],['hidden layer',270],['outputs',450]].forEach(([s,x])=>txt(gL,x,385,s,{'text-anchor':'middle','font-size':14,fill:'var(--muted)','font-family':MONO}));
  hooks['s-hidden']={step(s){
    hid.forEach((h,j)=>{const show=s>=1||j===1,dx=s>=1?0:center[0]-h.p[0],dy=s>=1?0:center[1]-h.p[1];
      for(const g of [h.g,h.gn]){g.style.transform=`translate(${dx}px,${dy}px)`;g.style.opacity=show?1:0;}});
    gO.style.opacity=s>=2?1:0;gL.style.opacity=s>=3?1:0;}};
}

/* ---------- forward propagation: the network with its matrices ---------- */
{
  const W=640,H=400,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'network with input x, hidden layer h computed with W1 and b1, and output p computed with W2, b2 and softmax'},$('fig-fwd'));
  const L=el('g',{},svg),I=layerPos(2,70,130,270),Hn=layerPos(3,270,70,330),O=layerPos(2,450,140,260);
  edges(L,I,Hn,{r:24,stroke:'var(--model)',width:1.4});edges(L,Hn,O,{r:24,stroke:'var(--mean)',width:1.4});
  I.forEach((p,k)=>node(L,p[0],p[1],22,`x${'₁₂'[k]}`));Hn.forEach((p,j)=>node(L,p[0],p[1],24,`h${'₁₂₃'[j]}`));O.forEach((p,k)=>node(L,p[0],p[1],22,`z${'₁₂'[k]}`));softmaxBox(L,472,O.map(p=>p[1]));
  label(L,170,62,'W₁, b₁',{'text-anchor':'middle',fill:'var(--model)'});label(L,360,62,'W₂, b₂',{'text-anchor':'middle',fill:'var(--mean)'});
  const g1=stepG(L,1);
  txt(g1,70,385,'x: N = 2',{'text-anchor':'middle','font-size':14,fill:'var(--muted)','font-family':MONO});
  txt(g1,270,385,'h: H = 3',{'text-anchor':'middle','font-size':14,fill:'var(--muted)','font-family':MONO});
  txt(g1,450,385,'z: C = 2',{'text-anchor':'middle','font-size':14,fill:'var(--muted)','font-family':MONO});
  txt(g1,170,86,'3 × 2',{'text-anchor':'middle','font-size':13,fill:'var(--muted)','font-family':MONO});
  txt(g1,360,86,'2 × 3',{'text-anchor':'middle','font-size':13,fill:'var(--muted)','font-family':MONO});
}

/* ---------- XOR by hand ---------- */
{
  const tb=$('t-hand');
  for(const [a,b] of [[0,0],[0,1],[1,0],[1,1]]){const h1=sig(20*a+20*b-10),h2=sig(20*a+20*b-30),f=20*h1-20*h2-10;
    tb.insertAdjacentHTML('beforeend',`<tr><td>${a}</td><td>${b}</td><td data-step="1">${h1.toFixed(2)}</td><td data-step="2">${h2.toFixed(2)}</td><td data-step="3">${fmt(f,1)}</td><td data-step="3" class="yc">${sig(f).toFixed(2)}</td></tr>`);}
}

/* ---------- training on XOR: replay of the precomputed run ---------- */
{
  const R=D.xor.runs.ok,F=R.frames,X=D.xor.X,y=D.xor.y,api=xorPlot($('fig-train'),'the network decision map during training',{fs:1.6});
  const gMap=api.layer('heat');drawPts(api,api.layer('pts'),X,y);
  const lx=it=>Math.log10(it+1),lapi=chart($('fig-trainloss'),{W:430,H:430,ml:70,fs:1.6,xmin:0,xmax:lx(4000),ymin:0,ymax:.8,xticks:[0,1,2,3],yticks:[0,.2,.4,.6,.8],
    xfmt:v=>['1','10','100','1000'][v],yfmt:v=>v.toFixed(1),xlabel:'step (log scale)',ylabel:'loss',label:'training loss per step'});
  const inp=$('r-tr');inp.max=F.length-1;let k=0,timer=null;
  function draw(){const fr=F[k];drawMap(api,gMap,xorP(fr.P));
    const LL=lapi.clear('fit');el('path',{d:F.slice(0,k+1).map((f,i)=>(i?'L':'M')+lapi.sx(lx(f.it)).toFixed(1)+' '+lapi.sy(f.loss).toFixed(1)).join(''),fill:'none',stroke:'var(--err)','stroke-width':2.5},LL);
    el('circle',{cx:lapi.sx(lx(fr.it)),cy:lapi.sy(fr.loss),r:6,fill:'var(--err)',stroke:'var(--surface)','stroke-width':2},LL);
    inp.value=k;$('v-tr-k').textContent=fr.it;$('v-tr-l').textContent=fr.loss.toFixed(4);$('v-tr-a').textContent=Math.round(fr.acc*100)+'%';}
  const stop=()=>{clearInterval(timer);timer=null;};
  const set=act('train',v=>{k=v;draw();});
  const play=()=>{stop();set(0);timer=setInterval(()=>{if(k>=F.length-1){stop();return;}set(k+1);},120);};
  inp.addEventListener('input',()=>{stop();set(+inp.value);});
  $('b-tr-play').onclick=play;
  hooks['s-train']={step(s){stop();if(s===0)set(0);else play();},enter(){stop();}};
  set(0);
}
