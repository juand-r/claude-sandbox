/* ================= Class 1 figures ================= */

/* ---------- losses for a classifier: 0–1, hinge and log loss against y · f(x) ---------- */
{
  const api=chart($('fig-zeroone'),{W:640,H:420,ml:62,fs:1.35,xmin:-3,xmax:3,ymin:0,ymax:4,xticks:[-3,-2,-1,0,1,2,3],yticks:[0,1,2,3,4],
    xfmt:v=>String(v).replace('-','−'),xlabel:'y · f(x)',ylabel:'loss',label:'the 0–1 loss, the hinge loss and the log loss as functions of y times f(x)'});
  const path=f=>{let d='';for(let i=0;i<=300;i++){const z=-3+6*i/300;d+=(i?'L':'M')+api.sx(z).toFixed(1)+' '+api.sy(f(z)).toFixed(1);}return d;};
  const F=api.layer('fit'),A=api.layer('anno'),g1=stepG(A,1);
  el('line',{x1:api.sx(0),x2:api.sx(0),y1:api.sy(0),y2:api.sy(4),stroke:'var(--muted)','stroke-width':1.2,'stroke-dasharray':'4 5'},g1);
  mtxt(g1,api.sx(-1.5),api.sy(3.6),'mistake',{'text-anchor':'middle','font-size':16,fill:'var(--muted)'});
  mtxt(g1,api.sx(1.5),api.sy(3.6),'correct',{'text-anchor':'middle','font-size':16,fill:'var(--muted)'});
  el('path',{d:`M${api.sx(-3)} ${api.sy(1)}H${api.sx(0)}V${api.sy(0)}H${api.sx(3)}`,fill:'none',stroke:'var(--err)','stroke-width':3},stepG(F,2));
  el('path',{d:path(z=>Math.max(0,1-z)),fill:'none',stroke:'var(--model)','stroke-width':3.5},stepG(F,3));
  el('path',{d:path(z=>Math.log(1+Math.exp(-z))),fill:'none',stroke:'var(--hi)','stroke-width':3.5},stepG(F,4));
}

/* ---------- recap: one neuron ---------- */
neuronDiagram($('fig-recap'),{aria:'one neuron: inputs and a bias node with value 1, weights, a sum, a sigmoid, a probability'});

/* ---------- −log p(true class), with the 0–1 loss dotted ---------- */
{
  const api=chart($('fig-logp'),{W:640,H:420,ml:62,fs:1.35,xmin:0,xmax:1,ymin:0,ymax:5,xticks:[0,.25,.5,.75,1],yticks:[0,1,2,3,4,5],
    xfmt:v=>String(v),xlabel:'p(true class)',ylabel:'loss',label:'minus log of the probability of the true class, with the 0–1 loss dotted'});
  const pmin=Math.exp(-5);let d='';for(let i=0;i<=300;i++){const p=pmin+(1-pmin)*(i/300)**2;d+=(i?'L':'M')+api.sx(p).toFixed(1)+' '+api.sy(-Math.log(p)).toFixed(1);}
  el('path',{d,fill:'none',stroke:'var(--hi)','stroke-width':3.5},api.layer('fit'));
  const g1=api.layer('anno');
  for(const [p,dx,anchor] of [[.99,-12,'end'],[.5,12,'start'],[.01,14,'start']]){const l=-Math.log(p);
    el('circle',{cx:api.sx(p),cy:api.sy(l),r:6,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2},g1);
    label(g1,api.sx(p)+dx,api.sy(l)-12,l.toFixed(2),{'text-anchor':anchor,fill:'var(--ink)','font-size':15});}
  el('path',{d:`M${api.sx(0)} ${api.sy(1)}H${api.sx(.5)}V${api.sy(0)}H${api.sx(1)}`,fill:'none',stroke:'var(--err)','stroke-width':3,'stroke-dasharray':'3 6','stroke-linecap':'round'},stepG(api.layer('extra'),1));
}

/* ---------- from neuron to model: the perceptron, with what each part stands for ---------- */
{
  const N=neuronDiagram($('fig-model'),{W:640,H:380,act:'step',out:'±1',aria:'a perceptron: inputs, weights, a sum, a step, an output of plus or minus one, each labelled with the part of a neuron it stands for'});
  const t=(x,y,s)=>mtxt(N.svg,x,y,s,{'text-anchor':'middle','font-size':15,fill:'var(--muted)'});
  N.svg.setAttribute('viewBox','0 -34 640 414');
  t(70,4,'dendrites');t(200,4,'connection strengths');t(N.S[0],N.S[1]+62,'cell body');t(N.SG[0],N.SG[1]+62,'fires or not');t(580,N.SG[1]+40,'axon');
}

