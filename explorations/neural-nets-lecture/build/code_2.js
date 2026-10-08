/* ================= Class 2 figures ================= */

/* ---------- a layered network picture; returns node positions and edge elements for highlighting ---------- */
// names: one array of node labels per layer; xs: the x position of each layer
function netDiagram(host,{names,xs,W=560,H=380,top=60,bot=320,r=24,aria='a neural network'}){
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':aria},host),gE=el('g',{},svg),gN=el('g',{},svg);
  const pos=names.map((n,l)=>layerPos(n.length,xs[l],n.length===1?(top+bot)/2:top+(bot-top)*(n.length===2?.22:0),n.length===1?(top+bot)/2:bot-(bot-top)*(n.length===2?.22:0)));
  const E=[];for(let l=0;l+1<pos.length;l++){E.push(pos[l].map(a=>pos[l+1].map(b=>el('line',{x1:a[0]+r,y1:a[1],x2:b[0]-r,y2:b[1],stroke:'var(--line)','stroke-width':1.6},gE))));}
  pos.forEach((P,l)=>P.forEach((p,k)=>node(gN,p[0],p[1],r,names[l][k])));
  return {svg,pos,E,gE,gN,r};}
// draw a thick coloured copy of edge (layer l, from node a to node b) into group g
function hiEdge(N,g,l,a,b,color='var(--hi)'){const A=N.pos[l][a],B=N.pos[l+1][b];
  el('line',{x1:A[0]+N.r,y1:A[1],x2:B[0]-N.r,y2:B[1],stroke:color,'stroke-width':5,'stroke-linecap':'round'},g);}

/* ---------- recap: the 2-3-2 network ---------- */
{
  const N=netDiagram($('fig-recap'),{names:[['x₁','x₂'],['h₁','h₂','h₃'],['z₁','z₂']],xs:[70,270,450],W:640,H:400,top:70,bot:330,aria:'a network with two inputs, three hidden units and two outputs, followed by a softmax'});
  softmaxBox(N.svg,472,N.pos[2].map(p=>p[1]));
  label(N.svg,170,62,'W₁, b₁',{'text-anchor':'middle',fill:'var(--model)'});label(N.svg,360,62,'W₂, b₂',{'text-anchor':'middle',fill:'var(--mean)'});
  const g=stepG(N.svg,2);txt(g,320,385,'∂ℒ/∂w for every weight w ?',{'text-anchor':'middle','font-size':17,'font-family':MONO,fill:'var(--hi)','font-weight':700});
}

/* ---------- the chain rule: v → z → p → ℒ ---------- */
{
  const W=640,H=330,svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':'the chain from the weight v to the score z, the probability p and the loss'},$('fig-chain'));
  const X=[60,230,400,570],Y=110,names=['v','z','p','ℒ'];
  X.forEach((x,k)=>node(svg,x,Y,30,names[k],k===3?{stroke:'var(--err)'}:{},k===3?{fill:'var(--err)'}:{}));
  for(let k=0;k<3;k++)arrow(svg,X[k]+30,Y,X[k+1]-32,Y,{stroke:'var(--ink)'});
  const mid=k=>(X[k]+X[k+1])/2,t=(g,x,y,s,c,a={})=>txt(g,x,y,s,{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:c,...a});
  ['∂z/∂v','∂p/∂z','∂ℒ/∂p'].forEach((s,k)=>t(svg,mid(k),Y-18,s,'var(--muted)'));
  const g1=stepG(svg,1),g2=stepG(svg,2),g3=stepG(svg,3);
  t(g1,mid(0),Y+40,'h','var(--model)',{'font-weight':700});t(g2,mid(1),Y+40,'p(1 − p)','var(--model)',{'font-weight':700});
  t(g2,mid(2),Y+40,'−y/p','var(--model)',{'font-weight':700});t(g2,mid(2),Y+62,'+ (1−y)/(1−p)','var(--model)',{'font-weight':700});
  el('path',{d:`M${X[1]} ${Y+86} v14 H${X[3]} v-14`,fill:'none',stroke:'var(--hi)','stroke-width':2.5},g3);
  t(g3,(X[1]+X[3])/2,Y+134,'∂ℒ/∂z = p − y','var(--hi)',{'font-size':20,'font-weight':700});
}

