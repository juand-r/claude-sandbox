import sys; sys.dont_write_bytecode=True
from pert import *
a=args("--K 1 --py 42,-14 --T 120 --wx 6 --wy 10 --phiL 0 --allow_empty".split())
bg = BG(a.N, a.T, -400, 300)
cnf,P,info=front_scene(a,bg)
sol=cnf.solve()
print(info)
x0,x1=info['x0'],info['x1']
lo,hi=x0-150,150
xs=range(lo,hi)
row=np.array([P.val(sol,0,x) if (0,x) in P.cells else P.init_const(x) for x in xs],np.uint8)
h=simulate(row,a.T)
bad=0
for (t,x),v in P.cells.items():
    if h[t,x-lo]!=sol.val(v): bad+=1
print('mismatch vars',bad,'of',len(P.cells))
# check outside-window constants
bad2=0
for t in range(1,a.T+1):
    L,R=P.bounds[t]
    for x in range(L-30,L):
        if h[t,x-lo]!=ether_bit(a.phiL,t,x): bad2+=1
    for x in range(R,R+30):
        if h[t,x-lo]!=bg(t,x): bad2+=1
print('outside mismatches',bad2)
for t in (0,1,2,3,10,40,80,120): print(t,P.bounds.get(t))