/* ---------- two classes: scores (f, 0), then a softmax ---------- */
{
  const W=520,H=330,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'three inputs feed two output scores, f and 0, followed by a softmax giving p1 and p2'},$('fig-two'));
  const L=el('g',{},svg),I=layerPos(3,70,60,270),O=layerPos(2,300,110,220);
  edges(L,I,[O[0]],{r:22});
  I.forEach((p,k)=>node(L,p[0],p[1],22,`x${'₁₂₃'[k]}`));
  node(L,O[0][0],O[0][1],26,'f',{stroke:'var(--model)'},{fill:'var(--model)'});
  node(L,O[1][0],O[1][1],26,'0',{stroke:'var(--muted)','stroke-dasharray':'4 4'},{fill:'var(--muted)'});
  const g1=stepG(L,1);
  el('rect',{x:360,y:95,width:80,height:140,rx:12,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},g1);
  mtxt(g1,400,172,'softmax',{'text-anchor':'middle','font-size':15,fill:'var(--model)'});
  for(const o of O)arrow(g1,o[0]+26,o[1],358,o[1]);
  mtxt(g1,452,O[0][1]+6,'p₁',{'font-size':18,fill:'var(--ink)'});
  mtxt(g1,452,O[1][1]+6,'p₂',{'font-size':18,fill:'var(--ink)'});
  mtxt(L,O[0][0],O[0][1]-38,'score of class 1',{'text-anchor':'middle','font-size':13,fill:'var(--muted)'});
  mtxt(L,O[1][0],O[1][1]+48,'score of class 2',{'text-anchor':'middle','font-size':13,fill:'var(--muted)'});
}

/* ---------- three classes: two inputs, four hidden neurons, three output scores, softmax; the example values at step 2 ---------- */
{
  const W=620,H=380,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'two inputs, a hidden layer of four neurons, three output scores, then a softmax'},$('fig-softmax'));
  const L=el('g',{},svg),I=layerPos(2,60,130,250),Hn=layerPos(4,200,50,330),O=layerPos(3,340,90,290);
  edges(L,I,Hn,{r:22});edges(L,Hn,O,{r:22});
  I.forEach((p,k)=>node(L,p[0],p[1],22,`x${'₁₂'[k]}`));
  Hn.forEach((p,j)=>node(L,p[0],p[1],22,`h${'₁₂₃₄'[j]}`));
  ['z₁','z₂','z₃'].forEach((s,k)=>node(L,O[k][0],O[k][1],24,s,{stroke:'var(--model)'},{fill:'var(--model)'}));
  const g=stepG(L,1);
  el('rect',{x:400,y:70,width:80,height:240,rx:12,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},g);
  mtxt(g,440,196,'softmax',{'text-anchor':'middle','font-size':15,fill:'var(--model)'});
  O.forEach((o,k)=>{arrow(g,o[0]+24,o[1],398,o[1]);mtxt(g,492,o[1]+6,['p₁','p₂','p₃'][k],{'font-size':18,fill:'var(--ink)'});});
  const g2=stepG(L,2),z=[2,1,-1],e=z.map(Math.exp),S=e.reduce((a,b)=>a+b,0);
  O.forEach((o,k)=>{mtxt(g2,o[0],o[1]-32,fmt(z[k],0),{'text-anchor':'middle','font-size':16,fill:'var(--model)','font-weight':700});
    mtxt(g2,528,o[1]+6,'= '+(e[k]/S).toFixed(2),{'font-size':18,fill:'var(--ink)'});});
  [['inputs',60],['hidden layer',200],['C = 3 classes',340]].forEach(([s,x])=>mtxt(L,x,370,s,{'text-anchor':'middle','font-size':13,fill:'var(--muted)'}));
}

