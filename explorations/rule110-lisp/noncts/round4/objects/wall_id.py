"""Identify the two domains on either side of the left-moving wall seen in the
cone witness, and measure the wall's velocity exactly."""
import numpy as np, cone, sys
tile="1101011100"; bg=cone.Background(tile)
T=90; tau=0; x0=0
m=cone.ConeModel(bg,tau,x0,x0+T,T)
x,row0=m.extreme("left")
TT=1200; pad=2*TT+50; lo=m.a-pad
full=np.array([m.bgbit(0,y) for y in range(lo,m.b+pad)],np.uint8)
full[m.a-lo:m.b-lo]=row0
rows=cone.simulate_window(full,TT)
# all 50 phase rows of E-bg as reference strings at time t
def phases_at(t):
    out={}
    for tt in range(bg.tper):
        for s in range(bg.p):
            out[(tt,s)]=np.roll(bg.row_at(t+tt),s)
    return out
def classify(t, y0, w=40):
    r=rows[t]; xs0=lo+t
    seg=r[y0-xs0:y0-xs0+w]
    hits=[]
    for tt in range(bg.tper):
        rr=bg.row_at(tau+t+tt)
        for s in range(bg.p):
            ref=np.array([rr[(y-s)%bg.p] for y in range(y0,y0+w)])
            if np.array_equal(ref,seg): hits.append((tt,s))
    return hits
for t in (600,900,1200):
    c=x0+int(round(-4*t/15))
    # find the wall: leftmost deviation
    r=rows[t]; xs=np.arange(lo+t,lo+t+len(r))
    bgr=np.array([bg.bit(tau+t,y) for y in xs])
    dev=np.nonzero(r!=bgr)[0]
    left=xs[dev[0]]
    print(t,"wall leftmost dev x",left, "rod-frame", left-c, "left domain",classify(t,left-60), "right domain", classify(t,left+10))
