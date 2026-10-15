/* ================= Class 2 figures ================= */

/* ---------- a layered network picture; returns node positions and edge elements for highlighting ---------- */
// names: one array of node labels per layer; xs: the x position of each layer
function netDiagram(host,{names,xs,W=560,H=380,top=60,bot=320,r=24,aria='a neural network'}){
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':aria},host),gE=el('g',{},svg),gN=el('g',{},svg);
  const pos=names.map((n,l)=>layerPos(n.length,xs[l],n.length===1?(top+bot)/2:top+(bot-top)*(n.length===2?.22:0),n.length===1?(top+bot)/2:bot-(bot-top)*(n.length===2?.22:0)));
  const E=[];for(let l=0;l+1<pos.length;l++){E.push(pos[l].map(a=>pos[l+1].map(b=>el('line',{x1:a[0]+r,y1:a[1],x2:b[0]-r,y2:b[1],stroke:'var(--line)','stroke-width':1.6},gE))));}
  pos.forEach((P,l)=>P.forEach((p,k)=>node(gN,p[0],p[1],r,names[l][k])));
  return {svg,pos,E,gE,gN,r,H};}
// draw a thick coloured copy of edge (layer l, from node a to node b) into group g
function hiEdge(N,g,l,a,b,color='var(--hi)'){const A=N.pos[l][a],B=N.pos[l+1][b];
  el('line',{x1:A[0]+N.r,y1:A[1],x2:B[0]-N.r,y2:B[1],stroke:color,'stroke-width':5,'stroke-linecap':'round'},g);}

/* ---------- recap: the 2-3-2 network; at step 1 every weight and input can be changed by hand ---------- */
{
  const N=netDiagram($('fig-recap'),{names:[['x₁','x₂'],['a₁','a₂','a₃'],['z₁','z₂']],xs:[90,290,460],W:770,H:432,top:60,bot:380,aria:'a network with two inputs, three hidden units and two outputs, followed by a softmax'});
  const SX=482,PX=632,PW=90;   // softmax arrows start at SX; the p bars start at PX and are PW long
  softmaxBox(N.svg,SX,N.pos[2].map(p=>p[1]),{weight:400,w:72});
  label(N.svg,190,40,'*W^(1), *b^(1)',{'text-anchor':'middle',fill:'var(--model)','font-weight':400});label(N.svg,375,40,'*W^(2), *b^(2)',{'text-anchor':'middle',fill:'var(--mean)','font-weight':400});
  mtxt(N.svg,385,424,'∂ℒ/∂w for every weight w ?',{'text-anchor':'middle','font-size':17,fill:'var(--hi)'});
  // the interactive part. Biases stay at 0 and are not drawn. Each weight is a vertical bar on its edge, dragged between −WMAX and WMAX
  const WMAX=3,TH=24,XMIN=-2,XMAX=2,XSTEP=.5;   // TH: half the height of a weight bar
  const START={W1:[[1.2,-.8],[-.6,1.5],[.9,.4]],W2:[[1.6,-1.1,.7],[-.9,1.3,-.5]],x:[1,.5]};   // W1[j][i]: input i to hidden j; W2[k][j]: hidden j to output k
  const copy=v=>JSON.parse(JSON.stringify(v));
  let S=copy(START),live=false;
  const G=stepG(N.svg,1);G.setAttribute('class','noanim');
  const toSvgY=e=>{const r=N.svg.getBoundingClientRect();return (e.clientY-r.top)/r.height*N.H;};
  const apply=act('recap-net',v=>{S=copy(v);draw();});
  // a drag follows the pointer anywhere over the figure until the button is released.
  // No pointer capture: the presenter window replays drags as synthetic events, which cannot be captured
  let dragging=null;
  N.svg.addEventListener('pointermove',e=>{if(dragging)dragging(toSvgY(e));});
  window.addEventListener('pointerup',()=>{dragging=null;});
  const drag=(hit,onY)=>{hit.style.cursor='ns-resize';
    hit.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();dragging=onY;onY(toSvgY(e));});};
  // where a weight's bar sits along its edge: the two columns of bars in each layer are kept apart
  const BAR_T=[[.62,.38],[.38,.62]];   // layer 1: by input i; layer 2: by output k
  const bars=[];   // {l,a,b,fill,knob}
  for(let l=0;l<2;l++)N.pos[l].forEach((A,a)=>N.pos[l+1].forEach((B,b)=>{
    const t=BAR_T[l][l?b:a],x=A[0]+N.r+t*(B[0]-A[0]-2*N.r),y=A[1]+t*(B[1]-A[1]);
    el('rect',{x:x-5,y:y-TH,width:10,height:2*TH,rx:3,fill:'var(--surface)',stroke:'var(--muted)','stroke-width':1},G);
    el('line',{x1:x-5,x2:x+5,y1:y,y2:y,stroke:'var(--muted)','stroke-width':1},G);
    const fill=el('rect',{x:x-4,width:8},G),knob=el('rect',{x:x-9,width:18,height:5,rx:2,fill:'var(--ink)'},G);
    const hit=el('rect',{x:x-11,y:y-TH-5,width:22,height:2*TH+10,fill:'transparent'},G);
    drag(hit,py=>{const v=copy(S),w=Math.round(clamp((y-py)/TH*WMAX,-WMAX,WMAX)*10)/10;
      if(l)v.W2[b][a]=w;else v.W1[b][a]=w;apply(v);});
    bars.push({l,a,b,x,y,fill,knob});}));
  // the inputs: a value with step buttons above and below it, left of each input node
  const inVals=N.pos[0].map((P,i)=>{const x=P[0]-54,y=P[1];
    const t=mtxt(G,x,y+6,'',{'text-anchor':'middle','font-size':17,fill:'var(--ink)'});
    for(const [d,dy] of [[1,-1],[-1,1]]){const yc=y+dy*24;
      el('path',{d:`M${x-7} ${yc+dy*-4}L${x+7} ${yc+dy*-4}L${x} ${yc+dy*5}Z`,fill:'var(--muted)'},G);
      const hit=el('rect',{x:x-14,y:yc-10,width:28,height:20,fill:'transparent'},G);hit.style.cursor='pointer';
      hit.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();});
      hit.addEventListener('click',e=>{e.stopPropagation();const v=copy(S);v.x[i]=clamp(v.x[i]+d*XSTEP,XMIN,XMAX);apply(v);});}
    return {t,x,y};});
  // the outputs: p₁ and p₂ as bars from 0 to 1
  const pBars=N.pos[2].map(P=>{const y=P[1];
    el('rect',{x:PX,y:y-8,width:PW,height:16,rx:3,fill:'none',stroke:'var(--muted)','stroke-width':1},G);
    return {fill:el('rect',{x:PX,y:y-8,height:16,rx:3,fill:'var(--model)'},G),t:mtxt(G,PX+PW+8,y+6,'',{'font-size':16,fill:'var(--ink)'})};});
  const yb=N.pos[2][1][1]+26;
  mtxt(G,PX,yb,'0',{'text-anchor':'middle','font-size':13,fill:'var(--muted)'});mtxt(G,PX+PW,yb,'1',{'text-anchor':'middle','font-size':13,fill:'var(--muted)'});
  function draw(){
    const w=(l,a,b)=>l?S.W2[b][a]:S.W1[b][a];
    for(const B of bars){const v=w(B.l,B.a,B.b),h=Math.abs(v)/WMAX*TH,ky=B.y-v/WMAX*TH;
      B.fill.setAttribute('y',v>=0?B.y-h:B.y);B.fill.setAttribute('height',h);B.fill.setAttribute('fill',v>=0?'var(--model)':'var(--err)');
      B.knob.setAttribute('y',ky-2.5);
      // the edge itself: colour by sign, thickness by size; back to plain at step 0
      const E=N.E[B.l][B.a][B.b];
      E.setAttribute('stroke',live?(v>=0?'var(--model)':'var(--err)'):'var(--line)');E.setAttribute('stroke-width',live?(.6+1.4*Math.abs(v)).toFixed(2):1.6);
      E.setAttribute('stroke-opacity',live?.55:1);}
    inVals.forEach((I,i)=>{I.t.replaceWith(I.t=mtxt(G,I.x,I.y+6,fmt(S.x[i],1),{'text-anchor':'middle','font-size':17,fill:'var(--ink)'}));});
    const {p}=mlpForward([S.W1,[0,0,0],S.W2,[0,0]],S.x);
    pBars.forEach((B,k)=>{B.fill.setAttribute('width',(p[k]*PW).toFixed(1));B.t.replaceWith(B.t=mtxt(G,PX+PW+8,N.pos[2][k][1]+6,fmt(p[k],2),{'font-size':16,fill:'var(--ink)'}));});}
  hooks['s-recap']={step(s){live=s>=1;draw();},enter(){S=copy(START);}};
  draw();
}