/* ---------- cross-entropy: a one-hot label, the softmax probabilities, the loss for each possible true class ---------- */
{
  const W=520,H=360,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'one-hot label y equals 1, 0, 0; bars of the probabilities 0.71, 0.26, 0.04; the loss if each class were the true one: 0.35, 1.35, 3.35'},$('fig-ce'));
  const L=el('g',{},svg),X=[190,310,430],y0=210,hp=150,z=[2,1,-1],e=z.map(Math.exp),S=e.reduce((a,b)=>a+b,0),p=e.map(v=>v/S);
  const row=(g,y,s)=>mtxt(g,40,y,s,{'font-size':18,fill:'var(--muted)'});
  el('line',{x1:130,x2:490,y1:y0,y2:y0,stroke:'var(--line)','stroke-width':1.5},L);
  X.forEach((x,k)=>mtxt(L,x,y0+28,`class ${k+1}`,{'text-anchor':'middle','font-size':15,fill:'var(--muted)'}));
  row(L,290,'*y');
  X.forEach((x,k)=>{el('rect',{x:x-24,y:266,width:48,height:36,rx:6,fill:k?'var(--surface)':'var(--model-soft)',stroke:k?'var(--line)':'var(--model)','stroke-width':1.6},L);
    mtxt(L,x,290,k?'0':'1',{'text-anchor':'middle','font-size':18,fill:k?'var(--muted)':'var(--model)','font-weight':700});});
  const g2=stepG(L,2);row(g2,y0-60,'*p');
  X.forEach((x,k)=>{el('rect',{x:x-30,y:y0-hp*p[k],width:60,height:hp*p[k],fill:'var(--hi-soft)',stroke:'var(--hi)','stroke-width':1.6},g2);
    mtxt(g2,x,y0-hp*p[k]-10,p[k].toFixed(2),{'text-anchor':'middle','font-size':16,fill:'var(--ink)','font-weight':700});
    mtxt(g2,x,340,(-Math.log(p[k])).toFixed(2),{'text-anchor':'middle','font-size':17,fill:'var(--err)','font-weight':700});});
  row(g2,340,'−log p_k');
}

/* ---------- multilayer perceptron: the general picture ---------- */
{
  const W=740,H=330,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'a general multilayer perceptron: inputs x1 to xN, hidden layers h1 to h(L−1) with more layers in between, output scores z1 to zC, and a softmax'},$('fig-mlp'));
  const L=el('g',{},svg),X=[60,200,400,540],C=[layerPos(3,X[0],60,240),layerPos(4,X[1],40,260),layerPos(4,X[2],40,260),layerPos(3,X[3],60,240)];
  const col=['var(--model)','var(--line)','var(--mean)'];
  edges(L,C[0],C[1],{r:22,stroke:col[0],width:1.2});edges(L,C[2],C[3],{r:22,stroke:col[2],width:1.2});
  for(const a of C[1])el('line',{x1:a[0]+22,y1:a[1],x2:a[0]+62,y2:a[1],stroke:'var(--line)','stroke-width':1.4},L);
  for(const b of C[2])el('line',{x1:b[0]-62,y1:b[1],x2:b[0]-22,y2:b[1],stroke:'var(--line)','stroke-width':1.4},L);
  mtxt(L,300,160,'⋯',{'text-anchor':'middle','font-size':30,fill:'var(--muted)'});
  const dots=(x,y)=>mtxt(L,x,y,'⋮',{'text-anchor':'middle','font-size':22,fill:'var(--muted)'});
  ['x₁','x₂','x_N'].forEach((s,k)=>k===2?(dots(X[0],C[0][2][1]-32),node(L,...C[0][2],22,s)):node(L,...C[0][k],22,s));
  for(const l of [1,2])C[l].forEach(q=>node(L,q[0],q[1],22,''));
  ['z₁','z₂','z_C'].forEach((s,k)=>node(L,...C[3][k],22,s,{stroke:'var(--model)'},{fill:'var(--model)'}));
  softmaxBox(L,562,C[3].map(q=>q[1]),{w:76,names:['p₁','p₂','p_C'],weight:400});
  [['*x',X[0]],['*h^(1)',X[1]],['*h^(L−1)',X[2]],['output',X[3]]].forEach(([s,x])=>mtxt(L,x,312,s,{'text-anchor':'middle','font-size':17,fill:'var(--muted)'}));
}

/* ---------- activation functions: sigmoid, tanh, ReLU on the same axes ---------- */
for(const [id,name,f] of [['sig','sigmoid',sig],['tanh','tanh',Math.tanh],['relu','ReLU',a=>Math.max(0,a)]]){
  const api=chart($('fig-act-'+id),{W:300,H:300,ml:52,fs:1.6,xmin:-3,xmax:3,ymin:-1.2,ymax:3,xticks:[-3,0,3],yticks:[-1,0,1,2,3],
    xfmt:v=>String(v).replace('-','−'),yfmt:v=>String(v).replace('-','−'),xlabel:'a',ylabel:'φ(a)',label:'the '+name+' activation function'});
  el('line',{x1:api.sx(-3),x2:api.sx(3),y1:api.sy(0),y2:api.sy(0),stroke:'var(--muted)','stroke-width':1},api.layer('extra'));
  let d='';for(let i=0;i<=200;i++){const a=-3+6*i/200;d+=(i?'L':'M')+api.sx(a).toFixed(1)+' '+api.sy(f(a)).toFixed(1);}
  el('path',{d,fill:'none',stroke:'var(--model)','stroke-width':3.5},api.layer('fit'));
  mtxt(api.layer('anno'),api.sx(-2.8),api.sy(2.6),name,{'font-size':20,fill:'var(--ink)','font-weight':700});
}

