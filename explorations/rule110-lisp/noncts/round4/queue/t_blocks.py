from q import *
m = Machine("NYYN", ["N"*8, "YNNNNN"], 20000, left_periods=2, right_periods=2)
bl = [(n,a,b) for n,a,b in m.blocks if n!='A']
print(bl[:200])