/* ---------- the chain rule: one path, then a branching one ---------- */
// an arrow between two node centres (radius r), with a derivative written above it and its value below
function link(L,A,B,r,top,bot,step){const t=Math.atan2(B[1]-A[1],B[0]-A[0]),c=Math.cos(t),s=Math.sin(t);
  arrow(L,A[0]+r*c,A[1]+r*s,B[0]-(r+2)*c,B[1]-(r+2)*s,{stroke:'var(--ink)'});
  // labels sit on either side of the arrow, along its normal (−sin, cos), so they never cross it
  const mx=(A[0]+B[0])/2,my=(A[1]+B[1])/2,nx=-s,ny=c,d=Math.abs(s)<.2?18:30;
  mtxt(L,mx-nx*d,my-ny*d+6,top,{'text-anchor':'middle','font-size':17});
  if(bot)mtxt(stepG(L,step),mx+nx*d,my+ny*d+6,bot,{'text-anchor':'middle','font-size':16,fill:'var(--model)'});}
{
  const svg=el('svg',{viewBox:'0 0 640 300',role:'img','aria-label':'the chain from x to u to y, with the derivative on each link'},$('fig-chain'));
  svg.setAttribute('fill','var(--ink)');
  const P=[[70,130],[320,130],[570,130]],r=30;
  P.forEach((q,k)=>node(svg,q[0],q[1],r,['x','u','y'][k]));
  link(svg,P[0],P[1],r,'d u/d x','3',1);link(svg,P[1],P[2],r,'d y/d u','2u',1);
  const g=stepG(svg,2);mtxt(g,P[0][0],P[0][1]+56,'x = 1',{'text-anchor':'middle','font-size':16,fill:'var(--model)'});
  mtxt(g,P[1][0],P[1][1]+56,'u = 4',{'text-anchor':'middle','font-size':16,fill:'var(--model)'});
  el('path',{d:'M70 230 v14 H570 v-14',fill:'none',stroke:'var(--hi)','stroke-width':2.5},g);
  mtxt(g,320,280,'d y/d x = 2u · 3 = 24',{'text-anchor':'middle','font-size':19,fill:'var(--hi)','font-weight':700});
}
{
  const svg=el('svg',{viewBox:'0 0 640 340',role:'img','aria-label':'x reaches y along two paths, through u1 and through u2'},$('fig-branch'));
  svg.setAttribute('fill','var(--ink)');
  const X=[80,170],U1=[320,70],U2=[320,270],Y=[560,170],r=30;
  [[X,'x'],[U1,'u₁'],[U2,'u₂'],[Y,'y']].forEach(([q,n])=>node(svg,q[0],q[1],r,n));
  link(svg,X,U1,r,'d u₁/d x','2x',1);link(svg,U1,Y,r,'∂y/∂u₁','u₂',1);
  link(svg,X,U2,r,'d u₂/d x','3',1);link(svg,U2,Y,r,'∂y/∂u₂','u₁',1);
  const g=stepG(svg,2);
  mtxt(g,U1[0],U1[1]-44,'path 1: u₂ · 2x = 24',{'text-anchor':'middle','font-size':16,fill:'var(--hi)','font-weight':700});
  mtxt(g,U2[0],U2[1]+56,'path 2: u₁ · 3 = 12',{'text-anchor':'middle','font-size':16,fill:'var(--hi)','font-weight':700});
}