/* ---------- the loss landscape: the cartoon in 3D and from above; gradient descent from a draggable start ---------- */
// the 3D view: an orthographic projection of the surface, drawn back to front (painter's algorithm)
// the starting view of the 3D surface (turn and tilt, in radians): both valleys and the gradient at A are visible
const LAND_AZ=1.45,LAND_EL=.6,EL_MIN=.2,EL_MAX=1.2,LAND_LEVELS=[.7,.8,.9,1,1.1,1.2,1.3,1.4,1.5];
function surface3d(host,{W=460,H=420,n=40,az=LAND_AZ,elev=LAND_EL}={}){
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'the same loss surface drawn in 3D: the height is the loss'},host);
  svg.classList.add('noanim');
  const G=[];for(let i=0;i<=n;i++){G.push([]);for(let j=0;j<=n;j++)G[i].push(cartoon([-3+6*i/n,-3+6*j/n]));}
  const lo=Math.min(...G.flat()),hi=Math.max(...G.flat()),zs=3.2/(hi-lo),L0=[-.5,.4,.77];   // light from the upper left, for shading
  const gS=el('g',{},svg),gT=el('g',{},svg),gO=el('g',{},svg);
  const view={az,el:elev,S:1,cx:0,cy:0};
  // world (θ₁, θ₂, height) → screen (u, v) and depth (larger is farther from the viewer)
  const raw=([a,b,z])=>{const c=Math.cos(view.az),s=Math.sin(view.az),x=c*a-s*b,y=s*a+c*b;
    return [x,-(z*Math.cos(view.el)+y*Math.sin(view.el)),y*Math.cos(view.el)-z*Math.sin(view.el)];};
  const P=p=>{const r=raw(p);return [view.cx+view.S*r[0],view.cy+view.S*r[1],r[2]];};
  const at=(a,b)=>[a,b,(cartoon([a,b])-lo)*zs];
  // the bounding box of the surface on screen, for the current view
  const box=()=>{const pts=[];for(const a of [-3,3])for(const b of [-3,3])for(const z of [0,(hi-lo)*zs])pts.push(raw([a,b,z]));
    const us=pts.map(p=>p[0]),vs=pts.map(p=>p[1]);return [Math.min(...us),Math.max(...us),Math.min(...vs),Math.max(...vs)];};
  // one scale for every view, so turning and tilting do not change the size; the picture is re-centred each time
  {const m=10,a0=view.az,e0=view.el;let S=1e9;
    for(let k=0;k<24;k++)for(const e of [EL_MIN,(EL_MIN+EL_MAX)/2,EL_MAX]){view.az=k*Math.PI/12;view.el=e;const b=box();S=Math.min(S,(W-2*m)/(b[1]-b[0]),(H-2*m)/(b[3]-b[2]));}
    view.az=a0;view.el=e0;view.S=S;}
  const centre=()=>{const b=box();view.cx=W/2-view.S*(b[0]+b[1])/2;view.cy=H/2-view.S*(b[2]+b[3])/2;};
  function draw(){centre();gS.textContent='';gT.textContent='';const Q=[];
    for(let i=0;i<n;i++)for(let j=0;j<n;j++){const a0=-3+6*i/n,a1=-3+6*(i+1)/n,b0=-3+6*j/n,b1=-3+6*(j+1)/n;
      const c=[[a0,b0,(G[i][j]-lo)*zs],[a1,b0,(G[i+1][j]-lo)*zs],[a1,b1,(G[i+1][j+1]-lo)*zs],[a0,b1,(G[i][j+1]-lo)*zs]].map(P);
      const v=(G[i][j]+G[i+1][j]+G[i][j+1]+G[i+1][j+1])/4,h=6/n;
      // the quad's normal from its slopes, and how much it faces the light
      const gx=((G[i+1][j]+G[i+1][j+1])-(G[i][j]+G[i][j+1]))/2*zs/h,gy=((G[i][j+1]+G[i+1][j+1])-(G[i][j]+G[i+1][j]))/2*zs/h,nn=Math.hypot(gx,gy,1);
      const lit=(-gx*L0[0]-gy*L0[1]+L0[2])/nn;
      // contour lines inside this cell (marching squares), drawn with the cell so hills hide them correctly
      const cv=[G[i][j],G[i+1][j],G[i+1][j+1],G[i][j+1]],cp=[[a0,b0],[a1,b0],[a1,b1],[a0,b1]],segs=[];
      for(const lev of LAND_LEVELS){const x=[];for(let k=0;k<4;k++){const u=cv[k]-lev,w=cv[(k+1)%4]-lev;
          if((u<0)!==(w<0)){const t=u/(u-w),A=cp[k],B=cp[(k+1)%4];x.push(P([A[0]+t*(B[0]-A[0]),A[1]+t*(B[1]-A[1]),(lev-lo)*zs]));}}
        for(let k=0;k+1<x.length;k+=2)segs.push(`M${x[k][0].toFixed(1)} ${x[k][1].toFixed(1)}L${x[k+1][0].toFixed(1)} ${x[k+1][1].toFixed(1)}`);}
      Q.push({c,segs,d:c.reduce((s,p)=>s+p[2],0)/4,t:Math.pow((v-lo)/(hi-lo),.5),sh:clamp(1-lit,0,1)});}
    Q.sort((p,q)=>q.d-p.d);
    for(const q of Q){const d='M'+q.c.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join('L')+'Z';
      el('path',{d,fill:'var(--surface)',stroke:'var(--surface)','stroke-width':.6,'stroke-linejoin':'round'},gS);
      el('path',{d,fill:'var(--model)','fill-opacity':(.1+.55*(1-q.t)).toFixed(3),stroke:'var(--model)','stroke-opacity':.25,'stroke-width':.5},gS);
      el('path',{d,fill:'#000','fill-opacity':(.4*q.sh).toFixed(3),stroke:'none'},gS);
      if(q.segs.length)el('path',{d:q.segs.join(''),fill:'none',stroke:'var(--model)','stroke-width':1.3,'stroke-opacity':.9},gS);}
    // axis names at the middle of two near edges
    const near=(p,q)=>P(p)[2]<P(q)[2]?p:q;
    const e1=near([0,-3],[0,3]),e2=near([-3,0],[3,0]);
    for(const [e,s] of [[e1,'θ₁'],[e2,'θ₂']]){const p=P(at(e[0]*1.18,e[1]*1.18));mtxt(gT,p[0],p[1]+22,s,{'text-anchor':'middle','font-size':17,fill:'var(--muted)'});}}
  draw();
  // the point of the surface drawn nearest to a screen position (for dragging on the surface)
  function pick(u,v){let best=null,bd=1e9;
    for(let i=0;i<=60;i++)for(let j=0;j<=60;j++){const a=-2.9+5.8*i/60,b=-2.9+5.8*j/60,p=P(at(a,b)),d=(p[0]-u)**2+(p[1]-v)**2-1e-3*p[2];if(d<bd){bd=d;best=[a,b];}}
    return best;}
  return {svg,gO,P,at,draw,view,pick,W,H};}