/* ---------- output weights and one layer deeper: a 2-2-1 network with one path highlighted ---------- */
const SMALL={names:[['x₁','x₂'],['h₁','h₂'],['z']],xs:[80,300,500],W:600,H:360,top:60,bot:300};
{
  const N=netDiagram($('fig-out'),{...SMALL,aria:'the path from the output weight v1 to the loss'}),g=stepG(N.gE,1);
  hiEdge(N,g,1,0,0);label(N.svg,400,N.pos[1][0][1]+28,'v₁',{fill:'var(--hi)','text-anchor':'middle'});
  label(N.svg,400,N.pos[1][1][1]-14,'v₂',{fill:'var(--muted)','text-anchor':'middle'});
  const g2=stepG(N.svg,1);txt(g2,500,N.pos[2][0][1]+52,'p − y',{'text-anchor':'middle','font-size':16,'font-family':MONO,fill:'var(--err)','font-weight':700});
  txt(g2,300,N.pos[1][0][1]-36,'h₁',{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:'var(--hi)','font-weight':700});
}
{
  const N=netDiagram($('fig-deep'),{...SMALL,aria:'the path from the hidden weight w11 through h1 to the loss'}),g=stepG(N.gE,1);
  hiEdge(N,g,0,0,0);hiEdge(N,g,1,0,0);
  label(N.svg,190,N.pos[0][0][1]-8,'w₁₁',{fill:'var(--hi)','text-anchor':'middle'});label(N.svg,400,N.pos[1][0][1]+28,'v₁',{fill:'var(--hi)','text-anchor':'middle'});
  const g2=stepG(N.svg,1),f=(x,y,s,c='var(--err)')=>txt(g2,x,y,s,{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:c,'font-weight':700});
  f(500,N.pos[2][0][1]+52,'p − y');f(300,N.pos[1][0][1]-36,'h₁(1 − h₁)','var(--model)');f(80,N.pos[0][0][1]-36,'x₁','var(--model)');
}

/* ---------- several paths: a 2-2-2 network ---------- */
{
  const N=netDiagram($('fig-paths'),{names:[['x₁','x₂'],['h₁','h₂'],['z₁','z₂']],xs:[80,300,500],W:600,H:360,top:60,bot:300,aria:'a hidden weight reaches the loss along two paths, through both outputs'});
  hiEdge(N,N.gE,0,0,0);hiEdge(N,N.gE,1,0,0);hiEdge(N,N.gE,1,0,1,'var(--err)');
  label(N.svg,190,N.pos[0][0][1]-8,'w₁₁',{fill:'var(--hi)','text-anchor':'middle'});
  const g2=stepG(N.svg,2),f=(x,y,s,c)=>txt(g2,x,y,s,{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:c,'font-weight':700});
  f(500,N.pos[2][0][1]-36,'δ₂ = p − y','var(--err)');f(300,N.pos[1][0][1]-36,'δ₁','var(--err)');
  arrow(g2,470,N.pos[2][0][1]-40,340,N.pos[1][0][1]-40,{stroke:'var(--err)'});
}

/* ---------- the recipe: forward, then backward ---------- */
{
  const N=netDiagram($('fig-recipe'),{names:[['x₁','x₂'],['h₁','h₂','h₃'],['z₁','z₂']],xs:[80,300,500],W:600,H:420,top:90,bot:330,aria:'forward pass from left to right, backward pass from right to left'});
  arrow(N.svg,60,40,520,40,{stroke:'var(--model)','stroke-width':3});txt(N.svg,290,30,'forward: h, p',{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:'var(--model)','font-weight':700});
  const g2=stepG(N.svg,2);arrow(g2,520,400,60,400,{stroke:'var(--err)','stroke-width':3});
  txt(g2,290,390,'backward: δ₂, then δ₁',{'text-anchor':'middle','font-size':15,'font-family':MONO,fill:'var(--err)','font-weight':700});
  const g1=stepG(N.svg,1);txt(g1,N.pos[2][1][0]+34,N.pos[2][1][1]+6,'δ₂',{'font-size':16,'font-family':MONO,fill:'var(--err)','font-weight':700});
  txt(g2,N.pos[1][2][0]+34,N.pos[1][2][1]+6,'δ₁',{'font-size':16,'font-family':MONO,fill:'var(--err)','font-weight':700});
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
const OPTC={gd:'var(--hi)',momentum:'var(--err)',adam:'var(--model)'};
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
optFigure('adam',[['gd',0],['momentum',0],['adam',1]],[['v-adam-gd','gd'],['v-adam-m','momentum'],['v-adam-a','adam']]);

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
    txt(g,x,y-3,t,{'text-anchor':'middle','font-size':17,'font-weight':700,fill:c});txt(g,x,y+20,yr,{'text-anchor':'middle','font-size':14,'font-family':MONO,fill:'var(--muted)'});};
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
  txt(g2,650,150,'every Transformer layer contains an MLP',{'text-anchor':'middle','font-size':14,'font-family':MONO,fill:'var(--model)'});
}