/* ---------- the general rule: one unit j, what feeds it, and the units it feeds ---------- */
{
  const svg=el('svg',{viewBox:'0 0 640 400',role:'img','aria-label':'unit j of layer l receives the activation of unit i through w_ji and feeds the units k = 1, 2, 3 of layer l+1; their errors come back along the same connections'},$('fig-general'));
  svg.setAttribute('fill','var(--ink)');
  const I=[80,200],J=[290,200],K=[[480,90],[480,200],[480,310]],r=28;
  node(svg,I[0],I[1],r,'i');node(svg,J[0],J[1],r,'j');K.forEach((q,n)=>node(svg,q[0],q[1],r,String(n+1)));   // the units k = 1, 2, 3
  [[I[0],'layer l − 1'],[J[0],'layer l'],[K[0][0],'layer l + 1, k = 1, 2, 3']].forEach(([x,s])=>mtxt(svg,x,30,s,{'text-anchor':'middle','font-size':15,fill:'var(--muted)'}));
  mtxt(svg,I[0],I[1]-42,'aᵢ^(l−1)',{'text-anchor':'middle','font-size':16,fill:'var(--model)'});
  mtxt(svg,J[0],J[1]+74,'zⱼ^(l) → aⱼ^(l)',{'text-anchor':'middle','font-size':16,fill:'var(--model)'});
  arrow(svg,I[0]+r,I[1],J[0]-r-2,J[1],{stroke:'var(--ink)'});weightLabel(svg,(I[0]+J[0])/2,I[1]-20,'wⱼᵢ^(l)');
  K.forEach(q=>{const t=Math.atan2(q[1]-J[1],q[0]-J[0]);arrow(svg,J[0]+r*Math.cos(t),J[1]+r*Math.sin(t),q[0]-(r+2)*Math.cos(t),q[1]-(r+2)*Math.sin(t),{stroke:'var(--ink)'});});
  // one weight per connection, written beside it (above the upper two, below the lowest)
  K.forEach((q,n)=>{const mx=(J[0]+q[0])/2,my=(J[1]+q[1])/2;
    mtxt(svg,mx-6,my+[-18,-12,30][n],'w'+'₁₂₃'[n]+'ⱼ^(l+1)',{'text-anchor':'middle','font-size':16});});
  // the units k feed further layers: short, light stubs toward layer l + 2
  const stubs=el('g',{opacity:.5},svg);
  K.forEach(q=>[-28,0,28].forEach(dy=>{const t=Math.atan2(dy,70);
    el('line',{x1:q[0]+r*Math.cos(t),y1:q[1]+r*Math.sin(t),x2:q[0]+r+62,y2:q[1]+dy*1.15,stroke:'var(--muted)','stroke-width':1.6,'stroke-dasharray':'3 4'},stubs);}));
  mtxt(stubs,K[1][0]+r+92,K[1][1]+6,'⋯',{'text-anchor':'middle','font-size':22,fill:'var(--muted)'});
  const g1=stepG(svg,1);mtxt(g1,(I[0]+J[0])/2,I[1]+40,'∂ℒ/∂zⱼ^(l) · aᵢ^(l−1)',{'text-anchor':'middle','font-size':16,fill:'var(--hi)','font-weight':700});
  const g=stepG(svg,2);
  K.forEach((q,n)=>mtxt(g,q[0]+8,q[1]-36,'∂ℒ/∂z'+'₁₂₃'[n]+'^(l+1)',{'text-anchor':'middle','font-size':15,fill:'var(--err)'}));
  arrow(g,450,370,330,370,{stroke:'var(--err)','stroke-width':2.5});
  mtxt(g,390,358,'errors come back',{'text-anchor':'middle','font-size':14,fill:'var(--err)'});
}

/* ---------- the worked example: a 2-2-1 network with its weights on the connections ---------- */
// Same numbers as the slides and check_numbers.py. Values are rounded to 3 decimals, as on the slides.
const EX={x:[2,1],W:[[-0.5,1],[0.5,-1]],b:[1,-0.5],v:[2,0.5],c:-1,h:['0.731','0.378'],z:'0.651'};
// the two versions of the output: regression (linear output ŷ = z, target 2) and a class (sigmoid output p, label 1)
const OUT={reg:{act:'',name:'ŷ',y:'y = 2',out:'0.651',L:'0.910'},cls:{act:'σ',name:'p',y:'y = 1',out:'0.657',L:'0.420'}};
// ŷ: an italic y with a hat (the KaTeX fonts have no precomposed ŷ)
function hatY(L,x,y,size){const t=mtxt(L,x,y,'y',{'text-anchor':'middle','font-size':size});
  txt(L,x+2,y-size*0.36,'^',{'text-anchor':'middle','font-size':(size*1.2).toFixed(1),'font-family':'KaTeX_Main'});return t;}
const EXN={names:[['x₁','x₂'],['a₁^(1)','a₂^(1)'],['z^(2)']],xs:[90,290,480],W:770,H:420,top:60,bot:320};
const num=v=>String(v).replace('-','−');
// a point a fraction t along the edge from node a in layer l to node b in layer l + 1
const edgeAt=(N,l,a,b,t)=>{const A=N.pos[l][a],B=N.pos[l+1][b],r=N.r;return [A[0]+r+(B[0]-r-A[0]-r)*t,A[1]+(B[1]-A[1])*t];};
// a weight written on its connection, on a solid background so a highlighted edge does not strike through it
function weightLabel(L,x,y,s,a2={}){const g=el('g',{},L),w=11*s.length+10;
  el('rect',{x:x-w/2,y:y-13,width:w,height:26,rx:6,fill:'var(--surface)'},g);
  label(g,x,y+6,s,{'text-anchor':'middle','font-weight':400,'font-size':17,...a2});return g;}
const MUTED={'text-anchor':'end','font-size':16,fill:'var(--muted)'};
const VAL=(g,x,y,s,anchor='start')=>mtxt(g,x,y,s,{'text-anchor':anchor,'font-size':17,fill:'var(--model)'});
// a bias drawn as a weight from a node whose value is always 1 (as in class 1): the node sits below
// layer l, with a dashed connection to each node of layer l + 1, labelled at fraction t along it
function biasLinks(N,l,labels,ts){const B=[N.pos[l][0][0],N.H-34],rb=18;
  N.pos[l+1].forEach((q,k)=>{const ang=Math.atan2(q[1]-B[1],q[0]-B[0]),x1=B[0]+rb*Math.cos(ang),y1=B[1]+rb*Math.sin(ang),x2=q[0]-N.r*Math.cos(ang),y2=q[1]-N.r*Math.sin(ang);
    el('line',{x1,y1,x2,y2,stroke:'var(--line)','stroke-width':1.6,'stroke-dasharray':'5 4'},N.gE);
    weightLabel(N.svg,x1+(x2-x1)*ts[k],y1+(y2-y1)*ts[k],labels[k],{fill:'var(--muted)'});});   // grey, like the bias node
  biasNode(N.svg,...B,rb);return B;}
// the inputs, the first layer's weights and biases (the same in every version of the example);
// hvals(g) writes the hidden values into g
function firstLayer(N){const P=N.pos,r=N.r,W=(a,b,t,v)=>{const [x,y]=edgeAt(N,0,a,b,t);return weightLabel(N.svg,x,y,num(v));};
  const wl={w11:W(0,0,.5,EX.W[0][0]),w22:W(1,1,.5,EX.W[1][1]),w21:W(0,1,.27,EX.W[1][0]),w12:W(1,0,.27,EX.W[0][1])};
  biasLinks(N,0,EX.b.map(num),[.82,.62]);
  P[0].forEach((q,i)=>mtxt(N.svg,q[0]-r-10,q[1]+6,String(EX.x[i]),{'text-anchor':'end','font-size':18,fill:'var(--model)'}));
  const hvals=g=>{VAL(g,P[1][0][0]+8,P[1][0][1]-32,EX.h[0]);VAL(g,P[1][1][0]+8,P[1][1][1]+46,EX.h[1]);};
  return {wl,hvals};}