{
  const S3=surface3d($('fig-land3d')),api=cartoonPlot($('fig-land'),{H:420}),gA=api.layer('anno');
  const A=[1.9,-1.7],B=[-2.6,.6];   // these two starts end in different valleys (check_numbers.py)
  const bottom=p=>cartoonPath(p,{steps:3000}).pop(),mins=[bottom(CART.m1),bottom(CART.m2)];
  mins.forEach(m=>star(api,api.layer('pts'),m));
  // the overlay groups for each step, one set per view
  const G2=[0,1,2,3].map(k=>stepG(gA,k)),G3=[0,1,2,3].map(k=>stepG(S3.gO,k));
  const handle=el('circle',{r:9,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2.5},api.layer('hover'));handle.style.cursor='grab';
  const handle3=el('circle',{r:9,fill:'var(--hi)',stroke:'var(--surface)','stroke-width':2.5},S3.svg);handle3.style.cursor='grab';
  let start=A.slice();
  const path3=(L,path,color)=>{const pts=path.map(p=>S3.P(S3.at(p[0],p[1])));
    el('path',{d:pts.map((p,k)=>(k?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(''),fill:'none',stroke:color,'stroke-width':3,'stroke-linejoin':'round'},L);
    const e=pts[pts.length-1];el('circle',{cx:e[0],cy:e[1],r:7.5,fill:color,stroke:'var(--surface)','stroke-width':2},L);};
  function draw(){
    for(const g of [...G2,...G3])g.textContent='';
    mins.forEach(m=>{const p=S3.P(S3.at(...m));const g=el('g',{},G3[0]);star({sx:()=>p[0],sy:()=>p[1]},g,[0,0]);});
    handle.setAttribute('cx',api.sx(start[0]));handle.setAttribute('cy',api.sy(start[1]));
    const h3=S3.P(S3.at(...start));handle3.setAttribute('cx',h3[0]);handle3.setAttribute('cy',h3[1]);
    // the gradient points uphill; drawn with a fixed length so it stays visible on flat ground
    const g=cartoonGrad(start),sc=.9/Math.max(Math.hypot(g[0],g[1]),1e-9),q=[start[0]+g[0]*sc,start[1]+g[1]*sc];
    arrow(G2[1],api.sx(start[0]),api.sy(start[1]),api.sx(q[0]),api.sy(q[1]),{stroke:'var(--ink)','stroke-width':2.5});
    label(G2[1],api.sx(q[0])-10,api.sy(q[1])+(q[1]<start[1]?22:-10),'∇ℒ',{fill:'var(--ink)','font-size':15,'text-anchor':'end','font-weight':400});
    // in 3D: the same direction, following the surface up the slope
    const up=Array.from({length:11},(_,k)=>S3.P(S3.at(start[0]+g[0]*sc*1.4*k/10,start[1]+g[1]*sc*1.4*k/10)));
    el('path',{d:up.slice(0,10).map((p,k)=>(k?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(''),fill:'none',stroke:'var(--ink)','stroke-width':2.5},G3[1]);
    arrow(G3[1],up[9][0],up[9][1],up[10][0],up[10][1],{stroke:'var(--ink)','stroke-width':2.5});
    drawPath(api,G2[2],cartoonPath(start),{dots:false});path3(G3[2],cartoonPath(start),'var(--hi)');
    el('circle',{cx:api.sx(B[0]),cy:api.sy(B[1]),r:7,fill:'var(--err)',stroke:'var(--surface)','stroke-width':2},G2[3]);
    drawPath(api,G2[3],cartoonPath(B),{dots:false,color:'var(--err)'});
    const b3=S3.P(S3.at(...B));el('circle',{cx:b3[0],cy:b3[1],r:7,fill:'var(--err)',stroke:'var(--surface)','stroke-width':2},G3[3]);
    path3(G3[3],cartoonPath(B),'var(--err)');}
  const svgXY=(svg,ev,W,H)=>{const r=svg.getBoundingClientRect();return [(ev.clientX-r.left)/r.width*W,(ev.clientY-r.top)/r.height*H];};
  const toData=ev=>{const [px,py]=svgXY(api.svg,ev,api.W,api.H);
    const x=api.xmin+(px-api.sx(api.xmin))/(api.sx(api.xmax)-api.sx(api.xmin))*(api.xmax-api.xmin),y=api.ymin+(py-api.sy(api.ymin))/(api.sy(api.ymax)-api.sy(api.ymin))*(api.ymax-api.ymin);
    return [clamp(x,-2.9,2.9),clamp(y,-2.9,2.9)];};
  const setStart=act('land',p=>{start=p.slice();draw();});
  const turn=act('land3d',([az,el])=>{S3.view.az=az;S3.view.el=el;S3.draw();draw();});
  // dragging: the amber point in either view; the background of the 3D view turns it
  for(const [h,svg,map] of [[handle,api.svg,toData],[handle3,S3.svg,ev=>S3.pick(...svgXY(S3.svg,ev,S3.W,S3.H))]]){
    h.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();h.setPointerCapture(e.pointerId);h.style.cursor='grabbing';});
    h.addEventListener('pointermove',e=>{if(h.hasPointerCapture(e.pointerId))setStart(map(e));});
    h.addEventListener('pointerup',()=>{h.style.cursor='grab';});}
  let rot=null;S3.svg.style.cursor='grab';
  S3.svg.addEventListener('pointerdown',e=>{if(e.target===handle3)return;e.preventDefault();S3.svg.setPointerCapture(e.pointerId);S3.svg.style.cursor='grabbing';rot={x:e.clientX,y:e.clientY,az:S3.view.az,el:S3.view.el};});
  S3.svg.addEventListener('pointermove',e=>{if(rot)turn([rot.az+(e.clientX-rot.x)*.01,clamp(rot.el+(e.clientY-rot.y)*.01,EL_MIN,EL_MAX)]);});
  S3.svg.addEventListener('pointerup',()=>{rot=null;S3.svg.style.cursor='grab';});
  hooks['s-land']={step(){},enter(){start=A.slice();S3.view.az=LAND_AZ;S3.view.el=LAND_EL;S3.draw();draw();}};
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

/* ---------- XOR: the data only ---------- */
{
  const api=xorPlot($('fig-xor'),'XOR data: green points in two opposite corners, purple points in the other two');
  drawPts(api,api.layer('pts'),D.xor.X,D.xor.y);
}

/* ---------- combining neurons: copy the neuron into a hidden layer, then add one output neuron ---------- */
{
  const W=640,H=400,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'two inputs; one neuron copied into three hidden neurons; one output neuron with a sigmoid'},$('fig-hidden'));
  svg.classList.add('noanim');
  const I=layerPos(2,70,130,270),Hn=layerPos(3,270,70,330),O=[[450,200]];
  const gE=el('g',{},svg),gN=el('g',{},svg),center=[270,200];
  // each hidden neuron (with its two input edges) lives in a group that slides from the centre to its place
  const hid=Hn.map((p,j)=>{const g=el('g',{class:'hcopy'},gE),e=I.map(a=>el('line',{x1:a[0]+22,y1:a[1],x2:p[0]-24,y2:p[1],stroke:'var(--line)','stroke-width':1.6},g));
    const gn=el('g',{class:'hcopy'},gN);node(gn,p[0],p[1],24,`h${'₁₂₃'[j]}`,{stroke:'var(--model)'},{fill:'var(--model)'});return {g,gn,e,p};});
  I.forEach((p,k)=>node(gN,p[0],p[1],22,`x${'₁₂'[k]}`));
  const gO=el('g',{class:'fadein'},svg);edges(gO,Hn,O,{r:24});
  node(gO,450,200,22,'z');arrow(gO,472,200,500,200);
  el('rect',{x:500,y:172,width:56,height:56,rx:10,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},gO);
  mtxt(gO,528,207,'σ',{'text-anchor':'middle','font-size':24,fill:'var(--model)'});
  arrow(gO,556,200,586,200);mtxt(gO,594,206,'p',{'font-size':20,fill:'var(--ink)'});
  const gL=el('g',{class:'fadein'},svg);
  [['inputs',70],['hidden layer',270],['output',450]].forEach(([s,x])=>mtxt(gL,x,385,s,{'text-anchor':'middle','font-size':14,fill:'var(--muted)'}));
  hooks['s-hidden']={step(s){
    hid.forEach((h,j)=>{const show=s>=1||j===1,dx=s>=1?0:center[0]-h.p[0],dy=s>=1?0:center[1]-h.p[1];
      for(const g of [h.g,h.gn]){g.style.transform=`translate(${dx}px,${dy}px)`;g.style.opacity=show?1:0;}});
    gO.style.opacity=s>=2?1:0;gL.style.opacity=s>=3?1:0;}};
}

/* ---------- forward propagation: the network with its matrices ---------- */
{
  const W=640,H=460,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'network with input x, hidden layer h computed with W1 and b1, output scores z computed with W2 and b2, then a softmax; each bias drawn as a node with value 1'},$('fig-fwd'));
  const L=el('g',{},svg),I=layerPos(2,70,130,270),Hn=layerPos(3,270,70,330),O=layerPos(3,450,70,330),B0=[70,350],B1=[270,400];
  edges(L,I,Hn,{r:24,stroke:'var(--model)',width:1.4});edges(L,Hn,O,{r:24,stroke:'var(--mean)',width:1.4});
  edges(L,[B0],Hn,{r:20,stroke:'var(--model)',width:1.1}).forEach(e=>e.setAttribute('stroke-dasharray','4 4'));
  edges(L,[B1],O,{r:20,stroke:'var(--mean)',width:1.1}).forEach(e=>e.setAttribute('stroke-dasharray','4 4'));
  I.forEach((p,k)=>node(L,p[0],p[1],22,`x${'₁₂'[k]}`));Hn.forEach((p,j)=>node(L,p[0],p[1],24,`h${'₁₂₃'[j]}`));O.forEach((p,k)=>node(L,p[0],p[1],22,`z${'₁₂₃'[k]}`));softmaxBox(L,472,O.map(p=>p[1]),{weight:400});
  biasNode(L,...B0);biasNode(L,...B1);
  label(L,170,20,'*W^(1), *b^(1)',{'text-anchor':'middle',fill:'var(--model)','font-weight':400});label(L,360,20,'*W^(2), *b^(2)',{'text-anchor':'middle',fill:'var(--mean)','font-weight':400});
  const g1=stepG(L,1);
  mtxt(g1,70,445,'*x: N = 2',{'text-anchor':'middle','font-size':14,fill:'var(--muted)'});
  mtxt(g1,270,445,'*h: H = 3',{'text-anchor':'middle','font-size':14,fill:'var(--muted)'});
  mtxt(g1,450,445,'*z: C = 3',{'text-anchor':'middle','font-size':14,fill:'var(--muted)'});
  mtxt(g1,170,40,'3 × 2',{'text-anchor':'middle','font-size':13,fill:'var(--muted)'});
  mtxt(g1,360,40,'3 × 3',{'text-anchor':'middle','font-size':13,fill:'var(--muted)'});
}

