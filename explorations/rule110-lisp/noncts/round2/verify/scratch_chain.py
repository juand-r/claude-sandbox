import itertools, models
OPS2 = [("INC",0),("INC",1),("CH",(0,)),("CH",(1,)),("CH",(0,1)),("CH",(1,0))]
OPS3 = OPS2 + [("INC",2),("CH",(2,)),("CH",(0,2)),("CH",(2,0)),("CH",(1,2)),("CH",(2,1)),
               ("CH",(0,1,2)),("CH",(2,1,0)),("CH",(1,0,2)),("CH",(0,2,1)),("CH",(2,0,1)),("CH",(1,2,0))]
import sys
k = int(sys.argv[1]); L = int(sys.argv[2])
OPS = OPS2 if k == 2 else OPS3
nonper = 0; tot = 0
for prog in itertools.product(OPS, repeat=L):
    if prog[0] != OPS[0] and k==2: pass
    for regs in ([3]*k, [0]*k, [7,2,5][:k]):
        tot += 1
        _, pat = models.run_chain(list(prog), regs, 400)
        if models.eventual_period(pat) is None:
            _, pat = models.run_chain(list(prog), regs, 4000)
            if models.eventual_period(pat) is None:
                nonper += 1
                if nonper <= 5: print(prog, regs)
print(k, L, tot, nonper)