// draw the network; returns positions and helpers. path: null, 'v1' or 'w11' (highlighted from the start);
// kind: 'reg' or 'cls' (see OUT)
function exNet(id,{path=null,kind='reg',aria,still=false}){
  const O=OUT[kind];
  const N=netDiagram($(id),{...EXN,aria});
  // still: the same network as the slide before, so it is shown at once instead of being drawn in
  if(still)N.svg.classList.add('noanim');
  N.svg.setAttribute('fill','var(--ink)');   // default colour for labels, so they follow the theme
  const P=N.pos,r=N.r,zy=P[2][0][1],px=590,bx=690,bw=58;
  const at=(l,a,b,t)=>edgeAt(N,l,a,b,t);
  // the output: z → (σ) → ŷ or p → loss box
  const gA=el('g',{},N.svg);
  arrow(gA,P[2][0][0]+r,zy,px-14,zy,{stroke:'var(--ink)'});
  if(O.act)mtxt(gA,(P[2][0][0]+r+px-14)/2,zy-10,O.act,{'text-anchor':'middle','font-size':17});
  if(O.name==='ŷ')hatY(gA,px,zy+6,20);else mtxt(gA,px,zy+6,O.name,{'text-anchor':'middle','font-size':20});
  arrow(gA,px+14,zy,bx-2,zy,{stroke:'var(--ink)'});
  el('rect',{x:bx,y:zy-24,width:bw,height:48,rx:8,fill:'var(--surface)',stroke:'var(--err)','stroke-width':2},gA);
  mtxt(gA,bx+bw/2,zy+7,'ℒ',{'text-anchor':'middle','font-size':20,fill:'var(--err)'});
  mtxt(gA,bx+bw/2,zy-36,O.y,{'text-anchor':'middle','font-size':17});
  // highlighted path
  const gH=el('g',{},N.gE);
  if(path){hiEdge(N,gH,1,0,0);if(path==='w11')hiEdge(N,gH,0,0,0);
    for(const [x1,x2] of [[P[2][0][0]+r,px-14],[px+14,bx-2]])el('line',{x1,y1:zy,x2,y2:zy,stroke:'var(--hi)','stroke-width':5,'stroke-linecap':'round'},gH);}
  // weights on the connections, biases and inputs
  const F=firstLayer(N),V=(b,t,v)=>{const [x,y]=at(1,b,0,t);return weightLabel(N.svg,x,y,num(v));};
  const wl={...F.wl,v1:V(0,.45,EX.v[0]),v2:V(1,.45,EX.v[1])};
  biasLinks(N,1,[num(EX.c)],[.45]);
  // forward values, each in its own group so a slide can reveal them step by step
  const val=VAL;
  const fwd=k=>{const g=el('g',{},N.svg);
    if(k===1)F.hvals(g);
    if(k===2){val(g,P[2][0][0],zy-36,EX.z,'middle');val(g,px,zy-34,O.out,'middle');}
    if(k===3){val(g,bx+bw/2,zy+48,O.L,'middle');}
    return g;};
  return {N,P,zy,px,bx,bw,at,wl,fwd};
}
// a factor written next to the path, in the highlight colour
const fac=(g,x,y,s,a={})=>mtxt(g,x,y,s,{'text-anchor':'middle','font-size':17,fill:'var(--hi)','font-weight':700,...a});
/* ---------- the network as one function: the symbols on the 2-2-1 network ---------- */
{
  const N=netDiagram($('fig-formula'),{...EXN,aria:'the 2-2-1 network with each weight, bias and value named'});
  N.svg.setAttribute('fill','var(--ink)');
  const P=N.pos,r=N.r,zy=P[2][0][1],px=590,bx=690,bw=58;
  const W=(l,a,b,t,s)=>{const [x,y]=edgeAt(N,l,a,b,t);weightLabel(N.svg,x,y,s);};
  W(0,0,0,.5,'w₁₁^(1)');W(0,1,1,.5,'w₂₂^(1)');W(0,0,1,.27,'w₂₁^(1)');W(0,1,0,.27,'w₁₂^(1)');W(1,0,0,.45,'w₁₁^(2)');W(1,1,0,.45,'w₁₂^(2)');
  biasLinks(N,0,['b₁^(1)','b₂^(1)'],[.82,.62]);
  mtxt(N.svg,P[1][0][0]+8,P[1][0][1]-32,'a₁^(1) = σ(z₁^(1))',{'font-size':15,fill:'var(--model)'});
  biasLinks(N,1,['b^(2)'],[.45]);
  arrow(N.svg,P[2][0][0]+r,zy,px-14,zy,{stroke:'var(--ink)'});hatY(N.svg,px,zy+6,20);
  const g=stepG(N.svg,1);arrow(g,px+14,zy,bx-2,zy,{stroke:'var(--ink)'});
  el('rect',{x:bx,y:zy-24,width:bw,height:48,rx:8,fill:'var(--surface)',stroke:'var(--err)','stroke-width':2},g);
  mtxt(g,bx+bw/2,zy+7,'ℒ',{'text-anchor':'middle','font-size':20,fill:'var(--err)'});mtxt(g,bx+bw/2,zy-36,'y',{'text-anchor':'middle','font-size':17});
}

{
  const X=exNet('fig-example',{still:true,aria:'a network with inputs 2 and 1, two sigmoid hidden units and a linear output, weights on the connections'});
  [1,2,3].forEach(k=>X.fwd(k).setAttribute('data-step',k));
}
// the names of the highlighted weights, written beside their connections (slides 7 and 8)
const nameV1=X=>{const [x,y]=X.at(1,0,0,.28);fac(X.N.svg,x+14,y-16,'w₁₁^(2)',{'font-size':16});};
const nameW11=X=>{const [x,y]=X.at(0,0,0,.5);fac(X.N.svg,x,y-20,'w₁₁^(1)',{'font-size':16});};
{
  const X=exNet('fig-out',{still:true,path:'v1',aria:'the path from the output weight v1 through z and the prediction to the loss, highlighted'});
  [1,2,3].forEach(k=>X.fwd(k));nameV1(X);
  fac(stepG(X.N.svg,1),(X.px+14+X.bx)/2,X.zy+32,'−1.349');
  fac(stepG(X.N.svg,2),(X.P[2][0][0]+24+X.px-14)/2,X.zy+32,'1');
  const [x,y]=X.at(1,0,0,.45);fac(stepG(X.N.svg,3),x-26,y+30,'0.731');
  fac(stepG(X.N.svg,4),X.P[2][0][0]+24,X.zy-62,'∂ℒ/∂z^(2) = −1.349');
}
{
  const X=exNet('fig-deep',{still:true,path:'w11',aria:'the path from the hidden weight w11 through h1, z and the prediction to the loss, highlighted'});
  [1,2,3].forEach(k=>X.fwd(k));nameV1(X);nameW11(X);
  fac(X.N.svg,X.P[2][0][0]+24,X.zy-62,'∂ℒ/∂z^(2) = −1.349');   // carried over from slide 7, shown from the start
  const g=stepG(X.N.svg,2),[x,y]=X.at(1,0,0,.45);
  fac(g,x-26,y+30,'×2');fac(g,X.P[1][0][0],X.P[1][0][1]+48,'×0.1966');fac(g,X.P[0][0][0],X.P[0][0][1]-34,'×2');
}
{
  const X=exNet('fig-update',{still:true,aria:'the network with the new values of v1 and w11'});
  [1,2,3].forEach(k=>X.fwd(k));
  const [ax,ay]=X.at(0,0,0,.5),[bx_,by]=X.at(1,0,0,.45),g=el('g',{},X.N.svg);
  for(const [x,y,t] of [[ax,ay,'−0.394'],[bx_,by,'2.099']]){el('rect',{x:x-34,y:y-13,width:68,height:26,rx:6,fill:'var(--surface)'},g);
    label(g,x,y+6,t,{'text-anchor':'middle','font-size':17,fill:'var(--hi)'});}
  // the bullets with the arithmetic come first (step 1); the new values replace the old labels at step 2
  hooks['s-update']={step(s){g.style.display=s>=2?'':'none';X.wl.w11.style.display=X.wl.v1.style.display=s>=2?'none':'';}};
  g.style.display='none';
}
{
  const X=exNet('fig-class',{still:true,kind:'cls',aria:'the same network with a sigmoid output p, label 1 and the log loss'});
  [1,2].forEach(k=>X.fwd(k));X.fwd(3).setAttribute('data-step',1);
  fac(stepG(X.N.svg,2),X.P[2][0][0]+24,X.zy-62,'∂ℒ/∂z^(2) = −0.343');
}