/* ---------- deeper networks: two hidden layers, layer-l notation ---------- */
{
  const W=720,H=470,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'a network with input x, two hidden layers h1 and h2, and an output layer of three scores with a softmax; weights W1, W2, W3; each bias drawn as a node with value 1'},$('fig-layers'));
  const L=el('g',{},svg),X=[60,220,380,530],C=[layerPos(2,X[0],130,270),layerPos(3,X[1],70,330),layerPos(3,X[2],70,330),layerPos(3,X[3],70,330)];
  const col=['var(--model)','var(--hi)','var(--mean)'],B=[[X[0],350],[X[1],400],[X[2],400]];
  for(let l=0;l<3;l++){edges(L,C[l],C[l+1],{r:22,stroke:col[l],width:1.3});
    edges(L,[B[l]],C[l+1],{r:20,stroke:col[l],width:1}).forEach(e=>e.setAttribute('stroke-dasharray','4 4'));
    label(L,(X[l]+X[l+1])/2,50,`*W^(${l+1})`,{'text-anchor':'middle',fill:col[l],'font-weight':400});}
  C[0].forEach((p,k)=>node(L,p[0],p[1],22,`x${'₁₂'[k]}`));
  for(const l of [1,2])C[l].forEach(p=>node(L,p[0],p[1],22,''));
  C[3].forEach((p,k)=>node(L,p[0],p[1],22,`z${'₁₂₃'[k]}`));B.forEach(b=>biasNode(L,...b));
  const g1=stepG(L,1);softmaxBox(g1,552,C[3].map(p=>p[1]),{w:76,weight:400});
  [['*h^(0) = *x',X[0]],['*h^(1)',X[1]],['*h^(2)',X[2]],['output',X[3]]].forEach(([s,x])=>mtxt(L,x,455,s,{'text-anchor':'middle','font-size':15,fill:'var(--muted)'}));
}