/* ---------- the worked example with two outputs: softmax and cross-entropy ---------- */
// Same input and first layer; output 1 keeps v₁₁ = 2, v₁₂ = 0.5, c₁ = −1. Label: class 1, y = (1, 0).
const EX2={V:[[2,0.5],[1,0.5]],c:[-1,-1],z:['0.651','−0.080'],p:['0.675','0.325'],err:['−0.325','0.325']};
function exNet2(id,{aria,still=false}){
  const N=netDiagram($(id),{names:[['x₁','x₂'],['a₁^(1)','a₂^(1)'],['z₁^(2)','z₂^(2)']],xs:[80,265,440],W:770,H:430,top:60,bot:330,aria});
  N.svg.setAttribute('fill','var(--ink)');
  if(still)N.svg.classList.add('noanim');   // shown at once; step reveals still fade in
  const P=N.pos,r=N.r,F=firstLayer(N),bx=692,bw=58,ly=(P[2][0][1]+P[2][1][1])/2;
  softmaxBox(N.svg,P[2][0][0]+r,P[2].map(q=>q[1]),{x:516,w:76,weight:400});
  for(const q of P[2])el('line',{x1:642,y1:q[1],x2:bx-2,y2:ly,stroke:'var(--ink)','stroke-width':1.6},N.svg);
  el('rect',{x:bx,y:ly-24,width:bw,height:48,rx:8,fill:'var(--surface)',stroke:'var(--err)','stroke-width':2},N.svg);
  mtxt(N.svg,bx+bw/2,ly+7,'ℒ',{'text-anchor':'middle','font-size':20,fill:'var(--err)'});
  mtxt(N.svg,bx+bw/2,ly-36,'y = (1, 0)',{'text-anchor':'middle','font-size':16});
  const V=(j,k,t)=>{const [x,y]=edgeAt(N,1,j,k,t);return weightLabel(N.svg,x,y,num(EX2.V[k][j]));};
  V(0,0,.5);V(1,1,.5);V(0,1,.27);V(1,0,.27);
  biasLinks(N,1,['−1','−1'],[.78,.4]);
  return {N,P,F,ly,bx,bw};}
const z2vals=(X,g)=>{VAL(g,X.P[2][0][0]+8,X.P[2][0][1]-32,EX2.z[0]);VAL(g,X.P[2][1][0]+8,X.P[2][1][1]+46,EX2.z[1]);};
const p2vals=(X,g)=>{X.P[2].forEach((q,k)=>VAL(g,630,q[1]-24,EX2.p[k],'middle'));};
{
  const X=exNet2('fig-two',{still:true,aria:'the network with two outputs and a softmax'});
  X.F.hvals(X.N.svg);
  z2vals(X,stepG(X.N.svg,1));p2vals(X,stepG(X.N.svg,2));mtxt(stepG(X.N.svg,2),X.bx+X.bw/2,X.ly+48,'0.393',{'text-anchor':'middle','font-size':17,fill:'var(--model)'});
  const g=stepG(X.N.svg,3);fac(g,X.P[2][0][0],X.P[2][0][1]-60,'∂ℒ/∂z₁^(2) = −0.325');fac(g,X.P[2][1][0],X.P[2][1][1]+74,'∂ℒ/∂z₂^(2) = 0.325',{fill:'var(--err)'});
}
{
  const X=exNet2('fig-paths',{still:true,aria:'the hidden weight w11 reaches the loss along two paths, through both outputs'});
  // everything slide 11 ended with stays: the values, the probabilities, the loss and the output errors
  X.F.hvals(X.N.svg);z2vals(X,X.N.svg);p2vals(X,X.N.svg);
  mtxt(X.N.svg,X.bx+X.bw/2,X.ly+48,'0.393',{'text-anchor':'middle','font-size':17,fill:'var(--model)'});
  fac(X.N.svg,X.P[2][0][0],X.P[2][0][1]-60,'∂ℒ/∂z₁^(2) = −0.325');fac(X.N.svg,X.P[2][1][0],X.P[2][1][1]+74,'∂ℒ/∂z₂^(2) = 0.325',{fill:'var(--err)'});
  const gH=el('g',{},X.N.gE);hiEdge(X.N,gH,0,0,0);hiEdge(X.N,gH,1,0,0);hiEdge(X.N,gH,1,0,1,'var(--err)');
  {const [x,y]=edgeAt(X.N,0,0,0,.5);fac(X.N.svg,x,y-20,'w₁₁^(1)',{'font-size':16});}   // name the weight, as on slide 8
  const g1=stepG(X.N.svg,1),g2=stepG(X.N.svg,2);
  const [ax,ay]=edgeAt(X.N,1,0,0,.5);fac(g1,ax,ay-18,'×2');
  fac(g1,X.P[1][0][0],X.P[1][0][1]+48,'×0.1966');fac(g1,X.P[0][0][0],X.P[0][0][1]-34,'×2');
  const [bx_,by]=edgeAt(X.N,1,0,1,.27);fac(g2,bx_+30,by+12,'×1',{fill:'var(--err)'});
}

/* ---------- the recipe: forward, then backward ---------- */
{
  const N=netDiagram($('fig-recipe'),{names:[['x₁','x₂'],['a₁^(1)','a₂^(1)','a₃^(1)'],['a₁^(2)','a₂^(2)']],xs:[80,300,500],W:670,H:420,top:90,bot:330,aria:'forward pass from left to right, backward pass from right to left'});
  arrow(N.svg,60,40,520,40,{stroke:'var(--model)','stroke-width':3});mtxt(N.svg,290,30,'forward: every z and a',{'text-anchor':'middle','font-size':15,fill:'var(--model)'});
  // step 1: both outputs feed the loss, drawn once, between them
  const Lx=580,Ly=(N.pos[2][0][1]+N.pos[2][1][1])/2,gL=stepG(N.svg,1);
  N.pos[2].forEach(q=>arrow(gL,q[0]+N.r,q[1],Lx-14,Ly+(q[1]-Ly)*.15,{stroke:'var(--err)'}));
  mtxt(gL,Lx,Ly+7,'ℒ',{'text-anchor':'middle','font-size':20,fill:'var(--err)'});
  const g2=stepG(N.svg,2);arrow(g2,520,400,60,400,{stroke:'var(--err)','stroke-width':3});
  mtxt(g2,290,390,'backward: ∂ℒ/∂*z^(2), then ∂ℒ/∂*z^(1)',{'text-anchor':'middle','font-size':15,fill:'var(--err)'});
  mtxt(g2,N.pos[2][1][0]+22,N.pos[2][1][1]+48,'∂ℒ/∂*z^(2)',{'font-size':16,fill:'var(--err)'});   // the vector of output errors, under the lower output
  mtxt(g2,N.pos[1][2][0]+34,N.pos[1][2][1]+6,'∂ℒ/∂*z^(1)',{'font-size':16,fill:'var(--err)'});
}

/* ---------- learning-rate schedules ---------- */
const SCHED={epochs:100,step:30,tdecay:20};   // also in the notes
{
  const api=chart($('fig-lr'),{W:560,H:400,ml:70,fs:1.4,xmin:0,xmax:SCHED.epochs,ymin:0,ymax:1.1,xticks:[0,25,50,75,100],yticks:[0,.5,1],
    yfmt:v=>({0:'0',.5:'η₀/2',1:'η₀'})[v],xlabel:'epoch',ylabel:'learning rate',label:'three learning-rate schedules'});
  const g=stepG(api.layer('fit'),2),curve=(fn,c,name,ly)=>{let d='';for(let t=0;t<=SCHED.epochs;t+=.5)d+=(t?'L':'M')+api.sx(t).toFixed(1)+' '+api.sy(fn(t)).toFixed(1);
    el('path',{d,fill:'none',stroke:c,'stroke-width':3},g);const y=api.sy(ly);
    el('line',{x1:api.sx(62),x2:api.sx(70),y1:y-5,y2:y-5,stroke:c,'stroke-width':3},g);label(g,api.sx(72),y,name,{fill:c,'font-size':15});};
  curve(()=>1,'var(--ink)','constant',.88);
  curve(t=>Math.pow(.5,Math.floor(t/SCHED.step)),'var(--hi)','step decay',.78);
  curve(t=>1/(1+t/SCHED.tdecay),'var(--model)','1/t decay',.68);
}

/* ---------- optimizers on the raw-hours valley: replay with a slider ---------- */
const OPTC={gd:'var(--hi)',momentum:'var(--err)'};
function optFigure(id,names,tiles){
  const R=D.lr_raw,api=chart($('fig-'+id),{W:440,H:440,ml:70,fs:1.6,xmin:-.6,xmax:1.4,ymin:-6.5,ymax:3,xticks:[-.5,0,.5,1],yticks:[-6,-4,-2,0,2],
    xfmt:v=>String(v).replace('-','−'),yfmt:v=>String(v).replace('-','−'),xlabel:'w',ylabel:'b',label:'loss over w and b with optimizer paths'});
  landscape(api,api.layer('heat'),R.grid,[.5,.52,.56,.62,.7,.85,1.05,1.3,1.6,2]);star(api,api.layer('pts'),R.opt);
  const lapi=chart($('fig-'+id+'loss'),{W:440,H:440,ml:70,fs:1.6,xmin:0,xmax:150,ymin:.4,ymax:1.05,xticks:[0,50,100,150],yticks:[.4,.6,.8,1],yfmt:v=>v.toFixed(1),xlabel:'step',ylabel:'loss',label:'loss per step'});
  el('line',{x1:lapi.sx(0),x2:lapi.sx(150),y1:lapi.sy(.495),y2:lapi.sy(.495),stroke:'var(--ink)','stroke-width':1.2,'stroke-dasharray':'4 5'},lapi.layer('extra'));
  // one group per optimizer, so each can appear at its own step (names[k] = [optimizer, step])
  const G=names.map(([n,s])=>[n,stepG(api.layer('anno'),s),stepG(lapi.layer('fit'),s)]);
  const inp=$('r-'+id);let k=0,timer=null;
  function draw(){for(const [n,g,gl] of G){g.textContent='';gl.textContent='';const r=R.runs[n];
    drawPath(api,g,r.path,{upTo:k,dots:false,color:OPTC[n]});
    el('path',{d:r.loss.slice(0,k+1).map((v,i)=>(i?'L':'M')+lapi.sx(i).toFixed(1)+' '+lapi.sy(v).toFixed(1)).join(''),fill:'none',stroke:OPTC[n],'stroke-width':2.5},gl);}
    inp.value=k;for(const [t,n] of tiles){if(n==='k')$(t).textContent=k;else $(t).textContent=R.runs[n].loss[k].toFixed(3);}}
  const stop=()=>{clearInterval(timer);timer=null;};
  const set=act(id,v=>{k=v;draw();});
  const play=()=>{stop();set(0);timer=setInterval(()=>{if(k>=150){stop();return;}set(Math.min(150,k+2));},40);};
  inp.addEventListener('input',()=>{stop();set(+inp.value);});$('b-'+id+'-play').onclick=play;
  hooks['s-'+id]={step(){stop();set(150);},enter(){stop();}};
  set(150);
}
optFigure('mom',[['gd',0],['momentum',1]],[['v-mom-k','k'],['v-mom-gd','gd'],['v-mom-m','momentum']]);

/* ---------- local minima: restarts and momentum on the cartoon; the stalled XOR run ---------- */
const LOCAL={start:[-2.8,-2.8],eta:.25,beta:.9,
  restarts:[[-2.8,-2.8],[2.5,2.5],[-2.5,2.0],[2.2,-2.5],[0,-2.6],[-2.6,-.5],[.5,2.6],[2.7,.2]]};   // checked in check_numbers.py
{
  const api=cartoonPlot($('fig-local'),{H:440}),A=api.layer('anno'),g0=stepG(A,0),g1=stepG(A,1),g2=stepG(A,2);
  const dot=(g,p,c)=>el('circle',{cx:api.sx(p[0]),cy:api.sy(p[1]),r:6,fill:c,stroke:'var(--surface)','stroke-width':2},g);
  dot(g0,LOCAL.start,'var(--hi)');drawPath(api,g0,cartoonPath(LOCAL.start,{eta:LOCAL.eta}),{dots:false});
  const ends=LOCAL.restarts.slice(1).map(s=>{const P=cartoonPath(s,{eta:LOCAL.eta});dot(g1,s,'var(--muted)');drawPath(api,g1,P,{dots:false,color:'var(--muted)',width:1.8});return P[P.length-1];});
  ends.push(cartoonPath(LOCAL.start,{eta:LOCAL.eta}).pop());
  const best=ends.reduce((a,b)=>cartoon(b)<cartoon(a)?b:a);star(api,g1,best,{color:'var(--hi)'});
  drawPath(api,g2,cartoonPath(LOCAL.start,{eta:LOCAL.eta,beta:LOCAL.beta,steps:400}),{dots:false,color:'var(--err)'});
  const S=D.xor.runs.stuck,F=S.frames[S.frames.length-1],sapi=xorPlot($('fig-stuck'),'the XOR network that stalled: its decision map after 4,000 steps',{H:440,fs:1.6});
  drawMap(sapi,sapi.layer('heat'),xorP(F.P));drawPts(sapi,sapi.layer('pts'),D.xor.X,D.xor.y);
  $('v-st-l').textContent=F.loss.toFixed(3);$('v-st-a').textContent=Math.round(F.acc*100)+'%';
}