/* ---------- XOR by hand: the 2-2-1 network, its weights shown step by step, and the table (values only at the last step) ---------- */
{
  const W=620,H=350,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'network with inputs x1 and x2, hidden units h1 (OR) and h2 (AND), and an output f with a sigmoid; input weights 20, hidden biases minus 10 and minus 30, output weights 20 and minus 20, output bias minus 10'},$('fig-handnet'));
  const L=el('g',{},svg),I=[[60,70],[60,230]],Hn=[[260,70],[260,230]],B0=[60,318],B1=[260,318],O=[440,150];
  // each weight: [from, to, value, position along the edge, step]
  const E=[[I[0],Hn[0],20,.5,1],[I[1],Hn[0],20,.28,1],[B0,Hn[0],-10,.8,1],[I[0],Hn[1],20,.28,2],[I[1],Hn[1],20,.5,2],[B0,Hn[1],-30,.6,2],
    [Hn[0],O,20,.5,3],[Hn[1],O,-20,.5,3],[B1,O,-10,.6,3]];
  for(const [a,b,v,t,k] of E){const bias=a===B0||a===B1,r0=bias?18:22,ang=Math.atan2(b[1]-a[1],b[0]-a[0]);
    const x1=a[0]+r0*Math.cos(ang),y1=a[1]+r0*Math.sin(ang),x2=b[0]-24*Math.cos(ang),y2=b[1]-24*Math.sin(ang);
    const ln=el('line',{x1,y1,x2,y2,stroke:'var(--line)','stroke-width':1.6},L);if(bias)ln.setAttribute('stroke-dasharray','4 4');
    label(stepG(L,k),x1+(x2-x1)*t,y1+(y2-y1)*t+6,fmt(v,0),{'text-anchor':'middle',fill:'var(--model)','font-size':17});}
  I.forEach((p,k)=>node(L,p[0],p[1],22,`x${'₁₂'[k]}`));biasNode(L,...B0);biasNode(L,...B1);
  Hn.forEach((p,j)=>node(L,p[0],p[1],24,`h${'₁₂'[j]}`,{stroke:'var(--model)'},{fill:'var(--model)'}));
  mtxt(stepG(L,1),260,32,'OR',{'text-anchor':'middle','font-size':15,fill:'var(--muted)','font-weight':700});
  mtxt(stepG(L,2),260,284,'AND',{'text-anchor':'middle','font-size':15,fill:'var(--muted)','font-weight':700});
  node(L,O[0],O[1],24,'f');arrow(L,464,150,492,150);
  el('rect',{x:492,y:122,width:56,height:56,rx:10,fill:'var(--model-soft)',stroke:'var(--model)','stroke-width':1.8},L);
  mtxt(L,520,157,'σ',{'text-anchor':'middle','font-size':24,fill:'var(--model)'});
  arrow(L,548,150,578,150);mtxt(L,586,156,'p',{'font-size':20,fill:'var(--ink)'});
  const tb=$('t-hand');
  for(const [a,b] of [[0,0],[0,1],[1,0],[1,1]]){const h1=sig(20*a+20*b-10),h2=sig(20*a+20*b-30),f=20*h1-20*h2-10;
    tb.insertAdjacentHTML('beforeend',`<tr><td>${a}</td><td>${b}</td><td data-step="4">${h1.toFixed(2)}</td><td data-step="4">${h2.toFixed(2)}</td><td data-step="4">${fmt(f,1)}</td><td data-step="4" class="yc">${sig(f).toFixed(2)}</td></tr>`);}
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