/* ---------- batch, stochastic, mini-batch ---------- */
{
  const S=D.sgd,api=chart($('fig-sgd'),{W:600,H:500,ml:70,fs:1.4,xmin:-2,xmax:2.5,ymin:-1.5,ymax:2.6,xticks:[-2,-1,0,1,2],yticks:[-1,0,1,2],
    xfmt:v=>String(v).replace('-','−'),yfmt:v=>String(v).replace('-','−'),xlabel:'w',ylabel:'b',label:'paths of batch, stochastic and mini-batch gradient descent'});
  landscape(api,api.layer('heat'),S.grid,[.5,.52,.56,.62,.7,.8,.95,1.15,1.4,1.7]);star(api,api.layer('pts'),D.lr_std.opt);
  const C={batch:'var(--hi)',sgd:'var(--err)',mini:'var(--model)'};
  let run='batch',k=0,timer=null;
  function draw(){const R=S.runs[run],L=api.clear('anno');drawPath(api,L,R.path,{upTo:k,color:C[run],dots:run!=='sgd',width:2.2});
    $('v-sgd-bs').textContent=R.batch_size;$('v-sgd-u').textContent=R.updates_per_epoch;$('v-sgd-l').textContent=R.loss[R.loss.length-1].toFixed(2);
    for(const n of ['batch','sgd','mini'])$('b-sgd-'+n).classList.toggle('sel',n===run);}
  const stop=()=>{clearInterval(timer);timer=null;};
  const play=()=>{stop();k=0;draw();const n=S.runs[run].path.length-1;timer=setInterval(()=>{if(k>=n){stop();return;}k++;draw();},Math.max(25,2400/n));};
  const set=act('sgd',([r,go])=>{stop();run=r;k=S.runs[r].path.length-1;draw();if(go)play();});
  for(const n of ['batch','sgd','mini'])$('b-sgd-'+n).onclick=()=>set([n,true]);
  $('b-sgd-play').onclick=()=>set([run,true]);
  hooks['s-sgd']={step(s){set([{0:'batch',1:'sgd',2:'mini',3:'mini'}[s],s<3]);},enter(){stop();}};
  set(['batch',false]);
}

const PATIENCE=400;   // epochs without improvement before stopping (checked in check_numbers.py)
/* ---------- when to stop: training and validation loss; the map at the best epoch and at the end ---------- */
{
  const O=D.overfit,E=O.epochs,best=O.best_epoch,ymax=Math.ceil(Math.max(...O.val_loss)*4)/4;
  const api=chart($('fig-stop'),{W:440,H:440,ml:70,mr:30,fs:1.6,xmin:0,xmax:E,ymin:0,ymax,xticks:[0,1000,2000,3000],yticks:[0,.5,1,1.5].filter(v=>v<=ymax),
    yfmt:v=>String(v),xlabel:'epoch',ylabel:'loss',label:'training and validation loss per epoch'});
  const line=(ys,c,g)=>{let d='';for(let i=0;i<ys.length;i+=3)d+=(i?'L':'M')+api.sx(i+1).toFixed(1)+' '+api.sy(ys[i]).toFixed(1);el('path',{d,fill:'none',stroke:c,'stroke-width':2.5},g);};
  const g1=stepG(api.layer('fit'),1),g2=stepG(api.layer('fit'),2),g3=stepG(api.layer('anno'),3);
  line(O.train_loss,'var(--hi)',g1);label(g1,api.sx(E)-4,api.sy(O.train_loss[E-1])-10,'training',{fill:'var(--hi)','text-anchor':'end','font-size':15});
  line(O.val_loss,'var(--err)',g2);label(g2,api.sx(E)-4,api.sy(O.val_loss[E-1])+24,'validation',{fill:'var(--err)','text-anchor':'end','font-size':15});
  el('line',{x1:api.sx(best),x2:api.sx(best),y1:api.sy(0),y2:api.sy(ymax),stroke:'var(--ink)','stroke-width':1.5,'stroke-dasharray':'5 5'},g3);
  el('circle',{cx:api.sx(best),cy:api.sy(O.val_loss[best-1]),r:7,fill:'var(--err)',stroke:'var(--surface)','stroke-width':2},g3);
  label(g3,api.sx(best)+8,api.sy(ymax)+20,`epoch ${best}`,{fill:'var(--ink)','font-size':15});
  // patience: stop once the validation loss has not improved for PATIENCE epochs
  let bestSoFar=Infinity,bestE=0,stopE=E;
  for(let e=1;e<=E;e++){if(O.val_loss[e-1]<bestSoFar){bestSoFar=O.val_loss[e-1];bestE=e;}if(e-bestE>=PATIENCE){stopE=e;break;}}
  const g4=stepG(api.layer('extra'),4);
  el('rect',{x:api.sx(bestE),y:api.sy(ymax),width:api.sx(stopE)-api.sx(bestE),height:api.sy(0)-api.sy(ymax),fill:'var(--hi)',opacity:.12},g4);
  el('line',{x1:api.sx(stopE),x2:api.sx(stopE),y1:api.sy(0),y2:api.sy(ymax),stroke:'var(--hi)','stroke-width':2,'stroke-dasharray':'6 4'},g4);
  label(g4,api.sx(stopE)+8,api.sy(ymax*.3),`stop at ${stopE}`,{fill:'var(--hi)','font-size':15});
  label(g4,api.sx(stopE)+8,api.sy(ymax*.3)+20,`patience ${PATIENCE}`,{fill:'var(--hi)','font-size':13});
  const X=O.train_X,mapi=chart($('fig-stopmap'),{W:440,H:440,ml:58,fs:1.6,xmin:-2,xmax:3,ymin:-1.5,ymax:2,xticks:[-2,0,2],yticks:[-1,0,1,2],
    xfmt:v=>String(v).replace('-','−'),yfmt:v=>String(v).replace('-','−'),xlabel:'x₁',ylabel:'x₂',label:'the network decision map'});
  drawPts(mapi,mapi.layer('pts'),X,O.train_y);
  const show=atBest=>{const P=atBest?O.P_best:O.P_end;drawMap(mapi,mapi.layer('heat'),x=>mlpForward(P,x).p[1],{N:50});
    $('v-stop-e').textContent=atBest?best:E;$('v-stop-tr').textContent=Math.round(100*(atBest?O.acc.train_best:O.acc.train_end))+'%';
    $('v-stop-va').textContent=Math.round(100*(atBest?O.acc.val_best:O.acc.val_end))+'%';};
  hooks['s-stop']={step(s){show(s>=3);}};
  show(false);
}

/* ---------- the family tree ---------- */
{
  const W=1100,H=440,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'family tree of neural network architectures'},$('fig-tree'));
  svg.classList.add('noanim');
  const box=(g,x,y,t,yr,c='var(--ink)')=>{const w=Math.max(150,t.length*10+40);el('rect',{x:x-w/2,y:y-30,width:w,height:60,rx:12,fill:'var(--surface)',stroke:c,'stroke-width':2},g);
    txt(g,x,y-3,t,{'text-anchor':'middle','font-size':17,'font-weight':700,fill:c});mtxt(g,x,y+20,yr,{'text-anchor':'middle','font-size':14,fill:'var(--muted)'});};
  const link=(g,a,b,c='var(--line)',dash='')=>el('path',{d:`M${a[0]} ${a[1]} C${(a[0]+b[0])/2} ${a[1]} ${(a[0]+b[0])/2} ${b[1]} ${b[0]} ${b[1]}`,fill:'none',stroke:c,'stroke-width':2.2,'stroke-dasharray':dash},g);
  const P={perc:[100,220],mlp:[300,220],cnn:[520,80],rnn:[520,300],lstm:[730,250],gru:[730,350],att:[920,300],tr:[1000,150]};
  const g0=el('g',{},svg),g1=stepG(svg,1),g2=stepG(svg,2);
  link(g0,[P.perc[0]+75,220],[P.mlp[0]-90,220]);
  link(g1,[P.mlp[0]+90,220],[P.cnn[0]-80,80]);link(g1,[P.mlp[0]+90,220],[P.rnn[0]-80,300]);
  link(g1,[P.rnn[0]+80,300],[P.lstm[0]-85,250]);link(g1,[P.rnn[0]+80,300],[P.gru[0]-85,350]);
  link(g2,[P.gru[0]+85,350],[P.att[0]-100,300]);link(g2,[P.att[0]+60,270],[P.tr[0]-30,182]);link(g2,[P.mlp[0]+90,210],[P.tr[0]-90,150],'var(--model)','6 6');
  box(g0,...P.perc,'Perceptron','1958');box(g0,...P.mlp,'MLP + backprop','1986','var(--model)');
  box(g1,...P.cnn,'CNN','1989');box(g1,...P.rnn,'RNN','1990');box(g1,...P.lstm,'LSTM','1997');box(g1,...P.gru,'GRU','2014');
  box(g2,...P.att,'Attention','2014');box(g2,...P.tr,'Transformer','2017','var(--hi)');
  mtxt(g2,650,150,'every Transformer layer contains an MLP',{'text-anchor':'middle','font-size':14,fill:'var(--model)'});
}

/* ---------- the training loop: four boxes and an arrow back ---------- */
{
  const W=1000,H=290,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'training loop: forward propagation, total error, gradients by backpropagation, update the weights, then back to forward propagation'},$('fig-loop'));
  const BX=[{t:'Forward propagation',m:'compute h and p',c:'var(--model)'},{t:'Total error',m:'the loss ℒ',c:'var(--err)'},
            {t:'Gradients',m:'backpropagation',c:'var(--hi)'},{t:'Update',m:'θ ← θ − η∇ℒ',c:'var(--mean)'}];
  const w=216,h=110,gap=(W-40-4*w)/3,y=40,xs=BX.map((_,k)=>20+k*(w+gap));
  BX.forEach((b,k)=>{const g=stepG(svg,k),x=xs[k];
    el('rect',{x,y,width:w,height:h,rx:14,fill:'var(--surface)',stroke:b.c,'stroke-width':2.5},g);
    txt(g,x+w/2,y+46,b.t,{'text-anchor':'middle','font-size':17,'font-weight':700,fill:b.c});
    mtxt(g,x+w/2,y+80,b.m,{'text-anchor':'middle','font-size':16,fill:'var(--ink)'});
    if(k)arrow(g,xs[k-1]+w+4,y+h/2,x-4,y+h/2,{stroke:'var(--ink)','stroke-width':2.5});});
  const g4=stepG(svg,4),yb=y+h+70;
  el('path',{d:`M${xs[3]+w/2} ${y+h+4} V${yb} H${xs[0]+w/2} V${y+h+14}`,fill:'none',stroke:'var(--ink)','stroke-width':2.5},g4);
  arrow(g4,xs[0]+w/2,y+h+30,xs[0]+w/2,y+h+4,{stroke:'var(--ink)','stroke-width':2.5});
  txt(g4,W/2,yb+30,'repeat with the new weights, until a stopping condition holds',{'text-anchor':'middle','font-size':17,fill:'var(--muted)'});
}

/* ---------- bonus: every path from one first-layer weight in a deeper network ---------- */
{
  const names=[['x₁','x₂'],['a₁^(1)','a₂^(1)','a₃^(1)'],['a₁^(2)','a₂^(2)','a₃^(2)'],['a₁^(3)','a₂^(3)','a₃^(3)'],['a₁^(4)','a₂^(4)']];
  const N=netDiagram($('fig-manypaths'),{names,xs:[60,220,380,540,700],W:830,H:390,top:60,bot:330,aria:'a network with three hidden layers; the paths from the first-layer weight w11 to the loss are highlighted layer by layer'});
  N.svg.setAttribute('fill','var(--ink)');N.svg.classList.add('noanim');
  const P=N.pos,r=N.r,Ly=(P[4][0][1]+P[4][1][1])/2,Lx=790;
  P[4].forEach(q=>arrow(N.svg,q[0]+r,q[1],Lx-14,Ly+(q[1]-Ly)*.15,{stroke:'var(--ink)'}));
  mtxt(N.svg,Lx,Ly+7,'ℒ',{'text-anchor':'middle','font-size':20,fill:'var(--err)'});
  // red copies of the edges on the paths, one layer per step
  const red=(g,l,a,b)=>{const A=P[l][a],B=P[l+1][b];el('line',{x1:A[0]+r,y1:A[1],x2:B[0]-r,y2:B[1],stroke:'var(--err)','stroke-width':3,'stroke-linecap':'round'},g);};
  const g1=stepG(N.gE,1),g2=stepG(N.gE,2),g3=stepG(N.gE,3),g4=stepG(N.gE,4);
  red(g1,0,0,0);
  [0,1,2].forEach(b=>red(g2,1,0,b));
  [0,1,2].forEach(a=>[0,1,2].forEach(b=>red(g3,2,a,b)));
  [0,1,2].forEach(a=>[0,1].forEach(b=>red(g4,3,a,b)));
  mtxt(stepG(N.svg,1),(P[0][0][0]+P[1][0][0])/2-14,(P[0][0][1]+P[1][0][1])/2-14,'w₁₁^(1)',{'text-anchor':'middle','font-size':16,fill:'var(--err)','font-weight':700});
  [[2,'3 paths'],[3,'9 paths'],[4,'18 paths']].forEach(([k,s])=>mtxt(stepG(N.svg,k),[0,0,300,460,620][k],372,s,{'text-anchor':'middle','font-size':15,fill:'var(--err)','font-weight':700}));
}
